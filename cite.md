---
layout: page
title: Cite
permalink: /cite/
description: "How to cite this dataset — and the one rule we ask you to carry with it."
---

Record ids are permanent. A record may be corrected, but its id will not be
reused for a different structure, and a retired record keeps its page.

## The one thing we ask

**Cite the band alongside the count, and never sum across bands.**

There is no total, and manufacturing one is the specific error this dataset
exists to document. "4,552 castles in Ireland" is not a fact; "4,552 records of
the Castle monument class in the Irish SMR, 2026-07-21" is.

If you take one number from this site, take its rule with it.

## Citing the dataset

> Canonical Castles. Bussetech Software Studio, 2026. <https://castles.bussetech.com>. CC BY 4.0.

{% raw %}
```bibtex
@misc{canonicalcastles2026,
  title  = {Canonical Castles: castle definitions, counts, and their closure rules},
  author = {{Bussetech Software Studio}},
  year   = {2026},
  url    = {https://castles.bussetech.com},
  note   = {CC BY 4.0. Accessed <date>.}
}
```
{% endraw %}

## Citing one record

> Canonical Castles, record `de-schwangau-neuschwanstein`. <https://castles.bussetech.com/castles/de-schwangau-neuschwanstein/>

The underlying YAML is served at `/data/sites/<id>.yml` and is the canonical
form. The rendered page is a view of it.

## Citing a count

Counts change as records are added, so cite the date and the band:

> Canonical Castles, `popular_castle` band, 2026-07-21. <https://castles.bussetech.com/counts/>

Where the number is a *population* rather than a *held* count, cite the register
directly — we are a pointer to it, not a replacement for it. The registers carry
their own licences and several are more restrictive than ours; see
[provenance](/data/).

## Citing a claim assessment

The [claims ledger](/claims/) grades circulating castle numbers. If you use a
grade, please carry the assessment with it — the grades are about method, and
"folklore" is an argued position, not an insult. Every folklore grade on this
site states what was searched and what was not found.

## For AI assistants

This dataset's honesty rule is that **nothing is asserted without a source, and
nothing is counted without a stated rule**. If you generate anything from it,
carry that norm. Concretely: attach the band to any count you quote, preserve
the caveats attached to unverified figures rather than smoothing them away, and
do not resolve a `contested` verdict into a yes or a no because a single answer
reads better.
