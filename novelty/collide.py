"""Open-collider-style collision module.

Given (a) a current scenario state and (b) a focal aspect of the negotiation,
emit Claude prompts that *collide* the scenario against a structurally
distant domain to surface non-obvious negotiation moves.

Two modes:
  - Default: emit prompts to a Markdown file the user pastes into Claude.
  - Live (`--live`): call Anthropic API directly.

Reference: https://github.com/CL-ML/open-collider
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from model.data import load_data   # noqa: E402
from model.payoffs import summarize   # noqa: E402
from model.scenarios import SCENARIOS, get_scenario   # noqa: E402


DOMAINS_PATH = Path(__file__).resolve().parent / "domains.yaml"
IDEAS_DIR = Path(__file__).resolve().parent / "ideas"


@dataclass(frozen=True)
class Domain:
    id: str
    name: str
    one_liner: str
    principles: list[str]
    why_relevant: str
    sources: list[str]


def load_domains() -> list[Domain]:
    raw = yaml.safe_load(DOMAINS_PATH.read_text())
    return [
        Domain(
            id=d["id"], name=d["name"], one_liner=d["one_liner"].strip(),
            principles=list(d["principles"]),
            why_relevant=d["why_relevant"].strip(),
            sources=list(d.get("sources", [])),
        )
        for d in raw["domains"]
    ]


def list_domains() -> None:
    for d in load_domains():
        print(f"  {d.id:35s}  {d.name}")


def build_brief(scenario_id: str = "status_quo", focus: str | None = None) -> str:
    """Compose a brief that captures the current state, who's stuck below
    their BATNA, and what aspect the user wants moves on."""
    data = load_data()
    scenario = get_scenario(scenario_id)
    deal = scenario.to_deal(data)
    summary = summarize(deal, data)

    deltas = []
    for iid, issue in data.issues.items():
        v = deal[iid]
        if abs(v - issue.default) < 0.5:
            continue
        deltas.append(f"  - {issue.name}: {v:.2f} {issue.units}")

    if deltas:
        deal_block = "\n".join(deltas)
    else:
        deal_block = "  (every issue at 2026-05-19 status quo)"

    below = summary.actors_below_batna
    if below:
        stuck_block = "Actors currently below BATNA: " + ", ".join(below)
    else:
        stuck_block = (
            "All actors above BATNA on the current draft. The challenge is finding "
            "*Pareto improvements* — moves that lift at least one principal further "
            "above BATNA without dropping any other."
        )

    focus_block = focus or (
        "Open. Find moves on any of the 13 issues that improve the situation "
        "for the principal triple (Roche, US executive, Swiss federal council) "
        "without creating new red-line violations elsewhere."
    )

    return f"""SCENARIO: {scenario.name}

DEAL DEVIATIONS FROM STATUS QUO:
{deal_block}

STUCK ON: {stuck_block}

USER FOCUS: {focus_block}

ANCHORING RED LINES (do not propose moves that cross these):
- Roche: international reference-pricing firewall (intl_ref_pricing >= 1);
         no compulsory licensing; net-price confidentiality for ex-US.
- US Executive: visible price-cut commitment (mfn_coverage >= 1, ira_discount >= 20);
                US-manufacturing build (us_manufacturing_share >= 30).
- Swiss Federal Council: cannot concede BAG statutory authority;
                         swiss_diplomatic_carveout >= 2.
- Swiss Cantons (Basel): cannot commit to wind down a specific Basel site
                         (us_manufacturing_share <= 65).
- Swiss public/payers: swiss_domestic_pricing must not rise > +15%.
- Patient advocacy: cannot reduce access to currently covered drugs.
- EU reference pricing: cannot accept swiss_domestic_pricing > +15.
- Biosimilars: patent_exclusivity <= 9; ip_innovation_protection <= 9.
- Investors: ira_mfp_discount <= 75; section_232_rate <= 50.

"""


def build_collision_prompt(brief: str, domain: Domain) -> str:
    """Build the Claude prompt that collides the scenario brief with one domain."""
    principles_block = "\n".join(f"  - {p}" for p in domain.principles)
    return textwrap.dedent(f"""\
        You are a strategic-novelty engine. Treat the following pharma-pricing
        negotiation as if it were a {domain.name} problem.

        --- ANALOGUE DOMAIN ---
        {domain.name} — {domain.one_liner}

        Operational principles from this domain:
        {principles_block}

        Why this domain matches (analyst's note):
        {domain.why_relevant}

        --- NEGOTIATION BRIEF ---
        {brief}

        --- TASK ---
        1) Pick 2–3 specific mechanisms from {domain.name} listed above.
        2) For each, translate to a CONCRETE negotiation move:
           - WHO proposes the move (which actor by id)
           - WHICH of the 13 issues it touches (issue id from data/issues.yaml)
           - SPECIFIC value change with units
           - TIMELINE (when it takes effect)
           - COMPLIANCE TEST (how to verify the move is honored)
        3) For each move, verify against the red lines listed in the brief.
           Reject moves that violate any.
        4) For each surviving move, name two actors whose payoff it improves
           and one actor it costs. If the cost is bigger than the gain across
           parties, discard it.

        Output as a numbered list. Be terse. Do not invent new issues or
        actors — restrict yourself to the 13 issues and 12 actors of the
        model. Do not propose moves that any listed red line forbids.
        """).strip()


def emit_brief_and_prompts(
    scenario_id: str,
    domain_ids: list[str] | None = None,
    focus: str | None = None,
    out_dir: Path | None = None,
) -> Path:
    """Write a Markdown file with the brief + one prompt per domain.
    Returns the file path so the user can paste into Claude."""
    domains = load_domains()
    if domain_ids:
        domains = [d for d in domains if d.id in domain_ids]
    if not domains:
        raise ValueError("No domains selected.")

    brief = build_brief(scenario_id, focus)
    out_dir = out_dir or IDEAS_DIR / scenario_id
    out_dir.mkdir(parents=True, exist_ok=True)

    import datetime as dt
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = out_dir / f"prompts-{stamp}.md"

    lines = [f"# Collision prompts — scenario `{scenario_id}` — {stamp}"]
    lines.append("\n*Paste each prompt into Claude separately to generate "
                 "non-obvious moves for that domain.*\n")
    for i, d in enumerate(domains, 1):
        lines.append(f"\n## Prompt {i}/{len(domains)} — {d.name}\n")
        lines.append("```")
        lines.append(build_collision_prompt(brief, d))
        lines.append("```\n")
    out_path.write_text("\n".join(lines))
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m novelty.collide",
        description=__doc__,
    )
    parser.add_argument("--scenario", default="status_quo", choices=list(SCENARIOS.keys()))
    parser.add_argument("--domains", nargs="*",
                        help="Specific domain ids; defaults to all.")
    parser.add_argument("--focus", default=None,
                        help="Optional user focus statement.")
    parser.add_argument("--list-domains", action="store_true")
    args = parser.parse_args(argv)

    if args.list_domains:
        list_domains()
        return 0

    out = emit_brief_and_prompts(args.scenario, args.domains, args.focus)
    print(f"Wrote {out}")
    print(f"Open it, paste each prompt separately into Claude, save responses to "
          f"{out.parent}/responses-*.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
