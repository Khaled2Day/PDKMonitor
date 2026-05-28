# CORNERSTONE PDK Monitor — Changelog

All notable changes are documented here.

---

## v1.0.0 — Official Public Release (28 May 2026)

### Core dashboard
- Multi-platform tabs: SOI 220 nm, SOI 340 nm, SOI 500 nm, TFLN 300 nm, SiN 300 nm, SiN 200 nm
- Role-based access: Admin · User-admin (`users/<id>/`) · Read-only
- Real-files architecture — every uploaded binary lives as a separate file in the GitHub repo; `dashboard.json` stays lean
- Multi-user pool: Fetch all sources · Fetch user repos · Discover slices · Fetch my slice
- Duplicate resolver for cross-platform BB names
- GDS viewer with layer colours and hover descriptions
- BB procedural sketches with material gradients (Si / SiN / LN)
- Inline Python script runner (Pyodide sandbox)
- Local JSON backups on every replace
- CDI maturity axes (Chip / Wafer / Assembly, 1–4)
- EDA tool tagging per BB (gdsfactory, IPKISS, KLayout, Synopsys, …)
- Editable lists: statuses, categories, BB types, EDA tools, CDI axes, GDS layers, platforms

### AI Insight agent (new in this release)
- Multi-turn chat agent (Claude / OpenAI / Ollama / any OpenAI-compatible endpoint)
- Full PDK tool-use: list_platforms, list_bbs, get_bb, list_contributors, get_bb_metrics, search_bbs, summarise_bb
- BB summariser with citation-checked metrics — executive + deep-dive, cached per BB
- Executive summary for whole platform or entire dashboard (exports to .md)
- Monthly token cap + usage meter

### AI Data Agent (new in this release)
- **📁 GitHub file fetcher** — single file, entire folder, or multi-URL batch (one per line / comma-separated)
  - Folder URLs (`github.com/org/repo/tree/branch/path`) resolved via GitHub Contents API
  - Recursive scan up to 2 levels; auto-uses dashboard GitHub PAT for private repos / higher rate limits
  - Supported types: CSV, TSV, JSON, YAML, Python, Markdown, log, TOML, .s2p, .s4p, and more
- **🔬 Analyse files with AI** — client-side pre-analysis before any LLM call:
  - CSV/TSV: delimiter detection, column type inference, count/null%/min/max/mean/median/std, IQR outlier detection, Pearson correlations
  - JSON: recursive schema map (4 levels), null field detection
  - YAML: top-level key extraction, null/empty field list
  - Pre-computed report sent to LLM; agent produces markdown table + anomaly flags + insight bullets
- Collapsible file panel (▶ header) — collapses to free up chat space; state persists in localStorage
- **⧉ Detach** — lifts the entire chat window into a free-floating, independently resizable overlay
  - Drag by title bar, resize from bottom-right corner, minimise to pill, ⊞ Dock back to modal
  - Window position and size remembered in localStorage

### Default dashboard
- Pre-populated with 38 building blocks across all 6 platforms
- SOI 220 nm: waveguides, bends, MMIs, directional coupler, grating couplers, edge coupler, ring resonators, crossing, MZI, thermal phase shifter, photodetector, spiral
- SOI 340 nm: waveguide, grating coupler, MMI, ring resonator, MZI modulator
- SOI 500 nm: waveguide, grating coupler, MMI (planned)
- TFLN 300 nm: strip waveguide, grating/edge couplers, EO phase shifter, MZI modulator, ring modulator
- SiN 300 nm: waveguide, grating coupler, MMI, high-Q ring resonator, Euler bend
- SiN 200 nm: waveguide, grating coupler, MMI (planned)
- Design Manual: Process Specs, Layer Maps, DRC, Designer Guide, EDA integrations (gdsfactory, IPKISS, KLayout)
- Post-Processing: DRC decks, GDS merge script, density fill, tape-out checklist

---

*CORNERSTONE PDK Monitor is licenced under the TAPR Open Hardware Licence v1.0.*
*Designed by Emre Kaplan · pdk.cornerstone.soton.ac.uk*
