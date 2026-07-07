# Batch A report — ALMA protoplanetary crops

Date: 2026-07-06. Scope: exoALMA IV, Long+2018, Long+2019, ODISEA III, 12 single-target papers.
All crops visually verified against in-panel labels (contact sheets in `images/_sources/_views/`).

## Staged files (do NOT re-run; ready for merge_staging.py)

| staging file | records | notes |
|---|---|---|
| `exoalma.json` | 15 | fills existing `<id>_exoalma` records (file was null) |
| `taurus-long2018.json` | 12 | fills existing `<id>_taurus-long2018` records |
| `taurus-long2019.json` | 20 | 5 fill existing records; 6 append to existing systems; 9 create new systems |
| `odisea.json` | 10 | doar-44 appends; 9 create new systems |
| `single-*.json` (10) | 10 | fill existing single-paper records (survey stays null) |

## Crop table

### exoALMA (2504.18725, Curone+2025 Fig. 1; 0.9 mm, Band 7) — 3x5 grid, alphabetical
aa-tau, cq-tau, dm-tau, hd-135344b, hd-143006, hd-34282, rx-j1604-3-2130 (panel "J1604"),
rx-j1615-3-3255 ("J1615"), rx-j1842-9-3532 ("J1842"), rx-j1852-3-3700 ("J1852"), lkca-15,
mwc-758, pds-66, sy-cha, v4046-sgr — image_id `<id>_exoalma`. All 15 verified.

### Taurus-Long2018 (1810.06044, Long+2018 Fig. 1; 1.33 mm) — 2x6, decreasing flux
mwc-480, ry-tau, dl-tau, ci-tau, uz-tau-e, ft-tau, dn-tau, iq-tau, go-tau, cida-9, ds-tau,
ip-tau — image_id `<id>_taurus-long2018`. All 12 verified.

### Taurus-Long2019 (1906.10809, Long+2019 Fig. 3; 1.33 mm) — 4x8 mosaic
Cropped only the 20 compact/smooth disks (panels 13–32); panels 1–12 duplicate Long2018.
Row2(5-8): bp-tau, v409-tau, dr-tau, ho-tau*; Row3: haro-6-13*, do-tau, dq-tau, gi-tau,
v836-tau, hq-tau, hp-tau*, gk-tau*; Row4 (binaries): v710-tau, hk-tau*, dh-tau, t-tau*,
hn-tau*, rw-aur, dk-tau*, uy-aur* — image_id `<id>_taurus-long2019`. (*) = new system.
All 20 verified. Binary panels (T Tau, UY Aur) naturally show the faint companion too.

### ODISEA (2012.00189, Cieza+2021 ODISEA III Fig. 3; 1.3 mm) — 2x5, blue-framed panels
iso-oph-54*, wly-2-63*, iso-oph-37*, iso-oph-17*, doar-44, wsb-82*, iso-oph-2*,
iso-oph-196*, sr-24s* (panel "EM* SR 24S"), rx-j1633-9-2442* — image_id `<id>_odisea`.
All 10 verified. ISO-Oph 2 panel includes the paper's own inset with the 2B companion disk.

### Singles (existing image_ids, file was null -> now filled)

| system | image_id | source figure | crop |
|---|---|---|---|
| hl-tau | hl-tau_alma2015 | 1503.02649 f2.eps (gs->PNG in `_views/hltau_f2.png`) | Fig. 2e, B6+B7 1.0 mm iconic image |
| tw-hya | tw-hya_alma2016 | 1603.09352 f1.pdf | Fig. 1 (870 um + 1-au-gap inset) |
| pds-70 | pds-70_alma2021 | 2108.07123 FIG/LB1_SB1...annotations.pdf | Fig. 1 right, annotated (CPD around c) |
| ab-aur | ab-aur_alma2017 | 1704.02699 4p-obs.pdf | Fig. 1b (1.3 mm contours + 12CO M0 spirals) |
| hd-142527 | hd-142527_alma2013 | 1305.6062 summary_cycle0_main_v1.pdf | Fig. 1a (horseshoe + filament inset) |
| oph-irs-48 | oph-irs-48_alma2013 | 1306.1768 full PDF p.7 | Fig. 1A (0.44 mm dust trap) |
| hd-169142 | hd-169142_alma2017 | 1702.02844 fig_hd169142_cont.jpg | Fig. 1 left (1.3 mm rings) |
| mwc-758 | mwc-758_alma2018 | 1805.12141 plot_image.pdf | Fig. 1a (0.87 mm) |
| elias-27 | elias-27_alma2016 | 1610.05139 Elias2-27_withUnsharpMasking_color.pdf | Fig. 1A (spirals) |
| gm-aur | gm-aur_alma2020 | 2001.11040 continuumoverview.pdf | Fig. 1 top-left (Band 6 1.1 mm); re-cropped at 480 px to stay <300 KB |

## New systems (auto-created by merge_staging; SIMBAD names in `data/coords_todo_batchA.txt`)

| system_id | SIMBAD | region | category | notes |
|---|---|---|---|---|
| ho-tau | HO Tau | Taurus | protoplanetary | Long19 smooth single |
| haro-6-13 | Haro 6-13 | Taurus | protoplanetary | = V806 Tau |
| hp-tau | HP Tau | Taurus | protoplanetary | |
| gk-tau | GK Tau | Taurus | protoplanetary | |
| hk-tau | HK Tau | Taurus | protoplanetary | binary |
| t-tau | T Tau | Taurus | protoplanetary | triple; panel shows N + faint S |
| hn-tau | HN Tau | Taurus | protoplanetary | binary |
| dk-tau | DK Tau | Taurus | protoplanetary | binary |
| uy-aur | UY Aur | Taurus (Auriga) | protoplanetary | binary; both components in panel |
| iso-oph-54 | ISO-Oph 54 | Ophiuchus | protoplanetary | Class I; no Gaia — coords in todo file |
| wly-2-63 | WLY 2-63 | Ophiuchus | protoplanetary | = IRS 63, flat-spectrum |
| iso-oph-37 | ISO-Oph 37 | Ophiuchus | protoplanetary | flat-spectrum |
| iso-oph-17 | ISO-Oph 17 | Ophiuchus | protoplanetary | |
| wsb-82 | WSB 82 | Ophiuchus | protoplanetary | |
| iso-oph-2 | ISO-Oph 2 | Ophiuchus | protoplanetary | binary, 2.2 au cavity |
| iso-oph-196 | ISO-Oph 196 | Ophiuchus | protoplanetary | |
| sr-24s | EM* SR 24S | Ophiuchus | protoplanetary | S component of SR 24 |
| rx-j1633-9-2442 | RX J1633.9-2442 | Ophiuchus | protoplanetary | transition disk |

The seed file (`backend/seeds/alma_proto.py`) now carries all of these as survey members
(Taurus-Long2019 = 20, ODISEA = 10), so the next `make_systems.py` run fills names/regions.

## Seed metadata fixes (backend/seeds/alma_proto.py)

- ODISEA paper: title was wrong; fixed from ms.tex to "...(ODISEA) - III: the evolution of
  substructures in massive discs at 3-5 au resolution"; added bibcode 2021MNRAS.501.2934C; _verify dropped.
- HD 169142 Fedele+2017: title fixed from hd169142.tex ("ALMA unveils rings and gaps ...
  signatures of two giant protoplanets"); _verify dropped.
- GM Aur Huang+2020: bibcode 2020ApJ...891...48H added (doi in exoALMA .bbl); _verify dropped.
- HL Tau image metadata: now matches the cropped panel — Bands 6+7, 1000 um,
  "1.0 mm continuum (B6+B7 combined...)" (was Bands 3/6/7 / 1300 um).
- Verified & de-flagged (_verify) from local sources: AB Aur Tang+2017 (title in b6ms-v1.tex),
  IRS 48 van der Marel+2013 (SI cover: Science 340, 1199, 2013 + "IRS 48 a.k.a. WLY 2-48"),
  MWC 758 Dong+2018, Elias 27 Perez+2016 (scifile.tex), HD 142527 Casassus+2013 (see problems).

## Problems / follow-ups for the orchestrator

1. **HD 100546 (Walsh+2014): wrong arXiv id in seeds.** Tarball 1403.0121 is an unrelated
   Agundez hot-Jupiter chemistry paper. Set arxiv=None, bibcode=2014ApJ...791L...6W
   (confirmed via a .bbl). `hd-100546_alma2014` file stays null. TODO: find true arXiv id
   (likely 1406.6060 — VERIFY), fetch source, crop. `_verify` kept (title unconfirmed).
2. **V1247 Ori (Kraus+2017): wrong arXiv id in seeds.** Tarball 1709.02068 is a
   particle-physics paper. Correct id **1710.05028** recovered from a bib Eprint field
   (exact title + ApJ 848 match) and fixed in seeds. Source not on disk ->
   `v1247-ori_alma2017` file stays null. TODO: host-fetch 1710.05028, then crop.
3. **exoALMA I (2504.18688) `_verify` left in place** — that source was not downloaded, and
   the exoALMA IV .bbl cites sibling exoALMA papers as "ApJL, TBD" (preprint stage), so
   journal details could not be confirmed locally.
4. HD 142527 Casassus+2013: the arXiv tex draft title is "Observations of gas flows inside
   a protoplanetary gap"; kept the published Nature title "Flows of gas through a
   protoplanetary gap" (Nature 493, 191; content/target verified). 
5. Journal strings kept on memory (not locally verifiable, low risk): Tang ApJ 840, 32;
   Dong ApJ 860, 124; Fedele A&A 600, A72; Kraus ApJL 848, L11; Cieza MNRAS 501, 2934.
6. ingestion_status.json not touched (orchestrator merges): exoALMA/Long18/Long19/ODISEA
   images -> done; singles done except hd-100546 + v1247-ori (pending sources).
7. `images/_sources/_views/` now contains the rasterized pages/contact sheets used for QA,
   including `hltau_f2.png` which is REFERENCED by `backend/manifests/alma-proto/single-hltau.json`
   (crop_panels cannot read EPS) — do not delete it.
