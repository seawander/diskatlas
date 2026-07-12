<p align="center"><img src="frontend/logo.svg" alt="diskatlas logo" width="128"></p>

# `diskatlas`: all-sky interactive atlas for resolved circumstellar disks and imaged companions

`diskatlas`: 已分辨星周盘与直接成像伴体 · 交互式全天图

**🌐 Browse it live: <https://seawander.github.io/diskatlas/>** · 
[Source & data on GitHub](https://github.com/seawander/diskatlas) — or clone and
double-click `index.html` for the fully offline version.

An offline-capable, interactive all-sky atlas of every system with a **resolved circumstellar
disk** (mm/submm/cm interferometry, high-contrast scattered light / thermal IR, and resolved
far-IR single-dish imaging), a **directly imaged planet or substellar companion**, or a
**coronagraphically imaged quasar host**. Click any object on the sky map to browse its images
across instruments, wavelengths and epochs, with clickable arXiv / SciX citations for every image.

**双击根目录的 `index.html` 即可离线使用。**  Double-click `index.html` — no server, no internet needed.

Contributions are welcome — human or AI-agent-driven. See **[Contributing](#contributing--欢迎共建)** below.

---

## Folder layout / 目录结构

```
index.html          ← THE app. Open this. (loads frontend/ + images/)
frontend/           ← app.js, style.css, data.js (data.js is GENERATED — do not hand-edit)
data/               ← the database: one JSON per system + docs. THIS is what you edit.
backend-data/            ← Python scripts: seed → coordinates → crop → validate → build
images/             ← _sources/ (downloaded figures) + <system_id>/*.png (cropped panels)
```

Every folder has its own `README.md` with update instructions for humans **and** AI agents.

**Resuming in a new AI session?** `CLAUDE.md` auto-loads and routes you: ironclad
rules + a task→doc table so you only read what the task needs. Full method:
`HANDOFF.md` (~3k tokens). Session history: `grep docs/HISTORY.md` — never load it whole.

## Contributing / 欢迎共建

Contributions are very welcome: new systems, missing instruments/epochs for existing
systems, coordinate or citation fixes, new UI languages, frontend improvements. Open a
pull request. Two hard rules for any PR:

1. `python3 backend-data/validate.py` must report **0 errors**.
2. Never hand-edit `frontend/data.js` — it is generated; run `python3 backend-data/build.py`.

### Contributing with your own AI agent / 用你自己的 AI 智能体继续建设

Most of this atlas was built by AI agents (Claude Code) supervised by an astronomer, and
the repo is designed so anyone can continue it the same way. After cloning, paste this
into your agent (Claude Code, or any coding agent that can run Python and view images):

```text
You are working in a clone of "diskatlas" — a mature, offline, double-click-index.html
all-sky atlas of resolved circumstellar disks (protoplanetary, debris, edge-on, embedded,
eruptive, proplyds, far-IR-resolved), directly imaged planets/BD companions, and
coronagraphic quasar hosts. `python3 backend-data/build.py` prints the live statistics.

FIRST, orient yourself (token discipline — do NOT read everything):
1. CLAUDE.md auto-loads (rules + task→doc routing). Read ONLY the one doc your
   task needs (records/crops → HANDOFF.md; schema → data/README.md; UI →
   frontend/README.md). Never load data/paper_finder/candidates.md,
   frontend/data.js, or docs/HISTORY.md (grep the latter).
2. Run `python3 backend-data/validate.py && python3 backend-data/build.py`; confirm 0 errors.

STANDING RULES: verify every paper's arXiv id + figure FROM THE SOURCE, never from
memory; never use press-release images — every image is cropped from a peer-reviewed
figure, PANEL-ONLY (axes/margins trimmed), and you must VIEW every crop before and after
saving; keep validate.py at 0 errors; never hand-edit frontend/data.js; update
data/ingestion_status.json (batch ledger) and data/paper_finder_state.json (per-paper
dispositions) after any change.

MY TASK: <paste arXiv links / bibcodes to ingest, or "run the weekly maintenance"
(python3 backend-data/fresh_papers.py digest -> VIEW figures -> ingest or exclude), or
"audit system X" (backend-data/system_audit.py), or a frontend request — or leave blank
for a status report>
```

The complete agent handbook is `HANDOFF.md`. The
literature-crawling Skill ships with the repo in `.claude/skills/diskatlas-paper-finder/`
(also packaged as `diskatlas-paper-finder.skill`), so "find new papers for the atlas" works
out of the box in Claude Code. When contributing images, respect the licensing note below:
crops are panel-only excerpts of published figures with a mandatory `credit` line and
citation links in the record.

## Quickstart: rebuild after any data change / 改动数据后重建

```bash
cd backend-data
python3 build.py          # data/systems/*.json → frontend/data.js (+ checks)
```

## Fetch sources + rebuild / 抓取源并重建

**Live internet from the shell is required** for contribution work — arXiv, SIMBAD, ADS
and the observatory archives are what the agents parse (test: `curl -sI https://arxiv.org`).
The maintainer's reference platform is an NVIDIA DGX Spark, but any platform with Python 3
and connectivity works. Then run the whole fetch yourself:

```bash
cd backend-data
bash fetch_sources.sh          # arXiv tarballs + fetch_extra.txt PDFs + SIMBAD coords
python3 parse_simbad.py && python3 extract_sources.py \
  && python3 make_systems.py && python3 validate.py && python3 build.py
```

(A network-isolated sandbox can at most receive `images/_sources/` fetched on another
host — but SIMBAD/ADS/archive queries still need the working session online, so treat
internet as a hard prerequisite for contributing.)

## Current contents (2026-07-11 build) / 当前规模

**520 systems (incl. quasar hosts, embedded Class 0/I protostars, Orion proplyds and
evolved-star envelopes) · 2082 image records · all with local panels · 87 imaged-companion
hosts · coordinates for every system (SIMBAD idents coordinate-verified) · 0 validation
errors / 0 warnings · every paper block carries an ADS-verified bibcode · ~83% of records
carry the observation epoch (never the publication year), each with machine-readable
provenance (the rest are recent additions still being back-filled).**
`python3 backend-data/build.py` prints the canonical live stats — trust its output over any number
written in prose. Recent 2026-07-11 additions: the Vioque 2026 transition-disk gallery
(+15 new systems, crossing 500 systems) and the Kurtovic 2026 154-ring ALMA gallery, a
notes-citation sweep (58 systems now cite their claims in-line), historical β Pic
coronagraphy (Heap 2000 STIS, Apai 2015 two-epoch), plus a deep Orion silhouette/proplyd dive
(giant disk 114-426 in JWST/NIRCam 12-band, the ground-based-AO silhouette 218-354,
Ricci 2008 ACS proplyds, McCaughrean 1998 HST classics), V883 Ori (landmark FUor
water-snow-line disk, +5 ALMA bands), PDS 70 (+SPHERE) and the BHR 71 IRS1 JWST jet, a
Herschel PACS debris-ring sweep (β Pic, HR 8799, AU Mic, Vega, η Crv …), the SONS
JCMT/SCUBA-2 survey (new observatory), and systematic wavelength / epoch / multi-panel
audit burn-downs that read every figure of every atlas paper for missed bands and
companions. Earlier 2026-07-06/07 expansions: a full instrument-level sweep over every
system (44 parallel agents), Tamura+2016 SEEDS Fig. 3, Hom+2024 GPI total intensity,
Ren+2023 Ks Qphi, Xie+2022 RDI gallery, MAPS CO line maps, pre-ALMA mm classics
(SMA/PdBI/CARMA/OVRO/BIMA), far-IR resolved images (Herschel/Spitzer/JCMT/CSO), eDisk +
AGE-PRO + SPHERE NIR census + σ Orionis batches, ~25 imaged-companion hosts recovered by
citation chasing (PZ Tel B, VHS J1256 b, HD 33632 Ab, HIP 21152 B, …), eruptive stars
(Z CMa, V960 Mon, EX Lup), β Pic d, WISPIT 2 planets, and external-catalog cross-checks
(Wikipedia list + circumstellardisks.org).

**Frontend (2026-07-09):** three views — **Sky**, **Coverage matrix**, **Tonight**
(observability snapshot + per-target **airmass.org** night-chart links per site/date, CSV).
Faceted filters: wavelength band / missing modality / **Facility** (AAS facility keywords;
joint A+B images appear under both; VLT⊃VLTI) / **Instrument** (families, parent⊇children
so `SPHERE`⊇`SPHERE/IRDIS` etc.), with facility↔instrument relationship highlighting.
**Light/dark theme toggle** (persisted), **multi-language UI — 12 languages**
(EN/中文/FR/ES/DE/IT/日本語/PT/RU/한국어/हिन्दी/العربية, incl. **right-to-left Arabic** and
translated constellation names). Citation links to **SciX** + arXiv, auto-linkified
"Author+Year" notes that resolve to the real abstract when the paper is recorded, SIMBAD
link per system. **Mobile-ready**: touch pan / pinch-zoom / double-tap on the sky map,
facets collapsed by default, keyboard-navigable search. Directly imaged objects are labelled
**"companions"** (not "planets"). Crops are panel-only; everything offline (`file://`, no
CDN). See `frontend/README.md` for the full feature map and conventions.

## Finding new papers / 自动找文献

**Ongoing (weekly):** `python3 backend-data/fresh_papers.py` sweeps the last 14 days of
astro-ph.EP/SR (via the anonymous ADS API) and digests papers that mention an atlas
target or look like a new resolved-imaging result. Review each hit by **viewing the
figure** (metadata is not enough), then ingest it or record an `excluded` entry in
`data/paper_finder_state.json` keyed by arXiv id. `backend-data/README.md` documents the full
maintenance toolset (`audit_bibcodes.py --fix --fill`, `crop_qa.py`, `system_audit.py`).

**Retrospective (saturated as of 2026-07-09; use for targeted questions only):**
`.claude/skills/diskatlas-paper-finder/` (also packaged as `diskatlas-paper-finder.skill`)
snowballs the literature outward from every paper already cited in the atlas — targets,
instruments, and the citation graph in both directions (SciX/arXiv; bundled script
`scripts/find_papers.py` bulk-harvests forward citations). **Bookkeeping — three ledgers,
no overlap:**

1. `data/systems/*.json` — ground truth: papers actually in the atlas (the finder treats
   every arXiv id cited here as done automatically).
2. `data/paper_finder_state.json` — per-paper dispositions for papers **not** in the atlas
   (`excluded` + reason, or `ingested` pointers). The dedupe ledger for both the skill
   (Semantic-Scholar-hash keys) and `fresh_papers.py` (arXiv-id keys — same flat dict).
3. `data/ingestion_status.json` — human-readable per-survey/batch session log. Not a
   per-paper dedupe source.

`data/paper_finder/` holds regenerable working files (candidates, citation cache).

## Full update workflow (new paper / new discovery) / 新论文入库全流程

1. **Add records** — either append the system/paper in `backend-data/seeds/` (survey-style, batch)
   and run `python3 backend-data/make_systems.py`, **or** directly edit/create
   `data/systems/<id>.json` (single target). Schema: `data/README.md`.
2. **Coordinates** — new systems need RA/Dec. `gen_fetch_script.py` adds every system
   with `ra_deg: null` to the SIMBAD query, so `bash fetch_sources.sh` + `parse_simbad.py`
   fills `data/coords_cache.json`. **Systems created directly as JSON (not via seeds) must
   then have their coords copied from `coords_cache.json` into the JSON by a small script**
   (`make_systems.py` only auto-applies coords to seed systems). For HSC/2MASS-designated
   objects, parse RA/Dec straight from the name if SIMBAD misses it.
3. **Figures** — `python3 backend-data/gen_fetch_script.py` regenerates `backend-data/fetch_sources.sh`,
   then `cd backend-data && bash fetch_sources.sh` (this checkout has internet) downloads the
   arXiv tarballs + `fetch_extra.txt` PDFs into `images/_sources/`. Then `extract_sources.py`.
4. **Crop panels** — either a manifest (`python3 backend-data/crop_panels.py manifests/<name>.json`)
   or, for one-off / already-existing records, crop directly with Pillow to
   `images/<sid>/<image_id>.png` and stage `{system_id, image_id, file, credit}`. For batches
   use the **Workflow tool crop-agent pattern** (see HANDOFF.md). VIEW every crop.
5. **Merge & build** — `python3 backend-data/merge_staging.py && python3 backend-data/validate.py && python3 backend-data/build.py`.
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

## License / 许可

Three parts, three answers:

- **Code** (`index.html`, `frontend/` JS+CSS, `backend-data/` Python): **MIT** — see
  [LICENSE](LICENSE).
- **Compiled database** (`data/systems/*.json`, the metadata in generated
  `frontend/data.js`): **CC BY 4.0** — see [LICENSE-DATA.md](LICENSE-DATA.md). Cite this
  repository (and the accompanying paper, once published) when reusing.
- **Images** (`images/**/*.png`): **not** covered by either license. They are
  low-resolution crops of figures from peer-reviewed papers — cropped from the
  **authors' own arXiv source files** (preprint figures), not from the journal-typeset
  articles. Rights remain **© the original authors** (and the journals for the published
  versions — AAS, A&A, MNRAS, …); each crop is reproduced here with a per-image credit
  line and full citation for scholarly reference. Follow each record's links
  (arXiv / SciX / DOI) for the originals and for any reuse permissions.

## Disclaimer & fair-use statement / 免责声明与合理使用

`diskatlas` is a **non-commercial, not-for-profit** resource created solely for scientific
research and education. The image excerpts are small, reduced-resolution crops taken from
the **authors' own arXiv source files** (preprint figures) — not from the journals'
typeset versions of record — to help researchers **locate and navigate the primary
literature**. Every excerpt carries a credit line and links back to the original paper
(arXiv / SciX / DOI), and is not a substitute for the published article. We believe this
constitutes fair use (17 U.S.C. § 107) / fair dealing for purposes of research and
scholarship.

We have **no intention to infringe any copyright**. All rights in the original figures
remain with their authors (and, for the versions of record, their publishers). If you are
a rights holder and would prefer that a particular image not appear here, please
[open an issue](https://github.com/seawander/diskatlas/issues) and it will be removed
promptly.

## Current ingestion state / 数据现状

See `data/ingestion_status.json` (machine-readable) — per-survey status of catalog entries,
coordinates, image crops. Agents: update it whenever you ingest anything.
