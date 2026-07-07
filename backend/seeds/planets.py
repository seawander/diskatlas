"""Directly imaged planetary-mass companions (<~16 MJup) and their discovery images.

Systems already defined elsewhere (beta Pic, HR 8799, PDS 70, Fomalhaut, AB Aur,
HD 95086, HD 106906, TWA 7, ...) get planets[] merged from those seeds; here we add
the planet-image records and the planet-only systems.

Excluded by policy (mass clearly >16 MJup): PZ Tel B, HR 2562 B, HD 19467 B, GJ 758 B,
HD 4747 B, GJ 229 B, HD 206893 B (~25 MJ; but planet c IS included).
"""
from .util import system, img, paper, planet

PL = {"type": "planet"}


def pimg(suffix, facility, instrument, wl, wl_label, technique, p, credit=None):
    return img(suffix, "planet", facility, instrument, wl, wl_label, technique, p,
               credit=credit)


SYSTEMS = [
    system("HR 8799", categories=("debris",),
           planets=[planet("b"), planet("c"), planet("d"), planet("e")],
           images=[
               pimg("keck2008", "Keck", "NIRC2", 2.1, "JHK composite; b, c, d discovery", "ADI",
                    paper("Marois", 2008,
                          "Direct Imaging of Multiple Planets Orbiting the Star HR 8799",
                          "Science 322, 1348", arxiv="0811.2606", bibcode="2008Sci...322.1348M")),
               pimg("keck2010", "Keck", "NIRC2", 3.8, "L' band; planet e discovery", "ADI",
                    paper("Marois", 2010,
                          "Images of a fourth planet orbiting HR 8799",
                          "Nature 468, 1080", arxiv="1011.4918", bibcode="2010Natur.468.1080M")),
           ]),

    system("beta Pic",
           planets=[planet("b"), planet("c", "confirmed", "GRAVITY interferometry"),
                    planet("d", "confirmed",
                           "third planet, announced 2026 (Sutlieff+ imaging / Gibbs+ JWST)")],
           images=[pimg("naco2010", "VLT-NACO", "NACO", 3.8,
                        "L' band; planet b confirmed bound", "ADI",
                        paper("Lagrange", 2010,
                              "A Giant Planet Imaged in the Disk of the Young Star beta Pictoris",
                              "Science 329, 57", arxiv="1006.3314", bibcode="2010Sci...329...57L"))]),

    system("PDS 70",
           images=[pimg("muse2019", "VLT-MUSE", "MUSE NFM", 0.656,
                        "H-alpha; accreting planets b & c", "other",
                        paper("Haffert", 2019,
                              "Two accreting protoplanets around the young star PDS 70",
                              "Nature Astronomy 3, 749", arxiv="1906.01486",
                              bibcode="2019NatAs...3..749H"))]),

    system("2M1207", simbad="2MASSWJ 1207334-393254", alt_names=("2M1207A",),
           region="TW Hya assoc.", categories=(),
           planets=[planet("b", "confirmed", "First directly imaged planetary-mass companion (2004)")],
           images=[pimg("naco2004", "VLT-NACO", "NACO", 2.2,
                        "H+Ks+L' composite; first image of a planetary-mass companion", "other",
                        paper("Chauvin", 2004,
                              "A giant planet candidate near a young brown dwarf",
                              "A&A 425, L29", arxiv="astro-ph/0409323",
                              bibcode="2004A&A...425L..29C"))]),

    system("51 Eri", categories=(),
           planets=[planet("b")],
           images=[pimg("gpi2015", "Gemini-GPI", "IFS", 1.65,
                        "H band; T-dwarf planet discovery", "ADI",
                        paper("Macintosh", 2015,
                              "Discovery and spectroscopy of the young jovian planet 51 Eri b with the Gemini Planet Imager",
                              "Science 350, 64", arxiv="1508.03084", bibcode="2015Sci...350...64M"))]),

    system("HIP 65426", region="Sco-Cen", categories=(),
           planets=[planet("b")],
           images=[
               pimg("sphere2017", "VLT-SPHERE", "IRDIS+IFS", 1.65,
                    "H band; SHINE discovery", "ADI",
                    paper("Chauvin", 2017,
                          "Discovery of a warm, dusty giant planet around HIP 65426",
                          "A&A 605, L9", arxiv="1707.01413", bibcode="2017A&A...605L...9C")),
               pimg("jwst2023", "JWST", "NIRCam+MIRI", 11.4,
                    "2-16 um; first JWST exoplanet imaging", "coronagraphy",
                    paper("Carter", 2023,
                          "The JWST Early Release Science Program for Direct Observations of Exoplanetary Systems I: High-Contrast Imaging of the Exoplanet HIP 65426 b from 2-16 um",
                          "ApJL 951, L20", arxiv="2208.14990", bibcode="2023ApJ...951L..20C")),
           ]),

    system("HD 95086", planets=[planet("b")],
           images=[pimg("naco2013", "VLT-NACO", "NACO", 3.8,
                        "L' band; planet discovery", "ADI",
                        paper("Rameau", 2013,
                              "Discovery of a probable 4-5 Jupiter-mass exoplanet to HD 95086 by direct-imaging",
                              "ApJL 772, L15", arxiv="1305.7428", bibcode="2013ApJ...772L..15R"))]),

    system("GJ 504", categories=(),
           planets=[planet("b", "confirmed", "Mass debated (4-30 MJup depending on system age)")],
           images=[pimg("seeds2013", "Subaru-HiCIAO", "HiCIAO", 1.65,
                        "J/H composite; SEEDS discovery", "ADI",
                        paper("Kuzuhara", 2013,
                              "Direct Imaging of a Cold Jovian Exoplanet in Orbit around the Sun-like Star GJ 504",
                              "ApJ 774, 11", arxiv="1307.2886", bibcode="2013ApJ...774...11K"))]),

    system("kappa And", categories=(),
           planets=[planet("b", "confirmed", "Near the planet/BD boundary (~13-22 MJup)")],
           images=[pimg("seeds2013", "Subaru-HiCIAO", "HiCIAO", 1.65,
                        "JHK composite; SEEDS discovery", "ADI",
                        paper("Carson", 2013,
                              "Direct Imaging Discovery of a 'Super-Jupiter' Around the Late B-Type Star kappa And",
                              "ApJL 763, L32", arxiv="1211.3744", bibcode="2013ApJ...763L..32C"))]),

    system("HD 106906",
           images=[pimg("mago2014", "Magellan-MagAO", "Clio2", 3.8,
                        "L'; wide companion discovery", "ADI",
                        paper("Bailey", 2014,
                              "HD 106906 b: A planetary-mass companion outside a massive debris disk",
                              "ApJL 780, L4", arxiv="1312.1265", bibcode="2014ApJ...780L...4B"))]),

    system("Fomalhaut",
           images=[pimg("acs2008", "HST", "ACS", 0.6,
                        "optical; Fomalhaut b source", "coronagraphy",
                        paper("Kalas", 2008,
                              "Optical Images of an Exosolar Planet 25 Light-Years from Earth",
                              "Science 322, 1345", arxiv="0811.1994", bibcode="2008Sci...322.1345K"))]),

    system("AF Lep", categories=(),
           planets=[planet("b", "confirmed",
                           "First planet jointly found via astrometric acceleration + imaging (2023, three groups)")],
           images=[pimg("sphere2023", "Keck", "NIRC2", 3.8,
                        "L' band; discovery via astrometric acceleration + imaging", "ADI",
                        paper("Franson", 2023,
                              "Astrometric Accelerations as Dynamical Beacons: A Giant Planet Imaged Inside the Debris Disk of the Young Star AF Lep",
                              "ApJL 950, L19", arxiv="2302.05420", bibcode="2023ApJ...950L..19F")),
                   pimg("sphere2023-mesa", "VLT-SPHERE", "IRDIS+IFS", 1.65,
                        "near-IR; independent SPHERE discovery", "ADI",
                        paper("Mesa", 2023,
                              "AF Lep b: The lowest-mass planet detected by coupling astrometric and direct imaging data",
                              "A&A 672, A93", arxiv="2302.06213", bibcode="2023A&A...672A..93M")),
                   pimg("sphere2023-derosa", "VLT-SPHERE", "IRDIS", 2.2,
                        "K band; independent discovery via star-hopping RDI", "RDI",
                        paper("De Rosa", 2023,
                              "Direct imaging discovery of a super-Jovian around the young Sun-like star AF Leporis",
                              "A&A 672, A94", arxiv="2302.06332", bibcode="2023A&A...672A..94D")),
                   pimg("gravity2024", "VLTI-GRAVITY", "GRAVITY", 2.2,
                        "K band interferometric detection (GRAVITY)", "interferometry",
                        paper("Balmer", 2024,
                              "VLTI/GRAVITY Observations of AF Lep b: Preference for Circular Orbits, Cloudy Atmospheres, and a Moderately Enhanced Metallicity",
                              "AJ (2025)", arxiv="2411.05917", bibcode=None)),
                   pimg("jwst2024", "JWST", "NIRCam", 4.4,
                        "4.4 um (F444W) coronagraphic detection", "coronagraphy",
                        paper("Franson", 2024,
                              "JWST/NIRCam 4-5 um Imaging of the Giant Planet AF Lep b",
                              "ApJL 974, L11", arxiv="2406.09528", bibcode="2024ApJ...974L..11F"))],
           notes="Independently discovered in 2023 by three groups: Franson+2023 (Keck/NIRC2; "
                 "note image_id af-lep_sphere2023 is that Keck image, historical id), Mesa+2023 "
                 "(VLT/SPHERE) and De Rosa+2023 (VLT/SPHERE star-hopping RDI - not GPI). "
                 "Re-detected with VLTI/GRAVITY (Balmer+2024) and JWST/NIRCam F444W (Franson+2024)."),

    system("HIP 99770", categories=(),
           planets=[planet("b")],
           images=[pimg("scexao2023", "Subaru-SCExAO", "CHARIS", 1.65,
                        "JHK; accelerating-star discovery", "ADI",
                        paper("Currie", 2023,
                              "Direct Imaging and Astrometric Detection of a Gas Giant Planet Orbiting an Accelerating Star",
                              "Science 380, 198", arxiv="2212.00034", bibcode="2023Sci...380..198C"))]),

    system("AB Aur",
           images=[pimg("scexao2022", "Subaru-SCExAO", "CHARIS", 1.65,
                        "NIR; embedded protoplanet candidate", "RDI",
                        paper("Currie", 2022,
                              "Images of embedded Jovian planet formation at a wide separation around AB Aurigae",
                              "Nature Astronomy 6, 751", arxiv="2204.00633", bibcode="2022NatAs...6..751C"))]),

    system("YSES-1", simbad="TYC 8998-760-1", alt_names=("TYC 8998-760-1",),
           region="Lower Cen-Crux", categories=(),
           planets=[planet("b"), planet("c")],
           images=[pimg("sphere2020", "VLT-SPHERE", "IRDIS", 2.1,
                        "K1 band; first multi-planet system imaged around a Sun-like star", "coronagraphy",
                        paper("Bohn", 2020,
                              "Two Directly Imaged, Wide-orbit Giant Planets around the Young, Solar Analog TYC 8998-760-1",
                              "ApJL 898, L16", arxiv="2007.10991", bibcode="2020ApJ...898L..16B"))]),

    system("YSES-2", categories=(),
           planets=[planet("b")],
           images=[pimg("sphere2021", "VLT-SPHERE", "IRDIS", 1.65,
                        "H band discovery", "ADI",
                        paper("Bohn", 2021,
                              "Discovery of a directly imaged planet to the young solar analog YSES 2",
                              "A&A 648, A73", arxiv="2104.08285", bibcode="2021A&A...648A..73B"))]),

    system("GQ Lup", region="Lupus", categories=("protoplanetary",),
           planets=[planet("b", "confirmed", "~10-30 MJup; CPD detected around b")],
           images=[pimg("naco2005", "VLT-NACO", "NACO", 2.2,
                        "Ks band; companion discovery", "other",
                        paper("Neuhauser", 2005,
                              "Evidence for a co-moving sub-stellar companion of GQ Lup",
                              "A&A 435, L13", arxiv="astro-ph/0503691",
                              bibcode="2005A&A...435L..13N"))]),

    system("DH Tau", region="Taurus", categories=("protoplanetary",),
           planets=[planet("b", "confirmed", "~11 MJup wide companion")],
           images=[pimg("subaru2005", "Subaru", "CIAO", 2.2,
                        "K band; companion discovery", "coronagraphy",
                        paper("Itoh", 2005,
                              "A Young Brown Dwarf Companion to DH Tauri",
                              "ApJ 620, 984", arxiv="astro-ph/0411177",
                              bibcode="2005ApJ...620..984I"))]),

    system("CT Cha", region="Chamaeleon", categories=(),
           planets=[planet("b", "confirmed", "~17 MJup — borderline; kept for historical completeness")],
           images=[pimg("naco2008", "VLT-NACO", "NACO", 2.2, "Ks band; companion discovery", "other",
                        paper("Schmidt", 2008,
                              "Direct evidence of a sub-stellar companion around CT Cha",
                              "A&A 491, 311", arxiv="0809.2812", bibcode="2008A&A...491..311S"))]),

    system("1RXS J1609", simbad="1RXS J160929.1-210524", region="Upper Sco",
           categories=(),
           planets=[planet("b", "confirmed", "~8 MJup at 330 au")],
           # NB 2026-07-06: a stray copy-paste record ("tess-c", the AU Mic c TESS
           # light curve, Martioli+2021) used to live here and once resurrected a
           # deleted record — the real one is on au-mic. Keep images empty here.
           images=[]),

    system("HD 135344 A", simbad="HD 135344", alt_names=("HD 135344A",),
           region="Sco-Cen", categories=(),
           planets=[planet("Ab", "confirmed",
                           "~10 MJup at 15-20 au; one of the youngest fully-formed imaged planets (2025). NOT the same star as HD 135344B/SAO 206462!")],
           images=[pimg("sphere2025", "VLT-SPHERE", "IRDIS H23/K12", 1.65,
                        "H2H3/K12; discovery of HD 135344 Ab", "ADI",
                        paper("Stolker", 2025,
                              "Direct imaging discovery of a young giant planet orbiting on Solar System scales",
                              "A&A (2025)", arxiv="2507.06206"))],
           notes="Visual binary with HD 135344B (SAO 206462); the planet orbits the disk-depleted A0 primary."),

    system("COCONUTS-2", simbad="WISEPA J075108.79-763449.6", categories=(),
           planets=[planet("b", "confirmed", "~6 MJup, 7000 au separation")],
           images=[]),

    system("GU Psc", categories=(),
           planets=[planet("b", "confirmed", "~11 MJup at 2000 au")],
           images=[]),
]
