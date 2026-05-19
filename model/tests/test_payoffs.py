"""Payoff sanity tests.

- Monotonicity: pushing an issue further in an actor's preferred direction
  should not decrease their payoff (modulo red-line violations).
- BATNA dominance: an actor's payoff at their own BATNA deal is exactly the
  reference floor — and any deal that violates their red lines must be
  strictly worse than this floor.
- Symmetry: swapping the deal across actors with identical positions yields
  matching payoff changes (loose check via the `status_quo` reference).
"""

from __future__ import annotations

import pytest

from model.data import Data, load_data
from model.payoffs import (
    RED_LINE_PENALTY,
    Deal,
    all_payoffs,
    batna_deal_for,
    batna_payoffs,
    payoff,
    summarize,
)
from model.scenarios import SCENARIOS


@pytest.fixture(scope="module")
def data() -> Data:
    return load_data()


def test_yaml_loads_cleanly(data: Data) -> None:
    assert len(data.actors) == 12
    assert len(data.issues) == 13
    assert (data.snapshot_date) == "2026-05-19"


def test_every_actor_has_at_least_one_position(data: Data) -> None:
    actor_set = {actor for (actor, _) in data.positions}
    missing = set(data.actors) - actor_set
    assert not missing, f"Actors with no positions: {missing}"


def test_payoff_monotonicity_in_preferred_direction(data: Data) -> None:
    """For each (actor, issue) where the actor's direction is non-zero and they
    have a position, increasing the value in their preferred direction (modulo
    red lines) must not strictly *decrease* their payoff."""
    for (actor, issue_id), pos in data.positions.items():
        issue = data.issues[issue_id]
        direction = issue.direction_for.get(actor, 0)
        if direction == 0:
            continue
        base_deal: Deal = {iid: i.default for iid, i in data.issues.items()}
        # build two deals at safe values around the default
        v_low = issue.lo + 0.25 * issue.width
        v_high = issue.lo + 0.75 * issue.width
        # avoid crossing the actor's red line in either direction
        if pos.red_line_value is not None:
            if direction > 0:
                v_low = max(v_low, pos.red_line_value + 0.05 * issue.width)
                v_high = max(v_high, v_low + 0.01 * issue.width)
            else:
                v_high = min(v_high, pos.red_line_value - 0.05 * issue.width)
                v_low = min(v_low, v_high - 0.01 * issue.width)
        d_low: Deal = dict(base_deal)
        d_high: Deal = dict(base_deal)
        d_low[issue_id] = v_low
        d_high[issue_id] = v_high
        p_low = payoff(actor, d_low, data)
        p_high = payoff(actor, d_high, data)
        if direction > 0:
            assert p_high >= p_low - 1e-9, (
                f"Monotonicity violated for {actor} on {issue_id} (direction=+1): "
                f"payoff at {v_low}={p_low}, at {v_high}={p_high}"
            )
        else:
            assert p_low >= p_high - 1e-9, (
                f"Monotonicity violated for {actor} on {issue_id} (direction=-1): "
                f"payoff at {v_low}={p_low}, at {v_high}={p_high}"
            )


def test_batna_floor(data: Data) -> None:
    """Every actor's payoff at their own BATNA deal equals the documented BATNA payoff."""
    bps = batna_payoffs(data)
    for actor in data.actors:
        # The BATNA payoff need not be zero, but it must be the deterministic
        # output of payoff(actor, batna_deal_for(actor)).
        assert payoff(actor, batna_deal_for(actor, data), data) == bps[actor]


def test_red_line_violation_drops_to_penalty(data: Data) -> None:
    """A deal that strictly violates an actor's red line returns RED_LINE_PENALTY."""
    # Pick an actor with a red line on some issue.
    actor, issue_id = None, None
    pos = None
    for (a, iid), p in data.positions.items():
        if p.red_line_value is not None:
            issue = data.issues[iid]
            if issue.direction_for.get(a, 0) != 0:
                actor, issue_id, pos = a, iid, p
                break
    assert actor is not None, "Expected at least one actor with a red line."
    issue = data.issues[issue_id]
    direction = issue.direction_for[actor]
    deal: Deal = {iid: i.default for iid, i in data.issues.items()}
    # Move the issue strictly past the red line.
    if direction > 0:
        violating_value = pos.red_line_value - 0.1 * issue.width
        deal[issue_id] = max(issue.lo, violating_value)
    else:
        violating_value = pos.red_line_value + 0.1 * issue.width
        deal[issue_id] = min(issue.hi, violating_value)
    assert payoff(actor, deal, data) == RED_LINE_PENALTY


def test_status_quo_feasible(data: Data) -> None:
    """The May 2026 status-quo deal — which mirrors the actual signed
    Genentech MFN + Swiss framework + IRA Round 3 selection — must be a
    feasible deal: all actors at or above their BATNA, no red-line violations.

    This is the Phase B calibration test. If status_quo isn't feasible, the
    red-line settings or payoff weights are too tight; investigate and fix."""
    status_quo = SCENARIOS["status_quo"].to_deal(data)
    summary = summarize(status_quo, data)
    assert summary.all_above_batna, (
        f"Status quo (the actual May 2026 signed state) is infeasible. "
        f"Actors below BATNA: {summary.actors_below_batna}. "
        f"This means the model is over-constrained — relax red lines or "
        f"weights in positions.yaml."
    )


def test_trade_war_is_worse_than_status_quo_for_most(data: Data) -> None:
    """The 'trade_war_collapse' scenario should make most actors worse off
    than the status quo. Any actor better off in trade war is suspicious."""
    sq = SCENARIOS["status_quo"].to_deal(data)
    tw = SCENARIOS["trade_war_collapse"].to_deal(data)
    sq_p = all_payoffs(sq, data)
    tw_p = all_payoffs(tw, data)
    worse_in_war = [a for a in data.actors if tw_p[a] < sq_p[a]]
    assert len(worse_in_war) >= len(data.actors) // 2, (
        f"Trade war should hurt at least half the actors. "
        f"Only {len(worse_in_war)} are worse off: status_quo={sq_p}; war={tw_p}"
    )
