# CORNERSTONE PDK Monitor — User Manual

**Version 1.2.0 · 28 May 2026**
Designed by Emre Kaplan · [pdk.cornerstone.soton.ac.uk](https://pdk.cornerstone.soton.ac.uk)
Licence: TAPR Open Hardware Licence v1.0

---

## Overview

The CORNERSTONE PDK Monitor is a single-file, browser-based dashboard for managing and monitoring Process Design Kit (PDK) building blocks (BBs), design documentation, and fabrication data for silicon photonics platforms. No server, no install — open `pdk-monitor.html` in any modern browser.

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Header Controls](#2-header-controls)
3. [Platform Tabs](#3-platform-tabs)
4. [Building Block (BB) Cards](#4-building-block-bb-cards)
5. [BB Detail View](#5-bb-detail-view)
6. [Data & File Management](#6-data--file-management)
7. [Multi-User Pool](#7-multi-user-pool)
8. [GitHub Integration](#8-github-integration)
9. [AI Insight Agent](#9-ai-insight-agent)
    - [9.1 Configuration](#91-configuration)
    - [9.2 BB Summariser](#92-bb-summariser)
    - [9.3 Multi-Turn Chat](#93-multi-turn-chat)
    - [9.4 GitHub File Fetcher](#94-github-file-fetcher)
    - [9.5 Analyse Files with AI](#95-analyse-files-with-ai)
10. [Roles & Access Control](#10-roles--access-control)
11. [Import / Export](#11-import--export)
12. [Keyboard Shortcuts](#12-keyboard-shortcuts)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Quick Start

1. Open `pdk-monitor.html` in Chrome, Firefox, or Safari (latest versions).
2. Accept the licence terms on first launch.
3. Click **ⓘ About** in the header to confirm the version.
4. Use the **platform tabs** (SOI 220 nm, SOI 340 nm, TFLN 300 nm, …) to navigate.
5. Click any BB card to view details, upload files, or add test data.
6. Click **🧠 Insight** to open the AI agent (requires an API key — see §9).

All data is stored locally in your browser's `localStorage`. To share or back up, use **Export JSON** or publish to a GitHub repository (see §8).

---

## 2. Header Controls

| Button | Function |
|--------|----------|
| 🔄 (refresh) | Reload model from localStorage |
| Search box | Full-text search across BBs, platforms, contributors |
| Status / Category dropdowns | Filter the BB list |
| Useful Links | Configurable chip links (set in About modal) |
| 🐙 GitHub | Configure GitHub PAT and identity |
| 🧠 Insight | Open the AI Agent (§9) |
| ⓘ About | Version info, notes, editable links and logo |
| 💾 / Export | Export dashboard JSON |

**Storage indicator** (bottom-left of header): shows localStorage usage. Turns amber at 70% and red at 90%.

---

## 3. Platform Tabs

Each tab represents one fabrication platform (e.g. SOI 220 nm). Tabs show:
- Platform name and material (Si / SiN / LN)
- BB count and completion statistics
- A progress bar coloured by status

**Adding a platform:** Click **+ Platform** (Admin only).
**Reordering:** Drag tabs left or right.
**Platform settings:** Click the ✏ icon on any tab to edit name, material, waveguide thickness, and default waveguide width.

---

## 4. Building Block (BB) Cards

Each BB is shown as a card with:
- **Name** and **type icon** (waveguide, MMI, ring resonator, grating coupler, etc.)
- **Status dot**: Available (green) · In progress (amber) · Planned (blue) · Discontinued (red)
- **Material badge**: Si · SiN · LN
- **EDA tools** supported (IPKISS, gdsfactory, KLayout, etc.)
- **File count** (GDS, S-matrix, scripts, images)
- **Contributor** chip
- **CDI axes** (Chip / Wafer / Assembly maturity, 1–4)

Click a card to open the **BB Detail** panel (right side).

---

## 5. BB Detail View

The detail panel has five tabs:

### Details
- Edit name, description, type, category, status, contributor
- Set CDI maturity levels (chip, wafer, assembly)
- Tag EDA tools where a PDK cell exists
- Assign to a platform variant

### Files
Upload or link:
- **GDS / OASIS** layout files
- **S-matrix** data (Touchstone `.s2p`, `.s4p`, CSV)
- **Images** (SEM, cross-section, layout renders)
- **Scripts** (Python, KLayout, gdsfactory cells)
- **Documents** (PDF datasheets, README)

Each file can be opened, downloaded, or deleted. GDS files render a layer-coloured preview inline.

### Tests
Log characterisation results:
- Add test entries with date, contributor, and pass/fail status
- Attach raw data files to each test
- View per-test metrics (insertion loss, return loss, bandwidth, etc.)

### 🧠 AI
AI-generated summary of this BB (requires API key — see §9.2). Shows:
- Executive sentence (≤40 words)
- Deep-dive analysis (1–3 paragraphs, citing only measured values)
- Cached after first generation; click **🔁 Refresh** to regenerate

### Parameters
Structured parameter table (waveguide width, gap, coupling length, etc.) editable per sub-entity (e.g. per waveguide width or platform variant).

---

## 6. Data & File Management

### Uploading files
Drag files onto a BB card or use the upload button in the Files tab. Supported formats: GDS, OASIS, s2p, s4p, CSV, TSV, PNG, JPEG, PDF, PY, KPY, LYML, and more.

### GDS viewer
GDS files render inline with layer colours from the configured GDS layer map. Hover a shape for layer name and description. The layer map is editable in **Manage Lists → GDS Layers**.

### S-matrix viewer
Upload a Touchstone file (`.s2p`, `.s4p`, `.sNp`) or CSV containing S-parameter sweeps. The viewer plots |S| vs wavelength/frequency for each port pair.

### Python script runner
Scripts tagged as Python can be run in-browser via a Pyodide sandbox. Output is shown in a console panel. For scripts that need native binaries or large datasets, use **💻 Run locally** to download a self-contained folder.

---

## 7. Multi-User Pool

The pool system lets multiple contributors maintain their own slices of the dashboard in separate GitHub repository folders (`users/<id>/`), which are merged on fetch.

| Button | What it does |
|--------|-------------|
| 📥 Fetch all sources | Fetches the main repo + all enabled user slices and merges |
| 📚 Fetch user repos | One-click fetch of all registered user repositories |
| 🔍 Discover user slices | Scans the `users/` folder of the configured repo for new contributors |
| 🪪 Fetch my slice | Fetches only your own `users/<id>/` folder |

**User-admin controls** (for contributors managing their own slice):
- Add / remove BBs in your slice
- Orphan pruning on publish (removes BBs from the repo that are no longer in the local model)
- **🗑 Wipe my repo folder** — removes your entire `users/<id>/` from GitHub

Duplicate BBs (same name across platforms or slices) are flagged in the **Duplicate Resolver**, where you can choose which version to keep or merge them as variants.

---

## 8. GitHub Integration

### Setting up your GitHub token

1. Click **🐙** in the header.
2. Paste a GitHub Personal Access Token (PAT) with `repo` scope (fine-grained: Contents read/write).
3. Optionally enter your GitHub username / email and display name.
4. Tick **Remember token** to persist in `localStorage` (stays on this device only, sent only to `api.github.com`).

### Publishing

Use **📤 Publish** (Admin) to commit the current `dashboard.json` and all file changes to the configured repository. The dashboard uses the real-files architecture — each uploaded binary lives as its own file; the JSON only stores metadata references.

---

## 9. AI Insight Agent

The AI Insight agent is powered by any Claude, OpenAI, or OpenAI-compatible API endpoint (including Ollama and LM Studio for local models).

### 9.1 Configuration

Click **🧠 Insight → ⚙ Configure** or open Insight and choose **⚙ Settings**.

| Field | Notes |
|-------|-------|
| API endpoint | Default: `https://api.anthropic.com/v1/messages`. For OpenAI: `https://api.openai.com/v1/chat/completions`. For Ollama: `http://localhost:11434/v1/chat/completions` |
| Model | e.g. `claude-sonnet-4-5`, `gpt-4o`, `llama3` |
| API key | Your `sk-ant-…` or `sk-…` key. Stored only in this browser's localStorage |
| Monthly token cap | Hard limit on input+output tokens per calendar month |
| Egress mode | **metrics-only** (safest) · **metrics + extracts** (4 KB per file) · **full** (50 KB per file) |
| Prompt style | Brief · Balanced · Deep (process-tolerance interpretation) |

Click **🔌 Test connection** to verify the endpoint, model and key before saving.

### 9.2 BB Summariser

Open any BB detail panel → **🧠 AI tab** → **🧠 Summarise this BB**.

The agent extracts metrics from all uploaded files (S-matrix data, test results, parameters) entirely in-browser, then sends only the computed JSON to the LLM. It never sends raw file bytes unless egress mode is set to "full". The resulting summary is cached and reused until you click **🔁 Refresh**.

You can also trigger an **📋 Executive summary** for an entire platform or the whole dashboard from the main Insight modal.

### 9.3 Multi-Turn Chat

Click **🧠 Insight → 💬 Chat with the agent**.

The agent has access to the following tools, which it calls automatically to answer your questions:

| Tool | What it reads |
|------|--------------|
| `list_platforms` | All platforms and their BB counts |
| `list_bbs` | BBs filtered by platform, category, status, or contributor |
| `get_bb` | Full detail for a specific BB |
| `list_contributors` | All contributors and their BB counts |
| `get_bb_metrics` | Computed metrics for a BB (calls the same extractor as the summariser) |
| `search_bbs` | Full-text search across names, descriptions, parameters |
| `summarise_bb` | Generates and caches an AI summary for a BB |

**Example queries:**
- "List every grating coupler on SOI 220 nm with their insertion loss"
- "Which BBs are in progress and have no S-matrix data?"
- "Who contributed the most BBs to the TFLN platform?"
- "Summarise the MMI 1×2 on SOI 340 nm"

Chat history is saved in localStorage and persists across sessions. Use **🗑 Clear conversation** to start fresh, or **⬇ Export .md** to download the transcript.

### 9.4 GitHub File Fetcher

Inside the Chat modal, the **📁 Data files in context** panel lets you load external data files for analysis.

**Supported URL formats:**

| URL type | Example |
|----------|---------|
| Single file (blob) | `github.com/org/repo/blob/main/data/results.csv` |
| Single file (raw) | `raw.githubusercontent.com/org/repo/main/data/results.csv` |
| Folder | `github.com/org/repo/tree/main/measurements/` |
| Repo root | `github.com/org/repo` |
| Multiple (one per line or comma-separated) | Paste several of the above |

**How to use:**
1. Paste one or more URLs into the textarea.
2. Click **Fetch** or press **Ctrl+Enter** / **Cmd+Enter**.
3. The fetcher resolves each URL, calls the GitHub Contents API for folders (recursive up to 2 levels), and loads every matching data file.
4. Loaded files appear as rows with ✅ (in context) or ⬜ (excluded). Click the icon to toggle, or ✕ to remove.

**Supported file types automatically fetched from folders:** `.csv`, `.tsv`, `.json`, `.yaml`, `.yml`, `.py`, `.md`, `.log`, `.txt`, `.toml`, `.ini`, `.cfg`, `.dat`, `.s2p`, `.s4p`

**Tip:** For private repos or to avoid the 60 req/hr unauthenticated limit, set your GitHub PAT in **🐙 GitHub** — the fetcher picks it up automatically.

All active files are injected into the AI system prompt for every subsequent chat message. The agent can then answer questions like "What is the mean insertion loss across all rows?" or "Are there outliers in column 3?"

### 9.5 Analyse Files with AI

Once one or more files are loaded and active (✅), click **🔬 Analyse files with AI**.

**What happens:**

1. **Client-side pre-analysis (instant, no API tokens used):**
   - **CSV / TSV:** delimiter detection → per-column type inference → statistics (count, null%, min, max, mean, median, std, Q1, Q3) → IQR outlier detection with examples → Pearson correlation for numeric column pairs
   - **JSON:** recursive schema map (4 levels deep) → null/empty field detection
   - **YAML:** top-level key extraction → null/empty field list

2. **LLM interpretation:** The pre-computed report is sent to the AI, which produces:
   - A **markdown table** of column statistics per file
   - **Anomaly flags**: constant columns, high-null columns (>30%), outlier-rich columns, strong correlations (|r| > 0.5)
   - **2–4 insight bullets** focused on what matters for a photonics PDK engineer

The analysis result appears as an agent reply in the chat, so you can follow up naturally: "What's causing the outliers in the loss column?" or "Filter the data to rows where IL > 3 dB".

---

## 10. Roles & Access Control

| Role | Permissions |
|------|------------|
| **Admin** | Full access: add/remove/edit all BBs, platforms, users, publish, manage lists |
| **User-admin** | Can edit BBs in their own `users/<id>/` folder; read-only for others |
| **Read-only** | View all data, run scripts, download files; cannot edit or publish |

The role is set in `localStorage` (key: `pdk-monitor.role`). By default the dashboard opens in read-only. To switch to Admin mode, see the comment at the top of the `<script>` block in the HTML file.

---

## 11. Import / Export

### Export JSON
Downloads the full dashboard model as `dashboard.json`. Use this to:
- Back up your data
- Commit to a GitHub repository
- Share with collaborators

### Import JSON
Loads a previously exported `dashboard.json`, replacing the current model. A local backup is saved automatically before replacing.

### Export BB folder (zip)
From any BB detail panel → Files tab → **⬇ Download folder**: downloads a zip containing all files for that BB, plus an auto-generated `README.md` manifest.

### Run locally (zip)
For Python scripts: downloads a self-contained folder with the script, its data files, and a `run.sh` helper, ready to execute from a terminal.

---

## 12. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `/` | Focus search box |
| `Escape` | Close modal / detail panel |
| `Ctrl+Enter` / `Cmd+Enter` | Send message in AI chat; Fetch files in URL input |
| `Ctrl+S` / `Cmd+S` | (In script editor) Save script |

---

## 13. Troubleshooting

**AI agent returns "No API key"**
→ Open 🧠 Insight → ⚙ Settings and enter your API key. Click 🔌 Test connection to verify.

**GitHub file fetch returns 403**
→ You've hit the unauthenticated rate limit (60 req/hr). Add your GitHub PAT in 🐙 GitHub settings.

**GitHub file fetch returns 404**
→ Check the branch name in your URL. GitHub defaults to `main`; some repos still use `master`.

**File fetcher loads 0 files from a folder**
→ The folder may contain no files with supported extensions, or it may be empty. Check the URL points to the correct subfolder.

**Storage indicator is red**
→ You're near the localStorage limit (~5–10 MB depending on browser). Export JSON, then use **🧹 Clear AI cache** in AI Settings and **Local Backups → Delete old backups** to free space.

**Pyodide script runner times out**
→ Pyodide loads from CDN on first use (~10 MB). Check your network connection. Scripts that import large packages (numpy, scipy) take longer to initialise.

**Dashboard shows stale data after a pool fetch**
→ Click the 🔄 refresh button in the header to reload the model from localStorage.

---

*For questions, issues, or contributions, see the GitHub repositories linked in the dashboard header.*
*CORNERSTONE PDK Monitor is free and open under the TAPR Open Hardware Licence v1.0.*
