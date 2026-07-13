# Contributing to `diskatlas` / 欢迎共建

Contributions are very welcome — **new systems, missing instruments/epochs for existing
systems, coordinate or citation fixes, new UI languages, frontend improvements** — from
humans working by hand *or* from an AI agent you drive on your own machine. Most of this
atlas was built by AI agents (Claude Code) supervised by an astronomer, and the repo is
designed so anyone can continue it the same way.

Open a **pull request**; the maintainer reviews each one. To suggest a paper or target
without doing the work, just [open an issue](https://github.com/seawander/diskatlas/issues).

## Two hard rules (every PR)

1. `python3 backend-data/validate.py` must report **0 errors / 0 warnings**.
2. **Never hand-edit `frontend/data.js`** — it is GENERATED; run `python3 backend-data/build.py`.

The full quality bar is the five hard rules in [`AGENTS.md`](AGENTS.md) (VIEW every crop,
verify arXiv ids from the source, record the observation epoch, panel-only crops from the
authors' arXiv source figures, one record per band). The PR template restates them as a
checklist.

## Prerequisites

- **Python 3** (plus Pillow for cropping). No Node, no build system — the app is vanilla.
- **Live internet from the shell** is required for ingestion work: arXiv, SIMBAD, ADS and
  the observatory archives are what you parse (test: `curl -sI https://arxiv.org`). The
  maintainer's reference platform is an NVIDIA DGX Spark, but any platform with Python 3
  and connectivity works.

## Contribute with your own AI agent (recommended)

1. **Fork & clone**, then open the repo in your agent/harness. Claude Code auto-loads
   `CLAUDE.md`; OpenCode / Cursor / Codex / Aider auto-load [`AGENTS.md`](AGENTS.md) — so
   your agent is oriented the moment it opens the repo, no copy-paste needed.
2. **Give it a one-line task** (paste arXiv links, name a figure, or ask for a sweep):

```text
You are working in a clone of "diskatlas" — a mature, offline, double-click-index.html
all-sky atlas of resolved circumstellar disks (protoplanetary, debris, edge-on, embedded,
eruptive, proplyds, far-IR-resolved), directly imaged planets/BD companions, and
coronagraphic quasar hosts. `python3 backend-data/build.py` prints the live statistics.

FIRST, orient yourself (token discipline — do NOT read everything): read AGENTS.md (or
CLAUDE.md) for the rules + task→doc routing, then read ONLY the one doc your task needs
(records/crops → HANDOFF.md; schema → data/README.md; UI → frontend/README.md). Never load
data/paper_finder/candidates.md, frontend/data.js, or docs/HISTORY.md (grep the latter).
Run `python3 backend-data/validate.py && python3 backend-data/build.py`; confirm 0 errors.

STANDING RULES: verify every paper's arXiv id + figure FROM THE SOURCE, never from memory;
never use press-release images — every image is cropped from a peer-reviewed figure,
PANEL-ONLY (axes/margins trimmed), and you must VIEW every crop before and after saving;
record the OBSERVATION epoch; keep validate.py at 0 errors; never hand-edit
frontend/data.js; update data/ingestion_status.json (batch ledger) and
data/paper_finder_state.json (per-paper dispositions) after any change.

MY TASK: <paste arXiv links / bibcodes to ingest, or "run the weekly maintenance"
(python3 backend-data/fresh_papers.py digest -> VIEW figures -> ingest or exclude), or
"audit system X" (backend-data/system_audit.py), or a frontend request — or leave blank
for a status report>
```

3. **Let it run the workflow below**, confirm `validate.py` is at 0 errors, then have it
   open a PR (`gh pr create`) and fill in the checklist.

The complete agent handbook is [`HANDOFF.md`](HANDOFF.md). The literature-crawling Skill
ships in `.claude/skills/diskatlas-paper-finder/` (also packaged as
`diskatlas-paper-finder.skill`), so "find new papers for the atlas" works out of the box
in Claude Code.

## Full update workflow (new paper / new discovery)

1. **Add records** — either append the system/paper in `backend-data/seeds/` (survey-style,
   batch) and run `python3 backend-data/make_systems.py`, **or** directly edit/create
   `data/systems/<id>.json` (single target). Schema: `data/README.md`.
2. **Coordinates** — new systems need RA/Dec. `gen_fetch_script.py` adds every system with
   `ra_deg: null` to the SIMBAD query, so `bash fetch_sources.sh` + `parse_simbad.py` fills
   `data/coords_cache.json`. Systems created directly as JSON (not via seeds) must then have
   their coords copied from `coords_cache.json` into the JSON (`make_systems.py` only
   auto-applies coords to seed systems). For HSC/2MASS-designated objects, parse RA/Dec
   straight from the name if SIMBAD misses it.
3. **Figures** — `python3 backend-data/gen_fetch_script.py` regenerates
   `backend-data/fetch_sources.sh`, then `cd backend-data && bash fetch_sources.sh`
   downloads the arXiv tarballs + `fetch_extra.txt` PDFs into `images/_sources/`. Then
   `python3 extract_sources.py`.
4. **Crop panels** — either a manifest (`python3 backend-data/crop_panels.py
   manifests/<name>.json`) or, for one-off / existing records, crop directly with Pillow to
   `images/<sid>/<image_id>.png` and stage `{system_id, image_id, file, credit}`. For
   batches use the crop-agent pattern (see `HANDOFF.md`). **VIEW every crop.**
5. **Merge & build** — `python3 backend-data/merge_staging.py && python3
   backend-data/validate.py && python3 backend-data/build.py`.
6. Open `index.html`, verify, update `data/ingestion_status.json`, and open your PR.

### Quick rebuild (after any data edit)

```bash
python3 backend-data/build.py    # data/systems/*.json → frontend/data.js (+ checks)
```

### Fetch sources + rebuild (from scratch)

```bash
cd backend-data
bash fetch_sources.sh            # arXiv tarballs + fetch_extra.txt PDFs + SIMBAD coords
python3 parse_simbad.py && python3 extract_sources.py \
  && python3 make_systems.py && python3 validate.py && python3 build.py
```

## Finding new papers

- **Ongoing (weekly):** `python3 backend-data/fresh_papers.py` sweeps the last 14 days of
  astro-ph.EP/SR (anonymous ADS API) and digests papers that mention an atlas target or
  look like a new resolved-imaging result. Review each hit by **viewing the figure**
  (metadata is not enough), then ingest it or record an `excluded` entry in
  `data/paper_finder_state.json` keyed by arXiv id. `backend-data/README.md` documents the
  full maintenance toolset (`audit_bibcodes.py --fix --fill`, `crop_qa.py`,
  `system_audit.py`).
- **Retrospective (saturated; targeted questions only):**
  `.claude/skills/diskatlas-paper-finder/` snowballs the citation graph outward from every
  paper already in the atlas (`scripts/find_papers.py` bulk-harvests forward citations).

**Three ledgers, no overlap:** `data/systems/*.json` = ground truth (papers in the atlas);
`data/paper_finder_state.json` = per-paper dispositions for papers **not** in the atlas
(the dedupe ledger); `data/ingestion_status.json` = human-readable per-batch session log.

## Scope (what belongs in the atlas)

See the [Scope section in the README](README.md#scope--收录标准). In short: **spatially
resolved** disks (≥ a few beams/PSFs) — protoplanetary and debris — plus directly imaged
planets/brown-dwarf companions and coronagraphic quasar hosts. Marginally-resolved
single-beam detections, unresolved excesses, and press-release composites are **excluded**;
every image is a panel cropped from a peer-reviewed figure and linked to its paper.

## Licensing your contribution

Code is MIT, the compiled database is CC BY 4.0, and image crops stay © their original
authors/journals (reproduced for scholarly reference). By contributing you agree your work
is offered under those same terms. Only add image crops made from the **authors' own arXiv
source figures**, each with a `credit` line and citation links. See
[README §License](README.md#license--许可) and [LICENSE-DATA.md](LICENSE-DATA.md).
