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

## Current state (2026-07-09)

- **466 systems · 1484 image records (all with local panels) · full coords · 0 validate
  errors** (`python3 backend/build.py` is always canonical). Paper-finder ledger:
  ~565 in-atlas / ~857 explored / ~9915 known-candidate (the "known" pool ballooned
  after adding the backward-reference axis — see below; it is a discovery-frontier
  count, NOT papers read).
- Published live at **github.com/seawander/diskatlas** + GitHub Pages. Publish flow is
  **direct push to `master`** (no PRs; `gh` is not installed). Multiple checkouts/sessions
  commit to `master` concurrently — always `git fetch` before assuming ahead/behind.

## Session state 2026-07-09 (live log — update on every hand-off)

CURRENT: 466 systems / 1484 image records / 0 errors.

WHAT THE 07-09 CONTINUATION DID (all committed + pushed to master):
- **Directed multi-figure adds (user-requested, high yield):** Weber+2023 SPHERE/IRDIS
  H for AS 205 / SR 24S / FU Ori; Dasgupta+2025 ERIS L' for V960 Mon; Ren+2019 Fig. 1
  STIS/NICMOS/GPI for HD 191089; Faramaz+2021 ALMA B7 for HR 8799; Stark+2023 STIS for
  HD 53143; Wagner+2015 IRDIS K1/K2 + IFS Y/J/H for HD 100453. FIXED DoAr 44 Casassus
  mislabel (crop was Fig 1b = ALMA 336 GHz, labeled SPHERE → split into correct a+b).
- **NEW TOOL `backend/system_audit.py` — target-side completeness audit** (see the
  `target-side-completeness-audit` memory). ADS `abs:"<name>"` per system (anonymous
  tier has NO `object:`), gate = imaging-phrase + named-facility + DISK_CTX
  (disk/companion context; kills the abs:"DO Tau"→Planck collisions), rank by
  citations × instrument-novelty. Headline output = NEW-INSTR gaps. Cache + report
  under `data/paper_finder/` (gitignored). Verified finds ingested: PDS 70 MagAO Hα
  (Wagner+2018 — the ORIGINAL accreting-planet detection), HD 100546 MagAO Hα
  (Follette+2017), HR 4796A MagAO Clio-2 L' + VisAO Ys (Rodigas+2015), HD 100453 NACO
  Ks companion-B discovery (Chen+2006, non-arXiv; ADS `link_gateway/<bib>/PUB_PDF`).
  False positives correctly skipped by VIEW-verify: Fomalhaut "Subaru" (J-band
  non-detection), HD 100546 "ZIMPOL" (sample mention; figures are HD 142527).
- **Miles Lucas feedback:** instrument taxonomy now `SCExAO/CHARIS` (23 records,
  was flat CHARIS) + `SCExAO/VAMPIRES` + `SCExAO/MEC`, matching the SPHERE/<sub>
  convention (frontend parent-prefix filtering handles it generically). His papers:
  HD 169142 (Lucas+2025 AJ) Fig. 3 2×4 gallery → 7 per-instrument records incl. the
  atlas' first VAMPIRES record; VAMPIRES instrument paper (Lucas+2024 PASP) → NEW
  SYSTEM R Aqr (evolved; Hα jet+nebula); AB Aur Dykes+2024 Fig. 2 → J/H/K split
  (replaced JHK composite; paper has TWO caption typos: band order and "January"
  epoch — trust panel labels: 2020-10-04); HD 34700 Chen+2024 Fig. 3 middle column
  → Qphi J/H/K. Mullin+2026 & HD 1160 stamps reviewed (already in / not atlas-grade).
- Worklist CLOSED OUT 2026-07-09 (all four items resolved):
  (1) "T Tau Keck (Bally+2000)" = COLLISION — ADS stems abs:"T Tau" to match
  "T Tauri", so EVERY t-tau audit flag was about other Taurus objects; Bally 2000
  is Orion proplyds. Lesson recorded in the target-side-completeness-audit memory.
  (2) Vega NICMOS/Keck flags = "Vega-like" phrase collisions — coverage verified
  complete. (3) DISCS SMA (Öberg+2011): ingested 267 GHz continuum for IM Lup +
  HD 142527 (MY Lup flag = false positive, not in the sample). BONUS from the same
  worklist row: Looney+2000 BIMA 2.7 mm panel-(d) maps ingested for DG Tau,
  DG Tau B, L1551 IRS5, HL Tau, GG Tau, GM Aur (new BIMA facility for all six).
  (4) Morales+2013: title lists the full sample (HD 70313/71722/159492/104860) —
  all four already in the atlas; nothing left. (Fukagawa+2010: user-checked,
  dropped. Padgett+1999: done, 5 panels + 3 new systems.)
- FINAL burn-down of the remaining top-of-list flags (2026-07-09, list now clean):
  GQ Lup NACO discovery + AU Mic Keck (Liu 2004) = already in atlas (flags were
  im-lup/beta-pic name collisions). NGC 1068 VLA = REAL gap → ingested Gallimore
  1996 Fig. 2 VLA-A 6 cm jet map (ADS scan, no arXiv; skipped the 18 cm Fig. 1 —
  inset-collage too tangled to crop cleanly). Verified non-imaging and skipped:
  DG Tau STIS (jet spectroscopy), Keck-Interferometer/PTI visibilities (dg-tau,
  mwc-297), NIR spectral library (ct-cha/dh-tau/et-cha), [Ne II] spectroscopy
  (cs-cha/hd-34700), PDS 70 GRAVITY astrometry (no image figure), Natta 2004 VLA
  Herbig 'search' (photometry), as-218/et-cha ALMA sample-statistics flags.

## Session state 2026-07-08 (previous log)

WHAT THIS SESSION DID (all committed + pushed to master):
- **Snowball deepening then saturation.** Added the BACKWARD reference axis to
  `find_papers.py` (`--direction both`, `cache_refs/`, `--min-year 1995`) so non-arXiv
  classics (Grady 2005, Perrin 2009, Schneider/Augereau…) surface, not just forward
  citations. Ran many PF/discovery batches → grew from ~405 to 462 systems (post-AGB
  "evolved" disks, AGB/RSG, massive-YSO, edge-on protostellar, quasar-host, plus classic
  HST/NICMOS/STIS/ACS coronagraphy). Hit genuine SATURATION: last keyword sweep was
  ~2 hits / 700 candidates. **The user's directed "add paper X, crop figure Y" requests
  are far higher-yield than the autonomous dragnet** — treat the snowball as a *targeted*
  tool now, not a background crawl.
- **Multi-panel figure splitting (big theme; see the `split-multipanel-figures` memory).**
  Source figures that show one target at several wavelengths were often ingested as ONE
  crop → mis-sorted (a Ks+L' strip hidden at 3.8 µm). Split ~26 records → ~74 per-band
  records across fleets + individual asks (3C 273 Komugi 3 ALMA bands, PDS 201 Wagner LBTI
  Ks/L'/vAPP, HD 135344B Stolker R/I/Y/J, HL Tau Mullin NIRCam 2×2, CY Tau Perez mm strip,
  ESO Hα 569 Wolff F606W, HD 15115 CHARIS J/H/K, HIP 65426 JWST 6-band, etc.). RULE:
  re-crop each band FROM SOURCE (don't slice the low-res combined image); one record per
  band; DON'T split RGB composites / wavelength ranges / same-band roll angles / multi-epoch
  galleries / "B/C"=companion-letter panels. Splitting also caught facility mislabels
  (CY Tau "VLA" was really CARMA at 1.3/2.8 mm).
- **New local QA tooling (runs on the DGX, token-free — use these before eyeballing):**
  `backend/crop_qa.py` (edge-uniformity / colorbar-bleed / gutter / MULTIPANEL / `--ocr`
  axis-text; report → `data/paper_finder/crop_qa.json`), `backend/dup_check.py` (md5
  exact-dup reliable; `--near` GPU pHash is noisy for faint crops), `backend/audit_bibcodes.py`
  (arxiv→ADS bibcode audit, `--fix`). GPU note: at ~1.4k small crops there is NO useful
  GPU speedup (I/O-bound); the real bottleneck is token-judgement + source-PDF fetches.
- **Bibcode/metadata audit** (`audit_bibcodes.py`): fixed 14 hallucinated/wrong bibcodes
  + 4 mislabeled first-authors (AR Pup Kluska→Ertel, Orion Src I Chen→Wright, HH 212
  Lin→Lee, BD+45 598 Farkas→Vincent), re-derived 29 journal strings. Anonymous ADS via
  `ui.adsabs.harvard.edu/v1/accounts/bootstrap` (no token). Keep bibcodes ADS-correct;
  resolve `bibcode:null` records opportunistically.
- **`evolved` category added** (backend `validate.py` CATS + frontend chip/legend/hexagon
  marker; 21 systems: post-AGB + AGB). **SPHERE instrument facet split** into
  `SPHERE/IRDIS` · `SPHERE/ZIMPOL` · `SPHERE/IFS` (`facility_map.instr_key`); the frontend
  INSTRUMENT facet does parent⊇children (clicking "SPHERE" matches all three).

NEXT / OPEN: snowball is at diminishing returns — prefer user-directed adds. `crop_qa.py`
GUTTER_EDGE (167) is mostly benign (edge-on disks have dark-sky edges) — screening only;
its MULTIPANEL flags are the actionable ones. Morales 2013 has 3 more Herschel belts if
wanted (HD 70313/71722/159492 already added; sample was 4). A local ML QA-classifier (fine-tune
on the GB10 to replace token-costly crop eyeballing) was proposed but not built.
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
  **`python3 backend/crop_qa.py [--ocr]`** automates this over every crop (report →
  `data/paper_finder/crop_qa.json`); its MULTIPANEL flag reliably finds un-split
  multi-band strips (the highest-value category — GUTTER/edge flags are noisier).
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
- **Multi-language** (`frontend/i18n.js`): 12 languages (en/zh/fr/es/de/it/ja/pt/ru/ko/hi/ar,
  ar is RTL), persisted in localStorage. UI strings route through `t(key)` / `data-i18n`;
  scientific data stays as-is. NEW `cat_evolved` key = the evolved category.
- **Facets**: band / missing-modality / **Facility** (AAS facility keywords via
  `backend/facility_map.py` incl. `Gemini:South`=Gemini S, `Gemini:Gillett`=Gemini N;
  applied at build time as `fac_keys`; A+B images appear under both; VLT selection also
  matches VLTI) / **Instrument** (`instr_key` families). SPHERE is split into
  `SPHERE/IRDIS`·`SPHERE/ZIMPOL`·`SPHERE/IFS`; selecting a parent instrument matches its
  children (parent⊇children).
- **Light/dark theme** toggle (`body.light`, persisted; `refreshCOL()` re-reads CSS vars,
  canvas sky uses `--sky`). **Tonight** rows link to per-object airmass.org charts
  (obsid map in SITES). Notes auto-linkify "Author+Year" to SciX searches;
  `planets[].extra_papers` render as extra arXiv/SciX links. Systems with `simbad: null`
  get a SIMBAD coordinate-search link instead of an Ident link.
- **Markers**: distinct SHAPE per category (● proto / ▲ debris / ◆ planet-only / ■ quasar /
  ⬢ evolved, colorblind + B/W-print friendly), a **★ star** overlay marks imaged-planet
  hosts, and a white circle marks selection. Marker size is uniform per type (image count
  only sets fill opacity). Sky Dec axis is bounded to −90…+90 via `view.topInset`.
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
