---
layout: home
title: Canonical Castles
description: "How many castles are there? A source-cited dataset that answers per definition, not in general — every structure records which definitions of castle it satisfies, and every definition carries its own count and its own closure rule."
---

**How many castles are there?**

The honest answer is that the question has no single number, and the reason is
not missing data. It is that "castle" names at least six different things, and
each one has a different count.

Ireland proves it in a single database. The state's own Sites and Monuments
Record answers "how many castles?" with **129**, **4,552** or **31,431** —
depending purely on which class filter you accept, on the same day, from the
same official source. Nothing about the buildings changes. Only the word does.

So this dataset never records that something *is* a castle. It records a
verdict against each of six named [definitions](/definitions/), with the
reasoning that produced it and the sources behind it — and it publishes
[a count per definition](/counts/), never a total across them.

## What that looks like

Schloss Moritzburg, in the Saxony whose coverage gap started all this:

| Definition | Verdict |
|---|---|
| Fortified residence | **no** — the water setting is ornamental; no wall walks, no parapets |
| Palatial seat | **yes** — the paradigm *Schloss*, rebuilt 1723–1736 as a baroque hunting palace |
| Popularly a castle | **yes** — signposted as Schloss Moritzburg, rendered "Moritzburg Castle" in English |
| Revival / folly | **no** — a genuine early-modern residence, not castle-form built for effect |

A dataset with one castle field has to lie about one of those rows.

## Why this exists

A [Hacker News thread](https://news.ycombinator.com/item?id=48994178) took apart
a map of "the world's 2,400 castles". The coverage complaints were loud —
Saxony showing nine, France showing about a hundred — but the deeper problem was
quieter: it published **a single integer for a contested term**.

Its own criteria (a photo, an English Wikipedia article, coordinates) define
about 6,594 Wikidata items. It publishes 2,435 of them — roughly 37% of the
population its own filter describes. The underlying map is careful, openly
licensed and honest about its Wikidata provenance. The number on the label is
the problem: "The World's 2,400 Castles" reads as a census when it is a
selection.

We think that is the general failure, not a local one. So:

- **[Definitions](/definitions/)** — the six bands, each with a named authority, an explicit criterion, and its own closure rule
- **[Counts](/counts/)** — a number per band, and a plain statement of which ones can ever be finished
- **[Castles](/castles/)** — the records, each carrying six verdicts rather than one
- **[Claims](/claims/)** — the castle numbers people repeat, graded by how well they are sourced. "France has 45,000 châteaux" turns out to be folklore with no traceable origin
- **[Coverage](/coverage/)** — what has been surveyed, what has not, and which register would settle each open cell

## The rule we hold ourselves to

Three bands can in principle be counted to completion, because national
registers bound them. Three cannot, and never will. Where a band closes, we
publish an integer. Where it does not, we publish a range with its assumptions
showing — and we never quietly promote one into the other.

Every number on this site is regenerated from the records by
[`scripts/counts.py`](https://github.com/bussetech/canonical-castles/blob/main/scripts/counts.py),
and the build fails if a published figure drifts from the data behind it.

This is a [Bussetech Software Studio](https://bussetech.com) project. Its data
lives in the repo as text — see [the datasets](/data/) — and the site is rebuilt
from it on every change.
