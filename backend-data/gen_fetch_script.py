#!/usr/bin/env python3
"""Generate backend-data/fetch_sources.sh + backend-data/simbad_script.txt.

fetch_sources.sh must be run OUTSIDE the sandbox (host with internet):
downloads every referenced arXiv source tarball into images/_sources/arxiv/
and fetches SIMBAD coordinates for all systems into data/simbad_raw.txt.
Idempotent: skips already-downloaded tarballs.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from seeds import ALL_BLOCKS, ALL_SYSTEMS   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SYS_DIR = ROOT / "data" / "systems"


def arxiv_ids():
    ids = set()

    def add(p):
        if p and p.get("arxiv"):
            ids.add(p["arxiv"])

    for b in ALL_BLOCKS:
        add(b["paper"])
    for s in ALL_SYSTEMS:
        for im in s.get("images", []):
            add(im.get("paper"))
    if SYS_DIR.exists():
        for f in SYS_DIR.glob("*.json"):
            for im in json.loads(f.read_text()).get("images", []):
                add(im.get("paper"))
    return sorted(ids)


def simbad_names():
    names = []

    def add(n):
        if n and n not in names:
            names.append(n)

    for b in ALL_BLOCKS:
        for m in b["members"]:
            name, ov = (m, {}) if isinstance(m, str) else m
            add(ov.get("simbad") or name)
    for s in ALL_SYSTEMS:
        add(s.get("simbad") or s["name"])
    if SYS_DIR.exists():
        for f in SYS_DIR.glob("*.json"):
            s = json.loads(f.read_text())
            if s.get("ra_deg") is None:
                add(s.get("simbad") or s["name"])
    return names


def main():
    ids = arxiv_ids()
    names = simbad_names()

    (Path(__file__).parent / "simbad_script.txt").write_text(
        'format object form1 "%IDLIST(1)|%COO(d;A D)|%PLX(V)|%SP(S)|'
        '%FLUXLIST(U,B,V,G,R,I,J,H,K;N=F,)"\n'
        + "".join(f"echodata ###{n}\nquery id {n}\n" for n in names))

    sh = ["#!/usr/bin/env bash",
          "# Run this ON THE HOST (normal internet), from the backend-data/ directory:",
          "#   bash fetch_sources.sh",
          "set -u",
          'cd "$(dirname "$0")"',
          "mkdir -p ../images/_sources/arxiv",
          'UA="disk-atlas/1.0 (personal research use)"',
          "ok=0; fail=0",
          "for id in \\"]
    sh += [f"  {i} \\" for i in ids]
    sh += ["  ; do",
           '  out="../images/_sources/arxiv/${id/\\//_}.tar"',
           '  if [ -s "$out" ]; then echo "skip $id"; ok=$((ok+1)); continue; fi',
           '  echo "fetching $id"',
           '  if curl -fsSL -A "$UA" --retry 3 -o "$out" "https://arxiv.org/e-print/$id"; then',
           "    ok=$((ok+1))",
           "  else",
           '    echo "  FAILED $id"; fail=$((fail+1)); rm -f "$out"',
           "  fi",
           "  sleep 2",
           "done",
           'echo "tarballs ok=$ok fail=$fail"',
           "# --- extra non-arXiv sources (backend-data/fetch_extra.txt: URL<TAB>relative_dest) ---",
           'if [ -f fetch_extra.txt ]; then',
           '  while IFS=$\'\\t\' read -r url dest; do',
           '    case "$url" in \\#*|"") continue;; esac',
           '    if [ -s "../$dest" ]; then echo "skip extra $dest"; continue; fi',
           '    mkdir -p "$(dirname "../$dest")"',
           '    echo "fetching extra $dest"',
           '    curl -fsSL -A "$UA" --retry 3 -o "../$dest" "$url" || { echo "  FAILED $url"; rm -f "../$dest"; }',
           '    sleep 1',
           '  done < fetch_extra.txt',
           'fi',
           "# --- SIMBAD coordinates ---",
           'curl -fsS "https://simbad.cds.unistra.fr/simbad/sim-script" \\',
           '  --data-urlencode "script@simbad_script.txt" > ../data/simbad_raw.txt \\',
           '  && echo "SIMBAD ok -> data/simbad_raw.txt" || echo "SIMBAD FAILED"',
           'echo "Done. Next (in the sandbox/agent): python3 parse_simbad.py && python3 extract_sources.py"']
    out = Path(__file__).parent / "fetch_sources.sh"
    out.write_text("\n".join(sh) + "\n")
    out.chmod(0o755)
    print(f"fetch_sources.sh: {len(ids)} arXiv ids; simbad_script.txt: {len(names)} names")


if __name__ == "__main__":
    main()
