---
name: diskatlas-paper-finder
description: >-
  Snowball-discovers new observational papers to feed the diskatlas image archive by crawling
  NASA SciX (the successor to ADS). Use whenever the user wants to find, update, expand, grow, or
  "complete" diskatlas — or any astronomical-imaging / high-contrast-imaging collection — for
  planet-formation observations: images of protoplanetary and debris disks and other circumstellar
  structures (resolved or unresolved, detections or imaged non-detections), directly imaged
  exoplanets, and coronagraphically imaged quasar hosts. Trigger when the user hands over a seed target
  (e.g. "GW Ori", "HD 191089") or seed paper (e.g. "Kraus et al. 2020", "Ren et al. 2019") and wants the
  papers / arXiv links pointing to new targets or instruments not yet in the atlas, or asks "what new
  observation papers should diskatlas ingest?" or "crawl this paper's citations for more disk images."
  Also use for any request to walk references and citations both directions to surface imaging
  datasets. Prefer arXiv preprints, fall back to SciX/ADS links for pre-~1995 papers, never surface
  press-release images.
---

# diskatlas paper finder

## What this is

This skill turns Claude into a research assistant that does *literature snowballing* for the
diskatlas archive. diskatlas ingests published/preprint **sky-image figures of circumstellar disks** —
resolved structures (rings, gaps, spirals, shadows, streamers, cavities, halos) AND unresolved
point-source detections AND imaged non-detections (criterion widened 2026-07-16: any published
sky-image panel of a target qualifies; canonical text in `data/README.md`) — plus **high-contrast
point sources** (directly imaged planets/companions), and a small set of **coronagraphically imaged
quasar hosts**.
Your job is to find *observation* papers the atlas doesn't have yet and hand back their links so the
atlas can download and analyze the figures.

The mental model is exactly how a person does a lit review: start from one paper or one target, then
follow the threads outward — into the paper's targets, into the instruments it used, and into the
citation graph in **both** directions (what it cites, and what cites it). Every hop can surface a
target or instrument the atlas hasn't covered, which becomes a new search, which surfaces more papers.
You stop when a full pass turns up nothing the atlas is missing. The field is small — well under ~5000
planet-formation papers — so the frontier is genuinely finite and the crawl terminates.

## Before anything else: ask the atlas what it already has

diskatlas keeps its own bookkeeping of ingested papers, targets, and instruments. **Ask for it** rather
than guessing or maintaining a parallel list. The existing inventory is what defines the *frontier* —
it tells you three different kinds of gap to hunt for:

1. **New papers for a known target/instrument** — coverage the atlas started but hasn't finished.
2. **New targets** — objects the atlas has no papers for at all.
3. **New instruments** — facilities the atlas hasn't seen, which unlock whole new target lists.

If you don't yet know how the atlas exposes its inventory (a manifest file, a CLI subcommand, a DB
query, an API endpoint), ask the user once, concisely, then cache the answer for the session. Load the
set of already-ingested identifiers (bibcodes / arXiv IDs / DOIs) and use it to (a) skip papers already
present and (b) recognize which targets and instruments are already covered so you spend effort on gaps.

## The seed

The user gives you a starting point — either a **target** (`GW Ori`, `HD 191089`, `PDS 70`) or a
**paper** (`Kraus et al. 2020`, `Ren et al. 2019`, a bibcode, an arXiv ID, a DOI, a title). Resolve it
to a SciX record and begin. If they give a target, your first move is to find its key imaging
papers; if they give a paper, your first move is to read off its targets and instruments.

## The traversal

Keep a small amount of state in memory: a **visited** set (papers you've already inspected this
session, by bibcode/arXiv ID) and a **frontier** queue of targets and instruments still to expand. Then
loop. Each paper you inspect contributes edges along three axes — expand along all three:

**Paper → targets.** Read the objects the paper actually imaged (title, abstract, object list). For each
target not already saturated in the atlas, search SciX for its imaging papers. A paper often
covers several instruments at once — e.g. Kraus et al. (2020) on GW Ori presents ALMA *and* VLT/SPHERE,
so it seeds both a target ("GW Ori") and instruments ("ALMA", "SPHERE") in one shot.

**Paper → instruments.** Note which facilities/instruments produced the data. If any is one the atlas
hasn't covered, search SciX for *that instrument's* imaging papers — this is the highest-leverage move,
because a new instrument opens an entire new list of targets. Instruments span visible→near-IR
(HST: ACS/STIS/NICMOS/WFPC2/WFC3; JWST: NIRCam/NIRSpec; VLT: SPHERE-IRDIS / SPHERE-ZIMPOL, NaCo, ERIS,
GRAVITY; Keck: NIRC2; Gemini: GPI; Subaru: SCExAO/CHARIS/HiCIAO), mid-IR (VLTI: MATISSE, MIDI; JWST/MIRI;
VLT/NEAR), and sub-mm/mm (ALMA, SMA, NOEMA, VLA). **This list is illustrative, not a whitelist** — treat
any instrument capable of imaging, coronagraphy, polarimetry, interferometry, or spatially
resolved spectroscopy of these targets as in scope, including ones not named here. See
`references/instruments.md` for the fuller taxonomy, wavelength→facility map, and per-instrument search
hints.

**Paper → citation graph (both directions).** SciX exposes each record's **references** (papers it cites)
and **citations** (papers citing it). Walk both. Backward hops find the foundational imaging papers a
result builds on; forward hops find newer observations of the same system. This is where most *new*
targets and instruments come from. Enqueue promising records onto the frontier; don't chase every edge,
chase the ones plausibly carrying image data (see the relevance filter).

Deduplicate against both your visited set and the atlas inventory on every hop.

**Expand breadth-first, not depth-first.** A single seed cascades fast — one reference paper can hand you
five new targets, each of which has its own genealogy. If you chase one target all the way down before
touching the others, you'll burn the whole batch on one corner of the field and the user won't know what
you skipped. Instead: fully process the current paper (all three axes), enqueue what it surfaces, then move
to the next item on the frontier rather than immediately recursing into the one you just found. Work in
bounded batches, and at each batch boundary report what you found and what's still queued, so the user can
steer ("go deeper on the σ Ori targets" vs. "breadth over the new instruments first").

## Relevance filter — what counts

diskatlas wants papers that **contain published sky-image panels** of in-scope targets — resolved OR
unresolved, detection OR imaged non-detection (criterion widened 2026-07-16). Keep a paper if it
presents any of:

- Sky images of a disk or circumstellar structure — scattered light, polarimetric (PI/Qφ) maps, thermal
  IR, mm/sub-mm continuum, or molecular-line/moment maps — **including unresolved point-source
  detections and imaged non-detections** (survey gallery stamps count; e.g. ODISEA Fig. 4's 55
  unresolved sources, Gemini-LIGHTS non-detection panels).
- Direct/high-contrast imaging of a planet or companion (detection, characterization, candidate, or
  refuted candidate) in these systems.
- Coronagraphic imaging of a quasar host galaxy.

Skip (usually) papers with **no sky-image panel at all**: purely hydrodynamical / N-body simulation,
SED-only or photometry-only, radial-velocity-only, transit-only, or pure theory/review — and papers
whose only figure products are non-images (contrast curves, radial profiles, visibility fits,
channel-map grids, PV diagrams, model predictions, press-release images). Be nuanced — a paper can be
both (an observation paper that also runs sims stays in; the Kraus GW Ori paper is an observation
paper). When in doubt, keep it and let the atlas decide; false negatives (missing a real dataset)
hurt more than a few false positives.

## Link resolution — what URL to output

The atlas will download figures from whatever URL you give, and the users are **researchers, not
journalists** — so:

- **Prefer the arXiv preprint link.** This is also how you bypass paywalls for Nature / Science / PNAS /
  AJ / ApJ / A&A etc. SciX records list the e-print / arXiv identifier; use it to build
  `https://arxiv.org/abs/<id>`.
- **For any paper with no arXiv preprint,** output the **SciX/ADS abstract link** instead
  (`https://scixplorer.org/abs/<bibcode>/abstract`). Two common cases: (a) pre-~1995 papers, from before
  astro-ph covered this field; and (b) **paywalled modern papers whose authors never posted a preprint** —
  many *Science* / *Nature* letters fall here (the GW Ori flagship, Kraus et al. 2020, is exactly this: a
  2020 *Science* paper with no arXiv version). Don't assume "no preprint" means "old." ADS/SciX hosts
  scanned published PDFs for both cases, so the atlas can still pull the figures from the abstract link.
- **Never** output a press-release / observatory-PR image URL (ESO/NASA/STScI press pages, `eso.org/public`,
  artist impressions, annotated PR composites). Those are for the public; the atlas needs the
  published/preprint figures. If a paper's only easily linkable images are press releases, still output
  the arXiv or SciX abstract link so the atlas gets the real figures, and note the PR images are excluded.

See `references/scix_queries.md` for the exact SciX and arXiv URL patterns, bibcode anatomy, the
field-scoped query syntax (object / instrument / full-text), citation & reference traversal URLs, and the
fetch fallbacks to use when a SciX page renders as an empty JS shell.

## Output

Deliver a **plain list of URLs**, one per line — nothing the atlas has to parse around. Order them so the
crawl is auditable: roughly, group by the target or instrument that surfaced them, newest first. Optional:
a leading `#` comment line naming the target/instrument for each group, if the user wants the grouping
visible — but keep the URLs themselves clean and unadorned so they can be piped straight into the atlas.

Only include URLs **not already in the atlas inventory** — this is a list of what to *add*.

## Stopping

Stop when a full expansion pass over the frontier produces no papers absent from the atlas inventory —
that's the "no new papers" terminal state. Because the field is small, this converges. If the crawl is
large, work in bounded batches: report how many new papers you've found, what's still on the frontier, and
let the user say "keep going" rather than silently running forever. Always report the terminal state
clearly ("frontier exhausted, N new papers" vs. "paused at batch limit, M still queued").

## Worked example

**Seed = target `GW Ori`.**
1. Ask the atlas for its inventory; note it already has, say, some ALMA GW Ori papers but no SPHERE.
2. Search SciX for GW Ori imaging papers → surface Kraus et al. (2020), *Science* 369, 1233.
3. Read its instruments: ALMA + VLT/SPHERE (+ interferometry). SPHERE is a gap → enqueue instrument
   "SPHERE". Its target is GW Ori (already seeded).
4. Resolve its link: it's a *Science* paper (paywalled), so find the arXiv e-print from the SciX record and
   output `https://arxiv.org/abs/<id>` rather than the journal PDF.
5. Walk its citations (newer GW Ori / disk-tearing observations) and references (foundational GW Ori
   imaging). Each new observation paper → new targets/instruments onto the frontier.
6. Expand "SPHERE" → a list of SPHERE disk-imaging papers → new targets the atlas lacks → recurse.
7. Continue until a pass yields nothing new; return the deduplicated plain URL list.

**Seed = paper `Ren et al. 2019` (HD 191089).** Same loop, entered at the paper: read off HD 191089 +
HST/STIS + Gemini/GPI, output its arXiv link, then crawl outward through its targets, instruments, and
citation graph.

## Bundled script: batch citation harvesting (session-added)

`scripts/find_papers.py --repo <diskatlas-root>` implements the *citation axis* at
atlas scale when SciX pages render as JS shells: it collects every arXiv id cited in
`data/systems/*.json` as seeds, pulls their forward citations from the Semantic
Scholar graph (cached in `data/paper_finder/cache/`, resumable, 429-safe), and ranks
candidates by how many distinct atlas seeds they cite. Use it to bulk-populate the
frontier; triage, target/instrument expansion, link resolution, and the final plain
URL list still follow the rules above. Dispositions go in
`data/paper_finder_state.json` via `--mark <arxiv> ingested|excluded "<reason>"`.

**Triage order (lesson from 2026-07-08):** raw hub-score ordering buries
target-specific observation papers (hub ~5-10) behind reviews and theory (hub 15-40) —
two MWC 758 imaging papers sat at rank ~650 for a day. ALWAYS run
`scripts/find_papers.py --repo <root> --rank` after harvesting (and after every batch
of `--mark`s): it re-sorts candidates.json so that undispositioned papers whose TITLE
names an atlas system and reads like an observation paper come first, and it hides
already-dispositioned entries at the bottom. Work the queue in that order.

## Depth axes — the forward-citation queue is NOT enough (lesson 2026-07-08)

Two whole classes of missing imagery never show up in the forward-citation queue, and
skipping them makes the atlas look "explored" when it isn't. Always work these too:

1. **Backward reference axis (non-arXiv classics).** Foundational coronagraphy papers
   (Grady 2005 STIS Herbig Ae; Schneider/Weinberger/Augereau/Krist NICMOS; the Perrin
   2009 GO-11155 poster) predate astro-ph, so they have no arXiv id — the forward S2
   graph never reaches them and the old `--min-year 2010` filter hid them. `find_papers.py`
   now also harvests **references** (`--direction both`, cached in `cache_refs/`) and keeps
   any paper ≥3 atlas papers cite; run with `--min-year 1995`. When a classic has no arXiv,
   cite it by **ADS bibcode** (or a stable poster/preprint URL in `hires_url`); never invent a
   bibcode — a validate WARN for "neither arxiv nor bibcode" is acceptable for a genuine poster.

2. **Per-paper / per-survey completeness (finish the figure).** A multi-panel or multi-target
   paper is only half-ingested if you crop one panel. When ingesting a survey, enumerate its
   FULL figure gallery / sample table and capture *every* imaged target you lack — resolved or
   unresolved, detection or imaged non-detection (2026-07-16 criterion). Audit the
   surveys already in the atlas the same way: list which of the paper's targets you hold vs. what
   its galleries actually show. Caveats that make a naive "atlas-count < sample-size" gap a false
   alarm — verify before crediting a gap: (a) surveys **split across papers** (Long 2018's 12
   substructured disks + Long 2019's 20 compact ones = the full 32-disk program, both already in);
   (b) sample **tables list comparison objects** never imaged in that paper (ODISEA III's DSHARP
   rows); (c) papers **publish image panels only for a subset** (Wallack NIRC2 shows detection
   galleries only; DESTINYS-Orion non-detections appear only as sky-map markers) — a target with
   NO published panel has nothing to crop and is correctly absent. Use the paper's own
   visibility/size fits (AGE-PRO X) to ANNOTATE each record's resolved-vs-unresolved disposition
   in its note/label — the fits set the annotation, not inclusion.

Agent-fleet note: give each completeness agent the paper id + the *exact* atlas target list it
already holds, so it hunts true gaps instead of re-deriving coverage. And set the agent's cwd to
the repo (or have it write crops to absolute `images/<slug>/` paths) — a relative `images/` path
lands crops in the agent's scratchpad cwd, not the repo, and merge_staging then finds nothing.
