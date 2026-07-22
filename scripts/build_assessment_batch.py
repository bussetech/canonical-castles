#!/usr/bin/env python3
"""Assemble one assessment batch: records that need verdicts, plus their evidence.

DETERMINISTIC. Selects which structures to assess and pairs each with its
designation report. Makes no model call and no judgement — it decides only what
is ELIGIBLE, and the eligibility rules are the interesting part:

  * Already assessed?  Skip. Setting `assessment: assessed` transfers ownership
    of a record to a human (ADR 0001); this must never hand it back.
  * Report too thin?   Skip, and say which. A designation reading "This
    description is in the process of being updated" cannot support a verdict
    however famous the castle is.
  * No report at all?  Skip. Assessment without evidence is invention.

Selection is deterministic and stable: eligible records sorted by id, then
sliced by --offset/--limit. The same flags always produce the same batch, so a
re-run reproduces a batch exactly and a failed batch can be retried without
guessing what was in it.

Usage:
    scripts/build_assessment_batch.py --register gb-wls-cadw --limit 5
    scripts/build_assessment_batch.py --register gb-wls-cadw --limit 5 --offset 5
    scripts/build_assessment_batch.py --register gb-wls-cadw --limit 5 --out batch.yml
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import re

import yaml

TODAY = "2026-07-22"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-") or "x"


ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = ROOT / "data" / "sites"
SNAPSHOTS = ROOT / "data" / "snapshots"

REPORTS = {"gb-wls-cadw": "gb-wls-cadw-reports.json"}

# Below this, a designation report is boilerplate rather than description.
# Measured: 3 of 104 Welsh reports fall under it, including Denbigh — one of the
# greatest castles in Wales, whose entire text is a placeholder.
MIN_REPORT_CHARS = 400

# A batch this size is a deliberate ceiling, not a technical limit. Cost scales
# with batch count, but so does the blast radius of a bad profile: 5 records is
# small enough to read every verdict before funding the next batch.
MAX_BATCH = 25

# Evidence budget per batch. Report length is wildly uneven — the Welsh median
# is 2,609 characters and the longest is 21,464, so a naive "5 records per call"
# can cost 2-3x what the median implies purely by which reports land in it.
# Capping characters rather than record count makes batch cost predictable,
# which is the whole point of batching. A single report over the cap still gets
# its own batch — it is never dropped for being long.
MAX_BATCH_CHARS = 24_000


def eligible(register: str) -> tuple[list[dict], dict[str, list[str]]]:
    """Records that can be assessed, and why the rest cannot."""
    reports = json.loads((SNAPSHOTS / REPORTS[register]).read_text())
    by_ref = {r: v for r, v in reports.items()}

    out: list[dict] = []
    skipped: dict[str, list[str]] = {"already-assessed": [], "report-too-thin": [],
                                     "no-report": []}

    for path in sorted(SITES.glob("*.yml")):
        rec = yaml.safe_load(path.read_text())
        entry = next((e for e in rec.get("register_entries") or []
                      if e.get("register") == register), None)
        if not entry:
            continue

        bands = rec.get("definitions_met") or {}
        if any(v.get("assessment", "assessed") == "assessed" for v in bands.values()):
            skipped["already-assessed"].append(rec["id"])
            continue

        report = by_ref.get(entry["ref"])
        if not report:
            skipped["no-report"].append(rec["id"])
            continue
        if report["chars"] < MIN_REPORT_CHARS:
            skipped["report-too-thin"].append(f"{rec['id']} ({report['chars']}c)")
            continue

        out.append({
            "site_id": rec["id"],
            "name": rec["name"],
            "register": register,
            "ref": entry["ref"],
            "current_designation": entry.get("designation"),
            "current_verdict": {
                b: {"verdict": v["verdict"], "assessment": v.get("assessment", "assessed")}
                for b, v in bands.items()
            },
            "report_url": report["url"],
            "report": "\n".join(report["text"]),
        })
    return out, skipped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", required=True, choices=sorted(REPORTS))
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--out-dir", help="write the gnome's three input files here")
    ap.add_argument("--materialise", action="store_true",
                    help="ALSO write each signal into data/signals/ as a committed file")
    ap.add_argument("--out", help="write a single combined batch here (inspection)")
    args = ap.parse_args()

    if args.limit < 1 or args.limit > MAX_BATCH:
        print(f"--limit must be 1..{MAX_BATCH} (got {args.limit}). The ceiling is "
              f"deliberate: every verdict in a batch should be read before the next "
              f"one is funded.", file=sys.stderr)
        return 2

    pool, skipped = eligible(args.register)

    # Fill by character budget as well as count, so cost per batch is bounded.
    batch: list[dict] = []
    used = 0
    for item in pool[args.offset:]:
        if len(batch) >= args.limit:
            break
        size = len(item["report"])
        if batch and used + size > MAX_BATCH_CHARS:
            print(f"  batch closed early at {len(batch)} structures: adding "
                  f"{item['site_id']} ({size}c) would exceed the {MAX_BATCH_CHARS}c "
                  f"evidence budget", file=sys.stderr)
            break
        batch.append(item)
        used += size

    for reason, ids in skipped.items():
        if ids:
            print(f"  skipped ({reason}): {len(ids)}"
                  + (f" — {', '.join(ids[:3])}" if reason != "already-assessed" else ""),
                  file=sys.stderr)
    print(f"  eligible: {len(pool)}  ·  this batch: {len(batch)} "
          f"(offset {args.offset})", file=sys.stderr)

    if not batch:
        print("  nothing to assess at this offset — honest no-op", file=sys.stderr)
        return 0

    doc = {"register": args.register, "offset": args.offset, "structures": batch}
    text = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)

    if args.out_dir:
        # The gnome's input contract is fixed (signals / existing_sites /
        # entities). A designation report fits `signals` honestly: it is one
        # claim, from one source, about one structure — the archetype's own
        # definition. These are assembled at RUN TIME from the committed
        # snapshot, never committed as duplicate signal files.
        out = pathlib.Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)

        signals = [{
            "id": f"sig-{TODAY.replace('-', '')}-report-{slug(s['ref'])}",
            "site_id": s["site_id"],
            "attribute": "designation_report",
            "value": s["report"],
            "source_url": s["report_url"],
            "source_title": f"Scheduled Monument Full Report — {s['name']}",
            "publisher": "Cadw",
            "observed_date": TODAY,
            "collected_by": "scripts/build_assessment_batch.py",
            "confidence": "high",
            "notes": ("The designation text. Assess the six bands against THIS evidence "
                      "only; omit any band it does not speak to."),
        } for s in batch]
        (out / "signals.yml").write_text(
            yaml.safe_dump(signals, sort_keys=False, allow_unicode=True, width=100))

        existing = []
        for s in batch:
            rec = yaml.safe_load((SITES / f"{s['site_id']}.yml").read_text())
            existing.append(rec)
        (out / "existing_sites.yml").write_text(
            yaml.safe_dump(existing, sort_keys=False, allow_unicode=True, width=100))

        # `entities` carries the canonical vocabulary the gnome resolves into.
        # For this project that is the definition bands, not an operator registry.
        (out / "entities.yml").write_text(
            (ROOT / "data" / "definitions.yml").read_text())

        print(f"  wrote {out}/: signals.yml ({len(signals)}), existing_sites.yml, "
              f"entities.yml", file=sys.stderr)

        # MATERIALISE. Assembling signals only at run time was a design error:
        # the gnome correctly records which signals a verdict came from, so the
        # resulting records cite ids that exist nowhere on disk and integrity
        # rightly fails. Evidence a record cites has to be evidence a reader can
        # open — that is the dataset's whole claim — so the signal becomes a
        # committed file. The snapshot stays the raw provenance; the signal is
        # the citable claim.
        if args.materialise:
            sigdir = ROOT / "data" / "signals"
            sigdir.mkdir(parents=True, exist_ok=True)
            for s in signals:
                (sigdir / f"{s['id']}.yml").write_text(
                    yaml.safe_dump(s, sort_keys=False, allow_unicode=True, width=88))
            print(f"  materialised {len(signals)} signal file(s) into data/signals/",
                  file=sys.stderr)

    if args.out:
        pathlib.Path(args.out).write_text(text)
    if not args.out and not args.out_dir:
        print(text)
    print(f"  batch: {len(batch)} structures, {used} chars of evidence "
          f"({100 * used // MAX_BATCH_CHARS}% of budget)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
