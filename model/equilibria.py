"""Equilibrium solvers.

We compute multiple solution concepts because each diagnoses a different
question:

  Nash bargaining (asymmetric)  — what's the efficient compromise weighted
                                  by leverage?
  Kalai-Smorodinsky             — what's the proportional-gain compromise?
                                  (rules out unfair Nash outcomes)
  Shapley values                — who marginally contributes value to the
                                  grand coalition?
  Core check                    — would any sub-coalition prefer to walk?

We solve over a discrete grid of deal vectors. The grid is coarse — each
issue gets a small number of candidate values — because:

  (a) the design space is conceptual not numeric;
  (b) actors' payoff functions are linear, so optima land at corners or
      mid-points of the grid;
  (c) we want every result to be inspectable.

If finer resolution is needed later, swap the grid for scipy.optimize.minimize
on the negated objective. The interface stays the same.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .data import Data, Issue
from .payoffs import (
    BATNA_DEAL,
    Deal,
    all_payoffs,
    batna_payoffs,
    payoff,
    summarize,
)


# ---------------------------------------------------------------------------
# Grid construction
# ---------------------------------------------------------------------------


def issue_grid(issue: Issue, n: int = 5) -> list[float]:
    """N evenly-spaced candidate values across the issue's range, inclusive."""
    if issue.width == 0:
        return [issue.lo]
    if n <= 1:
        return [issue.default]
    step = issue.width / (n - 1)
    return [issue.lo + i * step for i in range(n)]


def deal_grid(data: Data, n_per_issue: int = 4) -> Iterable[Deal]:
    """Cartesian product of per-issue grids. Pruned by skipping issues
    where no actor has a stake (the value doesn't matter for any payoff).
    """
    relevant_issues = [
        issue
        for issue in data.issues.values()
        if any(d != 0 for d in issue.direction_for.values())
    ]
    grids = {iss.id: issue_grid(iss, n_per_issue) for iss in relevant_issues}
    keys = list(grids.keys())
    for combo in itertools.product(*[grids[k] for k in keys]):
        yield dict(zip(keys, combo))


# ---------------------------------------------------------------------------
# Solution concepts
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Outcome:
    """The result of a solver: best deal + diagnostics."""
    concept: str
    deal: Deal
    payoffs: dict[str, float]
    batnas: dict[str, float]
    objective: float
    notes: str = ""


def _surplus_vector(payoffs: dict[str, float], batnas: dict[str, float]) -> dict[str, float]:
    return {a: payoffs[a] - batnas[a] for a in payoffs}


def nash_bargaining(
    data: Data,
    weights: dict[str, float] | None = None,
    n_per_issue: int = 2,
) -> Outcome:
    """Asymmetric Nash bargaining: maximise sum_i w_i * log(payoff_i - batna_i),
    over deals where every actor is strictly above BATNA.

    If `weights` is None, each actor's weight = its average importance weight
    across the issues where it has positions. This roughly proxies leverage
    by intensity-of-preference; it can be overridden.
    """
    batnas = batna_payoffs(data)
    if weights is None:
        weights = _default_weights(data)

    best_obj = -math.inf
    best_deal: Deal | None = None
    best_payoffs: dict[str, float] = {}

    for deal in deal_grid(data, n_per_issue):
        ps = all_payoffs(deal, data)
        surplus = _surplus_vector(ps, batnas)
        # require all actors strictly above BATNA
        if any(s <= 0 for s in surplus.values()):
            continue
        obj = sum(weights.get(a, 1.0) * math.log(s) for a, s in surplus.items())
        if obj > best_obj:
            best_obj = obj
            best_deal = deal
            best_payoffs = ps

    if best_deal is None:
        return Outcome(
            concept="nash_bargaining",
            deal={i.id: i.default for i in data.issues.values()},
            payoffs={},
            batnas=batnas,
            objective=-math.inf,
            notes="No deal exists where all actors strictly improve on BATNA at this grid resolution.",
        )

    return Outcome(
        concept="nash_bargaining",
        deal=best_deal,
        payoffs=best_payoffs,
        batnas=batnas,
        objective=best_obj,
    )


def kalai_smorodinsky(data: Data, n_per_issue: int = 2) -> Outcome:
    """Maximise the minimum proportional surplus (payoff - batna) / (ideal - batna)
    across actors. This guarantees a more equal distribution than Nash.
    Ideal point for each actor = the payoff they'd get if every issue went
    their way to the extreme.
    """
    batnas = batna_payoffs(data)
    ideals = _ideal_payoffs(data)

    best_obj = -math.inf
    best_deal: Deal | None = None
    best_payoffs: dict[str, float] = {}

    for deal in deal_grid(data, n_per_issue):
        ps = all_payoffs(deal, data)
        ratios = []
        all_above = True
        for actor in data.actors:
            denom = ideals[actor] - batnas[actor]
            if denom <= 0:
                continue
            surplus = ps[actor] - batnas[actor]
            if surplus <= 0:
                all_above = False
                break
            ratios.append(surplus / denom)
        if not all_above or not ratios:
            continue
        obj = min(ratios)
        if obj > best_obj:
            best_obj = obj
            best_deal = deal
            best_payoffs = ps

    if best_deal is None:
        return Outcome(
            concept="kalai_smorodinsky",
            deal={i.id: i.default for i in data.issues.values()},
            payoffs={},
            batnas=batnas,
            objective=-math.inf,
            notes="No deal exists where all actors strictly improve on BATNA at this grid resolution.",
        )

    return Outcome(
        concept="kalai_smorodinsky",
        deal=best_deal,
        payoffs=best_payoffs,
        batnas=batnas,
        objective=best_obj,
    )


def shapley_values(
    data: Data,
    deal: Deal | None = None,
    n_per_issue: int = 3,
) -> dict[str, float]:
    """Approximate Shapley values for each actor's marginal contribution to
    the *negotiation surplus* — i.e., the sum of (payoff - BATNA) over all
    actors in a coalition's best deal.

    Exact Shapley over 12 actors is 2^12 = 4096 coalitions, each requiring a
    grid search. That's heavy but tractable; we cache the per-coalition best.
    """
    actors = list(data.actors)
    n = len(actors)
    batnas = batna_payoffs(data)

    grids = list(deal_grid(data, n_per_issue))

    def coalition_value(members: tuple[str, ...]) -> float:
        if not members:
            return 0.0
        best = 0.0
        for d in grids:
            ps = all_payoffs(d, data)
            v = sum(max(0.0, ps[a] - batnas[a]) for a in members)
            if v > best:
                best = v
        return best

    coalition_cache: dict[frozenset[str], float] = {}
    def value(members_set: frozenset[str]) -> float:
        if members_set not in coalition_cache:
            coalition_cache[members_set] = coalition_value(tuple(members_set))
        return coalition_cache[members_set]

    shapley = {a: 0.0 for a in actors}
    factorials = [math.factorial(i) for i in range(n + 1)]
    full_set = frozenset(actors)
    for coalition_size in range(n):
        weight = factorials[coalition_size] * factorials[n - coalition_size - 1] / factorials[n]
        for coalition in itertools.combinations(actors, coalition_size):
            S = frozenset(coalition)
            v_S = value(S)
            for actor in actors:
                if actor in S:
                    continue
                v_S_plus = value(S | {actor})
                shapley[actor] += weight * (v_S_plus - v_S)

    return shapley


def in_core(deal: Deal, data: Data, n_per_issue: int = 3) -> tuple[bool, dict[frozenset[str], float]]:
    """Does any sub-coalition strictly prefer their best deal among themselves
    to what they get under the proposed deal?

    Heuristic core check: for each proper non-empty subset of actors, compute
    the coalition value (max sum of surplus they can get if they coordinate
    among themselves on issues they collectively care about) and compare to
    the sum of their actual surplus under the proposed deal. If any coalition
    strictly improves, the deal is not in the core.

    Returns (in_core, blocking_coalitions_with_surplus).
    """
    actors = list(data.actors)
    n = len(actors)
    batnas = batna_payoffs(data)
    ps = all_payoffs(deal, data)
    deal_surplus = {a: max(0.0, ps[a] - batnas[a]) for a in actors}

    grids = list(deal_grid(data, n_per_issue))

    blocking: dict[frozenset[str], float] = {}
    for k in range(1, n):
        for combo in itertools.combinations(actors, k):
            S = frozenset(combo)
            best_v = 0.0
            for d in grids:
                p2 = all_payoffs(d, data)
                v = sum(max(0.0, p2[a] - batnas[a]) for a in S)
                if v > best_v:
                    best_v = v
            their_total = sum(deal_surplus[a] for a in S)
            if best_v > their_total + 1e-6:
                blocking[S] = best_v - their_total

    return (len(blocking) == 0, blocking)


# ---------------------------------------------------------------------------
# Pareto utilities
# ---------------------------------------------------------------------------


def pareto_dominates(a_payoffs: dict[str, float], b_payoffs: dict[str, float]) -> bool:
    """True if a dominates b: a >= b on every actor and a > b on at least one."""
    actors = a_payoffs.keys()
    if not all(a_payoffs[x] >= b_payoffs[x] for x in actors):
        return False
    return any(a_payoffs[x] > b_payoffs[x] for x in actors)


def pareto_frontier(data: Data, n_per_issue: int = 3) -> list[tuple[Deal, dict[str, float]]]:
    """Return the (non-dominated) Pareto frontier of (deal, payoffs) pairs
    over the grid.
    """
    candidates: list[tuple[Deal, dict[str, float]]] = []
    for deal in deal_grid(data, n_per_issue):
        ps = all_payoffs(deal, data)
        candidates.append((deal, ps))

    frontier: list[tuple[Deal, dict[str, float]]] = []
    for i, (di, pi) in enumerate(candidates):
        dominated = False
        for j, (_, pj) in enumerate(candidates):
            if i == j:
                continue
            if pareto_dominates(pj, pi):
                dominated = True
                break
        if not dominated:
            frontier.append((di, pi))
    return frontier


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _default_weights(data: Data) -> dict[str, float]:
    """Each actor's weight = mean importance over issues where they have a position.
    Floor of 1.0 to avoid zero-weight actors being silently excluded from Nash.
    """
    out: dict[str, float] = {}
    for actor in data.actors:
        weights = [
            pos.weight
            for (a, _), pos in data.positions.items()
            if a == actor and pos.weight > 0
        ]
        out[actor] = max(1.0, sum(weights) / len(weights)) if weights else 1.0
    return out


def _ideal_payoffs(data: Data) -> dict[str, float]:
    """For each actor, the payoff they'd get if every issue's value was extreme
    in their direction. Sum of (weight) across their positions, since their
    own normalised contribution maxes out at 1.0 per issue.
    """
    out: dict[str, float] = {}
    for actor in data.actors:
        total = 0.0
        for (a, _), pos in data.positions.items():
            if a != actor:
                continue
            issue = data.issues.get(pos.issue)
            if issue is None:
                continue
            direction = issue.direction_for.get(actor, 0)
            if direction == 0 or pos.weight == 0:
                continue
            total += pos.weight  # max normalised contribution = 1.0
        out[actor] = total
    return out
