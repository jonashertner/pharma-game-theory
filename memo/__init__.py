"""Phase E: advisory synthesis — Roche-facing memo generator.

Reads model outputs + actor profiles + scenario + (optional) novelty ideas;
populates memo/template.md into memo/drafts/<scenario>-<concept>-<ts>.md.
"""

from .generator import generate

__all__ = ["generate"]
