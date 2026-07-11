# Data license

The **compiled database** of this repository — the per-system JSON records in
`data/systems/` and the generated `frontend/data.js` (system metadata,
coordinates, companion/disk classifications, citation records, notes) — is
licensed under the **Creative Commons Attribution 4.0 International license
(CC BY 4.0)**: <https://creativecommons.org/licenses/by/4.0/>.

Attribution: cite this repository (and the accompanying paper, once published)
when reusing the database.

## What this license does NOT cover

- **Image files** (`images/**/*.png`) and any thumbnails embedded in the app:
  these are low-resolution crops of figures from peer-reviewed papers, made
  from the **authors' own arXiv source files** (preprint figures), not from the
  journal-typeset articles. Rights remain **© the original authors** and, for
  the published versions, the publishers (AAS journals, A&A, MNRAS, Nature,
  Science, …). They are reproduced here in reduced form, with a per-image
  credit line and links to the source paper (arXiv / SciX / DOI), for
  scholarly reference. They are **not** redistributable under CC BY; obtain
  the originals from the authors or publisher for any reuse.
- **Code** (`frontend/*.js`, `frontend/*.css`, `index.html`, `backend-data/`),
  which is under the MIT license — see [LICENSE](LICENSE).

## Summary of the three-way grant

| Component | Files | License / status |
|---|---|---|
| Code | `frontend/*.js·css`, `index.html`, `backend-data/` | **MIT** |
| Database records / metadata | `data/systems/*.json`, metadata in `frontend/data.js` | **CC BY 4.0** |
| Image panels | `images/**/*.png` | **excluded** — © original authors / publishers, linked to source |

## Per-panel licensing manifest

`backend-data/licensing_manifest.py` builds `data/paper_finder/licensing_manifest.csv`,
one row per cropped panel with its source journal, publisher, open-access flag, and a
**license class**: `arxiv-preprint-figure` (cropped from the authors' arXiv source
package — the large majority), `archive-product` (an official archive preview such as
ALICE/MAST), or `publisher-pdf` (a pre-arXiv classic obtained from the publisher PDF).

Panels whose source venue is **restrictive** (Nature, Science, Nature Astronomy,
Nature Communications) are flagged in the manifest so that permission can be sought
before any figure is *reproduced* in the atlas paper. The atlas itself only shows
reduced crops with a credit line and source links (scholarly reference); the paper
reproduces a small number of demo panels, for which permission is tracked in the
`permission_status` column (`not-needed` / `pending` / `granted`). The TWA 7 JWST/MIRI
panel (Lagrange et al. 2025, *Nature* 642, 905) is marked **pending** — author
permission is being requested for its reproduction in the paper.
