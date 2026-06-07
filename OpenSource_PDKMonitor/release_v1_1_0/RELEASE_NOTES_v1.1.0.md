# CORNERSTONE PDK Monitor — Release Notes

## v1.1.0

A maintenance + capability release focused on **resilient fetching** and **storing large datasets outside GitHub**. The headline feature is provider-agnostic cloud storage: keep the catalogue in GitHub and the heavy raw data on any cloud service, fetched on demand.

### Highlights

- **Cloud data storage (any provider).** Datasets no longer have to live in the GitHub repo. Point a file, folder, or whole BB at a cloud location and the dashboard fetches the bytes on demand and caches them locally. Works with any host that allows cross-origin (CORS) reads — Amazon S3, Azure Blob, Google Cloud Storage, Backblaze B2, Cloudflare R2, MinIO, an internal file server, and Dropbox / Google Drive share links — plus private **SharePoint / OneDrive** via Microsoft sign-in.
- **Per-tab `☁ Cloud links` buttons**, next to `⤓ GitHub fetch`, on every BB tab (Layout, S-matrix, Tests, Fabrication, Scripts, Documents). **Available to read-only viewers** so anyone can pull data.
- **Fetch everything in a folder.** A tick option lists the cloud folder and pulls every file (S3 via ListObjectsV2, SharePoint via Microsoft Graph), in addition to name-matching.
- **One-click BB fetch.** The Details tab has a `☁ Fetch all cloud data for this BB` button that runs every section's cloud links at once and populates the BB.
- **Per-link Test button** that performs the same request the real fetch uses, so it honestly reports CORS reachability before you commit a link — and surfaces S3's actual error reason (e.g. `AccessDenied`) instead of a bare 403.

### Reliability fixes

- **Read-only Distribution fetch works again without a PAT.** `dashboard.json` files over 1 MB no longer fail: the fetch falls back to `raw.githubusercontent.com` (no size cap, no auth needed for public repos) when the GitHub Contents API returns 403.
- **Contributor (`users/`) repos are pulled by default again** during a Distribution fetch, with a safety-net fallback that walks `users/` if the main fetch finds nothing.
- **Platform import survives GitHub's unauthenticated rate limit.** When the per-folder Contents API listing 403s, the importer falls back to a single Git Trees call, so public platforms import without a PAT.
- **Fixed a crash that left "Merge / Replace" disabled** after a successful fetch (a null SHA from the raw-host path broke the preview render).

### New collaboration + UX

- **Per-item comments.** Any contributor can comment on items created by others — S-matrix folders, test folders, fabrication sub-tabs, and scripts each have their own `💬 Comments` thread. Author or admin can delete; comments travel with publish/merge.
- **Platform import defaults the parameters/dimensions section OFF** for imported BBs (enable per BB when you want a parameter table in Details).
- **Auto-generated BB sketches removed.** Sketches are now managed solely via repo fetches, uploads, or the shared sketch library; the panel shows a neutral placeholder when no image is supplied.
- **Contributor list Save button** no longer shows a stuck "busy" cursor after saving.

### Cloud, continued

- **Two-source model (GitHub + cloud mirror).** A platform import can name a cloud mirror of the repo; GitHub stays the principal source (catalogue + layout) while the cloud assists with heavy data. A default-off *"populate cloud links"* tick distributes per-tab links that mirror the repo's **real** folder names (discovered from GitHub), nested per BB. A **☁ Cloud sync** button re-distributes links without downloading.
- **☁ Cloud folder on fetch.** Fetched files land under a clearly-marked **☁ Cloud** folder, with the cloud's subfolder structure recreated as nested subfolders so it's obvious what came from cloud.
- **Individual single-file fetch.** Handles the common S-matrix layout where a section's data is one file named after the BB (`sparams/<bb>.csv`), not a per-BB folder. **Fetch everything** (re-added, off by default) lists the whole folder recursively when you want it.
- **Cloud upload (admins).** Push files *into* your bucket — AWS S3 / S3-compatible (browser-side **AWS Signature V4**) or a generic PUT endpoint. Configure once in ☁ Cloud storage; then any S-matrix / Tests / Fab folder has a **⬆ Cloud upload** button that mirrors the folder (and subfolders) up. Credentials stay in the browser only.
- **Design-manual cloud fetch** alongside GitHub sync.

### Data integrity & repo size

- **Published `dashboard.json` is now metadata-only.** File bytes and parsed arrays (S-matrix / tests / fab / uploads) are stripped on publish regardless of size — only filenames, sizes, cloud/GitHub pointers, comments and notes travel. This stops repos ballooning as data and comments accumulate; adopters re-hydrate bytes on demand. Small documents/YAML descriptors (<512 KB) still round-trip. Local copies keep full bytes.
- **Details notes propagate and merge.** A note added to any BB (even one you don't own) now travels in your slice and is unioned across contributors on fetch — so you see everyone's comments, de-duplicated by id.
- **File totals include subfolders.** Platform summaries, BB tab badges, and the dashboard overview now count files inside nested subfolders.

### Tidy-up & navigation

- **Consolidated header.** About now hosts Contributors / Help / Activity; **⚙ Configuration** hosts GitHub account / Cloud storage / Manage lists / Status manager (with a GitHub connection dot); **Analyse ▾** hosts cross-platform analysis + AI Insight; **⬇ Download ▾** hosts scoped download / Export BBs / Backup; **⤓ Import ▾** hosts import + GitHub fetch. Dropdowns auto-fit within the viewport.
- **‹ Back button** on every nested modal, so you can step back through windows.
- **Duplicate-files resolver** (Distribution) finds files duplicated within a BB across tabs/subfolders/uploads and lets you delete the redundant copy.
- **File multi-select.** Per-folder **Select all / Delete selected** on S-matrix / Tests / Fab folders (and subfolders).
- **Uploads view** now lists **layout files (GDS/OAS/SVG)** per BB and allows per-file deletion.
- **Platform Select-all** appears once you tick a BB, keeping the column header clean.

### Defaults

- Removed the default `cornerstone-uos/cornerstone-community` header link from a fresh install (both the code default and the bundled default dashboard).

### Notes & requirements

- Cloud fetching is **client-side**: the host must allow CORS. For S3, add a bucket CORS rule (`GET`/`HEAD` for your dashboard origin) and make objects readable (public-read or pre-signed URLs). For private SharePoint/OneDrive, register an Azure AD single-page-app and sign in via `☁ Cloud` settings; this requires the dashboard to be served over **https** (not `file://`).
- Auto-discovery (listing a folder) is supported for S3 (needs `s3:ListBucket`) and SharePoint/OneDrive; other hosts need filenames from a GitHub fetch or per-file links.

---

*First designed and released by Emre Kaplan, University of Southampton. Maintained by the CORNERSTONE PDK team.*
