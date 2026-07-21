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
