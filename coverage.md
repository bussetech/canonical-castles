---
layout: page
title: Coverage
permalink: /coverage/
description: "What has been surveyed, what has not, and which register would settle each open cell."
---

{% assign cells = site.data.coverage.cells %}
{% assign defs = site.data.definitions.definitions %}
{% assign registers = site.data.registers.registers %}

The failure this project was built to answer is a map that showed nine castles
in Saxony and let the reader assume that was Saxony. So coverage is claimed
per **(definition × jurisdiction)** cell, and every cell states which of four
things it is:

| State | Meaning |
|---|---|
| **complete** | Every structure the bounding register lists has a record here. The integer is real. |
| **partial** | Work has started. The count is a floor, not a total. |
| **surveyed-empty** | We looked, found none, and that is a finding. |
| **unexamined** | Not started — said out loud. |

An unexamined cell naming its register is a work order. One naming no register
is a research question.

## The grid

{% for d in defs %}{% assign mine = cells | where: "definition", d.id %}{% if mine.size > 0 %}
### {{ d.label }}

<div style="overflow-x:auto">
<table>
  <thead><tr><th>Where</th><th>State</th><th>Held</th><th>Population</th><th>Would be settled by</th></tr></thead>
  <tbody>
  {%- for c in mine %}
    <tr>
      <td><strong>{{ c.jurisdiction }}</strong></td>
      <td>{{ c.state }}</td>
      <td>{{ c.records_held }}</td>
      <td>{% if c.register_count %}{{ c.register_count }}{% else %}—{% endif %}</td>
      <td>{% if c.settled_by and c.settled_by.size > 0 %}{% for r in c.settled_by %}{% assign reg = registers | where: "id", r | first %}{{ reg.name }}{% unless forloop.last %}, {% endunless %}{% endfor %}{% else %}<em>nothing currently could</em>{% endif %}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
</div>

{% for c in mine %}**{{ c.jurisdiction }}** — {{ c.note }}

{% endfor %}
{% endif %}{% endfor %}

## Why some cells will never close

Three of the six bands are **open**: no register bounds them and none could. A
coverage cell for an open band carries no population figure at all — and that is
enforced in CI, not merely intended. A cell that tried to publish one would fail
the build.

The `—` in a population column is doing real work. It means *no honest number
exists*, which is different from *we have not looked yet*.

## The blocked cells are the interesting ones

Four cells are blocked rather than merely unstarted, and each is blocked for a
different structural reason:

- **England** — the National Heritage List's bulk schema has no type field. 379,680 listed buildings, and castles cannot be filtered out of them.
- **Scotland** — "castle" is not a category; the scheduled-monument class field has exactly one distinct value across every record. The record side is behind a WAF.
- **Saxony** — the state register classifies by *Denkmalart* with no fortification category, splits archaeology to a different agency, and is licensed CC BY-NC-ND. Not open data.
- **Spain** — uncountable by law: castles are protected automatically under a 1949 decree, so the protected class is open-ended by construction.

Northern Ireland is a fifth case and the sharpest. Its register *does* have a
castle type, and querying it returns **4**. Northern Ireland obviously has more
than four castles — they are filed under FORTIFICATION (353) and MOTTE (48). Of
61 records mentioning a tower house, exactly one carries the type `TOWER HOUSE`.
Anyone building a castle dataset by filtering national registers on a castle
field would publish 4 and never notice.

That cell's population is recorded as `—`, not 4.
