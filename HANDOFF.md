# HANDOFF — for the next model / agent picking up this project

Read this FIRST, then skim `README.md`, `backend/README.md`, `data/README.md`,
`backend/AGENT_BRIEFS.md`, and the machine-readable to-do queue in
`data/ingestion_status.json`. This file is the single source of truth for how to
work on the project: architecture, environment, the ingestion method, hard-won
gotchas, and preferences.

## What this project is

An offline, double-click `index.html` all-sky atlas of every system with a
**spatially resolved circumstellar disk** (mm/submm interferometry + high-contrast
scattered light / thermal-IR), a **directly imaged exoplanet/companion**, or a
**coronagraphically imaged quasar/AGN host**. Every image is a low-res crop of a
peer-reviewed figure (or an official archive preview) with clickable **arXiv +
SciX** citations. Pure static files — no server, no build step at runtime.

## Current state (2026-07-07)

- **403 systems · 1200 image records (all with local panels) · full coords · 0 validate
  errors · SIMBAD idents coordinate-verified** (as of 2026-07-08; `python3
  backend/build.py` is always canonical). Several batches were USER-CANCELLED mid-flight —
  see `data/ingestion_status.json` → "user-cancelled-2026-07-07" for what remains open.

## Session state 2026-07-08 (live log — update on every hand-off)

CURRENT: 405 systems / 1249 image records / 0 errors (build.py canonical).
Paper-finder ledger: 484 in-atlas / 721 explored / 5477 known.

CRASH RECOVERY (2026-07-08): a process exit killed 7 background agents mid-run.
No partial data had merged (working tree was clean at commit c87218e). 43 orphan
PNGs (VIEW-verified crops whose staging JSONs were lost with the scratchpad) were
found on disk; 42 were recovered by re-deriving each source paper from the filename,
re-verifying every arXiv id from arxiv.org, and rebuilding full records
(data/staging/orphan-recovery.json, merged). 1 dropped (61 Vir Herschel — id
unverifiable). GJ 581 created + coords. All 42 papers marked in the ledger.

LESSON: the scratchpad (findings/cropresult/cache) is volatile across process exits.
Reconcile + merge agent output PROMPTLY (don't let many cropresults accumulate
unmerged), and commit after each batch.

NEXT QUEUE: keep triaging data/paper_finder/candidates.json in --rank order
(917 target-matched observation papers lead; run --rank after every --mark batch).
Genuinely-open PF4/PF6 leftovers (not recovered): 49 Cet Herschel (1907.06427),
Class I grain-growth 2309.06076, CGI AB Aur commissioning 2509.02681. Also: the
user-cancelled batches only on request; embedded-YSO/straggler ingests.
## Bookkeeping — the three ledgers (do NOT create a fourth)

1. **`data/systems/*.json`** — ground truth. A paper is "in the atlas" iff its arXiv id is
   cited by some record here. The paper-finder auto-treats all of these as done.
2. **`data/paper_finder_state.json`** — per-paper dispositions for papers NOT in the atlas:
   `{"<arxiv>": {"status": "excluded|ingested", "reason", "date"}}`. This is the dedupe
   ledger for the paper-finder Skill; add an entry every time you decide about a paper.
3. **`data/ingestion_status.json`** — per-survey/batch human ledger + session notes. Keep
   updating it after each batch, but per-paper decisions belong in ledger 2.
`data/paper_finder/` (candidates.json/md, cache/, triage-queue.json) is regenerable working
state for the Skill — safe to delete, expensive to refetch.

## The paper-finder Skill

`.claude/skills/diskatlas-paper-finder/` (user-authored SKILL.md + references;
`scripts/find_papers.py` added 2026-07-07). Literature snowballing: seeds = every cited
paper; expand along targets, instruments, and the citation graph BOTH directions (SciX
index, arXiv content; the script bulk-harvests forward citations via Semantic Scholar with
an on-disk cache). Triage with the relevance filter in the SKILL.md; ingest keepers through
the standard crop pipeline; print a per-paper report block in chat for every disposition;
mark ledger 2 via `find_papers.py --mark`. ~340 hub-ranked candidates remained queued in
`data/paper_finder/triage-queue.json` at the end of the 2026-07-07 session.

## How to pick up (quick start)

```bash
python3 backend/validate.py && python3 backend/build.py   # confirm 0 errors, see stats
```
Then: read `data/ingestion_status.json` (`pending_actions`, `known_missing`,
per-survey `notes`) for what's queued. The user typically (a) pastes arXiv links
to ingest, (b) asks for a comprehensiveness sweep, or (c) asks for a frontend tweak.

## Environment (IMPORTANT — differs from the original sandbox handoff)

- **This DGX session (`/home/brinen2spark/Developments/diskatlas`) HAS live internet
  from bash** — arxiv.org, aanda.org, and SIMBAD are directly reachable via `curl`.
  So you can run the whole pipeline yourself: `cd backend && bash fetch_sources.sh`
  downloads every referenced arXiv tarball + `fetch_extra.txt` PDFs + SIMBAD coords.
  No host hand-off is needed. (The repo still supports the old isolated-sandbox flow
  where the user runs `fetch_sources.sh` on a networked host — treat that as a
  fallback if `curl https://arxiv.org` ever fails here.)
- Tools available: `pdftoppm`, `pdfinfo`, ImageMagick `convert`, ghostscript `gs`
  (EPS → PNG: `gs -dEPSCrop -sDEVICE=png16m -r200`), Python + Pillow. Node is NOT
  installed (so `backend/test_frontend_logic.js` can't run here — verify the
  frontend via a preview server instead: `python3 -m http.server`).
- **Captcha/paywall reality**: IOP/AAS journal PDFs via `curl` return a **14367-byte
  captcha page** (the tell-tale size). ADS `link_gateway` targets, best→worst for curl:
  `EPRINT_PDF` (→ arXiv, best), `PUB_PDF` (works for A&A/AJ open-access, captcha for
  IOP ApJ/ApJL), `ADS_PDF` (scanned pre-~2005 only). Genuinely captcha-locked PDFs
  (e.g. recent ApJ, Nature/Science with no arXiv) need the user to browser-download
  into `images/_sources/extra/<name>.pdf` — give them the exact filename.
- A failed download can leave a garbage file that BLOCKS re-fetch (`fetch_sources.sh`
  skips existing files). Delete the bad file first; PDFs <20 KB are almost always HTML.

## The pipeline (scripts in backend/)

```
seeds/*.py ─┐
            ├─ make_systems.py (+ data/coords_cache.json) → data/systems/*.json
new JSON ───┘
data/systems/*.json → gen_fetch_script.py → fetch_sources.sh  (run in backend/)
   → images/_sources/arxiv/<id>.tar + extra PDFs + data/simbad_raw.txt
parse_simbad.py → data/coords_cache.json         (coords/plx/sptype/UBVGRIJHK mags)
extract_sources.py → images/_sources/extracted/<id>/   (tar → tex+figs, or PDF)
crop → images/<sid>/<image_id>.png (≤560–640 px, ≤300 KB PNG)
merge_staging.py  (folds data/staging/*.json image records into data/systems/*.json)
validate.py && build.py → frontend/data.js (+ stats)
coverage_audit.py → data/coverage_todo.md
```
- `gen_fetch_script.py` collects every arXiv id in `seeds` + `data/systems/*.json`
  images, adds `backend/fetch_extra.txt` (`URL<TAB>dest` for non-arXiv sources), and
  writes the SIMBAD `sim-script` for every system whose `ra_deg` is null.
- `merge_staging.py`: a staging record = image-record fields + `system_id`. Existing
  `image_id`s are **updated in place** (only non-null staging fields win). New systems
  get a minimal shell. So to fill a `file:null` record without clobbering its metadata,
  stage just `{system_id, image_id, file, credit}`.

### Pipeline gotchas (each has bitten past sessions)
- **Coords for non-seed systems**: `make_systems.py` applies `coords_cache` ONLY to
  seed systems. Systems you create directly as JSON must have ra/dec/plx/mags/sptype
  filled DIRECTLY from `data/coords_cache.json` with a small script after `parse_simbad.py`.
  For objects whose designation encodes coordinates (e.g. `HSC Jhhmmss.ss±ddmmss.s`,
  SHELLQs quasars), parse RA/Dec straight from the name — SIMBAD may not resolve them.
- **Deleting a record permanently**: remove it from BOTH the system JSON and any seed
  that generated it, else `make_systems.py` resurrects it.
- **image_id**: `<sysid>_<slug>` — survey members use the survey slug; singles use
  `<facility/instrument-slug><year>` (e.g. `hd-163296_stis2000`, `2m1207_nicmos2006`).
  Keep consistent to avoid duplicates.
- **Wrong-system assignment**: a sweep agent once put V1247 Ori's ALMA image on PDS 201
  (same first author, different target). Always confirm the paper's target matches the
  system — the crop VIEW step catches this.

## Ingesting via parallel agents (the modern, primary method)

Batches are done with background subagents (the Agent tool in Claude Code; historically
called the "Workflow tool"), not by hand. Two patterns, both battle-proven:

1. **Research/verify sweep** — one agent per paper cluster or per system-chunk. Each
   agent WebSearches, VERIFIES the arXiv id by fetching its abstract (title+author
   match — never trust an id from memory), and returns a **structured** finding
   (arxiv, figure, target, instrument metadata, ingestable?). You then add records.
2. **Crop workflow** — one agent per source figure/record. Each agent renders the
   figure (`pdftoppm`/`gs`), **VIEWs it with the Read tool** (panel labels are the only
   ground truth), crops the right panel, saves to `images/<sid>/<image_id>.png`, VIEWs
   the saved crop to self-verify, and returns `{system_id, image_id, file, credit, ok}`.
   You collect the ok crops, write ONE staging file, merge, build.

**Agent-fleet gotchas (critical, each has bitten):**
- **Hardcode file paths in agent prompts** (chunk file in, result file out); never rely on
  argument propagation. Write shared briefs (crop rules, schema) to one scratchpad file and
  have every agent read it.
- **export.arxiv.org rate-limits hard (HTTP 429) when tens of agents share one IP.**
  Working fallbacks: `arxiv.org/abs/<id>` HTML meta tags (citation_title/author),
  `arxiv.org/pdf/<id>`, Semantic Scholar API. The orchestrator re-verifies every id
  centrally anyway; crop-VIEW is the content check of last resort.
- **Parallel `curl` PDFs get silently truncated** (exactly 4 MiB, or corrupt xref). Check
  `pdfinfo` after download; re-fetch sequentially with `--max-time 90` on failure.
- **Agents sometimes spawn their own background children and stop ("I'll wait")** — the
  completion notification fires but the work is half-done. Resume them with SendMessage:
  "do it yourself synchronously; reconcile what your children left on disk first."
- Some crop agents die after saving PNGs — always **reconcile against disk** (the
  reconcile.py pattern: result JSONs + PNG existence + id-collision checks) rather than
  trusting returned JSON.
- New-system agents may both create the same system when batches overlap — instruct
  re-`ls data/systems/` right before each write, and spot-check after.

### The instrument-level coverage sweep (comprehensiveness tool)
The coarse `coverage_audit.py` only tracks mm/nir/planet modality gaps. The higher-value
sweep is **instrument-level**: build a per-system inventory of existing
`(facility/instrument)` sets, then run ~1 agent per 6-system chunk to find published
**resolved images from instruments NOT yet represented** for each system. This found 40+
real additions (e.g. 2M1207/NICMOS, 51 Eri/SPHERE, HR 4796A/MagAO-X, HH 30/JWST,
NGC 1068/GRAVITY, LBTI/LMIRCam LEECH planets). Re-run periodically; the user cares about
instrument/epoch completeness, not just filling empty modality buckets.

## Crop discipline (full protocol in backend/AGENT_BRIEFS.md)
- Panel labels INSIDE figures are the ONLY ground truth for target identity — never
  guess from position or memory.
- VIEW every crop (Read tool) before staging. `_sources/_views/` is the scratch dir for
  rasterized figures to Read; clean it (`rm -f images/_sources/_views/*.png`) when done.
- **Panel-only crops (2026-07-07 rule): trim axes, tick labels and white margins — keep
  just the image panel** (attached colorbars may stay). A batch trimmer with a safe
  fallback for white-background contour figures lives in the session log; new crops
  should be cut panel-only at the source.
- Output: longest side capped at **480 px** (≈150 dpi of a typical panel; uniform across
  the atlas), ≤300 KB. If a noisy PNG exceeds 300 KB, requantize:
  `img.quantize(colors=256, method=Image.FASTOCTREE)`.
- QA: the four cropped edges should each be near-uniform in color; OCR (tesseract) must
  not find a target-name at the crop CENTER (offset-grid bug) nor axis values at edges.
- No press-release composites, ever — only peer-reviewed figures / official archive previews.
- If a "found" paper turns out to be uv-plane modeling with no image-plane figure, DROP
  the record (happened with HD 141569 / White 2018).

## Data conventions (schema in data/README.md)
- `hires_url` (optional): external hi-res source. Set on ALICE HLSP NICMOS records →
  `https://archive.stsci.edu/prepds/alice/`; the frontend shows a "hi-res data ↗" link
  to it instead of the arXiv PDF.
- Quasars: `categories:["quasar"]`, `redshift` (not `dist_pc`), `image_type:"quasar"`.
- Citations render **arXiv + SciX** (scixplorer.org, the ADS successor) — NOT NASA ADS.
- Transiting planets must NOT be called "imaged" (`method:"transit"`, separate from imaging).

## Frontend (frontend/ — pure vanilla JS, offline, file://)
- `index.html` loads `data.js` (generated — never hand-edit), `constellations.js`,
  `i18n.js`, `app.js`, `style.css`.
- **Views** (top switcher): Sky map · Coverage matrix (systems × Visible/NIR/MIR/mm/Planet,
  a live gap-finder) · Tonight (observability planner: site + date → airmass/transit + CSV).
- **Faceted filters**: wavelength band / missing-modality / facility, driving all views.
- **Multi-language** (`frontend/i18n.js`): English / 中文 / Français / Español, persisted in
  localStorage. UI strings route through `t(key)` / `data-i18n`; scientific data stays as-is.
- **Facets**: band / missing-modality / **Facility** (AAS facility keywords via
  `backend/facility_map.py`, applied at build time as `fac_keys`; A+B images appear under
  both; VLT selection also matches VLTI) / **Instrument** (`instr_key` families; top-8 by
  usage first, alphabetical, then the rest).
- **Light/dark theme** toggle (`body.light`, persisted; `refreshCOL()` re-reads CSS vars,
  canvas sky uses `--sky`). **Tonight** rows link to per-object airmass.org charts
  (obsid map in SITES). Notes auto-linkify "Author+Year" to SciX searches;
  `planets[].extra_papers` render as extra arXiv/SciX links. Systems with `simbad: null`
  get a SIMBAD coordinate-search link instead of an Ident link.
- **Markers**: distinct SHAPE per category (● proto / ▲ debris / ◆ planet-only / ■ quasar,
  colorblind + B/W-print friendly), a **★ star** overlay marks imaged-planet hosts, and a
  white circle marks selection. Marker size is uniform per type (image count only sets fill
  opacity). Sky Dec axis is bounded to −90…+90 via `view.topInset` (header offset).
- Verify frontend changes with a preview server + screenshots/eval (Node isn't installed).

## User preferences
- **Reply in English** (the project originally used Chinese; the user switched — repo docs
  are English regardless).
- Active astronomer; supplies arXiv links rapid-fire and expects each ingested (record +
  citation + VIEW-verified crop). Happily browser-downloads captcha-locked PDFs when given
  exact filenames.
- **Comprehensiveness is the goal**, at instrument/epoch level: multi-instrument,
  multi-epoch, historical (back to Smith & Terrile 1984), extragalactic (quasar hosts).
- Verify paper metadata FROM THE SOURCE, not memory. No press-release images. Redshift for
  quasars. Keep `validate.py` at 0 errors and update `README.md` + `data/ingestion_status.json`
  stats after each batch.

## Where the current work lives
`data/ingestion_status.json` — per-survey status + `known_missing` + `pending_actions`
(machine-readable; update it every time you ingest). `data/coverage_todo.md` — coarse
modality gaps (mostly genuinely unobserved). Beyond that: watch new astro-ph.EP/SR
postings and re-run the instrument-level sweep for deeper completeness.
