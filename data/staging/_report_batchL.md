# Batch L report — SEEDS Fig. 3 gallery crops (Tamura 2016)

Source: `images/_sources/extra/seeds_tamura2016.pdf` (Tamura 2016, Proc. Japan Acad. Ser. B 92, 45;
bibcode 2016PJAB...92...45T; 11 pages). Fig. 3 is on **PDF page 8** (journal p. 52): a 4x5 gallery,
embedded raster 1819x1517 px @ 350 ppi, so the manifest rasterizes at `dpi: 350` (native resolution;
each panel ~363x380 px, no downsizing needed).

## Fig. 3 layout (row-major, from the caption; verified visually on the rasterized page)

| Row | Panels (original reference per caption) |
|---|---|
| 1 | AB Aur (Hashimoto+2011) · SAO 206462 (Muto+2012) · MWC 758 (Grady+2013) · **LkHa 330 (Bonnefoy et al. in prep.)** · TW Hya (Akiyama+2015) |
| 2 | PDS 70 (Hashimoto+2012) · Sz 91 (Tsukagoshi+2014) · WLY 2-48 (Follette+2015) · LkCa 15 (Thalmann+2010) · HR 4796A (Thalmann+2011) |
| 3 | AB Aur close-up (Hashimoto+2011) · **HD 142527 (Fukagawa et al. in prep.)** · HD 169142 (Momose+2015) · RX J1604.3-2130A (Mayama+2012) · **GM Aur (Oh et al. in prep.)** |
| 4 | RY Tau (Takami+2013) · SR 21 (Follette+2013) · MWC 480 (Kusakabe+2012) · UX Tau A (Tanii+2012) · HIP 79977 (Thalmann+2013) |

Grid-vs-label sanity anchors viewed at full res: (1,1) = AB Aur (only 500 AU scale bar, "Spiral"
labels) and (4,5) = HIP 79977 (edge-on streak through speckles) — both match, no off-by-one.

## Cropped (3 panels — the only `_seeds` records still `file: null` in data/systems)

| system | image_id | file | credit / paper |
|---|---|---|---|
| lkha-330 | `lkha-330_seeds` | `images/lkha-330/lkha-330_seeds.png` (363x379) | Tamura 2016, Fig. 3 (crop); original: Bonnefoy et al. (in prep.) — paper block stays Tamura 2016 (original never published; caption ground truth) |
| hd-142527 | `hd-142527_seeds` | `images/hd-142527/hd-142527_seeds.png` (363x380) | Tamura 2016, Fig. 3 (crop); original: Fukagawa et al. (in prep.) — paper block stays Tamura 2016 |
| gm-aur | `gm-aur_seeds` | `images/gm-aur/gm-aur_seeds.png` (363x380) | Tamura 2016, Fig. 3 (crop); original: Oh et al. (in prep.) — paper block stays Tamura 2016 |

All three viewed after cropping: LkHa 330 (masked core + "Spiral" annotation), HD 142527 (large
asymmetric double-arc ring, "Gap"), GM Aur (inclined disk, "Gap") — morphologies and annotations
match the expected targets; edges clean, no neighbour-panel bleed. `trim_borders.py` run on all
three: 0 trimmed (panels sit on the figure's own noisy dark background; no uniform margins — expected).

Per-target paper blocks were reused from the pending records in data/systems; the caption agrees
with all three (all are "in prep." there, so Tamura 2016 remains the citable paper). Credits were
normalized to the requested format `Tamura 2016, Fig. 3 (crop); original: <Author (in prep.)>`.

## Skipped (17 panels)

- **13 panels already filled from their original publications** (`_seeds` records in data/systems
  have files + original-paper credits; NOT overwritten, per brief): MWC 758, TW Hya, PDS 70, Sz 91,
  WLY 2-48 (= oph-irs-48), LkCa 15, HR 4796A, HD 169142, RY Tau, SR 21, MWC 480, UX Tau A, HIP 79977.
- **4 panels without `<id>_seeds` records, but whose SEEDS data are already in the atlas from the
  original papers under other image_ids** — creating `_seeds` records would duplicate the same
  observation with a strictly lower-quality gallery crop, so skipped:
  - AB Aur (row 1) and AB Aur close-up (row 3): `ab-aur_seeds2011` (Hashimoto et al. 2011, Fig. 1 crop).
  - SAO 206462 = hd-135344b: `hd-135344b_seeds2012` (Muto et al. 2012, Fig. 2 crop).
  - RX J1604.3-2130A = rx-j1604-3-2130: `rx-j1604-3-2130_seeds2012` (Mayama et al. 2012, Fig. 1a crop).

No new systems needed (all 20 panel targets exist in data/systems); no `coords_todo_L.txt`.

## Files touched

- `backend/manifests/batch-l/seeds-fig3.json` (survey `seeds-fig3`, survey_name `SEEDS`;
  4x5 grid, `trim_frac` = figure region on page 8, `image_id_pattern` `{id}_seeds`, dpi 350;
  17 of 20 grid cells nulled).
- `images/{lkha-330,hd-142527,gm-aur}/<id>_seeds.png` (3 crops).
- `data/staging/l-seeds.json` (3 records, per-record credit; intermediate auto-generated
  `data/staging/seeds-fig3.json` removed to avoid double-merge).
- `images/_sources/_views/seeds_p8-08.png` (page preview kept; temporary test crops removed).

No merge/build run (orchestrator's job). After merge, the three records update in place
(system_id+image_id match; staging wins for file/credit/paper).
