#!/usr/bin/env bash
# Regenerate committed page stubs + derived counts. Run after editing records.
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
"$PY" scripts/gen_pages.py
"$PY" scripts/counts.py
