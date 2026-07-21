---
layout: post
title: "Founded: how many castles are there?"
description: "A dataset that answers per definition, not in general — because the question has no single number, and the reason is not missing data."
---

A [Hacker News thread](https://news.ycombinator.com/item?id=48994178) took apart
a map of "the world's 2,400 castles" today. The coverage complaints were loud —
Saxony showing nine structures against a literature that counts hundreds, France
showing about a hundred against a folkloric forty-five thousand. But the sharper
problem was quieter: the map published **a single integer for a contested term**.

Canonical Castles is the answer we thought that deserved.

It never records that something *is* a castle. It records a verdict against each
of [six named definitions](/definitions/) — fortified residence, enclosure
fortification, state fortification, palatial seat, revival and folly, and
popularly a castle — each with a cited authority, an explicit criterion, and its
own **closure rule**. Three of those bands can in principle be counted to
completion against national registers. Three cannot, and never will. The site
says which is which everywhere it prints a number, and it publishes
[a count per band](/counts/) rather than a total across them.

Ireland settles the argument on its own. The state's Sites and Monuments Record
answers "how many castles?" with **129**, **4,552** or **31,431** — same
database, same day, depending only on which class filter you accept.

Three things we found while building it:

- Only **19.5%** of OpenStreetMap objects carrying a `castle_type` are tagged `defensive`. The rest are stately homes, manors and palaces.
- **"France has 45,000 châteaux" is folklore.** No primary source, no stated method, and it circulates as 20,000, 30,000, 40,000 and 45,000 *simultaneously* — the signature of a meme, not a statistic. The register supports about 6,286, and even that depends on which of four defensible tokenisations you use.
- Northern Ireland's register has a castle type. Querying it returns **4**. Its castles are filed under FORTIFICATION.

The seed dataset is thirteen records, collected by hand from a console session —
no research agent has run against this repo yet, and the
[provenance page](/data/) says so rather than implying otherwise. Thirteen
records is a seed, not a survey, and the [coverage grid](/coverage/) states cell
by cell what has been examined, what has not, and which register would close
each open one.

A [Bussetech Software Studio](https://bussetech.com) project.
