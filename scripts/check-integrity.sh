#!/usr/bin/env bash
# Integrity hook for shared data CI (bussetech/ci reusable-data-ci).
# Schema validation happens upstream; this proves the files agree with each
# other and that every published number is re-derivable from the records.
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
"$PY" scripts/check_integrity.py
"$PY" scripts/gen_pages.py --check
"$PY" scripts/counts.py --check
