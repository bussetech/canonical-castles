---
layout: page
title: Counts
permalink: /counts/
description: "One number per definition. Never a total across them — that would double-count every structure satisfying more than one."
---

{% assign counts = site.data.counts %}
{% assign defs = site.data.definitions.definitions %}

**There is no total on this page, and there will never be one.** Summing the
bands would double-count every structure that satisfies more than one — most of
them — and would re-create exactly the single global integer this project
exists to reject.

Two different questions get two different columns, and conflating them is the
most common error in this field:

- **Held** — how many records *this dataset* holds. A fact about our progress.
- **Population** — how many exist in the world, per the bounding register. A fact about castles.

And a third distinction, which matters just as much:

- **Assessed** — somebody applied the band's criterion to the structure.
- **Register-derived** — a register asserted its own typology and we transcribed it in bulk.

They are never summed. Copying 104 rows out of Cadw is not the same act as
assessing 104 structures, and a headline that added them together would be a
dataset reporting how many rows it copied. Register-derived verdicts all carry
`confidence: low` and say so on every record.

## Per definition

{% for band in counts.bands %}{% assign d = defs | where: "id", band.definition | first %}
### {{ d.label }}

| | assessed | register-derived |
|---|---|---|
| Satisfies this definition | **{{ band.held.assessed.yes }}** | {{ band.held.register_derived.yes }} |
| Contested | {{ band.held.assessed.contested }} | {{ band.held.register_derived.contested }} |
| Does not satisfy | {{ band.held.assessed.no }} | {{ band.held.register_derived.no }} |
| Unassessed | {{ band.held.unassessed }} | |
| Closure | **{{ band.closure }}** | |

{{ d.closure_note }}
{% endfor %}

Held counts are derived from {{ counts.records_total }} records by
[`scripts/counts.py`](https://github.com/bussetech/canonical-castles/blob/main/scripts/counts.py).
CI regenerates this file and fails on drift, so a number here cannot disagree
with the records behind it.

## Contested is a result, not a gap

A verdict of *contested* means competent sources genuinely disagree under that
band's criterion — not that we could not be bothered. It is reported in its own
column and never folded into yes or no.

[Crac des Chevaliers](/castles/sy-homs-crac-des-chevaliers/) is contested on two
bands at once because the Knights Hospitaller sit between "private lord" and
"state", and those are precisely the categories the criteria depend on. The
ambiguity is in the twelfth century, not in our evidence.

## Where the real populations are

Held counts are small; this dataset is young. The bounding registers are not,
and these are the figures that matter:

| Population | Count | Register |
|---|---|---|
| Irish ringfort-class monuments | 31,431 | Archaeological Survey of Ireland |
| Irish Castle-class monuments | 4,552 | Archaeological Survey of Ireland |
| Irish Anglo-Norman masonry castles | 129 | Archaeological Survey of Ireland |
| French protected châteaux | 6,286 | Base Mérimée (one of four defensible tokenisations) |
| Hillforts of Britain and Ireland | 4,147 | Atlas of Hillforts |
| Welsh scheduled castles | 104 | Cadw |
| Wikidata castle-class items | 36,716 | Wikidata (24,886 without the subclass walk) |
| OSM `historic=castle` | 54,182 | OpenStreetMap |

The first three rows are the same country, the same register and the same day.

## The number that started this

Of the 28,544 OpenStreetMap objects carrying a `castle_type`, only **19.5%** are
tagged `defensive`. The rest are *stately* (23.7%), *manor* (20.5%), *palace*
(16.4%) and *fortress* (10.9%).

Read one way, four in five things tagged as castles are misfiled. Read the other
way, the crowd's working definition of "castle" is overwhelmingly *stately
residence*, and the scholars are the ones out of step with usage.

Both readings are defensible. That is the finding.

See also: [the claims ledger](/claims/), where circulating castle numbers are
graded by how well they are sourced.
