# 0001 — Importers do not own human judgement

- **Status:** accepted
- **Date:** 2026-07-22
- **Deciders:** sysop (via console)

## Context

This dataset is built by two kinds of act. Deterministic importers transcribe
registers in bulk; people assess structures against the definition bands. The
importers are drift-checked in CI — the committed records must match what the
script would regenerate from a committed snapshot — because an import that
cannot be reproduced is not evidence of anything.

That drift check and human judgement collided **three times in a single day**,
and each collision resolved, by default, in favour of the machine.

**1. The drift check wanted to revert corrections.** Two Welsh records were
corrected from a register-derived `yes` to `contested` after a second register
disagreed. The next `--check` run reported them stale and asked for them to be
regenerated — which would have erased the correction, on every run, forever.

**2. Path-based adoption missed a record under a different id.** Adoption was
first keyed on the file path the importer would have written. Trim Castle was
hand-authored as `ie-meath-trim-castle` with a mistyped SMR reference, while
the register files it under its townland, Manorland. The importer saw no
conflict, created a second record for the same castle, and the Irish coverage
cell came out at 4,553 against a register total of 4,552.

**3. An orphan sweep deleted a hand-authored record.** When the importer gained
the ability to remove its own residue, it treated an *absent* `assessment`
field as "not adopted" and deleted Dún Aonghasa — a founding record. The schema
defines an absent `assessment` as the assessed default. The deletion was caught
by a record-count check that happened to be run, not by a test.

Three different mechanisms, one shared failure: **the pipeline was given the
benefit of the doubt over data a person had authored.**

## Decision

**An importer seeds records. It never owns them, and it never resolves an
ambiguity in its own favour.** Concretely:

1. **Adoption is by register reference, never by file path.** A record claiming
   a register ref belongs to whoever holds it, wherever it sits and whatever it
   is called. Identifiers, never names — the same rule the disagreement ledger
   already runs on, and for the same reason: name matching manufactures both
   false matches and false gaps.

2. **Adopted means untouched.** Once any band on a record is upgraded from
   `register-derived` to `assessed`, the importer reports the record as adopted
   and writes nothing to it. Register evidence still lands: the signal is
   re-pointed at the adopting record rather than dropped.

3. **Deletion requires a positive signal.** A record may be removed only when
   it carries an explicit `register-derived` marker for that band. Absence of a
   marker is never permission. The default on ambiguity is to keep.

4. **Silence is not consent, anywhere in this codebase.** The same rule already
   governs the cross-register comparison — a register class meaning
   "unclassified" is skipped rather than read as a claim, and an unmapped class
   is our ignorance rather than the register's error. This ADR extends the
   principle from analysis to storage.

## Consequences

- Corrections survive re-import. The two Welsh and three Irish contested
  verdicts persist across every subsequent run, and CI proves it: the import
  reports `4 adopted` rather than `4 stale`.
- The importer can safely clean up after itself, which it must — changing the
  id rule once left thousands of orphan records and made the register appear to
  hold more structures than it does.
- A hand-authored record with a *wrong* register reference is still invisible
  to ref-based adoption. That is a real residual gap: the Trim Castle duplicate
  was only caught because a coverage cell went one over its register total.
  **Completeness assertions are load-bearing** — `records_held == register_count`
  on a complete cell is not a formality, it is the check that found this.
- Anything added to this repo that generates files a person may edit inherits
  these rules. There will be more importers; there should not be a fourth
  instance of this bug.

## Alternatives rejected

- **Drop the drift check.** It is the only thing making an import reproducible,
  and reproducibility is the whole argument for importing rather than asserting.
- **Forbid editing imported records.** Register-derived verdicts are provisional
  by construction; upgrading them to assessed is the dataset's main remaining
  work. Making the machine-written layer read-only would freeze the debt in place.
- **Keep a separate override file.** A second source of truth for the same field
  is how records and reality drift apart quietly. The record is the record.
