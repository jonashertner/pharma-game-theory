# Game model (Phase B)

Formal payoff model for the Roche pharma-pricing negotiation. Reads the
sourced knowledge base from `data/` and turns it into actor utility functions
plus a small library of equilibrium solvers.

## Design choices

- **Linear in normalised issue value × actor weight × direction.** Simple,
  inspectable, monotone by construction. Red-line violations apply a single
  hard penalty below BATNA. We do not fit a nonlinear surface; if a kink is
  needed, add it explicitly as a piecewise linear segment with a citation in
  positions.yaml.
- **Grid search, not gradient descent.** The design space is conceptual not
  numeric. A linear objective on a hyper-rectangle has its optimum at a
  vertex, and a small grid captures most realistic mid-points. If you need
  finer resolution, raise `n_per_issue`.
- **Multiple solution concepts.** Each diagnoses a different question:
  - **Nash bargaining (asymmetric):** efficient compromise weighted by
    importance.
  - **Kalai–Smorodinsky:** proportional gain, fairer than Nash.
  - **Shapley values:** who marginally contributes to the negotiation
    surplus? Surfaces *who is loud but contributes little*, vs *who is
    quiet but pivotal*.
  - **Core check:** is the proposed deal stable, or would some sub-coalition
    rather walk?

## CLI

From the repo root (with deps installed):

```bash
python -m model                       # status_quo, payoffs only
python -m model status_quo --concept all
python -m model mfn_hardline --concept nash
python -m model basel_relocation_stress --concept ks
python -m model --list
```

## Files

| File | Responsibility |
|---|---|
| `data.py` | Load `data/issues.yaml` and `data/positions.yaml` into typed structs |
| `payoffs.py` | `payoff(actor, deal, data) -> float`; red-line aware |
| `equilibria.py` | Nash, KS, Shapley, core, Pareto frontier |
| `scenarios.py` | Named scenarios |
| `__main__.py` | CLI entry |
| `tests/` | pytest: monotonicity, BATNA dominance, red-line penalty, Genentech calibration |

## Intended use

- The **playground** (Phase C) embeds a JS port of `payoffs.py` for live
  sliders. Whenever the YAML files change, the playground re-generates its
  embedded constants.
- The **agents** harness (Phase D) uses `data.positions` to construct actor
  dossiers and uses `summarize()` to score proposals.
- The **memo** generator (Phase E) reads the equilibrium outcomes plus the
  novelty engine's idea pool to populate the advisory template.

## Known limits

- The hard red-line penalty is large but finite — search routines should not
  treat `-1000.0` as a numerical bug. It's the design.
- Shapley over 12 actors is 4096 coalitions; at `n_per_issue=2` it runs in a
  few seconds. At `n_per_issue=3` it takes ~1 minute. For interactive use,
  prefer 2.
- The `_default_weights` for Nash bargaining proxies leverage by mean
  importance weight. That's a placeholder — a more principled weighting
  would use coalition-formation theory. See the open decision in the plan.
