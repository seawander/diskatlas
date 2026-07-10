"""Normalize free-text facility/instrument strings to canonical facet keys.

- fac_keys: list of AAS facility keywords (https://journals.aas.org/facility-keywords/,
  Keyword column) where the platform appears there; plain telescope name otherwise.
  Joint "A + B" observations yield multiple keys (the frontend shows the record under
  both). VLT and VLTI are distinct keys; the frontend applies the subset rule
  (selecting VLT also matches VLTI, not vice versa).
- instr_key: one canonical instrument family per record (SPHERE not IRDIS/ZIMPOL;
  interferometer/single-dish facilities double as their own "instrument", e.g. ALMA).

Applied by build.py when writing frontend/data.js; the data/systems/*.json files keep
their original free-text fields.
"""
import re

# exact-match table for facility strings currently in the data -----------------
FAC_TABLE = {
    "VLT-SPHERE": ["VLT"], "VLT-NACO": ["VLT"], "VLT-MUSE": ["VLT"],
    "VLT-ISAAC": ["VLT"], "VLT": ["VLT"],
    "VLTI": ["VLTI"], "VLTI-GRAVITY": ["VLTI"],
    "VLTI-GRAVITY + VLT-SPHERE": ["VLTI", "VLT"],
    "VLT-SPHERE + ALMA": ["VLT", "ALMA"],
    "VLT-ERIS/JWST-NIRCam/VLT-SPHERE": ["VLT", "JWST"],
    "ALMA": ["ALMA"], "ALMA/SMA": ["ALMA", "SMA"], "SMA": ["SMA"],
    "SMA/PdBI/VLA": ["SMA", "IRAM:Interferometer", "VLA"],
    "NOEMA": ["IRAM:NOEMA"], "IRAM-PdBI": ["IRAM:Interferometer"], "VLA": ["VLA"], "CARMA": ["CARMA"], "BIMA": ["BIMA"],
    "ATCA": ["ATCA"], "CSO": ["CSO"], "JCMT": ["JCMT"],
    "HST": ["HST"], "JWST": ["JWST"],
    "Herschel": ["Herschel"], "Spitzer": ["Spitzer"], "WISE": ["WISE"],
    "TESS": ["TESS"], "TESS+Spitzer": ["TESS", "Spitzer"],
    "Gemini-GPI": ["Gemini:South"], "Gemini-NICI": ["Gemini:South"],
    "Gemini-South": ["Gemini:South"], "Gemini-NIRI": ["Gemini:Gillett"],
    "Gemini-GMOS/CFHT": ["Gemini:Gillett", "CFHT"],
    "Gemini-GPI + Magellan-MagAO": ["Gemini:South", "Magellan:Clay"],
    "Subaru": ["Subaru"], "Subaru Telescope": ["Subaru"],
    "Subaru-HiCIAO": ["Subaru"], "Subaru-SCExAO": ["Subaru"],
    "LBT": ["LBT"], "LBTI": ["LBT"],
    "Magellan": ["Magellan:Clay"], "MagAO": ["Magellan:Clay"],
    "Magellan-MagAO": ["Magellan:Clay"], "Magellan-MagAO-X": ["Magellan:Clay"],
    "Magellan I (Baade) 6.5m": ["Magellan:Baade"],
    "Las Campanas 2.5m du Pont": ["Du Pont"],
    "CFHT": ["CFHT"], "AEOS": ["AEOS"], "UH 2.2m": ["UH:2.2m"],
    "Palomar": ["Hale"], "Palomar 5-m Hale Telescope": ["Hale"],
    "Pan-STARRS1": ["PS1"], "VISTA": ["ESO:VISTA"], "CTIO-1.5m": ["CTIO:1.5m"],
}

_MM_FACILITY_INSTR = {  # facilities that double as the canonical instrument
    "ALMA": "ALMA", "SMA": "SMA", "VLA": "VLA", "CARMA": "CARMA", "BIMA": "BIMA",
    "ATCA": "ATCA", "IRAM:NOEMA": "NOEMA", "IRAM:Interferometer": "PdBI",
    "OVRO": "OVRO",
}

INSTR_RULES = [  # (substring-of-lowercased(facility+instrument), canonical family)
    ("magao-x", "MagAO-X"), ("visao", "MagAO"), ("magao", "MagAO"),
    ("sphere", "SPHERE"),  # plain/ambiguous SPHERE; sub-instruments handled in instr_key()
    ("gravity", "GRAVITY"), ("matisse", "MATISSE"), ("pionier", "PIONIER"),
    ("midi", "MIDI"), ("amber", "AMBER"),
    ("gpi", "GPI"), ("nici", "NICI"), ("niri", "NIRI"),
    ("t-recs", "T-ReCS"), ("trecs", "T-ReCS"), ("michelle", "Michelle"), ("gmos", "GMOS"),
    ("nircam", "NIRCam"), ("nirspec", "NIRSpec"), ("miri", "MIRI"),
    ("pacs", "PACS"), ("stis", "STIS"), ("nicmos", "NICMOS"), ("acs", "ACS"), ("wfc3", "WFC3"),
    ("wfpc2", "WFPC2"), ("foc", "FOC"),
    ("naco", "NACO"), ("conica", "NACO"), ("muse", "MUSE"), ("visir", "VISIR"),
    ("near", "VISIR"), ("eris", "ERIS"), ("isaac", "ISAAC"), ("sofi", "SofI"),
    # SCExAO platform instruments (Miles Lucas 2026-07-09): report as SCExAO/<sub>,
    # matching the SPHERE/<sub> convention. VAMPIRES before the plain-scexao fallback.
    ("hiciao", "HiCIAO"), ("vampires", "SCExAO/VAMPIRES"), ("charis", "SCExAO/CHARIS"),
    ("mec", "SCExAO/MEC"), ("scexao", "SCExAO/CHARIS"),
    ("comics", "COMICS"), ("ircs", "IRCS"), ("ciao", "CIAO"),
    ("nirc2", "NIRC2"), ("lws", "LWS"), ("osiris", "OSIRIS"),
    ("lmircam", "LMIRCam"), ("ales", "LMIRCam"), ("nomic", "LMIRCam"), ("lbti", "LMIRCam"),
    ("p1640", "P1640"), ("project 1640", "P1640"),
    ("pacs", "PACS"), ("spire", "PACS"), ("mips", "MIPS"),
    ("scuba", "SCUBA-2"), ("sharc", "SHARC-II"),
    ("simon", "SIMON"), ("photometer", "TESS"), ("tess", "TESS"), ("wise", "WISE"),
    ("gpc", "GPC1"), ("pan-starrs", "GPC1"), ("vista", "VIRCAM"),
    ("wfcam", "WFCAM"),
    ("lyot", "Lyot"), ("mirlin", "MIRLIN"), ("mirac", "MIRAC"),
]


def fac_keys(facility, instrument=""):
    f = (facility or "").strip()
    il = (instrument or "").lower()
    if f in FAC_TABLE:
        keys = list(FAC_TABLE[f])
    else:  # heuristics for strings introduced later
        fl = f.lower()
        if fl.startswith("vlti"):
            keys = ["VLTI"]
        elif fl.startswith("vlt"):
            keys = ["VLT"]
        elif fl.startswith("subaru"):
            keys = ["Subaru"]
        elif fl.startswith("gemini"):
            keys = ["Gemini:South" if any(x in fl + il for x in ("gpi", "nici", "t-recs", "south"))
                    else "Gemini:Gillett"]
        elif fl.startswith("keck"):
            keys = ["Keck:I" if ("lws" in il or "osiris" in il) else "Keck:II"]
        elif fl.startswith("magellan") or "magao" in fl:
            keys = ["Magellan:Baade" if "baade" in fl else "Magellan:Clay"]
        elif "palomar" in fl or fl == "hale":
            keys = ["Hale"]
        elif "du pont" in fl:
            keys = ["Du Pont"]
        elif "ntt" in fl:
            keys = ["NTT"]
        else:
            keys = [f or "?"]
    # Keck table entries need the per-instrument split too
    if f in ("Keck", "Keck-NIRC2"):
        keys = ["Keck:I" if ("lws" in il or "osiris" in il) else "Keck:II"]
    return keys


_WORDY = {"acs", "foc", "near", "mec", "lws", "gpc", "ciao"}  # substring-collision-prone

def instr_key(facility, instrument):
    text = ((facility or "") + " " + (instrument or "")).lower()
    # SPHERE sub-instrument split (requested 2026-07-08): report IRDIS / ZIMPOL / IFS
    # separately as SPHERE/<sub>. IRDIS and ZIMPOL are SPHERE-only; IFS is gated on the
    # SPHERE context so Gemini/GPI's own IFS (e.g. "Gemini-GPI / IFS pol") stays GPI.
    if "zimpol" in text:
        return "SPHERE/ZIMPOL"
    if "irdis" in text:
        return "SPHERE/IRDIS"
    if "sphere" in text and "ifs" in text:
        return "SPHERE/IFS"
    for sub, fam in INSTR_RULES:
        if sub in _WORDY:
            if re.search(r"(?<![a-z0-9])" + re.escape(sub) + r"(?![a-z0-9])", text):
                return fam
        elif sub in text:
            return fam
    for k in fac_keys(facility, instrument):
        if k in _MM_FACILITY_INSTR:
            return _MM_FACILITY_INSTR[k]
    ins = (instrument or "").strip()
    return re.split(r"[/(]", ins)[0].strip() or "other"
