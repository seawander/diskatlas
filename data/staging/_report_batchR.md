# Batch R report — final 5 pending single-target records filled

All 5 crops produced with `crop_panels.py`, each final PNG individually VIEWED,
each trimmed with `backend/trim_borders.py` (all 5 reported trimmed; note: when
trim_borders is given *relative* paths its success print crashes on
`relative_to(ROOT)` and shows a cosmetic "SKIP" line AFTER the file was already
trimmed — verified by before/after sizes and the final "5/5 trimmed" count).
Manifests: `backend/manifests/batch-r/r-*.json` (5, one per panel).
Staging: `data/staging/r-*.json` (5 files, 5 records; exact existing `image_id`s
reused; `survey_name: null` in every manifest so the record's `survey` stays null).
No merge/build/validate run; no edits to `data/systems/*`, seeds, or
`ingestion_status.json` (concurrency protocol — orchestrator merges).
No new systems discovered; nothing for coords_todo.

## Crops (source → panel choice)

| image_id | source | crop | px |
|---|---|---|---|
| eps-ind-a_jwst2024 | 2503.01599 `figures/c1_data.pdf` = Fig. 1 | the two-band pair (10.65 + 15.50 um panels, planet upper-left, orange star marks Eps Ind A, scale bars + compass in right panel) — kept both since the record label is "10.65/15.5 um coronagraphy"; 15.50 um alone is the cleanest single panel if a square crop is ever preferred | 545x263 |
| beta-pic_alma2014 | 1404.1380 full PDF p. 8 = Fig. 1 | both map panels: (A) 870 um continuum + (B) CO J=3-2 with the SW clump, axes in AU, colorbars + beams in-panel — matches record label "870 um continuum + CO clump" | 498x536 |
| au-mic_acs2005 | astro-ph_0410466 `Krist.fig1.jpg.eps` (gs -dEPSCrop -r200 → `_views/r_krist_fig1.png`) = Fig. 1 | panel c) "F606W (PSF Subtracted)" — the classic clean edge-on midplane strip with E/N compass (panels a/b are raw star+PSF, d is a hard stretch, e/f other filters); trim leaves the "c)" label flush to the left edge but intact | 548x91 |
| hd-141569_acs2003 | astro-ph_0303605 `clampin.fig5.jpg` = Fig. 5 | direct coronagraphic false-color V-band (F606W) image of the tightly-wound spiral ring system, top arcsec ruler + N compass + companions 1/2 kept, bottom colorbar block excluded (deprojected Fig. 7/8 versions inspected but the color Fig. 5 is the iconic panel) | 351x333 |
| au-mic_sphere2015 | `extra/boccaletti2015_aumic.pdf` p. 2 = Fig. 1 | panel e "IRDIS 2014 (LOCI)" — the annotated panel with fast-moving features A–E labeled, yellow star, 1"=9.9 au segmented scale bar, E/N compass (panels a/b are HST/STIS epochs, c/d other reductions) | 556x133 |

## Metadata verification / fixes (carried in the staging records)

- **au-mic_sphere2015 (`_verify` flag resolved) — 3 real fixes:** the paper text
  (p. 1 + Methods) says AU Mic was observed 2014-08-10 with SPHERE/IRDIS **in the
  J band (1.25 um, broadband J in both channels)** using **ADI** reductions
  (avg. profile subtraction / KLIP / LOCI — no polarimetry; the record's 1.65 um
  was the *Strehl reference wavelength* quoted in the same sentence). Fixed:
  `technique` PDI → **ADI**, `wavelength_um` 1.65 → **1.25**, `wavelength_label`
  "H band; fast-moving features" → **"J band; fast-moving features A-E"**.
  Title/journal verified from the reprint: "Fast-moving features in the debris
  disk around AU Microscopii", doi:10.1038/nature15705, Nature 526, 230 ✓,
  bibcode 2015Natur.526..230B ✓; `arxiv` stays null (Nature reprint, no arXiv id).
  The staging `paper` block intentionally omits `_verify`, so the flag is dropped
  on merge.
- **eps-ind-a_jwst2024 — verified, no fix needed:** the 2503.01599 source tex
  (`sn-nature` class) carries exactly the title "A temperate super-Jupiter imaged
  with JWST in the mid-infrared" → the tarball IS the late-posted source of the
  Nature 2024 paper, so `journal` "Nature 633, 789", `bibcode` 2024Natur.633..789M
  (kept as instructed) and `arxiv` 2503.01599 are mutually consistent.
- **beta-pic_alma2014 — verified, no fix:** PDF p. 1 header: "Molecular Gas Clumps
  from the Destruction of Icy Bodies in the β Pictoris Debris Disk, Science (2014)
  343, 1490" ✓; Fig. 1 caption confirms 870 um continuum + CO J=3-2 (345.796 GHz)
  → Band 7 ✓.
- **au-mic_acs2005 — verified, no fix:** tex `\title` matches; slugcomment
  "Submitted to The Astronomical Journal" consistent with AJ 129, 1008 ✓; panel is
  F606W → 0.6 um ✓.
- **hd-141569_acs2003 — verified, no fix:** tex `\title` "HST/ACS Coronagraphic
  Imaging of the Circumstellar Disk around HD 141569A" = record's published-form
  title; AJ 126, 385 ✓; Fig. 5 is V-band (F606W) → 0.6 um ✓.

## Files touched

- `backend/manifests/batch-r/`: r-epsind-jwst2024.json, r-betapic-alma2014.json,
  r-aumic-acs2005.json, r-hd141569-acs2003.json, r-aumic-sphere2015.json
- `images/eps-ind-a/eps-ind-a_jwst2024.png`, `images/beta-pic/beta-pic_alma2014.png`,
  `images/au-mic/au-mic_acs2005.png`, `images/au-mic/au-mic_sphere2015.png`,
  `images/hd-141569/hd-141569_acs2003.png`
- `data/staging/r-*.json` (5) + this report
- scratch renders in `images/_sources/_views/r_*.png` (page/figure views, test
  crops, label zoom — safe to delete)
