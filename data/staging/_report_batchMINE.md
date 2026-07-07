# Batch MINE report — multi-wavelength mining of already-fetched tarballs

Agent: batch "MINE". 14 new image records staged from 10 papers, all for systems that
already had records; every crop visually verified; trim_borders run on all 14
(11 trimmed, 3 already clean). No merge/build run; no data/systems or
ingestion_status edits. No new systems (data/coords_todo_batchMINE.txt not needed).
Manifests: backend/manifests/mine/mine-*.json; staging: data/staging/mine-*.json.

## 1. Crops produced

| staging file | image_id | survey | what it adds vs sibling |
|---|---|---|---|
| mine-fomalhaut-f1550c | fomalhaut_jwst2023-f1550c | null | MIRI F1550C 15.5 um warm inner disk (sibling jwst2023 = F2550W outer ring); Fig2.png top-left |
| mine-fomalhaut-f2300c | fomalhaut_jwst2023-f2300c | null | MIRI F2300C 23 um coronagraphic view, intermediate belt; Fig2.png top-middle |
| mine-vega-f1550c | vega_jwst2024-f1550c | null | MIRI F1550C 15.5 um inner-disk panel (sibling = enlarged F2550W); fig1_rot_ver2.pdf bottom-left, incl. colorbar |
| mine-hltau-b3 | hl-tau_alma2015-b3 | null | single-band 2.9 mm B3 panel (a) — longest-wavelength view |
| mine-hltau-b7 | hl-tau_alma2015-b7 | null | single-band 0.87 mm B7 panel (c), sharpest rings (sibling = B6+B7 combined panel e) |
| mine-abaur-inner | ab-aur_sphere2020-inner | null | Boccaletti+20 Fig 1b: inner 2" Qphi with spirals S1/S2 + twist. NOTE: sibling ab-aur_sphere2020 is the LARGE 10" Qphi*r^2 view (panel a), not the inner twist as the priority list assumed — so the inner panel was the missing one |
| mine-pds70-k1 | pds-70_sphere2016-k1 | null | Haffert+19 Fig 2b: SPHERE/IRDIS K1 (2016-05-31) ADI, both planets circled; type planet, 2.11 um |
| mine-hd34700-j | hd-34700_gemini-lights-j | Gemini-LIGHTS | J-band Qphi (Final_images_1 row 3, label "HD 34700 A 20180103", band letter J verified in-crop) |
| mine-gpies-toti2 | au-mic_gpies-debris-toti | GPIES-debris | Fig 6 total-intensity (ADI) edge-on counterpart to Qphi crop |
| mine-gpies-toti2 | beta-pic_gpies-debris-toti | GPIES-debris | Fig 6 total-intensity counterpart (speckle-dominated but disk beam visible) |
| mine-dartts-j | im-lup_dartts-s-j | DARTTS-S | appendix gallery Qphi J r^2 (col 3, row 1) |
| mine-dartts-j | ru-lup_dartts-s-j | DARTTS-S | appendix gallery Qphi J **log** (col 4, row 3) — the r^2 J panel is speckle noise; log panel shows the disk |
| mine-hip65426-f1140c | hip-65426_jwst2023-f1140c | null | single-filter clean MIRI F1140C ADI+RDI panel (Carter+23 Fig 13 r1c4; sibling = Fig 8 multi-filter mosaic) |
| mine-twhya-zoom | tw-hya_alma2016-zoom | null | Fig 1 inset re-cropped at 500 dpi: inner 10.8 au, 1 au dark annulus resolved |

Survey field: set to the sibling record's survey (Gemini-LIGHTS / GPIES-debris /
DARTTS-S) where one exists, else null; paper blocks copied verbatim from the sibling
records in data/systems/*.json. image_id naming: gallery-survey additions use the
survey stem + band tag (`*_gemini-lights-j`, `*_gpies-debris-toti`, `*_dartts-s-j`)
to stay consistent with hd-15115/nz-lup whose `*_gpies-debris` already come from the
same totI figure; single-paper additions use `<sysid>_<facilityYEAR>-<tag>`.

## 2. Priority items skipped, with reasons

- **P4 PDS 70 MUSE separate b/c panels** — do not exist. Fig 1 and Fig 2a are the only
  MUSE Halpha images (both show b+c in one map; Fig 1 is aperture-annotated). Panels
  2b/2c are SPHERE K1 / NACO Lp; added the K1 one instead (pds-70_sphere2016-k1).
  A NACO Lp crop would be a third possibility but is PSF-smeared (c blended with disk) — skipped.
- **P6 GG Tau second panel** — skipped. Keppler+2020 is single-epoch H-band PDI only;
  the other figure candidates (GGTauA_..._I_pol_details_v2, GGTau_inner_region_Aasubtr_annot_2,
  spirals_2) are the SAME PI data smoothed and heavily annotated (dashed overlays, labels)
  = cosmetic variants per the near-duplicate rule.
- **P7 HD 142527 / HD 100453 second band** — not in the paper. Rich+2022 final-images
  appendix (all 71 observations indexed) has HD 142527 only at H (20140425) and
  HD 100453 only at J (20150411). Only HD 34700 A was observed in both bands.
- **P12 exoALMA I 12CO gallery** — tarball 2504.18688 not present in images/_sources/
  (only 2504.18725 = Paper IV continuum). Nothing to crop; consider adding the id to a
  future fetch list if CO panels are wanted.

## 3. Notes for the orchestrator

- fomalhaut now has 3 same-paper JWST records (F1550C/F2300C/F2550W) — intended
  (three physically distinct belts/views at three wavelengths).
- hip-65426_jwst2023-f1140c reuses wavelength_um 11.4 like its mosaic sibling; if the
  slider dislikes duplicates, the mosaic sibling could be re-labeled to its NIRCam
  anchor (e.g. 4.4) — orchestrator's call, not done here.
- hl-tau_alma2015-b3/-b7 keep the sibling's dashed-tick panel frame style (source
  figure style, matches existing hl-tau_alma2015).
- Rendered helper views kept in images/_sources/_views/ as mine_* (dartts fig2 r300,
  hltau f2 r300, GL index sheets, gpies toti closeup, twhya f1 r300, ggtau inner).
