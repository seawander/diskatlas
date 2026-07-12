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

# Release-pin sanity: if the pages.yml being pushed pins RELEASE_REF to a tag,
# that tag must already exist on origin or be part of THIS push — otherwise
# every Pages deploy fails at checkout until someone pushes the tag.
# (Bitten twice on 2026-07-11: release-2026-07-11 and release-2026-07-11.1
# were both pinned and pushed as commits before their tags reached origin.)
# Under the pre-push hook, stdin lists the refs being pushed; on a manual run
# stdin is a tty and we check HEAD against origin.
pin_sha="HEAD"; push_refs=""
if [ ! -t 0 ]; then
  while read -r _lref lsha rref _rsha; do
    push_refs="$push_refs $rref"
    [ "$rref" = "refs/heads/master" ] && pin_sha="$lsha"
  done
fi
pin_ref=$(git show "$pin_sha:.github/workflows/pages.yml" 2>/dev/null \
          | sed -n 's/^  RELEASE_REF: *//p' | head -1)
if [ -n "$pin_ref" ]; then
  case " $push_refs " in
    *" refs/tags/$pin_ref "*) : ;;   # the tag rides along in this push — fine
    *)
      if git ls-remote --exit-code origin "refs/tags/$pin_ref" >/dev/null 2>&1; then
        echo "── release pin: tag '$pin_ref' present on origin"
      else
        echo "✗ pages.yml pins RELEASE_REF=$pin_ref but that tag is NOT on origin"
        echo "  and not part of this push — the Pages deploy will fail at checkout."
        echo "  Fix: git push origin $pin_ref   (or push tag + branch together)"
        fail=1
      fi
      ;;
  esac
fi

if [ "$fail" -ne 0 ]; then
  echo ""
  echo "✗ checks FAILED — fix before pushing (CI would reject this)."
  echo "  stale data.js?  run:  python3 backend-data/build.py"
fi
exit $fail
