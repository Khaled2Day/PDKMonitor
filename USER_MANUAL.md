---
title: "CORNERSTONE PDK Monitor — User Manual"
subtitle: "Version 2.1.0"
author: "CORNERSTONE Open Platform PDK · University of Southampton"
date: "June 2026"
---

# 1. Introduction

**PDK Monitor** is a single-file, browser-based dashboard for managing the
content of an open-source photonic **Process Design Kit (PDK)**: the building
blocks (BBs), their layouts and GDS, S-parameters, characterisation and test
data, fabrication notes, documentation, and their **maturity** — captured by the
**Component Development Index (CDI, 1a–4b)**.

It is designed for the CORNERSTONE Open Platform and runs entirely in your web
browser. There is **nothing to install**, no server, and no database — the whole
application is one HTML file. Your team shares and aggregates content through a
GitHub repository, so many contributors can build one trusted, living view of
the PDK.

**Who this is for**

- *Anyone* who wants to browse what is in the PDK and how mature each block is
  (read-only — no sign-in).
- *Contributors* (user-admins) who add their own building blocks, measurements,
  and documents and publish them back to the repository.
- The *curator* (admin) who maintains the canonical dashboard.

# 2. Quick start

1. **Open** `cornerstone-pdk-monitor-v2.1.0.html` in a modern browser (Chrome,
   Edge, Firefox, or Safari). You can double-click the file, or host it on
   GitHub Pages and open the URL.
2. On first launch you will see the **Terms of Use** prompt. Read the summary
   (or expand the full text), tick the box, and click **Accept & continue**.
   Nothing is sent anywhere.
3. The dashboard opens in **Read-only** mode. Browse the **Technology Platforms**
   tab, search, filter, and open any building block — no sign-in required.

> The application works fully **offline** once it has loaded. It stores your
> working copy in your browser, so re-opening the same file in the same browser
> shows where you left off.

# 3. Roles and signing in

PDK Monitor has three roles. Switch role with the **mode pill** in the top-right
corner.

| Role | What you can do | How to enter |
|------|-----------------|--------------|
| **Read-only** (default) | Browse, search, filter, export. | No sign-in. |
| **User-admin** | Add and edit **your own** building blocks, files and data; publish them to the repository. | Sign in with a **GitHub Personal Access Token** (and your email or GitHub username). |
| **Admin** | Full control of the canonical dashboard, lists, CDI definitions, and resets. | Sign in with the global **admin password**. |

**Signing in (user-admin).** Click the mode pill → **Sign in**. Paste a GitHub
token (`ghp_…` classic, or `github_pat_…` fine-grained). The token stays in your
browser session only; it is never transmitted anywhere except GitHub when you
publish. A trust-token is shown in the sign-in prompt — if it does not match the
one shown earlier in the same browser session, close the tab and reopen the
dashboard from a trusted source before entering anything.

**What user-admins may change.** You may add new content to *any* block (that is
how contributors feed each other's dashboards), but you can only **edit or
delete** items you created yourself. Items owned by someone else show a 🔒 lock
in place of the delete control; **click the lock** to see why it is restricted.

# 4. The board

**Tabs** across the top group the PDK into **technology platforms** (for example
*SOI 220 nm Passive/Active*, *SiN 300 nm*). Each tab holds **platform groups**,
and each group holds **building-block cards**.

- **Search** — the search box matches names, owners, and files across the board.
- **Filters** — narrow by **status**, **category** (passive/active), and **BB
  type**.
- **Contributor filter ("All users")** — scope the board to the building blocks
  created by a particular contributor. The list shows the people who actually
  own building blocks in the dashboard.
- **Status badges** show availability at a glance.

Expand any card to open the building block's full record.

# 5. Working with a building block

A building block gathers everything known about one component:

- **Identity** — name, category (passive/active), status, owner.
- **CDI** — its single demonstration-maturity rank (see §6).
- **Layout** — GDS / SVG preview with a layer legend.
- **Files & scripts** — datasheets, simulation and measurement scripts.
- **S-matrix datasets** — scattering-parameter data.
- **Test results** and **Fabrication** tabs — measured data and fab notes.
- **Documents** — component YAML, ready-made notes, design manuals.
- **Variants** — different generations of the same device, grouped under a
  parent block, each with its own data.

To add content (user-admin/admin), open a block and use the upload / add
controls in each section. Drag-and-drop is supported for files.

# 6. CDI — the Component Development Index

CDI is a **single maturity rank from 1a to 4b** for every building block, built
on a **five-stratum nested model** of where the evidence comes from:

> σ²_tot = σ²_B + σ²_W + σ²_D + σ²_E + σ²_ε  
> (batch, wafer, die, device, measurement)

Each rung "turns on" one further stratum of evidence. Scope is foundry /
chip-level only — there is no packaging or assembly level.

| CDI | What it demonstrates | Gate | Level |
|-----|----------------------|------|-------|
| 1a | Theory / simulation only — no measurement | — | Theoretical |
| 1b | First experimental proof-of-concept | 1σ | Experimental |
| 2a | Foundry-fabricated; single device, repeatability | 1σ | Chip |
| 2b | Multiple devices on one die (device-to-device) | 1σ | Chip |
| 3a | Multiple dies on one wafer (die-to-die) | 1σ | Wafer |
| 3b | Across multiple wafers (wafer-to-wafer) | 2σ | Wafer |
| 4a | Multiple foundry batches (batch-to-batch) | 2σ | Batch |
| 4b | Sustained across batches; system-qualified | 3σ | Batch |

**Setting a block's CDI.** In the block editor, choose the **CDI** rank from the
dropdown; the panel shows that rank's official description and pass criterion.
Admins can edit the rank definition texts via **✎ Edit definitions**.

**CDI reference.** Open **Help → 📊 CDI levels** for the full staircase (which
strata each rung requires) and the complete definitions table.

## 6.1 The CDI Calculator

The dashboard ships with a full **CDI Calculator** that computes a block's CDI
from measurement data. Open it from the **Analysis** view → **🧮 CDI
Calculator** (it opens in its own window), or use the standalone file
`cdi_calculator.html`.

- **Specifications** table — one row per BB criterion (spec limit, ≤/≥
  direction, optional σ_model).
- **Measurements** table — one row per measurement: the **CDI level** it
  supports, a **GroupID** (the top token is the batch/run, e.g. `Run1/W2/D3`,
  which drives the nested variance), and the **value**.
- **Import Excel template** — load a `.xlsx` with `BB_Specs` and `Measurements`
  sheets; rows are appended to the tables. A ready-made rich template
  (`CDI_BB_template_rich.xlsx`) is included.
- **Run analysis** computes, for every level: sample size and adequacy status,
  the **Nσ criterion** (μ̂ ± gate·σ̂ vs spec), Cpk, yield, nested variance
  components, and the rigorous **unified 95 % tolerance** test
  (μ̂ ± k·σ̂_tot with an **exact non-central-t** tolerance factor *k*).
- **Achieved CDI** cards show the highest claimable level per block (scrollable
  and searchable). **Click a card** to preview that block's qualification
  datasheet.
- Every result column has a **hover info window** explaining the quantity.

## 6.2 Qualification datasheets

From the calculator's **Datasheets** section (or by clicking an Achieved CDI
card) you can generate a one-page **CORNERSTONE qualification datasheet** per
block: point estimates and the Nσ test, the unified tolerance criterion, the
fabrication-scope evidence vs the CDI minimums, and pre-check diagnostics. Pick
one, several, or all blocks (with a search box), then **Download → PDF** — the
datasheets open in a print window; choose **Save as PDF** to keep them.

# 7. Benchmarking

Compare platforms and building blocks on key photonic metrics.

- Editable **tables, one per metric**, with live **bar charts**.
- **Detach** the chart into its own floating window, and **hide the table** to
  enlarge the graph.
- Built collaboratively: every admin (including user-admins) can add rows and
  metrics, and each row records **who contributed it**. Contributions merge
  additively when slices are fetched.

# 8. Cross-platform analysis

The **Analysis** view is one screen to see the whole PDK: counts of blocks,
S-matrix datasets and test files across a selection; **BB distribution by
platform** (click a slice to drill into status / category); the benchmark
tables and charts; and the **CDI Calculator** launcher. Export a scoped overview
to **Markdown or Excel** for reports. The window adapts to its size — shrink it
and everything still fits.

# 9. Contributing (the fork-and-merge model)

PDK Monitor aggregates work from many people without anyone overwriting anyone
else:

1. **You keep your own slice.** Your contributions live under
   `users/<your-login>/` in the repository.
2. **Publish** — when signed in as a user-admin, your additions and edits are
   written to your own slice (Fork & PR where needed).
3. **Fetch & merge** — the dashboard pulls every slice and **merges them
   additively** into one aggregated view. Nothing is overwritten; same-named
   blocks can be merged or kept as **variants**.

Because the merge is additive and non-destructive, removing something locally
does not delete other people's contributions.

# 10. Keeping the data clean

- **Duplicate resolver** — finds blocks that share a name. **Same-platform**
  duplicates can be merged into one keeper; for any cluster you can also
  **Make variants** (attach the others as sub-blocks of the keeper). A backup
  `.json` downloads before any change so you can roll back.
- **Manage lists** — statuses, categories, BB types, EDA tools, platforms, and
  the **benchmark metric list** are all editable; contributions merge add-only.
- **Editable CDI definitions** — admins maintain the official rank descriptions
  (Calculator/Help → Edit definitions).

# 11. Distribution & sync

The dashboard fetches from configured **distribution sources** — the canonical
`cornerstone-uos/PDKMonitor` dashboard and the `users/` folder of contributor
slices. Use the distribution panel to pick which slices to install. A
**Read-only** user can refresh from a trusted source without being able to add
arbitrary content.

# 12. Data, storage & privacy

- The application is **one self-contained HTML file**. It collects **no
  telemetry**.
- Your working copy is stored **in your browser** (IndexedDB / localStorage), so
  edits persist across reloads on the same machine. **GitHub is the source of
  truth** for shared content.
- **Export / backup** — you can export the dashboard content (Markdown / Excel),
  and a backup `.json` is downloaded before any merge or dedupe.
- Because the model is stored in your browser, **editing the HTML file does not
  change what a returning browser shows** until you Reset or clear site data.

# 13. Troubleshooting & FAQ

**My change / the new data isn't showing.** Your browser is loading its saved
copy. Use the dashboard's **Reset**, or clear the site's storage, to pick up a
fresh file.

**I clicked a 🔒 lock and nothing was removed.** That control is locked because
you do not own the item (or you are read-only). The lock now shows a message
explaining who owns it — only the creator or a full admin can remove it.

**Pop-up blocked when opening the CDI Calculator / a datasheet.** Allow pop-ups
for the site, then click again.

**Excel import needs internet the first time.** The standalone calculator loads
the spreadsheet parser from a CDN on first import; when launched from the
dashboard it reuses the copy already loaded.

**The CDI ladder stops at a low level.** The *achieved* CDI climbs contiguously
from 1b — a level with no data (or a failing spec) stops the ladder. Check the
per-level results table for the first FAIL or "no data".

# 14. Appendix — bundle contents

This release (`cornerstone-pdk-monitor-v2.1.0.zip`) contains:

- `cornerstone-pdk-monitor-v2.1.0.html` — the dashboard application.
- `cdi_calculator.html` — the standalone CDI Calculator.
- `CDI_BB_template_rich.xlsx` — a rich BB spec/measurement template (full CDI
  ladder, n ≥ 100 at 4b) for the calculator's Excel import.
- `USER_MANUAL.pdf` / `.docx` / `.md` — this manual.
- `CHANGELOG.md` — what changed in v2.1.0.
- `README.txt` — bundle overview and quick start.
- `CORNERSTONE_PDK_Monitor_Introduction.pptx` — an introductory slide deck.
- `dashboard.json` — the baked dashboard model (reference export).

---

*CORNERSTONE Open Platform PDK · University of Southampton · PDK Monitor
v2.1.0.*
