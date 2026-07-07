# SciX / arXiv query & fetch recipes

Everything here is designed to work with plain web fetching (no personal API token). SciX
(`scixplorer.org`) is the successor to NASA ADS and shares the ADS/Solr backend and bibcode scheme.

## Bibcode anatomy

A bibcode is a 19-character record key: `YYYYJJJJJVVVVMPPPPA`

- `YYYY` — year (e.g. `2020`)
- `JJJJJ` — journal/source abbreviation, dot-padded (`Sci..`, `ApJ..`, `A&A..`, `MNRAS`, `ApJL.`, `arXiv`)
- `VVVV` — volume, right-justified
- `M` — one-letter section/qualifier (`L` for Letters, `.` otherwise)
- `PPPP` — starting page/article id, right-justified
- `A` — first author's last initial

Examples: `2020Sci...369.1233K` (Kraus et al. 2020, *Science*), `2019ApJ...882...64R` (Ren et al. 2019,
*ApJ*). You usually get bibcodes from search results and from citation/reference lists — you rarely need
to construct them by hand, but knowing the shape helps you validate and recognize duplicates.

## SciX URL patterns

- **Search:** `https://scixplorer.org/search?q=<url-encoded-query>&sort=date%20desc&p_=0`
- **Abstract:** `https://scixplorer.org/abs/<bibcode>/abstract`
- **References (what it cites):** `https://scixplorer.org/abs/<bibcode>/references`
- **Citations (what cites it):** `https://scixplorer.org/abs/<bibcode>/citations`
- **Exportable identifiers / e-print:** the abstract record lists alternate identifiers including the
  arXiv e-print ID and DOI.

### Field-scoped query syntax (ADS/SciX Solr)

- `object:"GW Ori"` — resolves against SIMBAD object names; best for target sweeps.
- `instr:"SPHERE"` — instrument metadata (populated inconsistently; combine with a full-text fallback).
- `full:"polarimetric" full:"disk"` — full-text terms.
- `author:"Kraus, S"` , `year:2018-2026` , `bibstem:ApJ` — narrow as needed.
- `citations(bibcode:2020Sci...369.1233K)` — the set citing a paper.
- `references(bibcode:2020Sci...369.1233K)` — the set it cites.
- Sort newest-first with `sort=date desc` to catch the latest observations first.

Compose sweeps like:
`object:"HD 100546" (instr:"SPHERE" OR full:"SPHERE")` ,
`instr:"ALMA" full:"protoplanetary" full:"rings" year:2015-2026`.

## arXiv patterns (fetchable, clean, no token — the reliable content surface)

- **Abstract page:** `https://arxiv.org/abs/<id>` (e.g. `https://arxiv.org/abs/1906.10130`)
- **PDF:** `https://arxiv.org/pdf/<id>`
- **Export API (structured Atom XML):**
  `http://export.arxiv.org/api/query?search_query=all:<terms>&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending`
  — returns titles, authors, abstracts, `<id>` (abs URL), and dates. Good for modern keyword/target/instrument
  sweeps and for confirming an arXiv ID exists.
- arXiv has **no "cited-by"** — use SciX for the citation graph, arXiv for fetchable content and modern
  keyword search.

## Handling the JS-shell problem

SciX is a client-rendered single-page app. A raw fetch of a SciX **abstract/search page can come back as a
near-empty HTML shell** with the data loaded later by JavaScript. Plan for it:

1. **Try the SciX page first.** If the fetch returns the bibliographic content (title, abstract, identifiers,
   the reference/citation list), use it directly — this is the ideal path.
2. **If it's an empty shell,** don't get stuck. Use SciX purely as the *index* (you still learned the
   bibcode / target / instrument from search-result metadata or from the user), and switch to **arXiv** for
   fetchable content: resolve the arXiv ID (from the paper's title via the export API, or from a bibcode's
   known e-print) and fetch `arxiv.org/abs/<id>`.
3. **For the citation graph specifically,** the reference/citation *lists* live in SciX. If those pages
   render for your fetcher, read the bibcodes off them; if they don't, fall back to searching the target +
   nearby years on arXiv to approximate the forward hops (newer observations of the same system), and use
   the seed paper's own reference section (from its arXiv PDF) for the backward hops.
4. **Whatever renders, keep the bibcode as the identity key** so dedup against the atlas inventory and your
   visited set stays consistent across SciX and arXiv representations.

The point of these fallbacks is resilience: the crawl should keep making progress even when one surface is
uncooperative, and the *output link* still follows the resolution rules in SKILL.md (arXiv preferred; SciX
abstract link for pre-~1995 / no-preprint papers; never press releases).

## arXiv coverage by era

astro-ph began in 1992 and coverage of observational imaging papers is spotty before ~1995. So: if a paper
is older than ~1995, or the export API / record shows no e-print, treat it as **no arXiv** and output the
SciX/ADS abstract link — ADS/SciX hosts scanned historical published PDFs the atlas can still read figures
from.
