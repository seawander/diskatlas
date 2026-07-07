# Resolved Circumstellar Disks & Imaged Exoplanets — Interactive Sky Atlas
# 已分辨星周盘与直接成像系外行星 · 交互式全天图

An offline-capable, interactive all-sky atlas of every system with a **resolved circumstellar
disk** (mm/submm/cm interferometry, high-contrast scattered light / thermal IR, and resolved
far-IR single-dish imaging), a **directly imaged planet or substellar companion**, or a
**coronagraphically imaged quasar host**. Click any object on the sky map to browse its images
across instruments, wavelengths and epochs, with clickable arXiv / SciX citations for every image.

**双击根目录的 `index.html` 即可离线使用。**  Double-click `index.html` — no server, no internet needed.

---

## Folder layout / 目录结构

```
index.html          ← THE app. Open this. (loads frontend/ + images/)
frontend/           ← app.js, style.css, data.js (data.js is GENERATED — do not hand-edit)
data/               ← the database: one JSON per system + docs. THIS is what you edit.
backend/            ← Python scripts: seed → coordinates → crop → validate → build
images/             ← _sources/ (downloaded figures) + <system_id>/*.png (cropped panels)
```

Every folder has its own `README.md` with update instructions for humans **and** AI agents.

**Resuming in a new AI session?** Read `HANDOFF.md` (full project design, environment
quirks, lessons learned, pending work) and use the ready-made prompts in
`CONTINUATION_PROMPTS.md`.

## Quickstart: rebuild after any data change / 改动数据后重建

```bash
cd backend
python3 build.py          # data/systems/*.json → frontend/data.js (+ checks)
```

## Fetch sources + rebuild / 抓取源并重建

This DGX checkout has live internet, so run the whole fetch yourself (no host hand-off):

```bash
cd backend
bash fetch_sources.sh          # arXiv tarballs + fetch_extra.txt PDFs + SIMBAD coords
python3 parse_simbad.py && python3 extract_sources.py \
  && python3 make_systems.py && python3 validate.py && python3 build.py
```

(If ever run in a network-isolated sandbox, run `fetch_sources.sh` on a host with
internet instead — everything else is the same.)

## Current contents (2026-07-07 build) / 当前规模

**401 systems (incl. quasar hosts and Class 0/I eDisk protostars; Orion proplyds queued) ·
1181 image records · all with local panels · 65 imaged-companion hosts ·
coordinates for every system (SIMBAD idents coordinate-verified) · 0 validation errors.**
`python3 backend/build.py` prints the canonical live stats — trust its output over any number
written in prose. Major 2026-07-06/07 expansions: a full instrument-level sweep over every
system (44 parallel agents), the Tamura+2016 SEEDS Fig. 3 completion, Hom+2024 GPI total
intensity, Ren+2023 Ks Qphi completion, Xie+2022 RDI gallery, MAPS CO line maps, pre-ALMA
mm classics (SMA/PdBI/CARMA/OVRO/BIMA), far-IR resolved images (Herschel/Spitzer/JCMT/CSO —
scope extension), eDisk + AGE-PRO + SPHERE NIR census + σ Orionis survey batches, ~25
imaged-companion hosts recovered by citation chasing (PZ Tel B, VHS J1256 b, HD 33632 Ab,
HIP 21152 B, …), eruptive stars (Z CMa, V960 Mon, EX Lup), β Pic d, WISPIT 2 planets, and
external-catalog cross-checks (Wikipedia list + circumstellardisks.org).

**Frontend (2026-07-07):** three views — **Sky**, **Coverage matrix**, **Tonight**
(observability snapshot + per-target **airmass.org** night-chart links per site/date, CSV).
Faceted filters: wavelength band / missing modality / **Facility** (normalized to AAS
facility keywords; joint A+B images appear under both; selecting VLT also shows VLTI, not
vice versa) / **Instrument** (54 families, most-used first). **Light/dark theme toggle**
(persisted), **multi-language UI** (EN/中文/FR/ES), citation links to **SciX** + arXiv,
auto-linkified "Author+Year" citations in notes, SIMBAD link per system (coordinate-search
fallback for objects SIMBAD lacks). Crops are panel-only (axes/margins trimmed). Everything
offline (`file://`, no CDN).

## Finding new papers (the paper-finder Skill) / 自动找文献

`.claude/skills/diskatlas-paper-finder/` (also packaged as `diskatlas-paper-finder.skill`)
snowballs the literature outward from every paper already cited in the atlas — targets,
instruments, and the citation graph in both directions (SciX/arXiv; bundled script
`scripts/find_papers.py` bulk-harvests forward citations). **Bookkeeping — three ledgers,
no overlap:**

1. `data/systems/*.json` — ground truth: papers actually in the atlas (the finder treats
   every arXiv id cited here as done automatically).
2. `data/paper_finder_state.json` — per-paper dispositions for papers **not** in the atlas
   (`excluded` + reason, or `ingested` pointers). The skill's dedupe ledger.
3. `data/ingestion_status.json` — human-readable per-survey/batch session log. Not a
   per-paper dedupe source.

`data/paper_finder/` holds regenerable working files (candidates, citation cache).

## Full update workflow (new paper / new discovery) / 新论文入库全流程

1. **Add records** — either append the system/paper in `backend/seeds/` (survey-style, batch)
   and run `python3 backend/make_systems.py`, **or** directly edit/create
   `data/systems/<id>.json` (single target). Schema: `data/README.md`.
2. **Coordinates** — new systems need RA/Dec. `gen_fetch_script.py` adds every system
   with `ra_deg: null` to the SIMBAD query, so `bash fetch_sources.sh` + `parse_simbad.py`
   fills `data/coords_cache.json`. **Systems created directly as JSON (not via seeds) must
   then have their coords copied from `coords_cache.json` into the JSON by a small script**
   (`make_systems.py` only auto-applies coords to seed systems). For HSC/2MASS-designated
   objects, parse RA/Dec straight from the name if SIMBAD misses it.
3. **Figures** — `python3 backend/gen_fetch_script.py` regenerates `backend/fetch_sources.sh`,
   then `cd backend && bash fetch_sources.sh` (this checkout has internet) downloads the
   arXiv tarballs + `fetch_extra.txt` PDFs into `images/_sources/`. Then `extract_sources.py`.
4. **Crop panels** — either a manifest (`python3 backend/crop_panels.py manifests/<name>.json`)
   or, for one-off / already-existing records, crop directly with Pillow to
   `images/<sid>/<image_id>.png` and stage `{system_id, image_id, file, credit}`. For batches
   use the **Workflow tool crop-agent pattern** (see HANDOFF.md). VIEW every crop.
5. **Merge & build** — `python3 backend/merge_staging.py && python3 backend/validate.py && python3 backend/build.py`.
6. Open `index.html`, verify, update `data/ingestion_status.json` + these stats. Done.

## Scope / 收录标准

- **Disks**: spatially resolved (≥ a few beams / PSFs) circumstellar disks — protoplanetary
  (incl. transition, edge-on, eruptive-star and Class 0/I embedded) and debris — imaged by
  mm/submm/cm interferometers (ALMA, SMA, PdBI/NOEMA, VLA, CARMA, OVRO, BIMA, ATCA), in
  scattered light / thermal IR by high-contrast instruments (HST, JWST, GPI, SPHERE, Subaru
  HiCIAO/SCExAO, NACO, MagAO(-X), LBTI, …), by VLTI interferometric reconstruction, and in
  the resolved far-IR (Herschel/Spitzer/JCMT/CSO). Orion proplyd silhouettes included.
- **Companions**: directly imaged planets and brown-dwarf companions (status
  `confirmed`/`candidate`/`disputed`/`refuted` tracked per companion; a few borderline or
  later-refuted objects are kept for the historical record and flagged).
- **Quasar hosts**: coronagraphic / PSF-subtracted host-galaxy imaging (`redshift` instead
  of `dist_pc`).
- Resolved **far-IR/submm single-dish** images (Herschel PACS/SPIRE, Spitzer MIPS, JCMT,
  CSO) are in scope (2026-07-07 extension); marginally resolved single-beam detections and
  unresolved excesses remain **excluded**.
- Press-release composites are **not** used; every image is cropped from a peer-reviewed
  figure and linked to its paper (arXiv + SciX).

## Image licensing note / 图像版权说明

Local thumbnails are low-resolution crops of published figures, used here for personal
research/reference with full citation. © original authors & journals — follow the links
(arXiv / SciX / DOI) for originals and for any reuse.

## Current ingestion state / 数据现状

See `data/ingestion_status.json` (machine-readable) — per-survey status of catalog entries,
coordinates, image crops. Agents: update it whenever you ingest anything.
