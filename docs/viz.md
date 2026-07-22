# Figures: how they are built, and how to reuse them

`/figures/` draws every mark from four includes in `_includes/viz/`. They are
**project-agnostic** — nothing in them knows about castles — and they are
written to be lifted into the shared studio theme, where sibling projects such
as kdc can use them without copying anything.

## The includes

| include | job |
|---|---|
| `viz/styles.html` | The stylesheet. Include ONCE per page, before any mark. |
| `viz/figure.html` | Figure wrapper — title, one-line subtitle, closing note. |
| `viz/bar-row.html` | One labelled bar against a **shared** maximum. |
| `viz/bullet.html` | Stephen Few's bullet graph: a measure inside a reference track. |
| `viz/stacked-row.html` | Ordered part-to-whole, up to three segments. |

Each file documents its own parameters. Two rules are worth repeating here
because breaking them silently produces a wrong chart rather than a broken one:

- **`max` must be shared across every row in a figure.** A per-row maximum makes
  every bar full-width and destroys the comparison the bars exist to support.
- **Internal variables are `_`-prefixed.** Liquid includes share the caller's
  scope, so a bare `assign a` inside an include overwrites the caller's `a` —
  and an `assign b` clobbers a caller's `for b in …` loop variable. That bug
  produced six identical 100% bars here before it was caught by reading the
  rendered HTML.

## The design rules these encode

The studio theme's law is that [colour is wayfinding only](https://bussetech.com):
there is no decorative colour and no categorical palette to draw on. That is a
constraint, and it is also the right answer — encoding classes by **lightness**
rather than hue survives every form of colour blindness by construction.

Only two steps are ever used as classes a reader must tell apart: `--color-ink`
and `--gray-500`, measured **ΔE 31** apart under normal vision and under
deutan/protan/tritan simulation. A third (`--gray-400`) appears only in ordered
scales where every segment is also labelled in text, because it sits below 3:1
against the page and cannot carry meaning alone. The lightest steps are **track,
never data**.

Everything else follows Few:

- One shared scale per figure, so bars compare along a straight edge.
- A **fixed** value column, so the longest label cannot shorten its own track.
- No gridlines, no chart borders, no gradients, no shadows.
- The number is always printed. A bar is a comparison aid, never the only way to
  read a value — and there is no tooltip, so nothing is hidden behind a hover.
- No minimum bar width in `bar-row`: where magnitudes span orders, the short bars
  are honestly short. `bullet` is the exception and floors a non-zero measure at
  0.6% so "present but tiny" is distinguishable from absent; the exact value sits
  beside it.

## Reusing this in another project

Copy `_includes/viz/` and this document. Nothing else is needed — no build step,
no JavaScript, no chart library, and no new dependency in the `Gemfile`.

**The right long-term home is the theme**, so every project gets them from
`remote_theme` rather than a copy. That is a change to shared studio design
machinery and rides the theme release train (label the PR, sysop merges) rather
than being pushed unilaterally from a project. Until then, treat this directory
as the reference copy.

For kdc specifically, the obvious figures already exist in its data: sites by
status as an ordered stacked row, capacity against its basis as bullets, and
coverage of surveyed-versus-unexamined regions — the same three forms used here,
pointed at a different dataset.

## What deliberately is not here

**No hero number on `/figures/`.** A dashboard usually opens with one big figure;
this dataset's argument is that the figure everybody wants does not exist, so
leading with one would contradict the rest of the site. The form follows the
claim, which is the whole of Few's method.
