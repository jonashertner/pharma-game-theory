"""CLI: `python -m model <scenario> [--concept ...]`

Prints the deal, every actor's payoff vs BATNA, the actors below their BATNA,
and (optionally) equilibrium solutions on the same model.
"""

from __future__ import annotations

import argparse
import sys
import textwrap

from .data import load_data
from .equilibria import (
    in_core,
    kalai_smorodinsky,
    nash_bargaining,
    pareto_frontier,
    shapley_values,
)
from .payoffs import summarize
from .scenarios import SCENARIOS, get_scenario


def _print_deal(deal: dict[str, float], data) -> None:
    print("\nDeal vector:")
    for issue_id in data.issue_ids():
        issue = data.issues[issue_id]
        value = deal.get(issue_id, issue.default)
        print(f"  {issue_id:34s}  {value:8.2f}   ({issue.units})")


def _print_payoffs(summary) -> None:
    print("\nPayoffs vs BATNA:")
    print(f"  {'actor':40s}  {'payoff':>10s}  {'BATNA':>10s}  {'surplus':>10s}")
    for actor in summary.payoffs:
        p = summary.payoffs[actor]
        b = summary.batnas[actor]
        s = p - b
        flag = " *" if actor in summary.actors_below_batna else ""
        print(f"  {actor:40s}  {p:10.2f}  {b:10.2f}  {s:10.2f}{flag}")
    if summary.actors_below_batna:
        print(f"\n  ✗ {len(summary.actors_below_batna)} actor(s) below BATNA: " +
              ", ".join(summary.actors_below_batna))
    else:
        print("\n  ✓ All actors above BATNA — feasible deal.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m model",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "scenario",
        nargs="?",
        default="status_quo",
        choices=list(SCENARIOS.keys()),
        help="Named scenario to evaluate (default: status_quo).",
    )
    parser.add_argument(
        "--concept",
        choices=["payoffs", "nash", "ks", "pareto", "core", "shapley", "all"],
        default="payoffs",
        help="Solution concept to compute. 'payoffs' just shows the scenario.",
    )
    parser.add_argument(
        "--n-per-issue",
        type=int,
        default=4,
        help="Grid resolution per issue for solvers. Higher = slower but better.",
    )
    parser.add_argument("--list", action="store_true", help="List scenarios and exit.")
    args = parser.parse_args(argv)

    if args.list:
        print("Available scenarios:")
        for sc in SCENARIOS.values():
            print(f"\n  {sc.id}  —  {sc.name}")
            print(textwrap.fill(sc.description, width=78,
                                initial_indent="      ",
                                subsequent_indent="      "))
        return 0

    data = load_data()
    scenario = get_scenario(args.scenario)

    print(f"=== Scenario: {scenario.name} ===")
    print(textwrap.fill(scenario.description, width=78))

    deal = scenario.to_deal(data)
    summary = summarize(deal, data)
    _print_deal(deal, data)
    _print_payoffs(summary)

    if args.concept in ("nash", "all"):
        print("\n--- Nash bargaining (asymmetric, leverage-weighted) ---")
        outcome = nash_bargaining(data, n_per_issue=args.n_per_issue)
        _print_deal(outcome.deal, data)
        s = summarize(outcome.deal, data)
        _print_payoffs(s)
        if outcome.notes:
            print(f"  Note: {outcome.notes}")

    if args.concept in ("ks", "all"):
        print("\n--- Kalai-Smorodinsky (proportional gain) ---")
        outcome = kalai_smorodinsky(data, n_per_issue=args.n_per_issue)
        _print_deal(outcome.deal, data)
        s = summarize(outcome.deal, data)
        _print_payoffs(s)
        if outcome.notes:
            print(f"  Note: {outcome.notes}")

    if args.concept in ("pareto", "all"):
        print("\n--- Pareto frontier (sample of 10) ---")
        frontier = pareto_frontier(data, n_per_issue=max(2, args.n_per_issue - 1))
        print(f"  {len(frontier)} non-dominated points on the grid.")
        for i, (d, ps) in enumerate(frontier[:10]):
            print(f"\n  Point {i+1}:")
            for actor in data.actors:
                print(f"    {actor:40s}  {ps[actor]:10.2f}")

    if args.concept in ("core", "all"):
        print("\n--- Core check on current deal ---")
        ok, blocking = in_core(deal, data, n_per_issue=max(2, args.n_per_issue - 1))
        if ok:
            print("  ✓ Deal is in the core (no blocking coalition found).")
        else:
            print(f"  ✗ Deal NOT in core. Top 5 blocking coalitions by surplus gain:")
            top = sorted(blocking.items(), key=lambda x: -x[1])[:5]
            for coalition, gain in top:
                members = ", ".join(sorted(coalition))
                print(f"    +{gain:8.2f}  {{{members}}}")

    if args.concept in ("shapley", "all"):
        print("\n--- Shapley values (approximate) ---")
        sv = shapley_values(data, n_per_issue=2)
        total = sum(sv.values())
        for actor, v in sorted(sv.items(), key=lambda x: -x[1]):
            share = (100 * v / total) if total > 0 else 0.0
            print(f"  {actor:40s}  {v:10.2f}   ({share:5.1f}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
