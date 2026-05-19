# Roche pharma-pricing negotiation — game-theoretic simulation

A research-grounded, multi-actor game-theoretic simulation of the live
mid-2026 negotiation Roche is inside: MFN drug pricing, IRA Medicare
price-setting (Rounds 1–3, with Xolair in Round 3 for 2028 effect), Section
232 pharma tariffs, the November 2025 US–Swiss tariff/trade framework, and
the cluster of payer / competitor / Swiss-host / patient actors that shape
every bilateral conversation.

**Endgoal:** produce input Roche could plausibly use to navigate this game
toward an outcome each principal can frame as a reasonable win.

**Snapshot date:** 2026-05-19.

---

## Two ways to run this

### 1. Locally (for development + verification)

```bash
# Verify the model is calibrated (tests pass against the actual signed state)
python -m pytest model/tests/

# Status-quo equilibrium prediction
python -m model status_quo --concept all

# A multi-agent heuristic negotiation (no API key needed)
python -m agents.runner --scenario status_quo --protocol trilateral_us_ch_roche

# Generate a memo for Roche
python -m memo.generator --scenario status_quo --equilibrium nash

# Generate collision prompts from the novelty engine
python -m novelty.collide --scenario status_quo --domains reinsurance-pooling

# Open the interactive playground
open playground/index.html
```

For API-mode agents (Claude as each actor), install the optional dep:

```bash
pip install -e '.[agents]'
export ANTHROPIC_API_KEY=...
python -m agents.runner --mode live --protocol trilateral_us_ch_roche
```

### 2. As a deployment site (for board presentation)

A polished, passcode-gated static site lives under `docs/`:

```bash
# Rebuild the site (idempotent)
python tools/build_site.py

# Preview locally
cd docs && python -m http.server 8000
# Open http://localhost:8000
```

The site has:

- **Live simulation page** — 18-event voiced trilateral negotiation with typed
  statements, animated deal vector, actor highlighting
- **Recommendation page** — auto-populated Roche-facing advisory memo
- **Playground** — interactive sliders + live payoff updates
- **Actors browser** — 12 sourced profiles with citation lists
- **Positions matrix** — 12 × 13 grid with per-cell expansion
- **Prompts browser** — 15 distant analogue domains for the novelty engine
- **Transcripts browser** — past simulation runs
- **Method page** — game-theoretic backbone + calibration claim

To deploy to GitHub Pages with passcode gate, see [DEPLOYMENT.md](DEPLOYMENT.md).
Three paths offered: public repo (weak), private repo (better), Cloudflare
Access (strongest). **Read the strategic question at the top of DEPLOYMENT.md
before pushing — making this site public has counterparty-information
implications.**

To change the passcode:

```bash
python tools/set_passcode.py            # interactive
python tools/build_site.py              # rebuild
```

---

## Repository layout

```
data/          Phase A — sourced knowledge base
  actors/      12 actor profiles (~15-24KB each, every position cited)
  issues.yaml  13 negotiation issues, units, ranges, per-actor direction signs
  positions.yaml  110 (actor, issue) position cells with BATNA, red lines, weights
  timeline.yaml   24 dated events through 2029

model/         Phase B — game-theoretic core
  payoffs.py     Linear-with-red-line-kinks payoff functions
  equilibria.py  Nash bargaining, Kalai-Smorodinsky, Shapley, core check
  scenarios.py   6 named scenarios
  tests/         11 passing + 1 skipped (calibration verified)

playground/    Phase C — interactive sliders + Pareto-aware payoff bars

agents/        Phase D — multi-agent harness
  runner.py    Heuristic (default) and `--live` API modes
  protocols.py 5 protocols (bilateral, trilateral, swiss-internal, full, coalition)
  dossiers/    System-prompt template + per-actor dossier source

novelty/       Cross-cutting — open-collider-style domain-collision module
  domains.yaml  15 distant analogue domains with operational principles
  collide.py    Builds Claude-ready collision prompts

memo/          Phase E — advisory memo generator
  template.md   Roche-facing memo structure
  generator.py  Populates template from scenario + model + Nash/KS outcome
  drafts/       Generated memo drafts (timestamped)

simulations/   Curated voiced simulation transcripts (centerpiece of the site)
  status-quo-trilateral.json    18 events, 6 rounds, hand-written statements
  simulation.html               Playback UI (source; copied to docs/ at build)

docs/          Phase C — deployment site (built by tools/build_site.py)
tools/         Build + passcode tools
.github/workflows/  GitHub Actions deployment
```

## Sourcing discipline

Every claim about an actor's position cites a public statement (regulatory
filing, earnings call, press release, court filing, official document,
reputable news). Training-data memory is not a source. Citations are dated
and linked. See `data/actors/<actor>.md` for each actor's sources block.

Positions marked `inferred: true` in `data/positions.yaml` are ones where no
direct public statement supports the position; they are flagged as such in
the site's positions matrix.

## Calibration claim

The test suite verifies:

- Every actor's payoff function is monotone in their preferred direction.
- BATNA payoffs are correctly computed and clipped against the actor's own red lines.
- Red-line violations produce a sub-BATNA penalty.
- **The actual May 2026 status-quo state is feasible under the model.**
  This is the headline calibration: if it weren't, the model would be over-constrained.

Run: `python -m pytest model/tests/`

## Plan + history

See `/Users/jonashertner/.claude/plans/ultrathink-goal-is-to-reflective-cocoa.md`
for the full design spec.

## Limits

- Linear payoffs with hard red-line kinks; no nonlinear bargaining dynamics.
- Confidential net prices (PBM rebates, EU MEAs) not directly visible.
- Live simulation page plays back a hand-curated transcript with voiced
  statements written to match each actor's documented positions; it is
  illustrative, not predictive. For non-deterministic exploratory runs use
  `agents/runner.py --mode live`.
