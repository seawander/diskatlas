#!/usr/bin/env python3
"""CI guard: every deployed image referenced by frontend/data.js is valid.

For each image record with a non-null `file`, assert:
  * the file exists on disk            -> ERROR if missing (broken <img> live)
  * the extension is .png/.jpg/.jpeg   -> ERROR otherwise
  * the longest side is <= 640 px      -> ERROR otherwise (hard spec cap)
  * the file is <= ~300 KB             -> WARN only (borderline crops exist)

Dimensions are read straight from the PNG/JPEG header (stdlib only, no Pillow).
If a file's dimensions can't be parsed, the size cap is skipped rather than
failing spuriously.

Exit 1 if any ERROR; warnings are informational.
"""
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_JS = ROOT / "frontend" / "data.js"

MAX_SIDE = 640          # hard cap (data/README.md)
SOFT_BYTES = 300 * 1024  # ~300 KB soft cap -> warning only
OK_EXT = {".png", ".jpg", ".jpeg"}


def png_size(head):
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def jpeg_size(data):
    if data[:2] != b"\xff\xd8":
        return None
    i, n = 2, len(data)
    while i + 9 < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        # SOF0..SOF15 carry the frame dimensions (skip DHT/DAC/RST/SOI/EOI)
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg
    return None


def dims(path):
    with open(path, "rb") as f:
        blob = f.read()
    if path.suffix.lower() == ".png":
        return png_size(blob[:26])
    return jpeg_size(blob)


def main():
    text = DATA_JS.read_text(encoding="utf-8")
    payload = json.loads(text[text.index("{"):text.rindex("}") + 1])
    errors, warns, n = [], [], 0
    for s in payload.get("systems", []):
        for im in s.get("images", []):
            f = im.get("file")
            if not f:
                continue
            n += 1
            tag = f"{s.get('id')}/{im.get('image_id')}"
            p = ROOT / f
            if not p.exists():
                errors.append(f"{tag}: missing file {f}")
                continue
            if p.suffix.lower() not in OK_EXT:
                errors.append(f"{tag}: unexpected extension {p.suffix}")
                continue
            size = p.stat().st_size
            wh = dims(p)
            if wh:
                w, h = wh
                if max(w, h) > MAX_SIDE:
                    errors.append(f"{tag}: {w}x{h}px exceeds {MAX_SIDE}px cap")
                elif size > SOFT_BYTES:
                    warns.append(f"{tag}: {size // 1024} KB (> ~300 KB)")
            elif size > SOFT_BYTES:
                warns.append(f"{tag}: {size // 1024} KB (> ~300 KB)")

    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e, file=sys.stderr)
    print(f"\nchecked {n} deployed images: {len(errors)} errors, {len(warns)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
