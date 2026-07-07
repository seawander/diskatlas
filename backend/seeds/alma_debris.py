"""mm/submm-resolved debris disks (planetesimal belts): REASONS, ARKS, classics.

- REASONS (Matra+2025, arXiv 2501.09058): 74 resolved belts, uniform models.
  COMPLETE membership below (74/74), in gallery (RA) order, ids = Fig. 1 panel
  labels (verified against the figure by Batch B crop agent, 2026-07-06).
- ARKS (Marino+2026, arXiv 2601.11708): ALMA Large Program, 24 belts (all also
  in REASONS). Complete membership from Fig. 3 gallery.
"""
from .util import survey, system, img, paper, planet

P_REASONS = paper("Matra", 2025,
                  "REsolved ALMA and SMA Observations of Nearby Stars (REASONS): A population of 74 resolved planetesimal belts at millimetre wavelengths",
                  "A&A 693, A151", arxiv="2501.09058", bibcode="2025A&A...693A.151M")
P_ARKS = paper("Marino", 2026,
               "The ALMA survey to Resolve exoKuiper belt Substructures (ARKS) I: Motivation, sample, data reduction, and results overview",
               "A&A", arxiv="2601.11708")

MM = {"type": "disk_mm", "facility": "ALMA/SMA", "technique": "interferometry",
      "instrument": "Band 6/7", "wavelength_um": 1300,
      "wavelength_label": "~0.9-1.3 mm continuum"}

# ARKS: new observations are ALMA Band 7 (0.88 mm); a few systems use archival Band 6.
MM_ARKS = {"type": "disk_mm", "facility": "ALMA", "technique": "interferometry",
           "instrument": "Band 7/6", "wavelength_um": 880,
           "wavelength_label": "~0.88-1.3 mm continuum"}

BLOCKS = [
    # ------------------------------------------------------------------
    # REASONS resolved sample, 74 belts (Matra+2025 Fig. 1, ordered by RA).
    # Display names slugify to the system ids used by the cropped panels.
    survey("REASONS", P_REASONS, MM,
           [
               ("HD 105", {}),
               ("GJ 14", {}),
               ("49 Cet", {"alt_names": ["HD 9672"]}),
               ("HD 10638", {}),
               ("HD 10647", {"alt_names": ["q1 Eri"]}),
               ("HD 14055", {"alt_names": ["gamma Tri"]}),
               ("HD 15115", {}),
               ("HD 15257", {}),
               ("HD 15745", {}),
               ("HD 16743", {}),
               ("HD 21997", {}),
               ("HD 22049", {"alt_names": ["eps Eri"]}),
               ("HD 32297", {}),
               ("HD 35841", {}),
               ("HD 36546", {}),
               ("HD 38206", {}),
               ("HD 38858", {}),
               ("beta Pic", {"alt_names": ["HD 39060"]}),
               ("HD 48682", {}),
               ("HD 50571", {}),
               ("HD 53143", {}),
               ("HD 54341", {}),
               ("HD 61005", {"alt_names": ["The Moth"]}),
               ("HD 76582", {}),
               ("HD 84870", {}),
               ("TWA 7", {}),
               ("HD 92945", {"alt_names": ["V419 Hya"]}),
               ("HD 95086", {}),
               ("HD 104860", {}),
               ("HD 105211", {}),
               ("HD 106906", {}),
               ("HD 107146", {}),
               ("eta Crv", {"alt_names": ["HD 109085"]}),
               ("HR 4796A", {"alt_names": ["HD 109573"]}),
               ("HD 110058", {}),
               ("HD 111520", {}),
               ("HD 112810", {}),
               ("HD 113556", {}),
               ("HD 113766", {}),
               ("HD 114082", {}),
               ("HD 115600", {}),
               ("HD 117214", {}),
               ("HD 121191", {}),
               ("HD 121617", {}),
               ("HD 127821", {}),
               ("HD 129590", {}),
               ("HD 131488", {}),
               ("HD 131835", {}),
               ("HD 138813", {}),
               ("HD 139664", {}),
               ("HD 142315", {}),
               ("HD 142446", {}),
               ("HD 145560", {}),
               ("HD 146181", {}),
               ("HD 146897", {}),
               ("HD 147137", {}),
               ("HD 158352", {}),
               ("HD 161868", {"alt_names": ["gamma Oph"]}),
               ("HD 164249", {}),
               ("GSC 07396-00759", {}),
               ("HD 170773", {}),
               ("Vega", {"alt_names": ["HD 172167", "alpha Lyr"]}),
               ("HD 181327", {}),
               ("HD 182681", {}),
               ("HD 191089", {}),
               ("AU Mic", {"alt_names": ["HD 197481"]}),
               ("HD 202628", {}),
               ("HD 205674", {}),
               ("HD 206893", {}),
               ("HD 207129", {}),
               ("TYC 9340-437-1", {}),
               ("Fomalhaut", {"alt_names": ["alpha PsA", "HD 216956"]}),
               ("HD 216956C", {"simbad": "Fomalhaut C",
                               "alt_names": ["Fomalhaut C", "LP 876-10"]}),
               ("HR 8799", {"alt_names": ["HD 218396"]}),
           ],
           categories=("debris",),
           notes="complete 74-belt membership from Matra+2025 Fig. 1 panel labels"),

    # ------------------------------------------------------------------
    # ARKS 24-belt sample (Marino+2026 Fig. 3 gallery order); all in REASONS.
    survey("ARKS", P_ARKS, MM_ARKS,
           [
               ("49 Cet", {}),
               ("HD 10647", {}),
               ("HD 14055", {}),
               ("HD 15115", {}),
               ("HD 15257", {}),
               ("HD 32297", {}),
               ("beta Pic", {}),
               ("HD 61005", {}),
               ("HD 76582", {}),
               ("HD 84870", {}),
               ("HD 92945", {}),
               ("HD 95086", {}),
               ("HD 107146", {}),
               ("HR 4796A", {}),
               ("HD 121617", {}),
               ("HD 131488", {}),
               ("HD 131835", {}),
               ("HD 145560", {}),
               ("HD 161868", {}),
               ("HD 170773", {}),
               ("AU Mic", {}),
               ("HD 206893", {}),
               ("TYC 9340-437-1", {}),
               ("HR 8799", {}),
           ],
           categories=("debris",),
           notes="ALMA Large Program, 24 exoKuiper belts; substructure-quality images"),
]

SYSTEMS = [
    system("Fomalhaut", categories=("debris",),
           planets=[planet("b", "dust-cloud",
                           "Kalas+2008 imaged source; now interpreted as expanding dust cloud")],
           images=[
               img("alma2017", "disk_mm", "ALMA", "Band 6", 1300,
                   "1.3 mm continuum (full ring)", "interferometry",
                   paper("MacGregor", 2017,
                         "A Complete ALMA Map of the Fomalhaut Debris Disk",
                         "ApJ 842, 8", arxiv="1705.05867", bibcode=None)),
               img("jwst2023", "disk_mm", "JWST", "MIRI F2550W", 25.5,
                   "25.5 um thermal (inner disk + outer ring)", "other",
                   paper("Gaspar", 2023,
                         "Spatially resolved imaging of the inner Fomalhaut disk using JWST/MIRI",
                         "Nature Astronomy 7, 790", arxiv="2305.03789", bibcode=None)),
           ]),

    system("AU Mic", region="beta Pic moving group", categories=("debris",),
           images=[img("alma2013", "disk_mm", "ALMA", "Band 6", 1300,
                       "1.3 mm continuum (edge-on belt)", "interferometry",
                       paper("MacGregor", 2013,
                             "Millimeter Emission Structure in the First ALMA Image of the AU Mic Debris Disk",
                             "ApJL 762, L21", arxiv="1211.5148", bibcode="2013ApJ...762L..21M"))]),

    system("beta Pic", alt_names=("HD 39060",), region="beta Pic moving group",
           categories=("debris",),
           planets=[planet("b"),
                    planet("c", "confirmed", "GRAVITY interferometric detection (Nowak+2020)")],
           images=[img("alma2014", "disk_mm", "ALMA", "Band 7", 870,
                       "870 um continuum + CO clump", "interferometry",
                       paper("Dent", 2014,
                             "Molecular Gas Clumps from the Destruction of Icy Bodies in the beta Pictoris Debris Disk",
                             "Science 343, 1490", arxiv=None, bibcode="2014Sci...343.1490D"))]),

    system("HR 8799", categories=("debris",),
           planets=[planet("b"), planet("c"), planet("d"), planet("e")],
           images=[img("alma2016", "disk_mm", "ALMA", "Band 6", 1340,
                       "1.34 mm continuum (outer belt; planets inset)", "interferometry",
                       paper("Booth", 2016,
                             "Resolving the Planetesimal Belt of HR 8799 with ALMA",
                             "MNRAS 460, L10", arxiv="1603.04853", bibcode=None))]),

    system("Vega", alt_names=("alpha Lyr",), categories=("debris",),
           images=[img("jwst2024", "disk_mm", "JWST", "MIRI F2550W", 25.5,
                       "25.5 um thermal (smooth face-on disk)", "other",
                       paper("Su", 2024,
                             "Imaging of the Vega Debris System using JWST/MIRI",
                             "ApJ 979, 43", arxiv="2410.23636", bibcode=None))],
           notes="JWST/HST images remarkably smooth — no planet sculpting signatures."),

    system("eta Crv", categories=("debris",),
           images=[img("alma2017", "disk_mm", "ALMA", "Band 6", 1300,
                       "1.3 mm continuum ring", "interferometry",
                       # arXiv id 1611.02196 was WRONG (it is Faramaz+2017,
                       # "Inner mean-motion resonances with eccentric planets", an
                       # exozodi dynamics paper — not the eta Crv ALMA imaging paper).
                       # Correct arXiv id for Marino+2017 (MNRAS 465, 2595) TBD.
                       paper("Marino", 2017,
                             "ALMA observations of the eta Corvi debris disc: inward scattering of CO-rich exocomets?",
                             "MNRAS 465, 2595", arxiv=None, bibcode=None, verify=True))]),

    system("HD 107146", categories=("debris",),
           images=[img("alma2015", "disk_mm", "ALMA", "Band 6", 1250,
                       "1.25 mm continuum (broad belt + gap)", "interferometry",
                       paper("Ricci", 2015,
                             "ALMA Observations of the Debris Disk around the Young Solar Analog HD 107146",
                             "ApJ 798, 124", arxiv="1410.8265", bibcode=None))]),

    system("HD 95086", categories=("debris",),
           planets=[planet("b")],
           images=[img("alma2017", "disk_mm", "ALMA", "Band 6", 1300,
                       "1.3 mm continuum (broad belt)", "interferometry",
                       # arXiv id 1703.10893 was WRONG (an IEEE speech-enhancement
                       # paper, not astronomy). Correct HD 95086 ALMA paper is
                       # believed to be Su+2017 "ALMA 1.3 mm Map of the HD 95086
                       # System", AJ 154, 225 — id needs online confirmation.
                       paper("Su", 2017,
                             "ALMA 1.3 mm Map of the HD 95086 System",
                             "AJ 154, 225", arxiv=None, bibcode=None, verify=True))],
           notes="Debris + imaged planet b (Rameau+2013)."),
]
