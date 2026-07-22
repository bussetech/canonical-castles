# Founding proposal vs as-built

The three documents beside this one are `gn_project_founder`'s founding
proposal, preserved as filed (canonical-castles#5, 2026-07-21). They are a
**historical artefact, not current documentation** — the build extended them
the same day.

Recording the delta rather than silently updating the proposal: a founding
document rewritten to match what was built stops being evidence of what was
proposed, and this project has opinions about that kind of tidying.

## Where the proposal and the build agree

Substantially everywhere that matters, and the convergence is worth noting
because the proposal was produced independently while the build was underway:

- Info archetype; the frozen signal shape and `data/sites/` path transcribed
  verbatim rather than redesigned (ADR-0045, platform#232).
- `site_id` typed `["string","null"]`, `site_hint` omitted once resolved.
- Domain nuance in the attribute vocabulary and profiles, never in renamed
  keys — the menowise trap, cited independently in both.
- `definitions.yml` as authored reference data and the spine of the dataset.
- Coverage derived by code, with open bands carrying ranges rather than
  integers.
- Zero new gnomes, no project knoll.

## Where the build went further

Four datasets the proposal did not anticipate, each added for a reason that
only appeared during the build:

| dataset | why it exists |
|---|---|
| `registers.yml` | Counts are only honest against a named, bounded inventory. Registers needed to be first-class, with the exact query behind each figure. |
| `claims.yml` | The research surfaced circulating castle numbers ("France has 45,000 châteaux") that are neither records nor registers. They needed grading by method. |
| `disagreements.yml` | Stage 4. Once two registers could be joined on an identifier, where they disagree became the dataset's own contribution. |
| `production.yml` | Cost recorded as the work happened, because reconstructed cost is estimated cost. |

Two smaller divergences:

- **Attribute vocabulary.** The proposal carries definition verdicts as bare
  slugs (`attribute: schloss`). As built they are namespaced
  (`attribute: definition.<band>`), so structural attributes and band claims
  cannot collide as the band list grows.
- **`verdict.assessment`.** Not in the proposal, and it could not have been:
  the need appeared only when bulk import made it possible to hold 104
  verdicts nobody had assessed. It separates `assessed` from
  `register-derived` so the two are never summed.

## What the proposal got right that the build initially missed

The proposal's schema sketch states that `source_title`, `publisher` and
`source_date` are REQUIRED on signals. The as-built
`schema/signals.schema.json` marks them optional, matching the archetype
contract's own skeleton. The contract wins — but the proposal's stricter
reading is the better editorial standard and is worth revisiting as a
project-level tightening rather than a schema divergence.
