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
# Imports are reproducible from their committed snapshot, or they are not imports.
"$PY" scripts/import_register.py --register gb-wls-cadw --transform --check
# The disagreement ledger is derived, so it is drift-checked like every other
# published number.
"$PY" scripts/analyse_disagreements.py --check
