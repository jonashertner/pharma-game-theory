"""Actor payoff functions over the issue-vector deal space.

Design choice (per plan §5): keep payoffs *simple and inspectable* — linear
in normalised issue values weighted by the actor's importance weight,
multiplied by the direction sign (+1 if higher value is better for that
actor, -1 if lower is better). Red-line violations apply a hard penalty
that drops the payoff below the BATNA value by a large margin.

This is not a black-box ML model. It is a transparent specification of how
each actor's interests aggregate. The point is reproducibility and debug-
ability, not predictive accuracy at the third decimal.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data import Data, Issue, Position

# A "deal" is just a dict of issue_id -> value (in that issue's natural units).
Deal = dict[str, float]

# BATNA_DEAL is the disagreement-point deal: every issue at its BATNA value
# for the actor in question. Computed lazily per actor by `batna_deal_for`.

# The penalty applied when a deal violates an actor's red line on any issue.
# Set large enough that no realistic positive payoff can outweigh a red-line
# violation — but finite so optimisers don't blow up on it.
RED_LINE_PENALTY = -1000.0


def batna_deal_for(actor: str, data: Data) -> Deal:
    """The deal where every issue takes its BATNA value for this actor.

    Edge case: if an actor's own batna_value crosses their own red line, the
    raw BATNA payoff would be RED_LINE_PENALTY — making any deal trivially
    preferable. That distorts solver comparisons. We instead clip the BATNA
    just inside the red-line boundary, which is the principled
    interpretation: "the worst the actor will tolerate before walking is
    the red line itself, not beyond it."  Diagnostically we record actors
    with no usable BATNA in `actors_with_unusable_batna`.
    """
    out: Deal = {}
    for issue_id, issue in data.issues.items():
        pos = data.position(actor, issue_id)
        if pos is None:
            out[issue_id] = issue.default
            continue
        value = pos.batna_value
        if pos.red_line_value is not None:
            direction = issue.direction_for.get(actor, 0)
            # If the BATNA crosses this actor's own red line, clip to just
            # inside the red line (epsilon = 1% of the issue width).
            eps = 0.01 * issue.width if issue.width else 0
            if direction > 0 and value < pos.red_line_value:
                value = pos.red_line_value + eps
            elif direction < 0 and value > pos.red_line_value:
                value = pos.red_line_value - eps
            value = issue.clip(value)
        out[issue_id] = value
    return out


def actor_has_unusable_batna(actor: str, data: Data) -> tuple[bool, list[str]]:
    """Diagnostic: which issues have a BATNA-vs-red-line conflict for this actor?
    Returns (True, [issue_ids]) when the no-deal state crosses the actor's
    own red lines — meaning the actor literally cannot walk away.
    """
    conflicts: list[str] = []
    for issue_id, issue in data.issues.items():
        pos = data.position(actor, issue_id)
        if pos is None or pos.red_line_value is None:
            continue
        direction = issue.direction_for.get(actor, 0)
        if direction == 0:
            continue
        if direction > 0 and pos.batna_value < pos.red_line_value:
            conflicts.append(issue_id)
        elif direction < 0 and pos.batna_value > pos.red_line_value:
            conflicts.append(issue_id)
    return (len(conflicts) > 0, conflicts)


BATNA_DEAL = "BATNA_DEAL"  # sentinel for caller convenience


def _violates_red_line(actor: str, issue: Issue, value: float, pos: Position) -> bool:
    """Did the deal cross this actor's red line on this issue?

    A red line is a one-sided threshold defined by the position's direction
    (the issue's `direction_for[actor]`). If direction is +1, the red line
    is a floor (deal < red_line_value violates). If direction is -1, it is
    a ceiling (deal > red_line_value violates).
    """
    if pos.red_line_value is None:
        return False
    direction = issue.direction_for.get(actor, 0)
    if direction == 0:
        return False  # no preference -> no red line
    if direction > 0:
        return value < pos.red_line_value
    return value > pos.red_line_value


def payoff(actor: str, deal: Deal, data: Data) -> float:
    """Aggregate payoff for an actor under a candidate deal.

    Sum of (weight × direction × normalised_value) across issues where the
    actor has a stake. Red-line violations push the actor strictly below
    their BATNA.
    """
    total = 0.0
    red_line_hit = False

    for issue_id, value in deal.items():
        issue = data.issues.get(issue_id)
        if issue is None:
            continue
        pos = data.position(actor, issue_id)
        if pos is None:
            continue

        if _violates_red_line(actor, issue, value, pos):
            red_line_hit = True

        direction = issue.direction_for.get(actor, 0)
        if direction == 0 or pos.weight == 0:
            continue
        norm = issue.normalize(issue.clip(value))
        total += pos.weight * direction * norm

    if red_line_hit:
        return RED_LINE_PENALTY

    return total


def all_payoffs(deal: Deal, data: Data) -> dict[str, float]:
    """Compute every actor's payoff under the same deal."""
    return {actor: payoff(actor, deal, data) for actor in data.actors}


def batna_payoffs(data: Data) -> dict[str, float]:
    """Each actor's payoff at their own BATNA deal (their disagreement floor)."""
    out: dict[str, float] = {}
    for actor in data.actors:
        out[actor] = payoff(actor, batna_deal_for(actor, data), data)
    return out


@dataclass(frozen=True)
class PayoffSummary:
    """Diagnostic for a deal: payoff and BATNA for each actor."""
    deal: Deal
    payoffs: dict[str, float]
    batnas: dict[str, float]
    actors_below_batna: list[str]

    @property
    def all_above_batna(self) -> bool:
        return len(self.actors_below_batna) == 0


def summarize(deal: Deal, data: Data) -> PayoffSummary:
    ps = all_payoffs(deal, data)
    bs = batna_payoffs(data)
    below = [a for a in data.actors if ps[a] < bs[a]]
    return PayoffSummary(deal=dict(deal), payoffs=ps, batnas=bs, actors_below_batna=below)
