---
layout: page
title: Castles
permalink: /castles/
description: "Every record, with its verdict against each of the six definitions."
---

{% assign recs = site.data.sites | sort %}
{% assign defs = site.data.definitions.definitions %}

{{ recs.size }} records. Each carries a verdict against every
[definition](/definitions/) — **y** yes, **n** no, **?** contested, blank
unassessed. Blank means no source consulted so far speaks to that band; it is
not a quiet no.

A **†** marks a verdict transcribed in bulk from a register's own typology
rather than assessed against the band's criterion. 104 of these rows are the
Cadw import that [closed the Welsh cell](/coverage/) — real register entries at
`confidence: low`, counted separately from assessed verdicts everywhere on this
site. They are here because a closed cell is worth having, not because anyone
has yet decided whether they meet the criterion.

<div style="overflow-x:auto">
<table>
  <thead>
    <tr>
      <th>Structure</th>
      <th>Where</th>
      {%- for d in defs %}
      <th title="{{ d.summary }}">{{ d.label }}</th>
      {%- endfor %}
    </tr>
  </thead>
  <tbody>
    {%- for pair in recs %}{% assign r = pair[1] %}
    <tr>
      <td><a href="/castles/{{ r.id }}/">{{ r.name }}</a>{% if r.disputed %} <abbr title="Sources disagree about at least one verdict">※</abbr>{% endif %}</td>
      <td>{{ r.location.country }}{% if r.location.region %} · {{ r.location.region }}{% endif %}</td>
      {%- for d in defs %}{% assign m = r.definitions_met[d.id] %}
      <td>{% if m.verdict == "yes" %}<strong>y</strong>{% elsif m.verdict == "no" %}n{% elsif m.verdict == "contested" %}?{% endif %}{% if m.assessment == "register-derived" %}<abbr title="Register-derived: transcribed from the register's typology, not assessed against the criterion">†</abbr>{% endif %}</td>
      {%- endfor %}
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

※ marks a record where sources disagree about at least one verdict. The
disagreement is recorded on the record page rather than resolved.

## How to read this table

The columns are the point. A row of mixed verdicts is not a data-quality
problem — it is what a castle actually looks like when you stop forcing a
single answer.

- **[Neuschwanstein](/castles/de-schwangau-neuschwanstein/)** fails every scholarly band and is probably the most famous castle on Earth.
- **[Sham Castle](/castles/gb-bath-sham-castle/)** is a wall with nothing behind it, and everybody calls it a castle.
- **[Neuf-Brisach](/castles/fr-haut-rhin-neuf-brisach/)** is overwhelming fortification and zero castle — one yes, five nos.
- **[The North Carolina State Capitol](/castles/us-nc-raleigh-state-capitol/)** scores no on all six. It is in this dataset *because* it appears in another one.

That last case is worth dwelling on. A dataset with a single castle flag can
only include or omit. This one can assess something, reject it, and show its
reasoning — which means a false positive becomes a record rather than a
silent absence.

## Coverage

One cell is now [closed](/coverage/): every scheduled monument Cadw classes
`SiteType: Castle` in Wales — all 104 — has a record here. That is the narrowest
possible reading of "complete", and the coverage grid states exactly what it
does and does not mean.

Everything else is a floor. The [coverage grid](/coverage/) says so cell by cell,
including which register would close each one. Ireland's `fortified_residence`
cell has 4,552 waiting in it, and its `enclosure_fortification` cell has 31,431.
