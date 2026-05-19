"""Round-based negotiation runner.

Default mode: **heuristic** — each actor moves issues toward its preferred
direction by a step proportional to its weight, clipped at red lines. No API
calls. Fast, deterministic, useful for sanity checks.

API mode (`--live`): each actor is a Claude instance with a system prompt
built from the actor profile + dossier template. Requires `ANTHROPIC_API_KEY`.

Both modes emit a JSON state log + a Markdown transcript per run.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Path hygiene so `python agents/runner.py` works from anywhere.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from model.data import Data, Issue, load_data   # noqa: E402
from model.payoffs import Deal, summarize, payoff   # noqa: E402
from model.scenarios import SCENARIOS, get_scenario   # noqa: E402
from agents.protocols import PROTOCOLS, get_protocol   # noqa: E402


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class Turn:
    round: int
    actor: str
    action: str   # PROPOSE | COUNTER | ACCEPT | WALK
    moves: list[dict[str, Any]] = field(default_factory=list)
    rationale: str = ""
    payoff_after: float | None = None
    batna: float | None = None


@dataclass
class RunResult:
    scenario_id: str
    protocol_id: str
    mode: str
    final_deal: Deal
    final_payoffs: dict[str, float]
    final_batnas: dict[str, float]
    actors_below_batna: list[str]
    turns: list[Turn] = field(default_factory=list)
    converged: bool = False


# ---------------------------------------------------------------------------
# Heuristic agent
# ---------------------------------------------------------------------------


def _heuristic_proposal(actor: str, deal: Deal, data: Data) -> Turn:
    """Pick the issue where this actor has the highest weight and is currently
    *worst off* (furthest from their ideal), and propose a step toward their
    ideal, within red-line bounds.

    Deterministic given (actor, deal, data) — no randomness.
    """
    best_issue: Issue | None = None
    best_weight: float = 0.0
    best_target: float = 0.0

    for issue_id, issue in data.issues.items():
        pos = data.position(actor, issue_id)
        if pos is None or pos.weight <= 0:
            continue
        direction = issue.direction_for.get(actor, 0)
        if direction == 0:
            continue
        current = deal[issue_id]
        # how far is current from this actor's ideal extreme?
        if direction > 0:
            slack = issue.hi - current
        else:
            slack = current - issue.lo
        # weight × slack heuristic — issues with high weight + lots of room to gain
        score = pos.weight * (slack / issue.width if issue.width else 0)
        if score > best_weight:
            best_weight = score
            best_issue = issue
            # take a 25% step toward the actor's preferred bound
            if direction > 0:
                proposed = current + 0.25 * (issue.hi - current)
                # don't overrun another actor's red line in the same direction
                proposed = min(proposed, issue.hi)
            else:
                proposed = current - 0.25 * (current - issue.lo)
                proposed = max(proposed, issue.lo)
            best_target = proposed

    if best_issue is None:
        # actor has no stake — just accept
        return Turn(round=0, actor=actor, action="ACCEPT",
                    rationale="no salient issues, content to defer")

    return Turn(
        round=0, actor=actor, action="PROPOSE",
        moves=[{"issue": best_issue.id, "to": float(best_target),
                "rationale": f"high-weight ({best_weight:.1f}) issue, step toward preferred direction"}],
        rationale="heuristic: highest-weight × slack issue, 25% step",
    )


# ---------------------------------------------------------------------------
# API agent (Anthropic SDK) — optional path
# ---------------------------------------------------------------------------


def _build_system_prompt(actor: str, data: Data) -> str:
    """Compose a system prompt for an actor from its data/actors/<actor>.md profile.
    Falls back to a minimal stub if the file is missing.
    """
    profile_path = ROOT / "data" / "actors" / f"{actor}.md"
    if not profile_path.exists():
        return f"You are {actor}. (No detailed profile available.)"
    profile = profile_path.read_text()
    template_path = ROOT / "agents" / "dossiers" / "_template.md"
    template_hint = template_path.read_text() if template_path.exists() else ""
    return (
        "You are the actor described in the following profile. Speak in the "
        "institutional voice of your role under the constraints documented "
        "below. Stay terse and concrete.\n\n"
        f"--- PROFILE ---\n{profile}\n--- /PROFILE ---\n\n"
        "Your output format must follow this protocol description:\n\n"
        f"{template_hint}\n"
    )


def _api_proposal(actor: str, deal: Deal, data: Data, prior_turns: list[Turn]) -> Turn:
    """Ask Claude playing this actor to propose a move on the current deal.
    Requires anthropic package + ANTHROPIC_API_KEY.
    """
    try:
        import anthropic  # type: ignore
    except ImportError:
        raise RuntimeError(
            "API mode requires `anthropic` package. Install with: "
            "`pip install -e '.[agents]'` from the project root."
        )
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable required for --live mode.")

    client = anthropic.Anthropic(api_key=api_key)

    deal_table = "\n".join(
        f"  - {iid}: {deal[iid]:.2f} ({data.issues[iid].units})"
        for iid in data.issues
    )
    summary = summarize(deal, data)
    pa = summary.payoffs.get(actor, 0.0)
    ba = summary.batnas.get(actor, 0.0)

    prior_summary = "\n".join(
        f"  Round {t.round}, {t.actor}: {t.action}" +
        (f" — {t.moves[0]['issue']} → {t.moves[0]['to']:.2f}" if t.moves else "")
        for t in prior_turns[-12:]
    ) or "  (no prior turns this round)"

    user_msg = f"""Current draft deal:
{deal_table}

Your current payoff: {pa:.2f}  (BATNA: {ba:.2f}; surplus: {pa - ba:+.2f})

Recent turns by other actors:
{prior_summary}

Output your action now, strictly as YAML between `---` fences."""

    resp = client.messages.create(
        model="claude-opus-4-7",   # latest Opus per system prompt; switch as needed
        max_tokens=600,
        system=_build_system_prompt(actor, data),
        messages=[{"role": "user", "content": user_msg}],
    )

    text = "".join(b.text for b in resp.content if hasattr(b, "text"))
    return _parse_yaml_action(actor, text)


def _parse_yaml_action(actor: str, text: str) -> Turn:
    """Extract the YAML block from a model response and convert to a Turn."""
    import yaml
    blocks = []
    inside = False
    buf: list[str] = []
    for line in text.splitlines():
        if line.strip() == "---":
            if inside:
                blocks.append("\n".join(buf))
                buf = []
                inside = False
            else:
                inside = True
            continue
        if inside:
            buf.append(line)
    if not blocks:
        return Turn(round=0, actor=actor, action="COUNTER",
                    rationale="response did not contain a valid YAML block")
    try:
        parsed = yaml.safe_load(blocks[0]) or {}
    except yaml.YAMLError as e:
        return Turn(round=0, actor=actor, action="COUNTER",
                    rationale=f"YAML parse error: {e}")
    return Turn(
        round=0,
        actor=actor,
        action=str(parsed.get("action", "COUNTER")).upper(),
        moves=list(parsed.get("moves") or []),
        rationale=str(parsed.get("rationale", "")),
    )


# ---------------------------------------------------------------------------
# Round runner
# ---------------------------------------------------------------------------


def _apply_moves(deal: Deal, moves: list[dict[str, Any]], data: Data) -> Deal:
    """Average new proposals into the running deal. Simple 50/50 mix per moved
    issue — gives the simulation a smoothing dynamic rather than letting any
    single actor dictate."""
    new = dict(deal)
    for m in moves:
        iid = m.get("issue")
        if iid not in data.issues:
            continue
        target = float(m.get("to", deal[iid]))
        issue = data.issues[iid]
        target = max(issue.lo, min(issue.hi, target))
        new[iid] = 0.5 * deal[iid] + 0.5 * target
    return new


def _converged(turns_this_round: list[Turn]) -> bool:
    """Convergence: all participants ACCEPT (or no PROPOSE/COUNTER moved a value)."""
    actions = [t.action for t in turns_this_round]
    if all(a == "ACCEPT" for a in actions):
        return True
    return False


def run(
    scenario_id: str = "status_quo",
    protocol_id: str = "trilateral_us_ch_roche",
    mode: str = "heuristic",
    max_rounds: int = 8,
    seed: int | None = 42,
) -> RunResult:
    data = load_data()
    scenario = get_scenario(scenario_id)
    protocol = get_protocol(protocol_id)

    random.seed(seed)
    deal = scenario.to_deal(data)
    turns: list[Turn] = []
    converged = False

    for r in range(1, max_rounds + 1):
        round_turns: list[Turn] = []
        for actor in protocol.participants:
            if mode == "heuristic":
                t = _heuristic_proposal(actor, deal, data)
            elif mode == "live":
                t = _api_proposal(actor, deal, data, turns)
            else:
                raise ValueError(f"Unknown mode: {mode}")
            t.round = r
            t.payoff_after = payoff(actor, deal, data)
            t.batna = summarize(deal, data).batnas[actor]
            if t.action == "PROPOSE" and t.moves:
                deal = _apply_moves(deal, t.moves, data)
            round_turns.append(t)
            turns.append(t)
        if _converged(round_turns):
            converged = True
            break

    summary = summarize(deal, data)
    return RunResult(
        scenario_id=scenario_id,
        protocol_id=protocol_id,
        mode=mode,
        final_deal=deal,
        final_payoffs=summary.payoffs,
        final_batnas=summary.batnas,
        actors_below_batna=summary.actors_below_batna,
        turns=turns,
        converged=converged,
    )


# ---------------------------------------------------------------------------
# CLI + output
# ---------------------------------------------------------------------------


def _write_transcripts(result: RunResult, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = f"{result.scenario_id}-{result.protocol_id}-{result.mode}-{stamp}"

    # JSON
    json_path = out_dir / f"{base}.json"
    json_path.write_text(json.dumps({
        "scenario_id": result.scenario_id,
        "protocol_id": result.protocol_id,
        "mode": result.mode,
        "converged": result.converged,
        "final_deal": result.final_deal,
        "final_payoffs": result.final_payoffs,
        "final_batnas": result.final_batnas,
        "actors_below_batna": result.actors_below_batna,
        "turns": [dataclasses.asdict(t) for t in result.turns],
    }, indent=2))

    # Markdown transcript
    md_path = out_dir / f"{base}.md"
    md = [f"# Transcript — {result.scenario_id} / {result.protocol_id} / {result.mode}"]
    md.append(f"\n**Converged**: {result.converged}  ·  **Rounds**: {result.turns[-1].round if result.turns else 0}")
    md.append("\n## Turns\n")
    for t in result.turns:
        md.append(f"### Round {t.round} — {t.actor} — {t.action}")
        if t.moves:
            for m in t.moves:
                md.append(f"- propose `{m.get('issue')}` → `{m.get('to')}`  ·  *{m.get('rationale','')}*")
        if t.rationale:
            md.append(f"- {t.rationale}")
        if t.payoff_after is not None and t.batna is not None:
            md.append(f"- payoff {t.payoff_after:+.2f}  (BATNA {t.batna:+.2f})")
        md.append("")
    md.append("## Final deal vector\n")
    for iid, v in result.final_deal.items():
        md.append(f"- `{iid}`: {v:.2f}")
    md.append("\n## Final payoffs vs BATNA\n")
    md.append("| Actor | Payoff | BATNA | Surplus |")
    md.append("|---|---:|---:|---:|")
    for actor in result.final_payoffs:
        p = result.final_payoffs[actor]
        b = result.final_batnas[actor]
        flag = " ✗" if actor in result.actors_below_batna else ""
        md.append(f"| {actor}{flag} | {p:+.2f} | {b:+.2f} | {p - b:+.2f} |")
    md_path.write_text("\n".join(md))

    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m agents.runner", description=__doc__)
    parser.add_argument("--scenario", default="status_quo", choices=list(SCENARIOS.keys()))
    parser.add_argument("--protocol", default="trilateral_us_ch_roche", choices=list(PROTOCOLS.keys()))
    parser.add_argument("--mode", default="heuristic", choices=["heuristic", "live"])
    parser.add_argument("--rounds", type=int, default=6)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=Path, default=ROOT / "agents" / "transcripts")
    args = parser.parse_args(argv)

    print(f"=== {args.scenario} / {args.protocol} / {args.mode} ===")
    result = run(
        scenario_id=args.scenario,
        protocol_id=args.protocol,
        mode=args.mode,
        max_rounds=args.rounds,
        seed=args.seed,
    )
    j, m = _write_transcripts(result, args.out)
    print(f"Converged: {result.converged}  ·  Rounds: {result.turns[-1].round if result.turns else 0}")
    print(f"Actors below BATNA: {result.actors_below_batna or 'none'}")
    print(f"JSON: {j}")
    print(f"Markdown: {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
