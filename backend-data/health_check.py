#!/usr/bin/env python3
"""System-level integrity checks for diskatlas (complements validate.py).

validate.py checks per-record schema; this checks CROSS-system invariants that
have each caused real data bugs (all found+fixed 2026-07-11):

 1. DUPLICATE SYSTEMS — two entries for the same star. Detected two ways:
    (a) identical `simbad` field on 2+ systems, (b) coordinate pairs closer
    than --pair-arcsec (default 8"). Real hits: gamma-oph+hd-161868,
    gw-lup+sz-71, mp-mus+pds-66, tyc-9340-437-1+cp-72-2713, v606-ori+so-1274,
    j16070854+lup-160708, rx-j1604-3-2130+j160421-7, j11095340+ced112-irs4.
    Known TRUE close pairs (distinct stars) live in ALLOW_PAIRS.
 2. COORDS vs DESIGNATION — if any name/simbad/alt encodes a position
    (2MASS/WISE JHHMMSSss±DDMMSSs; centiseconds, NO decimal point), the parsed
    position must match ra_deg/dec_deg. A naive HH MM SSSS parse puts systems
    DEGREES off (bug hit 9 Kurtovic-gallery systems). Coarse catalog names
    (1RXS/HSCS/RX-J ~0.1' precision) get a 60" allowance.
 3. NAMING CONVENTIONS — catalog prefix+number spaced ("Sz 113" not "Sz113");
    "IRS <n>" spaced; Bayer names use 3-letter constellation abbreviations
    (gamma Oph, not gamma Ophiuchi); no bare RA-only J-names ("J16000236");
    `simbad` must be a resolvable identifier (never a bare J-number);
    JHHMM±DDMM monikers carry BOTH halves; exact display-name collisions.
 4. HYGIENE — placeholder notes ("AUTO-CREATED"), double/trailing spaces.

Usage:  python3 backend-data/health_check.py [--pair-arcsec 8]
Exit 1 on any finding (run it with validate.py after batch ingestions).
"""
import argparse, glob, json, math, re, sys
from collections import defaultdict

# distinct stars that legitimately sit within the pair threshold
ALLOW_PAIRS = {
    frozenset(("hk-tau", "hk-tau-b")),      # 2.3" binary, separate disks
    frozenset(("mho-1", "mho2")),           # ~4" Taurus pair
    frozenset(("sz-65", "sz-66")),          # 6.4" Lupus pair
    frozenset(("gy-263", "oph-irs43")),     # 6.9" pair: GY 263 transition disk
                                            # NW of the IRS 43 binary (eDisk X)
    frozenset(("s68nb1", "s68nb2")),        # 5.4" pair: distinct Class 0 + Class I
                                            # protostars in the S68N clump (Aso 2019)
}
COARSE = ("1RXS", "HSCS", "RX J", "RXJ", "JCMTSE", "BKLT")  # + single-dish JCMT ~15" beam; BKLT truncates RA seconds (up to ~15" off)    # ~arcmin-precision catalog names

def parse_pos_name(s):
    """JHHMMSSss±DDMMSSs (2MASS-style, centisecond RA / 0.1\" Dec) -> deg."""
    m = re.search(r"J\s?(\d{2})(\d{2})(\d{2}(?:\.\d+)?)(\d*)\s*([+-])\s?"
                  r"(\d{2})(\d{2})(\d{2}(?:\.\d+)?)(\d*)", (s or "").replace(" ", ""))
    if not m:
        return None
    hh, mm, ss, ssx, sgn, dd, dm, ds, dsx = m.groups()
    rss = float(ss) if "." in ss else float(ss + ("." + ssx if ssx else ""))
    dss = float(ds) if "." in ds else float(ds + ("." + dsx if dsx else ""))
    ra = (int(hh) + int(mm) / 60 + rss / 3600) * 15
    dec = (int(dd) + int(dm) / 60 + dss / 3600) * (1 if sgn == "+" else -1)
    return ra, dec

def sep_arcsec(ra1, dec1, ra2, dec2):
    return math.hypot((ra1 - ra2) * math.cos(math.radians(dec1)), dec1 - dec2) * 3600

NOSPACE_PREFIXES = r"(Sz|MHO|SVS|GSS|BHR|WSB|DoAr|GY|Hn|Ced|CIDA|ROXs?)"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair-arcsec", type=float, default=8.0)
    args = ap.parse_args()

    systems = []
    for f in sorted(glob.glob("data/systems/*.json")):
        systems.append(json.load(open(f)))
    bad = []

    # 1a. identical simbad ids
    by_simbad = defaultdict(list)
    for s in systems:
        if s.get("simbad"):
            by_simbad[s["simbad"]].append(s["id"])
    for sm, ids in by_simbad.items():
        if len(ids) > 1:
            bad.append(f"DUP-SIMBAD  {ids} share simbad={sm!r} — same star twice?")

    # 1b. coordinate proximity
    for i in range(len(systems)):
        for j in range(i + 1, len(systems)):
            a, b = systems[i], systems[j]
            if abs(a["dec_deg"] - b["dec_deg"]) > args.pair_arcsec / 3600 * 1.5:
                continue
            sep = sep_arcsec(a["ra_deg"], a["dec_deg"], b["ra_deg"], b["dec_deg"])
            if sep < args.pair_arcsec and frozenset((a["id"], b["id"])) not in ALLOW_PAIRS:
                bad.append(f"DUP-COORD   {a['id']} <-> {b['id']} sep={sep:.1f}\" — same star twice?")

    # 2. coords vs positional designation
    for s in systems:
        for cand in [s.get("name"), s.get("simbad")] + (s.get("alt_names") or []):
            p = parse_pos_name(cand)
            if not p:
                continue
            tol = 60.0 if any((cand or "").startswith(c) for c in COARSE) else 5.0
            sep = sep_arcsec(p[0], p[1], s["ra_deg"], s["dec_deg"])
            if sep > tol:
                bad.append(f"COORD-NAME  {s['id']}: stored coords {sep:.0f}\" from designation {cand!r}")
            break  # first parseable designation is authoritative

    # 3. naming conventions
    names = defaultdict(list)
    for s in systems:
        nm = s.get("name", "")
        names[nm].append(s["id"])
        if re.match(rf"^{NOSPACE_PREFIXES}\d", nm):
            bad.append(f"NAME-SPACE  {s['id']}: {nm!r} — catalog prefix needs a space")
        if re.search(r"IRS\d", nm):
            bad.append(f"NAME-SPACE  {s['id']}: {nm!r} — 'IRS <n>' needs a space")
        if re.search(r"\b(Ophiuchi|Gruis|Tauri|Aurigae|Pictoris|Corvi|Andromedae|Centauri|Eridani|Ceti)\b", nm):
            bad.append(f"NAME-BAYER  {s['id']}: {nm!r} — use 3-letter constellation abbrev")
        if re.fullmatch(r"[Jj]\d{6,9}", nm.replace(" ", "")):
            bad.append(f"NAME-BAREJ  {s['id']}: {nm!r} — RA-only J-name (add Dec half / real name)")
        if re.fullmatch(r"[Jj]\d{6,9}", (s.get("simbad") or "").replace(" ", "")):
            bad.append(f"SIMBAD-BAD  {s['id']}: simbad={s.get('simbad')!r} not a resolvable id")
        if "  " in nm or nm != nm.strip():
            bad.append(f"NAME-WS     {s['id']}: {nm!r} — stray whitespace")
    for nm, ids in names.items():
        if len(ids) > 1:
            bad.append(f"NAME-DUP    {ids} share display name {nm!r}")

    # 4b. placeholder-notes backlog — a WARNING (research debt, not corruption)
    todo = [s["id"] for s in systems if "AUTO-CREATED" in (s.get("notes") or "")]

    if bad:
        print(f"{len(bad)} finding(s):")
        for b in bad:
            print("  " + b)
        if todo:
            print(f"(+ {len(todo)} systems with placeholder AUTO-CREATED notes — backlog, not fatal)")
        sys.exit(1)
    msg = f"OK — {len(systems)} systems pass all cross-system checks"
    if todo:
        msg += f"  [backlog: {len(todo)} placeholder-notes systems]"
    print(msg)

if __name__ == "__main__":
    main()
