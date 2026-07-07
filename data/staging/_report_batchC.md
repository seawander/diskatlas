# Batch C report — scattered-light disk crops

Agent: Batch C (scattered light). 127 image records staged, all crops visually verified
(>=3 outputs per gallery; all outputs for small sets/singles). No merge/build run.

## 1. Crops produced (staging file -> records)

| Survey / set | arXiv | Source figure | Records | image_id pattern |
|---|---|---|---|---|
| GPIES debris Qphi | 2004.13722 | Fig. 5 gallery (5x5, 24 panels) | 24 | `<id>_gpies-debris` |
| GPIES debris totI | 2004.13722 | Fig. 6 gallery (r1c3, r4c3) | 2 (hd-15115, nz-lup) | `<id>_gpies-debris` |
| GPIES proto | 2004.13722 | Fig. 9 (Qphi row) | 3 (ak-sco, hd-100546, hd-141569) | `<id>_gpies` |
| DARTTS-S | 1803.10882 | Fig. 1 (8 panels) | 8 | `<id>_dartts-s` |
| SPHERE-Taurus | 2403.02158 | Fig. 2 "Imagery" mosaic (43 panels) | 32 (28 H + 2 J + 2 K) | `<id>_sphere-taurus` |
| STIS-Schneider14 | 1406.7303 | per-target figs (composite of pp. 49-102) | 11 (10 debris + pds-66) | `<id>_stis-schneider14` |
| Gemini-LIGHTS | 2206.05815 | Spirals/Rings/Continuous/Irregulars montages | 22 | `<id>_gemini-lights` |
| SPHERE-Ks-RDI | 2310.08589 | fig-K_Total-good (3x6, 18 panels) | 15 | `<id>_sphere-ks-rdi` |
| Singles (10) | see below | one manifest each | 10 | seeded image_ids |

Singles cropped (existing image records completed): `hr-4796a_stis2018` (1712.08599 Fig 8L),
`ab-aur_sphere2020` (2005.09064 Fig 1a), `ab-aur_seeds2011` (1102.4408 Fig 1L),
`gg-tau_sphere2020` (2005.09037 no_features_log), `su-aur_sphere2021` (2102.08781 SPHERE Qphi),
`hd-34700_gpi2019` (1901.02467 Fig 2 H), `tw-hya_sphere2017` (1610.08939 Fig 2 H-Qphi),
`mwc-758_sphere2015` (1505.05325 Mar-2015 PI), `hd-135344b_seeds2012` (1202.6139 Fig 2 zoom),
`hd-202628_stis2012` (1206.2078 Fig 3).

GPIES Qphi panel-label -> id mapping of note: `CE Ant` = TWA 7 (confirmed in tex) -> twa-7;
`HR 4796 A*` -> hr-4796a; `HR 7012` (= HD 172555) -> hr-7012 (new). HD 15115 + NZ Lup are the
two total-intensity-only GPIES detections (their records carry instrument "IFS", technique
"ADI", label "total intensity" — hd-15115's pre-seeded PDI metadata is corrected by staging).

Gemini-LIGHTS label mapping: `MWC 275` -> hd-163296, `CU Cha` -> hd-97048, `MWC 863` = HD 150193
(undetermined category, NOT cropped). Ks-RDI label `SAO 206462` -> hd-135344b; multi-epoch
targets: MWC 758 -> epoch (s)'' 2020-12-26, SZ Cha -> epoch (x)' 2020-12-30.

## 2. New systems (auto-created shells; SIMBAD names in data/coords_todo_batchC.txt)

29 new systems. Suggested categories/region:

| id | SIMBAD | cat. | region / note |
|---|---|---|---|
| hd-111161 | HD 111161 | debris | LCC (Sco-Cen); ALMA-selected GPIES addition |
| hr-7012 | HR 7012 | debris | beta Pic MG; = HD 172555; tiny r~12 au ring |
| nz-lup | NZ Lup | debris | field (no MG in GPIES table); totI-only detection |
| ak-sco | AK Sco | protoplanetary | UCL (Sco-Cen); circumbinary; also Gemini-LIGHTS |
| doar-44 | DoAr 44 | protoplanetary | Ophiuchus |
| rw-aur, dg-tau, ux-tau, v409-tau, v710-tau, cy-tau, cx-tau, gi-tau, de-tau, v836-tau, cw-tau | same, spaced | protoplanetary | Taurus (Garufi+2024 census) |
| hd-15745 | HD 15745 | debris | field F2V, 63.5 pc, ~100 Myr |
| hd-45677 | HD 45677 | protoplanetary | FS CMa B[e], isolated |
| hd-50138 | HD 50138 | protoplanetary | B[e], isolated |
| hd-145718 | HD 145718 | protoplanetary | Upper Sco |
| mwc-297 | MWC 297 | protoplanetary | massive Herbig Be, Aquila |
| mwc-614 | MWC 614 | protoplanetary | isolated Herbig |
| mwc-789 | MWC 789 | protoplanetary | isolated Herbig |
| fu-ori | FU Ori | protoplanetary | FUor prototype, Orion |
| gw-ori | GW Ori | protoplanetary | circumtriple disk, Orion |
| hen-3-365 | Hen 3-365 | protoplanetary | B[e]/Herbig |
| lkha-330 | LkHa 330 | protoplanetary | Perseus |
| pds-201 | PDS 201 | protoplanetary | = V351 Ori, Orion |
| sz-cha | SZ Cha | protoplanetary | Chamaeleon I |

## 3. Membership findings / seed edits (backend/seeds/scattered.py)

- **GPIES-debris**: completed to the full 26 (added TWA 7 [CE Ant], HD 111161, HR 7012, NZ Lup).
  New small `GPIES` survey block for the 3 PPDs (AK Sco, HD 100546, HD 141569).
- **DARTTS-S**: completed 8/8. The 3 targets missing from seeds were **RX J1615.3-3255**
  (existing system rx-j1615-3-3255), **DoAr 44** (new), **AS 209** (existing as-209).
- **SPHERE-Taurus**: 32 detected members (of 43 observed) per Fig. 2 + Table C.1 (r_out
  measurable). Excluded (ambient-dominated or formally undetected): T Tau, XZ Tau, UY Aur,
  RY Tau, HP Tau, HN Tau, DS Tau, GK Tau, DK Tau, V807 Tau, V1025 Tau. Bands: H for all
  except CQ Tau + LkCa 15 (J) and MWC 758 + CY Tau (K) — member overrides added.
  Panel "UZ Tau" mapped to existing uz-tau-e (disk is around UZ Tau E).
- **STIS-Schneider14**: true sample (Table 1) = HD 15115, HD 15745, HD 32297, HD 53143,
  HD 61005, HD 92945, HD 107146, HD 139664, HD 181327, AU Mic (+ MP Mus = PDS 66 as the
  11th, protoplanetary, imaged via staging). **HD 191089 was wrongly seeded — removed.**
- **Gemini-LIGHTS**: 22 resolved detections seeded (spirals 4 / rings 7 / continuous 11 /
  irregulars 4, minus cross-category duplicates HD 34700A, HD 142527, HD 100453, HD 139614).
  **HD 135344B and MWC 758 are NOT in the Rich+2022 sample — removed from members.**
  HD 150193 (= MWC 863) is in the sample but "undetermined" (unresolved) — removed too.
  The 13 undetermined + 9 non-detections were not cropped.
- **SPHERE-Ks-RDI**: 15 members from the "good" total-intensity gallery; paper metadata
  verified from ms.tex (Bin Ren; bibcode 2023A&A...680A.114R added; _verify cleared).
- `_verify` cleared after checking titles in local arXiv sources for: tw-hya_sphere2017
  (also corrected to H band / 1.62 um Qphi; old seed said ZIMPOL 1.25), ab-aur_seeds2011,
  ab-aur_sphere2020, gg-tau_sphere2020 (title is "Gap, shadows, spirals, and streamers ...
  GG Tau A"), su-aur_sphere2021, hd-34700_gpi2019, mwc-758_sphere2015, hd-135344b_seeds2012
  (full two-clause title), hd-202628_stis2012.

## 4. Wrong arXiv ids discovered (downloads are unrelated papers)

- **twa-7_stis2021 (Ren+2021)**: 2104.10620 is a graphene/STM condensed-matter paper.
  Seed arxiv set to None, verify kept. SKIPPED crop. (TWA 7 still got twa-7_gpies-debris.)
- **hd-110058_sphere2023 (Stasevic+2023)**: 2309.01035 is an AAAI-24 machine-learning paper.
  Seed arxiv set to None, verify kept. SKIPPED crop.
  -> Orchestrator: find correct ids (WebSearch), refetch, crop later.

## 5. Actions needed from orchestrator (cannot touch data/systems myself)

1. Delete stale image records: `hd-191089_stis-schneider14` (target not in Schneider+2014),
   `hd-135344b_gemini-lights`, `mwc-758_gemini-lights` (targets not in Rich+2022),
   `hd-150193_gemini-lights` (undetermined/unresolved only; or keep as metadata-only
   with file:null and a note — my recommendation is delete).
2. SIMBAD coords for the 29 new systems (data/coords_todo_batchC.txt) + fill shells'
   categories/regions per table above (incl. planets: none known for these).
3. Correct arXiv ids for TWA 7 Ren+2021 and HD 110058 Stasevic+2023 (Section 4).
4. data/ingestion_status.json: images "done" for gpies-debris, dartts-s, sphere-taurus,
   stis-schneider14, gemini-lights, sphere-ks-rdi; "partial" for scattered singles
   (2 skipped, see Section 4 + 6).
5. The truncated file images/_sources/extracted/2104.10620/2104.10620.pdf should be
   re-extracted (its .tar in _sources/arxiv is the complete PDF) — moot if the id is
   replaced per (3).

## 6. Skipped / not attempted (and why)

- twa-7_stis2021, hd-110058_sphere2023 crops — wrong-source arXiv ids (Section 4).
- Gemini-LIGHTS "undetermined" (13) and non-detections (9) — per "detections only".
- Garufi+2024 non-/ambient-detections (11) — per "detections only".
- Ks-RDI Qphi gallery — only the total-intensity "good" gallery cropped (matches the
  seeded RDI image defaults); duplicate epochs (MWC 758 x3, SZ Cha x2) cropped once.
- Other Batch C singles that remain metadata-only (file:null) and were not in my priority
  list: 1407.2495 (HR 4796A GPI 2015), 1508.04787 (beta Pic GPI), 1510.02747 (HD 106906
  GPI), 1601.07861 (HD 61005 SPHERE), 1609.04027 (HD 97048 SPHERE), 1610.10089
  (HD 100453 SPHERE), 0704.0645 (HD 15115 ACS), 1306.2969 (TW Hya STIS 2013), 1402.1766
  (LkCa 15 SEEDS), 1211.3284 (RX J1604 SEEDS), astro-ph singles (Fomalhaut ACS, AU Mic
  ACS, HD 53143/HD 139664 ACS, HD 181327 NICMOS, HR 4796A NICMOS, HD 32297 STIS 2005,
  HD 163296 STIS, HD 100546 ACS) — sources are extracted and ready for a follow-up pass.

## 7. Manifests written (backend/manifests/scattered/)

gpies-debris, gpies-debris-toti, gpies-proto, dartts-s, sphere-taurus, sphere-taurus-j,
sphere-taurus-k, stis-schneider14 (uses composite images/_sources/_views/stis_s14_composite.png),
gemini-lights-{spirals,rings,continuous,irregulars}-{j,h} (7 files), sphere-ks-rdi,
single-* (10 files). Intermediate rasterizations live in images/_sources/_views/.
