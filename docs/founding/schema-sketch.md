# canonical-castles — data design

> **Historical artefact.** This is `gn_project_founder`'s founding proposal as
> filed (canonical-castles#5, 2026-07-21), preserved unedited. The build
> extended it the same day — see [as-built-delta.md](as-built-delta.md) for
> where the two differ. Do not read this as current documentation.

This is an **info archetype** deployment: the signal emission shape and the
`data/sites/` record path are **given, not designed** (archetype contracts,
ADR-0045). The founding transcribes those verbatim and designs only the
profile-owned surfaces plus the domain's extra reference datasets.

## Datasets

| dataset | file(s) | format | emitted by |
|---|---|---|---|
| signals | `data/signals/sig-*.yml` | YAML | `gn_info_scout` (frozen shape) |
| structures | `data/sites/<id>.yml` | YAML | `gn_info_records` (frozen path; profile fields) |
| definitions | `data/definitions.yml` | YAML | authored editorial (reference) |
| coverage | `data/coverage.yml` | YAML | derived by code + authored open-band ranges |
| sources | `data/sources.yml` | YAML | authored (founding) |

---

## 1. signals — `data/signals/sig-*.yml` (FROZEN — transcribed verbatim)

`schema/signals.schema.json` must validate **exactly this shape**, not a
domain-idealized one.

| field | type | constraints |
|---|---|---|
| `id` | string | REQUIRED; equals filename stem; `^sig-\d{8}-[a-z0-9-]+$` |
| `site_id` | `["string","null"]` | REQUIRED; **type both** (scout emits `null` + `site_hint` for a newly-discovered structure) |
| `site_hint` | string | present only when `site_id` is null; OMIT when set |
| `attribute` | string | REQUIRED; from the attribute vocabulary (profile) |
| `value` | string | REQUIRED; the claim, raw |
| `source_url` | string (uri) | REQUIRED |
| `source_title` | string | REQUIRED |
| `publisher` | string | REQUIRED |
| `source_date` | string | REQUIRED; double-quoted date |
| `observed_date` | string | REQUIRED; double-quoted date |
| `collected_by` | string | REQUIRED; e.g. `gn_info_scout/1.0.1` |
| `confidence` | string | REQUIRED; `low` \| `medium` \| `high` |
| `notes` | string | optional |

**Attribute vocabulary (profile-defined, not renamed fields):** definition
slugs carried in `attribute` with the verdict in `value` — e.g.
`attribute: schloss`, `value: "listed as Schloss in the Saxony
Denkmalliste"`; plus structural attributes `name`, `country`, `region`,
`period`, `register_entry`, `location`. Domain nuance lives here and in the
profile — **never** in renamed keys (`claim`/`citation` are the trap that
broke menowise).

## 2. structures — `data/sites/<id>.yml` (FROZEN path; profile fields)

One file per structure under `data/sites/` — the path is fixed even though
the subjects are structures, not "sites" (backpacks precedent). Structural
rules are frozen (`id` = filename stem; all dates double-quoted strings;
records hold only profile fields; numeric metrics plain numbers). The
**fields** are the profile's to define:

| field | type | constraints |
|---|---|---|
| `id` | string | = filename stem; structure slug |
| `name` | string | required |
| `aka` | list[string] | optional alternate names |
| `country` | string | required |
| `region` | string | subdivision (e.g. `Saxony`); optional |
| `location` | object `{lat,lon}` | optional; plain numbers |
| `period` | string | optional; construction period |
| `definitions` | list[verdict] | each: `definition_id` (→definitions.id), `satisfies` (bool), `signal_refs` (list of sig ids), `confidence`, `notes` |
| `registers` | list[obj] | each: `register_id` (→sources), `entry_ref`, `signal_refs` |
| `confidence` | string | overall; `low`\|`medium`\|`high` |
| `sources` | list[string] | signal ids / source refs backing the record |
| `notes` | string | optional |

Disagreement is preserved, not averaged (`signal > canon`): a definition
verdict may cite conflicting `signal_refs` and record the disagreement in
`notes` rather than collapsing to a single truth.

## 3. definitions — `data/definitions.yml` (authored reference, outside the frozen contract)

The domain's headline object. Not gnome-emitted.

| field | type | constraints |
|---|---|---|
| `id` | string | slug, e.g. `fortified_residence`, `schloss`, `popular_castle` |
| `label` | string | display name |
| `description` | string | what this definition admits/excludes |
| `closure_rule` | string | `enumerable` \| `open` |
| `register_ref` | `["string","null"]` | source id of the settling register when `enumerable`; `null` when `open` |
| `scope_source` | string | citation to the definitional literature |
| `notes` | string | optional |

## 4. coverage — `data/coverage.yml` ((definition × region × register) cells)

Derived by code where deterministic; open-band ranges authored. **Negative
space is data (GD-0004):** an empty enumerated cell is `surveyed_empty`,
never conflated with `unexamined`, and `unexamined` names its settling
register.

| field | type | constraints |
|---|---|---|
| `definition_id` | string | → definitions.id |
| `country` | string | required |
| `region` | string | optional subdivision |
| `register_id` | `["string","null"]` | → sources; `null` for open bands |
| `state` | string | `complete` \| `partial` \| `unexamined` \| `surveyed_empty` |
| `count` | `["integer","null"]` | closed cells only; else `null` |
| `count_low` | `["integer","null"]` | open-band range floor |
| `count_high` | `["integer","null"]` | open-band range ceiling |
| `assumptions` | string | required when a range is published |
| `settling_register` | `["string","null"]` | register that would close an `unexamined` cell |
| `source_refs` | list[string] | citations |
| `notes` | string | optional |

## 5. sources — `data/sources.yml`

National heritage registers (Historic England NHLE, Historic Environment
Scotland, Cadw, German state Denkmallisten), Wikidata/OSM (**as subjects of
study, not ground truth**), and the definitional literature. Each entry
carries id, publisher, url, and a robots/ToS review note. Gnomes never
fetch — the scout reads only what a source registration and its cached
material permit.

## Keys & relationships

- `signals.site_id` → `sites.id` (nullable; `null` + `site_hint` for new).
- `sites.definitions[].definition_id` → `definitions.id`.
- `sites.definitions[].signal_refs[]` → `signals.id`.
- `sites.registers[].register_id`, `coverage.register_id`,
  `coverage.settling_register` → `sources` ids.
- `coverage.definition_id` → `definitions.id`.
- Published counts (`data/index.md`) = code aggregation over `coverage`.

## Where the domain maps awkwardly onto the frozen contract (stated, not fixed)

- **The headline object is the definition, not the structure.** The
  archetype gives a structure layer (signals → `data/sites/`); definitions,
  coverage, and counts live in designed datasets *outside* the frozen
  contract. This is correct, not a contract gap — I am not proposing a new
  emission shape.
- **A "count" is not a record.** Closed-band counts are code-derived
  aggregates over structures and finite registers; they are never authored
  integers. Only open-band ranges are authored (with assumptions).
- **Verdicts are per-structure record fields, carried by the profile.** The
  scout still emits one claim per signal; the multi-definition verdict block
  is assembled by the records gnome into the structure record. No signal
  field is renamed to fit this.

## Required founding proof (closing check)

The founding is not schema-done until the frozen gnomes' own dry-run output
validates against this repo's schemas:

```sh
bin/gn-run --gnome gn_info_scout --mode dry-run --repo canonical-castles \
  --fixtures gnomes/gn_info_scout/fixtures/projects/canonical-castles --out /tmp/cc
# validate /tmp/cc/data/signals/*.yml against schema/signals.schema.json

bin/gn-run --gnome gn_info_records --mode dry-run --repo canonical-castles \
  --fixtures gnomes/gn_info_records/fixtures/projects/canonical-castles --out /tmp/cc
# validate /tmp/cc/data/sites/*.yml against schema/sites.schema.json
```
