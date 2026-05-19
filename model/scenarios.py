"""Named scenarios — pre-baked starting points for analysis.

A scenario is a complete deal vector plus a short label and a note about
what it captures. The CLI and the playground use these as presets; the
agent harness uses them as initial conditions.

The reference snapshot is `status_quo`: every issue at the default value
from issues.yaml as of 2026-05-19.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data import Data, Issue
from .payoffs import Deal


@dataclass(frozen=True)
class Scenario:
    id: str
    name: str
    description: str
    overrides: dict[str, float]   # issue_id -> override value (rest default to issue.default)

    def to_deal(self, data: Data) -> Deal:
        deal: Deal = {}
        for issue_id, issue in data.issues.items():
            deal[issue_id] = float(self.overrides.get(issue_id, issue.default))
        return deal


SCENARIOS: dict[str, Scenario] = {

    "status_quo": Scenario(
        id="status_quo",
        name="Status quo (2026-05-19 snapshot)",
        description=(
            "Every issue at its default value as of the snapshot date. "
            "Reflects the existing Dec-2025 Genentech MFN deal, the Nov-2025 "
            "Swiss framework, IRA Round-3 selection of Xolair, and the "
            "April-2026 Section 232 proclamation with 0% MFN-deal track."
        ),
        overrides={},   # all defaults
    ),

    "mfn_hardline": Scenario(
        id="mfn_hardline",
        name="MFN hardline",
        description=(
            "The administration pushes MFN aggressively: coverage doubles "
            "across Roche's catalog, IRA discount deepens, Section 232 "
            "exemption is denied, TrumpRx SKU count expands, and "
            "international protections are eroded. Tests whether Roche's "
            "BATNA still binds at this extreme."
        ),
        overrides={
            "mfn_coverage": 20,
            "ira_mfp_discount": 70,
            "section_232_rate": 15,
            "trumprx_skus": 20,
            "intl_ref_pricing_protection": 1,
            "swiss_diplomatic_carveout": 2,
        },
    ),

    "swiss_carveout": Scenario(
        id="swiss_carveout",
        name="Swiss diplomatic carve-out",
        description=(
            "Strong Swiss-specific protections: 0% Section 232, deep "
            "carve-out language, ex-US firewall reinforced. US gives up "
            "some MFN coverage on Roche in exchange for Swiss "
            "investment + jobs commitments."
        ),
        overrides={
            "mfn_coverage": 4,
            "section_232_rate": 0,
            "swiss_diplomatic_carveout": 9,
            "intl_ref_pricing_protection": 8,
            "us_manufacturing_share": 50,
            "rnd_commitment": 12,
        },
    ),

    "ira_escalation": Scenario(
        id="ira_escalation",
        name="IRA escalation",
        description=(
            "IRA expanded by Congress to cover more Roche drugs in Round 4 "
            "and beyond; pipeline pricing protocols formalised; biosimilar "
            "incentives sharpened. MFN coverage held but discount deepens."
        ),
        overrides={
            "ira_mfp_discount": 65,
            "mfn_coverage": 8,
            "pipeline_pricing_protocol": 6,
            "patent_exclusivity": 4,
            "ip_innovation_protection": 5,
        },
    ),

    "basel_relocation_stress": Scenario(
        id="basel_relocation_stress",
        name="Basel-relocation stress test",
        description=(
            "Roche accelerates US capex by relocating Basel manufacturing. "
            "Tests Swiss internal coherence: federal-council payoff may "
            "hold while Basel cantons + domestic payers diverge sharply."
        ),
        overrides={
            "us_manufacturing_share": 60,
            "rnd_commitment": 13,
            "swiss_diplomatic_carveout": 7,
            "section_232_rate": 0,
        },
    ),

    "trade_war_collapse": Scenario(
        id="trade_war_collapse",
        name="Trade-war collapse",
        description=(
            "Negotiation breaks down. Section 232 reverts to tier-2 (15-20%) "
            "or higher; MFN deals abrogated; Swiss framework unwinds. Every "
            "actor falls toward their BATNA."
        ),
        overrides={
            "section_232_rate": 50,
            "mfn_coverage": 1,
            "swiss_diplomatic_carveout": 1,
            "intl_ref_pricing_protection": 2,
            "us_manufacturing_share": 35,
        },
    ),
}


def get_scenario(name: str) -> Scenario:
    if name not in SCENARIOS:
        valid = ", ".join(SCENARIOS.keys())
        raise KeyError(f"Unknown scenario '{name}'. Valid: {valid}")
    return SCENARIOS[name]
