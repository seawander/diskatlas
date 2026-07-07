# Batch M report — census-figure completion (ambient/outflow + companion panels) + AU Mic c LC

Scope: add EVERY remaining target panel from the three SPHERE census imagery figures
(previously only "clean disk detections" were cropped), plus the AU Mic c transit
light curve from the newly fetched Martioli+2021 source. No merge/build run here.

Manifests: `backend/manifests/batch-m/{m-taurus-ambient,m-taurus-faint,m-orion-companions,m-aumic-tessc}.json`
Staging: `data/staging/{m-taurus-ambient,m-taurus-faint,m-orion-companions,m-aumic-tessc}.json`
All 19 crops were VIEWED individually (in-panel labels match ids) and border-trimmed.

## 1. Garufi+2024 SPHERE-Taurus (2403.02158, Fig. 2 `Figures/Imagery.pdf`) — 11 new panels
All 11 previously excluded targets have panels in Fig. 2; all cropped as `<sysid>_sphere-taurus`
(survey SPHERE-Taurus, H band 1.65 um pol. intensity; A&A 685, A53).

Ambient/outflow-dominated per Garufi+2024 Table 3 ("Ambient") — credit carries the note
"(crop; ambient/outflow-dominated per Garufi+2024)":
- t-tau_sphere-taurus (PI image; close binary)
- xz-tau_sphere-taurus (PI image; close binary) — NEW system xz-tau
- uy-aur_sphere-taurus (PI image; close binary)
- ry-tau_sphere-taurus (disk + outflow cavities)
- hp-tau_sphere-taurus (tall panel, strong ambient nebulosity)

"Faint" category per the same table (marginal or formally undetected disk signal),
standard credit "Garufi et al. 2024, Fig. 2 (crop)":
- hn-tau_sphere-taurus (primary + companion visible)
- ds-tau_sphere-taurus (alpha_pol < 0.2, formal non-detection)
- gk-tau_sphere-taurus
- dk-tau_sphere-taurus (alpha_pol < 0.2)
- v807-tau_sphere-taurus (close binary; alpha_pol < 0.3) — NEW system v807-tau
- v1025-tau_sphere-taurus (alpha_pol < 0.2) — NEW system v1025-tau

Panel boxes were measured programmatically from the gray separator lines (260 dpi raster),
column/row fractions consistent with the earlier sphere-taurus manifests. GG Tau, RW Aur,
DG Tau, UX Tau, DO Tau, SU Aur etc. were already cropped in the first pass; with these 11
the Fig. 2 gallery (43 targets) is now fully covered: 32 + 11 = 43.

## 2. Ginski+2024 Cham I (2403.02149) second pass — NO additions needed
The imagery figure `figures/ChaI-gallery.pdf` (Fig. 2) contains exactly 13 target panels
(SZ 45, CV Cha, VZ Cha, CT Cha, CR Cha, SY Cha, CHX 22, WW Cha, HD 97048, HP Cha, CS Cha,
TW Cha, SZ Cha) around a central region map — all 13 were already cropped (`<id>_sphere-chami`).
The 7 non-detections (CHX 18N, WY Cha, SZ 41, RX J1106-7721, PDS 51, WX Cha, DI Cha) appear
only in the appendix same-scale gallery (`figures/gallery.pdf`) at pure noise level (no
circumstellar signal), so they were not cropped.

## 3. Valegard+2024 DESTINYS-Orion (2403.02156) second pass — 7 new panels
- Verified the first-pass 10/10 coverage of the detected-disks figure
  (`detected-disks-orion.pdf`); its "V351Ori" panel is the existing crop
  `pds-201_destinys-orion` (PDS 201 = V351 Ori, correct object; alias already in the system file).
- The sample "Imagery" figure (Fig. 1, `master_of_orion_3.0.png`) additionally shows 7
  orange-framed companion-detection thumbnails with clear signal (total intensity H band).
  All 7 cropped as `<sysid>_destinys-orion`, survey DESTINYS-Orion (A&A 685, A54), wavelength
  label "H band 1.6 um (total intensity)", technique "total intensity", credit
  "Valegard et al. 2024, Fig. 1 thumbnail (crop); companion detected, no disk in polarized light":
  - tx-ori_destinys-orion — NEW system tx-ori
  - v1788-ori_destinys-orion — NEW system v1788-ori (triple)
  - v2149-ori_destinys-orion — NEW system v2149-ori (binary)
  - v1787-ori_destinys-orion — NEW system v1787-ori
  - kiso-a-0904-60_destinys-orion — NEW system kiso-a-0904-60 (SIMBAD "Kiso A-0904 60")
  - brun-252_destinys-orion — NEW system brun-252
  - ry-ori_destinys-orion — NEW system ry-ori (companion ~72-80 MJup, stellar/substellar boundary)
- Note: Fig. 1 labels one blue thumbnail "HD 296268"; the paper text/tables and the
  detected-disks figure consistently use HD 294268 — figure typo, existing hd-294268 crop correct.
- The remaining 6 Orion non-detections (no disk, no companion) have no thumbnails in any figure.

## 4. Martioli+2021 AU Mic (2012.13238) — tar present, extracted, cropped
`images/_sources/arxiv/2012.13238.tar` existed; `extract_sources.py` unpacked it
(18 figure files). Verified `main.tex` title: "New constraints on the planetary system
around the young active star AU Mic — Two transiting warm Neptunes near mean-motion
resonance" (Martioli et al. 2021, A&A 649, A177). Cropped the phase-folded panel
(bottom-right of Fig. 6, `aumic_c_alltransits_mcmcfit.png`: binned TESS data + transit
model + previous model + residuals vs TBJD-Tc) as `au-mic_tess-c`
(`images/au-mic/au-mic_tess-c.png`, 501x289). The record reuses the paper block already in
`data/systems/au-mic.json` (image_id exists there with file:null; merge will fill `file`,
`credit` "Martioli et al. 2021, Fig. 6 (crop): phase-folded TESS transits of AU Mic c",
survey left null). Note: the c transits in this paper are TESS-only (Spitzer transits are
for planet b).

## New systems (10) → `data/coords_todo_batchM.txt`
Taurus (protoplanetary, region Taurus): xz-tau ("XZ Tau"), v807-tau ("V807 Tau"),
v1025-tau ("V1025 Tau").
Orion (region Orion; young stars with IR excess, disk undetected in scattered light,
companion imaged): tx-ori ("TX Ori"), v1788-ori ("V1788 Ori"), v2149-ori ("V2149 Ori"),
v1787-ori ("V1787 Ori"), kiso-a-0904-60 ("Kiso A-0904 60"), brun-252 ("Brun 252"),
ry-ori ("RY Ori").
These will be auto-created as shells by `merge_staging.py`; orchestrator should fill
coords/region/categories (suggest categories ["protoplanetary"] for the Taurus trio; for
the Orion seven the panels show no disk — categories at orchestrator's discretion).

## Files touched (allowed set only)
- backend/manifests/batch-m/*.json (4 manifests)
- images/<sysid>/*.png (19 new crops, all trimmed)
- data/staging/m-*.json (4 staging files) + this report
- data/coords_todo_batchM.txt
- images/_sources/_views/mM_*.png (inspection rasters)
Not run: merge_staging.py / validate.py / build.py; data/systems untouched.
