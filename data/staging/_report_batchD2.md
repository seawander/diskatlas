# Batch D2 report — imaged-planet follow-up crops (old-style astro-ph tarballs)

Agent: Batch D follow-up crop agent, 2026-07-06.
3 manifests in `backend/manifests/planets/` (2m1207.json, gqlup.json, dhtau.json),
3 staging files `data/staging/pl2-*.json` (one record each; record `survey` = null via
`survey_name: null`). All 3 crops viewed and verified. No `merge_staging.py`/`build.py`
run (per concurrency protocol). No new systems discovered (no coords_todo entries).

## Cropped (status ok)

| system | image_id | file | source fig | status |
|---|---|---|---|---|
| 2m1207 | 2m1207_naco2004 | images/2m1207/2m1207_naco2004.png | Chauvin+2004 Fig. 1 (`Gg222_fig1.eps`, full frame): H/Ks/L' color composite; brown dwarf bright blue-white at center, companion b = red dot to the E (lower-left), "778 mas / 55 AU at 70 pc" arrow, N-E compass | ok |
| gq-lup | gq-lup_naco2005 | images/gq-lup/gq-lup_naco2005.png | Neuhauser+2005 Fig. 1 (`Gj061_f1.ps`, full-page render; figure box cropped at frac [0.119,0.105,0.877,0.640]): "VLT-NaCo K-band", GQ Lup A saturated PSF center, companion "b" tick-marked 0.73" W, 0.3" scale bar, N-E compass | ok |
| dh-tau | dh-tau_subaru2005 | images/dh-tau/dh-tau_subaru2005.png | Itoh+2005 Fig. 1 (`f1.eps`, full-page render; figure box cropped at frac [0.024,0.496,0.902,0.983]): K-band coronagraphic image, DH Tau A occulted at center, DH Tau B bright dot 2.34" SE (lower-left), 2"/280 AU scale bar | ok |

Rasterization: ghostscript `gs -r200 -dEPSCrop -sDEVICE=png16m` (EPS/PS sources);
page previews kept in `images/_sources/_views/batchD2_*.png`.

## Metadata fixes (staging + backend/seeds/planets.py)

- **2M1207 / 2m1207_naco2004** — Fig. 1 is a color COMPOSITE of H (blue), Ks (green),
  L' (red), per the caption; and the observation used NACO IR wavefront sensing
  (N90C10 dichroic), direct AO imaging — no coronagraph.
  - wavelength_label: "K band; ..." -> "H+Ks+L' composite; first image of a planetary-mass companion"
    (wavelength_um kept at 2.2 = Ks, the representative middle band).
  - technique: "coronagraphy" -> "other".
  - Paper metadata already verified (bibcode 2004A&A...425L..29C); tex title matches.
- **GQ Lup / gq-lup_naco2005** — obs = NACO S13 Ks-band jitter imaging, shift+add
  ("direct K-band imaging", no coronagraph; Subaru/CIAO coronagraphy in the paper is
  archival 2nd-epoch data only).
  - technique: "coronagraphy" -> "other"; wavelength_label "K band" -> "Ks band" (2.2 um kept).
  - `verify` CLEARED: title confirmed from `Gj061.tex` ("Evidence for a co-moving
    sub-stellar companion of GQ Lup"), arXiv id from tarball, `aa` documentclass
    consistent with A&A 435, L13; bibcode added: **2005A&A...435L..13N**.
- **DH Tau / dh-tau_subaru2005** — seeded values CORRECT (Subaru/CIAO, K band 2.2 um,
  coronagraphy — occulting-mask observation confirmed in `ms.tex` and Fig. 1 caption).
  - `verify` CLEARED: title confirmed from `ms.tex` ("A Young Brown Dwarf Companion to
    DH Tauri"), arXiv id from tarball, aastex class consistent with ApJ 620, 984;
    bibcode added: **2005ApJ...620..984I**.

## Notes for the orchestrator

- `data/systems/gq-lup.json` and `data/systems/dh-tau.json` still carry the old
  `_verify: true` + `bibcode: null` and the old technique/label values; NOT edited here
  (protocol). Merging `pl2-gq-lup.json` / `pl2-dh-tau.json` / `pl2-2m1207.json` will bring
  in the corrected fields; please make sure merge replaces technique/wavelength_label/paper
  on the existing placeholder records (image_ids match: 2m1207_naco2004, gq-lup_naco2005,
  dh-tau_subaru2005), or re-run make_systems from the fixed seeds.
- Side observation (no action taken): Itoh+2005 itself derives 30-50 MJup for DH Tau B;
  the systems-JSON planet note "~11 MJup wide companion" reflects later re-analyses, so it
  was left alone.
