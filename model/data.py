"""Loads issues.yaml and positions.yaml into typed structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass(frozen=True)
class Issue:
    id: str
    name: str
    description: str
    units: str
    lo: float
    hi: float
    default: float
    direction_for: dict[str, int]
    actors_with_stake: list[str]

    @property
    def width(self) -> float:
        return self.hi - self.lo

    def normalize(self, value: float) -> float:
        """Map issue value to [0, 1] for cross-issue comparison."""
        if self.width == 0:
            return 0.0
        return (value - self.lo) / self.width

    def clip(self, value: float) -> float:
        return max(self.lo, min(self.hi, value))


@dataclass(frozen=True)
class Position:
    actor: str
    issue: str
    position: str
    batna_value: float
    red_line_value: float | None
    weight: float
    citation: str
    inferred: bool


@dataclass
class Data:
    snapshot_date: str
    actors: list[str]
    issues: dict[str, Issue]
    positions: dict[tuple[str, str], Position]   # (actor, issue) -> Position

    def issue_ids(self) -> list[str]:
        return list(self.issues.keys())

    def position(self, actor: str, issue: str) -> Position | None:
        return self.positions.get((actor, issue))

    def actor_weight(self, actor: str, issue: str) -> float:
        p = self.position(actor, issue)
        return p.weight if p is not None else 0.0


def _load_yaml(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_data(data_dir: Path | None = None) -> Data:
    data_dir = data_dir or DATA_DIR
    issues_raw = _load_yaml(data_dir / "issues.yaml")
    positions_raw = _load_yaml(data_dir / "positions.yaml")

    issues: dict[str, Issue] = {}
    for issue_dict in issues_raw["issues"]:
        lo, hi = issue_dict["range"]
        issues[issue_dict["id"]] = Issue(
            id=issue_dict["id"],
            name=issue_dict["name"],
            description=issue_dict["description"].strip(),
            units=issue_dict["units"],
            lo=float(lo),
            hi=float(hi),
            default=float(issue_dict["default"]),
            direction_for=dict(issue_dict.get("direction_for", {})),
            actors_with_stake=[
                actor
                for actor, direction in issue_dict.get("direction_for", {}).items()
                if direction != 0
            ],
        )

    positions: dict[tuple[str, str], Position] = {}
    for actor, issue_map in positions_raw["positions"].items():
        if not issue_map:
            continue
        for issue_id, cell in issue_map.items():
            if cell is None:
                continue
            red_line = cell.get("red_line_value")
            positions[(actor, issue_id)] = Position(
                actor=actor,
                issue=issue_id,
                position=str(cell.get("position", "")),
                batna_value=float(cell.get("batna_value", issues[issue_id].default)),
                red_line_value=(
                    float(red_line) if red_line is not None else None
                ),
                weight=float(cell.get("weight", 0)),
                citation=str(cell.get("citation", "")),
                inferred=bool(cell.get("inferred", True)),
            )

    return Data(
        snapshot_date=str(issues_raw["snapshot_date"]),
        actors=list(issues_raw["actors"]),
        issues=issues,
        positions=positions,
    )
