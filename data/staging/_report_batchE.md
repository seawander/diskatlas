# Batch E report — Ren+2023 HST STIS/NICMOS + ALICE (+ Hagan+2018 check)

50 crops produced, all viewed against burned-in panel labels (label sheets kept in
`images/_sources/_views/e_check_stis-ren.png`, `e_check_nicmos.png`, `e_check_alice.png`),
all run through `trim_borders.py` (46 trimmed, 4 already clean), all <=640 px / <400 KB.

## 1. Ren+2023 (2302.04273) — "Debris Disk Color with the Hubble Space Telescope"

- Exact title verified from `ms.tex` and fixed in `P_REN_STIS` (was paraphrased,
  `verify` flag removed). Journal A&A 672, A114; bibcode 2023A&A...672A.114R kept.
- Sample = 23 debris systems (Table 1, letters a–w). **Fig. 2 (STIS) shows all 23**
  -> 23 crops `<sysid>_stis-ren` (survey STIS-Ren), staging `stis-ren.json`.
- NICMOS: Fig. 3 (F110W) shows 20 targets (blank cells: HD 35650, TWA 7, TWA 25);
  Fig. 4 (F160W) shows 13. One record per system as briefed: F110W crop when it
  exists, F160W crop for the 3 F110W-less targets -> 23 crops `<sysid>_nicmos-ren2023`
  (survey NICMOS-Ren2023), staging `e-nicmos-ren2023-f110w.json` + `e-nicmos-ren2023-f160w.json`
  (split so wavelength metadata is per-filter: 1.12 um vs 1.60 um).
- Both member lists completed in `backend/seeds/scattered.py` (23 + 23, with
  F160W wavelength overrides for HD 35650/TWA 7/TWA 25).
- Slug notes: panel "49 Ceti" -> existing id `49-cet`; panel "HD 141569"
  (= HD 141569A in the text) -> existing id `hd-141569`; HR 4796A keeps
  simbad override "HR 4796".

### !! Orchestrator action needed: 6 stale `_stis-ren` pending records
`gsc-07396-00759`, `hd-114082`, `hd-117214`, `hd-129590`, `hd-146897`, `hd-106906`
have pending `<sysid>_stis-ren` records citing Ren "The Large-Scale Structure of
Debris Disks Newly Imaged with HST/STIS" (AAS240 abstract 2022, `_verify`).
**None of these systems are in 2302.04273** (checked against Table 1 and all three
gallery figures), so the ids could NOT be reused as the brief assumed. The records
belong to a different, apparently still-unpublished program. Recommend: delete them
(or re-point to the AAS abstract / its eventual paper) — I did not touch
`data/systems/*`. The seeds STIS-Ren block now carries a comment documenting this.

## 2. ALICE (1512.02220, Choquet+2016)

- Source tarball extracted (was un-extracted): `images/_sources/extracted/1512.02220/`.
- Title verified from ms.tex: "First images of debris disks around TWA 7, TWA 25,
  HD 35650, and HD 377" (emulateapj `[apjl]`); seeds fixed (sentence case), journal
  ApJL 817, L2 kept, bibcode 2016ApJ...817L...2C added, `verify` removed.
- Fig. 2 = 4 rows (TWA 7, TWA 25, HD 35650 in F160W; HD 377 in F110W) x 4 columns;
  cropped the leftmost "NICMOS images" column -> `twa-7_alice`, `twa-25_alice`,
  `hd-35650_alice`, `hd-377_alice` (staging `e-alice-f160w.json` + `e-alice-f110w.json`,
  survey ALICE). These fill the 4 pre-existing pending `_alice` records; the F160W
  members got wavelength overrides (1.6 um) in the seeds ALICE block.

## 3. Hagan+2018 (1802.07754) — checked, nothing to crop

- No source tarball in `images/_sources/arxiv/` AND (checked via ar5iv full text)
  the paper is the technical "ALICE Data Release: A revaluation of HST-NICMOS
  coronagraphic images" — **it contains no disk gallery figure** (tables + format
  specs only). The "11/12 disks" phrase refers to its intro: 12 disks newly revealed
  by ALICE = Soummer+2014 x5 (HD 30447, HD 35841, HD 141943, HD 191089, HD 202917)
  + Choquet+2016 x4 + Choquet+2017 (49 Cet) + Choquet+2018 x2 (HD 104860, HD 192758).
  All 12 are now covered in the atlas via `_nicmos-ren2023` and/or `_alice` images.
- **Choquet+2018 arXiv id (single WebSearch as briefed): 1801.05424** —
  "HD 104860 and HD 192758: Two Debris Disks Newly Imaged in Scattered Light with
  the Hubble Space Telescope", ApJ 854, 53, bibcode 2018ApJ...854...53C
  (sources: https://arxiv.org/abs/1801.05424 ,
  https://ui.adsabs.harvard.edu/abs/2018ApJ...854...53C/abstract ). Noted in the
  seeds ALICE block notes. Optional follow-up: host-fetch 1801.05424 if per-paper
  discovery images are wanted in addition to the Ren+2023 uniform ones.

## New systems (auto-created by staging; also in seeds now)

| id | name | category | note |
|---|---|---|---|
| hd-141943 | HD 141943 | debris | Ren+2023 sample (G2; first imaged Soummer+2014) |
| hd-192758 | HD 192758 | debris | Ren+2023 sample (F0V; Choquet+2018 discovery) |
| hd-202917 | HD 202917 | debris | Ren+2023 sample (G7V; first imaged Soummer+2014) |

Coordinates needed -> `data/coords_todo_batchE.txt` (also lists pre-existing
TWA 25 / HD 35650 / HD 377, which still have null ra/dec).

## Files touched

- `backend/manifests/hst-e/{stis-ren,e-nicmos-ren2023-f110w,e-nicmos-ren2023-f160w,e-alice-f160w,e-alice-f110w}.json`
- `data/staging/{stis-ren,e-nicmos-ren2023-f110w,e-nicmos-ren2023-f160w,e-alice-f160w,e-alice-f110w}.json` (23+20+3+3+1 = 50 records)
- `images/<sysid>/` 50 new PNGs (`*_stis-ren`, `*_nicmos-ren2023`, `*_alice`)
- `backend/seeds/scattered.py` — STIS-Ren, NICMOS-Ren2023, ALICE blocks only
- `data/coords_todo_batchE.txt`
- previews/checks in `images/_sources/_views/` (fig-*_prev, e_check_*)

No merge/build run; `data/systems/*` and `data/ingestion_status.json` untouched
(ingestion_status suggestion: stis-ren images done 23/23, nicmos-ren2023 done 23/23,
alice done 4/4; Hagan+2018 = no-op).
