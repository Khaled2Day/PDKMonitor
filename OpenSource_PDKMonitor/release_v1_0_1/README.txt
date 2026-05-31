CORNERSTONE PDK Monitor v1.0.1
===============================
Single-file browser dashboard for silicon photonics PDK management.
Designed by Emre Kaplan · pdk.cornerstone.soton.ac.uk
Licence: TAPR Open Hardware Licence v1.0

CONTENTS
--------
  cornerstone-pdk-monitor-v1.0.1.html   — Main dashboard (open in any modern browser)
  dashboard.json                        — Default pre-populated PDK dataset (full state)
  USER_MANUAL.md / .docx / .pdf         — Full user manual
  CHANGELOG.md                          — Release notes (full v1.1.x history included)
  CORNERSTONE_PDK_Monitor_Introduction.pptx — Slide deck
  README.txt                            — This file

HOW TO USE
----------
1. Open cornerstone-pdk-monitor-v1.0.1.html in Chrome, Firefox, or Safari.
2. No server or installation required — works fully offline.
3. On first launch: accept the licence terms.
4. The dashboard loads pre-populated with the full CORNERSTONE BB set.
5. Import dashboard.json via the Import button to reset to defaults.
6. See USER_MANUAL for the full guide.

ABOUT v1.0.1
------------
This is a consolidated stable release containing every improvement from the
v1.1.x development iterations, plus a final polish pass. Highlights:

ACCESS & SAFETY
- Sign-in: 5 attempts per identity per 1 hour (relaxed from 3 per 24 h).
- Read-only sessions can browse Manage Lists and manage their own local tabs.
- 30-second Undo on EVERY destructive action (tab, block, document, every
  Manage Lists item) — misclicks cost nothing.
- Auto-backup before "Replace whole dashboard". Schema validation rejects
  malformed imports cleanly.

SECURITY
- Login modal shows a session-keyed trust token (8-char hex) so users can
  recognize the real dialog vs a phishing fake.
- GitHub PAT field recommends fine-grained tokens with Contents: Read+Write
  on specific repos, with warning against classic broad-`repo` tokens.
- All user-controlled strings (owner names, BB labels, fetched payload
  fields) go through escapeHtml before reaching innerHTML.

UX
- 🕓 Activity log button in the header lists the last 100 mutations
  with timestamps, actor, action, and label. Lives in dashboard.json
  so the team can see who did what.
- Cross-tab search dropdown: type ≥ 2 chars in the search box and
  matches from every other tab appear below, click to jump.
- Keyboard shortcuts: "/" or Cmd/Ctrl+K to focus search, "t" to switch
  tabs, "n" to add a new block, "?" for the help overlay, Esc to close.
- Mobile responsive: works on iPad (tablet portrait) and phone.

ADMIN
- Tab merge tool: full Admin can merge one tab into another. Sub-entities
  with matching names are combined; BBs deduped by id; merged structure
  saves to dashboard.json so every fetcher inherits the result.
- Manage Lists × buttons line up in clean vertical columns regardless of
  owner attribution. Owner labels appear inline with the name as faded
  (parenthesized) text — uniform grid across rows.

OPERATIONAL (lives in repo, outside this zip)
- release.sh — version-bump + build automation. Usage: ./release.sh v1.0.2
- tests/smoke.spec.ts — 6 Playwright tests covering critical flows.
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
