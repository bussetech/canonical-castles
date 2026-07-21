---
layout: page
title: Production
permalink: /production/
description: "What it cost to build this dataset — recorded as the work happened, with unmeasured distinguished from zero."
---

{% assign batches = site.data.production.batches %}
{% assign counts = site.data.counts %}

A dataset with opinions about numbers that arrive without a method owes the same
scrutiny to its own. So this page records what it cost to build what you are
reading, batch by batch, written down as the work happened rather than
reconstructed afterwards.

**The rule this file is built around: `null` means NOT MEASURED. It never means
zero.** A genuine zero — a deterministic script that makes no model call — is
written as `0` with an explicit basis for how that was verified. An unmeasured
cost is never written as a figure and least of all as `0`, and CI rejects a
batch that tries. That guard exists because a sibling studio tool once estimated
every agent run at $0 and duly reported a budget that could never be breached.

## Batches

<div style="overflow-x:auto">
<table>
  <thead>
    <tr><th>Batch</th><th>Method</th><th>Produced</th><th>Model cost</th><th>Cells closed</th></tr>
  </thead>
  <tbody>
  {%- for b in batches %}
    <tr>
      <td><code>{{ b.id }}</code><br><small>{{ b.date }}</small></td>
      <td><strong>{{ b.method }}</strong></td>
      <td>{% for kv in b.produced %}{{ kv[1] }} {{ kv[0] }}{% unless forloop.last %}, {% endunless %}{% endfor %}</td>
      <td>{% if b.cost.measured %}<strong>${{ b.cost.model_usd }}</strong><br><small>measured</small>{% else %}—<br><small>not measured</small>{% endif %}</td>
      <td>{% if b.cells_closed and b.cells_closed.size > 0 %}{% for c in b.cells_closed %}<code>{{ c }}</code>{% endfor %}{% else %}none{% endif %}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
</div>

{% for b in batches %}
### {{ b.id }}

{{ b.note }}

**Cost basis.** {{ b.cost.basis }}

{% endfor %}

## What this is for

The comparison worth making is **cost per artefact by method**, and it is stark
enough that it changes how the rest of the dataset should be built.

The founding batch produced 13 records by hand, in an interactive session, and
its cost is unmeasured — there is no per-session token accounting to read after
the fact, so any figure would be invented. The Cadw import produced 104 records
and 104 signals for a measured **$0**, because a register row is a mechanical
transform and mechanical transforms are code, not agents.

That is the argument for the whole import pipeline. Ireland's two open cells
hold 4,552 and 31,431 entries between them. Pushing 36,000 records through a
language model would cost more than the studio's entire monthly budget to
produce something a script produces for nothing — and would produce it *worse*,
because a model asked to transcribe a register row will occasionally decide to
be helpful about it.

## What the numbers here cannot tell you

Three honest gaps, stated rather than papered over:

- **The expensive batch is the one with no number.** Console authoring is by far
  the most costly work per artefact and it is the one this ledger cannot price.
  The studio's cost ledger journals agent runs by `run_uid`; an interactive
  session is invisible to it. `run_ref` is null for that batch because there is
  genuinely no run to point at.
- **Actions minutes are not yet attributed.** The import consumes CI time and
  that time is real. It is recorded as `null` rather than `0` — reconcilable
  later against the studio's monthly Actions usage report via the workflow run
  id, which is exactly why `run_ref` exists as a field.
- **Cost is not value.** The $0 batch produced 104 register-derived verdicts at
  `confidence: low`. The unmeasured batch produced the six definition bands, the
  claims ledger, and every contested verdict on the site. Cheap and valuable are
  different axes, and the cheap batch is not the one doing the intellectual work.

The raw ledger is [`production.yml`](/data/production.yml); its schema is
[`production.schema.json`](/schema/production.schema.json).
