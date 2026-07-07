# Batch C2 report — scattered-light singles follow-up (old-style arXiv tarballs)

Agent: Batch C follow-up (fresh agent, brief re-read). 12 image records staged from
11 papers; ALL crops visually verified. No merge/build run; no data/systems edits.
All 11 requested tarballs were present (including every "[if present]" one).

## 1. Crops produced (manifests backend/manifests/scattered/c2-*.json, survey_name null)

| staging file | image_id | source figure | notes |
|---|---|---|---|
| c2-fomalhaut-acs2005 | fomalhaut_acs2005 | astro-ph_0506574.pdf p1, Fig. 1a | belt + Q1-Q4 labels + 2" bar |
| c2-kalas06-acs2006 | hd-53143_acs2006 | f1.eps panel (a) | ACS/HRC F606W |
| c2-kalas06-acs2006 | hd-139664_acs2006 | f1.eps panel (b) | edge-on ansae |
| c2-hd181327-nicmos2006 | hd-181327_nicmos2006 | f2_100gs.eps panel A | NICMOS 1.1 um combined image; small black inset bottom-right is IN the published EPS |
| c2-hr4796a-nicmos1999 | hr-4796a_nicmos1999 | FIGURE1_HR4796_RESUBMIT.ps panel b | see Section 3 (panel a is 1.6 um!) |
| c2-hd15115-hst2007 | hd-15115_hst2007 | f1.eps LEFT | ACS F606W blue needle (right half = Keck H, not used) |
| c2-hr4796a-gpi2015 | hr-4796a_gpi2015 | f8.jpg row 2 col 3 | K1 2013-Dec polarized intensity |
| c2-betapic-gpi2015 | beta-pic_gpi2015 | figure1.png left | Q_r H-band |
| c2-hd97048-sphere2016 | hd-97048_sphere2016 | hd97048_main_6.pdf row 1 col 3 | J Qphi r^2-scaled (rings visible) |
| c2-hd61005-sphere2016 | hd-61005_sphere2016 | all_data.pdf top-left | IRDIS ADI H (matches seeded ADI technique) |
| c2-hd100453-sphere2017 | hd-100453_sphere2017 | HD100453SPHEREIRDISQphiUphiv2.pdf left | J Qphi, two spirals |
| c2-lkca15-2014 | lkca-15_seeds2014 | methods_ann.eps panel (a) | NIRI Ks "PCA RefSub" |

EPS/PS sources rasterized to images/_sources/_views/c2_*.png (kept for reproducibility);
PDF/JPG/PNG sources cropped directly.

## 2. Metadata corrections carried in staging records (merge will fold into data/systems)

- **hr-4796a_gpi2015**: wavelength 1.65 -> **2.05 um**. All HR 4796A pol data in
  Perrin+2015 are K1 band (label already said "K1 pol."; the um value was H-band).
- **hd-97048_sphere2016**: 1.65 H -> **1.25 um J**, instrument IRDIS -> IRDIS DPI.
  Ginski+2016 DPI data are J band (figure label "SPHERE/DPI/J"; ADI was H2H3).
- **hd-100453_sphere2017**: 1.65 H -> **1.25 um J**, instrument IRDIS -> IRDIS DPI.
  Benisty+2017 NIR pol is IRDIS J (plus ZIMPOL R'/I'); there is no H-band image.
- **lkca-15_seeds2014**: Subaru-HiCIAO/HiCIAO/1.65 H/PDI -> **Gemini-NIRI / NIRI /
  2.15 um Ks / RDI** ("PCA-assisted reference PSF subtraction", Fig. 2a). Thalmann+2014's
  own imaging is Gemini NIRI Ks (epochs K1-K4); the HiCIAO H data are re-used from
  Thalmann+2010. image_id kept as `lkca-15_seeds2014` per instructions — it is now a
  misnomer; rename to `lkca-15_niri2014` would need a coordinated systems+file rename
  (orchestrator's call, optional).
- **fomalhaut_acs2005**: 0.6 -> **0.7 um**, label "optical (F606W+F814W); eccentric ring".
  Methods: primary data F814W (833 nm, ~80 min) + F606W follow-up, combined for the
  belt image.
- **hd-15115_hst2007** label -> "optical (F606W); ...". hd-61005 label -> "H band (ADI); ...".
- Bibcodes added everywhere (Kalas06 = 2006ApJ...637L..57K, Schneider06 =
  2006ApJ...650..414S, Kalas07 = 2007ApJ...661L..85K, Millar-Blanchaer15 =
  2015ApJ...811...18M, Ginski16 = 2016A&A...595A.112G, Olofsson16 = 2016A&A...591A.108O,
  Benisty17 = 2017A&A...597A..42B, Thalmann14 = 2014A&A...566A..51T). These are from
  agent knowledge of the published records (volume/page all match the local sources'
  journal refs); spot-checkable via ADS if desired.
- Staging paper dicts replace the seeds' `_verify` versions wholesale on merge, so the
  flags disappear from data/systems automatically for all 12 records.

## 3. HR 4796A NICMOS 1999 — panel-band gotcha

Figure 1 caption (tex, FIGURE CAPTIONS section): "Images a&c: 1.6 um (F160W), 15 March
1998. Images b&d: 1.1 um (F110W), 16 August 1998." The obvious crop (panel a) is the
WRONG band for the seeded 1.1 um record; I cropped **panel b** (F110W 1.1 um, the
higher-S/N epoch per the text). First cropped a, then re-cropped after reading the caption.

## 4. Seed edits (backend/seeds/scattered.py)

- verify=True cleared + bibcode added for the 9 cropped papers that had flags
  (Kalas06 x2, Schneider06, Schneider99, Kalas07, Millar-Blanchaer15, Ginski16,
  Olofsson16, Benisty17, Thalmann14) — titles confirmed from local arXiv sources.
- Wavelength/instrument fixes mirrored into seeds (HR 4796A gpi2015 K1 2.05; HD 97048 J;
  HD 100453 J; LkCa 15 NIRI Ks RDI; Fomalhaut 0.7 um).
- Bonus (title-grep only, no crops): verify cleared + bibcodes for **tw-hya_stis2013**
  (Debes 2013, full title with "...Detection of a Partially Filled Disk Gap at 80 AU",
  2013ApJ...771...45D), **hd-106906_gpi2015** (Kalas 2015, 2015ApJ...814...32K),
  **rx-j1604_seeds2012** (Mayama 2012, 2012ApJ...760L..26M) — their sources are in
  images/_sources/extracted/ and titles match.
- Still `_verify` (8; no local source): AU Mic acs2005 + sphere2015, HD 141569 acs2003,
  TWA 7 stis2021 (wrong arXiv id, see batch C report), HD 110058 sphere2023 (same),
  HD 32297 stis2005, HD 163296 stis2000, HD 100546 acs2007 (placeholder title is
  self-evidently wrong — needs the real Ardila+2007 reference).

## 5. Orchestrator actions

1. Run merge_staging (12 records, c2-*.json) then validate/build as usual. All 12
   target ids already exist in data/systems; no new systems, no coords needed
   (no data/coords_todo file written).
2. NOTE for data/systems consistency: the seed-side `_verify` flags for the three
   "bonus" verifications (Section 4) are cleared in seeds only — their records in
   data/systems/{tw-hya,hd-106906,rx-j1604-3-2130}.json still carry `_verify: true`
   + bibcode null since no staging record touches them. Either hand-clear or wait for
   their future crops.
3. ingestion_status: scattered singles can move closer to "done" — remaining un-cropped
   Batch C singles are now only: TW Hya STIS 2013 (source present, crop pending),
   HD 106906 GPI 2015 (source present), RX J1604 SEEDS 2012 (source present),
   AU Mic ACS/SPHERE (no arXiv sources), HD 32297 STIS 2005, HD 163296 STIS 2000,
   HD 100546 ACS 2007, HD 141569 ACS 2003 (no arXiv ids), TWA 7 + HD 110058
   (wrong ids, need WebSearch).
