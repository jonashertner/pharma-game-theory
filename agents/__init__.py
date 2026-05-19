"""Multi-agent simulation harness (Phase D).

Two run modes:
  - Heuristic (default, no API key): each actor moves issues toward its
    preferred direction within its weight envelope; converges quickly.
  - API (Anthropic SDK): each actor is an LLM agent with a system prompt
    synthesised from data/actors/<actor>.md plus the dossier template.

Both modes emit:
  - agents/transcripts/<scenario>-<protocol>-<mode>-<timestamp>.json
  - agents/transcripts/<scenario>-<protocol>-<mode>-<timestamp>.md
"""

from .runner import run, RunResult
from .protocols import Protocol, PROTOCOLS

__all__ = ["run", "RunResult", "Protocol", "PROTOCOLS"]
