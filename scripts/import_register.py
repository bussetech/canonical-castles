#!/usr/bin/env python3
"""Import a heritage register into signals and register-derived records.

DETERMINISTIC. This makes no model call, and that is a design property rather
than a happy accident: a register row is a mechanical transform, and the studio
rubric is explicit that deterministic work is code, not a gnome. It is also what
makes bulk import affordable — 4,552 Irish records through a model would cost
more than the studio's monthly budget to produce something a script produces for
nothing.

WHAT IT DELIBERATELY DOES NOT DO

It does not decide whether anything is a castle. A register row is ONE CLAIM
FROM ONE SOURCE, which is precisely the archetype's signal shape, so that is
what it emits. The record it then writes carries the register's own
classification as a `register-derived` verdict at `confidence: low`, marked so
that counts never fold it in with assessed verdicts.

That boundary is the whole reason this project exists. A dataset that ingests
Cadw's SiteType=Castle and reports 104 assessed castles has not counted castles;
it has copied Cadw. What it has genuinely done — and this is worth a lot — is
establish that the Welsh cell CAN be closed, and against exactly what.

FETCH AND TRANSFORM ARE SEPARATE. `--fetch` hits the network and writes a
verbatim snapshot under data/snapshots/. `--transform` reads that snapshot and
emits YAML. CI only ever runs the transform, against the committed snapshot, so
the build is hermetic and the import is reproducible: re-fetch, compare
checksums, and any drift in the register is visible as a diff.

Usage:
    scripts/import_register.py --register gb-wls-cadw --fetch
    scripts/import_register.py --register gb-wls-cadw --transform
    scripts/import_register.py --register gb-wls-cadw --transform --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import unicodedata

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAPSHOTS = ROOT / "data" / "snapshots"
SIGNALS = ROOT / "data" / "signals"
SITES = ROOT / "data" / "sites"

TODAY = "2026-07-21"

SITE_KEY_ORDER = [
    "id", "name", "name_local", "also_known_as", "tradition", "location",
    "built", "condition", "definitions_met", "register_entries", "disputed",
    "dispute_note", "first_seen", "last_updated", "confidence", "sources",
    "signals", "notes",
]
SIGNAL_KEY_ORDER = [
    "id", "site_id", "site_hint", "attribute", "value", "source_url",
    "source_title", "publisher", "source_date", "observed_date",
    "collected_by", "confidence", "notes",
]

# Generic words dropped when slugging a structure name for an id. "castle" goes
# because every record here is one — keeping it would make every id say so.
STOPWORDS = {
    "castle", "castell", "chateau", "château", "schloss", "the", "y", "yr",
    "a", "of", "and",
}


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text).strip().lower()
    parts = [w for w in text.split() if w not in STOPWORDS]
    if not parts:  # a name that was nothing but stopwords ("The Castle")
        parts = [w for w in text.split()] or ["unnamed"]
    return "-".join(parts)


# --------------------------------------------------------------------------
# Register adapters. Each returns a list of normalised dicts; everything below
# this point is register-agnostic.
# --------------------------------------------------------------------------

class CadwCastles:
    """Cadw scheduled monuments, SiteType = 'Castle' (Wales).

    Case matters and silently: SiteType='castle' returns zero rather than
    erroring, so the filter is asserted against the expected count rather than
    trusted.
    """

    register_id = "gb-wls-cadw"
    snapshot = "gb-wls-cadw-castles.json"
    expected = 104
    band = "fortified_residence"
    wfs = "https://datamap.gov.wales/geoserver/ows"
    params = {
        "service": "WFS", "version": "2.0.0", "request": "GetFeature",
        "typeName": "inspire-wg:Cadw_SAM", "outputFormat": "application/json",
        "srsName": "EPSG:4326", "CQL_FILTER": "SiteType='Castle'",
    }
    source_title = "Cof Cymru - National Historic Assets of Wales"
    publisher = "Cadw"
    landing = "https://cadw.gov.wales/advice-support/cof-cymru"

    def fetch(self) -> bytes:
        import urllib.parse
        import urllib.request
        url = f"{self.wfs}?{urllib.parse.urlencode(self.params)}"
        with urllib.request.urlopen(url, timeout=180) as fh:  # noqa: S310
            return fh.read()

    @staticmethod
    def _centroid(geom: dict | None) -> tuple[float | None, float | None]:
        """Representative point from a (Multi)Polygon ring — mean of its vertices.

        Deliberately crude: it locates the monument on a map and nothing more.
        A proper centroid would need a geometry library for no gain, and any
        precision implied beyond "roughly here" would be false.
        """
        if not geom:
            return None, None
        coords = geom.get("coordinates") or []
        pts: list[list[float]] = []

        def walk(node):
            if (isinstance(node, list) and len(node) == 2
                    and all(isinstance(x, (int, float)) for x in node)):
                pts.append(node)
            elif isinstance(node, list):
                for child in node:
                    walk(child)

        walk(coords)
        if not pts:
            return None, None
        return (round(sum(p[1] for p in pts) / len(pts), 5),
                round(sum(p[0] for p in pts) / len(pts), 5))

    def normalise(self, raw: dict) -> list[dict]:
        out = []
        for feat in raw["features"]:
            p = feat["properties"]
            sam = (p.get("SAMNumber") or "").strip()
            name = (p.get("Name") or "").strip()
            name_cy = (p.get("Name_cy") or "").strip()
            lat, lon = self._centroid(feat.get("geometry"))
            out.append({
                "ref": sam,
                "name": name,
                "name_local": name_cy if name_cy and name_cy != name else None,
                "locality": (p.get("Community") or "").strip() or None,
                "county": (p.get("UnitaryAuthority") or "").strip() or None,
                "period": (p.get("Period") or "").strip() or None,
                "site_type": (p.get("SiteType") or "").strip(),
                "broad_class": (p.get("BroadClass") or "").strip(),
                "url": (p.get("Report") or "").strip() or None,
                "lat": lat, "lon": lon,
            })
        return out

    def signal_id(self, item: dict) -> str:
        return f"sig-{TODAY.replace('-', '')}-cadw-{slug(item['ref'])}"

    def record_id(self, item: dict) -> str:
        place = item.get("locality") or item.get("county") or "wales"
        return f"gb-{slug(place)}-{slug(item['name'])}"

    def signal(self, item: dict) -> dict:
        return {
            "id": self.signal_id(item),
            "site_id": None,
            "site_hint": f"{item['name']} — {item.get('county') or 'Wales'}, GB",
            "attribute": "register_entry",
            "value": (f"Scheduled monument {item['ref']}. "
                      f"SiteType: {item['site_type']}. "
                      f"BroadClass: {item['broad_class']}."
                      + (f" Period: {item['period']}." if item.get("period") else "")),
            "source_url": item.get("url") or self.landing,
            "source_title": self.source_title,
            "publisher": self.publisher,
            "source_date": TODAY,
            "observed_date": TODAY,
            "collected_by": "import/gb-wls-cadw@1.0.0",
            "confidence": "high",
            "notes": ("Register classification, not an assessment against this "
                      "project's criterion. Cadw asserts its own typology; whether "
                      "the structure meets the fortified_residence criterion is a "
                      "separate question nobody has answered for this entry."),
        }

    def record(self, item: dict, signal_id: str) -> dict:
        period = item.get("period")
        rec = {
            "id": self.record_id(item),
            "name": item["name"],
            "tradition": "european_medieval",
            "location": {"country": "GB", "region": "Wales"},
            "definitions_met": {
                self.band: {
                    "verdict": "yes",
                    "assessment": "register-derived",
                    "basis": (
                        f"Cadw classes scheduled monument {item['ref']} as "
                        f"SiteType: Castle within BroadClass: {item['broad_class']}. "
                        "This verdict is transcribed from the register's own typology "
                        "and NOT assessed against this band's criterion — the register "
                        "designates by protection class, and its inclusion rule is not "
                        "this band's rule. Treat as provisional."
                    ),
                }
            },
            "register_entries": [{
                "register": self.register_id,
                "ref": item["ref"],
                "designation": f"Scheduled Monument — SiteType: {item['site_type']}",
            }],
            "first_seen": TODAY,
            "last_updated": TODAY,
            "confidence": "low",
            "sources": [{
                "url": item.get("url") or self.landing,
                "title": self.source_title,
                "publisher": self.publisher,
                "date": TODAY,
                "note": "Register entry; the sole source for this record.",
            }],
            "signals": [signal_id],
            "notes": (
                "Imported in bulk from Cadw's scheduled-monument register. One "
                "register speaks and nothing corroborates it, hence confidence: low. "
                "Only fortified_residence carries a verdict; every other band is "
                "OMITTED rather than set to no, because no source consulted so far "
                "speaks to them. Upgrading this record means applying the bands to "
                "the structure itself and setting assessment: assessed."
            ),
        }
        if item.get("name_local"):
            rec["name_local"] = item["name_local"]
        if item.get("locality"):
            rec["location"]["locality"] = item["locality"]
        if item.get("county"):
            rec["location"]["county"] = item["county"]
        if item.get("lat") is not None:
            rec["location"]["lat"] = item["lat"]
            rec["location"]["lon"] = item["lon"]
        if period:
            rec["built"] = {"period": period}
        if item.get("url"):
            rec["register_entries"][0]["url"] = item["url"]
        return rec


ADAPTERS = {"gb-wls-cadw": CadwCastles}


def dump(obj: dict, order: list[str]) -> str:
    return yaml.safe_dump({k: obj[k] for k in order if k in obj},
                          sort_keys=False, allow_unicode=True, width=88)


def resolve_ids(adapter, items: list[dict]) -> dict[str, str]:
    """Apply the id rule, including its collision clause, deterministically."""
    taken: dict[str, str] = {}
    assigned: dict[str, str] = {}
    for item in items:
        base = adapter.record_id(item)
        rid = base
        if rid in taken:
            county = slug(item.get("county") or "")
            rid = f"{base}-{county}" if county else base
            n = 2
            while rid in taken:
                rid = f"{base}-{n}"
                n += 1
        taken[rid] = item["ref"]
        assigned[item["ref"]] = rid
    return assigned


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", required=True, choices=sorted(ADAPTERS))
    ap.add_argument("--fetch", action="store_true", help="hit the network, write a snapshot")
    ap.add_argument("--transform", action="store_true", help="snapshot -> YAML")
    ap.add_argument("--check", action="store_true", help="fail on drift instead of writing")
    args = ap.parse_args()

    adapter = ADAPTERS[args.register]()
    snap = SNAPSHOTS / adapter.snapshot

    if args.fetch:
        SNAPSHOTS.mkdir(parents=True, exist_ok=True)
        body = adapter.fetch()
        snap.write_bytes(body)
        print(f"fetch: wrote {snap.relative_to(ROOT)} "
              f"({len(body) // 1024} KB, sha256 {hashlib.sha256(body).hexdigest()[:16]}…)")
        if not args.transform:
            return 0

    if not args.transform:
        ap.error("nothing to do — pass --fetch and/or --transform")

    if not snap.is_file():
        print(f"transform: no snapshot at {snap.relative_to(ROOT)} — run --fetch first",
              file=sys.stderr)
        return 1

    body = snap.read_bytes()
    raw = json.loads(body)
    items = adapter.normalise(raw)

    # The filter is asserted, not trusted: a mis-cased CQL filter returns zero
    # rather than erroring, and a silently empty import would read as "done".
    if len(items) != adapter.expected:
        print(f"transform: expected {adapter.expected} features, snapshot has {len(items)}.\n"
              f"  Either the register moved or the query changed. Both need a human — "
              f"update `expected` deliberately, never to make this pass.", file=sys.stderr)
        return 1

    ids = resolve_ids(adapter, items)
    adopted_ids: list[str] = []

    def adopted(path: pathlib.Path, band: str) -> bool:
        """Has a human taken this record over from the importer?

        IMPORT SEEDS A RECORD; IT DOES NOT OWN ONE. The moment somebody upgrades
        a band from `register-derived` to `assessed` — by weighing a second
        register, or by reading the site — that record is theirs and a re-import
        must not overwrite it. Without this, the drift check would helpfully
        revert every correction anyone ever made, which is the failure mode
        where a pipeline quietly outranks a person.
        """
        if not path.exists():
            return False
        try:
            existing = yaml.safe_load(path.read_text())
        except Exception:
            return False
        entry = ((existing or {}).get("definitions_met") or {}).get(band) or {}
        return entry.get("assessment") == "assessed"

    wanted: dict[pathlib.Path, str] = {}
    for item in items:
        rid = ids[item["ref"]]
        sig = adapter.signal(item)
        sig["site_id"] = rid
        sig.pop("site_hint", None)  # resolved: the contract says omit it
        rec = adapter.record(item, sig["id"])
        rec["id"] = rid
        wanted[SIGNALS / f"{sig['id']}.yml"] = dump(sig, SIGNAL_KEY_ORDER)
        site_path = SITES / f"{rid}.yml"
        if adopted(site_path, adapter.band):
            adopted_ids.append(rid)
        else:
            wanted[site_path] = dump(rec, SITE_KEY_ORDER)

    stale = [p.name for p, text in wanted.items()
             if not p.exists() or p.read_text() != text]

    if args.check:
        if stale:
            print(f"import: STALE — {len(stale)} file(s) differ from the snapshot, e.g. "
                  f"{', '.join(stale[:3])}\n  Run scripts/import_register.py "
                  f"--register {args.register} --transform and commit.", file=sys.stderr)
            return 1
        print(f"import[{args.register}]: fresh ({len(items)} entries"
              + (f", {len(adopted_ids)} adopted and left alone)" if adopted_ids else ")"))
        return 0

    SIGNALS.mkdir(parents=True, exist_ok=True)
    SITES.mkdir(parents=True, exist_ok=True)
    for path, text in wanted.items():
        path.write_text(text)
    print(f"import[{args.register}]: wrote {len(items)} signals + "
          f"{len(items) - len(adopted_ids)} records ({len(stale)} changed"
          + (f", {len(adopted_ids)} adopted: {', '.join(adopted_ids)})" if adopted_ids else ")"))
    print(f"  snapshot sha256: {hashlib.sha256(body).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
