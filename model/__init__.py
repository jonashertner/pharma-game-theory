"""Game-theoretic model: payoff functions, scenarios, equilibrium solvers.

The model treats the negotiation as a vector in 13-dimensional issue space.
A "deal" is an assignment of a value to each issue id. Each actor has a
payoff function over deals, parametrised by their interests, weights, BATNA
and red lines (loaded from data/positions.yaml).
"""

from .data import Issue, Position, load_data
from .payoffs import payoff, all_payoffs, BATNA_DEAL
from .scenarios import SCENARIOS, Scenario, get_scenario
from .equilibria import (
    nash_bargaining,
    kalai_smorodinsky,
    shapley_values,
    in_core,
    pareto_dominates,
    pareto_frontier,
)

__all__ = [
    "Issue",
    "Position",
    "load_data",
    "payoff",
    "all_payoffs",
    "BATNA_DEAL",
    "SCENARIOS",
    "Scenario",
    "get_scenario",
    "nash_bargaining",
    "kalai_smorodinsky",
    "shapley_values",
    "in_core",
    "pareto_dominates",
    "pareto_frontier",
]
