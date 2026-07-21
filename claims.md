---
layout: page
title: Claims
permalink: /claims/
description: "The castle numbers people repeat, graded by how well they are sourced."
---

{% assign claims = site.data.claims.claims %}

Records answer "is this a castle?". This page answers a different and often more
useful question: **where did that number come from?**

The grade is about *method*, not plausibility. A folkloric number can be roughly
right and an official one can be misread. The point is whether anyone can check
it.

| Grade | Meaning |
|---|---|
| **official** | A named body's own published figure |
| **scholarly** | Named author, disclosed method, datable publication |
| **derived** | This project re-ran a reproducible query and recorded it |
| **circulating** | Widely repeated, plausible origin, unconfirmed |
| **folklore** | No traceable source at all |

## The signature

Laid side by side, the reliable and the unreliable claims have opposite shapes,
and the tell is reusable:

- Every **citable** figure here has a named author or operator, a datable publication, and a disclosed underlying database.
- Every **folkloric** one is a round number with no author, circulating in several magnitudes at once.

"France has 45,000 châteaux" appears as 20,000, 30,000, 40,000 and 45,000
*simultaneously* rather than evolving from a datable original. That is the
signature of a meme, not a statistic.

## The ledger

{% for c in claims %}
### {{ c.claim }}

**{{ c.grade | upcase }}**{% if c.value %} · asserted value **{{ c.value }}**{% elsif c.value_range %} · asserted range **{{ c.value_range[0] }}–{{ c.value_range[1] }}**{% endif %} · {{ c.jurisdiction }}{% if c.definition %} · band: [{{ c.definition | replace: "_", " " }}](/definitions/{{ c.definition  }}/){% endif %}

{{ c.assessment }}

{% if c.sources %}**Sources**
{% for s in c.sources %}
- [{{ s.title | default: s.url }}]({{ s.url }}){% if s.publisher %} — {{ s.publisher }}{% endif %}{% if s.date %}, {{ s.date }}{% endif %}{% if s.note %}<br><em>{{ s.note }}</em>{% endif %}
{%- endfor %}
{% endif %}

---
{% endfor %}

## Two entries that are absences

`gb-eng-castle-count` and `es-castles-uncountable` record that we *cannot* state
a number, and why. England has an openly licensed register of 400,000 entries
whose bulk schema contains no type field at all. Spain protects all castles by a
1949 decree operating automatically, so no enumerated list is derivable even in
principle — the country is uncountable by law rather than by neglect.

An unanswered question with its blocker named is worth more than a borrowed
number. Both entries exist so the gap is visible rather than silent.

## One entry where we disagree with ourselves

The German 20,000–25,000 range was read at source in one research pass and could
not be verified in a second. Under `signal > canon` the conflict stays visible:
it is graded *circulating* and says so in its own assessment, rather than being
quietly promoted to a fact or quietly dropped.
