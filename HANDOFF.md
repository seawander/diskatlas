# HANDOFF — how to work on diskatlas

Entry point for agents is `CLAUDE.md` (auto-loaded, has the task→doc routing).
Read THIS file when you need the full working method. Session-by-session
narrative lives in `docs/HISTORY.md` — **grep it, never load it whole**.

## What this project is

An offline, double-click `index.html` all-sky atlas of every system with a
**spatially resolved circumstellar disk** (mm/submm interferometry +
high-contrast scattered light / thermal-IR), a **directly imaged
exoplanet/companion**, or a **coronagraphically imaged quasar/AGN host**. Every
image is a low-res crop of a peer-reviewed figure (or official archive preview)
with clickable **arXiv + SciX** citations. Pure static files — no server, no
runtime build.

## Current state (2026-07-11)

- **484 systems · 1815 image records (all with local panels) · validate.py
  0 errors / 0 warnings · all bibcodes ADS-verified · epoch coverage 94.3%**
  (`python3 backend-data/build.py` is always canonical for stats).
- Live at **github.com/seawander/diskatlas** + GitHub Pages. Publish = **direct
  push to `master`** (no PRs, `gh` not installed). Multiple sessions commit
  concurrently — `git fetch` before assuming ahead/behind.

## MAINTENANCE MODE — the ongoing rhythm

Retrospective discovery is DONE (snowball saturated, audit worklists burned
down). Now:

1. **Weekly**: `python3 backend-data/fresh_papers.py` → review digest → VIEW each
   figure (metadata lies) → ingest, or add an arXiv-keyed `excluded` entry to
   `data/paper_finder_state.json`.
2. **After any batch**: `audit_bibcodes.py --fix --fill`, then `crop_qa.py`
   (act on MULTIPANEL flags). Keep validate at 0/0.
   - `panel_audit.py` is the caption-based completeness sweep (complements
     crop_qa's pixel-based one): it reads each record's `Fig. N` credit, pulls
     that figure's caption from the arXiv `.tex`, estimates panel count, and
     flags figures where the atlas holds fewer records than the caption
     describes. Tags each flag `multiband` (≥2 distinct wavelength tokens =
     process FIRST, real missed images), `variant` (Uphi/r²/model/weighting =
     display-only, usually skip), or `review` (band names its regex can't
     tokenize — R'/I', mid-IR filters — genuine misses hide here too). ALWAYS
     VIEW before ingesting: the 2026-07-10 run's recurring false positives were
     re-imaged archival data already held from the original paper (PDS 70 B7 =
     Benisty21; AS 205 1.3mm = DSHARP), display variants, marginal/noise
     detections, and unresolved continuum insets.
3. **User-directed requests** ("add paper X, crop figure Y") outrank everything.
4. On demand: `system_audit.py --systems <ids>` for per-target completeness
   (good for HD/HR/IRAS names; short names like "T Tau" collide in ADS).
5. **Quarterly (or when a name recurs in requests)**: `author_audit.py` — the
   THIRD discovery axis (first-author ADS sweep). The citation snowball and the
   14-day fresh_papers window both miss the 2015–2024 output of prolific
   in-atlas authors; the 2026-07-10 run flagged 301 candidates (triage queue:
   `data/paper_finder/author_audit_*.txt`). The maintainer's own surname and
   close collaborators (Ren, Xie, Olofsson, Milli, Benisty, …) are hardcoded in
   the tool's EXTRA list — sweep them FIRST.

**Ingestion-time completeness rules** (each learned from a user correction —
doing it right the first time is the cheapest recall fix):
- Ingest **every qualifying panel** of a figure the first time (one record per
  band/epoch/reduction); "Fig. 1a-b" in a credit line is a split violation.
- **Cross-paper redundancy is WANTED, not deduped**: the same target/band shown
  in a *different* paper's figure is a separate record — including when paper B
  merely re-displays/re-frames paper A's product (the atlas documents reduction
  diversity across teams; never skip on "we already have a better one"). Only
  reject *same-paper* true duplicates + non-images (SED/profile/model/residual/
  spectral-index) + non-detections + unresolved point sources. See the
  `cross-paper-redundancy-ok` auto-memory.
- Multi-epoch figures (pattern-motion papers): **every epoch is a record**.
- Multi-reduction panels of ONE dataset get separate records (PDI/ADI/RDI in
  `technique`) — unless annotations straddle the panels (then one record + note).
- Non-detection panels are NOT records, whatever the user's panel list says —
  check the text ("cannot be recovered" ⇒ skip, cite the reason).
- When ingesting any paper, immediately check the SAME author's adjacent papers
  on the same target (the SAO 206462 motion paper had a 2021 predecessor).

## The three ledgers (do NOT create a fourth)

1. `data/systems/*.json` — ground truth; a paper is "in the atlas" iff cited here.
2. `data/paper_finder_state.json` — dispositions for papers NOT in the atlas
   (`excluded`/`ingested` + reason). The dedupe ledger.
3. `data/ingestion_status.json` — per-survey status + short current-state line.
   Longer narratives go to `docs/HISTORY.md`, ONE dated paragraph per session.

`data/paper_finder/` is regenerable Skill working state (safe to delete,
expensive to refetch). `candidates.md` there is ~330k tokens — never read it.

## Observation epochs (`epoch` field)

`epoch` = the date the data were **taken**, never the publication year.
Coverage 94.3% (2026-07-11 audit); the remaining 104 records are papers that
state no dates AND archives are silent. Method + numbers for the manuscript:
`paper_Overleaf/notes_epoch_methods.md`. Provenance per record:
`data/paper_finder/epoch_provenance.json`. Audit: `backend-data/epoch_audit.py`.

- Precision policy: `YYYY-MM-DD` if executions cluster ≤~45 d; `YYYY` if one
  calendar year; `YYYY-YYYY` if the image combines years.
- Tools: `epoch_harvest.py` (tex extraction; BLOCKLIST pins rejected
  candidates), `epoch_archives.py` (MAST/ESO/ALMA/HSA, bounded by paper date),
  `fetch_sources.py` (arXiv source packages).
- **RULE: every NEW record carries `epoch` at ingestion** — read the observing
  log while the source is open. Beware: dates near a different instrument,
  calibration/reference stars, RV/photometry, or received/accepted lines are
  poison; instrument-impossible years (Herschel>2013, ACS/HRC>2007-01) are the
  cheapest sanity check.

## Quick start

```bash
python3 backend-data/validate.py && python3 backend-data/build.py   # 0 errors + stats
```
Then read `data/ingestion_status.json` (`pending_actions`, `known_missing`,
per-survey `notes`).

## Environment

- **Reference platform**: the maintainer runs this on an NVIDIA DGX Spark
  (128 GB RAM, GB10 GPU) — but nothing is platform-specific; any Linux/macOS
  box with Python 3 works. Prefer local compute over token spend everywhere.
- **Live internet from the shell is REQUIRED** — arxiv.org, SIMBAD, ADS, and
  the observatory archives (MAST/ESO/ALMA TAP) are what the agents parse;
  without connectivity the source-verification and epoch/coordinate work
  cannot be done. Verify before starting: `curl -sI https://arxiv.org`.
  (At most, `fetch_sources.sh` can be run on a different networked host and
  `images/_sources/` copied over — but archive/ADS/SIMBAD queries still need
  the working session online, so treat internet as a hard prerequisite.)
- Typical tooling (check availability before relying on it): `pdftoppm`,
  `pdfinfo`, ImageMagick, ghostscript, Python+Pillow, astroquery. The frontend
  needs no Node — verify via `python3 -m http.server`.
- **Paywalls**: IOP/AAS PDFs via curl → 14367-byte captcha page. Best→worst ADS
  gateways for curl: `EPRINT_PDF` → `PUB_PDF` (A&A/AJ ok, IOP captcha) →
  `ADS_PDF` (scans). Captcha-locked → ask the user to browser-download to
  `images/_sources/extra/<name>.pdf` (give the exact filename).
- A failed download leaves a garbage file that blocks re-fetch — delete it
  first; PDFs <20 KB are almost always HTML.
- Anonymous ADS token: `ui.adsabs.harvard.edu/v1/accounts/bootstrap`.

## Pipeline (scripts in backend-data/)

```
seeds/*.py + new JSON → make_systems.py → data/systems/*.json
gen_fetch_script.py → fetch_sources.sh → images/_sources/… + simbad_raw.txt
parse_simbad.py → data/coords_cache.json
extract_sources.py → images/_sources/extracted/<id>/
crop → images/<sid>/<image_id>.png   (panel-only, ≤480 px, ≤300 KB)
merge_staging.py → validate.py → build.py → frontend/data.js
```

Gotchas (each has bitten):
- `make_systems.py` applies coords_cache ONLY to seed systems — direct-JSON
  systems need coords filled by script. Coordinate-encoding names (HSC J…)
  parse RA/Dec from the name; SIMBAD may not resolve them.
- Deleting a record: remove from system JSON AND its seed, else it resurrects.
- `image_id` = `<sysid>_<slug>`; survey members use the survey slug.
- Always confirm the paper's target matches the system (VIEW catches it).
- `merge_staging.py` updates existing image_ids in place (non-null fields win) —
  to fill a `file:null` record, stage just `{system_id,image_id,file,credit}`.
- `git mv a b/c.png` does NOT create `b/` — `mkdir -p` first.

## Ingesting via parallel agents (primary method for batches)

Two patterns: (1) research/verify sweep — one agent per paper cluster, verify
arXiv ids from source (never memory), return structured findings; (2) crop
workflow — one agent per figure: render, **VIEW with Read** (panel labels are
the only ground truth), crop, VIEW the saved crop, return
`{system_id,image_id,file,credit,ok}`. Orchestrator writes ONE staging file.

Fleet gotchas: hardcode file paths in prompts; export.arxiv.org 429s under
fleet load (`Rate exceeded` → a 14-byte "tarball"; back off, retry); parallel
curl truncates PDFs at 4 MiB, and **even a single sequential `curl` silently
caps arXiv e-print tarballs at exactly 2 MiB** (2097152 B) — use `wget -O` for
anything larger (Z CMa's source was 13 MB); check `pdfinfo`/tar-extract; agents
sometimes stop after spawning children (SendMessage: "do it synchronously,
reconcile disk first"); always reconcile results against disk; two agents can
create the same system — re-`ls data/systems/` before writes.

## Crop discipline (full protocol: backend-data/AGENT_BRIEFS.md)

Panel-only (trim axes/labels/margins; attached colorbars ok), ≤480 px longest
side, ≤300 KB (requantize with FASTOCTREE if over). VIEW every crop before
staging. Multi-wavelength source figures = one record per band, each re-cropped
FROM SOURCE — never slice the combined low-res image; don't split RGB
composites / same-band rolls / companion-letter panels. No press-release
composites, ever. If a paper is uv-plane-only (no image figure), drop it.
`crop_qa.py [--ocr]` automates edge/gutter/MULTIPANEL checks.

## Data conventions (schema: data/README.md)

- Quasars: `categories:["quasar"]`, `redshift` not `dist_pc`.
- Citations render arXiv + **SciX** (not NASA ADS).
- Transiting companions are never "imaged" (`method:"transit"`).
- `hires_url` for archive products (ALICE → archive.stsci.edu/prepds/alice/).
- Categories incl. `evolved` (post-AGB/AGB). Instrument families use
  parent/child (`SPHERE/IRDIS`, `SCExAO/CHARIS`) via `backend-data/facility_map.py`.

## Frontend

Vanilla JS, offline, file://-safe. `data.js` is GENERATED — never hand-edit.
Views: Sky map / Coverage matrix / Tonight planner; faceted by band, facility
(AAS keywords), instrument family; 12 languages; light/dark. Detail-card chips
show the **observation epoch** as a bare bold year (tooltip = full date or
"observations span YYYY-YYYY (combined data)"); publication year appears only
as an italic parenthesised fallback. Full UI map: `frontend/README.md`.

## User preferences

- Reply in **English**. Commit messages for review-driven fixes say "internal
  review fix" (never "referee"). Push only when the user says "gp".
- Comprehensiveness at **instrument/epoch level** is the goal — multi-epoch,
  historical (back to 1984), extragalactic.
- Verify paper metadata FROM THE SOURCE, not memory. Keep validate at 0/0 and
  refresh README + ledger stats after each batch.
- `paper_Overleaf/` is gitignored (Overleaf-bound); paper/source PDFs stay off
  GitHub.
