"""Negotiation protocols — round structures.

A protocol defines:
  - which actors participate in each round,
  - in what order they speak,
  - how proposals merge into the running draft,
  - termination condition.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Protocol:
    id: str
    name: str
    participants: list[str]
    description: str


PROTOCOLS: dict[str, Protocol] = {

    "bilateral_us_roche": Protocol(
        id="bilateral_us_roche",
        name="Bilateral US ↔ Roche",
        participants=["roche", "us-executive"],
        description=(
            "Pure two-party bargain: only Roche and the US executive at the "
            "table. Useful to see what they would agree to if all third "
            "parties were silent — surfaces what's actually private value "
            "to the two principals."
        ),
    ),

    "trilateral_us_ch_roche": Protocol(
        id="trilateral_us_ch_roche",
        name="Trilateral US ↔ CH ↔ Roche",
        participants=["roche", "us-executive", "swiss-federal-council"],
        description=(
            "Adds the Swiss Federal Council as the trade-frame counterparty. "
            "This is the structure of the actual November 2025 framework "
            "negotiation."
        ),
    ),

    "swiss_internal": Protocol(
        id="swiss_internal",
        name="Swiss internal coherence",
        participants=[
            "swiss-federal-council",
            "swiss-cantons-basel",
            "swiss-public-and-domestic-payers",
            "roche",
        ],
        description=(
            "Swiss-side disaggregated table: tests whether the federal "
            "council's negotiating mandate actually carries the cantons and "
            "the domestic payer/patient constituency. Verification scenario "
            "for Plan §9.4 (Swiss internal-coherence test)."
        ),
    ),

    "full_multilateral": Protocol(
        id="full_multilateral",
        name="Full multilateral",
        participants=[
            "roche",
            "us-executive",
            "us-congress",
            "swiss-federal-council",
            "swiss-cantons-basel",
            "swiss-public-and-domestic-payers",
            "novartis",
            "pbms-and-payers",
            "patient-advocacy",
            "eu-reference-pricing",
            "biosimilars-competitors",
            "investors",
        ],
        description=(
            "Everyone at the table. The most realistic structure but also "
            "the most prone to logjam — useful as a stress test of any "
            "candidate compromise."
        ),
    ),

    "coalition_formation": Protocol(
        id="coalition_formation",
        name="Coalition formation phase",
        participants=[
            "roche",
            "novartis",
            "swiss-federal-council",
            "swiss-cantons-basel",
            "us-executive",
            "us-congress",
        ],
        description=(
            "Sub-stage where actors form alliances before the main table. "
            "Detects coalition stability (cooperative-game-theory core)."
        ),
    ),
}


def get_protocol(name: str) -> Protocol:
    if name not in PROTOCOLS:
        valid = ", ".join(PROTOCOLS.keys())
        raise KeyError(f"Unknown protocol '{name}'. Valid: {valid}")
    return PROTOCOLS[name]
