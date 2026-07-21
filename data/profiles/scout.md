# canonical-castles scout profile — dataset configuration for gn_info_scout

(Consumed as the `dataset_profile` input. This file defines WHAT the dataset
catalogs; the gnome's prompt defines HOW. The signal field skeleton is the
frozen info-archetype contract — platform `docs/archetype-contracts.md` — and
this profile does not get to rename any part of it.)

## The dataset

Structures that someone, somewhere, calls a castle — and the evidence for and
against each of six named definitions.

The **subject-of-record is one physical structure on one site**. A castle
rebuilt as a palace on the same footprint is one subject with its phases in
`notes:`; two castles in one town are two subjects. A serial heritage
inscription covering twelve forts is twelve subjects, not one.

`site_hint` format for unknown subjects:
`"<name as reported> — <locality>, <country>"`.

## Attribute vocabulary

`name`, `location`, `tradition`, `built_from`, `built_to`, `built_period`,
`condition`, `register_entry`, `designation`, and — the ones that matter most
here — `definition.<band>` and `naming`.

- `definition.fortified_residence`, `definition.enclosure_fortification`,
  `definition.state_fortification`, `definition.palatial_seat`,
  `definition.revival_folly`, `definition.popular_castle` — a source's position
  on whether the structure meets that band, in the source's own words.
- `naming` — what a source *calls* the structure. This is evidence, not
  decoration: the popular_castle band is a claim about usage, so a national
  tourism body calling something a castle is a real signal about that band.

## What is signal-worthy

**The most valuable signal in this dataset is a source disagreeing with another
source about what something is.** Two scholars differing on whether a Hospitaller
castle counts as a lordly residence is worth more than ten sources agreeing on
its construction date.

Also signal-worthy: register entries and their designation classes (they are what
make counts closable), construction and destruction dates, condition, and any
*count claim* about a population of castles.

Not signal-worthy: visitor numbers, ticket prices, opening hours, architectural
appreciation, legends, and anything about the building's owner today.

**Never resolve a band verdict.** The scout records that a source takes a
position; the records gnome resolves what the dataset holds. A signal saying
"Historic England classes this as a fortified manor house" is correct. A signal
saying "therefore fortified_residence: yes" is out of scope.

**Cap: the most informative ~8 signals per structure.**

## Confidence refinement

Primary sources for this domain, in order: the national heritage register itself
(a designation class is close to a fact); statutory instruments and official
inscriptions (UNESCO, national decrees); peer-reviewed scholarship and standard
reference works; the structure's own operator; general reference works; travel
and tourism copy.

Tourism copy is `low` for anything factual — but it is a legitimate `medium`
source for the `popular_castle` band specifically, because there the question
*is* what people call the thing. Record it as evidence of usage, never as
evidence of fabric.

## The trap this domain sets

Castle counts circulate as round numbers with no author. If a source asserts a
population figure ("France has 45,000 châteaux"), capture it as a signal with
`attribute: count_claim` and the source's exact wording — **do not repair it,
average it against another figure, or drop it for being implausible.** Those
claims are studied on this site, not filtered out. If a source states its
method, that method belongs in `notes:`; if it states none, say so, because the
absence is the finding.
