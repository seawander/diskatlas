#!/usr/bin/env bash
# One-shot local runner for every CI guard (mirrors .github/workflows/ci.yml).
# Wired into .git/hooks/pre-push on the shared checkout so neither track can
# push a commit that CI would reject (stale data.js, schema errors, broken
# image paths). Safe to run by hand at any time; read-only apart from
# check_data_sync.py's rebuild-and-restore of frontend/data.js.
#
# Node checks are skipped with a warning when node isn't installed locally —
# CI still runs them on every push.
set -u
cd "$(dirname "$0")/.."

fail=0
run() { echo "── $*"; "$@" || fail=1; }

run python3 backend-data/validate.py
run python3 backend-infra/check_data_sync.py
run python3 backend-infra/check_images.py

if command -v node >/dev/null 2>&1; then
  run node backend-data/test_frontend_logic.js
  run node backend-infra/check_i18n.js
else
  echo "!! node not found — skipped frontend-logic + i18n checks (CI runs them)"
fi

if [ "$fail" -ne 0 ]; then
  echo ""
  echo "✗ checks FAILED — fix before pushing (CI would reject this)."
  echo "  stale data.js?  run:  python3 backend-data/build.py"
fi
exit $fail
