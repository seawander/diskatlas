# Batch F report — SPHERE/GPI scattered-light surveys (Engler+2025, DESTINYS ChamI/Orion, DISCS)

Agent: Batch F. **77 image records staged** from 4 papers (7 staging files); membership
read off the gallery figures (panel labels = ground truth); 25+ crops visually verified
(all four grid corners of every gallery + all unusual/new panels). No merge/build run;
no data/systems edits. Seeds: complete member lists appended to `backend/seeds/scattered2.py`
(scattered.py untouched). Verified: seed expansion produces exactly the 77 image_ids
matching the 77 cropped files; trim_borders run on all new PNGs.

## 1. Per-survey summary

| survey | staging files | crops | source | notes |
|---|---|---|---|---|
| SPHERE-debris-2025 (Engler+2025, A&A 704 A21, 2512.03128) | sphere-debris-2025-p[1-4].json | **50** | full-paper PDF pages 9/10 (Fig. 5a/b Qphi) + 6/7 (Fig. 2a/b total int.) | 36 PDI + 14 total-intensity-only systems |
| SPHERE-ChamI (Ginski+2024, A&A 685 A52, 2403.02149) | sphere-chami.json | **13** | figures/ChaI-gallery.pdf (Fig. 2 mosaic) | 12 disks + CHX 22 (see below) |
| DESTINYS-Orion (Valegard+2024, A&A 685 A54, 2403.02156) | destinys-orion.json | **10** | detected-disks-orion.pdf (Fig. 2) | all 10 detections (3 bright + 7 faint) |
| DISCS (Hom+2025, AJ in press, 2505.02976) | discs.json | **4** | Qr_image_all_v3.pdf (Fig. 1) | 4 resolved of 7 observed |

Manifests: `backend/manifests/sphere-f/{engler-p1..p4,chami,destinys-orion,discs}.json`.

### Engler+2025 details
- Paper resolves "51 debris disks" out of 161 archival SPHERE targets; the union of the
  two galleries is **50 unique systems — all cropped** (the 51 counts belts/multi-belt
  bookkeeping; Table 2 lists 47 systems, galleries add HD 141569, HD 202917, HD 218396).
- Qphi panel preferred where both exist; Fig. 2 (total intensity, ADI/RDI) used for the
  14 systems without a Fig. 5 panel: HD 105, HD 16743, HD 36546, HD 38206, HD 92945,
  HD 110058, HD 111520, HD 112810, HD 131488, HD 141011, HD 141943, HD 146181,
  HD 182681, TWA 25.
- Panel-label → id mapping of classics: HD 9672=49-cet, HD 39060=beta-pic,
  HD 109573=hr-4796a, HD 172555=hr-7012, HD 197481=au-mic, HD 218396=hr-8799.
- ZIMPOL (not IRDIS-H) panels, metadata fixed in staging (and mirrored in seeds):
  hd-98800 (R' 0.63 um; scale bar in its panel is 0.5", all others 1"),
  hd-145560 (VBB 0.74 um), hr-7012 (VBB 0.74 um).
- image_id `<sysid>_sphere-debris-2025`; survey name "SPHERE-debris-2025" (4 page-wise
  staging files all carry the same survey_name).

### DESTINYS Cham I details
- 13/20 targets show extended circumstellar signal (paper Fig. 2 mosaic around the
  Herschel map); 12 are disk detections. **CHX 22 kept with caveat**: tail-like
  structure shaped by the close binary, not a regular disk (Zhang+2023) — noted in seeds.
- Bands: H, except HD 97048 + SY Cha (K band) and CS Cha + CV Cha (J band) — fixed in
  staging records and seed overrides.
- Wide panels retain in-figure companion annotations (HP Cha "A, B/C" + the mosaic's
  1" bar; CS Cha "Aa/Ab, B") — part of the published figure.

### DESTINYS Orion details
- All 10 detected disks cropped. Panel "V351Ori" mapped to existing system **pds-201**
  (coords in data/systems/pds-201.json match V351 Ori; alt name added in seeds).
  V1247 Ori is NOT part of this paper's detection gallery.

### DISCS details
- Title/authors verified from source: first author is **Justin Hom** (Crotts is 3rd);
  "accepted May 1, 2025, The Astronomical Journal". The `P_DISCS` stub in scattered.py
  says Crotts+2025 with `verify=True` — stub has no members so it emits nothing, but the
  orchestrator may want to delete/correct it (correct block lives in scattered2.py).
- Facility is **Gemini-GPI** (GPI H-band pol, GS-2019A-Q-109), not SPHERE.
- Resolved & cropped: HD 98363, HD 109832, HD 146181 (first time ever), HD 112810
  (first time in pol. light). Excluded: HD 108904 + HD 119718 (non-detections) and
  HD 113556 (only a tentative arc "hint" after smoothing).

## 2. New systems (30) — appended to data/coords_todo_batchF.txt

| survey | new ids | region / category |
|---|---|---|
| SPHERE-debris-2025 | hd-36968, bd-20-951 (both first-ever resolutions), hd-38397, hd-98800, hd-120326, hd-141011, hd-141943, hd-160305, hd-192758, hd-202917 | mixed (mostly Sco-Cen/young MG) / debris |
| SPHERE-ChamI | sz-45, cv-cha, vz-cha, cr-cha, chx-22, ww-cha, hp-cha, cs-cha, tw-cha | Chamaeleon I / protoplanetary |
| DESTINYS-Orion | hd-294260, hd-294268, pds-110, pds-113, rv-ori, v1012-ori, v1650-ori, v599-ori, v606-ori | Orion / protoplanetary |
| DISCS | hd-98363, hd-109832 | Sco-Cen / debris |

Notes for the orchestrator:
- hd-98800: gas-rich circumbinary (transition) disk around HD 98800 B; seeded as
  "debris" following Engler+2025's sample definition.
- chx-22: SIMBAD name "CHX 22" — if the resolver balks, use 2MASS J11124268-7722230.
- Already-existing systems touched only via staging (49-cet, beta-pic, au-mic, twa-7,
  twa-25, hr-4796a, hr-7012, hr-8799, gsc-07396-00759, pds-201, sy-cha, sz-cha, ct-cha,
  hd-97048, hd-112810, hd-146181 + the ~20 hd-* debris systems).

## 3. Files written
- backend/manifests/sphere-f/*.json (7 manifests)
- data/staging/sphere-debris-2025-p{1,2,3,4}.json, sphere-chami.json,
  destinys-orion.json, discs.json  (77 records)
- images/<sysid>/<image_id>.png (77 files, border-trimmed)
- backend/seeds/scattered2.py (4 survey blocks, 77 members)
- data/coords_todo_batchF.txt (30 names)
- previews kept in images/_sources/_views/ (engler_fig*, chami_*, orion_gallery, discs_qr)
