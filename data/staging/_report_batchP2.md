# Batch P2 report — 14 pending single-target records filled (+1 confirmed no-source)

All 14 crops produced, each individually VIEWED, borders/colorbars/axis-labels trimmed.
Manifests: `backend/manifests/batch-p2/p2-*.json` (14, one per panel).
Staging: `data/staging/p2-*.json` (14 files, 14 records; exact existing `image_id`s reused,
`survey: null` in every record so the existing null survives the merge).
No merge/build/validate run, no seeds or `data/systems/*` edits, no `ingestion_status.json`
edit (concurrency protocol — orchestrator merges). No new systems discovered; nothing for coords_todo.

## Crops (source → panel choice)

| image_id | source (arXiv file = published Fig.) | crop | px |
|---|---|---|---|
| hd-32297_alma2018 | 1812.05610 `fig5a.pdf` = Fig. 5 left | 1.3 mm continuum (color) with 12CO(2-1) mom-0 contours; in-panel label "Continuum + 12CO(2-1)" | 560x559 |
| hd-61005_alma2018 | 1812.05610 `fig2b.pdf` = Fig. 2 | leftmost "HD 61005 - data" panel (pure ALMA image). Fig. 1 NOT used: its color map is the HST STIS image with ALMA only as contours — wrong content for a `disk_mm` record | 413x411 |
| hd-15115_alma2019 | 1905.08258 `fig1a.pdf` = Fig. 1 left | ALMA-only panel, in-panel label "HD 15115 ALMA 1.3mm" (right panel is the STIS overlay) | 554x560 |
| hd-92945_alma2019 | 1901.01406 `Figure_continuum_tapernatural_inferno_pbcor.pdf` = Fig. 1 right | 0.86 mm 12m+ACA image with 0.7" uv-taper (ring+gap much cleaner than the untapered left panel) | 559x560 |
| hd-206893_alma2020 | 2010.12582 `Figure_continuum_band6_pbcor_taper_0.4.pdf` = Fig. 1 right | Band 6 1.3 mm, 0.4" taper, in-panel "1.3 mm" label (checked B6 untapered + both B7 images — all noisier) | 559x560 |
| hd-181327_alma2016 | 1605.05331 `figure_ALMA_mem_restored_fov.png` = Fig. 1 | panel b) restored Briggs-weighted image (panel a is the MEM *model* — avoided; colorbar+axis strip trimmed) | 560x546 |
| hr-4796a_alma2018 | 1801.05429 `im_briggs.eps` = Fig. 1 (gs-rendered to `_views/p2_4796_briggs.png`) | self-calibrated Briggs r=0.5 ring image, colorbar excluded | 480x560 |
| hd-10647_alma2021 | 2106.05975 `Figures/B7_Image_newBeamNewAxes_301020_USE.png` = Fig. 4 | tapered natural-weighted Band 7 image, in-panel "Band 7: 0.86mm" (far cleaner than the Fig. 1 Band 6 image) | 560x560 |
| hd-131835_alma2019 | 1811.08439 `mom0_hd131835briggs05_CI.pdf` = Fig. 8 | [CI] 3P1-3P0 moment-0 image — matches the record's "[CI] 492 GHz" metadata (Band 8 continuum is Fig. 5) | 560x323 |
| hd-129590_alma2020 | 2005.05841 `continuumlast.pdf` = Fig. 1 | "HD129590" panel (row 3 left of the 10-star gallery, title kept). CO mom-0 gallery (`gaslast.pdf`, Fig. 2) is noise-dominated for this target — not used | 529x560 |
| hd-105_alma2018 | 1811.06440 `hd105_alma.pdf` = Fig. 2 | left "Image" panel (data; Model/Residual panels excluded; neighbour panel's axis labels trimmed) | 560x555 |
| 49-cet_alma2017 | 1704.01972 `f1.pdf` = Fig. 1 middle | 0.75" gaussian-tapered 850 um continuum — the cleanest resolved image (CO(3-2) mom-0 = Fig. 7 left carries best-fit model contours; CARMA Fig. 2 unresolved) | 428x418 |
| hd-95086_sphere2018 | 1801.05850 `fig14.pdf` = Fig. 14 bottom-left | IRDIS DPI Q_phi quadrant with the 106 au / 320 au belt-edge circles — the SPHERE debris-belt detection panel (detection is significant in the azimuthal average, Fig. 15) | 554x547 |
| vega_hst2024 | 2410.24042 full PDF, page 4 = Fig. 2 left | STIS cRDI (alpha Cyg reference) wide-halo mosaic out to ~50", incl. 27"/30" dashed circles; S/N map + colorbar excluded | 550x538 |

- **aa-tau_hst2013: left `file: null` as instructed.** Confirmed: Cox et al. 2013 (2013ApJ...762...40C)
  has no arXiv id, no `images/_sources/extracted/` dir exists, record already carries full paper
  metadata → renders as "image pending — see paper".
- 3 PNGs quantized to 256-color palette to meet the ≤300 KB guideline
  (hd-95086 499→214 KB, vega 355→170 KB, hd-206893 336→204 KB); quality visually re-checked.

## Paper-metadata fixes (carried in staging `paper` dicts; `_verify` flags drop out on merge)

1. **hd-15115 / 1905.08258 (_verify)** — title verbatim-confirmed from `hd15115_final.tex`; journal
   confirmed as **ApJL** via slugcomment "Accepted to ApJL: May 15, 2019". Volume/page not in source
   → journal stays "ApJL", bibcode stays null (link works via arXiv id).
2. **hd-206893 / 2010.12582 (_verify)** — title verbatim-confirmed ("Insights into the planetary
   dynamics of HD 206893 with ALMA"), MNRAS class + pubyear 2020 consistent; seeded
   "MNRAS 498, 1319" / bibcode kept (vol/page not verifiable offline, not contradicted).
3. **hd-131835 / 1811.08439 (_verify)** — long title verbatim-confirmed from tex. Journal
   "MNRAS 489, 3670" kept; **bibcode 2019MNRAS.489.3670K added — derived mechanically from the
   seeded vol/page, spot-check advised**.
4. **hd-105 / 1811.06440 (_verify)** — title + first author (J. P. Marshall) verbatim-confirmed.
   Journal was null → set to **"ApJ"** (emulateapj/iop class + apj.bst; no accepted-line in tex, so
   no vol/page). Bibcode left null.
5. **hd-95086 / 1801.05850 (_verify)** — full title is \title + \subtitle:
   *"Investigating the young Solar System analog HD 95086: A combined HARPS and SPHERE exploration"*
   ("Solar System" capitalized per tex). Journal "A&A 617, A76" + bibcode kept.
6. **vega / 2410.24042 (_verify)** — verified from the published page-1 header:
   *The Astronomical Journal, 168:236 (16pp), 2024 December*, DOI 10.3847/1538-3881/ad67cb, Wolff et al.
   → journal "AJ" upgraded to **"AJ 168, 236"**, **bibcode 2024AJ....168..236W added** (from that header),
   title capitalization per publication ("Deep Search for a Scattered Light Dust Halo Around Vega...").
7. **hr-4796a / 1801.05429** (no flag) — title verbatim-confirmed; **bibcode 2018MNRAS.475.4924K
   added — derived mechanically from the seeded "MNRAS 475, 4924", spot-check advised**.
8. **hd-10647 / 2106.05975** — tex title is "High resolution ALMA and HST images of q1 Eri..."
   (record had hyphenated "High-resolution"); fixed to verbatim.
9. Titles verbatim-confirmed, seeds already correct: MacGregor 2018 (slugcomment "Accepted to ApJ"
   consistent with "ApJ 869, 75"), Marino 2019 (full two-line title), Marino 2016, Kral 2020, Hughes 2017.

## Field fixes in image records (staging overrides on merge)

- **hd-95086_sphere2018 — WAVELENGTH WAS WRONG**: the IRDIS DPI sequence is **J band** (obs table:
  "IRDIS DPI J", 2015-05-02; Fig. 14 caption "IRDIS J-band ... Q_phi"). `wavelength_um` 1.65 → **1.26**,
  label → "J band 1.26 um Q_phi (faint pol. detection, azimuthally averaged)".
- **hd-10647_alma2021**: crop is the Band 7 image → `instrument` "Band 6/7" → **"Band 7"**,
  `wavelength_um` 1300 → **860**, label → "0.86 mm continuum (tapered)".
- **hd-181327_alma2016**: label "1.3 mm continuum + CO 2-1" → **"1.3 mm continuum"** (no CO image
  exists in the paper — CO shown only as spectra/radial profiles; crop is continuum-only).
- **hd-129590_alma2020**: label "1.3 mm continuum + CO 2-1" → **"1.3 mm continuum"** (continuum panel
  used; CO mom-0 not usable).
- **49-cet_alma2017**: label "0.85 mm continuum + CO 3-2" → **"0.85 mm continuum (tapered)"**.
- **hd-32297_alma2018**: label → "1.3 mm continuum (CO 2-1 contours)" (describes the Fig. 5 overlay).
- **hd-131835_alma2019**: label → "[CI] 492 GHz gas emission (moment 0)".
- All other records: type/facility/instrument/wavelength re-asserted unchanged; credits carry
  "Author et al. YYYY, Fig. N (crop)" with tex-verified figure numbers.
