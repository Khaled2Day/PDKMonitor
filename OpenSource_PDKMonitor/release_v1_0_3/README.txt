CORNERSTONE PDK Monitor v1.0.3
===============================
Single-file browser dashboard for silicon photonics PDK management.
Designed by Emre Kaplan · pdk.cornerstone.soton.ac.uk
Licence: TAPR Open Hardware Licence v1.0

CONTENTS
--------
  cornerstone-pdk-monitor-v1.0.3.html   — Main dashboard (open in any modern browser)
  dashboard.json                        — Default pre-populated PDK dataset (full state)
  USER_MANUAL.md / .docx / .pdf         — Full user manual (rewritten for v1.0.3)
  CHANGELOG.md                          — Release notes
  CORNERSTONE_PDK_Monitor_Introduction.pptx — Slide deck
  README.txt                            — This file

HOW TO USE
----------
1. Open cornerstone-pdk-monitor-v1.0.3.html in Chrome, Firefox, or Safari.
2. No server or installation required — works fully offline.
3. On first launch: accept the licence terms.
4. The dashboard loads pre-populated with the full CORNERSTONE BB set.
5. Import dashboard.json via the Import button to reset to defaults.
6. See USER_MANUAL.pdf (or .md) for the full guide.

ABOUT v1.0.3
------------
v1.0.3 is the "open collaboration" release. The headline change is that
contributors WITHOUT direct push access to your upstream PDKmonitor repo
can now do the entire fork → commit → PR → review flow inside the
dashboard, with no manual github.com steps.

CONTRIBUTOR WORKFLOW (no PR-from-fork on github.com required)
- Sign in with a GitHub PAT (no dashboard password needed)
  → dashboard auto-promotes to user-admin, identity = your GitHub login,
    your fork(s) of every Distribution source are auto-added as enabled
    rows targeting users/<login>/dashboard.json
- ⚡ Direct commit → preflight detects no push → offers 🔱 Fork & publish
- 🔱 Fork & publish → API forks the repo, commits to the fork
- 🚀 Open PR to upstream → rich modal (title / body / reviewers / labels /
    draft) → POST /pulls files the PR
- If the API call fails (e.g. fine-grained PAT can't open PRs on the
  upstream), one-click 📤 Open PR creation page on github.com fallback
  takes you straight to the pre-filled PR-compose page

MAINTAINER WORKFLOW (review PRs without leaving the dashboard)
- Distribution → 4. GitHub collaborators (live) → 👥 Show collaborators
- Three sections render: collaborators (with PR counts + remove button),
  open PRs (with author, fork source, draft flag, Review link, Merge…
  button), and ➕ Invite collaborator (admin-only, full-width input)

OTHER MAJOR IMPROVEMENTS
- 🔱 Discover forks — walks GitHub's forks for every enabled upstream
  source and lets you tick which forks to add as Distribution sources.
- Plot windows stay open until you close them; new plots ask whether to
  use a new window or merge into an existing one; 📈 Plot raw can
  overlay datasets from any BB across any tab.
- Subfolders inside test / S-matrix folders (unlimited depth). Subfolder
  × delete now actually works (walks the tree).
- 📝 Edit folder keywords — tune which folder names map to which BB
  section per team convention.
- Two-step token diagnostic: 🔍 Test token + sources verifies the PAT
  AND reports per-source read / push / admin permissions, with SSO
  Configure-SSO links surfaced from the response header.
- Tab strip stays a fixed-height single row even with many tabs.
- ↺ Reset admin password to factory default link in the sign-in modal —
  recovers from "I changed it and forgot it" lockouts.
- Relaxed publish cooldown: flat 30 s between submits, 20 / rolling
  1 hour quota per identity (replaces the progressive backoff).

INHERITED FROM v1.0.2 / v1.0.1
- Layout / Docs tab split on every BB card.
- 📁 Platform-level Design manuals chip on every group head.
- Multi-source platform import + name-match BB routing.
- Pin coverage on Files / Folders / BBs / Scripts / Fab / EDA.
- Dedupe-by-filename on every upload / fetch path.
- Sign-in: 5 attempts per identity per 1 hour, 30-second Undo on every
  destructive action, schema-validated imports, login trust token,
  cross-tab search, keyboard shortcuts, activity log, mobile-responsive.

OPERATIONAL (lives in repo, outside this zip)
- release.sh — version-bump + build automation.
- tests/smoke.spec.ts — Playwright smoke tests.
- .github/workflows/smoke.yml — runs on every PR.

(See CHANGELOG.md for the full per-version history.)

AI AGENT QUICK START
--------------------
1. Click 🧠 Insight in the header.
2. Choose ⚙ Configure — enter your Anthropic/OpenAI API key.
3. Click 💬 Chat with the agent to start.
4. In the chat, click ▶ Data files in context to load CSV/JSON files
   from GitHub for analysis (🔬 Analyse files with AI).
5. Click ⧉ Detach to pop the chat into a floating window.

LINKS
-----
Open Platform GitHub : https://github.com/cornerstone-uos/cornerstone-community
Main PDK GitHub      : https://github.com/cornerstone-uos/cornerstone-pdk
Website              : https://cornerstone.sotonfab.co.uk
