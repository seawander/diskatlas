# Batch T report — final crop batch (HD 100546 ACS / HSC z>6 quasar hosts / Bahcall quasar classics)

Date: 2026-07-06. Ran `extract_sources.py` first (unpacked 2211.14329 with 17 figure
files; both Bahcall astro-ph sources turned out to be dvips PostScript, 0 figure files
listed — see Job 3). All crops VIEWED individually; label↔file match confirmed for
all 7 panels; `trim_borders.py` run on all 7 (2 trimmed, rest had no uniform margins).
`merge_staging.py` + `validate.py` run at the end: **0 errors** (7 expected
"no coordinates" warnings for the new quasar systems, covered by
`data/coords_todo_batchT.txt`; the other 10 warnings are pre-existing >400 KB files
from earlier batches).

## Job 1 — hd-100546_acs2007 (Ardila+2007)
- Source: `images/_sources/extra/ardila2007_hd100546.pdf` (23 pp, ADS/EPRINT copy).
- Exact title verified from p.1: **"Hubble Space Telescope Advanced Camera for
  Surveys Coronagraphic Observations of the Dust Surrounding HD 100546"**,
  Ardila, Golimowski, Krist, Clampin, Ford & Illingworth, ApJ 665:512-534 (2007
  Aug 10) — journal/bibcode of the stub were already right; placeholder title
  fixed via staging (`_verify` flag cleared). arXiv id left null (not verifiable
  from the PDF itself).
- Best single panel: Fig. 1 (PDF p.5) **F606W** direct coronagraphic
  surface-brightness map (log stretch) — label, N/E compass, 6" bar and its
  colorbar all inside the crop. Chosen over the Fig. 3 deconvolved version and
  the Fig. 4 RGB composite (heavy PSF-mismatch radial streaks). Instrument
  refined to ACS/HRC (HRC named in §2 of the paper). 523x540 px.
- Manifest: `backend/manifests/batch-t/t-hd100546-acs2007.json`.

## Job 2 — HSC J2236+0032 & J2255-0251 JWST host detections (Ding+2023, 2211.14329)
- Fig. 2 rows verified by eye: fig2a = J2236+0032 F356W, fig2c = J2255+0251 F356W;
  cropped the third panel of each row ("data − point source" = the host-only
  detection). 551x551 px after trim. Manifests
  `t-hsc-j2236-jwst2023.json` / `t-hsc-j2255-jwst2023.json`.
- **Coordinate check (Extended Data Table 1)**: RA 22:36:44.58 +00:32:56.90 →
  339.18575/+0.549139 and RA 22:55:38.04 +02:51:26.60 → 343.9085/+2.857389 —
  IDENTICAL to the name-decoded values already in the two systems JSONs (table
  caption: HSC positions, "consistent with JWST's"). **No ra/dec changes needed.**
- **Redshift check**: table lists z=6.40 / 6.34 — matches stored values. More
  precise NIRSpec [OIII] systemic redshifts (6.4039±0.0009 / 6.333±0.001) recorded
  in each system's notes; J2255 host detected in F356W only (F150W > 26.3 mag).
- Record polish via staging: instrument narrowed from "NIRCam F150W/F356W" to
  "NIRCam F356W" (the band actually shown), label reworded, credit added.

## Job 3 — Bahcall quasar hosts (astro-ph/9409028, astro-ph/9501018)
Both "tex" sources are actually dvips **PostScript** files (bitmap Type-3 fonts, so
no text extraction; converted with ps2pdf and read/verified BY EYE page by page).

### Paper I = astro-ph/9409028 ("quasarpaper", 13 pp) — FIGURES PRESENT → CROPPED
- Verified: **"HST Images of Nearby Luminous Quasars"**, Bahcall, Kirhakos &
  Schneider. Journal **ApJ 435, L11** verified from Paper II's own reference list
  (p.38: "Bahcall, J. N., Kirhakos, S., & Schneider, D. P. 1994, ApJ, 435, L11");
  bibcode 1994ApJ...435L..11B.
- Contrary to expectation the source DOES embed Fig. 1: 2x2 grid of the four
  F606W WFPC2 (WFC camera) PSF-subtracted quasar images, clean 300-dpi bitmap.
  Cropped all four panels (labels inside panels confirmed):
  Table 1 (verified): PG 0953+414 z=0.239, PG 1116+215 z=0.177,
  PG 1202+281 (=GQ Com) z=0.165, PG 1307+085 z=0.155. Hosts NOT detected — these
  are the classic "naked quasar" upper-limit images; labels/notes say so.
- Manifest `t-bahcall-quasars-1994.json`, survey value "Bahcall-quasars-1994"
  (kept the seed-file capitalization used across the atlas; image_ids
  `<slug>_bahcall1994` as requested, set via per-member seed overrides so a future
  `make_systems.py` run matches instead of duplicating).

### Paper II = astro-ph/9501018 ("qpaper2", 43 pp) — NO FIGURES → pending path
- Verified: **"HST Images of Nearby Luminous Quasars II: Results for Eight Quasars
  and Tests of the Detection Sensitivity"**, Bahcall, Kirhakos & Schneider
  (submitted version; the published ApJ title probably spells out "Hubble Space
  Telescope"). Source contains figure CAPTIONS only (Figs. 1-9), no images.
- Journal **ApJ 450, 486** / bibcode **1995ApJ...450..486B** are from agent
  knowledge (the preprint has blank "Received/accepted"); the ADS gateway line
  below will fail loudly at fetch time if the bibcode is wrong — please confirm.
- Sample (Table 1, p.6, verified): the Paper-I four + **3C 273 z=0.158,
  PKS 1302-102 z=0.286, PG 1444+407 z=0.267, 3C 323.1 z=0.266**. Candidate host
  detections (abstract): PG 1116+215, 3C 273, PG 1444+407.
- Seed stub fixed with the four NEW quasars as members (the Paper-I four are not
  re-seeded under 1995 to avoid duplicate near-identical F606W records).
- Pending systems created (file=null records, paper II attached):
  `pks-1302-102`, `pg-1444-407`, `3c-323-1`. **3C 273 not touched** (exists,
  outside batch-T's write set): its `3c-273_bahcall1995` pending record is seeded
  and will materialize on the next `make_systems.py` run — orchestrator to note.
- `backend/fetch_extra.txt` (append-only): ADS_PDF gateway lines for
  1994ApJ...435L..11B → `bahcall1994_quasars.pdf` and 1995ApJ...450..486B →
  `bahcall1995_quasars.pdf` (published scans; can later replace the 1994 bitmap
  crops and provide the missing Paper-II figures incl. 3C 273 / PG 1444+407 hosts).

## New systems added by this batch (all region=extragalactic, categories=["quasar"], coords pending)
| id | name | z | image |
|---|---|---|---|
| pg-0953-414 | PG 0953+414 | 0.239 | cropped (bahcall1994) |
| pg-1116-215 | PG 1116+215 | 0.177 | cropped (bahcall1994) |
| pg-1202-281 | PG 1202+281 / GQ Com | 0.165 | cropped (bahcall1994) |
| pg-1307-085 | PG 1307+085 | 0.155 | cropped (bahcall1994) |
| pks-1302-102 | PKS 1302-102 | 0.286 | pending (bahcall1995) |
| pg-1444-407 | PG 1444+407 | 0.267 | pending (bahcall1995) |
| 3c-323-1 | 3C 323.1 | 0.266 | pending (bahcall1995) |

SIMBAD names for the coordinate pass: `data/coords_todo_batchT.txt` (all seven
resolve as written; sources give no usable coordinates and PG/PKS/3C names encode
only truncated B1950 positions, so ra/dec were left null rather than mis-plotted).

## Files touched
- `backend/manifests/batch-t/` (4 manifests), `backend/seeds/scattered3.py`
  (Bahcall stubs), `backend/fetch_extra.txt` (append), 7 PNGs under `images/<id>/`,
  `data/staging/t-*.json` (now `.merged`), `data/systems/`: 7 new + hd-100546 +
  2 HSC (via merge) , `data/coords_todo_batchT.txt`, `images/_sources/_views/t_*`
  (scratch views incl. ps2pdf conversions `b94.pdf`/`b95.pdf` left inside the two
  astro-ph extracted dirs for reproducibility of the 1994 manifest).
- NOT touched per batch rules: `data/ingestion_status.json` (orchestrator: mark
  hd-100546_acs2007 done, hsc pair done, bahcall-1994 done, bahcall-1995 pending
  fetch), `build.py` not run.
