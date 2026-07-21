#!/usr/bin/env python3
"""Referential integrity for the castles dataset.

JSON Schema proves each file is well-shaped. This proves the files agree with
each other — which is where an agent-written dataset actually goes wrong. The
checks below are ordered from structural to editorial; the last few exist
because this project makes claims about completeness and counting, and a claim
is only as good as the machinery that can falsify it.

Usage:  scripts/check_integrity.py
Exit:   0 clean, 1 on any violation (every violation printed, not just the first)
"""

from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PAGES = ROOT / "castles"

problems: list[str] = []


def fail(msg: str) -> None:
    problems.append(msg)


def load(path: pathlib.Path):
    with path.open() as fh:
        return yaml.safe_load(fh)


def main() -> int:
    definitions = load(DATA / "definitions.yml")["definitions"]
    registers = load(DATA / "registers.yml")["registers"]
    coverage = load(DATA / "coverage.yml")["cells"]

    band_ids = {d["id"] for d in definitions}
    register_ids = {r["id"] for r in registers}
    closure = {d["id"]: d["closure"] for d in definitions}

    records = {}
    for path in sorted((DATA / "sites").glob("*.yml")):
        rec = load(path)
        stem = path.stem
        if rec.get("id") != stem:
            fail(f"sites/{path.name}: id {rec.get('id')!r} != filename stem {stem!r}")
        if stem in records:
            fail(f"sites/{path.name}: duplicate id {stem!r}")
        records[stem] = rec

    signals = {}
    for path in sorted((DATA / "signals").glob("*.yml")):
        sig = load(path)
        stem = path.stem
        if sig.get("id") != stem:
            fail(f"signals/{path.name}: id {sig.get('id')!r} != filename stem {stem!r}")
        signals[stem] = sig

    # --- cross-references -------------------------------------------------
    for sid, sig in signals.items():
        target = sig.get("site_id")
        if target is not None and target not in records:
            fail(f"signals/{sid}: site_id {target!r} has no record in data/sites/")
        if target is None and not sig.get("site_hint"):
            fail(f"signals/{sid}: site_id is null but site_hint is missing — the "
                 f"structure would be unidentifiable")
        if target is not None and sig.get("site_hint"):
            fail(f"signals/{sid}: site_hint present alongside a resolved site_id — "
                 f"the archetype contract says omit it once resolved")

    for rid, rec in records.items():
        for ref in rec.get("signals") or []:
            if ref not in signals:
                fail(f"sites/{rid}: signals[] references {ref!r}, which does not exist")

        # --- the spine: every verdict names a real band -------------------
        met = rec.get("definitions_met") or {}
        for band in met:
            if band not in band_ids:
                fail(f"sites/{rid}: definitions_met has unknown band {band!r} "
                     f"(not in data/definitions.yml)")

        for entry in rec.get("register_entries") or []:
            if entry["register"] not in register_ids:
                fail(f"sites/{rid}: register_entry names unknown register "
                     f"{entry['register']!r}")

        if rec.get("disputed") and not rec.get("dispute_note"):
            fail(f"sites/{rid}: disputed is true but dispute_note is empty — a "
                 f"flagged dispute the reader cannot see is worse than none")

        # A verdict must engage the criterion, not merely assert a conclusion.
        for band, entry in met.items():
            basis = (entry.get("basis") or "").strip()
            if len(basis) < 20:
                fail(f"sites/{rid}: definitions_met.{band}.basis is too thin "
                     f"({basis!r}) — state why against the band's criterion")

        # --- page stub ----------------------------------------------------
        if not (PAGES / f"{rid}.md").exists():
            fail(f"sites/{rid}: no page stub at castles/{rid}.md "
                 f"(run scripts/gen-pages.sh)")

    for stub in sorted(PAGES.glob("*.md")):
        if stub.stem == "index":
            continue
        if stub.stem not in records:
            fail(f"castles/{stub.name}: orphan page stub — no matching record")

    # --- definitions and their registers ----------------------------------
    for d in definitions:
        if d["closure"] == "enumerable" and not d.get("registers"):
            fail(f"definitions/{d['id']}: closure is 'enumerable' but no registers "
                 f"are named — a band cannot be closable against nothing")
        for reg in d.get("registers") or []:
            if reg not in register_ids:
                fail(f"definitions/{d['id']}: names unknown register {reg!r}")

    # --- coverage grid ----------------------------------------------------
    seen_cells = set()
    for cell in coverage:
        key = (cell["definition"], cell["jurisdiction"])
        if key in seen_cells:
            fail(f"coverage: duplicate cell {key}")
        seen_cells.add(key)

        if cell["definition"] not in band_ids:
            fail(f"coverage {key}: unknown definition {cell['definition']!r}")
        for reg in cell.get("settled_by") or []:
            if reg not in register_ids:
                fail(f"coverage {key}: settled_by names unknown register {reg!r}")

        if cell["state"] == "complete" and not cell.get("settled_by"):
            fail(f"coverage {key}: claims 'complete' without naming the register "
                 f"that bounds it — completeness against nothing is not a claim")

        # The load-bearing rule: an open band has no world-population figure.
        if cell.get("register_count") is not None and closure.get(cell["definition"]) == "open":
            fail(f"coverage {key}: register_count is set on an OPEN band. No "
                 f"register bounds this band, so any population figure here "
                 f"would be invented — put a sourced range on the band instead")

        if cell["state"] == "complete":
            held, total = cell.get("records_held"), cell.get("register_count")
            if total is not None and held != total:
                fail(f"coverage {key}: 'complete' but holds {held} of {total} "
                     f"register entries")

        # A register-derived verdict must name the register it came from,
        # otherwise "the register said so" is unfalsifiable.
        for band, entry in met.items():
            if entry.get("assessment") == "register-derived" and not rec.get("register_entries"):
                fail(f"sites/{rid}: definitions_met.{band} is register-derived but the "
                     f"record names no register_entries — the claim cannot be checked")

    # --- production ledger ------------------------------------------------
    production = load(DATA / "production.yml")["batches"]
    complete_cells = {f"{c['definition']}/{c['jurisdiction']}"
                      for c in coverage if c["state"] == "complete"}
    for batch in production:
        cost = batch["cost"]
        # THE rule: an unmeasured cost is never a number, and least of all 0.
        if not cost["measured"] and cost["model_usd"] is not None:
            fail(f"production/{batch['id']}: measured is false but model_usd is "
                 f"{cost['model_usd']!r} — an unmeasured cost must be null, never a "
                 f"figure and never 0")
        if cost["measured"] and cost["model_usd"] is None:
            fail(f"production/{batch['id']}: measured is true but model_usd is null — "
                 f"say what was measured or set measured: false")
        for cell in batch.get("cells_closed") or []:
            if cell not in complete_cells:
                fail(f"production/{batch['id']}: claims to have closed {cell}, but that "
                     f"cell is not 'complete' in data/coverage.yml")

    # --- count claims -----------------------------------------------------
    claims = load(DATA / "claims.yml")["claims"]
    claim_ids = {c["id"] for c in claims}
    for claim in claims:
        if claim.get("definition") is not None and claim["definition"] not in band_ids:
            fail(f"claims/{claim['id']}: unknown definition {claim['definition']!r}")
        if claim.get("supersedes") and claim["supersedes"] not in claim_ids:
            fail(f"claims/{claim['id']}: supersedes unknown claim {claim['supersedes']!r}")
        # A folklore grade is an accusation; it has to be argued, not asserted.
        if claim["grade"] == "folklore" and len(claim["assessment"]) < 200:
            fail(f"claims/{claim['id']}: graded folklore on a thin assessment — "
                 f"say what was searched and what was not found")
        if claim.get("value") is not None and claim.get("value_range"):
            fail(f"claims/{claim['id']}: has both value and value_range — pick one")

    if problems:
        print(f"integrity: {len(problems)} problem(s)\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print(
        f"integrity: OK — {len(records)} records, {len(signals)} signals, "
        f"{len(band_ids)} bands, {len(register_ids)} registers, {len(coverage)} cells"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
