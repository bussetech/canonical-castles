---
layout: page
title: Figures
permalink: /figures/
description: "The shape of the dataset — what it holds, how well evidenced it is, and how much of the knowable population that represents."
---

{% include viz/styles.html %}
{% assign counts = site.data.counts %}
{% assign defs = site.data.definitions.definitions %}
{% assign cells = site.data.coverage.cells %}
{% assign dis = site.data.disagreements.disagreements %}
{% assign claims = site.data.claims.claims %}

**There is no headline number on this page, and its absence is the point.**

A dashboard usually opens with one big figure. This dataset's whole argument is
that the figure everybody wants — *how many castles are there* — does not exist,
so putting one at the top would contradict every other page on the site. What
follows is the shape of the data instead: what it holds, how well evidenced it
is, and how small a fraction of the knowable population that represents.

Every figure prints its numbers. The bars are there to let you compare along a
straight edge; the text is what carries the meaning.

---

{% capture t1 %}Six answers, not one{% endcapture %}{% capture s1 %}Records held per definition band. One band dwarfs the other five — not because castles cluster there, but because it is the only band a register has been imported into.{% endcapture %}
{% include viz/figure.html title=t1 sub=s1 %}

<ul class="viz-legend">
  <li><span class="viz-swatch viz-swatch--ink"></span> records held</li>
</ul>

{% assign band_max = 0 %}
{% for b in counts.bands %}
  {% assign h = b.held %}
  {% assign t = h.assessed.yes | plus: h.assessed.contested | plus: h.register_derived.yes | plus: h.register_derived.contested %}
  {% if t > band_max %}{% assign band_max = t %}{% endif %}
{% endfor %}

{% for b in counts.bands %}
  {% assign d = defs | where: "id", b.definition | first %}
  {% assign h = b.held %}
  {% assign t = h.assessed.yes | plus: h.assessed.contested | plus: h.register_derived.yes | plus: h.register_derived.contested %}
  {% include viz/bar-row.html label=d.label sub=b.closure value=t max=band_max %}
{% endfor %}

{% capture note1 %}Bars share one scale, so the five short ones are honestly short. The three <strong>enumerable</strong> bands can in principle be counted to completion against a named register; the three <strong>open</strong> bands cannot, and never will — popular usage has no register and no edges. Adding records to an open band increases its size and never its completeness.{% endcapture %}
{% include viz/figure.html close=true note=note1 %}

---

{% capture t2 %}What the holdings actually rest on{% endcapture %}{% capture s2 %}The same records, split by whether anyone applied the band criterion to the structure — or whether a register's own typology was transcribed in bulk and nobody checked it.{% endcapture %}
{% include viz/figure.html title=t2 sub=s2 %}

<ul class="viz-legend">
  <li><span class="viz-swatch viz-swatch--ink"></span> assessed — a person applied the criterion</li>
  <li><span class="viz-swatch viz-swatch--muted"></span> register-derived — transcribed, unchecked</li>
</ul>

{% for band in counts.bands %}
  {% assign d = defs | where: "id", band.definition | first %}
  {% assign h = band.held %}
  {% assign n_assessed = h.assessed.yes | plus: h.assessed.contested %}
  {% assign n_derived = h.register_derived.yes | plus: h.register_derived.contested %}
  {% assign n_total = n_assessed | plus: n_derived %}
  {% if n_total > 0 %}
    {% include viz/stacked-row.html label=d.label sub=band.closure a=n_assessed b=n_derived %}
  {% endif %}
{% endfor %}

{% capture note2 %}Read this figure against the one above it, not on its own. Five bands are almost entirely assessed — but they hold two to ten records each, so the proportion is flattering and the magnitude is not. The sixth holds 4,659 records of which 4,650 are unchecked transcriptions. <strong>Proportion and magnitude tell opposite stories here, which is exactly why both figures exist.</strong>{% endcapture %}
{% include viz/figure.html close=true note=note2 %}

---

{% capture t3 %}How much of the world this represents{% endcapture %}{% capture s3 %}Each track is the population a register says exists. The filled portion is what this dataset holds. Only cells with a bounding register appear — an open band has no denominator, so it cannot appear here at all.{% endcapture %}
{% include viz/figure.html title=t3 sub=s3 %}

<ul class="viz-legend">
  <li><span class="viz-swatch viz-swatch--ink"></span> held</li>
  <li><span class="viz-swatch viz-swatch--track"></span> the register's population</li>
</ul>

{% for c in cells %}
  {% if c.register_count %}
    {% assign d = defs | where: "id", c.definition | first %}
    {% capture sub %}{{ d.label }} · {{ c.jurisdiction }}{% endcapture %}
    {% include viz/bullet.html label=c.jurisdiction sub=d.label value=c.records_held reference=c.register_count state=c.state %}
  {% endif %}
{% endfor %}

{% capture note3 %}Two cells are full because they were closed deliberately: every monument Cadw classes <code>SiteType: Castle</code>, and every record the Irish survey holds under <code>MONUMENT_CLASS LIKE 'Castle%'</code>. The Irish enclosure cell is the extreme case — one record against 31,431 — and it is <a href='/coverage/'>deliberately not being filled</a>. A bar too small to see is the correct rendering of that number.{% endcapture %}
{% include viz/figure.html close=true note=note3 %}

---

{% capture t4 %}Coverage, honestly stated{% endcapture %}{% capture s4 %}Twenty cells, one per definition band and jurisdiction. An unexamined cell is a published admission; three of them can never be closed by anyone.{% endcapture %}
{% include viz/figure.html title=t4 sub=s4 %}

{% assign complete = cells | where: "state", "complete" | size %}
{% assign partial = cells | where: "state", "partial" | size %}
{% assign unexamined = cells | where: "state", "unexamined" | size %}

{% include viz/stacked-row.html label="All cells" sub="complete · partial · unexamined" a=complete b=partial c=unexamined %}

{% capture note4 %}Of the eight unexamined cells, <strong>three name no register that could settle them</strong>: Spain is uncountable by law (castles are protected automatically, so the class is open-ended by construction), Saxony's register carries no fortification category and is not open data, and England's national list has no type field at all. Those are research questions, not work orders — and they are stated rather than left as gaps.{% endcapture %}
{% include viz/figure.html close=true note=note4 %}

---

{% capture t5 %}Where two registers disagree{% endcapture %}{% capture s5 %}680 monuments classified differently by two registers joined on a shared identifier. The kind of disagreement matters more than the count.{% endcapture %}
{% include viz/figure.html title=t5 sub=s5 %}

<ul class="viz-legend">
  <li><span class="viz-swatch viz-swatch--ink"></span> granularity — same band, different precision</li>
  <li><span class="viz-swatch viz-swatch--muted"></span> band-conflict — a real dispute</li>
  <li><span class="viz-swatch viz-swatch--faint"></span> category-error — someone is wrong</li>
</ul>

{% assign gran = dis | where: "kind", "granularity" | size %}
{% assign bandc = dis | where: "kind", "band-conflict" | size %}
{% assign cat = dis | where: "kind", "category-error" | size %}

{% include viz/stacked-row.html label="Cadw & Irish SMR vs Wikidata" sub="granularity · band-conflict · category-error" a=gran b=bandc c=cat %}

{% capture dis_note %}Most apparent disagreement is <strong>granularity</strong> — one register distinguishing a motte from a ringwork where the other says &ldquo;castle&rdquo;. That is two registers agreeing about the world and describing it at different resolutions, and reporting it as conflict would overstate the discord badly. Only {{ cat }} of {{ dis.size }} are cases where somebody is simply wrong. <a href="/disagreements/">Read the ledger.</a>{% endcapture %}
{% include viz/figure.html close=true note=dis_note %}

---

{% capture t6 %}How well sourced the numbers people repeat are{% endcapture %}{% capture s6 %}Castle counts in circulation, graded by method rather than by plausibility. A folkloric number can be roughly right; the grade is about whether anyone can check it.{% endcapture %}
{% include viz/figure.html title=t6 sub=s6 %}

{% assign grades = "official,scholarly,derived,circulating,folklore" | split: "," %}
{% assign claim_max = 0 %}
{% for g in grades %}
  {% assign n = claims | where: "grade", g | size %}
  {% if n > claim_max %}{% assign claim_max = n %}{% endif %}
{% endfor %}
{% for g in grades %}
  {% assign n = claims | where: "grade", g | size %}
  {% assign tone = "" %}
  {% if g == "circulating" %}{% assign tone = "muted" %}{% endif %}
  {% if g == "folklore" %}{% assign tone = "muted" %}{% endif %}
  {% include viz/bar-row.html label=g value=n max=claim_max tone=tone %}
{% endfor %}

{% capture note5 %}Ordered best-attested first. The reliable and the unreliable have opposite signatures: every citable figure here has a named author, a datable publication and a disclosed database, while every folkloric one is a round number with no author circulating in several magnitudes at once. &ldquo;France has 45,000 châteaux&rdquo; appears as 20,000, 30,000, 40,000 and 45,000 <em>simultaneously</em>. <a href='/claims/'>Read the ledger.</a>{% endcapture %}
{% include viz/figure.html close=true note=note5 %}

---

## The numbers, as a table

Every figure above renders from these values. If a bar and a number ever
disagree, the number is right — and CI should have caught it, because
`scripts/counts.py` regenerates them from the records and the build fails on drift.

| measure | value |
|---|---|
| records | {{ site.data.sites.size }} |
| signals | {{ site.data.signals.size }} |
| definition bands | {{ defs.size }} — {{ counts.bands | where: "closure", "enumerable" | size }} enumerable, {{ counts.bands | where: "closure", "open" | size }} open |
| registers catalogued | {{ site.data.registers.registers.size }} |
| coverage cells | {{ cells.size }} — {{ complete }} complete, {{ partial }} partial, {{ unexamined }} unexamined |
| cross-register disagreements | {{ dis.size }} |
| count claims graded | {{ claims.size }} |

## A note on how these are drawn

There is no chart library on this page, no JavaScript, and no colour that is not
already a theme token. Every mark is a rectangle sized by a percentage, and the
whole page works with scripting disabled — the numbers are in the markup, not in
a tooltip.

The near-monochrome palette is a design decision twice over. The studio theme's
law is that [colour is wayfinding only](https://bussetech.com), so a chart here
does not get a categorical palette to play with. It also happens that encoding
classes by **lightness** rather than hue survives every form of colour blindness
by construction — the two readable steps used here measure ΔE 31 apart, and the
third appears only in figures where every segment is labelled in text.

The forms follow Stephen Few: bullet graphs for a measure against a reference,
one shared scale per figure so bars compare along a straight edge, no gridlines,
no gradients, no chart borders, and no number printed on a mark where the value
column already carries it.
