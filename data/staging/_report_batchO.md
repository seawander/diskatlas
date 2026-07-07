# Batch O report — 12 pending single-target records filled

All 12 crops produced, individually VIEWED against panel labels, and border-trimmed.
Manifests: `backend/manifests/batch-o/*.json` (9). Staging: `data/staging/o-*.json` (9 files, 12 records).
No merge/build run (orchestrator to run `merge_staging.py` → `validate.py` → `build.py`).
No new systems discovered; nothing added to coords_todo.

## Crops (source → panel choice)

| image_id | source | crop | size |
|---|---|---|---|
| tw-hya_stis2017-shadow | 1701.03152 `imagesrsq.ps` (Fig. 2, rendered 280 dpi → `_views/batch-o/src_debes17_imagesrsq.png`) | 2016-R^2 panel (bottom-right; cleanest single epoch, no annotation arrows) | 560x560 |
| tw-hya_stis2023-shadows | 2305.03611 `fig-r2.pdf` (Fig. 2) | right panel: 2021 epoch with the TWO shadows labeled B, C (+1" bar) | 480x480 |
| rx-j1604-3-2130_alma2023 | 2301.01684 `figures/J1604_Dust_PeakFlux_Temp_resid_new_res.png` (Fig. 1) | full 3-panel figure: (a) 231 GHz continuum, (b) 12CO peak Tb, (c) residuals | 551x210 |
| hd-107146_acs2004-f606w | astro-ph/0411422 `f1.eps` (Fig. 1, rendered 250 dpi → `_views/batch-o/src_ardila_f1.png`) | TOP-LEFT panel, label "F606W", V-mag colorbar | 480x480 |
| hd-107146_acs2004-f814w | same | TOP-RIGHT panel, label "F814W", I-mag colorbar | 480x480 |
| hd-107146_nicmos2011 | 1107.1057 `imaSca.pdf` (Fig. 1) | RIGHT panel = HST/NICMOS 1.1 um (caption: left 0.6, center 0.8, right 1.1 um) | 557x535 |
| hd-216956c_jwst2024 | 2405.00573 `figures/fomc_alma_overlay_and_astrometry.pdf` (Fig. 1) | LEFT panel: NIRCam F356W MCRDI detection (right panel is the same image + ALMA contours — redundant for a thumbnail) | 559x557 |
| hr-8799_miri2024 | 2310.13414 `images_raw_and_sub.pdf` (Fig. 1) | full BOTTOM row (ref-subtracted, N up): F1065C w/ planets b,c,d,e labeled; F1140C w/ 50 au bar+compass; F1550C & F2100W w/ "inner disk" marked | 552x144 |
| hd-100453_gravity2022-shadow | 2112.00123 `data/shadow_predictions_a.pdf` = **Fig. 7**, row 1 | middle+right pair (Δθ1 blue / Δθ2 orange) as one image | 560x272 |
| hd-142527_gravity2022-shadow | Fig. 7, row 2 | middle+right pair | 560x273 |
| cq-tau_gravity2022-shadow | Fig. 7, row 3 | middle+right pair | 560x273 |
| hd-135344b_sphere2016 | 1603.00481 `figures/images_irdis.pdf` = **Fig. 2**, row 3 middle | IRDIS **J-band** r^2-scaled Q_phi (paper: shadow features seen at highest S/N in J band) | 547x558 |

Bohn Fig. 7 row order verified by in-panel labels: HD 100453 / HD 142527 / CQ Tau / V1247 Ori / V1366 Ori / RY Lup.
Fig. 8 (`shadow_predictions_b.pdf`) holds only the ambiguous cases DoAr 44 / HD 135344 B / HD 139614 — none of our three targets.

## Paper-metadata fixes (carried in staging `paper` dicts; `_verify` flags drop out on merge)

1. **2301.01684 Stadler+2023 — TITLE WAS WRONG.** Actual (main.tex): *"A kinematically detected planet candidate in a transition disk"* (seed had "The kinematically disturbed disk around RXJ1604.3-2130A…", which does not exist). Journal seed "A&A 670, L1" consistent with the Letter format; bibcode 2023A&A...670L...1S added (derived from that vol/page).
2. **2405.00573 Lawson+2024 — JOURNAL WAS WRONG.** main.tex has `\submitjournal{\apjl}` + `\accepted{2024 April 28}` → fixed "AJ (2024)" → **"ApJL (2024)"**. Title/first author confirmed (Kellen Lawson).
3. **1107.1057 — first author "Ertel" CONFIRMED** (Steve Ertel, paper.tex). Title expanded to the actual tex title *"Multi-wavelength modeling of the spatially resolved debris disk of HD 107146"* (seed had the shorter running title). Journal upgraded "A&A (2011)" → "A&A 533, A132" + bibcode 2011A&A...533A.132E — **vol/page from model memory, not the source; spot-check advised**.
4. **1701.03152 Debes+2017** — title/author confirmed from ms_v4_rev2.tex; bibcode 2017ApJ...835..205D added (derived from seeded "ApJ 835, 205").
5. **2305.03611 Debes+2023** — title confirmed: "The surprising evolution of the shadow on the TW Hya disk" (aastex631). Journal left "ApJ (2023)" — volume/page not verifiable offline.
6. **2310.13414 Boccaletti+2024** — title confirmed verbatim; first author A. Boccaletti confirmed. Journal left "A&A (2024)".
7. **Bohn+2022, Ardila+2004, Stolker+2016** — seed title/journal/bibcode confirmed correct against the tex (Bohn title+subtitle merged in seed, fine).

## Field fixes in image records (staging overrides)

- **hd-135344b_sphere2016**: panel is IRDIS **BB_J** → `instrument` "IRDIS/ZIMPOL"→"IRDIS", `wavelength_um` 0.62→**1.245** (tex: BB_J λc=1.245 um), label → "J band Q_phi (r^2-scaled); spirals + shadows cast by the inner disk". (ZIMPOL bands in that paper are R_PRIM 0.626 / I_PRIM 0.790 um, Fig. 1 — not used.)
- **hd-216956c_jwst2024**: Fig. 1 detection panel is **F356W** → `wavelength_um` 4.4→**3.56**, label updated.
- rx-j1604 label now mentions the actual Fig. 1 content (continuum + 12CO peak Tb + residuals).

## Notes

- ACS F606W/F814W crops re-made at `--max-px 480` to get under the 400 KB validator cap (noisy rainbow colormap compresses poorly): 349/348 KB.
- trim_borders printed harmless "SKIP …relative_to" messages when given relative paths — trimming itself succeeded (8/12 files had trimmable margins; sizes confirmed).
- View/render intermediates kept in `images/_sources/_views/batch-o/` (incl. the two .ps/.eps → PNG crop sources, which the manifests reference).
