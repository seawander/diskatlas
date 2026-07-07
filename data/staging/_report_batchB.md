# Batch B report — ALMA/mm debris (REASONS, ARKS, singles)

Agent: Batch B crop agent, 2026-07-06.
Staging written (NOT merged, per protocol): `reasons.json`, `arks.json`,
`single-fomalhaut-alma2017.json`, `single-fomalhaut-jwst2023.json`,
`single-aumic-alma2013.json`, `single-hr8799-alma2016.json`,
`single-vega-jwst2024.json`, `single-hd107146-alma2015.json`.
Manifests in `backend/manifests/alma-debris/`. 104 crops total, all ≤560 px.

## 1. REASONS (2501.09058, Matrà+2025, A&A 693, A151) — 74/74 belts cropped

Source: `REASONS_comboplot_merged.pdf` (Fig. 1; single page, 10 cols × 8 rows,
74 filled cells, ordered by RA). Manifest `reasons.json` (explicit bbox per
panel, dpi 200). image_id `<sysid>_reasons`, survey "REASONS".
Panel labels read from label contact-sheet + 7 individual crops spot-checked
(hd-105, vega, hd-216956c, hd-138813, hd-129590, beta-pic, gsc-07396-00759):
label ↔ file match confirmed everywhere.

Label → id map (label as printed; 38 existed, 36 NEW):
row-major RA order = HD105, GJ14, HD9672(=49-cet), HD10638, HD10647, HD14055,
HD15115, HD15257, HD15745, HD16743, HD21997, HD22049, HD32297, HD35841,
HD36546, HD38206, HD38858, HD39060(=beta-pic), HD48682, HD50571, HD53143,
HD54341, HD61005, HD76582, HD84870, TWA7(=twa-7), HD92945, HD95086, HD104860,
HD105211, HD106906, HD107146, HD109085(=eta-crv), HD109573(=hr-4796a),
HD110058, HD111520, HD112810, HD113556, HD113766, HD114082, HD115600,
HD117214, HD121191, HD121617, HD127821, HD129590, HD131488, HD131835,
HD138813, HD139664, HD142315, HD142446, HD145560, HD146181, HD146897,
HD147137, HD158352, HD161868, HD164249, GSC_07396-00759(=gsc-07396-00759),
HD170773, HD172167(=vega), HD181327, HD182681, HD191089, HD197481(=au-mic),
HD202628, HD205674, HD206893, HD207129, TYC93404371(=tyc-9340-437-1),
HD216956(=fomalhaut), HD216956C(=hd-216956c NEW), HD218396(=hr-8799).

All 20 pre-seeded `<id>_reasons` placeholders got their files; the appendix
figure `REASONS_comboplot_confused.pdf` (10 undetected/unresolved targets,
e.g. HD6798) was intentionally NOT cropped — non-detections.

### NEW systems (36, all category "debris"; SIMBAD names in coords_todo_batchB.txt)

| system id | SIMBAD name | note |
|---|---|---|
| hd-105 | HD 105 | |
| gj-14 | GJ 14 | |
| hd-10638 | HD 10638 | |
| hd-14055 | HD 14055 | = gamma Tri |
| hd-15257 | HD 15257 | also ARKS |
| hd-16743 | HD 16743 | |
| hd-22049 | HD 22049 | = eps Eri (id follows panel label) |
| hd-36546 | HD 36546 | |
| hd-38206 | HD 38206 | |
| hd-38858 | HD 38858 | |
| hd-48682 | HD 48682 | |
| hd-50571 | HD 50571 | |
| hd-54341 | HD 54341 | |
| hd-76582 | HD 76582 | also ARKS |
| hd-84870 | HD 84870 | also ARKS |
| hd-104860 | HD 104860 | |
| hd-105211 | HD 105211 | = eta Cru |
| hd-112810 | HD 112810 | |
| hd-113556 | HD 113556 | |
| hd-113766 | HD 113766 | |
| hd-121191 | HD 121191 | |
| hd-127821 | HD 127821 | |
| hd-131488 | HD 131488 | also ARKS |
| hd-138813 | HD 138813 | |
| hd-142315 | HD 142315 | |
| hd-142446 | HD 142446 | |
| hd-146181 | HD 146181 | |
| hd-147137 | HD 147137 | |
| hd-158352 | HD 158352 | |
| hd-161868 | HD 161868 | = gamma Oph; also ARKS |
| hd-164249 | HD 164249 | |
| hd-182681 | HD 182681 | |
| hd-205674 | HD 205674 | |
| hd-207129 | HD 207129 | |
| tyc-9340-437-1 | TYC 9340-437-1 | label printed TYC93404371; also ARKS |
| hd-216956c | Fomalhaut C | = LP 876-10; label HD216956C. merge_staging shell will guess simbad "HD 216956C" — replace with "Fomalhaut C" |

(These will be auto-created as shells by merge_staging; names/simbad/alt_names
come from the completed seeds on the next `make_systems.py` run. Watch the
tyc-9340-437-1 shell: auto-guessed name/simbad "tyc 9340 437 1" needs the
seeded form "TYC 9340-437-1".)

## 2. ARKS (2601.11708, Marino+2026 "ARKS I") — 24/24 belts cropped

Source: `Figures/Figure_continuum_images_arks_paper.png` (Fig. 3; 4 cols ×
6 rows, 4000×6000 px). Manifest `arks.json`. image_id `<sysid>_arks`, survey
"ARKS". Band: new ARKS data are Band 7 (0.88 mm), some systems archival
Band 6 → defaults set to Band 7/6, 880 um, "~0.88–1.3 mm continuum".
Gallery order (labels verified; 3 crops viewed: 49-cet, hd-131488,
tyc-9340-437-1): HD 9672 (49 Ceti), HD 10647 (q1 Eri), HD 14055 (γ Tri),
HD 15115, HD 15257, HD 32297, HD 39060 (β Pic), HD 61005, HD 76582, HD 84870,
HD 92945, HD 95086, HD 107146, HD 109573 (HR 4796), HD 121617, HD 131488,
HD 131835, HD 145560, HD 161868, HD 170773, HD 197481 (AU Mic), HD 206893,
TYC 9340-437-1, HD 218396 (HR 8799). All 24 are REASONS members → no extra
new systems beyond the 36 above. Gas moment maps and SMG gallery not cropped.

## 3. Singles (existing image_id records; staging updates them in place)

| image_id | source | crop | verified title |
|---|---|---|---|
| fomalhaut_alma2017 | 1705.05867 fig1a.pdf | Fig. 1 map area | "A Complete ALMA Map of the Fomalhaut Debris Disk" (MacGregor+2017) ✓ |
| fomalhaut_jwst2023 | 2305.03789 Fig2.png | Fig. 2 top-right F2550W sky panel | "Spatially resolved imaging of the inner Fomalhaut disk using JWST/MIRI" (Gáspár+2023) ✓ — record updated to MIRI F2550W, 25.5 um, technique "other" |
| au-mic_alma2013 | 1211.5148 f1.eps | Fig. 1 map area | "Millimeter Emission Structure in the First ALMA Image of the AU Mic Debris Disk" (MacGregor+2013) ✓ |
| hr-8799_alma2016 | 1603.04853 fig3.pdf | Fig. 3 restored image (+planet inset) | "Resolving the Planetesimal Belt of HR 8799 with ALMA" (Booth+2016) ✓ |
| vega_jwst2024 | 2410.23636 fig1_rot_ver2.pdf | Fig. 1 top annotated F2550W panel | "Imaging of the Vega Debris System using JWST/MIRI" (Su+2024) ✓ — record updated to MIRI F2550W, 25.5 um, technique "other" |
| hd-107146_alma2015 | 1410.8265 data_natural.eps | Fig. 1 natural-weight map | "ALMA Observations of the Debris Disk around the young Solar Analog HD 107146" (Ricci+2015) ✓ |

beta Pic Dent+2014 (bibcode-only): no source tarball → skipped, as briefed.

## 4. Seed fixes in backend/seeds/alma_debris.py

- REASONS membership completed: 20 → 74 members (gallery order, display names
  slugify exactly to the crop/system ids; checked programmatically against
  staging).
- ARKS stub filled: 24 members; new MM_ARKS defaults (Band 7/6, 880 um).
- P_REASONS: added bibcode 2025A&A...693A.151M.
- `verify=True` REMOVED (titles confirmed from local tex sources) for:
  MacGregor+2017 (1705.05867), Gáspár+2023 (2305.03789), MacGregor+2013
  (1211.5148), Booth+2016 (1603.04853; title case fixed to "Resolving the
  Planetesimal Belt of HR 8799 with ALMA"), Su+2024 (2410.23636),
  Ricci+2015 (1410.8265).
- Fomalhaut jwst2023 & Vega jwst2024 seed image records updated to
  MIRI F2550W / 25.5 um / technique "other" to match the actual crops.

## 5. WRONG-TARBALL FLAGS (need orchestrator follow-up)

1. **1611.02196 is NOT the eta Crv paper.** Tarball contains Faramaz+ "Inner
   mean-motion resonances with eccentric planets: A possible origin for
   exozodiacal dust clouds" (exozodi dynamics; no eta Crv image). Seeds:
   eta Crv alma2017 set to arxiv=None, verify=True kept. No crop made
   (`eta-crv_alma2017` stays file:null). Correct id for Marino+2017
   (MNRAS 465, 2595) must be looked up online + re-fetched.
   NOTE: systems JSON `eta-crv.json` still carries arxiv "1611.02196" —
   orchestrator should clear it when convenient (I did not touch systems/*).
2. **1703.10893 is NOT an astronomy paper.** The tarball is a raw PDF of an
   IEEE speech-enhancement article (Hou+ "Audio-Visual Speech Enhancement
   Using Multimodal Deep CNNs"). Seeds: hd-95086 alma2017 set to arxiv=None,
   verify=True kept, title/journal corrected to the believed-correct paper
   Su+2017 "ALMA 1.3 mm Map of the HD 95086 System", AJ 154, 225 (unconfirmed
   locally). No single-paper crop (`hd-95086_alma2017` stays file:null; the
   system DID get its REASONS + ARKS crops). Same note re systems JSON.

## 6. Crop inventory (104 files)

- 74 × `images/<sysid>/<sysid>_reasons.png` (348×347 px)
- 24 × `images/<sysid>/<sysid>_arks.png` (560×560 px)
- 6 singles: fomalhaut_alma2017 (509×560), fomalhaut_jwst2023 (560×560),
  au-mic_alma2013 (560×559), hr-8799_alma2016 (560×559),
  vega_jwst2024 (560×447), hd-107146_alma2015 (510×560)

ingestion_status.json NOT updated (orchestrator merges; suggested state:
reasons images done, arks images done, debris singles done except
eta-crv_alma2017 / hd-95086_alma2017 blocked on wrong tarballs).
