<p align="center"><img src="frontend/logo.svg" alt="diskatlas logo" width="128"></p>

# `diskatlas`: all-sky interactive atlas for resolved circumstellar disks and imaged companions

`diskatlas`: 星周盘图像与直接成像伴体 · 交互式全天图

**🌐 Browse it live: <https://seawander.github.io/diskatlas/>** · 
[Source & data on GitHub](https://github.com/seawander/diskatlas) — or clone and
double-click `index.html` for the fully offline version.

An offline-capable, interactive all-sky atlas of every system with a **resolved circumstellar
disk** (mm/submm/cm interferometry, high-contrast scattered light / thermal IR, and resolved
far-IR single-dish imaging), a **directly imaged planet or substellar companion**, or a
**coronagraphically imaged quasar host**. Click any object on the sky map to browse its images
across instruments, wavelengths and epochs, with clickable arXiv / SciX citations for every image.

**双击根目录的 `index.html` 即可离线使用。**  Double-click `index.html` — no server, no internet needed.

## What's inside

**606 systems · 2702 image records**, every one a panel cropped from a peer-reviewed
figure with full citations; coordinates for every system; a companion catalogue with
per-object status (`confirmed` / `candidate` / `disputed` / `refuted`).
`python3 backend-data/build.py` prints the exact live counts — trust it over any number in
prose. Session-by-session history lives in `docs/HISTORY.md`.

The viewer offers three views — **Sky map**, **Coverage matrix**, and **Tonight** (an
observability planner with per-target [airmass.org](https://airmass.org) night-chart links
and CSV export) — with faceted filters (wavelength band, facility, instrument, missing
modality), a light/dark theme, and a **12-language UI** (including right-to-left Arabic and
translated constellation names). Everything runs client-side from `file://` — no server, no
build step, no CDN. See `frontend/README.md` for the full feature map.

## Contributing

Contributions are very welcome — new systems, missing instruments/epochs, coordinate or
citation fixes, translations, frontend improvements — whether you edit by hand or **drive an
AI agent on your own machine** (most of the atlas was built that way). Fork, make your
change, and open a pull request; to just suggest a paper or target,
[open an issue](https://github.com/seawander/diskatlas/issues).

- **Read [`CONTRIBUTING.md`](CONTRIBUTING.md)** for the full recipe (human and agent-driven).
- **Using an agent?** [`AGENTS.md`](AGENTS.md) (and `CLAUDE.md` for Claude Code) auto-loads
  in most harnesses and orients it the moment you open the repo.

Two rules for any PR: `python3 backend-data/validate.py` must report **0 errors**, and never
hand-edit the generated `frontend/data.js` (rebuild with `python3 backend-data/build.py`).

## Repository layout

```
index.html          ← THE app. Open this. (loads frontend/ + images/)
frontend/           ← app.js, style.css, data.js (data.js is GENERATED — do not hand-edit)
data/               ← the database: one JSON per system + docs. THIS is what you edit.
backend-data/       ← Python pipeline: seed → coordinates → crop → validate → build
images/             ← _sources/ (downloaded figures) + <system_id>/*.png (cropped panels)
```

Every folder has its own `README.md`. Agents: `CLAUDE.md` / `AGENTS.md` route you to the one
doc your task needs; `HANDOFF.md` is the complete handbook.

## Scope / 收录标准

- **Disks**: spatially resolved (≥ a few beams / PSFs) circumstellar disks — protoplanetary
  (incl. transition, edge-on, eruptive-star and Class 0/I embedded) and debris — imaged by
  mm/submm/cm interferometers (ALMA, SMA, PdBI/NOEMA, VLA, CARMA, OVRO, BIMA, ATCA), in
  scattered light / thermal IR by high-contrast instruments (HST, JWST, GPI, SPHERE, Subaru
  HiCIAO/SCExAO, NACO, MagAO(-X), LBTI, …), by VLTI interferometric reconstruction, and in
  the resolved far-IR (Herschel/Spitzer/JCMT/CSO). Orion proplyd silhouettes included.
- **Companions**: directly imaged planets and brown-dwarf companions (status
  `confirmed`/`candidate`/`disputed`/`refuted` tracked per companion; a few borderline or
  later-refuted objects are kept for the historical record and flagged).
- **Quasar hosts**: coronagraphic / PSF-subtracted host-galaxy imaging (`redshift` instead
  of `dist_pc`).
- Resolved **far-IR/submm single-dish** images (Herschel PACS/SPIRE, Spitzer MIPS, JCMT,
  CSO) are in scope; marginally resolved single-beam detections and unresolved excesses
  remain **excluded**.
- Press-release composites are **not** used; every image is cropped from a peer-reviewed
  figure and linked to its paper (arXiv + SciX).

## License / 许可

Three parts, three answers:

- **Code** (`index.html`, `frontend/` JS+CSS, `backend-data/` Python): **MIT** — see
  [LICENSE](LICENSE).
- **Compiled database** (`data/systems/*.json`, the metadata in generated
  `frontend/data.js`): **CC BY 4.0** — see [LICENSE-DATA.md](LICENSE-DATA.md). Cite this
  repository (and the accompanying paper, once published) when reusing.
- **Images** (`images/**/*.png`): **not** covered by either license. They are
  low-resolution crops of figures from peer-reviewed papers — cropped from the
  **authors' own arXiv source files** (preprint figures), not from the journal-typeset
  articles. Rights remain **© the original authors** (and the journals for the published
  versions — AAS, A&A, MNRAS, …); each crop is reproduced here with a per-image credit
  line and full citation for scholarly reference. Follow each record's links
  (arXiv / SciX / DOI) for the originals and for any reuse permissions.

## Disclaimer & fair-use statement / 免责声明与合理使用

`diskatlas` is a **non-commercial, not-for-profit** resource created solely for scientific
research and education. The image excerpts are small, reduced-resolution crops taken from
the **authors' own arXiv source files** (preprint figures) — not from the journals'
typeset versions of record — to help researchers **locate and navigate the primary
literature**. Every excerpt carries a credit line and links back to the original paper
(arXiv / SciX / DOI), and is not a substitute for the published article. We believe this
constitutes fair use (17 U.S.C. § 107) / fair dealing for purposes of research and
scholarship.

We have **no intention to infringe any copyright**. All rights in the original figures
remain with their authors (and, for the versions of record, their publishers). If you are
a rights holder and would prefer that a particular image not appear here, please
[open an issue](https://github.com/seawander/diskatlas/issues) and it will be removed
promptly.
