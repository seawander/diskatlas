# Instrument & facility taxonomy

This is a **map, not a whitelist.** The atlas covers imaging / high-contrast imaging / spatially resolved
spectroscopy / interferometry of planet-formation targets — and since 2026-07-16 ANY published sky-image
panel qualifies (resolved or unresolved, detection or imaged non-detection). Any instrument that produces
such data is in scope, including ones not listed here and ones commissioned after this file was written.
Use this to (a) recognize instruments named in a paper, (b) generate instrument-scoped SciX searches, and
(c) know what *kind* of image data to expect (which affects the relevance call).

When you search SciX by instrument, both the instrument name and the facility name are worth trying, and
so are common aliases — ADS/SciX metadata is inconsistent about which is recorded. Query hints below give
the strings that tend to hit.

## Visible → near-infrared (scattered light, coronagraphy, polarimetry, direct imaging, resolved IFS)

| Facility | Instruments | Notes / data products | Search hints |
|---|---|---|---|
| HST | ACS, STIS, NICMOS, WFPC2, WFC3, FOC | Coronagraphy & broadband scattered light; STIS/ACS coronagraphic disk imaging | `HST STIS coronagraph disk`, `NICMOS disk imaging`, `instr:"HST"` |
| JWST | NIRCam, NIRSpec (IFU), NIRISS (AMI) | Coronagraphic imaging, IFU, aperture-masking interferometry | `JWST NIRCam coronagraph disk`, `NIRISS AMI` |
| VLT | SPHERE/IRDIS, SPHERE/IFS, SPHERE/ZIMPOL, NaCo (CONICA), ERIS, GRAVITY | High-contrast polarimetry (Qφ/PI), ADI, IFS; GRAVITY = interferometric astrometry/spectroscopy of companions | `SPHERE IRDIS disk`, `ZIMPOL polarimetric`, `NACO disk`, `GRAVITY exoplanet` |
| Gemini | GPI (Gemini Planet Imager), NICI, GPI 2.0 | Polarimetric + spectral high-contrast IFS | `GPI polarimetry disk`, `Gemini Planet Imager` |
| Subaru | SCExAO, CHARIS, HiCIAO, AO188 | Extreme AO, IFS, polarimetric differential imaging | `SCExAO CHARIS`, `HiCIAO polarimetric disk` |
| Keck | NIRC2 (+ vortex/pyramid AO), OSIRIS, KPIC | AO imaging & polarimetry, IFS, high-res companion spectroscopy | `NIRC2 disk imaging`, `NIRC2 vortex`, `OSIRIS companion` |
| LBT | LMIRcam, LBTI | AO imaging/interferometry | `LBTI disk`, `LMIRcam` |
| Magellan | MagAO, MagAO-X, VisAO | Visible/NIR extreme AO, Hα for accreting protoplanets | `MagAO-X protoplanet`, `VisAO H-alpha` |
| Palomar / others | PALM-3000, WIRC-Pol, SDC | AO / polarimetric imaging | `Palomar disk polarimetry` |

Notable data-product cues that mean "a sky-image panel is present": *scattered light image*, *polarimetric
intensity / Qφ / PI*, *ADI / KLIP / reference-star differential imaging*, *contrast curve* + detection,
*spectral IFS cube*.

## Mid-infrared (thermal imaging, interferometry, nulling)

| Facility | Instruments | Notes | Search hints |
|---|---|---|---|
| VLTI | MATISSE, MIDI (decommissioned), PIONIER, AMBER | Long-baseline interferometry; resolved inner-disk / geometry | `MATISSE disk`, `MIDI protoplanetary`, `VLTI interferometry disk` |
| JWST | MIRI (imaging, coronagraph, MRS IFU) | Thermal coronagraphy + IFU | `JWST MIRI coronagraph disk`, `MIRI MRS` |
| VLT | NEAR (VISIR upgrade), VISIR | Mid-IR imaging / nulling | `NEAR nulling`, `VISIR disk` |
| Gemini | T-ReCS, Michelle | Mid-IR imaging of resolved disks (esp. earlier debris-disk detections) | `T-ReCS disk`, `Gemini Michelle debris` |
| Keck / LBT | Nuller, NOMIC | Nulling interferometry (exozodi, inner disks) | `Keck Nuller exozodi`, `NOMIC` |
| Herschel | PACS, SPIRE | Far-IR thermal (70–500 µm). Keep any paper that publishes an actual **image panel** of the target (resolved maps of nearby/large debris disks, but also unresolved/marginal maps since 2026-07-16); skip photometry-table-only papers | `Herschel PACS disk image` |

## Sub-millimeter / millimeter / radio (continuum + molecular line, resolved maps)

| Facility | Notes | Search hints |
|---|---|---|
| ALMA | The workhorse: continuum rings/gaps + resolved line/moment maps; kinematic planet detections | `ALMA disk rings`, `ALMA protoplanetary continuum`, `ALMA kinematic planet` |
| SMA | Sub-mm continuum & line imaging | `SMA disk`, `Submillimeter Array disk` |
| NOEMA / PdBI | mm interferometry | `NOEMA disk`, `Plateau de Bure disk` |
| VLA | cm continuum, large grains / inner disk | `VLA disk continuum`, `Jansky VLA protoplanetary` |
| ATCA / others | mm/cm resolved imaging | `ATCA disk` |

## Using this in searches

- Instrument-scoped SciX field: `instr:"SPHERE"` (works when instrument metadata is populated).
- When `instr:` misses, fall back to full-text: `full:"SPHERE" full:"disk"` or plain `SPHERE disk imaging`.
- Combine with the target when chasing coverage of a known object: `object:"HD 100546" instr:"SPHERE"`.
- For a *new-instrument* sweep (find targets you don't have), search the instrument alone, newest-first,
  and filter by the relevance rules — e.g. `MagAO-X protoplanet` sorted by date.
