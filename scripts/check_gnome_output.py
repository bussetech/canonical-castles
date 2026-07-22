#!/usr/bin/env python3
"""Refuse gnome output that damages a record, however valid it looks.

WHY THIS EXISTS. A metered assessment run produced three faults that every
existing check passed: a record returned with its verdicts intact but its
`name`, `location`, `built` and `sources` silently gone; three records echoed
back from context with no verdict changed but `last_updated` bumped; and a
`basis` whose prose contained `: ` unquoted, which is a YAML mapping.

The first two are the dangerous ones. They produce well-formed YAML that
validates against the schema, so schema validation cannot see them — the damage
is in what is MISSING or in what did not change, and neither is a thing a
schema can express. This compares each record against the version it replaces.

Three refusals:

  * STUB      — a field present before is now absent. A records gnome assesses
                bands; it is not licensed to delete a structure's name.
  * ECHO      — no verdict changed, but the record was rewritten anyway. An echo
                must never read as an assessment, and a bumped `last_updated`
                on an untouched verdict is exactly how it comes to.
  * UNASSESSED— the record was rewritten and still carries no assessed verdict.

Usage:
    scripts/check_gnome_output.py --against main
"""

from __future__ import annotations

import argparse
import subprocess
import sys

import yaml

# Descriptive fields a verdict never justifies removing.
PROTECTED = ("id", "name", "location", "register_entries", "sources")


def at_ref(ref: str, path: str) -> dict | None:
    out = subprocess.run(["git", "show", f"{ref}:{path}"],
                         capture_output=True, text=True)
    return yaml.safe_load(out.stdout) if out.returncode == 0 else None


def verdicts(rec: dict) -> dict:
    """The judgement content only — what a real assessment must change."""
    return {b: (v.get("verdict"), v.get("assessment"), v.get("basis"))
            for b, v in (rec.get("definitions_met") or {}).items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--against", default="main", help="ref the run started from")
    args = ap.parse_args()

    changed = subprocess.run(
        ["git", "diff", "--name-only", args.against, "--", "data/sites"],
        capture_output=True, text=True, check=True).stdout.split()

    faults: list[str] = []
    ok = 0
    for path in changed:
        before = at_ref(args.against, path)
        after = at_ref("HEAD", path) or yaml.safe_load(open(path).read())
        if before is None or after is None:
            continue

        gone = [f for f in PROTECTED if f in before and f not in after]
        if gone:
            faults.append(f"STUB       {path}: lost {', '.join(gone)} — a verdict "
                          f"does not license deleting a structure's identity")
            continue
        if verdicts(before) == verdicts(after):
            faults.append(f"ECHO       {path}: rewritten, but no verdict changed. "
                          f"Echoing a record from context is not assessing it")
            continue
        if not any(v.get("assessment") == "assessed"
                   for v in (after.get("definitions_met") or {}).values()):
            faults.append(f"UNASSESSED {path}: rewritten with no assessed verdict")
            continue
        ok += 1

    for f in faults:
        print(f"  {f}", file=sys.stderr)
    if faults:
        print(f"gnome-output: REFUSED — {len(faults)} damaged, {ok} sound. "
              f"These validate against the schema; the damage is in what is "
              f"missing or in what did not change.", file=sys.stderr)
        return 1
    print(f"gnome-output: OK — {ok} record(s) assessed, none stubbed or echoed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
