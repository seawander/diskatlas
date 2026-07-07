# Batch D report — imaged planets (discovery-image crops)

Agent: Batch D crop agent, 2026-07-06.
20 manifests in `backend/manifests/planets/`, 20 staging files `data/staging/pl-*.json`
(one record each, `survey` field = null via `survey_name: null`). All crops viewed and
verified: planet/companion visible (dot + arrow/circle/label) plus star and, where the
figure provides one, scale bar/compass. No `merge_staging.py`/`build.py` run (per protocol).

## Cropped (status ok)

| system | image_id | file | source fig | status |
|---|---|---|---|---|
| hr-8799 | hr-8799_keck2008 | images/hr-8799/hr-8799_keck2008.png | Marois+2008 Fig. 1 (bottom JHK panel; b,c,d labeled) | ok |
| hr-8799 | hr-8799_keck2010 | images/hr-8799/hr-8799_keck2010.png | Marois+2010 Fig. 1 (pdf p15, Nov 2009 L' panel; b,c,d,e) | ok |
| beta-pic | beta-pic_naco2010 | images/beta-pic/beta-pic_naco2010.png | Lagrange+2010 Fig. 1 (pdf p5, right/2009 panel) | ok |
| pds-70 | pds-70_sphere2018 | images/pds-70/pds-70_sphere2018.png | Keppler+2018 Fig. 9 (IRDIS H2H3 2015-05-03 panel) | ok |
| pds-70 | pds-70_muse2019 | images/pds-70/pds-70_muse2019.png | Haffert+2019 Fig. 2a (pdf p9, Halpha; b & c circled) | ok |
| 51-eri | 51-eri_gpi2015 | images/51-eri/51-eri_gpi2015.png | Macintosh+2015 Fig. 1 (pdf p14, GPI H panel, arrow) | ok |
| hip-65426 | hip-65426_sphere2017 | images/hip-65426/hip-65426_sphere2017.png | Chauvin+2017 Fig. 1 (right, IRDIS-H2H3) | ok |
| hip-65426 | hip-65426_jwst2023 | images/hip-65426/hip-65426_jwst2023.png | Carter+2023 Fig. 8 (all 7 NIRCam+MIRI filters) | ok |
| af-lep | af-lep_sphere2023 | images/af-lep/af-lep_sphere2023.png | Franson+2023 Fig. 1 (right, NIRC2 L' Feb 2023) | ok |
| hip-99770 | hip-99770_scexao2023 | images/hip-99770/hip-99770_scexao2023.png | Currie+2023 Fig. 1 panel A (planet circled) | ok |
| yses-1 | yses-1_sphere2020 | images/yses-1/yses-1_sphere2020.png | Bohn+2020 Fig. 1 (SPHERE/K1 panel; b & c arrowed) | ok |
| hd-95086 | hd-95086_naco2013 | images/hd-95086/hd-95086_naco2013.png | Rameau+2013 Fig. 1 (2012 sADI L' panel, arrow) | ok |
| gj-504 | gj-504_seeds2013 | images/gj-504/gj-504_seeds2013.png | Kuzuhara+2013 Fig. 5 panel b (annotated) | ok |
| kappa-and | kappa-and_seeds2013 | images/kappa-and/kappa-and_seeds2013.png | Carson+2013 Fig. 1 center panel (annotated) | ok |
| hd-106906 | hd-106906_mago2014 | images/hd-106906/hd-106906_mago2014.png | Bailey+2014 Fig. 1 (L'_Clio panel, circled) | ok |
| fomalhaut | fomalhaut_acs2008 | images/fomalhaut/fomalhaut_acs2008.png | Kalas+2008 Fig. 1 (belt + Fomalhaut b inset) | ok |
| ab-aur | ab-aur_scexao2022 | images/ab-aur/ab-aur_scexao2022.png | Currie+2022 Fig. 1 right (pdf p3, "Protoplanet AB Aur b") | ok |
| ct-cha | ct-cha_naco2008 | images/ct-cha/ct-cha_naco2008.png | Schmidt+2008 Fig. 1 (NACO Ks, companion labeled) | ok |
| gsc-6214-210 | gsc-6214-210_keck2011 | images/gsc-6214-210/gsc-6214-210_keck2011.png | Ireland+2011 Fig. 1 (Kp; companion at -2.2") | ok |
| roxs-42b | roxs-42b_keck2014 | images/roxs-42b/roxs-42b_keck2014.png | Currie+2014 Fig. 1 (NIRC2 H 2011 panel; "b" labeled) | ok |

## Skipped (with reasons)

| system | image_id | reason |
|---|---|---|
| 2m1207 | 2m1207_naco2004 | tarball astro-ph/0409323 not in images/_sources/arxiv/ (not yet downloaded) |
| twa-7 | twa-7_jwst2025 | tarball 2506.21857 not downloaded |
| gq-lup | gq-lup_naco2005 | tarball astro-ph/0503691 not downloaded |
| dh-tau | dh-tau_subaru2005 | tarball astro-ph/0411177 not downloaded |
| eps-ind-a | eps-ind-a_jwst2024 | **tarball 2407.15453.tar contains the WRONG paper** (a NeurIPS-2024 ML paper "Regression under demographic parity constraints..."); needs re-download on host |
| yses-2 | yses-2_sphere2021 | **seed had wrong arXiv id**: 2103.05657 = Swain+2021 "Detection of an Atmosphere on a Rocky Exoplanet" (GJ 1132 b). Correct Bohn+2021 YSES 2 id is **2104.08285** (seed fixed); correct tarball not downloaded yet |
| 1rxs-j1609 | 1rxs-j1609_gemini2008 | tarball 0809.1424 OK but the source contains **no image figure** — only f1.ps (spectra) and f2.ps (SED). Discovery image not recoverable from arXiv source; record stays file=null |
| 14-her | 14-her_jwst2025 | metadata-only task (step 7); no source download possible from sandbox |

## Seed fixes made (backend/seeds/planets.py)

- **AF Lep**: facility/instrument were wrong (VLT-SPHERE/IRDIS/H) → **Keck / NIRC2 / 3.8 um L'**;
  title corrected to "Astrometric Accelerations as Dynamical Beacons: A Giant Planet Imaged
  Inside the Debris Disk of the Young Star AF Lep" (verified from main.tex); bibcode added.
  NOTE: image_id suffix stays `sphere2023` (kept to update the existing placeholder record;
  cosmetically wrong — orchestrator may rename later if desired, in systems JSON + file + seeds together).
- **YSES-2**: arxiv 2103.05657 → **2104.08285**; bibcode 2021A&A...648A..73B; verify removed
  (journal/id are well-established; source itself unavailable).
- **14 Her c**: paper identified via WebSearch → arXiv **2506.09201**,
  "JWST Coronagraphic Images of 14 Her c: a Cold Giant Planet in a Dynamically Hot, Multi-planet System",
  Bardalez Gagliuffi et al. 2025, ApJL (DOI 10.3847/2041-8213/ade30f). Planet note fixed:
  ~250-300 K (the "26" figure circulating in press was degrees Fahrenheit, not Kelvin).
- verify=True removed after checking source .tex / first PDF page, with title/case fixes and
  bibcodes added for: Haffert 2019 (PDS 70), Carter 2023 (HIP 65426 JWST; "High-Contrast ... 2-16 um"),
  Rameau 2013 ("probable 4-5 Jupiter-mass exoplanet ... by direct-imaging"), Kuzuhara 2013,
  Carson 2013, Currie 2023 (HIP 99770), Bohn 2020, Currie 2022 (AB Aur), Schmidt 2008
  (title is "... around CT Cha", not "CT Chamaeleontis"), Lafreniere 2008 ("Planetary Mass",
  no hyphen), Ireland 2011 ("Planetary-Mass ... Solar-Type"), Currie 2014 (ROXs 42B),
  Matthews 2024 (eps Ind; fixed from public record since tarball is wrong).
- Metadata corrected to match the actual cropped panels: HR 8799 keck2008 label "JHK composite";
  GJ 504 "J/H composite"; kappa And "JHK composite"; YSES-1 wl 1.65→**2.1 (K1)** + technique
  coronagraphy; ROXs 42B wl 2.2→**1.65 (H band 2011 panel)**; GSC 6214-210 wl 2.1 "Kp band",
  technique "other" (plain AO imaging); CT Cha technique "other"; AB Aur instrument "CHARIS",
  technique "RDI" (crop is the Oct 2020 radius-scaled RDI panel).
- Still `verify=True` (sources unavailable, could not check): TWA 7 (Lagrange 2025 journal
  ref), GQ Lup (Neuhauser 2005), DH Tau (Itoh 2005).

## Ambiguities / decisions for the orchestrator

- **pds-70_sphere2018 kept `type: disk_scattered`** (as in the existing placeholder), NOT the
  batch default "planet": the crop (Keppler Fig. 9, H2H3 2015-05-03) shows disk + planet b, and
  flipping the type would leave PDS 70 without a scattered-light disk entry. Override if unwanted.
- hip-65426_jwst2023 crop is the full 7-filter gallery (Fig. 8), matching the record's
  "2-16 um" framing, rather than a single-filter stamp.
- beta-pic_naco2010 crop = the autumn-2009 (SW side) panel of Fig. 1, which carries the scale
  bar + compass; the 2003 epoch panel is the left half of the same figure if preferred.
- gj-504/kappa-and/yses-1 PNGs were palette-quantized (256 colors, dithered) to get under the
  ~300 KB guidance; visually checked, no noticeable degradation.
- New systems discovered from panels: **none** → no `data/coords_todo_batchD.txt` written.
- Missing/wrong tarballs to re-fetch on host: astro-ph/0409323, astro-ph/0503691,
  astro-ph/0411177, 2506.21857, 2104.08285, and re-download of 2407.15453 (current tar is a
  mismatched ML paper). 2506.09201 (14 Her c) also worth adding to the fetch list.
- `images/_sources/_views/batchD_*` holds all intermediate previews (also used as manifest
  sources for the EPS-based figures — do not delete without re-running manifests).
