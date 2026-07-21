#!/usr/bin/env python3
"""Find where two registers classify the same structure differently.

DETERMINISTIC, and the third pillar of the dataset. Records answer "what is
this?"; the claims ledger answers "where did that number come from?"; this
answers "who disagrees, and about what kind of thing?" — which is the part no
other castle dataset has, because everyone else picks one register and inherits
its opinions.

THE JOIN IS ON AN IDENTIFIER, NEVER A NAME. Wikidata property P3007 is the Cadw
Monument ID, so the two registers can be joined on the monument itself rather
than on a string. Name matching would manufacture agreement and disagreement in
roughly equal measure — "Castell Dinas" names several different places, and the
same structure appears as "Aberlleiniog Castle" in one register and "Castell
Aberlleiniog" in the other.

THE KIND MATTERS MORE THAN THE COUNT. A register calling a motte a castle and a
register calling a burial mound a castle are not the same event:

    granularity     both classes map to the SAME band — one register is just
                    more specific. Real, but nobody is wrong.
    band-conflict   they map to DIFFERENT bands. A genuine dispute about what
                    kind of thing this is, and the case that should make a
                    record `contested`.
    category-error  one class maps to NO band. A round barrow is not a
                    fortification under any definition here, so one of the two
                    registers is simply wrong.

Usage:  scripts/analyse_disagreements.py [--check]
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAPSHOTS = ROOT / "data" / "snapshots"
OUT = ROOT / "data" / "disagreements.yml"

CADW_ALL = SNAPSHOTS / "gb-wls-cadw-all-sam.json"
WIKIDATA = SNAPSHOTS / "wikidata-cadw-monuments.json"

# ---------------------------------------------------------------------------
# The band mapping. THIS IS THE REVIEWABLE ARTEFACT — the code around it is
# plumbing. Every classification either maps to a definition band or explicitly
# to None, and None is a claim: "under this project's bands, that is not a
# fortification at all".
#
# Deliberately conservative. Where a class could arguably sit in a band, it is
# mapped; only classes that are plainly something else map to None. Being too
# eager with None would inflate `category-error`, which is the accusatory kind.
# ---------------------------------------------------------------------------

FORTIFIED = "fortified_residence"
ENCLOSURE = "enclosure_fortification"
STATE = "state_fortification"
PALATIAL = "palatial_seat"

CADW_BANDS: dict[str, str | None] = {
    # Lordly fortifications — the strict band. A motte IS a castle earthwork;
    # Cadw is simply more specific than Wikidata about which sort.
    "Castle": FORTIFIED,
    "Motte": FORTIFIED,
    "Motte and Bailey": FORTIFIED,
    "Ringwork": FORTIFIED,
    "Ringwork and bailey": FORTIFIED,
    "Tower": FORTIFIED,
    "Tower House": FORTIFIED,
    "Gatehouse": FORTIFIED,
    # Prehistoric / early-medieval enclosure works — a different band entirely.
    "Hillfort": ENCLOSURE,
    "Enclosure": ENCLOSURE,
    "Enclosure - Defensive": ENCLOSURE,
    "Promontory Fort - inland": ENCLOSURE,
    "Promontory Fort - coastal": ENCLOSURE,
    "Promontory Fort- coastal": ENCLOSURE,   # the register's own typo, preserved
    "Rath": ENCLOSURE,
    "Camp": ENCLOSURE,
    # State/military works. Town defences sit here rather than in the strict
    # band on purpose: they are communal, and fortified_residence explicitly
    # excludes "urban defences and town walls (communal, not private)" while
    # state_fortification explicitly includes "urban citadels and town defences
    # held communally". The bands were written before this data existed and the
    # mapping follows them rather than the other way round.
    "Fort": STATE,
    "Roman Fort": STATE,
    "Legionary Fortress": STATE,
    "Town Defences": STATE,
    "Town Wall": STATE,
    # Palatial.
    "Bishops Palace": PALATIAL,
    "Palace": PALATIAL,
    "Manor": PALATIAL,
    "House (domestic)": PALATIAL,
    "Country House": PALATIAL,
    # NOT fortifications under any band here. Each None is a POSITIVE ASSERTION
    # that a register calling this thing a castle has made a category error, so
    # the list is kept to classes where that is genuinely defensible: a burial
    # monument is not a fortification under any definition on this site.
    "Mound": None,
    "Round Barrow": None,
    "Henge": None,
    "Standing Stone": None,
    "Cairn": None,
    "dovecote": None,
    "Farmstead": None,
    # Present with band None so the mapping is total; the CADW_DISPUTED branch
    # below relabels them as a dispute rather than an error.
    "Moated Site": None,
    "Vicus": None,
}

# Classes this project's bands EXCLUDE on a stance others reject. The exclusion
# is real — fortified_residence explicitly rules out "moated houses and walled
# sites with no active defensive capability", following Gatehouse — but it is a
# definitional position, not a fact, and Wikidata's "fortified manor house" is a
# respectable reading of the same structure. So these produce a band-conflict
# (the registers disagree) rather than a category-error (someone is wrong).
CADW_DISPUTED = {
    "Moated Site",
    "Vicus",   # the civil settlement beside a Roman fort — scope, not error
}

# Administratively vague: Cadw DECLINED to classify. Silence is not an
# assertion that the thing is not a fortification, and comparing against it
# would manufacture a disagreement out of a blank field.
CADW_UNCLASSIFIED = {
    "Building (Unclassified)",
    "Earthwork (unclassified)",
    "Unclassified site",
}

# Wikidata P31 labels -> band.
#
# CRITICAL ASYMMETRY WITH CADW_BANDS. A Cadw class mapped to None is a positive
# claim ("a round barrow is not a fortification"). A Wikidata class that is
# simply ABSENT from this dict is not a claim at all — it is our ignorance, and
# it must never be reported as a category error. An earlier pass conflated the
# two and duly accused Wikidata of category errors for classing things
# "ringwork castle", "fortified manor house" and "peel tower", which are
# obviously fortifications this map had not yet learned.
#
# Ambiguous terms are deliberately left out rather than guessed. Bare "tower" is
# the clearest case: one monument here is typed "archaeological site, chapel,
# church ruin, church tower, tower" and is a church. Mapping "tower" to the
# strict band would silently turn it into a castle.
WIKIDATA_BANDS: dict[str, str] = {
    "castle": FORTIFIED,
    "motte-and-bailey castle": FORTIFIED,
    "motte": FORTIFIED,
    "concentric castle": FORTIFIED,
    "shell keep": FORTIFIED,
    "tower house": FORTIFIED,
    "castle ruin": FORTIFIED,
    "fortification": FORTIFIED,
    "ringwork castle": FORTIFIED,
    "fortified manor house": FORTIFIED,
    "peel tower": FORTIFIED,
    "bastle house": FORTIFIED,
    "keep": FORTIFIED,
    "hillfort": ENCLOSURE,
    "contour fort": ENCLOSURE,
    "promontory fort": ENCLOSURE,
    "partial contour fort": ENCLOSURE,
    "hillslope fort": ENCLOSURE,
    "ringfort": ENCLOSURE,
    "Martello tower": STATE,
}

# Sentinel: "this project has no mapping for that class", as distinct from
# "that class is not a fortification". Never an accusation.
UNKNOWN = "UNKNOWN"

CADW_REGISTER = "gb-wls-cadw"
WD_REGISTER = "wikidata"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-") or "x"


def load_cadw() -> dict[str, dict]:
    out = {}
    for feat in json.loads(CADW_ALL.read_text())["features"]:
        p = feat["properties"]
        ref = (p.get("SAMNumber") or "").strip()
        if not ref:
            continue
        out[ref] = {
            "name": (p.get("Name") or "").strip(),
            "site_type": (p.get("SiteType") or "").strip(),
            "url": (p.get("Report") or "").strip() or None,
        }
    return out


def load_wikidata() -> dict[str, dict]:
    types: dict[str, set[str]] = collections.defaultdict(set)
    meta: dict[str, dict] = {}
    for b in json.loads(WIKIDATA.read_text())["results"]["bindings"]:
        ref = b["cadw"]["value"].strip()
        if "typeLabel" in b:
            types[ref].add(b["typeLabel"]["value"])
        meta[ref] = {
            "qid": b["item"]["value"].rsplit("/", 1)[-1],
            "name": b.get("itemLabel", {}).get("value", ""),
        }
    for ref, m in meta.items():
        m["types"] = types.get(ref, set())
    return meta


def band_of_wikidata(types: set[str]) -> tuple[str | None, str]:
    """Pick the most specific mapped class, preferring the fortified reading.

    Returns UNKNOWN — not None — when nothing is mapped. None would assert that
    Wikidata places the structure outside every band, which we are in no
    position to say.
    """
    mapped = {t: WIKIDATA_BANDS[t] for t in types if t in WIKIDATA_BANDS}
    if not mapped:
        return UNKNOWN, ", ".join(sorted(types)) or "(unclassified)"
    for term, band in sorted(mapped.items()):
        if band == FORTIFIED:
            return band, term
    term, band = sorted(mapped.items())[0]
    return band, term


def _row(ref, c, m, cadw_band, wd_band, wd_term, kind, basis) -> dict:
    return {
        "id": f"gb-wls-{slug(ref)}",
        "kind": kind,
        "left": {
            "register": CADW_REGISTER, "ref": ref, "name": c["name"],
            "classification": c["site_type"], "band": cadw_band,
            **({"url": c["url"]} if c["url"] else {}),
        },
        "right": {
            "register": WD_REGISTER, "ref": m["qid"], "name": m["name"],
            "classification": wd_term, "band": wd_band,
            "url": f"https://www.wikidata.org/wiki/{m['qid']}",
        },
        "site_id": None,   # filled by build() where this dataset holds the structure
        "basis": basis,
    }


def held_records() -> dict[str, str]:
    """Cadw ref -> local record id, for structures this dataset already holds."""
    out = {}
    for path in sorted((ROOT / "data" / "sites").glob("*.yml")):
        rec = yaml.safe_load(path.read_text())
        for entry in rec.get("register_entries") or []:
            if entry.get("register") == CADW_REGISTER:
                out[entry["ref"]] = rec["id"]
    return out


def build() -> dict:
    cadw = load_cadw()
    wd = load_wikidata()
    held = held_records()

    rows = []
    unknown_wd: collections.Counter = collections.Counter()
    unclassified = 0
    # SYMMETRIC. An earlier pass started only from "Wikidata says castle" and was
    # blind to the opposite direction — Cadw calling something a Castle that
    # Wikidata calls a hillfort is exactly as much a disagreement, and two of
    # them sit inside this dataset's own closed Welsh cell. Iterating the join
    # instead of one register's castle set catches both.
    for ref, m in sorted(wd.items()):
        c = cadw.get(ref)
        if not c or not c["site_type"]:
            continue                      # unresolvable; silence beats a guess

        wd_band, wd_term = band_of_wikidata(m["types"])
        if c["site_type"] in CADW_UNCLASSIFIED:
            unclassified += 1
            continue
        cadw_band = CADW_BANDS.get(c["site_type"], "UNMAPPED")

        # RELEVANCE FIRST, then mapping gaps. Wales has ~200 scheduled-monument
        # classes and most are bridges, cairns and lead mines; warning about
        # every one of them would bury the handful that actually bear on a
        # castle argument. A monument is in scope only if at least one register
        # places it in the strict band.
        if wd_band == UNKNOWN and "castle" not in m["types"]:
            unknown_wd[wd_term] += 1
            continue
        wd_castleish = wd_band == FORTIFIED or "castle" in m["types"]
        cadw_castleish = cadw_band == FORTIFIED
        if not (wd_castleish or cadw_castleish):
            continue

        if cadw_band == "UNMAPPED":
            # NOW it is a gap in OUR mapping and worth saying so, because a
            # register has called this thing a castle and we cannot place it.
            print(f"  note: unmapped Cadw SiteType {c['site_type']!r} ({ref}, "
                  f"{c['name'][:40]}) — add it to CADW_BANDS deliberately",
                  file=sys.stderr)
            continue

        if wd_band == UNKNOWN:
            # Wikidata says "castle" among other unmapped terms; treat the
            # castle assertion as the mapped one rather than guessing.
            wd_band, wd_term = FORTIFIED, "castle"

        if cadw_band is None and wd_band is None:
            continue

        if cadw_band == wd_band:
            # Same band. Only a `granularity` row if the terms actually differ.
            if c["site_type"] == "Castle" or wd_term == c["site_type"].lower():
                continue
            rows.append(_row(ref, c, m, cadw_band, wd_band, wd_term, "granularity",
                f"Both map to {cadw_band}. Cadw is more specific ({c['site_type']}) "
                f"than Wikidata ({wd_term}); the registers agree about the kind of "
                f"thing and differ only in precision."))
            continue

        if c["site_type"] in CADW_DISPUTED:
            kind, basis = "band-conflict", (
                f"Cadw classes this {c['site_type']}; Wikidata's {wd_term} maps to "
                f"{wd_band}. This project's bands EXCLUDE {c['site_type'].lower()}s — "
                f"fortified_residence rules out passive defences without active "
                f"defensive capability — but that exclusion is a definitional stance "
                f"others reject, not a fact. Recorded as a dispute between readings "
                f"rather than as anyone's error.")
        elif cadw_band is None:
            kind, basis = "category-error", (
                f"Cadw classes this {c['site_type']}, which maps to no definition band "
                f"— under this project's bands it is not a fortification at all. "
                f"Wikidata's {wd_term} maps to {wd_band}. One of the two is wrong.")
        elif wd_band is None:
            kind, basis = "category-error", (
                f"Wikidata classes this {wd_term}, which maps to no definition band — "
                f"under this project's bands it is not a fortification at all. Cadw's "
                f"{c['site_type']} maps to {cadw_band}. One of the two is wrong.")
        else:
            kind, basis = "band-conflict", (
                f"Cadw's {c['site_type']} maps to {cadw_band}; Wikidata's {wd_term} maps "
                f"to {wd_band}. The registers disagree about what KIND of thing this is, "
                f"not merely how precisely to describe it.")
        rows.append(_row(ref, c, m, cadw_band, wd_band, wd_term, kind, basis))

    granular = []
    if unclassified:
        print(f"  note: {unclassified} monument(s) skipped — Cadw declined to classify "
              f"them, and silence is not a claim", file=sys.stderr)
    for term, n in unknown_wd.most_common(10):
        print(f"  note: no Wikidata band mapping for {term!r} ({n}x) — skipped rather "
              f"than reported as an error", file=sys.stderr)

    for r in rows:
        r["site_id"] = held.get(r["left"]["ref"])

    allrows = sorted(rows + granular, key=lambda r: (r["kind"], r["id"]))
    return {
        "version": 1,
        "generated_from": {
            "registers": [CADW_REGISTER, WD_REGISTER],
            "join": "Wikidata P3007 (Cadw Monument ID) == Cadw SAMNumber",
            "note": (
                "Joined on an identifier, never a name. SYMMETRIC: a row is emitted "
                "whenever the two registers place the same monument in different "
                "definition bands, in either direction — Cadw calling a Castle what "
                "Wikidata calls a hillfort counts exactly as much as the reverse. "
                "Generated by scripts/analyse_disagreements.py from the "
                "committed snapshots; CI fails on drift. The band mapping lives in "
                "that script and is the reviewable artefact — every row carries the "
                "band each register's class was mapped to, so a reader can disagree "
                "with the mapping without reading the code."
            ),
        },
        "disagreements": allrows,
    }


def render(doc: dict) -> str:
    header = (
        "# Where two registers classify the same structure differently.\n"
        "#\n"
        "# GENERATED by scripts/analyse_disagreements.py — do not hand-edit.\n"
        "# CI regenerates this file and fails on drift.\n"
        "#\n"
        "# `kind` is the point. granularity = same band, different precision (nobody\n"
        "# is wrong). band-conflict = different bands (a real dispute). category-error\n"
        "# = one register's class maps to no band at all (someone is wrong).\n"
    )
    return header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    doc = build()
    text = render(doc)
    kinds = collections.Counter(d["kind"] for d in doc["disagreements"])

    if args.check:
        if not OUT.exists() or OUT.read_text() != text:
            print("disagreements: STALE — run scripts/analyse_disagreements.py and commit.",
                  file=sys.stderr)
            return 1
        print(f"disagreements: fresh ({len(doc['disagreements'])} rows)")
        return 0

    OUT.write_text(text)
    print(f"disagreements: wrote {len(doc['disagreements'])} rows — "
          + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
