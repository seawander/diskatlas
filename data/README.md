# data/ — the database

One JSON file per stellar system in `data/systems/<system_id>.json`.
`frontend/data.js` is compiled from these by `backend-data/build.py`. **Edit here, never edit data.js.**


**Optional `epoch` field** (on image records): the **observation** date — the date the data were *taken*, NOT the publication year. Precision is honest per record: `YYYY-MM-DD` / `YYYY Mon DD` when the executions cluster within ~45 days, `YYYY` when they span one calendar year, `YYYY-YYYY` when a published image combines executions across years. Sources, in priority order: (1) the record's own paper — observing-log table rows matched by target alias and instrument (`backend-data/epoch_harvest.py tex` + curated `backend-data/epoch_picks.py`); (2) observatory archives queried by position/instrument/band and bounded by the paper date — ALMA TAP, MAST (HST+JWST), ESO TAP (`backend-data/epoch_archives.py`). Every recovered epoch's origin and evidence snippet is recorded in `data/paper_finder/epoch_provenance.json`; `backend-data/epoch_audit.py` reports coverage. The viewer shows the observation-epoch year as a **bare** year on each detail-card chip (tooltip gives the full date); where the obs epoch is not yet recovered it shows the publication year in **parentheses** instead — so the two are never conflated and duplicate band+instrument labels stay distinguishable.

## Inclusion / resolution criterion

A record earns a place only if it is a **spatially resolved image** or a **direct/interferometric
companion detection** (or a coronagraphic quasar-host image). Numeric bar for *disk* records: the
disk structure must span **≥ 3 resolution elements** (synthesized beams, or PSF/diffraction-limit
FWHMs) along at least one axis in the published image — i.e. resolved structure, not an unresolved
blob. **Companion records** (`type: "planet"`) are point-source *detections*; they need not be
spatially resolved, but must be a genuine imaging/interferometric detection (not a transit light
curve, RV curve, SED, or photometry — those are out of scope). This bar is enforced at ingestion
by the mandatory VIEW-verify step; there is no stored per-record beam/PSF size, so marginal cases
are flagged qualitatively in the record `note` rather than auto-rejected.

## system_id convention

Lowercase; spaces and special chars → `-`; keep the most common name.
Examples: `hd-163296`, `as-209`, `tw-hya`, `beta-pic`, `hr-8799`, `pds-70`, `2m1207`,
`rxj1604-2130`, `im-lup`. Greek letters spelled out (`beta-pic`, `eta-crv`).

## Schema (v1)

```jsonc
{
  "id": "hd-163296",
  "name": "HD 163296",                  // display name
  "alt_names": ["MWC 275"],             // optional
  "simbad": "HD 163296",                // name to feed SIMBAD's resolver. Audited against
                                        // SIMBAD with coordinate verification (2026-07-07);
                                        // set EXPLICITLY to null for objects SIMBAD lacks —
                                        // the frontend then links a coordinate search instead
  "ra_deg": 269.0887,                   // ICRS deg (J2000). REQUIRED for the sky map.
  "dec_deg": -21.9562,
  "dist_pc": 101.0,                     // null if unknown (derived from plx when absent)
  "plx_mas": 9.9,                       // SIMBAD parallax (mas); null if unknown
  "mags": {"V": 6.85, "G": 6.77, "J": 6.2, "H": 5.5, "K": 4.8},
                                        // SIMBAD magnitudes (any of U B V G R I J H K);
                                        // null/absent if unknown. Frontend links every
                                        // system to its SIMBAD page as the source.
  "sptype": "A1Ve",                     // null if unknown
  "region": "Isolated / Sco-Cen / Taurus / Lupus / ...",   // free text, optional
  "categories": ["protoplanetary"],     // any of: "protoplanetary", "debris", "quasar"
                                        // (a system with only an imaged planet and no
                                        //  resolved disk has categories: [];
                                        //  "quasar" = coronagraphic quasar-host imaging)
  "planets": [                          // companions; [] if none
    { "name": "b", "status": "confirmed", "method": "imaging",
      "note": "optional short note (Author+Year mentions get auto-linked to SciX)",
      "paper": {"first_author": "Marois", "year": 2008,
                "arxiv": "0811.2606", "bibcode": "2008Sci...322.1348M"},
      "extra_papers": [ {"label": "independent discovery", "first_author": "...",
                         "year": 2023, "arxiv": "...", "bibcode": null} ] }
                                        // status: "confirmed" | "candidate" | "disputed"
                                        //   | "dust-cloud" (Fomalhaut b) | "refuted"
                                        //   (background star / stellar — kept for the
                                        //    historical record; excluded from planet-host
                                        //    counts and the ★ marker)
                                        // method: "imaging" | "transit" | "interferometry"
                                        // paper: discovery/claim ref; extra_papers:
                                        //   optional additional refs, all linked arXiv+SciX
  ],
  "images": [
    {
      "image_id": "hd-163296_dsharp",   // unique within system; also the filename stem
      "type": "disk_mm",                // "disk_mm" (thermal emission: mm/submm interferometry
                                        //   AND mid-IR space imaging e.g. JWST/MIRI)
                                        // | "disk_scattered" | "planet"
      "facility": "ALMA",               // ALMA / SMA / HST / JWST / VLT-SPHERE / Gemini-GPI /
                                        // Subaru-HiCIAO / VLT-NACO / Keck-NIRC2 / ...
      "instrument": "Band 6",           // free text (Band 7, STIS, IRDIS, MIRI, ...)
      "wavelength_um": 1250,            // number, for the wavelength slider sort. REQUIRED.
      "wavelength_label": "1.25 mm continuum",
      "technique": "interferometry",    // interferometry | PDI | ADI | RDI | coronagraphy | other
      "content": "continuum",           // continuum | line. REQUIRED on disk_mm records.
                                        // GRANULARITY RULE (decided 2026-07-11): spectral-line
                                        // data products (moment-0/integrated-intensity maps,
                                        // per-molecule ALMA maps, narrow-band Halpha/[SII]
                                        // emission-line images) enter as ONE RECORD PER LINE,
                                        // exactly as continuum enters one record per band —
                                        // lines are physically distinct tracers (different
                                        // chemistry, layers, radii). Do NOT consolidate a
                                        // multi-line gallery into one record. `content`
                                        // separates the two populations so the frontend can
                                        // facet on it and the paper can count them separately.
      "survey": "DSHARP",               // null for individual papers
      "file": "images/hd-163296/hd-163296_dsharp.png",  // relative to repo root; null = pending
      "credit": "Andrews et al. 2018, Fig. 3 (crop)",   // where the crop came from
      "hires_url": null,                // optional external hi-res source; when set, the
                                        // frontend shows a "hi-res data ↗" link to it instead
                                        // of the arXiv PDF (used for ALICE HLSP NICMOS records
                                        // -> https://archive.stsci.edu/prepds/alice/)
      "paper": {
        "first_author": "Andrews",
        "year": 2018,
        "title": "The Disk Substructures at High Angular Resolution Project (DSHARP). I. ...",
        "journal": "ApJL 869, L41",     // free text; null ok
        "arxiv": "1812.04040",          // arXiv id WITHOUT "arXiv:"; null if none
        "bibcode": "2018ApJ...869L..41A" // null if unsure — links still work via arXiv id
      }
    }
  ],
  "notes": "free text (candidate planets, disputed claims, ...)",   // optional
  "last_updated": "2026-07-06"
}
```

### Link rules (frontend builds URLs — do NOT store full URLs)

- arXiv:  `https://arxiv.org/abs/<arxiv>`
- ADS:    `https://ui.adsabs.harvard.edu/abs/<bibcode>` if bibcode set,
          else `https://ui.adsabs.harvard.edu/abs/arXiv:<arxiv>`
- A paper with neither `arxiv` nor `bibcode` shows title only (avoid this).

### Image files

≤ 640 px on the longest side, PNG (or JPG for photographic content), ≤ ~300 KB.
Path must be `images/<system_id>/<image_id>.png`. `file: null` renders a
"image pending — see paper" placeholder, so metadata-only entries are fine.

## How to add things

| Case | Do this |
|---|---|
| New image for existing system | Append to `images[]`, set `file` (or null), bump `last_updated`, run `backend-data/build.py`. |
| New system | Create `data/systems/<id>.json` (copy one as template). Get RA/Dec via SIMBAD (see `backend-data/README.md`). Run `validate.py` + `build.py`. |
| Whole new survey | Add to `backend-data/seeds/` (see its README) + crop manifest. Batch-friendly. |
| New imaged planet around known star | Append to that system's `planets[]` + add a `"type": "planet"` image entry. |

## Staging (for crop agents)

Automated agents drop new/updated image records in `data/staging/<batch>.json`
(format documented in `backend-data/README.md`); `backend-data/merge_staging.py` folds them
into `data/systems/`. This avoids concurrent edits to the same system file.

## Build-time enrichment (not stored here)

`backend-data/build.py` adds `fac_keys` (AAS facility keywords, list — joint A+B images carry
both) and `instr_key` (canonical instrument family) to every image record in
`frontend/data.js`, via `backend-data/facility_map.py`. Keep the free-text `facility` /
`instrument` fields as-is in these JSONs; extend the mapping table when a new facility
string appears.

## Bookkeeping ledgers (who records what — avoid duplicates)

- **`data/systems/*.json`** (this folder) — ground truth; a paper is "in the atlas" iff
  cited here. The paper-finder Skill auto-treats all cited arXiv ids as done.
- **`data/paper_finder_state.json`** — per-paper dispositions for papers NOT in the atlas
  (`excluded`+reason / `ingested` pointer). One flat dict with two key styles that
  coexist: Semantic-Scholar hashes (written by the Skill / `find_papers.py --mark`)
  and plain arXiv ids (written when reviewing `backend-data/fresh_papers.py` weekly
  digests — the sweeper dedupes on these).
- **`data/ingestion_status.json`** — per-survey/batch human ledger + session notes:
  `entries`/`coords`/`images` each `"done"|"partial"|"todo"` + free-text `notes`.
  **Always update it when you ingest a batch** — but per-paper decisions go in the
  state file above, not into prose here.
- `data/paper_finder/` — regenerable Skill working files (candidates, citation cache).
- `data/staging/_report_*.md` — historical per-batch crop reports (append-only archive).
