# Four method questions on reconciling two curve readings (batches curves-appc-b1, -b2)

You are a colleague on this project, not a reviewer of a rival: Claude and you each read eight
direct shear data sheets (Figures C-1C, C-1D, C-2B, C-2C, C-3B, C-3C, C-4B, C-4C of AM-68-1 Vol. II)
blind and independently, and the readings were diffed mechanically. Claude has written its own
answers to the questions below to a file you cannot see; afterwards the two sets of answers are
compared and the better reasoning wins, with credit. Dan (the PI) is away and asked us to settle
method questions between us.

You run read-only in the project repository. Useful files:

- `docs/CURVE-READING.md` (the protocol; section 4 is the comparison rule), `AGENTS.md`,
  `docs/DATA-ORGANIZATION.md` (status vocabulary, bounds), `docs/decisions.csv`.
- `tools/diff_curves.py` (the comparison; read `interp_trace` and the gap rule: no interpolation
  across a gap wider than three times the other reading's median sample spacing). As of today it
  pairs markers and features by position on the page, closest first (it used to pair by sequence
  when counts matched; that shifted every pair in the lower panel of FC-4C).
- The readings: `extractions/claude/curves-appc-b1/<FIG>/`, `extractions/codex/curves-appc-b1/<FIG>/`
  (and `-b2`), each with `points-p1-native.csv`, `points-p2-native.csv`, `notes.md`.
- The diffs and draft canonical points: `qa/curves-appc-b1/diff-<FIG>-p<n>.md`,
  `qa/curves-appc-b1/canonical-<FIG>-p<n>.csv` (and `-b2`).
- The pilot's precedent: `qa/curves-pilot-b1/review.md`, `decisions-p1.csv`.
- Page images: `corpus/1968-vol2/images/p0118.png` (FC-1C) to `p0128.png` (FC-4C).

The numbers: 16 panels, 4602 matched points, 4539 agreed, 56 disagreed. 275 trace samples of the
canonical reading are one-sided. Of these, 196 lie inside a gap of the other reading's trace that
is wider than the gap rule allows (these are dashed curves whose ink is interrupted around every
marker; one reader sampled the dash ends near the markers, the other left the gap); bridging the
other reading's trace linearly across its gap agrees with all 196 within the usual tolerance
(|dy| <= b_y + b_y' + |slope| (b_x + b_x')). The other 79 lie before the other reading's first trace
sample or after its last (the steep first segment near x 3 to 14 thousandths, and the end near
x 245 to 250): the readers disagree about where the drawn line begins and ends. Of the 56
disagreements, 39 are `feature` points (first point, peak, last point of each upper curve); the
peak features mostly agree in y and differ in x on flat-topped peaks (up to 46 thousandths), and
the first-point features differ by 400 to 900 psf where the readers chose different points on a
near-vertical first segment. About 30 markers were recorded by the non-canonical reader only;
the current tool keeps only the canonical reading's points, so those markers would be lost. In
FC-2C's lower panel the two readers assigned several small stacked symbols to different series.

## Questions

1. **The gap rule.** For the 196 one-sided samples inside a gap of the other reading, what should
   the comparison do: keep them one-sided (every one then goes to the human audit as a mandatory
   row), bridge the gap under some revised rule and call them agreed, or something else? If a
   revised rule, state it exactly (a threshold in what units, and why that threshold protects what
   the original rule protected).
2. **Feature points.** Should first/peak/last features be compared at all, and if so how (which
   coordinate, which tolerance)? What goes into the canonical data for a flat-topped peak whose x is
   ill-defined?
3. **Points only in the non-canonical reading** (markers above all, also curve-end trace samples
   the canonical reader did not take): keep them in the canonical output? With what status and
   source, and in whose calibration?
4. **Series ids.** Both readers saw "2935" printed in the legends of FC-2B and FC-2C, and the page
   transcriptions (`corpus/1968-vol2/pages/p0121.md`, `p0122.md`) agree; the figures index
   (`corpus/1968-vol2/figures.csv`, `legend_entries`) says 2995 and the packets told both readers to
   use `n2995`. What should the canonical series id be, and how should the figures index be
   corrected given the rule that indexes are built by tools from extractions, never edited by hand?

For each question give your recommendation, the reason, and what would make you change your mind.
Be concrete and short; a page or two in all. Do not edit any file.
