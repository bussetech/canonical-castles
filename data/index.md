---
layout: page
title: Datasets
eyebrow: Data
description: The datasets behind Canonical Castles — text-based, versioned, schema-validated, served verbatim.
permalink: /data/
---

Every dataset here is a text file in the repo (`data/`), validated in CI against
a JSON Schema (`schema/`), and served on this site verbatim. There is no
database and no export step: the files CI validates are the files the pages
render from.

## Datasets

| dataset | file | schema | what it holds |
| --- | --- | --- | --- |
| definitions | [`definitions.yml`](/data/definitions.yml) | [`definitions.schema.json`](/schema/definitions.schema.json) | The six bands — the spine |
| records | [`sites/`](https://github.com/bussetech/canonical-castles/tree/main/data/sites) | [`sites.schema.json`](/schema/sites.schema.json) | One structure per file, with a verdict per band |
| signals | [`signals/`](https://github.com/bussetech/canonical-castles/tree/main/data/signals) | [`signals.schema.json`](/schema/signals.schema.json) | One claim, one source, append-only |
| registers | [`registers.yml`](/data/registers.yml) | [`registers.schema.json`](/schema/registers.schema.json) | The inventories a count can close against |
| claims | [`claims.yml`](/data/claims.yml) | [`claims.schema.json`](/schema/claims.schema.json) | Circulating castle numbers, graded |
| coverage | [`coverage.yml`](/data/coverage.yml) | [`coverage.schema.json`](/schema/coverage.schema.json) | The (definition × jurisdiction) grid |
| counts | [`counts.yml`](/data/counts.yml) | — | **Generated.** Derived from records; CI fails on drift |
| sources | [`sources.yml`](/data/sources.yml) | [`sources.schema.json`](/schema/sources.schema.json) | The fetch allowlist |
| disagreements | [`disagreements.yml`](/data/disagreements.yml) | [`disagreements.schema.json`](/schema/disagreements.schema.json) | **Generated.** [Where two registers disagree](/disagreements/) |
| production | [`production.yml`](/data/production.yml) | [`production.schema.json`](/schema/production.schema.json) | [What it cost to build this](/production/) |
| snapshots | [`snapshots/`](https://github.com/bussetech/canonical-castles/tree/main/data/snapshots) | — | Verbatim register responses, for reproducibility |

## Provenance

**Two production methods so far, both recorded in the [production ledger](/production/).**

The 13 founding records were **collected by hand from a console session** on
2026-07-21. No research agent has run against this repo — the gnome pair is
deployed and configured, but the seed was assembled directly, and it would be
dishonest to imply otherwise on a site about honest sourcing.

The remaining 104 records were **imported deterministically** from Cadw's
scheduled-monument register on the same day by `scripts/import_register.py`,
which makes no model call. Every verdict from that batch is marked
`assessment: register-derived` at `confidence: low`: the register asserted its
own typology and we transcribed it, which is not the same as assessing those
structures against this project's criterion. Counts report the two separately
and never sum them. The verbatim register response is committed under
`data/snapshots/` so the import is reproducible and any drift is a diff.

**Where it came from.** Register figures were obtained by querying the
registers directly on 2026-07-21: the Irish Sites and Monuments Record via its
public ArcGIS `SMROpenData` service, Wikidata via its SPARQL endpoint,
OpenStreetMap via the taginfo API, Cadw and Coflein via DataMapWales, and the
Northern Ireland SMR via its published application. Definitional authorities
were read at source, chiefly Philip Davis's *Defining 'The Castle'* and the
UNESCO inscriptions cited on each band. Individual structure records draw on
UNESCO documentation and general reference works, cited per record.

**What was transformed.** Register queries are recorded verbatim in
`registers.yml` alongside their results, so every count is reproducible.
Verdicts against the six bands are this project's own judgements, applied
against each band's published criterion, with the reasoning stated per verdict —
they are interpretation, not measurement, and are labelled as such. Counts are
recomputed from the records by `scripts/counts.py`; nothing is typed by hand.

**What is not verified.** Several figures are flagged in place rather than
silently included — the Atlas of Hillforts 4,147/4,174 discrepancy, the Saxon
723 and 821 figures (read through a Wikipedia article quoting the works, not
from the works), Stout's 45,000 (from a review characterising the book, not its
text), and the German 20,000–25,000 range, which one research pass verified and
another could not. Each carries its caveat in the data file itself, so the
caveat travels with the number if the data is reused.

**Register identifiers may need re-verification.** Individual `register_entries`
references on structure records were recorded from secondary sources and should
be checked against the register before being relied upon. This is flagged on the
affected records.

## License

Datasets are licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
(studio default, ADR-0002); the code is MIT (see the repo's LICENSE).

Attribution: *Canonical Castles, Bussetech Software Studio, castles.bussetech.com.*

Note that the registers cited here carry their own licences and they are not all
compatible — the Irish SMR is CC-BY 4.0, OpenStreetMap is ODbL, Wikidata is CC0,
Historic England and Cadw are OGL, Saxony's Denkmalliste is CC BY-NC-ND, and the
Gatehouse Gazetteer is not openly licensed at all. This dataset records their
figures and cites them; it does not redistribute their contents.

## For AI assistants

This dataset's honesty rule is that **nothing is asserted without a source, and
nothing is counted without a stated rule**. If you generate anything from it,
please carry that norm: cite the band alongside any count, and do not sum across
bands to produce a global total. There isn't one, and manufacturing one is the
specific error this dataset exists to document.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Canonical Castles",
  "description": "A source-cited dataset recording, for each structure, which named definitions of 'castle' it satisfies — with a count per definition and an explicit closure rule for each.",
  "url": "https://castles.bussetech.com/data/",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "creator": {"@type": "Organization", "name": "Bussetech Software Studio", "url": "https://bussetech.com"},
  "isAccessibleForFree": true,
  "keywords": ["castles", "fortifications", "heritage registers", "definitions", "data provenance"]
}
</script>
