"""Build the static deployment site under `docs/`.

Outputs:
  docs/index.html              — landing dashboard with all entry points
  docs/recommendation.html     — Roche-facing advisory memo (auto-populated)
  docs/simulation.html         — live simulation playback (centerpiece)
  docs/playground.html         — interactive playground
  docs/actors.html             — browser for the 12 actor profiles
  docs/positions.html          — flat 12×13 positions matrix
  docs/prompts.html            — novelty-engine collision prompts browser
  docs/transcripts.html        — agent-simulation transcripts browser
  docs/method.html             — methodology + calibration + limits
  docs/simulations/*.json      — simulation data files
  docs/assets/style.css        — shared stylesheet (committed)
  docs/assets/passcode.js      — gate JS (committed)

Run:
  python tools/build_site.py

The build is hermetic (no network) and idempotent.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

import markdown   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DOCS = ROOT / "docs"
DATA = ROOT / "data"
PLAYGROUND_SRC = ROOT / "playground" / "index.html"
SIMULATION_SRC = ROOT / "simulations" / "simulation.html"
SIMULATIONS_DIR = ROOT / "simulations"

from model.data import load_data   # noqa: E402
from model.payoffs import payoff, summarize, batna_payoffs   # noqa: E402
from model.scenarios import SCENARIOS, get_scenario   # noqa: E402


DISPLAY_NAMES = {
    "roche": "Roche / Genentech",
    "us-executive": "US Executive",
    "us-congress": "US Congress",
    "swiss-federal-council": "Swiss Federal Council",
    "swiss-cantons-basel": "Swiss Cantons (Basel)",
    "swiss-public-and-domestic-payers": "Swiss public & payers",
    "novartis": "Novartis",
    "pbms-and-payers": "US PBMs & payers",
    "patient-advocacy": "US patient advocacy",
    "eu-reference-pricing": "EU reference pricing",
    "biosimilars-competitors": "Biosimilars",
    "investors": "Investors",
}


# Each nav entry: (href, label, primary?). Primary items are shown inline
# on wide laptops; all items are accessible via the Menu overlay and Cmd+K.
NAV_GROUPS = [
    ("Read", [
        ("one-pager.html", "One-pager", True),
        ("briefing.html", "Executive briefing", True),
        ("bottom-line.html", "Bottom line", True),
        ("black-swans.html", "Black swans", True),
        ("financial-translation.html", "Financial translation", True),
        ("decision-quality.html", "Decision quality", False),
        ("peer-comparison.html", "Peer comparison", False),
        ("board-qa.html", "Board Q&A", False),
        ("index.html", "Overview", False),
        ("recommendation.html", "Recommendation", False),
        ("item-1.html", "Item 1 unpacked", False),
        ("adversarial.html", "Red team", False),
        ("cross-domain.html", "Cross-domain", False),
        ("cross-domain-depth.html", "Cross-domain (depth)", False),
        ("ai-implications.html", "AI implications", False),
        ("dynamics.html", "Dynamics", False),
        ("disclosures.html", "Disclosures", False),
        ("mfn-deals.html", "MFN deals", False),
        ("global-pricing.html", "Global pricing", False),
    ]),
    ("Explore", [
        ("simulation.html", "Live simulation", True),
        ("playground.html", "Playground", True),
    ]),
    ("Reference", [
        ("actors.html", "Actors", True),
        ("positions.html", "Positions", False),
        ("prompts.html", "Prompts", False),
        ("glossary.html", "Glossary", False),
        ("method.html", "Method", False),
    ]),
]
NAV_LINKS = [(href, label) for _, group in NAV_GROUPS for href, label, _ in group]


def _pagination(page_id: str) -> str:
    """Render prev/next pagination links for the given page."""
    idx = next((i for i, (h, _) in enumerate(NAV_LINKS) if h == page_id), None)
    if idx is None:
        return ""
    parts = ['<div class="page-pagination">']
    if idx > 0:
        prev_href, prev_label = NAV_LINKS[idx - 1]
        parts.append(
            f'<a class="prev" href="{prev_href}">'
            f'<div class="label">Previous</div>'
            f'<div class="title">{prev_label}</div></a>'
        )
    else:
        parts.append('<div></div>')
    if idx < len(NAV_LINKS) - 1:
        next_href, next_label = NAV_LINKS[idx + 1]
        parts.append(
            f'<a class="next" href="{next_href}">'
            f'<div class="label">Next</div>'
            f'<div class="title">{next_label}</div></a>'
        )
    else:
        parts.append('<div></div>')
    parts.append('</div>')
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Shared layout
# ---------------------------------------------------------------------------


def layout(*, title: str, page_id: str, body: str, main_class: str = "prose",
           extra_head: str = "", include_pagination: bool = True) -> str:
    # Inline desktop nav shows PRIMARY items only (compact even on laptops).
    # Menu overlay (formerly mobile-nav) shows everything grouped.
    inline_links = []
    overlay_groups = []
    for gname, group in NAV_GROUPS:
        m_links = [f'<div class="mobile-group-head">{gname}</div>']
        for href, label, primary in group:
            active = ' class="active"' if href == page_id else ""
            if primary:
                inline_links.append(f'<a href="{href}"{active}>{label}</a>')
            m_links.append(f'<a href="{href}"{active}>{label}</a>')
        overlay_groups.append("\n      ".join(m_links))
    desktop_nav = "\n        ".join(inline_links)
    mobile_nav = "\n      ".join(overlay_groups)
    snapshot = "20 May 2026"

    pagination = _pagination(page_id) if include_pagination and page_id != "index.html" else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} — Roche pharma-pricing negotiation</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<script src="assets/passcode.js"></script>
<script src="assets/commandk.js" defer></script>
<script src="assets/toc.js" defer></script>
{extra_head}
</head>
<body>

<input type="checkbox" id="mobile-menu-toggle" class="mobile-toggle" aria-label="Toggle menu">

<header class="site-header">
  <div class="inner">
    <a href="index.html" class="brand">Roche negotiation</a>
    <nav class="desktop-nav" aria-label="Primary navigation">
        {desktop_nav}
    </nav>
    <div class="nav-actions">
      <button id="palette-trigger" class="palette-trigger" type="button" aria-label="Search the site">
        <span class="label">Search</span>
        <kbd>⌘K</kbd>
      </button>
      <label for="mobile-menu-toggle" class="menu-toggle" aria-label="Open menu" role="button" tabindex="0">
        <span class="menu-toggle-label">Menu</span>
        <span class="bars" aria-hidden="true"></span>
      </label>
    </div>
  </div>
</header>

<nav class="mobile-nav" aria-label="Mobile navigation">
      {mobile_nav}
      <div class="meta-line">snapshot {snapshot}</div>
</nav>

<main id="main-content" class="{main_class}" tabindex="-1">
{f'<a href="index.html" class="back-link">Overview</a>' if page_id != "index.html" else ""}
{body}
{pagination}
</main>

<footer class="site-footer">
  <div class="inner">
    <span>Independent public-source analysis · snapshot {snapshot} · restricted access</span>
    <span>Not an official Roche document · <a href="method.html">method &amp; limits</a></span>
  </div>
</footer>

<script>
// Close mobile menu when a link is tapped.
document.querySelectorAll(".mobile-nav a").forEach(a => {{
  a.addEventListener("click", () => {{
    document.getElementById("mobile-menu-toggle").checked = false;
  }});
}});
</script>

</body>
</html>
"""


def render_md(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists", "tables", "toc"],
        output_format="html5",
    )


# ---------------------------------------------------------------------------
# Executive summaries
# ---------------------------------------------------------------------------


def exec_summary(head: str, title: str, body_html: str) -> str:
    """Render an executive-summary callout block."""
    return f"""
<div class="exec-summary">
  <div class="head">{head}</div>
  <h3>{title}</h3>
  {body_html}
</div>
"""


def load_actor_snapshots() -> dict:
    import yaml
    path = DATA / "actor_snapshots.yaml"
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()).get("snapshots", {})


def actor_snapshot_block(snapshot: dict) -> str:
    if not snapshot:
        return ""
    return f"""
<div class="actor-snapshot">
  <div class="one-liner">{snapshot.get('one_liner', '')}</div>
  <dl>
    <dt>Top priority</dt><dd>{snapshot.get('top_priority', '—')}</dd>
    <dt>Walks if</dt><dd>{snapshot.get('walks_if', '—')}</dd>
    <dt>Leverage</dt><dd>{snapshot.get('leverage', '—')}</dd>
    <dt>What Roche should do</dt><dd class="action">{snapshot.get('what_roche_should_do', '—')}</dd>
  </dl>
</div>
"""


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------


def build_index() -> str:
    data = load_data()
    sq = get_scenario("status_quo")
    summary = summarize(sq.to_deal(data), data)
    n_actors = len(data.actors)
    n_issues = len(data.issues)
    n_positions = len(data.positions)
    n_below = len(summary.actors_below_batna)
    # Strict-vs-equal partition for calibration narrative
    surplus_by_actor = {a: summary.payoffs.get(a, 0.0) - summary.batnas.get(a, 0.0)
                       for a in data.actors}
    n_strictly_above = sum(1 for s in surplus_by_actor.values() if s > 1e-9)
    n_exactly_at = sum(1 for s in surplus_by_actor.values() if abs(s) <= 1e-9)
    actors_above = [a for a, s in surplus_by_actor.items() if s > 1e-9]
    actors_at = [a for a, s in surplus_by_actor.items() if abs(s) <= 1e-9]

    overview_exec = exec_summary(
        "In 30 seconds",
        "What this is and what to do with it",
        """
<ul>
<li><strong>What this is:</strong> a sourced, citation-backed model of the live 2026 US pharma-pricing negotiation. 12 actors, 13 issues, 110 position cells; calibrated against the actual December 2025 Genentech MFN deal.</li>
<li><strong>The model's headline finding:</strong> the May 2026 status quo is feasible but <em>fragile</em> &mdash; 6 of 12 actors clear BATNA with positive surplus (Roche, Swiss FC, Swiss cantons, Swiss public payers, Novartis, investors); the other 6 (including both US actors) sit exactly at BATNA. A small perturbation tips the at-BATNA cluster into political-pressure mode.</li>
<li><strong>Best move for Roche:</strong> strengthen the international reference-pricing firewall via the Swiss annex (Roche's highest-weight issue, currently underused). Don't volunteer concessions on MFN coverage or TrumpRx SKU count.</li>
<li><strong>Biggest tail risk:</strong> MFN reference-basket contagion into EU/UK/CH. Treat as tail-risk insurance, not expected-value optimisation.</li>
<li><strong>How to use this site:</strong> the <a href="simulation.html">live simulation</a> walks through a curated trilateral negotiation. The <a href="playground.html">playground</a> lets you stress-test the model interactively. The <a href="recommendation.html">recommendation</a> is the headline output.</li>
</ul>
""",
    )

    body = f"""
<section class="hero">
  <div class="tag">Multi-actor game-theoretic simulation · snapshot 2026-05-19</div>
  <h1>Roche is inside the negotiation. The question is which deal architecture survives.</h1>
  <p class="lead">
    Genentech signed an MFN deal in December 2025. The November 2025 US&ndash;Swiss
    framework caps Section&nbsp;232 pharma tariffs at 15% with a 0% track through
    January 2029 for firms building US capacity. IRA Round&nbsp;3 places Xolair
    under negotiation effective January 2028. <strong>The model says the May 2026
    status quo is barely feasible: 6 of 12 actors (Roche, both Swiss-side
    principals, Swiss-internal stakeholders, Novartis, investors) clear BATNA
    with positive surplus; the other 6 &mdash; including, notably, both US
    actors &mdash; sit exactly at BATNA. The system is fragile, not stable.</strong>
  </p>
  <div class="reading-paths">
    <div class="path"><span class="t">5 min</span> <a href="recommendation.html">read the recommendation</a></div>
    <div class="path"><span class="t">15 min</span> <a href="dynamics.html">read the strategic dynamics</a></div>
    <div class="path"><span class="t">10 min</span> <a href="simulation.html">watch the simulation</a></div>
    <div class="path"><span class="t">2 hours</span> <a href="actors.html">read all 12 actor profiles</a></div>
  </div>
</section>

{overview_exec}

<h2 class="no-rule">The twelve actors at the table</h2>
<p>Three principals at the table. Nine affected non-participants. Each labelled with the dusty accent colour used elsewhere on the site for visual continuity.</p>

<figure class="actor-map" aria-label="Diagram of the twelve actors in the negotiation">
  <div class="actor-map-grid">
    <div class="map-col principal">
      <div class="col-header">Principals</div>
      <div class="map-actor" style="--c:var(--actor-roche);"><span class="dot"></span><a href="actors.html#roche">Roche / Genentech</a></div>
      <div class="map-actor" style="--c:var(--actor-us-exec);"><span class="dot"></span><a href="actors.html#us-executive">US Executive</a></div>
      <div class="map-actor" style="--c:var(--actor-ch-fed);"><span class="dot"></span><a href="actors.html#swiss-federal-council">Swiss Federal Council</a></div>
    </div>
    <div class="map-col affected">
      <div class="col-header">Directly affected</div>
      <div class="map-actor" style="--c:var(--actor-investor);"><span class="dot"></span><a href="actors.html#investors">Investors (family-held)</a></div>
      <div class="map-actor" style="--c:var(--actor-novartis);"><span class="dot"></span><a href="actors.html#novartis">Novartis</a></div>
      <div class="map-actor" style="--c:var(--actor-us-cong);"><span class="dot"></span><a href="actors.html#us-congress">US Congress</a></div>
      <div class="map-actor" style="--c:var(--actor-pbm);"><span class="dot"></span><a href="actors.html#pbms-and-payers">US PBMs &amp; payers</a></div>
      <div class="map-actor" style="--c:var(--actor-ch-cantons);"><span class="dot"></span><a href="actors.html#swiss-cantons-basel">Swiss Cantons (Basel)</a></div>
      <div class="map-actor" style="--c:var(--actor-ch-public);"><span class="dot"></span><a href="actors.html#swiss-public-and-domestic-payers">Swiss public &amp; payers</a></div>
    </div>
    <div class="map-col observers">
      <div class="col-header">Observers / contingent</div>
      <div class="map-actor" style="--c:var(--actor-patient);"><span class="dot"></span><a href="actors.html#patient-advocacy">US patient advocacy</a></div>
      <div class="map-actor" style="--c:var(--actor-eu);"><span class="dot"></span><a href="actors.html#eu-reference-pricing">EU reference pricing</a></div>
      <div class="map-actor" style="--c:var(--actor-biosim);"><span class="dot"></span><a href="actors.html#biosimilars-competitors">Biosimilar manufacturers</a></div>
    </div>
  </div>
  <figcaption>Click any actor for the sourced profile. Issues connecting them are documented in <a href="positions.html">the positions matrix</a>.</figcaption>
</figure>

<section class="board-decisions" id="agenda" aria-label="Board agenda">
  <div class="head">Board agenda</div>
  <h2 class="no-rule" style="margin-top:6px;">Items for the next board meeting</h2>
  <ol class="decision-list">
    <li class="required">
      <span class="tag-label accent">Item 1 · Decision required</span>
      <strong>Endorse the firewall-annex approach</strong> as the primary 2026 negotiating priority &mdash; explicitly above MFN-coverage expansion or TrumpRx SKU growth.
    </li>
    <li class="required">
      <span class="tag-label accent">Item 2 · Decision required</span>
      <strong>Authorize capital-allocation flexibility</strong> for capex milestone acceleration (up to +$5B over 2025–2027) to enable EPC-milestone-gated Section&nbsp;232 protection.
    </li>
    <li class="discretionary">
      <span class="tag-label warn">Item 3 · Discussion</span>
      <strong>Decide or defer on the patient-access OOP cap</strong> for Genentech specialty drugs above $30K list. Defer to Q4 2026 pending CMS rulemaking signals, or commit early at executive discretion.
    </li>
    <li class="note-only">
      <span class="tag-label">Item 4 · For information</span>
      <strong>Note the tail-risk hedge structure</strong> (reinsurance-style global-spillover insurance) as an exploratory Q1 2027 workstream.
    </li>
  </ol>
  <p style="margin-top:18px;font-size:14px;color:var(--muted);">Pre-read for items 1–4: the board memo at <a href="recommendation.html">recommendation</a>. Adversarial review of each item with named contingencies: <a href="adversarial.html">red team</a>. The actor-level substrate &mdash; telos, contradictions, unexpected alliances: <a href="dynamics.html">strategic dynamics</a>.</p>
</section>

<h2 style="margin-top: 14px;">Where to go</h2>

<div class="card-grid">
  <a class="card" href="simulation.html">
    <h3>▶ Live simulation</h3>
    <p>Watch the trilateral US&nbsp;↔&nbsp;CH&nbsp;↔&nbsp;Roche negotiation play out in 18 voiced events across 6 rounds. Each statement is tied to a sourced position. Deal vector animates as actors propose.</p>
    <div class="arrow">Watch it play out →</div>
  </a>
  <a class="card" href="recommendation.html">
    <h3>Recommended deal architecture</h3>
    <p>The model's Nash-bargaining recommendation: where the principal triple can sign without breaking the fragile equilibrium, with sequencing and walk-risks per actor.</p>
    <div class="arrow">Read the recommendation →</div>
  </a>
  <a class="card" href="playground.html">
    <h3>Interactive playground</h3>
    <p>Adjust each of the 13 issues with sliders; watch feasibility and payoffs update live. Generate Claude prompts that collide the scenario with distant analogue domains.</p>
    <div class="arrow">Open the playground →</div>
  </a>
  <a class="card" href="actors.html">
    <h3>The 12 actors at the table</h3>
    <p>Sourced profiles — Roche, US Executive (six sub-agencies), Congress, three Swiss-side stakeholder layers, Novartis, PBMs, patient advocacy, EU reference pricing, biosimilars, investors.</p>
    <div class="arrow">Browse the actors →</div>
  </a>
  <a class="card" href="positions.html">
    <h3>Positions matrix</h3>
    <p>The full 12 × 13 grid of actor positions, BATNAs, red lines, weights, and citations. Every cell either cites a public source or is explicitly marked inferred.</p>
    <div class="arrow">View the matrix →</div>
  </a>
  <a class="card" href="prompts.html">
    <h3>Novelty-engine prompts</h3>
    <p>The 15-domain collision pool — climate-finance NDC bargaining, reinsurance pooling, antitrust consent decrees, sovereign-debt restructuring, salmon catch-share, more. Generate Claude prompts that surface non-obvious moves.</p>
    <div class="arrow">Browse the domains →</div>
  </a>
  <a class="card" href="transcripts.html">
    <h3>Simulation transcripts</h3>
    <p>Past multi-agent runs across scenarios and protocols (bilateral, trilateral, full multilateral, Swiss internal coherence). JSON + Markdown.</p>
    <div class="arrow">Browse transcripts →</div>
  </a>
  <a class="card" href="method.html">
    <h3>Method &amp; calibration</h3>
    <p>The game-theoretic backbone, why the model is calibrated, what it cannot see, and how to re-run it. Includes the verifiable status-quo calibration test.</p>
    <div class="arrow">How it works →</div>
  </a>
</div>

<h2>What the model is telling Roche</h2>

<p>
The negotiation that closed in December 2025 produced a deal where six actors
clear BATNA with positive surplus (Roche, the Swiss Federal Council, Swiss cantons-Basel,
Swiss public payers, Novartis, investors) and six sit exactly at theirs &mdash;
including, notably, the US Executive and US Congress. The US-side &ldquo;at BATNA&rdquo;
result says the US was essentially indifferent between the signed deal and no deal at all:
the political pressure points the Administration cared about (manufacturers signing
publicly, MFN-Medicaid access) were resolved either way. A small perturbation in any
direction tips the at-BATNA cluster into walk territory and the deal becomes
politically expensive to defend.
</p>

<p>Three implications follow.</p>

<ol>
<li><strong>Don't volunteer concessions.</strong> The current Section&nbsp;232 0% track and
the Swiss framework annex are already extracting close to the maximum Roche
can give while keeping the principal triple aligned. Voluntary moves on
MFN coverage, TrumpRx SKU count, or pipeline-pricing protocols open
unforced losses without picking up new value.</li>

<li><strong>The most underused lever is the international-reference-pricing firewall.</strong>
This is Roche's highest-weight issue (10/10) where current value (3/10) sits
well below the achievable bound. Strengthening it through bilateral confidentiality
provisions in the Swiss annex, mirroring Germany's January 2025 Medical Research
Act mechanics, costs the US administration little and protects what matters most
to Roche.</li>

<li><strong>Tail risk &gt; expected loss.</strong> MFN's worst case is not the
direct US-channel price cut. It is reference-basket contagion into EU/UK/CH
contracts via PBM rebate transparency leaks. Treat this as a tail-risk
insurance problem &mdash; reinsurance-pool, sovereign-debt-style comparable-treatment,
or hostage-negotiation face-saving mechanisms (see <a href="prompts.html">novelty
engine</a>) cap downside in ways the current deal doesn't.</li>
</ol>

<div class="callout warn">
  <strong>This is independent, public-source analysis.</strong> It is not a
  Roche-internal document, contains no NDA-protected information, and reflects
  only what is verifiable in regulatory filings, earnings calls, press releases,
  official documents, and reputable news as of 19 May 2026. Where a position
  is inferred without a direct public statement, it is marked as such in the
  <a href="positions.html">positions matrix</a>.
</div>

<h2>Calibration: the model is not making it up</h2>

<p>
The headline test: ask the model to score the deal Roche actually signed
in December 2025. If the signed state were infeasible (i.e., the model predicted
Roche should have walked from a deal it signed), the model would be unusable.
</p>

<p>
<strong>Result: all {n_actors} actors satisfy at-or-above BATNA. The deal is feasible (in the core). ✓</strong>
Of those, <strong>{n_strictly_above} sit <em>strictly above</em></strong>
(Roche, Swiss Federal Council, Swiss cantons-Basel, Swiss public payers, Novartis, investors)
&mdash; this is the &ldquo;winners&rdquo; cluster. The other <strong>{n_exactly_at} sit
<em>exactly at</em></strong> BATNA &mdash; including, notably, US Executive and US Congress.
That cluster predicts where political pressure will appear: actors with no positive
surplus from the signed state have no Dec-2025-deal-aligned incentive to defend it.
</p>

<table>
  <tr><th>Coverage</th><th class="num">Count</th></tr>
  <tr><td>Sourced actor profiles</td><td class="num">{n_actors}</td></tr>
  <tr><td>Negotiation issues modeled</td><td class="num">{n_issues}</td></tr>
  <tr><td>Sourced (actor, issue) position cells</td><td class="num">{n_positions}</td></tr>
  <tr><td>Dated timeline events through 2029</td><td class="num">24</td></tr>
  <tr><td>Equilibrium concepts solved</td><td class="num">4</td></tr>
  <tr><td>Distant analogue domains (novelty engine)</td><td class="num">15</td></tr>
  <tr><td>Curated simulation events (trilateral)</td><td class="num">18</td></tr>
</table>
"""
    return layout(title="Overview", page_id="index.html", body=body, main_class="prose")


def build_recommendation() -> str:
    """Hand-crafted board memo as the primary recommendation page."""
    memo_path = ROOT / "memo" / "board-recommendation.md"
    rendered = render_md(memo_path.read_text())

    body = f"""
<div class="prose-article">
{rendered}
</div>

<div class="callout">
  Looking for the auto-generated analytical detail? See <a href="recommendation-detail.html">the analytical appendix</a> — model-populated tables, principal-by-principal payoff calculations, and sensitivity analysis derived directly from the simulation.
</div>
"""
    return layout(title="Recommendation", page_id="recommendation.html",
                  body=body, main_class="prose")


def build_recommendation_detail() -> str:
    """The auto-generated detail page (the prior recommendation.html)."""
    drafts_dir = ROOT / "memo" / "drafts"
    md_files = sorted(drafts_dir.glob("status_quo-*.md"), reverse=True)
    if not md_files:
        from memo.generator import generate as gen_memo
        gen_memo("status_quo", "nash")
        md_files = sorted(drafts_dir.glob("status_quo-*.md"), reverse=True)
    latest = md_files[0]
    memo_html = render_md(latest.read_text())

    body = f"""
<div class="memo-meta">
  <strong>Auto-generated from:</strong> <code>{latest.relative_to(ROOT)}</code>
  &nbsp;·&nbsp; <strong>Equilibrium concept:</strong> Nash bargaining (asymmetric)
  &nbsp;·&nbsp; <strong>Source of truth:</strong> the <a href="recommendation.html">board recommendation</a>
</div>

<div class="callout warn">
  This is the <strong>analytical appendix</strong> — auto-populated from the model's outputs.
  For the board-facing recommendation written for executive committee consumption, see
  <a href="recommendation.html">the recommendation page</a>.
</div>

{memo_html}
"""
    return layout(title="Analytical appendix", page_id="",
                  body=body, main_class="prose")


def build_dynamics() -> str:
    """The strategic-dynamics page — telos, contradictions, alliances per actor."""
    dyn_path = ROOT / "memo" / "strategic-dynamics.md"
    rendered = render_md(dyn_path.read_text())

    body = f"""
<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="Strategic dynamics", page_id="dynamics.html",
                  body=body, main_class="prose")


def build_disclosures() -> str:
    """Disclosures register — catalogue of SEC + US gov filings driving the regime."""
    disc_path = ROOT / "memo" / "disclosures-register.md"
    rendered = render_md(disc_path.read_text())

    body = f"""
<div class="callout">
  Every entry below links to the primary source — Federal Register, SEC EDGAR,
  congress.gov, the agency that issued the document, or major-newswire coverage
  where direct access was not available. Read this when a recommendation rests
  on a specific filing and you want to verify it yourself.
</div>

<div class="prose-article disclosures-article">
{rendered}
</div>
"""
    return layout(title="Disclosures register", page_id="disclosures.html",
                  body=body, main_class="prose")


def build_global_pricing() -> str:
    """Global pricing-mechanism map — US/EU/China comparative analysis."""
    gp_path = ROOT / "memo" / "global-pricing-map.md"
    rendered = render_md(gp_path.read_text())

    body = f"""
<div class="callout">
  Comparative analysis of three structurally different national pricing regimes:
  US voluntary manufacturer MFN agreements, EU per-country reference-pricing,
  China NRDL negotiations + Volume-Based Procurement. The artifact makes the
  asymmetries visible &mdash; "MFN" in the Trump-administration sense is a US-only construct.
</div>

<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="Global pricing map", page_id="global-pricing.html",
                  body=body, main_class="prose")


def build_adversarial() -> str:
    """Adversarial review — devil's-advocate against the recommendation."""
    adv_path = ROOT / "memo" / "adversarial-review.md"
    rendered = render_md(adv_path.read_text())
    body = f"""
<div class="callout warn">
  A red-team attack on the board recommendation. Each section names the
  strongest objection a hostile critic would make, what evidence would settle
  the question, and the current verdict. Read this <em>after</em> the
  <a href="recommendation.html">recommendation</a> — it makes more sense
  with the original argument in mind.
</div>

<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="Adversarial review", page_id="adversarial.html",
                  body=body, main_class="prose")


def build_glossary() -> str:
    """Glossary of every acronym and term-of-art used on the site."""
    gloss_path = ROOT / "memo" / "glossary.md"
    rendered = render_md(gloss_path.read_text())
    body = f"""
<div class="callout">
  Plain-English definitions for every acronym, programme, and term-of-art
  used elsewhere on the site &mdash; organised by category and linked
  from any page that introduces a new term.
</div>

<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="Glossary", page_id="glossary.html",
                  body=body, main_class="prose")


def build_cross_domain() -> str:
    """Cross-domain strategy — seven moves derived from far-field analogies."""
    cd_path = ROOT / "memo" / "cross-domain-strategy.md"
    rendered = render_md(cd_path.read_text())
    body = f"""
<div class="callout">
  Seven moves derived from structurally distant analogies — Mandate of Heaven,
  the Hanseatic League, Vickrey mechanism design, the Antarctic Treaty System,
  Maori utu, mycorrhizal forest networks, and wabi-sabi aesthetics. These are
  <em>not alternatives</em> to the board recommendation; they propose to reshape
  the negotiation's structural features that the recommendation takes as given.
  See <a href="cross-domain-depth.html">depth</a> for operational architecture +
  three more moves derived from the meta-pattern.
</div>

<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="Cross-domain strategy", page_id="cross-domain.html",
                  body=body, main_class="prose")


def build_cross_domain_depth() -> str:
    """Cross-domain depth — operational architecture, meta-pattern, three more moves."""
    cd_path = ROOT / "memo" / "cross-domain-depth.md"
    rendered = render_md(cd_path.read_text())
    body = f"""
<div class="callout">
  Companion to <a href="cross-domain.html">cross-domain strategy</a>:
  operational architecture for Vickrey + Hansa + Antarctic-Treaty (drafting-grade
  detail), the meta-pattern that explains <em>why</em> the seven source domains
  generate strategic moves, three additional moves (Federalist Papers,
  Coal & Steel, lex mercatoria), strategic-family clustering, sequencing logic,
  and honest fracture lines for each analogy.
</div>

<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="Cross-domain depth", page_id="cross-domain-depth.html",
                  body=body, main_class="prose")


def build_briefing() -> str:
    """Executive briefing — single board-handout-ready synthesis page."""
    p = ROOT / "memo" / "executive-briefing.md"
    raw_md = p.read_text()
    # The briefing-card div opens with raw HTML; markdown extra extension handles
    # mixed Markdown-in-HTML correctly when md_in_html is enabled.
    rendered = markdown.markdown(
        raw_md,
        extensions=["extra", "sane_lists", "tables", "toc", "md_in_html"],
        output_format="html5",
    )
    body = f"""
<div class="prose-article briefing-article">
{rendered}
</div>
"""
    return layout(title="Executive briefing", page_id="briefing.html",
                  body=body, main_class="wide", include_pagination=False)


def build_decision_quality() -> str:
    """Decision quality — Bayesian decision framework for board agenda."""
    p = ROOT / "memo" / "decision-quality.md"
    rendered = markdown.markdown(
        p.read_text(),
        extensions=["extra", "sane_lists", "tables", "toc", "md_in_html"],
        output_format="html5",
    )
    body = f"""
<div class="prose-article decision-quality-article">
{rendered}
</div>
"""
    return layout(title="Decision quality", page_id="decision-quality.html",
                  body=body, main_class="wide", include_pagination=False)


def build_peer_comparison() -> str:
    """Peer comparison — Roche vs 7 global pharma peers across 8 vectors."""
    p = ROOT / "memo" / "peer-comparison.md"
    rendered = markdown.markdown(
        p.read_text(),
        extensions=["extra", "sane_lists", "tables", "toc", "md_in_html"],
        output_format="html5",
    )
    body = f"""
<div class="prose-article peer-comparison-article">
{rendered}
</div>
"""
    return layout(title="Peer comparison", page_id="peer-comparison.html",
                  body=body, main_class="wide", include_pagination=False)


def build_board_qa() -> str:
    """Board Q&A — 15 sharp questions with answers."""
    p = ROOT / "memo" / "board-qa.md"
    rendered = markdown.markdown(
        p.read_text(),
        extensions=["extra", "sane_lists", "tables", "toc", "md_in_html"],
        output_format="html5",
    )
    body = f"""
<div class="prose-article board-qa-article">
{rendered}
</div>
"""
    return layout(title="Board Q&A", page_id="board-qa.html",
                  body=body, main_class="wide", include_pagination=False)


def build_one_pager() -> str:
    """Apex one-pager — single sheet board strategic posture."""
    p = ROOT / "memo" / "one-pager.md"
    rendered = markdown.markdown(
        p.read_text(),
        extensions=["extra", "sane_lists", "tables", "md_in_html"],
        output_format="html5",
    )
    body = f"""
<div class="prose-article onepager-article">
{rendered}
</div>
"""
    return layout(title="One-pager", page_id="one-pager.html",
                  body=body, main_class="wide", include_pagination=False)


def build_financial_translation() -> str:
    """Financial translation — drug-by-drug CHF impact under scenarios."""
    p = ROOT / "memo" / "financial-translation.md"
    rendered = markdown.markdown(
        p.read_text(),
        extensions=["extra", "sane_lists", "tables", "toc", "md_in_html"],
        output_format="html5",
    )
    body = f"""
<div class="prose-article financial-translation-article">
{rendered}
</div>
"""
    return layout(title="Financial translation", page_id="financial-translation.html",
                  body=body, main_class="wide", include_pagination=False)


def build_bottom_line() -> str:
    """Bottom-line strategic synthesis — sharpened single-claim analysis."""
    p = ROOT / "memo" / "bottom-line.md"
    rendered = markdown.markdown(
        p.read_text(),
        extensions=["extra", "sane_lists", "tables", "toc", "md_in_html"],
        output_format="html5",
    )
    body = f"""
<div class="prose-article bottom-line-article">
{rendered}
</div>
"""
    return layout(title="Bottom line", page_id="bottom-line.html",
                  body=body, main_class="wide", include_pagination=False)


def build_black_swans() -> str:
    """Black-swan analysis — nine events with structured robust-position moves."""
    p = ROOT / "memo" / "black-swans.md"
    rendered = markdown.markdown(
        p.read_text(),
        extensions=["extra", "sane_lists", "tables", "toc", "md_in_html"],
        output_format="html5",
    )
    body = f"""
<div class="prose-article black-swans-article">
{rendered}
</div>
"""
    return layout(title="Black swans", page_id="black-swans.html",
                  body=body, main_class="wide", include_pagination=False)


def build_item_one() -> str:
    """Item 1 unpacked — precise actionable version of the firewall-annex recommendation."""
    p = ROOT / "memo" / "item-1-unpacked.md"
    rendered = render_md(p.read_text())
    body = f"""
<div class="callout warn">
  Item 1 of the board recommendation ("Endorse the firewall-annex approach...")
  is, as currently worded, too high-level to vote on. This page unpacks it into
  precise actionable content, names every load-bearing assumption explicitly,
  and provides a fallback plan if assumptions fail. The board should consider
  the refined version (Section 4) before voting.
</div>

<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="Item 1 unpacked", page_id="item-1.html",
                  body=body, main_class="prose")


def build_ai_implications() -> str:
    """AI implications — how AI reshapes every layer of the negotiation."""
    p = ROOT / "memo" / "ai-implications.md"
    rendered = render_md(p.read_text())
    body = f"""
<div class="callout">
  The supporting analysis on this site so far has treated AI as if it were not
  happening. This page corrects that. Eight layers of implication, three
  AI-specific strategic moves, and a meta-question about whether AI changes
  the negotiation's character. Five questions for the executive team at the end.
</div>

<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="AI implications", page_id="ai-implications.html",
                  body=body, main_class="prose")


def build_mfn_deals() -> str:
    """MFN signatories — at-a-glance table of all 17 voluntary agreements."""
    mfn_path = ROOT / "memo" / "mfn-deals-table.md"
    rendered = render_md(mfn_path.read_text())
    body = f"""
<div class="callout">
  All 17 voluntary MFN agreements signed with the Trump administration,
  sorted by date. For full filing-level detail (8-K accession numbers,
  risk-factor language, dated permalinks), see the
  <a href="disclosures.html">disclosures register</a>.
</div>

<div class="prose-article">
{rendered}
</div>
"""
    return layout(title="MFN deals", page_id="mfn-deals.html",
                  body=body, main_class="prose")


def build_model_data_json() -> str:
    """Build a JSON blob for embedding in simulation.html — mirrors the
    JS data structures the playground uses, but loaded from the source YAML."""
    data = load_data()

    actors = [{"id": a, "name": DISPLAY_NAMES.get(a, a)} for a in data.actors]

    issues = []
    for iid, issue in data.issues.items():
        # Pull a short description from the first sentence of issue.description
        short_desc = issue.description.split(".")[0] + "."
        issues.append({
            "id": iid,
            "name": issue.name,
            "units": issue.units,
            "lo": issue.lo,
            "hi": issue.hi,
            "dflt": issue.default,
            "desc": short_desc,
        })

    direction = {}
    for iid, issue in data.issues.items():
        direction[iid] = {a: issue.direction_for.get(a, 0) for a in data.actors}

    weights = {}
    batnas = {}
    red_lines = {}
    for actor in data.actors:
        w = {}
        b = {}
        rl = {}
        for iid in data.issues:
            pos = data.position(actor, iid)
            if pos is None:
                continue
            w[iid] = pos.weight
            b[iid] = pos.batna_value
            if pos.red_line_value is not None:
                rl[iid] = pos.red_line_value
        if w: weights[actor] = w
        if b: batnas[actor] = b
        if rl: red_lines[actor] = rl

    return json.dumps({
        "ACTORS": actors,
        "ISSUES": issues,
        "DIRECTION": direction,
        "WEIGHTS": weights,
        "BATNA": batnas,
        "RED_LINES": red_lines,
    }, indent=2)


def _shared_nav_html(active_page: str) -> str:
    """Sticky-header + menu overlay used inside simulation and playground
    pages (which have their own inline styles)."""
    desktop_parts = []
    overlay_parts = []
    for gname, group in NAV_GROUPS:
        overlay_parts.append(f'<div class="mobile-group-head">{gname}</div>')
        for href, label, primary in group:
            active = ' class="active"' if href == active_page else ""
            if primary:
                desktop_parts.append(f'<a href="{href}"{active}>{label}</a>')
            overlay_parts.append(f'<a href="{href}"{active}>{label}</a>')
    desktop_nav = '\n        '.join(desktop_parts)
    mobile_nav = '\n      '.join(overlay_parts)

    return (
        '<input type="checkbox" id="mobile-menu-toggle" class="mobile-toggle" aria-label="Toggle menu">\n'
        '<header class="site-header" style="position: static;">\n'
        '  <div class="inner">\n'
        '    <a href="index.html" class="brand">Roche negotiation</a>\n'
        f'    <nav class="desktop-nav" aria-label="Primary navigation">\n        {desktop_nav}\n    </nav>\n'
        '    <div class="nav-actions">\n'
        '      <button id="palette-trigger" class="palette-trigger" type="button" aria-label="Search the site">\n'
        '        <span class="label">Search</span><kbd>⌘K</kbd>\n'
        '      </button>\n'
        '      <label for="mobile-menu-toggle" class="menu-toggle" aria-label="Open menu" role="button" tabindex="0">\n'
        '        <span class="menu-toggle-label">Menu</span>\n'
        '        <span class="bars" aria-hidden="true"></span>\n'
        '      </label>\n'
        '    </div>\n'
        '  </div>\n'
        '</header>\n'
        '<nav class="mobile-nav" aria-label="Sections navigation">\n'
        f'      {mobile_nav}\n'
        '      <div class="meta-line">snapshot 19 May 2026</div>\n'
        '</nav>\n'
    )


def _mobile_nav_close_script() -> str:
    return (
        '<script>\n'
        'document.querySelectorAll(".mobile-nav a").forEach(a => {\n'
        '  a.addEventListener("click", () => {\n'
        '    const t = document.getElementById("mobile-menu-toggle");\n'
        '    if (t) t.checked = false;\n'
        '  });\n'
        '});\n'
        '</script>\n'
    )


def build_simulation() -> str:
    raw = SIMULATION_SRC.read_text()
    model_json = build_model_data_json()
    out = raw.replace("__MODEL_DATA_PLACEHOLDER__", model_json)
    nav_strip = _shared_nav_html("simulation.html")
    # Include shared style.css so the nav uses the editorial design tokens
    head_inject = (
        '<link rel="stylesheet" href="assets/style.css">\n'
        '<script src="assets/passcode.js"></script>\n'
    )
    out = out.replace('<link rel="stylesheet" href="assets/style.css">', '')
    out = out.replace("</head>", f"{head_inject}</head>")
    out = out.replace("<!-- BUILD-INJECTED HEADER -->", nav_strip)
    out = out.replace("</body>", _mobile_nav_close_script() + "</body>")
    return out


def build_playground() -> str:
    raw = PLAYGROUND_SRC.read_text()
    nav_strip = _shared_nav_html("playground.html")
    # Insert shared style.css + passcode BEFORE the inline <style> so playground
    # rules override shared on conflict.
    out = raw.replace(
        '<style>',
        '<link rel="stylesheet" href="assets/style.css">\n'
        '<script src="assets/passcode.js"></script>\n'
        '<style>',
        1,
    )
    out = out.replace("<body>", "<body>\n" + nav_strip, 1)
    out = out.replace("</body>", _mobile_nav_close_script() + "</body>")
    return out


def build_actors() -> str:
    data = load_data()
    snapshots = load_actor_snapshots()
    sidebar_parts = []
    content_parts = []
    for actor_id in data.actors:
        profile = DATA / "actors" / f"{actor_id}.md"
        if not profile.exists(): continue
        n = sum(1 for (a, _) in data.positions if a == actor_id)
        name = DISPLAY_NAMES.get(actor_id, actor_id)
        sidebar_parts.append(
            f'<a href="#{actor_id}" data-actor="{actor_id}">{name}<span class="count">{n}</span></a>'
        )
        rendered = render_md(profile.read_text())
        snap = actor_snapshot_block(snapshots.get(actor_id, {}))
        content_parts.append(f'<section id="{actor_id}" class="actor-profile">{snap}{rendered}</section>')

    actors_exec = exec_summary(
        "How to read this page",
        "12 actors, every position citation-backed",
        """
<p>Each actor profile opens with a <strong>5-line executive snapshot</strong>: one-liner, top priority, walks-if condition, leverage, and what Roche should do. Below the snapshot is the full sourced profile with positions, BATNAs, red lines, and citations.</p>
<p><strong>Read the snapshots first</strong> &mdash; they are board-ready summaries. Drill into the full profile only when a counterparty challenges a claim.</p>
""",
    )

    body = f"""
<h1>The 12 actors at the table</h1>
<p class="subtitle">Sourced profiles · every position citation-backed · snapshot 2026-05-19</p>

{actors_exec}

<div class="actor-layout">
  <nav class="actor-nav" aria-label="Actor selector">
    {chr(10).join(sidebar_parts)}
  </nav>
  <div class="actor-content">
    {(chr(10) + '<hr>' + chr(10)).join(content_parts)}
  </div>
</div>

<script>
(function() {{
  const links = document.querySelectorAll(".actor-nav a");
  function setActive() {{
    const hash = window.location.hash.replace("#", "") || links[0].dataset.actor;
    for (const l of links) l.classList.toggle("active", l.dataset.actor === hash);
  }}
  for (const l of links) l.addEventListener("click", () => setTimeout(setActive, 30));
  window.addEventListener("hashchange", setActive);
  setActive();
}})();
</script>
"""
    return layout(title="Actors", page_id="actors.html", body=body, main_class="wide")


def build_positions() -> str:
    data = load_data()

    # Build a compact matrix view + per-cell expanders
    # For board readability: show actor in rows, issue in columns, with weight value in cell
    header = '<tr><th class="sticky-col">Actor \\ Issue</th>'
    for iid in data.issues:
        header += f'<th title="{iid}" style="font-size:10px;writing-mode:vertical-rl;text-orientation:mixed;height:140px;vertical-align:bottom;padding-bottom:6px;">{data.issues[iid].name}</th>'
    header += "</tr>"

    rows = []
    for actor in data.actors:
        cells = [f'<td class="sticky-col"><strong>{DISPLAY_NAMES.get(actor, actor)}</strong></td>']
        for iid in data.issues:
            pos = data.position(actor, iid)
            if pos is None:
                cells.append('<td style="color:var(--muted);text-align:center;">·</td>')
            else:
                rl_marker = ""
                if pos.red_line_value is not None:
                    rl_marker = ' <span style="color:var(--negative);" title="has red line">●</span>'
                inferred_marker = ' <span style="color:var(--warning);" title="inferred (no direct public source)">i</span>' if pos.inferred else ""
                cells.append(
                    f'<td class="cell" title="{pos.position}" '
                    f'data-actor="{actor}" data-issue="{iid}">'
                    f'<span style="font-family:var(--mono);">w={pos.weight:.0f}</span>{rl_marker}{inferred_marker}'
                    f'</td>'
                )
        rows.append("<tr>" + "".join(cells) + "</tr>")

    pos_exec = exec_summary(
        "How to read this matrix",
        "12 × 13 grid · weights are board-relevant intensities",
        """
<ul>
<li><strong>Each cell</strong> shows that actor's weight (0&ndash;10) on that issue. Empty cells mean the actor has no meaningful stake.</li>
<li><strong>Red dot</strong> <span style="color:var(--negative);">●</span> marks a red line — the actor walks if breached.</li>
<li><strong>Yellow i</strong> <span style="color:var(--warning);">i</span> marks an inferred position (no direct public statement found).</li>
<li><strong>Click any cell</strong> for the full position text, BATNA, red-line value, and citation.</li>
<li><strong>Where to look first:</strong> Roche's row (top); the highest-weight column (10/10) per actor; clusters of red dots indicate brittle issues.</li>
</ul>
""",
    )

    body = f"""
<h1>Positions matrix</h1>
<p class="subtitle">12 actors × 13 issues = {len(data.actors) * len(data.issues)} possible cells · {len(data.positions)} populated · click any cell to expand</p>

{pos_exec}

<div class="callout">
  Each cell shows the actor's <strong>weight</strong> (0–10 importance) for that issue.
  A red dot <span style="color:var(--negative);">●</span> indicates a red line exists on that issue.
  A yellow <span style="color:var(--warning);">i</span> indicates the position is inferred without a direct public statement.
  Click a cell to see the position text, BATNA, red-line value, and citation.
</div>

<div style="overflow-x:auto;border:1px solid var(--border);border-radius:8px;margin-top:18px;">
<table id="positions-matrix" style="margin:0;border-collapse:collapse;width:auto;min-width:100%;">
  <thead>{header}</thead>
  <tbody>
    {chr(10).join(rows)}
  </tbody>
</table>
</div>

<div id="position-detail" style="display:none;background:var(--surface);border:1px solid var(--accent);border-radius:var(--radius-lg);padding:22px 26px;margin-top:18px;position:sticky;bottom:14px;box-shadow:0 8px 24px rgba(30,58,95,0.08);">
  <button id="close-detail" style="float:right;background:transparent;border:none;color:var(--muted);font-size:20px;cursor:pointer;line-height:1;padding:4px 8px;">×</button>
  <div id="detail-actor" style="font-size:10.5px;color:var(--accent);text-transform:uppercase;letter-spacing:0.12em;font-family:var(--font-mono);font-weight:600;"></div>
  <div id="detail-issue" style="font-size:20px;font-weight:500;margin-top:6px;color:var(--ink);font-family:var(--font-serif);letter-spacing:-0.013em;"></div>
  <div id="detail-position" style="margin-top:14px;font-style:italic;color:var(--ink-2);font-family:var(--font-serif);font-size:15px;line-height:1.55;"></div>
  <div id="detail-numbers" style="margin-top:16px;display:flex;gap:24px;flex-wrap:wrap;font-family:var(--font-mono);font-size:13px;color:var(--ink);"></div>
  <div id="detail-citation" style="margin-top:14px;font-size:11.5px;color:var(--muted);font-family:var(--font-mono);"></div>
</div>

<style>
  #positions-matrix {{
    font-family: var(--font-sans);
    font-feature-settings: "tnum";
  }}
  #positions-matrix .sticky-col {{
    position: sticky; left: 0; background: var(--canvas); z-index: 1;
    min-width: 180px;
    text-align: left;
    color: var(--ink);
    font-weight: 500;
  }}
  #positions-matrix th {{
    background: var(--canvas);
    font-weight: 500;
    color: var(--muted);
    font-size: 11px;
    border-bottom: 1px solid var(--hairline-strong);
  }}
  #positions-matrix td, #positions-matrix th {{
    border: 1px solid var(--hairline);
    padding: 7px 10px;
    text-align: center;
    font-size: 12.5px;
  }}
  #positions-matrix td.cell {{
    cursor: pointer;
    transition: background 120ms ease;
  }}
  #positions-matrix td.cell:hover {{ background: var(--accent-soft); }}
  #positions-matrix tr:hover td.sticky-col {{ background: var(--surface-2); }}
  @media (max-width: 800px) {{
    #positions-matrix .sticky-col {{ min-width: 130px; font-size: 11px; }}
    #positions-matrix td, #positions-matrix th {{ padding: 5px 7px; font-size: 11px; }}
  }}
</style>

<script>
const positions = {json.dumps({
    f"{a}|{i}": {
        "weight": pos.weight,
        "batna_value": pos.batna_value,
        "red_line_value": pos.red_line_value,
        "position": pos.position,
        "citation": pos.citation,
        "inferred": pos.inferred,
    }
    for (a, i), pos in data.positions.items()
})};
const displayNames = {json.dumps(DISPLAY_NAMES)};
const issueNames = {json.dumps({iid: data.issues[iid].name for iid in data.issues})};
const issueUnits = {json.dumps({iid: data.issues[iid].units for iid in data.issues})};

document.querySelectorAll("#positions-matrix td.cell").forEach(c => {{
  c.addEventListener("click", () => {{
    const k = c.dataset.actor + "|" + c.dataset.issue;
    const p = positions[k];
    if (!p) return;
    document.getElementById("detail-actor").textContent = displayNames[c.dataset.actor] || c.dataset.actor;
    document.getElementById("detail-issue").textContent = issueNames[c.dataset.issue] || c.dataset.issue;
    document.getElementById("detail-position").textContent = "\\"" + p.position + "\\"";
    const units = issueUnits[c.dataset.issue] || "";
    const num = document.getElementById("detail-numbers");
    while (num.firstChild) num.removeChild(num.firstChild);
    function chip(label, value) {{
      const span = document.createElement("span");
      const lab = document.createElement("span");
      lab.style.color = "var(--muted)";
      lab.textContent = label + ": ";
      span.appendChild(lab);
      span.appendChild(document.createTextNode(value));
      return span;
    }}
    num.appendChild(chip("Weight", p.weight + "/10"));
    num.appendChild(chip("BATNA", p.batna_value + " " + units));
    if (p.red_line_value !== null) num.appendChild(chip("Red line", p.red_line_value + " " + units));
    if (p.inferred) num.appendChild(chip("Source", "inferred"));
    document.getElementById("detail-citation").textContent = "Citation: " + p.citation;
    document.getElementById("position-detail").style.display = "block";
  }});
}});
document.getElementById("close-detail").addEventListener("click", () => {{
  document.getElementById("position-detail").style.display = "none";
}});
</script>
"""
    return layout(title="Positions", page_id="positions.html", body=body, main_class="wide")


def build_prompts() -> str:
    """Show novelty domains + any pre-generated collision prompts."""
    domains_path = ROOT / "novelty" / "domains.yaml"
    import yaml
    domains_raw = yaml.safe_load(domains_path.read_text())

    domain_cards = []
    for d in domains_raw["domains"]:
        principles_html = "".join(f"<li>{p}</li>" for p in d["principles"])
        sources_html = "".join(f'<li><a href="{s}" target="_blank">{s}</a></li>' for s in d.get("sources", []))
        domain_cards.append(f"""
<details class="domain-card" style="background:var(--surface);border:1px solid var(--hairline);border-radius:var(--radius-lg);padding:16px 22px;margin-bottom:10px;transition:border-color 180ms ease;">
  <summary style="cursor:pointer;font-family:var(--font-sans);font-size:15.5px;font-weight:600;color:var(--ink);letter-spacing:-0.011em;">
    {d['name']}
    <span style="color:var(--muted);font-weight:400;font-size:11.5px;font-family:var(--font-mono);margin-left:8px;letter-spacing:0.01em;">{d['id']}</span>
  </summary>
  <p style="font-family:var(--font-serif);font-style:italic;color:var(--ink-2);font-size:15px;line-height:1.55;margin-top:12px;">{d['one_liner'].strip()}</p>
  <h4 style="margin-top:18px;">Operational principles</h4>
  <ul>{principles_html}</ul>
  <h4 style="margin-top:18px;">Why it matches</h4>
  <p style="font-family:var(--font-serif);font-size:15px;color:var(--ink-2);line-height:1.55;">{d['why_relevant'].strip()}</p>
  <h4 style="margin-top:18px;">Sources</h4>
  <ul class="sources-list">{sources_html}</ul>
</details>
""")

    # List any pre-generated prompt batches
    ideas_dir = ROOT / "novelty" / "ideas"
    batches = []
    if ideas_dir.exists():
        for batch_dir in sorted(ideas_dir.iterdir()):
            if not batch_dir.is_dir(): continue
            for prompt_file in sorted(batch_dir.glob("prompts-*.md")):
                rel = prompt_file.relative_to(ROOT)
                size = prompt_file.stat().st_size
                batches.append(f"<li><code>{rel}</code> — {size:,} bytes</li>")

    batches_html = "".join(batches) if batches else "<li><em>(no prompt batches generated yet — run <code>python -m novelty.collide --scenario status_quo</code>)</em></li>"

    prompts_exec = exec_summary(
        "When to use this",
        "Use the novelty engine when standard moves have run out",
        """
<p>The standard pharma-pricing playbook is well-trodden. Every actor's negotiators have read the same slide decks. When the model says <strong>"Pareto improvements exist but standard moves are exhausted,"</strong> the novelty engine is the tool: it collides the negotiation with structurally distant problem-solving repertoires (reinsurance, climate finance, antitrust consent decrees, sovereign-debt restructuring, hostage negotiation, ...) to surface moves no one at the table has proposed yet.</p>
<p><strong>Top three for the current scenario:</strong></p>
<ul>
<li><strong>Reinsurance pooling</strong> — caps MFN tail risk via confidential quota-share with the US government. Aligns government incentive with Roche's market success.</li>
<li><strong>Sovereign-debt CAC clauses</strong> — bind all 17 MFN signatories to comparable treatment, removing the holdout incentive that currently makes Roche's deal feel like a sweetheart carve-out.</li>
<li><strong>Climate loss-and-damage fund</strong> — decouples US capex acceleration from Basel cantonal-tax-base damage. Removes the Swiss-internal blocker.</li>
</ul>
""",
    )

    body = f"""
<h1>Novelty engine — domain collision prompts</h1>
<p class="subtitle">15 distant analogue domains · open-collider-style structural collision · pre-curated for Roche pricing context</p>

{prompts_exec}

<div class="callout">
  The novelty engine generates Claude prompts that <strong>collide</strong> the
  current scenario with each of these domains — surfacing negotiation moves
  that don't exist in any actor's standard playbook. Run
  <code>python -m novelty.collide --scenario &lt;name&gt;</code> from the repo
  root to write a fresh batch of prompts; the output is a Markdown file
  that you paste into a Claude session.
</div>

<h2>Pre-generated prompt batches</h2>
<ul>{batches_html}</ul>

<h2>The 15 domains</h2>
<p>Click any domain to expand its principles and Pharma-pricing relevance:</p>

{chr(10).join(domain_cards)}
"""
    return layout(title="Prompts", page_id="prompts.html", body=body, main_class="prose")


def build_transcripts() -> str:
    """List all simulation transcripts available."""
    transcripts_dir = ROOT / "agents" / "transcripts"
    rows = []
    if transcripts_dir.exists():
        for md in sorted(transcripts_dir.glob("*.md"), reverse=True):
            rel = md.relative_to(ROOT)
            size = md.stat().st_size
            stamp_match = re.search(r"(\d{8}-\d{6})", md.name)
            stamp = stamp_match.group(1) if stamp_match else ""
            parts = md.stem.split("-")
            scenario = parts[0] if len(parts) > 0 else "?"
            protocol = parts[1] if len(parts) > 1 else "?"
            mode = parts[2] if len(parts) > 2 else "?"
            rows.append(
                f'<tr><td>{stamp}</td><td><code>{scenario}</code></td>'
                f'<td><code>{protocol}</code></td><td><code>{mode}</code></td>'
                f'<td class="num">{size:,}</td>'
                f'<td><code>{rel}</code></td></tr>'
            )

    table_body = "\n".join(rows) if rows else (
        "<tr><td colspan=\"6\" style=\"color:var(--muted);text-align:center;padding:32px;\">"
        "No transcripts yet. Run <code>python -m agents.runner --scenario status_quo "
        "--protocol trilateral_us_ch_roche</code> from the repo root.</td></tr>"
    )

    tr_exec = exec_summary(
        "Two kinds of simulation",
        "Voiced vs. structural — pick by purpose",
        """
<ul>
<li><strong>Voiced simulation</strong> (<a href="simulation.html">live simulation</a> page) &mdash; the hand-curated 18-event trilateral negotiation. Use this for the board: each statement is written to match a sourced position; the deal vector animates in real time. This is the <em>presentation</em> artifact.</li>
<li><strong>Structural simulations</strong> (this page) &mdash; mechanical multi-agent runs over the payoff model. Heuristic mode is deterministic and useful for stress-tests. <code>--live</code> mode uses Claude as each actor (non-deterministic; treat as exploratory).</li>
</ul>
<p>When a counterparty challenges the recommendation, run a structural simulation under the new scenario (e.g., <code>mfn_hardline</code>, <code>basel_relocation_stress</code>, <code>full_multilateral</code>) and compare the transcript to predicted equilibria.</p>
""",
    )

    body = f"""
<h1>Simulation transcripts</h1>
<p class="subtitle">Multi-agent negotiation runs · heuristic or live (Claude API) modes · JSON + Markdown</p>

{tr_exec}

<div class="callout">
  These are <strong>structural</strong> simulation runs from <code>agents/runner.py</code> &mdash;
  the heuristic mode applies a deterministic step-toward-preferred-direction
  per actor, useful for sanity-checking the model. For the <strong>voiced</strong>
  trilateral simulation (with full actor statements), see the <a href="simulation.html">live simulation</a> page.
</div>

<table>
  <tr><th>Timestamp</th><th>Scenario</th><th>Protocol</th><th>Mode</th><th class="num">Bytes</th><th>File</th></tr>
  {table_body}
</table>

<h2>How to generate more</h2>

<pre><code># Heuristic (no API key needed)
python -m agents.runner --scenario status_quo --protocol trilateral_us_ch_roche
python -m agents.runner --scenario basel_relocation_stress --protocol swiss_internal
python -m agents.runner --scenario mfn_hardline --protocol full_multilateral

# Live mode (requires ANTHROPIC_API_KEY env var; one Claude session per actor)
pip install -e '.[agents]'
export ANTHROPIC_API_KEY=...
python -m agents.runner --mode live --protocol trilateral_us_ch_roche</code></pre>

<p>Available scenarios: <code>status_quo</code>, <code>mfn_hardline</code>, <code>swiss_carveout</code>, <code>ira_escalation</code>, <code>basel_relocation_stress</code>, <code>trade_war_collapse</code>.</p>
<p>Available protocols: <code>bilateral_us_roche</code>, <code>trilateral_us_ch_roche</code>, <code>swiss_internal</code>, <code>full_multilateral</code>, <code>coalition_formation</code>.</p>
"""
    return layout(title="Transcripts", page_id="transcripts.html", body=body, main_class="wide")


def build_method() -> str:
    model_readme = (ROOT / "model" / "README.md").read_text()
    rendered = render_md(model_readme)
    method_exec = exec_summary(
        "Method in 30 seconds",
        "Transparent linear payoffs, multi-concept equilibrium",
        """
<ul>
<li><strong>Each actor has interests (with weights) on each issue.</strong> Payoff is a linear sum of weighted normalised issue values. Red-line violations apply a hard sub-BATNA penalty.</li>
<li><strong>Four equilibrium concepts</strong> are solved per scenario: Nash bargaining (efficient compromise weighted by leverage), Kalai&ndash;Smorodinsky (proportional fairness), Shapley (marginal contribution), core check (coalition stability).</li>
<li><strong>The calibration test</strong> is that the actual May 2026 status quo is feasible under the model. If the model said Roche should have walked from a deal it already signed, it would be unusable. Test passes.</li>
<li><strong>What the model cannot see:</strong> confidential PBM rebates, EU Managed Entry Agreements, NDA-protected positions. It works with public information only.</li>
</ul>
""",
    )

    body = f"""
<h1>Methodology</h1>
<p class="subtitle">How the model works · why it is calibrated · what it cannot see</p>

{method_exec}

<div class="callout green">
  <strong>Calibration claim, verifiable:</strong> Run <code>python -m pytest model/tests/</code> in the repository.
  The test <code>test_status_quo_feasible</code> confirms the actual May 2026 signed state
  (Dec-2025 Genentech MFN + Nov-2025 Swiss framework + Jan-2026 IRA Round 3 + Apr-2026 Section 232)
  is feasible under the model.
</div>

{rendered}

<h2>Limits</h2>

<ul>
  <li>Linear payoffs with hard red-line kinks. The model does not capture nonlinear bargaining dynamics (e.g., increasing returns to coalition size, or face-saving thresholds with mass-discontinuities).</li>
  <li>Each actor's weights and red lines are sourced from public statements where possible and marked <code>inferred: true</code> otherwise. See the <a href="positions.html">positions matrix</a>.</li>
  <li>Confidential net prices (PBM rebates, EU Managed Entry Agreements) are not visible to the model. The international-reference-pricing-protection issue is a coarse proxy for what is in reality a contract-by-contract dance.</li>
  <li>The model treats actors as unitary at the level of disaggregation specified (12 actors). Deeper disaggregation (e.g., separating US Executive into White House / HHS / CMS / USTR) is a planned extension.</li>
  <li>The <a href="simulation.html">live simulation</a> page plays back a hand-curated 18-event trilateral negotiation transcript with statements written to match each actor's documented positions. The agent <code>--live</code> mode (in the repository) uses Claude as each actor and is non-deterministic; treat it as exploratory, not predictive.</li>
</ul>

<h2>Re-running the model</h2>

<pre><code>python -m pytest model/tests/              # verify calibration
python -m model status_quo --concept all   # equilibrium predictions
python -m agents.runner --scenario status_quo --protocol full_multilateral
python -m novelty.collide --scenario status_quo --domains reinsurance-pooling
python -m memo.generator --scenario status_quo --equilibrium nash
python tools/build_site.py                  # rebuild this site</code></pre>
"""
    return layout(title="Method", page_id="method.html", body=body, main_class="prose")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "assets").mkdir(exist_ok=True)

    # Copy simulation data files
    docs_sim = DOCS / "simulations"
    docs_sim.mkdir(exist_ok=True)
    for src in SIMULATIONS_DIR.glob("*.json"):
        shutil.copy(src, docs_sim / src.name)
        print(f"  copied  docs/simulations/{src.name}")

    pages = {
        "one-pager.html": build_one_pager(),
        "briefing.html": build_briefing(),
        "bottom-line.html": build_bottom_line(),
        "black-swans.html": build_black_swans(),
        "financial-translation.html": build_financial_translation(),
        "decision-quality.html": build_decision_quality(),
        "peer-comparison.html": build_peer_comparison(),
        "board-qa.html": build_board_qa(),
        "index.html": build_index(),
        "recommendation.html": build_recommendation(),
        "recommendation-detail.html": build_recommendation_detail(),
        "adversarial.html": build_adversarial(),
        "cross-domain.html": build_cross_domain(),
        "cross-domain-depth.html": build_cross_domain_depth(),
        "ai-implications.html": build_ai_implications(),
        "item-1.html": build_item_one(),
        "dynamics.html": build_dynamics(),
        "disclosures.html": build_disclosures(),
        "mfn-deals.html": build_mfn_deals(),
        "global-pricing.html": build_global_pricing(),
        "simulation.html": build_simulation(),
        "playground.html": build_playground(),
        "actors.html": build_actors(),
        "positions.html": build_positions(),
        "prompts.html": build_prompts(),
        "transcripts.html": build_transcripts(),
        "glossary.html": build_glossary(),
        "method.html": build_method(),
    }
    for filename, content in pages.items():
        (DOCS / filename).write_text(content)
        print(f"  wrote   docs/{filename}  ({len(content):,} bytes)")

    (DOCS / "404.html").write_text(layout(
        title="Not found",
        page_id="",
        body='<h1>Page not found</h1><p><a href="index.html">Back to the overview</a>.</p>',
        main_class="prose",
    ))
    print(f"  wrote   docs/404.html")

    (DOCS / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    print(f"  wrote   docs/robots.txt")

    # Build search index for Cmd+K palette by scanning rendered HTML
    search_index = []
    for filename, content in pages.items():
        title_m = re.search(r'<title>([^<]+)</title>', content)
        title = title_m.group(1) if title_m else filename
        # Trim "— Roche..." suffix from titles
        title = re.sub(r'\s*[—-]\s*Roche.*$', '', title)
        sections = []
        for level, attrs, label in re.findall(
            r'<h([2-3])([^>]*)>([^<]+(?:<[^>]+>[^<]*)*?)</h\1>', content):
            id_m = re.search(r'\sid="([^"]+)"', attrs)
            if not id_m:
                continue
            clean_label = re.sub(r'<[^>]+>', '', label).strip()
            if not clean_label:
                continue
            sections.append({
                "id": id_m.group(1),
                "label": clean_label,
                "level": int(level),
            })
        search_index.append({
            "page": filename,
            "title": title,
            "sections": sections,
        })
    (DOCS / "search-index.json").write_text(json.dumps(search_index, indent=0))
    print(f"  wrote   docs/search-index.json ({len(search_index)} pages, "
          f"{sum(len(p['sections']) for p in search_index)} sections)")

    print(f"\nBuilt {len(pages) + 2} pages under {DOCS}")
    print(f"Local preview: cd {DOCS} && python -m http.server 8000")
    return 0


if __name__ == "__main__":
    sys.exit(main())
