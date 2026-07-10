# Continuation prompt (copy-paste into a new session)

One self-contained prompt: it orients the model, then takes whatever task you put in the
`MY TASK` line at the bottom (ingest papers, run the paper-finder, a sweep, a frontend
tweak — or leave it blank to just get a status report).

---

```
Open /home/brinen2spark/Developments/diskatlas. This is a mature, working offline
double-click-index.html all-sky atlas of resolved circumstellar disks (protoplanetary,
debris, edge-on, embedded Class 0/I, eruptive, Orion proplyds, far-IR-resolved,
evolved-star envelopes), directly imaged planets/BD companions, and coronagraphic
quasar hosts (460+ systems, 1480+ image records, 0 validation errors/warnings —
`python3 backend/build.py` prints the live numbers), built over several prior
sessions. The project is in MAINTENANCE MODE (see HANDOFF.md): retrospective
discovery is saturated; the ongoing rhythm is the weekly fresh_papers digest +
user-directed adds.

FIRST, orient yourself:
1. Read HANDOFF.md completely (architecture, the live-network environment, the
   parallel-agent ingestion method + its gotchas, crop discipline, the THREE bookkeeping
   ledgers, data conventions, my preferences), then skim README.md, data/README.md,
   and data/ingestion_status.json.
2. Run `python3 backend/validate.py && python3 backend/build.py`; confirm 0 errors.

Standing rules (per HANDOFF.md): reply in English; this machine has live internet, so run
`cd backend && bash fetch_sources.sh` yourself (no host hand-off); verify every paper's
arXiv id + figure FROM THE SOURCE, never from memory; never use press-release images;
VIEW every crop before AND after saving it; crops are PANEL-ONLY (trim axes/margins);
keep validate.py at 0 errors; update data/ingestion_status.json (batch ledger) and
data/paper_finder_state.json (per-paper dispositions) after any change. For any batch
bigger than ~5 crops, or any sweep, fan out background agents (shared brief file +
hardcoded in/out paths per agent; re-verify agent-reported arXiv ids centrally;
reconcile crops against the PNGs on disk; resume agents that stop after delegating).

THEN handle MY TASK below:
- arXiv links / bibcodes -> ingest each: record + full citation -> fetch -> crop the
  figure I name -> VIEW to confirm the panel -> merge -> build. New systems: follow
  data/README.md schema, coords via SIMBAD (parse RA/Dec from coordinate-encoding
  designations when SIMBAD misses), redshift (not distance) for quasars,
  planets[].method = imaging|transit|interferometry, extra_papers for independent
  discoveries.
- "weekly maintenance" / "find new papers" -> run `python3 backend/fresh_papers.py`
  (last-14-days astro-ph.EP/SR digest via anonymous ADS). For each hit: download the
  PDF, VIEW the figure (metadata lies — most hits dissolve on inspection), then either
  ingest it or add an arXiv-id-keyed `excluded` entry (with reason) to
  data/paper_finder_state.json. Afterwards `audit_bibcodes.py --fix --fill` and keep
  validate at 0 errors / 0 warnings. The retrospective snowball Skill
  (.claude/skills/diskatlas-paper-finder/) is SATURATED — use only for targeted
  questions; `backend/system_audit.py --systems <ids>` for per-target completeness
  (VIEW-verify every flag; short names like "T Tau" collide via ADS stemming).
- "comprehensiveness sweep" -> instrument-level sweep (inventory each system's
  facility/instrument set, fan out agents for instruments not yet represented, verify,
  ingest) + coverage_audit.py gaps + a recent astro-ph.EP/SR scan + external-catalog
  cross-checks (Wikipedia resolved-disk list, circumstellardisks.org).
- a frontend change -> pure vanilla JS in frontend/ (app.js, i18n.js, style.css; data.js
  is generated; facet keys come from backend/facility_map.py at build time). Verify with
  a preview server (Node isn't installed).
- nothing yet -> summarize the current state + what's open in ingestion_status.json and
  data/paper_finder/triage-queue.json, and wait.

MY TASK: <paste arXiv links, or "run the paper finder", or "run the comprehensiveness sweep", or a frontend request — or leave blank>
```

---

### Notes
- Start the message with **`ultracode`** to force maximal agent parallelism from the
  first step, otherwise the model may work single-threaded until told.
- The `/home/...diskatlas` path and "live internet from bash" hold for THIS machine. In a
  different/isolated environment the model should fall back to the host-fetch loop that
  HANDOFF.md still documents (run `fetch_sources.sh` on a networked host; drop
  captcha-locked PDFs into `images/_sources/extra/<name>.pdf`).
- After any data change: `python3 backend/validate.py && python3 backend/build.py`, then
  open `index.html` (double-click, or `python3 -m http.server` for the preview tools).
- Bookkeeping: data/systems/*.json = ground truth; data/paper_finder_state.json =
  per-paper dispositions (the Skill's dedupe ledger); data/ingestion_status.json =
  batch/session log. Don't invent a fourth ledger.
