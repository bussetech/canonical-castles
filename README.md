# Canonical Castles

**How many castles are there?** There is no single answer, and the reason is not
missing data — "castle" names at least six different things, and each has a
different count.

Live at **<https://castles.bussetech.com>**.

This dataset never records that something *is* a castle. It records a verdict
against each of six named definition bands, each with a cited authority, an
explicit criterion, and its own closure rule. Counts are published per band and
never summed.

Ireland proves the point in a single database: the state's Sites and Monuments
Record answers "how many castles?" with **129**, **4,552** or **31,431**,
depending purely on which class filter you accept.

## Why

A [Hacker News thread](https://news.ycombinator.com/item?id=48994178) took apart
a map of "the world's 2,400 castles". The coverage gaps were loud; the deeper
problem was that it published a single integer for a contested term. Its own
stated criteria define ~6,594 Wikidata items and it publishes 2,435 of them.

## Layout

| path | what |
|---|---|
| `data/definitions.yml` | The six bands — the spine |
| `data/sites/` | One structure per file, with a verdict per band |
| `data/registers.yml` | Inventories a count can close against, with the exact query |
| `data/claims.yml` | Circulating castle numbers, graded by method |
| `data/coverage.yml` | The (definition x jurisdiction) grid |
| `scripts/counts.py` | Derives every published number; CI fails on drift |

## Documents

- [Figures](https://castles.bussetech.com/figures/) — the shape of the data ([how they are built](docs/viz.md))
- [Roadmap](docs/roadmap.md) — what is planned, and what is deliberately not
- [ADR 0001](docs/decisions/0001-importers-do-not-own-human-judgement.md) — importers seed records, they do not own them
- [Founding proposal](docs/founding/) — the founder gnome's proposal, preserved, with an as-built delta

## Local

```sh
python3 -m venv .venv && .venv/bin/pip install pyyaml jsonschema
PYTHON=.venv/bin/python bash scripts/check-integrity.sh   # integrity + drift
bundle install && bundle exec jekyll serve                # the site
```

Data is CC BY 4.0; code is MIT. See [provenance](https://castles.bussetech.com/data/)
— the seed dataset was collected by hand from a console session, not by an agent,
and the site says so.

A [Bussetech Software Studio](https://bussetech.com) project.
