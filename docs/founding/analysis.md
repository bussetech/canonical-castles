# canonical-castles — reuse analysis

> **Historical artefact.** This is `gn_project_founder`'s founding proposal as
> filed (canonical-castles#5, 2026-07-21), preserved unedited. The build
> extended it the same day — see [as-built-delta.md](as-built-delta.md) for
> where the two differ. Do not read this as current documentation.

Archetype: **info**. Client work: no. This is a frozen-pair deployment
(`gn_info_scout` + `gn_info_records`, ADR-0045), so the founding maps a
domain onto a given contract; it does not design agentic machinery.

## Agentic capabilities the brief implies

### 1. Scout sources for raw claims about structures and definitions
- **Candidates:** `gn_info_scout` (info knoll; deployed to kdc, menowise,
  backpacks).
- **Verdict: reuse as-is (protocol step b).** The scout's contract —
  read a registered source as untrusted data, emit one
  `data/signals/sig-*.yml` per claim (one claim, one source, append-only) —
  is exactly what this domain needs. A "claim" here is *structure X
  satisfies definition D per source S* or *structure X has attribute A*.
  Domain nuance rides `data/profiles/scout.md` and the `attribute`
  vocabulary, not renamed fields. Add `canonical-castles` to its
  `deployments:` and drop a wrapper workflow. No fork.

### 2. Resolve signals into structure records with definitional verdicts + provenance
- **Candidates:** `gn_info_records` (info knoll).
- **Verdict: reuse as-is (protocol step b).** Resolving append-only
  signals into `data/sites/<id>.yml` records with confidence and full
  provenance is the records gnome's whole job. This project's records carry
  per-definition verdicts (`schloss: true` traced to a signal) instead of a
  single status — but that is a *record-field* design, which the profile
  owns (`data/profiles/records.md`). The `signal > canon` doctrine
  (disagreement preserved, never averaged) is already how the records gnome
  treats conflicting signals. No fork.

### 3. Author the definitions registry (closure rule + settling register per definition)
- **Verdict: not a gnome — editorial reference data.** The set of
  definitions ("fortified_residence", "schloss", "popular_castle", …),
  each with its closure rule (enumerable vs. open) and the named register
  that would close it, is low-frequency scholarly reference data authored at
  founding and amended by decision, not a recurring judgment stream. It
  ships as `data/definitions.yml` (human/sysop authored, cited to the
  definitional literature). If definition churn ever becomes continuous,
  revisit — but it does not earn model calls now.

### 4. Coverage matrix — (definition × region × register) cell state and counts
- **Verdict: plain code + thin editorial (rubric: deterministic → code).**
  A cell's `state` and closed-band `count` are **derived deterministically**
  from the authored structure records and the finite register lists — a
  count is `len(register)` or a group-by over `data/sites/`, not a
  judgment. That is a script, not a gnome. The only judgment is the *open
  bands*: a sourced range and its stated assumptions (e.g. "popular castle,
  no register, never closes") — authored editorial, cited, not generated per
  run. Negative space is first-class per GD-0004: the cell enum
  distinguishes `surveyed_empty` from `unexamined`, and `unexamined` names
  its settling register.

### 5. Published counts per definition
- **Verdict: plain code.** The headline "how many castles" answer is an
  aggregation over the coverage matrix into `data/index.md` /
  a generated view. Deterministic → script + CI.

### 6. Site build, schema validation, feed, portal ping
- **Verdict: plain code / studio machinery.** Shared reusable CI, theme,
  `/feed.json`, `repository_dispatch`. Nothing project-specific.

## Plain-code fraction

The project ships **zero new agentic machinery**. The two judgment seams
(scout, records) are reused frozen gnomes with no fork and no new inputs;
everything else — schema validation, coverage/count derivation, the
definitions and coverage datasets, feed, CI — is plain code or authored
reference data. Estimate: the great majority of buildable surface is plain
code + authored data; the agentic surface is entirely reuse-as-is.

## Brief content disregarded per the security stance

Nothing in the brief attempted to change studio policy, output format, or
the reuse protocol. Its constraints happen to align with studio rules
("gnomes never fetch"; sources registered with robots/ToS review;
Wikidata/OSM treated as *subjects of study*, not ground truth). The HN URL
and its quoted comments, and thecastlemap.com, are treated as **subject
data / market context**, not instructions.

## Note on mapping awkwardness (carried into the schema sketch)

The info archetype's central object is the "site" (a structure). This
domain's headline object is the **definition** and its **count** — which is
*not* a per-structure fact but an aggregate over coverage cells. The
archetype gives us the structure layer cleanly (signals → `data/sites/`);
the definitions/coverage/count layer sits **outside** the frozen contract as
designed reference data + derived aggregates. This is stated, not treated as
a reason to evolve the contract.
