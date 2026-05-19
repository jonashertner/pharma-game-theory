"""Equilibrium solver sanity tests."""

from __future__ import annotations

import pytest

from model.data import Data, load_data
from model.equilibria import (
    kalai_smorodinsky,
    nash_bargaining,
    pareto_frontier,
    pareto_dominates,
)
from model.payoffs import summarize


@pytest.fixture(scope="module")
def data() -> Data:
    return load_data()


def test_nash_bargaining_returns_feasible_outcome(data: Data) -> None:
    outcome = nash_bargaining(data, n_per_issue=2)
    # Either the solver found a feasible deal (all above BATNA) or it
    # honestly reported infeasibility via notes.
    if outcome.payoffs:
        summary = summarize(outcome.deal, data)
        assert summary.all_above_batna, (
            f"Nash returned a deal below BATNA for: {summary.actors_below_batna}"
        )


def test_ks_returns_feasible_outcome(data: Data) -> None:
    outcome = kalai_smorodinsky(data, n_per_issue=2)
    if outcome.payoffs:
        summary = summarize(outcome.deal, data)
        assert summary.all_above_batna


def test_pareto_frontier_nonempty(data: Data) -> None:
    frontier = pareto_frontier(data, n_per_issue=2)
    assert len(frontier) > 0, "Pareto frontier should not be empty."


def test_pareto_dominates_logic() -> None:
    """Unit test for the dominance predicate itself, not data-dependent."""
    a = {"x": 2.0, "y": 3.0}
    b = {"x": 1.0, "y": 3.0}
    c = {"x": 2.0, "y": 3.0}
    d = {"x": 1.0, "y": 4.0}
    assert pareto_dominates(a, b)      # strictly better on x
    assert not pareto_dominates(a, c)  # tied on all
    assert not pareto_dominates(a, d)  # worse on y
    assert not pareto_dominates(d, a)  # worse on x


def test_nash_pareto_efficient(data: Data) -> None:
    """The Nash bargaining outcome should be Pareto-undominated on the same grid."""
    outcome = nash_bargaining(data, n_per_issue=2)
    if not outcome.payoffs:
        pytest.skip("Nash returned no feasible deal at this resolution.")
    frontier = pareto_frontier(data, n_per_issue=2)
    # Is Nash's outcome dominated by anything on the frontier?
    dominated_by_any = any(
        pareto_dominates(fp, outcome.payoffs) for _, fp in frontier
    )
    assert not dominated_by_any, "Nash outcome is Pareto-dominated; bug."
