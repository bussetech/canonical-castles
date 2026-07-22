# Roadmap

Where this dataset stands, what is planned, and — as much as the rest — what is
deliberately not.

Last reviewed: 2026-07-22.

## Where it stands

| | |
|---|---|
| records | 4,668 |
| confidence | 4,338 low · 319 medium · 11 high |
| verdicts | 4,650 register-derived · 83 assessed |
| coverage cells | 2 complete · 10 partial · 8 unexamined |
| coverage of closable cells | 10.97% |
| cross-register disagreements | 680 across two register pairs |
| count claims graded | 17 |

**The number that matters is not coverage.** It is that 4,650 of 4,733 band
verdicts are `register-derived` — transcribed from a register's own typology,
at `confidence: low`, with nobody having applied this project's criterion to the
structure. Breadth has moved by two orders of magnitude. Depth has barely moved.
Everything this site actually argues rests on the 83 assessed verdicts and the
register comparisons.

## Planned, in priority order

### 1. Convert register-derived verdicts to assessed

The central debt, and the only work that changes what this dataset *knows*
rather than how much it holds.

There is no cheap version. Corroboration raised 317 records to `medium`
confidence at zero cost, but corroboration is evidence, not judgement — two
registers agreeing does not mean anyone applied the band criterion. Converting
a verdict means reading the structure against the criterion and writing a basis
that engages it.

Realistic approach: **work by cohort, not by volume.** The 129 Anglo-Norman
masonry castles are the strictest reading of an Irish castle and a bounded,
meaningful set. Assessing that cohort would give the `fortified_residence` band
a genuinely assessed core, and the register keeps the finer class on every
record so the cohort is already selectable without re-querying.

### 2. More register pairs

The disagreement method generalises anywhere two registers share an identifier,
and each pair both corroborates records and surfaces conflicts. Two are wired
(Cadw↔Wikidata via `P3007`, Irish SMR↔Wikidata via `P4057`). Candidates:

- **Coflein** (`P4658` is already on Wikidata items) — a second Welsh axis on an
  already-closed cell. Coflein returns 158 castles against Cadw's 104, so the
  set difference is itself a finding.
- **Northern Ireland**, once a joinable identifier is confirmed. Its register
  answers `General_Type='CASTLE'` with **4**, which makes it the sharpest
  available demonstration of why a single register should never be trusted alone.

### 3. Apply the other five bands to existing records

Every imported record carries a verdict on `fortified_residence` and nothing
else — the other five bands are omitted, which the schema correctly reads as
*unassessed* rather than *no*. Registers cannot settle them: `popular_castle` is
a claim about usage and needs naming sources, `palatial_seat` needs the building.
This is genuine research, and it is the work the `gn_info_scout` deployment
exists to feed.

### 4. Run the gnome pair for real

The pair is deployed, configured and fixture-proven, and has never run live
against this repo. The provenance page says so. Until it does, this is a
project *about* agentic research that has done none, and closing that gap is
worth doing for its own sake.

## Deliberately not planned

**Ireland's 31,431 ringforts.** The largest closable population available, and
recorded as a measured stop on the `enclosure_fortification/IE` coverage cell
rather than left as a gap. At 4,668 records CI runs 99s (data) and 71s (site);
7.7× the corpus puts it at roughly 15–40 minutes per pull request, permanently,
and the repository at ~72,000 files. What that buys is coverage of 11% → ~85%
composed entirely of `confidence: low` transcriptions of a register that already
publishes the figure. The import is a solved problem and one deliberate decision
away if the integer is ever wanted for its own sake.

**Filling the three open bands.** `palatial_seat`, `revival_folly` and
`popular_castle` have no denominator — no register bounds them and none could —
so adding records never increases completeness, only size. Their value is
boundary-stressing exemplars, and diminishing returns arrived at roughly thirty
records. Sham Castle earns its place; the five hundredth stately home does not.

**Closing the four blocked cells.** England (no type field in the bulk schema),
Scotland (no castle category, WAF-blocked), Saxony (CC BY-NC-ND, not open data),
Spain (uncountable by law — castles are protected automatically, so the class is
open-ended by construction). Each is recorded with its blocker named. An
unanswered question with a stated cause is worth more than a borrowed number.

## Known debts

- **Hand-entered register references are unreliable.** The first one checked
  against its register was wrong (Trim Castle), and it had produced a duplicate
  record. Every founding-era `register_entries` ref should be verified.
- **A hand-authored record with a wrong ref is still invisible to adoption** —
  see [ADR 0001](decisions/0001-importers-do-not-own-human-judgement.md). The
  duplicate was caught by a coverage cell going one over its register total,
  which makes completeness assertions load-bearing rather than decorative.
- **`source_title` / `publisher` / `source_date` are optional on signals** where
  the founding proposal argued they should be required. The frozen archetype
  contract wins, but the stricter reading is the better editorial standard and
  is worth revisiting as a project-level tightening.
- **Actions minutes are unattributed** in the production ledger — recorded as
  `null` rather than `0`, reconcilable via workflow run ids.
- **No `showcase:` entry** in the studio registry. Deliberate: a dataset with 83
  assessed verdicts should not sit beside a "fully populated flagship" claim.
  Revisit when depth justifies it.
