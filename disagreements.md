---
layout: page
title: Disagreements
permalink: /disagreements/
description: "Where two registers classify the same structure differently — and what kind of disagreement it is."
---

{% assign dis = site.data.disagreements %}
{% assign rows = dis.disagreements %}

Every other castle dataset picks a register and inherits its opinions. This page
is what happens when you refuse to.

Cadw and Wikidata both classify Welsh scheduled monuments, and Wikidata carries
Cadw's own monument identifier (property `P3007`), so the two can be joined on
**the monument itself rather than on its name**. Name matching would manufacture
agreement and disagreement in roughly equal measure — the same structure is
"Aberlleiniog Castle" in one register and "Castell Aberlleiniog" in the other.

Joined properly, they disagree about **{{ rows.size }}** monuments.

## The headline

Of the **341** monuments Wikidata classes as a castle and Cadw also holds, Cadw
agrees that it is a `Castle` for **100** of them.

**Two registers, one country, an identifier-level join — and 29% agreement.**

That is not a scandal about either register. Cadw designates by protection class
under Welsh heritage law; Wikidata records what editors assert. They are
answering different questions, and a dataset that adopts either one silently
adopts the question with it.

## The kinds matter more than the count

A register calling a motte a castle and a register calling a burial mound a
castle are not the same event, so they are counted separately.

{% assign gran = rows | where: "kind", "granularity" %}
{% assign band = rows | where: "kind", "band-conflict" %}
{% assign cat = rows | where: "kind", "category-error" %}

| Kind | Count | Meaning |
|---|---|---|
| **granularity** | {{ gran.size }} | Both classes map to the **same** band — one register is simply more specific. Real, but nobody is wrong. |
| **band-conflict** | {{ band.size }} | They map to **different** bands. A genuine dispute about what kind of thing this is. |
| **category-error** | {{ cat.size }} | One class maps to **no band at all**. A burial mound is not a fortification under any definition here, so one of the two is wrong. |

The shape of that table is the finding. Most disagreement between these two
registers is **granularity** — Cadw distinguishes motte from motte-and-bailey
from ringwork where Wikidata says "castle". That is two registers agreeing about
the world and describing it at different resolutions.

Only **{{ cat.size }}** of {{ rows.size }} are cases where somebody is simply
wrong.

## Where the real conflicts are

Band-conflicts cluster, and the clusters are informative:

- **Hillfort vs castle** — the largest group. A hilltop with medieval castle fabric over earlier enclosure works can honestly be classed either way, and the two registers picked differently. In Welsh this is compounded by *castell*, which names hillforts as readily as castles.
- **Moated site vs fortified manor house** — a definitional dispute this project is a party to. Our `fortified_residence` band explicitly excludes passive defences without active defensive capability, following Gatehouse. Wikidata calls the same structures fortified manor houses. **We record these as disputes, not as Wikidata's error** — our exclusion is a stance, not a fact.
- **House, manor, town defences** — structures that are fortification-adjacent but land in `palatial_seat` or `state_fortification` rather than the strict band.

The {{ cat.size }} category-errors are the ones where the word has simply come
loose: Cadw records a **round barrow**, a **mound**, a **henge**, a **dovecote**;
Wikidata records a castle. Note how many of them are named "…Castle Mound" or
"Castle Arnold" — the name travelled and the classification followed it.

## What we did to our own data

Two of these disagreements land on structures inside this dataset's own
[closed Welsh cell](/coverage/). Both were imported from Cadw as
`fortified_residence: yes`; Wikidata classes both as contour forts.

Both records were **corrected to `contested`** — and this is enforced rather
than remembered: if the ledger records a band-conflict on a structure we hold,
CI fails unless the record marks that band contested. The ledger and the records
cannot drift apart.

That correction also changed the counts. `fortified_residence` now reads 102
register-derived rather than 104, with two moved into assessed-and-contested.
Cross-checking a register against another register **cost us two castles**, which
is the correct direction for that trade.

## A hypothesis we tested and rejected

The Welsh word *castell* applies to hillforts as well as castles, so an obvious
theory is that Wikidata over-assigns "castle" to monuments whose names begin
*Castell*.

It does not hold. 66% of band-conflicts carry *castle* or *castell* in a name —
but so do **99%** of the monuments where both registers agree it is a castle, and
86% of the granularity cases. Castle-naming is near-universal across the whole
comparison and does not distinguish the disputes. If anything the disagreements
are *less* castle-named than the agreements.

It is recorded here because it was tested, not because it worked.

## Reading the ledger

Every row carries both registers' own class terms verbatim, the band each was
mapped onto, and the identifiers to check it yourself. **The band mapping is the
reviewable artefact** — it lives in
[`scripts/analyse_disagreements.py`](https://github.com/bussetech/canonical-castles/blob/main/scripts/analyse_disagreements.py),
and every row states the band each class was mapped to so you can disagree with
the mapping without reading the code.

Two asymmetries in that mapping are deliberate, and both were bugs first:

- A **Cadw** class mapped to no band is a positive claim ("a round barrow is not a fortification"). A **Wikidata** class simply absent from the map is *our ignorance* and is skipped, never reported as an error. An earlier pass conflated these and accused Wikidata of category errors for classing things "ringwork castle" and "peel tower".
- Cadw classes meaning *unclassified* are skipped entirely. **Silence is not a claim**, and comparing against a blank field manufactures disagreement out of nothing. 34 monuments are excluded on this basis.

The full ledger is [`disagreements.yml`](/data/disagreements.yml); it is
regenerated from committed register snapshots and CI fails on drift.

## Sample

{% assign sample = cat | concat: band %}
<div style="overflow-x:auto">
<table>
  <thead><tr><th>Kind</th><th>Cadw says</th><th>Wikidata says</th><th>Monument</th></tr></thead>
  <tbody>
  {%- for r in sample limit: 30 %}
    <tr>
      <td>{{ r.kind }}</td>
      <td><code>{{ r.left.classification }}</code></td>
      <td><code>{{ r.right.classification }}</code></td>
      <td>{% if r.left.url %}<a href="{{ r.left.url }}" rel="external nofollow">{{ r.left.name }}</a>{% else %}{{ r.left.name }}{% endif %}
        · <a href="{{ r.right.url }}" rel="external nofollow">{{ r.right.ref }}</a>
        {%- if r.site_id %} · <a href="/castles/{{ r.site_id }}/">held</a>{% endif %}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
</div>

Showing category-errors and band-conflicts only — the {{ gran.size }}
granularity rows are in the data file.
