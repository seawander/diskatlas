# Sweep-2 report (2026-07-06)

## A) HD 34700 crop from 2310.16873 — DONE

**Paper verified from source tex + WebSearch — the placeholder was wrong:**

| field | placeholder said | actual (verified) |
|---|---|---|
| first_author | (TBD) | **Columba** (G. Columba et al.) |
| title | "HD 34700 disk imaging (VERIFY...)" | "Disk Evolution Study Through Imaging of Nearby Young Stars (DESTINYS): HD 34700 A unveils an inner ring" |
| facility/instrument | Subaru-SCExAO / CHARIS | **VLT-SPHERE / IRDIS DPI** (paper also uses ZIMPOL Ha, IFS, LBT/LMIRCam L', ALMA) |
| year/journal | 2023 / null | 2024, **A&A 681, A19**, bibcode 2024A&A...681A..19C |
| survey | null | DESTINYS |

- **image_id `hd-34700_scexao2023` is a MISNOMER** (it is a SPHERE/DESTINYS image, not SCExAO).
  Kept as-is per instructions so the pending record merges in place; rename would need
  a coordinated file+id change by the orchestrator.
- Crop: IRDIS H-band (BB_H 1.625 um) Qphi, log stretch — third panel of Fig. 2
  (`Figures/irdisQphi_log_coll.png`), the panel best showing the outer ring + the two
  logarithmic spiral arms. Title text and colorbar excluded (colorbar cols 398-413 cut),
  borders trimmed with `trim_borders.py`.
- Output: `images/hd-34700/hd-34700_scexao2023.png` (386x357 px, 116 KB). VIEWED — clean:
  ring, both spirals, coronagraph spot, 0.5" scale bar.
- Manifest: `backend/manifests/sweep2/s2-hd34700.json`; staging: `data/staging/s2-hd34700.json`
  (no `_verify` — metadata confirmed; staging wins over the placeholder on merge).
- NOT touched: `data/systems/hd-34700.json` (per concurrency protocol; merge_staging
  updates the record in place by image_id).

## B) Missing-nir gap sweep (12/12 WebSearches used, verified ids only)

Skipped up-front (coverage_todo.md does not list them as missing nir; confirmed in systems JSONs):
**49-cet** (has sphere-debris-2025 H-band), **hd-121617** (sphere-debris-2025 — the Perrot-era
SPHERE data is folded into that survey record), **hd-131488** (sphere-debris-2025; its dedicated
paper is arXiv 2311.03272, already covered), **dm-tau** (has sphere-taurus), **hd-107146**
(NICMOS 1.1 um done), **lkha-330** (SEEDS + Ks RDI done), **fomalhaut** (per instructions).

### New pending records appended (file: null, no crops)

| system | image_id | paper | arXiv / bibcode | notes |
|---|---|---|---|---|
| hd-95086 | `hd-95086_sphere2018` | Chauvin et al. 2018, A&A 617, A76 | 1801.05850 / 2018A&A...617A..76C | disk detected in polarized scattered light, faint, azimuthally averaged; `_verify` on instrument/band details |
| vega | `vega_hst2024` | Wolff et al. 2024, AJ | 2410.24042 | HST/STIS 32-orbit RDI; scattered-light halo 10.5-30 arcsec (0.58 um → counts as *opt*, no NIR image exists); `_verify` (AJ volume/bibcode unchecked) |
| aa-tau | `aa-tau_hst2013` | Cox et al. 2013, ApJ 762, 40 | none / 2013ApJ...762...40C | HST/STIS coronagraphy of disk+jet at optical minimum; **paper has no arXiv posting** — bibcode verified via ADS, so ADS link works; no `_verify` |

(Vega "HST Su" guess in the brief resolved to **Wolff et al. 2024** — companion to the
Su et al. JWST/MIRI paper 2410.23636 already ingested.)

### No-exists — "coverage: ..." notes appended

- **hd-21997** — no resolved scattered-light image (swept).
- **eta-crv** — none; HST ACS/NICMOS GO-10244 did not detect the disk (surface brightness too low).
- **hd-170773** — none found.
- **hd-202628** — no *near-IR* image (optical STIS + mm exist); flagged only as candidate for future SPHERE/GPI.
- **gj-14** — none found.
- **hd-22049 / eps Eri** — none, as predicted; HST/STIS deepest limits (arXiv 2408.06973)
  and SPHERE polarimetric monitoring are both non-detections.
- **hd-138813** — none found (not in the SPHERE debris characterization survey either).

All 10 edited part-B system JSONs bumped to last_updated 2026-07-06.
`backend/validate.py`: **0 errors** (new warns = intentional `_verify` flags on
hd-95086_sphere2018 and vega_hst2024).

### Follow-ups for orchestrator
1. Merge `data/staging/s2-hd34700.json` (fixes the (TBD)/SCExAO placeholder in place).
2. Optional: rename `hd-34700_scexao2023` → `hd-34700_sphere2023` (id + file) after merge.
3. Vega/AA Tau STIS figures would need host-fetch (2410.24042 tar; AA Tau via ADS/journal
   — no arXiv source exists) before any future crop.
4. Coverage audit note: vega and aa-tau still count "missing nir" (their new records are
   optical) — genuine, no NIR data published as of 2026-07.
