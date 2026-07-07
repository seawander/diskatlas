# images/

## Layout

```
_sources/arxiv/<arxivid>.tar        ← raw downloads (host-fetched; keep, they're the originals)
_sources/extracted/<arxivid>/       ← unpacked tarballs (regenerable; safe to delete)
<system_id>/<image_id>.png          ← final cropped panels served by the frontend
```

## Final panel specs

- ≤ 640 px longest side, target ~200–450 px; ≤ ~300 KB each (they're thumbnails —
  users click through to the paper for full quality).
- PNG preferred. Keep panel label/scale bar if legible; crop colorbars/axes when they
  belong to a shared figure frame.
- Filename must equal the `image_id` in the system's JSON + `.png`.
- One folder per `system_id`, even for a single image.

## Provenance

Every file here must be traceable: the corresponding image record's `credit` field states
paper + figure ("Andrews et al. 2018, Fig. 3 (crop)"). No press-release images.
Low-res crops with citation = fair scholarly use; originals © authors/journals.

## Do not

- Do not upscale, annotate, recolor, or composite panels.
- Do not exceed ~300 KB per file (keeps the whole atlas portable).
- Do not delete `_sources/arxiv/` tarballs casually — re-downloading needs host access.
