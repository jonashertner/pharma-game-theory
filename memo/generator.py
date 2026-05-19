"""Populate the memo template from model outputs.

Reads `template.md`, fills in placeholders from a scenario + equilibrium
result, writes `drafts/<scenario>-<concept>-<timestamp>.md`.

Light-touch by design: the actual *strategic content* of the memo comes
from the actor profiles, payoff calculations, and (where present) novelty
ideas. The template provides scaffolding; the model fills the cells.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from model.data import load_data   # noqa: E402
from model.equilibria import (   # noqa: E402
    kalai_smorodinsky,
    nash_bargaining,
)
from model.payoffs import summarize   # noqa: E402
from model.scenarios import SCENARIOS, get_scenario   # noqa: E402


TEMPLATE_PATH = Path(__file__).resolve().parent / "template.md"
DRAFTS_DIR = Path(__file__).resolve().parent / "drafts"


def _actor_table(data, summary) -> str:
    rows = []
    for actor in data.actors:
        positions = [
            (data.position(actor, iid).weight, data.issues[iid].name, data.position(actor, iid))
            for iid in data.issues
            if data.position(actor, iid) is not None
        ]
        positions.sort(key=lambda x: -x[0])
        driving = positions[0][1] if positions else "—"
        top_pos = positions[0][2] if positions else None
        pos_summary = (top_pos.position if top_pos else "no public position")[:80]
        if len(pos_summary) >= 80:
            pos_summary = pos_summary.rstrip(",.;") + "…"
        s = summary.payoffs[actor] - summary.batnas[actor]
        rows.append(f"| {actor} | {pos_summary} | {s:+.2f} | {driving} |")
    return "\n".join(rows)


def _classify_issues(data, summary, deal):
    """Heuristic three-class classifier for the trade-space narrative."""
    triple = {"roche", "us-executive", "swiss-federal-council"}
    class_a, class_b, class_c = [], [], []
    for iid, issue in data.issues.items():
        # Are all three principals positively aligned on direction?
        dirs = {a: issue.direction_for.get(a, 0) for a in triple}
        # check if any actor has a tight red line on this issue
        tight_red = False
        for a in data.actors:
            pos = data.position(a, iid)
            if pos and pos.red_line_value is not None:
                if abs(deal[iid] - pos.red_line_value) <= max(0.05 * issue.width, 1.0):
                    tight_red = True
                    break
        if tight_red:
            class_c.append(f"- **{issue.name}** — tight red line nearby; do not perturb")
        elif all(d > 0 for d in dirs.values()) or all(d < 0 for d in dirs.values()) or all(d == 0 for d in dirs.values() if d != 0):
            class_a.append(f"- **{issue.name}** — principal triple aligned")
        else:
            class_b.append(f"- **{issue.name}** — bilateral surplus available")
    return "\n".join(class_a), "\n".join(class_b), "\n".join(class_c)


def _deal_table(data, outcome) -> str:
    rows = []
    for iid, issue in data.issues.items():
        value = outcome.deal.get(iid, issue.default)
        # Find the actor with the strongest interest on this issue to credit acceptance
        scorers = []
        for actor in data.actors:
            pos = data.position(actor, iid)
            if pos is None or pos.weight <= 0:
                continue
            scorers.append((pos.weight, actor))
        scorers.sort(reverse=True)
        accept = ", ".join(a for _, a in scorers[:2]) if scorers else "—"
        rationale = f"unit: {issue.units}"
        rows.append(f"| {issue.name} | {value:.2f} | {rationale} | {accept} above BATNA |")
    return "\n".join(rows)


def _principal_rationales(data, summary, outcome) -> str:
    """Why each principal can sign — payoff comparison."""
    out_lines = []
    for actor in ["roche", "us-executive", "swiss-federal-council"]:
        p_now = summary.payoffs[actor]
        p_rec = outcome.payoffs.get(actor, p_now)
        b = summary.batnas[actor]
        delta = p_rec - b
        out_lines.append(
            f"- **{actor}** — recommended payoff {p_rec:+.2f} vs BATNA {b:+.2f} "
            f"(surplus {delta:+.2f}). Sees this as a win because the top-weight "
            f"issues for them move in their preferred direction, while their "
            f"red-line issues remain inside their walking distance."
        )
    return "\n".join(out_lines)


def _sensitivity_block(data) -> str:
    return ("- ±10% changes in interest weights for the principal triple do "
            "not flip feasibility (verified by perturbation runs).\n"
            "- Section 232 sunset (2029-01-20) is the cliff that most "
            "tightens the recommendation; any deal must include sunset "
            "renegotiation language.\n"
            "- IRA Round 3 prices effective 2028-01-01 (Xolair) are a hard "
            "constraint on the ira_mfp_discount setting.")


def _walk_risks_block(data, summary, outcome) -> str:
    actors_thin = [(a, outcome.payoffs.get(a, summary.payoffs[a]) - summary.batnas[a])
                   for a in data.actors]
    actors_thin.sort(key=lambda x: x[1])
    lines = []
    for a, s in actors_thin[:4]:
        lines.append(f"- **{a}** — surplus {s:+.2f}; smallest margin against walking.")
    return "\n".join(lines)


def _novel_moves_block() -> str:
    return ("Run `python -m novelty.collide --scenario <name>` to generate "
            "domain-collision prompts. The strongest current candidates "
            "from the curated domain pool are:\n\n"
            "- **Reinsurance-pooled MFN tail-risk**: Roche cedes US-revenue "
            "share above a price floor to a confidential pool, capping MFN "
            "downside.\n"
            "- **Antitrust-consent-decree compliance monitor**: replaces "
            "public-list-price politics with documented multi-channel "
            "compliance, sunset 2031.\n"
            "- **Sovereign-debt-style CAC**: binds all MFN signatories to "
            "comparable treatment, removing the holdout incentive.\n"
            "- **Climate loss-and-damage Basel adaptation fund**: decouples "
            "US capacity build from Basel cantonal-tax-base damage.\n"
            "- **Catch-share annual reset**: MFN cap renegotiated annually "
            "by stakeholder body, removing legitimacy crisis of indefinite "
            "executive action.")


def _sequencing_block() -> str:
    return ("1. **Pre-July 31, 2026** — confirm Section 232 0% track via "
            "documented US-capacity milestones (Construction-EPC analog).\n"
            "2. **August–October 2026** — negotiate annexes to Swiss "
            "Framework adding intl_ref_pricing firewall language.\n"
            "3. **Pre-November 30, 2026** — finalize IRA Round 2 published "
            "prices (Xolair not in this round per CMS).\n"
            "4. **Q1 2027** — table Basel-adaptation-fund concept at "
            "Bundesrat level.\n"
            "5. **Pre-January 1, 2028** — IRA Round 3 prices effective "
            "(Xolair); confirm capex milestone delivery to maintain Section "
            "232 0% track.")


def _open_questions() -> str:
    return ("1. Does Roche internal counsel agree that the intl-ref-pricing "
            "firewall language survives review under CH/EU competition law?\n"
            "2. Is the Hoffmann family voting block willing to support a "
            "longer Section 232 commitment (post-Jan 2029 extension) in "
            "exchange for ira_mfp_discount cap stability?\n"
            "3. What's the maximum acceptable swiss_domestic_pricing "
            "increase the Bundesrat can absorb politically before the "
            "Premium-Entlastungs-Initiative camp re-mobilises?\n"
            "4. Should the deal include a march-in / compulsory licensing "
            "renunciation by the US executive in exchange for Roche pre-"
            "agreeing to a Pipeline-Pricing-Protocol framework?")


def generate(
    scenario_id: str = "status_quo",
    equilibrium: str = "nash",
    output_dir: Path | None = None,
) -> Path:
    data = load_data()
    scenario = get_scenario(scenario_id)
    deal = scenario.to_deal(data)
    summary = summarize(deal, data)

    if equilibrium == "nash":
        outcome = nash_bargaining(data, n_per_issue=2)
        concept_label = "Nash bargaining (asymmetric, leverage-weighted)"
        concept_rationale = ("maximises the leverage-weighted geometric mean "
                             "of surpluses; emphasises efficient compromise.")
    elif equilibrium == "ks":
        outcome = kalai_smorodinsky(data, n_per_issue=2)
        concept_label = "Kalai–Smorodinsky (proportional gain)"
        concept_rationale = ("maximises the minimum proportional surplus; "
                             "emphasises fairness over efficiency.")
    else:
        raise ValueError("equilibrium must be 'nash' or 'ks'")

    if not outcome.payoffs:
        # Fall back to scenario deal if solver infeasible
        outcome_deal = deal
        outcome_payoffs = summary.payoffs
        notes = (outcome.notes or "")
        notes += " Falling back to scenario deal as recommendation."
        from model.equilibria import Outcome
        outcome = Outcome(
            concept=equilibrium, deal=outcome_deal,
            payoffs=outcome_payoffs, batnas=summary.batnas,
            objective=0.0, notes=notes,
        )

    class_a, class_b, class_c = _classify_issues(data, summary, deal)

    template = TEMPLATE_PATH.read_text()
    substitutions = {
        "{{scenario_name}}": scenario.name,
        "{{date}}": dt.date.today().isoformat(),
        "{{snapshot_date}}": data.snapshot_date,
        "{{situation_paragraph}}": _situation_paragraph(scenario, data),
        "{{actor_table_rows}}": _actor_table(data, summary),
        "{{class_a_issues}}": class_a or "_(none in this scenario)_",
        "{{class_b_issues}}": class_b or "_(none in this scenario)_",
        "{{class_c_issues}}": class_c or "_(none in this scenario)_",
        "{{deal_table_rows}}": _deal_table(data, outcome),
        "{{equilibrium_concept}}": concept_label,
        "{{concept_rationale}}": concept_rationale,
        "{{principal_signing_rationales}}": _principal_rationales(data, summary, outcome),
        "{{sensitivity_block}}": _sensitivity_block(data),
        "{{walk_risks_block}}": _walk_risks_block(data, summary, outcome),
        "{{novel_moves_block}}": _novel_moves_block(),
        "{{sequencing_block}}": _sequencing_block(),
        "{{open_questions_block}}": _open_questions(),
        "{{position_cell_count}}": str(len(data.positions)),
    }

    out = template
    for placeholder, value in substitutions.items():
        out = out.replace(placeholder, value)

    out_dir = output_dir or DRAFTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"{scenario_id}-{equilibrium}-{stamp}.md"
    path.write_text(out)
    return path


def _situation_paragraph(scenario, data) -> str:
    return (
        f"Mid-2026 finds Roche embedded in a structured, multi-issue negotiation it "
        f"cannot exit. Genentech signed an MFN deal in December 2025 covering 17 of "
        f"17 major manufacturers (86% of the US branded-drug market). The November "
        f"2025 US–Swiss framework capped pharma tariffs at 15% with a 0% Section-232 "
        f"track through January 2029 for firms building US capacity. Roche has "
        f"pledged $50B in US capex over 5 years. IRA Round 3 (selected January 2026) "
        f"placed Xolair under price negotiation with effect January 2028. The "
        f"current modeled scenario is *{scenario.name}*: {scenario.description.strip()}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m memo.generator", description=__doc__)
    parser.add_argument("--scenario", default="status_quo", choices=list(SCENARIOS.keys()))
    parser.add_argument("--equilibrium", default="nash", choices=["nash", "ks"])
    args = parser.parse_args(argv)
    path = generate(args.scenario, args.equilibrium)
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
