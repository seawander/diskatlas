"""Shared helpers for seed modules."""
import re
import unicodedata

GREEK = {"α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon",
         "ζ": "zeta", "η": "eta", "θ": "theta", "κ": "kappa", "λ": "lambda",
         "μ": "mu", "π": "pi", "ρ": "rho", "σ": "sigma", "τ": "tau", "φ": "phi",
         "χ": "chi", "ψ": "psi", "ω": "omega"}


def slugify(name: str) -> str:
    s = name.strip()
    for g, latin in GREEK.items():
        s = s.replace(g, latin)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def paper(first_author, year, title, journal=None, arxiv=None, bibcode=None, verify=False):
    p = {"first_author": first_author, "year": year, "title": title,
         "journal": journal, "arxiv": arxiv, "bibcode": bibcode}
    if verify:
        p["_verify"] = True   # validate.py will flag: metadata needs confirmation
    return p


def survey(survey_name, paper_dict, image_defaults, members, region=None,
           categories=("protoplanetary",), notes=None):
    """A survey block. members: list of str or (display_name, overrides_dict).

    overrides_dict may set: simbad, region, categories, image_id, wavelength_um,
    wavelength_label, alt_names, notes, planets.
    """
    return {"survey": survey_name, "paper": paper_dict,
            "image_defaults": dict(image_defaults), "members": list(members),
            "region": region, "categories": list(categories), "notes": notes}


def system(name, images, simbad=None, alt_names=(), region=None,
           categories=(), planets=(), notes=None):
    """A fully explicit individual system (for non-survey classics)."""
    return {"individual": True, "name": name, "simbad": simbad or name,
            "alt_names": list(alt_names), "region": region,
            "categories": list(categories), "planets": list(planets),
            "images": list(images), "notes": notes}


def img(image_id_suffix, type_, facility, instrument, wl_um, wl_label, technique,
        paper_dict, survey=None, credit=None, file_status="pending"):
    """One image record; system id prefix is prepended by make_systems."""
    return {"image_id_suffix": image_id_suffix, "type": type_, "facility": facility,
            "instrument": instrument, "wavelength_um": wl_um,
            "wavelength_label": wl_label, "technique": technique, "survey": survey,
            "credit": credit, "file_status": file_status, "paper": paper_dict}


def planet(name, status="confirmed", note=None):
    p = {"name": name, "status": status}
    if note:
        p["note"] = note
    return p
