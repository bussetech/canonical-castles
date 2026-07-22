# canonical-castles records profile — dataset configuration for gn_info_records

(Consumed as the `dataset_profile` input. This file defines the record schema
surface and the id rule; the gnome's prompt defines the resolution method.
Record schema of record: `schema/sites.schema.json`. The `data/sites/` path is
the frozen archetype location even though this project's subjects are
structures, not sites.)

## The subject

One record per physical structure on one site. Cluster signals on name,
locality, country, and register reference. A register reference is the strongest
clustering key available — two sources naming the same NHLE or SMR entry are
about the same structure whatever they call it.

## Record schema fields (only these)

id, name, name_local, also_known_as, tradition,
location{country, region, county, locality, lat, lon},
built{from, to, period}, condition, **definitions_met{<band>: {verdict, basis}}**,
register_entries[{register, ref, designation, url}], disputed, dispute_note,
first_seen, last_updated, confidence, sources[{url, title, publisher, date,
note}], signals, notes.

- `location.country` is ISO 3166-1 alpha-2. Scotland and Wales are `GB` with
  `region: Scotland` / `region: Wales` — never `SCT` as a country.
- `tradition` is orthogonal to the bands, deliberately. A Japanese *shiro* is not
  a lesser castle; it is a fortified lordly residence in a different tradition
  and takes the `fortified_residence` verdict on the same functional criterion as
  an Anglo-Norman keep. Never use `tradition` to soften a verdict.

## The core judgement: definitions_met

This is the whole dataset. For each band in `data/definitions.yml`, decide
`yes`, `no`, or `contested`, and write a `basis` that **engages that band's
criterion in its own terms**. "It's obviously a castle" is not a basis and CI
rejects a basis under twenty characters.

**Quote the verdict.** `verdict: yes` unquoted is the BOOLEAN true in YAML 1.1
and fails schema validation. Write `verdict: "yes"` and `verdict: "no"`. This is
the same class of trap as the archetype's all-dates-double-quoted rule, and it
was caught by the founding's own closing check rather than in review.

Three rules that are not negotiable:

1. **Omission means unassessed, never no.** If no consulted source speaks to a
   band, leave the band out. A dataset that silently converts ignorance into a
   negative is the failure mode this project exists to document.
2. **`contested` is a result, not a hedge.** Use it when competent sources
   genuinely disagree under that band's criterion — and then set `disputed: true`
   and write `dispute_note` explaining who is on each side. Do not use it to
   avoid deciding a clear case.
3. **Never let one band's verdict drive another's.** A structure can be `yes` on
   `palatial_seat` and `yes` on `popular_castle` and `no` on everything else;
   that is not an inconsistency, it is Neuschwanstein.

## Confidence and conflict

Record-level `confidence` is aggregate corroboration. When sources conflict on a
*fact* (a construction date), resolve to the highest-confidence claim and surface
the conflict in `notes:` — never average. When sources conflict on a *band
verdict*, that is `contested`, not a resolution problem.

## The id rule (deterministic; collision clause at the end)

Build `<country>-<place>-<name>`, lowercase, ASCII, hyphenated:

- `<country>` = ISO 3166-1 alpha-2, lowercased.
- `<place>` = the single most-specific administrative place the signals give, in
  strict precedence: locality → else county → else region. Use exactly one;
  never combine two. Omit where it would merely repeat the name.
- `<name>` = a slug of the distinctive proper name, dropping generic words
  ("castle", "schloss", "château", "fort", "the").
- **Collision clause:** if that id would name a *different* existing structure,
  append `-<county>`, then `-2`, `-3` — the sole allowed disambiguation.

## What this dataset keeps that others drop

- **Vanished structures.** A destroyed castle is a record with `condition:
  vanished`, not an omission.
- **All-no records.** A structure that fails every band is a real finding,
  especially when it appears in another castle dataset. Record it with reasons.
- **False positives from other datasets.** Being wrong somewhere else is a
  reason to have a record here, not a reason to omit one.


## Assessment mode — turning a register transcription into a verdict

The task above resolves SIGNALS into records. This section covers a second,
distinct job: reading a designation report for a structure this dataset already
holds, and replacing its `register-derived` verdict with `assessed` ones.

The input is one official document per structure — Cadw's full scheduled-monument
report, or an equivalent. It carries fabric, defensive features, period, and
often documentary history. That is the evidence. Nothing outside it may be used:
if the report does not support a verdict, the band is OMITTED, not guessed.

### Rules, in order of how often they matter

**1. Omit any band the report does not speak to.** This is the most common
correct outcome and the easiest to get wrong. A report describing masonry and a
ditch supports `fortified_residence`; it says nothing about whether the public
calls the place a castle. Omission means unassessed, which is a true statement.
Setting `no` because the report is silent is a false one.

**2. `popular_castle` needs usage evidence, not a name.** A register calling
something "X Castle" is one body's naming convention, not proof of popular
usage. Assess this band only where the report shows real public standing — a
World Heritage citation, a visitor operation, a monument everybody has heard of.
For an obscure earthwork, leave it unassessed. Being eager here inflates the one
band that has no register to check it against.

**3. Several bands can be `yes` at once, for different phases.** This is normal
and is what the band model is for. A castle later rebuilt as a country seat is
`fortified_residence: yes` AND `palatial_seat: yes`. The strongest evidence for
the second is defensive fabric being REMOVED for amenity — a curtain wall taken
down to improve a view, a tower demolished to build a residential range.

**4. `contested` when the report itself argues both ways.** Not when you are
unsure — when the evidence genuinely cuts both directions. If a designation says
a monument was built "not as a defensive structure" while describing a great
tower, a gatehouse and a walled court, that is contested, and the basis should
quote both halves. Set `disputed: true` and write `dispute_note`.

**5. The basis must engage the criterion in ITS terms.** Name the feature and
say which half of the test it satisfies: wall walks, parapets, flanking fire, a
gatehouse meant to be held, an identified lord. "It is clearly a castle" is not
a basis and CI rejects anything under 20 characters. Quote the report where it
states a definition of its own — those are the best sentences available.

**6. Refuse thin reports.** Some designation texts are placeholders — one of the
greatest castles in Wales carries the entire text "This description is in the
process of being updated." Under ~400 characters of substance, produce NO
verdicts for that structure and say so. A famous name is not evidence.

**7. Confidence is corroboration, not certainty.** One official report plus the
register is `medium`. Do not write `high` on a single source however emphatic it
is. Confidence and `assessment` are different axes: `assessment` says who applied
the criterion, `confidence` says how well evidenced it is.

### Worked example

Raglan is the reference case. Cadw states it was built "not as a defensive
structure, but as a fortress-palace" whose great tower "mimicked the keeps of
earlier medieval castles" as "the ultimate status symbol" — while describing a
Great Tower, a gatehouse, a closet tower and a walled court. The correct output
is `fortified_residence: contested` (quoting both halves in the basis),
`palatial_seat: yes` (the register's own word is "fortress-palace"),
`revival_folly: no` (15th century, within the defensive era — a SYMBOLIC castle
is not a SHAM one), `popular_castle: yes` (a major operated monument), and
`disputed: true` with a dispute_note naming both readings.

### Output

For each structure, emit only `definitions_met`, `confidence`, and — when
contested — `disputed` and `dispute_note`. Everything else on the record is
carried forward by deterministic code. Setting `assessment: assessed` on a band
transfers ownership of that record away from the importer permanently, so do it
only where the report actually supports the verdict.


## Writing a record back — three rules a metered run had to teach

These are not style preferences. Each one names a fault that reached committed
data, validated against the schema, and cost real money to discover.

**8. Never write a colon-space inside unquoted prose.** A `basis` reading
`revival_folly is no: a symbolic status statement` is not a string — `: ` starts
a YAML mapping, and the whole record fails to parse. Write the em dash instead:
`revival_folly is no — a symbolic status statement`. This is the same family as
the `verdict: yes` boolean trap: prose written into YAML meets YAML's
punctuation rules, and loses. If a colon genuinely belongs in the sentence,
quote the whole scalar.

**9. Return the WHOLE record, never just the part you changed.** A record came
back carrying its verdicts and nothing else — `name`, `location`, `built`,
`sources` all gone. It was well-formed YAML and it passed the schema, because
the damage was in what was *missing*. Assessing a structure's bands never
licenses deleting its name. When a batch is large or its evidence is long, the
temptation to emit a patch is strongest and the loss is hardest to see.

**10. If you did not assess it, do not rewrite it.** Structures appear in
context that are not yours to assess. Returning one unchanged-but-reformatted,
with `last_updated` bumped, makes an echo look exactly like an assessment in
every downstream count. Emit only the structures you actually assessed.

`scripts/check_gnome_output.py` enforces 9 and 10 by comparing each returned
record against the version it replaces. It cannot enforce 8 — a record that
fails to parse never reaches it.
