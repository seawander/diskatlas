# Continuation prompt (copy-paste into a new session)

Keep it short — `CLAUDE.md` auto-loads in Claude Code and carries the rules +
the task→doc routing table, so the prompt itself only needs your task:

```
Open <path-to-your-clone>/diskatlas (offline all-sky atlas of
resolved disks / imaged companions / quasar hosts; CLAUDE.md has the rules and
tells you which single doc to read for your task — do NOT read everything).
Start with: python3 backend-data/validate.py && python3 backend-data/build.py

MY TASK: <arXiv links to ingest · "run the weekly maintenance"
(fresh_papers.py digest → VIEW figures → ingest or exclude) · "audit system X"
(system_audit.py) · a frontend request · or blank for a status report>
```

For an agent that does NOT auto-load CLAUDE.md, prepend one line:
"First read CLAUDE.md and obey its token-discipline table."

Per-task playbooks live in `HANDOFF.md` (§maintenance rhythm, §parallel agents,
§crop discipline) — the agent reads them on demand; don't paste them here.
