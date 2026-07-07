# Batch J report — final crop batch (planet/GRAVITY/JWST + classic PDFs + SEEDS originals)

Date: 2026-07-06. Agent: Batch J.

## Summary

- **35 image records filled** (34 manifests in `backend/manifests/batch-j/`, staging in
  `data/staging/j-*.json`; `j-jwst-bar-2025` carries 2 panels: HR 8799 + 51 Eri).
- **3 skips** (source PDFs turned out to be captcha HTML, see below). 0 missing tarballs —
  all 13 SEEDS originals were present and extracted.
- All crops viewed and verified against panel labels; borders trimmed
  (`backend/trim_borders.py`); every new file ≤ 300 KB, ≤ 560 px.
- No `data/systems/*.json` touched; no merge/build run. Metadata corrections ride in the
  staging records (staging wins on merge).

## Filled records (16 planet/GRAVITY/JWST)

| image_id | source | panel cropped |
|---|---|---|
| af-lep_gravity2024 | 2411.05917 Fig. 1 | middle epoch (2023-11-24) GRAVITY Δχ² detection map |
| af-lep_jwst2024 | 2406.09528 Fig. 1 | F444W Oct 2023 image (planet W of star) |
| af-lep_sphere2023-mesa | 2302.06213 Fig. 1 | IFS S/N map, 2022-12-20 epoch |
| af-lep_sphere2023-derosa | 2302.06332 Fig. 4 | IRDIS K1 KLIP residual map |
| beta-pic_gravity2020 | 1912.04651 | sky-projected orbit w/ GRAVITY-astrometry inset (`gravity_orbit_skyproj.pdf`) |
| beta-pic_gravity2020c | 2010.04442 Fig. 1 | 2020-03-08 periodogram power (χ²) map = detection of c |
| hr-8799_gravity2019 | 1903.11903 Fig. 2 | Keplerian orbit fit + GRAVITY point (paper has no image-style detection map) |
| hr-8799_jwst2025 | 2503.13608 Fig. 4 | F410M PSF-sub image (b,c,d) + zoom with e (left+middle panels) |
| 51-eri_jwst2025 | 2503.13608 Fig. 4 | right panel: 51 Eri b F410M detection |
| pds-70_jwst2024 | 2403.04855 Fig. 1e | F480M disk-subtracted, b & c circled |
| twa-7_jwst2025 | 2502.15081 (pdf-only, **p. 3**) | Fig. 1 MIRI F1140C image, CC#1 arrowed |
| gj-504_sphere2018 | 1807.00657 Fig. 1 (`Vignette.pdf`) | IRDIS H2 (1.593 µm) panel, b arrowed |
| kappa-and_scexao2018 | 1810.09457 Fig. 2 | CHARIS ADI (conservative) collapsed image |
| hd-95086_naco2013b | 1310.7483 Fig. 1a | 26 Jun 2013 cADI L' residual map, b arrowed |
| 1rxs-j1609_gemini2010 | 1006.3070 Fig. 5 | NIRI+ALTAIR L' panel, companion circled |
| hd-106906_gpi2015 | 1510.02747 Fig. 1 | GPI H-band KLIP panel (Warp/Backside labels) |

## Filled records (6 classic papers)

| image_id | source | note |
|---|---|---|
| tw-hya_wfpc2-2000 | `extra/krist2000_twhya.pdf` **Fig. 7, PDF p. 6** (user-specified) | left panel = real PSF-subtracted F606W image (right panel is the model sim — excluded) |
| au-mic_kalas2004 | astro-ph_0403132 Fig. 1 | R-band coronagraphic discovery image |
| au-mic_keck2004 | astro-ph_0408164 Fig. 1 | landscape PS rotated 90° CCW to upright (disk horizontal) |
| hd-141569_nicmos1999 | astro-ph_9909097 Fig. 1 | left (annotated) panel |
| hd-100546_nicmos2001 | astro-ph_0009496 Fig. 1 (`hd100combine.ps`) | rotated 90° CW to upright; main map + nucleus inset |
| hr-4796a_keck1998 | astro-ph_9806268 `fig1.eps` | 20.8 µm MIRLIN resolved-disk image |

## Filled records (13 SEEDS originals; citations kept intact, credits now point to the original figure)

hr-4796a_seeds (1110.2488 Fig. 1b — LOCI conservative, streamers arrowed; note Fig. 1d is an
HST/STIS reprint and was deliberately avoided) · lkca-15_seeds (1005.5162 Fig. 1a) ·
mwc-480_seeds (1205.3159 Fig. 1) · mwc-758_seeds (1212.1466 Fig. 2f) · pds-70_seeds
(1208.2075 Fig. 2a) · ry-tau_seeds (1306.1887 Fig. 1) · sr-21_seeds (1302.5705 Fig. 1
`PImed_v2.pdf`) · sz-91_seeds (1402.1538 Fig. 4a, Ks PI + 345 GHz contours) · tw-hya_seeds
(1503.01856 Fig. 1) · ux-tau_seeds (1206.1215 Fig. 1) · hip-79977_seeds (1301.0625
`images_6.eps` panel a) · oph-irs-48_seeds (1411.0671 Fig. 1, H band after halo subtraction)
· hd-169142_seeds (1505.04937 Fig. 1a `polimage.eps`).

## Metadata fixes carried in staging (staging wins on merge)

1. **1rxs-j1609_gemini2010**: record said K band 2.2 µm / ADI, but the 2010 paper's only
   NIRI image figure is Fig. 5 (3.05 µm + L'). Cropped the L' panel →
   `wavelength_um: 3.8`, label "L' band (NIRI+ALTAIR); common proper motion confirmed",
   `technique: "other"`. Instrument (NIRI+ALTAIR) unchanged.
2. **hd-106906_gpi2015** (`_verify`): title confirmed from source tex ("Direct imaging of an
   asymmetric debris disk in the HD 106906 planetary system"); staging supplies full paper
   block with bibcode `2015ApJ...814...32K`, `_verify` dropped.
3. **ux-tau_seeds** (`_verify`): title confirmed from `submituxt3.tex`; paper block re-sent
   without `_verify` (PASJ 64, 124 kept).
4. **hd-169142_seeds** (`_verify`): title confirmed from `momose-ver3.tex`; paper block
   re-sent without `_verify` (PASJ 67, 83 kept).
5. **mwc-758_seeds**: cropped panel is the H PI + K' color composite (Fig. 2f, all
   HiCIAO); label adjusted to "H band (pol. intensity; H PI + K' composite)".
6. **hr-8799_gravity2019**: no χ²/detection map exists in that paper's source; used Fig. 2
   (orbit + GRAVITY astrometry). Metadata unchanged.

## Skips

| record | reason |
|---|---|
| ab-aur_stis1999 | `extra/grady1999_abaur.pdf` is a "Radware Bot Manager Captcha" HTML page, not a PDF — host re-download needed |
| hd-163296_stis2000 | same (`grady2000_hd163296.pdf` = captcha HTML); its paper `_verify` flag therefore NOT cleared |
| gm-aur_nicmos2003 | same (`schneider2003_gmaur.pdf` = captcha HTML) |

Known-unfixable list from the brief left untouched (eps-ind-a_jwst2024, beta-pic_alma2014,
hd-32297_stis2005, hd-141569_acs2003, au-mic_acs2005, au-mic_sphere2015, hd-100546_acs2007,
hd-100546_alma2014, gm-aur_seeds, hd-142527_seeds, lkha-330_seeds, 1rxs-j1609_gemini2008).

## New systems / coords

None — all 35 records belong to existing systems. No `coords_todo` entries.

## Files touched

- `backend/manifests/batch-j/*.json` (34)
- `data/staging/j-*.json` (34, 35 records) + this report
- `images/<sysid>/<image_id>.png` (35 new files)
- `images/_sources/_views/j-*` (view/QA scratch, incl. two pre-rotated PS sources)
