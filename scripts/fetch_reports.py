#!/usr/bin/env python3
"""Fetch the designation report behind each register entry, and extract its text.

THE EVIDENCE LAYER. A register row says a body called something a castle; it
does not say why, and it cannot support a verdict against this project's band
criteria. The report behind it can: it carries fabric, defensive features,
period and often documentary history, plus the register's own inline definition
of the monument class.

This script is DETERMINISTIC and does no judging. It fetches, extracts text, and
writes a snapshot. What the text means is a separate act — by a person or by the
archetype's research gnome — and that act is what turns a `register-derived`
verdict into an `assessed` one.

The split is the studio's standing rule that research agents never fetch
(ADR-0025): a deterministic layer feeds them, and the source must already be on
this project's allowlist in data/sources.yml before a byte is requested.

Politeness: one request per second, only for monuments already held, never
crawled. No robots.txt is published by the host, and absence of a prohibition
is not an invitation.

Usage:
    scripts/fetch_reports.py --register gb-wls-cadw [--limit N]
    scripts/fetch_reports.py --register gb-wls-cadw --check
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys
import time
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = ROOT / "data" / "sites"
SNAPSHOTS = ROOT / "data" / "snapshots"

SNAPSHOT = {"gb-wls-cadw": "gb-wls-cadw-reports.json"}
UA = "canonical-castles/1.0 (+https://castles.bussetech.com; one req/sec)"

# Report boilerplate that appears on every page and carries no information about
# the monument. Stripped so the digest is signal, not furniture.
BOILERPLATE = {
    "Scheduled Monument - Full Report - HeritageBill Cadw Assets - Reports",
    "Scheduled Monuments- Full Report",
    "Summary Description of a Scheduled Monument",
    "The following provides a general description of the Scheduled Ancient Monument.",
    "Cadw : Scheduled Monuments- Full Report",
    "Export",
    "Description",
    "Location",
    "Summary Description and Reason for Designation",
}


def extract_text(raw: str) -> list[str]:
    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", raw)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t)
    out = []
    for line in (l.strip() for l in t.split("\n")):
        if not line or line in BOILERPLATE:
            continue
        if re.fullmatch(r"\[ Records \d+ of \d+ \]", line):
            continue
        out.append(line)
    return out


def targets(register: str) -> list[dict]:
    """Monuments this dataset holds for `register`, with a report URL."""
    out = []
    for path in sorted(SITES.glob("*.yml")):
        rec = yaml.safe_load(path.read_text())
        for e in rec.get("register_entries") or []:
            if e.get("register") == register and e.get("url"):
                out.append({"id": rec["id"], "ref": e["ref"], "url": e["url"],
                            "name": rec["name"]})
                break
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", required=True, choices=sorted(SNAPSHOT))
    ap.add_argument("--limit", type=int, default=0, help="fetch at most N (for a trial run)")
    ap.add_argument("--check", action="store_true", help="report coverage without fetching")
    args = ap.parse_args()

    snap = SNAPSHOTS / SNAPSHOT[args.register]
    have = json.loads(snap.read_text()) if snap.is_file() else {}
    want = targets(args.register)

    if args.check:
        missing = [t for t in want if t["ref"] not in have]
        print(f"reports[{args.register}]: {len(have)} held, {len(want)} monuments, "
              f"{len(missing)} missing")
        return 1 if missing else 0

    todo = [t for t in want if t["ref"] not in have]
    if args.limit:
        todo = todo[: args.limit]
    print(f"reports[{args.register}]: {len(have)} already held, fetching {len(todo)}")

    for i, t in enumerate(todo, 1):
        req = urllib.request.Request(t["url"], headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as fh:  # noqa: S310
                body = fh.read().decode("utf-8", "replace")
        except Exception as exc:                                  # noqa: BLE001
            print(f"  [{i}/{len(todo)}] {t['ref']}: FAILED {exc}", file=sys.stderr)
            continue
        lines = extract_text(body)
        have[t["ref"]] = {"site_id": t["id"], "name": t["name"], "url": t["url"],
                          "text": lines, "chars": sum(len(l) for l in lines)}
        if i % 10 == 0 or i == len(todo):
            print(f"  [{i}/{len(todo)}] {t['ref']} ({have[t['ref']]['chars']} chars)")
        time.sleep(1.0)          # one request per second, deliberately

    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    snap.write_text(json.dumps(have, separators=(",", ":"), ensure_ascii=False,
                               sort_keys=True))
    thin = [r for r, v in have.items() if v["chars"] < 400]
    print(f"reports[{args.register}]: {len(have)} reports held, "
          f"{len(thin)} under 400 chars (too thin to assess from)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
