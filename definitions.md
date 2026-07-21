---
layout: page
title: Definitions
permalink: /definitions/
description: "The six definition bands — each with a named authority, an explicit criterion, and its own closure rule."
---

Six answers to "what is a castle?". Each is a real definition held by real
people; none is this site's preferred one. A structure takes a verdict against
each band separately, and each band publishes [its own count](/counts/).

The man best placed to settle the question declined to. Philip Davis built a
gazetteer of roughly six thousand fortified sites and concluded:

> In effect it is impossible to define 'the castle' since there is no one such
> thing. Much of the controversy in castle studies between militarists and
> revisionists lies in a befuddled use of examples of 'castles' of very
> different function.

These bands are not a better definition. They are the consequence of accepting
that one definition was always the wrong shape.

{% assign defs = site.data.definitions.definitions %}
{% for d in defs %}
## {{ d.label }} {#{{ d.id }}}

*{{ d.summary }}*

**Closure: {{ d.closure }}.** {{ d.closure_note }}

**Criterion.** {{ d.criterion }}

**Includes**
{% for i in d.includes %}
- {{ i }}
{%- endfor %}

**Excludes**
{% for e in d.excludes %}
- {{ e }}
{%- endfor %}

**Who defines it this way**
{% for a in d.authority %}
- {{ a.name }}{% if a.work %} — *{{ a.work }}*{% endif %} ([source]({{ a.url }})){% if a.kind == "project" %} — **this project's own band; no external authority**{% endif %}{% if a.quote %}<br>&ldquo;{{ a.quote }}&rdquo;{% endif %}
{%- endfor %}

{% if d.registers and d.registers.size > 0 %}**Bounded by**
{% for r in d.registers %}{% assign reg = site.data.registers.registers | where: "id", r | first %}[{{ reg.name }}](/data/#registers){% unless forloop.last %} · {% endunless %}{% endfor %}
{% endif %}

{% if d.note %}**Note.** {{ d.note }}{% endif %}

---
{% endfor %}

## What "closure" means

A band is **enumerable** when a named register bounds it — a finite, citable
list a person could in principle work through. Those bands can reach a real
integer, one jurisdiction at a time.

A band is **open** when nothing bounds it and nothing could. "Popularly a
castle" has no register and never will, because popular usage has no edges.
Those bands publish a distribution or a range with its assumptions visible,
never a fabricated total.

This distinction is enforced in the data, not just in the prose: a coverage
cell for an open band that carries a world-population figure fails CI.

## Changing a band

Bands are the dataset's contract with its readers — moving one silently moves
every number on the site. Amendments go through a decision-request issue and a
PR, never a data edit.

Two are known to be unfinished. **Revival / folly** currently holds both what
Davis calls a *symbolic* castle (built in castle form to assert status) and a
*sham* castle (built as scenery); he insists these are not the same and he is
probably right. And the bands are a European instrument throughout — applied to
[Chittorgarh](/castles/in-rajasthan-chittorgarh-fort/) they return two contested
verdicts rather than knowledge, because the European lord-versus-state axis does
not transfer to Rajput polity, which classified forts by *terrain* instead.
That is a limitation of the bands, not of the fort.
