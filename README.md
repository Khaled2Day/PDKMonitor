# CORNERSTONE PDK Monitor — v1.1.0

A free, open-source, **single-file** dashboard for managing and sharing integrated-photonics Process Design Kits (PDKs). It is the gateway between designers and fabs: a single place to discover, use, and contribute open PDK building blocks (BBs) — layouts, S-parameters, test data, fabrication notes, scripts, and documents.

The entire app is one self-contained `.html` file. There is no server and no build step — open it in a browser, or host it on GitHub Pages / SharePoint / an internal server.

## What's in this bundle

| File | What it is |
|------|------------|
| `cornerstone-pdk-monitor-v1.1.0.html` | The dashboard. Open this in a browser. |
| `USER_MANUAL.md` | Full user guide — modes, fetching, cloud storage, publishing. |
| `RELEASE_NOTES_v1.1.0.md` | What changed in this release. |
| `CORNERSTONE_PDK_Monitor_Intro_v1.1.0.pptx` | Introduction slide deck. |
| `README.md` | This file. |

## Quick start

1. **Open** `cornerstone-pdk-monitor-v1.1.0.html` in a modern browser (Chrome / Edge / Firefox / Safari). It opens in **read-only** mode — browse everything, change nothing.
2. **Load the live data.** Click `🌐 Distribution` → *Fetch all enabled sources* to pull the published dashboard (and contributors' slices) from GitHub. No GitHub account or token needed for public repos.
3. **Explore.** Click any building block to see its Layout, S-matrix, Tests, Fabrication, Scripts, and Documents tabs.
4. **Sign in to contribute.** Admin / user-admin modes let you add and publish BBs and files.

## Working with large data (new in 1.1.0)

GitHub is for the catalogue, not gigabytes of raw data. Keep heavy datasets in cloud storage and let the dashboard fetch them on demand:

- Click `☁ Cloud links` on any BB tab (or `☁ Fetch all cloud data` on the Details tab).
- Paste a direct/public/pre-signed URL (S3, Azure Blob, GCS, …) or a SharePoint/OneDrive share link.
- Use `🔎 Test` to confirm the link is reachable, then fetch. Tick **Fetch everything** to pull a whole folder (incl. subfolders).
- **Admins can upload too** — configure a bucket in `⚙ Configuration → ☁ Cloud storage`, then use `⬆ Cloud upload` on any folder to push data into S3 (browser-side AWS SigV4) or a generic PUT endpoint.

The published `dashboard.json` is a **metadata-only catalogue** — file bytes live in cloud/GitHub and are fetched on demand, so the repo stays small even as data and comments grow.

See `USER_MANUAL.md` for S3 CORS setup, SharePoint sign-in, and the full feature guide (consolidated header, duplicate resolvers, uploads view, comments).

## Hosting

Open locally for personal use, or serve over **https** (GitHub Pages, SharePoint, internal server) — https hosting is required for SharePoint/OneDrive sign-in and for S3 CORS to whitelist a stable origin.

---

*First designed and released by Emre Kaplan, University of Southampton. Maintained by the CORNERSTONE PDK team. Open to everyone — let's build the open integrated-photonics community together.*
