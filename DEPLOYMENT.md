# Deployment guide

This site is designed to be presented to a small group (e.g., a board) via
GitHub Pages with passcode-gated access. Below are three deployment paths
ordered from **least to most secure**. Pick the one that matches who must
not see the analysis.

---

## Strategic question first

The site contains structured analysis of Roche's negotiating position. Once
hosted on the public web, it is in principle readable by counterparties
(US administration, USTR, CMS, Novartis, EU Commission, biosimilar
manufacturers, payer advocacy, journalists). Even with a passcode, anyone
who obtains the passcode can read everything.

**Before deploying, decide:**
1. **Who should the board show this to internally?** Is the recommendation
   ready to be shared with people outside the simulation team?
2. **What's the worst case if the URL leaks?** The analysis cites public
   sources only, but synthesizes them into Roche-favoring recommendations.
   A counterparty reading this learns what Roche's analyst thinks Roche's
   weakest issue is (Section 232 sunset), highest-value lever
   (intl-ref-pricing firewall), and acceptable concessions.
3. **Is GitHub Pages even the right host?** See Path C below for stronger
   alternatives.

If you proceed: at minimum, **change the passcode** (`python tools/set_passcode.py`)
and **never push the new passcode hash to a public repo**.

---

## Path A — GitHub Pages, public repo, passcode-gated (fast, weak security)

**Threat model defended against:** search-engine indexing, casual visitors
who stumble on the URL.

**Not defended against:** anyone with the URL who reads the JS source can
extract the SHA-256 hash and brute-force a weak passcode offline.

Steps:

```bash
# 1. Set a strong passcode (15+ chars, mixed types)
cd /Users/jonashertner/roche-game-theory
python tools/set_passcode.py

# 2. Build (must rerun after passcode change)
python tools/build_site.py

# 3. Test locally
cd docs && python -m http.server 8000
# open http://localhost:8000

# 4. Initialise repo
cd /Users/jonashertner/roche-game-theory
git init
git checkout -b main
git add .
git commit -m "Initial commit"

# 5. Push to GitHub
gh repo create roche-game-theory --public --source=. --remote=origin
git push -u origin main

# 6. Enable GitHub Pages
#   GitHub UI: Settings → Pages → Source: "GitHub Actions"
#   Or via CLI:
gh api -X POST /repos/<user>/roche-game-theory/pages \
  -f source.branch=main -f source.path=/docs
```

The workflow at `.github/workflows/pages.yml` runs on every push to `main`:
it runs the model tests (calibration gate), regenerates the latest memo,
regenerates a sample collision-prompt batch, builds the static site, and
deploys to Pages.

**URL pattern:** `https://<user>.github.io/roche-game-theory/`

The site will prompt for the passcode on first visit; localStorage remembers it.

---

## Path B — GitHub Pages, private repo (better)

GitHub Pages on a **private repo** requires GitHub Pro, Team, or Enterprise.
With this, only authenticated GitHub users you've added as collaborators
can view the site even with the URL.

Steps (same as Path A but private):

```bash
gh repo create roche-game-theory --private --source=. --remote=origin
git push -u origin main
# Enable Pages in repo Settings; add board members as collaborators.
```

The passcode gate still adds defense-in-depth. Combined with GitHub auth,
this is reasonable for board-internal sharing.

**Limit:** every viewer needs a GitHub account added to the repo. For board
members who aren't GitHub users, Path C is better.

---

## Path C — Cloudflare Pages + Cloudflare Access (strongest)

For genuine access control with email-based authentication:

1. Create a private GitHub repo (or stay on local).
2. Connect to **Cloudflare Pages** (free tier).
3. Set the build command to `python tools/build_site.py` with output dir `docs`.
4. Enable **Cloudflare Access** on the Pages site with a policy that requires:
   - Specific email addresses (board members), or
   - A specific email domain (`@roche.com`), or
   - A one-time-PIN sent to allowlisted emails (no account needed).
5. Cloudflare Access logs every viewer.

Cloudflare Pages also supports per-deployment passwords and CAPTCHAs.

For a board presentation, Cloudflare Access with one-time-PIN is ideal:
each board member gets an email with a magic link; no GitHub account needed;
access can be revoked instantly.

This is what I would actually recommend for board-restricted material.

---

## Path D — Local-only (no deployment at all)

Sometimes the right answer is just to present from a laptop:

```bash
cd /Users/jonashertner/roche-game-theory/docs
python -m http.server 8000
# Open http://localhost:8000 on the presenter's laptop, screen-share via Zoom/Teams.
```

Zero exposure. Use this if there's any chance the board hasn't approved
external hosting yet.

---

## Updating the passcode

```bash
python tools/set_passcode.py            # interactive prompt
python tools/set_passcode.py "MyN3wP@$$word!"   # CLI
python tools/build_site.py              # rebuild after change
git commit -am "Update passcode hash"
git push   # only if you're already deployed; otherwise just rebuild
```

Board members will be prompted for the passcode again on next visit (the
localStorage value won't match the new hash).

## Updating the analysis

When the underlying data changes:

```bash
# Edit data/actors/*.md or data/positions.yaml
python -m pytest model/tests/   # confirm calibration still holds
python -m memo.generator --scenario status_quo --equilibrium nash
python tools/build_site.py
git add data/ docs/ memo/drafts/
git commit -m "Update May refresh"
git push   # auto-deploys via Actions
```

## Removing the deployment

```bash
# Disable Pages: Settings → Pages → set Source to "None"
# Or delete the repo entirely:
gh repo delete <user>/roche-game-theory --confirm
```

The site goes dark within ~1 minute. Note: archive.org may have already
crawled it if it was public for any time. **This is the main reason to
prefer Path B or C from the start.**
