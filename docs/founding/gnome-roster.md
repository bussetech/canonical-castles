# canonical-castles — gnome roster

## New gnomes: none

This is an info-archetype deployment. It stands up **zero new gnomes** and
adds **zero new gnome inputs**. Per the reuse protocol it deploys the frozen
info pair as-is.

## Deployed (reuse as-is, protocol step b)

| gnome | display | level | knoll | trigger | input_trust | purpose |
|---|---|---|---|---|---|---|
| `gn_info_scout` | Gnome Info Scout | project | info | scheduled cron + manual dispatch | untrusted (reads registered sources as data) | Emit one `data/signals/sig-*.yml` per sourced claim about a structure or definition. |
| `gn_info_records` | Gnome Info Records | project | info | after scout / scheduled + manual dispatch | untrusted (reads its own signals as data) | Resolve signals into `data/sites/<id>.yml` structure records with per-definition verdicts, confidence, and provenance. |

Deployment is: add `canonical-castles` to each gnome's `deployments:` (manifest
+ registry), add a thin wrapper workflow in this repo, and write the two
profiles (`data/profiles/{scout,records}.md`) + `data/sources.yml`. Project
context arrives *only* through those files (EPIC4-05).

## What would have to become true for a new gnome here

- **Definitional judgment becomes a continuous stream.** If deciding which
  definitions a structure satisfies stops being resolvable by the records
  gnome from cited signals and needs a distinct, recurring scholarly
  judgment (e.g. adjudicating contested definitional boundaries at scale),
  that could earn a `gn_castle_adjudicator`. Not now — the records gnome
  handles verdict-from-signal today.
- **Open-band range estimation becomes recurring generation.** If the
  sourced ranges for open bands (e.g. "popular castle") need regular,
  argued re-estimation rather than one-time authored assumptions, that is a
  candidate. Until then it is authored editorial data.

Everything else the domain needs (coverage state, closed-band counts,
published totals) is deterministic → plain code, not a gnome.

## Knoll verdict

**No new project knoll.** Per GD-0023, an archetype deployment reuses its
knoll's gnomes; `gn_info_scout`/`gn_info_records` already belong to the
**info** knoll, and a gnome belongs to at most one knoll. Since this project
homes no new gnomes of its own, it is knoll-less by design. Do not create a
`canonical-castles` knoll.
