#!/usr/bin/env python3
"""Generate one page stub per record.

Jekyll renders each structure's page from `site.data.sites[page.site_id]` via
the `castle-record` layout, so the stub carries no content — only the front
matter that points the layout at the right record. Keeping the stubs committed
(rather than generating at build time) means the site's URL surface is
reviewable in the diff: adding a record visibly adds a page.

Usage:  scripts/gen_pages.py [--check]
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = ROOT / "data" / "sites"
PAGES = ROOT / "castles"
DEFINITIONS = ROOT / "data" / "definitions.yml"
BAND_PAGES = ROOT / "definitions"

BAND_TEMPLATE = """---
layout: definition
band: {bid}
title: "{title}"
permalink: /definitions/{bid}/
---
"""

TEMPLATE = """---
layout: castle-record
site_id: {rid}
title: "{title}"
permalink: /castles/{rid}/
---
"""


def render(path: pathlib.Path) -> tuple[str, str]:
    with path.open() as fh:
        rec = yaml.safe_load(fh)
    rid = rec["id"]
    title = rec["name"].replace('"', "'")
    return rid, TEMPLATE.format(rid=rid, title=title)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    PAGES.mkdir(exist_ok=True)
    wanted: dict[str, str] = {}
    for path in sorted(SITES.glob("*.yml")):
        rid, text = render(path)
        wanted[rid] = text

    stale = []
    for rid, text in wanted.items():
        target = PAGES / f"{rid}.md"
        if not target.exists() or target.read_text() != text:
            stale.append(rid)
            if not args.check:
                target.write_text(text)

    # Each band gets its own page: a definition is the unit this project
    # reasons in, so it earns a citable URL rather than a fragment.
    bands = yaml.safe_load(DEFINITIONS.read_text())["definitions"]
    BAND_PAGES.mkdir(exist_ok=True)
    for b in bands:
        text = BAND_TEMPLATE.format(bid=b["id"], title=b["label"].replace('"', "'"))
        target = BAND_PAGES / f"{b['id']}.md"
        if not target.exists() or target.read_text() != text:
            stale.append(f"definitions/{b['id']}")
            if not args.check:
                target.write_text(text)
    band_ids = {b["id"] for b in bands}
    for path in BAND_PAGES.glob("*.md"):
        if path.stem != "index" and path.stem not in band_ids:
            stale.append(f"definitions/{path.stem} (orphan)")
            if not args.check:
                path.unlink()

    orphans = [
        p for p in PAGES.glob("*.md") if p.stem != "index" and p.stem not in wanted
    ]
    for path in orphans:
        stale.append(f"{path.stem} (orphan)")
        if not args.check:
            path.unlink()

    if args.check:
        if stale:
            print("pages: STALE -> " + ", ".join(stale), file=sys.stderr)
            print("  Run scripts/gen-pages.sh and commit the result.", file=sys.stderr)
            return 1
        print(f"pages: fresh ({len(wanted)} stubs)")
        return 0

    print(f"pages: wrote {len(wanted)} stubs ({len(stale)} changed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
