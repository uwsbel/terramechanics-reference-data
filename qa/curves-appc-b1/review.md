# Review of batches curves-appc-b1 and curves-appc-b2: eight direct shear data sheets of Appendix C

Date: 2026-10-13. Reconciliation by Claude and Codex together (Dan away; method questions settled
between the two agents, `docs/decisions.csv` D-023). No human audit yet: `qa/audits.csv` has no
row for these batches, so "agreed" and "verified" below are agent results, not confirmations.
This file covers both batches; `qa/curves-appc-b2/review.md` points here.

## What was read

AM-68-1 Vol. II (CR-92215), Appendix C, 300 dpi renderings `corpus/1968-vol2/images/`:

| batch | figure | printed | PDF | soil, state | tests |
|---|---|---|---|---|---|
| b1 | FC-1C | C-4 | 118 | RS, Dr .73 to .88 | 7 (294 to 3520 psf) |
| b1 | FC-1D | C-5 | 119 | RS, Dr 1.0 to 1.16 | 7 (0 to 3520 psf) |
| b1 | FC-2B | C-7 | 121 | PS, Dr .33 to .53 | 6 (734 to 4400 psf) |
| b1 | FC-2C | C-8 | 122 | PS, Dr 1.15 to 1.3 | 6 (734 to 4400 psf) |
| b2 | FC-3B | C-10 | 124 | RSM-a, Dr 0 to .15 | 5 (734 to 4695 psf) |
| b2 | FC-3C | C-11 | 125 | RSM-a, Dr 1.0 to 1.3 | 5 (734 to 4695 psf) |
| b2 | FC-4B | C-13 | 127 | RC2, Dr 0 | 5 (734 to 4695 psf) |
| b2 | FC-4C | C-14 | 128 | RC2, Dr .95 | 5 (741 to 4695 psf) |

Each sheet has two panels: shear stress against shear displacement (curves with symbols) and
dilation against shear displacement (symbols only). 46 tests in all.

Evidence packets: the page images of the figures and of the Appendix C introduction and envelope
pages, the figures-index rows, a series list per figure, `docs/CURVE-READING.md`,
`tools/calibrate_axes.py` and `tools/plot_grid.py`. Hints available to both readers alike: the
figures-index rows still carried the inventory agents' notes (`notes_claude`, `notes_codex`), notes
of an earlier step that AGENTS.md keeps out of evidence packets (found by a Claude reader of batch
curves-appc-b5; removed from later packets, `docs/CURVE-READING.md` section 1); and the series ids,
taken from the index's legend column, which carried the shared misreading 2995. Both readers
overrode that one from the page. Codex read each batch in one run (gpt-6.1-sol,
high; 1838 s and 2465 s); Claude read each figure in its own subagent (898 to 1828 s), outside the
repository until both Codex runs had finished. Neither saw the other's output or any earlier
reading of these figures.

## A misreading both inventories shared

The packets named the third PS test `n2995`, from the figures index. Both curve readers, reading
the legends at full zoom, saw **2935** printed on FC-2B and FC-2C; the page transcriptions agree,
and the PS normal stresses are multiples of 733.7 psf (4 x 733.7 = 2935). Both inventory agents of
`inventory-vol2-b1` had read 2995 independently. Corrected through a new, source-cited input
`qa/inventory-vol2-b1/corrections.csv` applied by `tools/build_figures.py --corrections` (the
sidecar keeps the replaced value); the canonical series id is `n2935` (`series-ids.csv`; the
submissions keep the id they were given).

## Diff

The first comparison exposed a flaw in `tools/diff_curves.py`: with equal marker counts it paired
markers by sequence, so one marker missing at one end and one extra at the other shifted every
pair (FC-4C lower panel: 9 false disagreements). Markers are now paired by position on the page;
the pilot reproduces byte for byte under that change. With the rules of D-023 (features paired by
role, a peak compared in y only, points only the non-canonical reader recorded kept, identity
conflicts flagged):

| figure | panel | canonical | matched | agreed | disagreed | half-bound check: agreed |
|---|---|---|---|---|---|---|
| FC-1C | 1 | claude | 403 | 402 | 1 | 392 |
| FC-1C | 2 | claude | 84 | 76 | 8 | 54 |
| FC-1D | 1 | codex | 783 | 781 | 2 | 757 |
| FC-1D | 2 | claude | 78 | 77 | 1 | 69 |
| FC-2B | 1 | codex | 778 | 773 | 5 | 740 |
| FC-2B | 2 | codex | 125 | 125 | 0 | 112 |
| FC-2C | 1 | codex | 421 | 420 | 1 | 389 |
| FC-2C | 2 | claude | 42 | 39 | 3 | 24 |
| FC-3B | 1 | codex | 505 | 500 | 5 | 499 |
| FC-3B | 2 | claude | 64 | 64 | 0 | 62 |
| FC-3C | 1 | claude | 431 | 428 | 3 | 414 |
| FC-3C | 2 | claude | 64 | 64 | 0 | 62 |
| FC-4B | 1 | claude | 247 | 244 | 3 | 240 |
| FC-4B | 2 | codex | 64 | 64 | 0 | 56 |
| FC-4C | 1 | claude | 244 | 238 | 6 | 236 |
| FC-4C | 2 | codex | 68 | 67 | 1 | 60 |

No calibration, symbol or series disagreement on any panel. The upper panels agree well inside
their bounds; the crowded lower panels of FC-1C and FC-2C lean on their bounds (at half the bounds
36 and 43 percent of their matched markers would disagree), so the audit samples them.
Totals: 4401 matched, 4345 agreed, 56 disagreed (Claude first reported 4602 / 4539; Codex caught
the arithmetic error).

## Method questions settled with Codex (D-023)

Asked as a blind compare (`adjudication/method-questions.md`, both answers kept):

1. **Gap samples.** 196 trace samples of one reader sat inside a gap of the other's trace (dashed
   lines interrupted around symbols); all 196 agreed with the other trace bridged by a chord.
   Claude proposed calling them agreed below a 60 px gap; Codex argued that a chord does not show a
   sample is on the ink or on the right branch, and that the threshold was unvalidated. Codex's
   view was adopted, and the adjudication proved it: **36 of the 196 were off the line** (on the
   bases of triangle symbols, mostly FC-3C n734, or in white space).
2. **Features** are paired by role (first, peak, last) and a flat-topped peak compared in height
   only (Codex's proposal; Claude had proposed the height comparison without role pairing).
3. **Points only the non-canonical reader recorded** are kept with their own source (both agreed).
   Codex added the **identity-conflict check**: a one-sided marker on a marker the other reader
   filed under another test is one symbol, not two. It found 28 such cases, mostly in the stacked
   lower panels of FC-2B and FC-2C.

## Blind adjudication

Every disputed or one-sided point (314 items, 7 of them the pilot's curve-end samples that the old
tool had dropped silently) went into a packet: one crop per item with both readings drawn under
neutral labels P and Q, shuffled per item, the key kept outside (`adjudication/key.csv`). Four
Claude subagents and two Codex runs answered every item independently; a second round put the 62
split items, with both first-round answers under neutral names, to a fresh Claude and a fresh Codex
adjudicator, with three conventions fixed (a sample within 2 px of the line's ink is on it, a sample
on a symbol's outline is not; a line's first or last point is its ink end, or the symbol's center
when the line runs into it without a gap; a white pocket between symbols is not a symbol). Rules
in `docs/CURVE-READING.md` section 4.6; scripts in `adjudication/scripts/`.

Outcome:

1. **Disputes where one reading had to be right** (paired markers and features, identity
   conflicts): Claude's reading right 23 times, Codex's 33 (first round 18 and 13, second round 5
   and 20).
2. **Systematic slips found.** Codex ran its traces onto the first and last plotted symbols of a
   curve rather than stopping where the line's ink stops: 79 of its samples on FC-1C, FC-1D, FC-2B
   and FC-2C are excluded (48 at curve starts, 31 at curve ends). Claude's FC-3C reader followed the
   bases of the n734 triangles at dash gaps: 35 samples excluded (6 more on FC-4C). On the pilot, 8
   of Claude's 11 curve-start samples were on symbols (excluded), 3 are on the ink (now verified and
   in the data). All excluded points were one-sided: no value
   that both readers held is lost, and the first symbol of each curve is still its first marker.
3. **Still open after two rounds (19 items)**, `adjudication/still-split.csv`: six identity
   conflicts in the stacked lower panels of FC-2B (x 39 to 68) and FC-2C (x 90), where a square, an
   x and a triangle merge, `pending-review`; four trace samples at dash tips on FC-3C and one feature
   pair on FC-3C, which stay one-sided or pending; five subjective features ("knee") that stay
   one-sided; four first or last points that neither reader marked right, dropped (the curve's ends
   remain in its samples and markers). The pending and one-sided points are mandatory rows of the
   human audit (D-022).

Notable single findings: FC-4C items 304 and 305, a "symbol" each reader filed under a different
test (n2934, n3815), are a white pocket enclosed by the strokes of the n4695 plus, the n741
triangle and the axis; each reader had missed one real symbol nearby. Both rows are excluded.

## Canonical points

| batch | points | agreed | resolved | one-sided-verified | one-sided | pending-review |
|---|---|---|---|---|---|---|
| curves-appc-b1 | 2757 | 2693 | 20 | 37 | 2 | 5 |
| curves-appc-b2 | 1886 | 1669 | 14 | 194 | 8 | 1 |

(At this review. Now b1 2,007 and b2 1,764, after the re-derivation of D-025, the off-ink rule of D-032
and the correction of `some` answers of D-039: `qa/curves-rederivation-d025/review.md`, Totals.)

`canonical.csv` per batch (all figures and panels), `canonical-<figure>-p<n>.csv`,
`diff-<figure>-p<n>.md`, `decisions-<figure>-p<n>.csv`, `overlays.csv`, `panel-map.csv`,
`series-ids.csv` (b1), `audit-meta.json` (what a reviewer is told about each figure; three tests
drawn as filled dots are named "filled circle" there: FC-1D n0, FC-2B and FC-2C n734).

## Still to do

1. Done the same night: the Appendix C experiment inventory (`qa/experiments-vol2c-b1/review.md`)
   gave the 46 tests their rows, and `tools/build_observations.py` wrote their records to
   `data/experiments/b68-ds-fc-*/` (one figure at a time from the batch's canonical file,
   `series-map.csv` with a figure column). An independent check: the 1968 computer fit printed on
   Figure C-9A (tan 1.3059, cohesion 634.20 psf) is reproduced within 0.3 and 0.1 percent by a
   least-squares line through the C-1D peaks as read here.
2. The human audit (wave 1 of D-022) samples these figures with the pilot.
3. Notes from the readers worth a later look: FC-1D's 0 and 294 psf tests have no legend symbol
   (filled dot and open circle by elimination); several upper symbols sit off their drawn lines
   (FC-1D n2345, FC-3B n734, FC-4B); dilation points above the +100 frame on FC-1D.

## Afterwards: `span` bounds rounded outward (2026-11-19, batch curves-s5-b1)

A `span` decision widens a point's read bounds to take in the other reading's value and bound. `tools/diff_curves.py`
wrote the widened bound to three decimals by ordinary rounding, so a bound could fall short of the other reading by up
to half a unit of the last decimal (Codex's review of batch curves-s5-b1). It now rounds such a bound up. Here eight
bounds of six points of the span decisions of 2026-10-27 widen by 0.001 in their printed unit (both bounds of the
points in `b68-ds-fc-1c-n3520` and `-fc-1d-n2935`, one bound of those in `-fc-2b-n2200`, `-fc-2b-n2935`,
`-fc-2b-n734` and `-fc-2c-n3660`); no value or status changes.
