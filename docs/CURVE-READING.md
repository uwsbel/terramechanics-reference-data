# Reading a plotted curve from a scanned page

How a reader (an agent or a person) turns a plotted figure into numbers that can be checked back
to the page. Written for the pilot (batch `curves-pilot-b1`, the RS direct shear series at Dr .50
to .57) and applied to every curve after it. The method follows the plan: independent axis
calibration per reader, markers first, gridline crossings as repeatable sampling locations,
reading bounds instead of standard deviations, one canonical trace chosen by rule and never an
average of two readings.

## 1. Inputs (the evidence packet)

1. The page image rendered by `tools/render_pages.py` at 300 dpi, unrotated, from the PDF named
   in `sources/register.csv` (`corpus/<source>/images/pNNNN.png`). Every pixel coordinate below
   refers to this image: `u` to the right, `v` downward, origin at the top-left corner. A reader
   who renders the same page at the same dpi gets the same pixels.
2. The figure's row in `corpus/<source>/figures.csv` (panels, curves, legend, units, axis types)
   and the experiment rows it is evidence for, **without the agents' notes columns**
   (`notes_claude`, `notes_codex`): those are notes of an earlier step, and a hint both readers
   see can become an error both make (AGENTS.md, evidence packets are source only). The packets
   of batches curves-pilot-b1 and curves-appc-b1 to -b5 still carried them; their reviews say so.
3. The caption and the pages around the figure, for the test identities and the setup.

A reader never sees the other reader's output, nor either agent's notes from an earlier step.

## 2. Axis calibration (per reader)

1. Choose the box enclosing one panel's plot frame and run
   `tools/calibrate_axes.py detect` with the printed gridline values. The tool locates each
   grid line in narrow bands (a scan is tilted by up to a degree, which a whole-row search cannot
   see), fits each line with its tilt, and takes the grid intersections as anchors; an affine
   map from pixels to values is fitted to them by least squares. `calibration.json` records the
   map, the residuals and every detected line with its source (`detected`, `predicted` when the
   tool interpolated it from the frame, `mixed`).
2. The reader checks the result on the image: at least three gridline labels per axis read by eye
   against the fitted positions (listed in `calibration.json`), and any `predicted` line looked
   at. A residual above 0.5 percent of the axis span, or a line the reader cannot confirm, is
   noted in the reading's `notes.md` and the box or thresholds are changed before any point is
   read.
3. Both readers run the same tool, so a tool error would be shared; the by-eye label check in
   step 2 is what makes the two calibrations independent, and the diff compares the two fitted
   maps as well as the points.
4. **Values come from a piecewise map between verified lines (D-025, from 2026-10-14).** The
   affine map of step 1 is a diagnostic of the drafting; the values of the data are interpolated
   between the two lines of constant value around each point (`tools/calibrate_axes.py
   piecewise`), each line keeping its own tilt, so an unevenly drafted grid (FC-1A: 286 to 311.5 px
   per 1000 psf) is read as drawn. A line is a knot only if it is printed and verified: a
   `predicted` line never is, and every reader's line is checked against the ink of the page
   (`ink_offset`: the centre of the line's core across it, at up to 25 positions between its
   anchors; a lone tick on its stubs, 6 to 14 px from the axis line, which can be 8 px thick). A
   line with ink at fewer than a quarter of its positions, or a median distance from the ink above
   2 px, is not a knot (Claude's x = 50 line of the pilot, found in 10 of 24 bands with the wrong
   tilt, sits 16 px from the ink at the top of the plot). As implemented after Codex's review of
   2026-10-14: a drawn line is verified when ink is found at a quarter of its positions or more (at
   least 3), spread over a third of its length or more, and the straight line fitted to that ink
   (offsets more than 3 MAD from a first fit set aside as crossing curves) lies within 2 px of the
   reader's line at both ends; a tick when its stubs show ink at two positions or more within a
   median 2 px. A frame is a knot only with a value the page supports. A line a reader left out, or
   one the check rejected, is recovered when the page allows it: `tools/calibrate_axes.py recover`
   predicts it from that reading's own two nearest lines (never from the other reading), finds the
   ink across bands, keeps the points that agree on one straight line, and the batch records them
   in `qa/<batch>/knots.csv`, where they replace that reading's anchors of the same value (29 lines
   on 2026-10-14, each straight within 0.7 px; the left frames of FC-6B and FC-6D before them). A
   point's bound is the largest change of value over its pixel interval (four corners and centre)
   with each of its two bracketing lines moved to either end of its own position interval, the
   bracket recomputed after the move; a line's location error is the largest of 0.5 px, the
   scatter of its anchors, and the largest distance between it and the ink's line plus the ink's
   scatter. The global residual is not added. Values
   beyond the outermost verified line are flagged `extrapolated` in `cal_model`. The difference
   between the affine and the piecewise values is reported per series in
   `qa/<batch>/calibration-sensitivity.md` (a correlated calibration sensitivity, largest on the
   initial slope; a change of slope at a grid line is drafting, not soil behaviour).

## 3. Points

Points are read as pixel coordinates on zoomed crops with a labeled pixel grid
(`tools/plot_grid.py crop`, zoom 3, grid every 25 px). The reader writes `points.csv`:

| column | meaning |
|---|---|
| `figure_id` | id in the figures index (`FC-1B`) |
| `panel` | 1 from the top |
| `series_id` | the legend identity, as the figures index names it (`n3520` for the 3520 psf test) |
| `point_kind` | `marker` (a plotted symbol), `trace` (a point on the drawn line at a chosen displacement), `gridline` (the drawn line's crossing of a vertical gridline), `feature` (peak, knee, end of trace) |
| `sequence` | order along the trace, 1 up |
| `pixel_u`, `pixel_v` | center of the symbol or of the line at that location |
| `u_bound_px`, `v_bound_px` | half-width of the reader's uncertainty in pixels: half the symbol size where symbols overlap, half the line thickness where a trace is read (the line's center is known to within half its width; revised 2026-10-08 after the pilot, where one reader used the full thickness and the bounds came out near 1 percent of the axis span), 2 px for a clean marker center |
| `symbol` | as drawn (`x`, `asterisk`, `square`, `plus`, `triangle-down`, `triangle-up`, `circle`) |
| `note` | overlap, ambiguity, a symbol that could belong to two series, anything the student should look at |

Rules:

1. **Markers before traces.** Every plotted symbol is a point. Where a symbol sits on another
   symbol or on another series' line, say so in `note` and widen the bound.
2. **Gridline crossings are sampling locations, not observations.** They are read only for a
   drawn trace without markers, or when the student asks for a trace to be compared at fixed
   abscissae. They are kept in `point_kind = gridline` so no one counts them as data.
3. **Features are read for every trace:** the first point, the peak (maximum of the trace, not of
   the markers), any knee or kink, the last point.
4. **Never sort by x.** A trace that doubles back (unloading, a loop) keeps its drawing order in
   `sequence`.
5. **Log and reciprocal axes** (D-027, from 2026-10-15) are declared to the tool
   (`calibrate_axes.py detect --x-transform log10`, `--y-transform reciprocal`) and calibrated with
   the printed values; a reader never types a logarithm or a reciprocal. The tool predicts, fits and
   interpolates in the plotting coordinate q = T(value) in which the grid is drawn evenly, and writes
   values in the printed unit. On log paper a labelled line is a knot after the ink check; an
   unlabelled minor line is a knot only when its decade and its place in the standard subdivision
   (2, 3, ... 9 times the decade) are unambiguous on the page, with the convention named in its
   source; otherwise it is left out. Trace samples on a log axis are taken at even steps of the log
   (for example every 0.1 decade), not of the value. **Rotated pages** are read unrotated: the pixel
   coordinates refer to the page as scanned, and the calibration takes care of the orientation.
6. What cannot be read is not guessed: a point hidden under another is recorded with a wide
   bound and a note, or omitted with a note saying which symbol is missing.
7. **A trace sample is on the drawn line's ink**, never on a plotted symbol's outline or in the
   white gap between a dash and a symbol; a curve's first and last trace samples are where the
   line's ink starts and ends, not on its first or last symbol (that symbol is a marker). Where
   small symbols stack, a symbol that cannot be identified gets a note and a wide bound, never a
   series by guess. (Added 2026-10-13 after the adjudication of batches curves-appc-b1 and -b2:
   one reader had run its traces onto the first and last symbols of each curve, the other had
   followed the bases of triangle symbols across dash gaps; 114 such samples were excluded.)
   Since 2026-10-30 the rule is also checked mechanically on every trace sample of both readings
   (`tools/check_trace_ink.py`, D-031 v1; `qa/<batch>/ink-checks.csv`): a sample without the line's
   own ink within 2 px, once the fitted symbols, the grid and the frame are removed, is excluded
   before the comparison, and a hand decision cannot keep it (D-032). The check is precise and
   incomplete: it catches about half of the off-ink samples, so reviewers still look for them.
8. **Triangle centers** are the centroid of the reconstructed triangle (from its sides or vertices,
   leaving out stray ink and lines through it), one third of the height from the base for an
   upright triangle. Until the 1968 registration point is established, the bound in the apex
   direction is at least height/6, so that the bounding-box midpoint is inside it (D-024; readings
   before 2026-10-14 mixed both conventions and are to be normalized).
9. **Identity on a derived figure** (an envelope whose points are the peaks of data-sheet tests):
   the legend shape and the line a symbol sits on are both evidence, neither decides alone; where
   the data-sheet peaks of the same tests distinguish the candidates, they settle it (Fig. C-1A,
   C-2A: D-024).

`tools/calibrate_axes.py apply` adds `x_native`, `y_native` (values in the printed units) and
`x_read_bound`, `y_read_bound` (pixel bounds times the local scale, plus the calibration's RMS
residual). `tools/to_si.py` then adds the SI columns; the native columns stay for traceability.

## 4. Comparing two readings (`tools/diff_curves.py`)

1. Series present in one reading only, and symbol or identity disagreements, are reported first.
2. Calibration: the two readings' piecewise maps (section 2, step 4) are compared line by line: for
   every printed value, whether both readings hold a verified line, the largest distance between the
   two lines, and each line's distance from the ink, located once between them; then both maps along
   every verified line of either reading and along the midline of every interval between adjacent
   lines, against the two maps' bracketing line errors. (Before D-025: the affine maps at the four
   corners of the frame, which `--maps affine` still reports.)
3. Points: markers and gridline points are matched by position on the page (both readers use the
   same page pixels), closest pairs first, each point used once, within half the typical spacing
   of the series' points. (Until 2026-10-13 they were matched by sequence whenever both readers had
   the same number; one marker missing at one end and one extra at the other then shifted every
   pair, as in the lower panel of FC-4C.) Features are matched by role first (first point, peak,
   last point, from the reader's note), then by position. Two matched points agree when
   |xA - xB| <= bA + bB and likewise in y; for a peak only y is compared (on a flat top its x is not
   an observation) and the canonical x bound is widened to take in the other reading's x. The rest
   are disagreements, listed with both readings and both bounds.
   Trace samples are different: each reader samples the drawn line at displacements of their own
   choosing, so x is a sampling location, not a measurement. The other reading's trace is
   interpolated linearly, in drawing order, at each sample of the canonical reading, and the
   sample agrees when |y - y_interp| <= b_y + b_y_other + |slope| (b_x + b_x_other). No
   interpolation across a gap wider than three times the other reading's median spacing (a gap
   in the drawn line); such samples stay one-sided. (Rule added 2026-10-08: the pilot's two
   readers sampled every 5 and every 3.4 thousandths and the nearest-x rule reported 92 false
   disagreements.)
4. The canonical reading of a panel (D-025, with Codex's review of 2026-10-14): when both readings
   hold the same verified lines, the one whose lines lie closer to the ink (the mean over the shared
   lines of each line's median distance from the ink); within 0.25 px of each other, which the ink
   cannot separate, the first submission (Claude, reading A), a rule anyone can recompute from the
   submissions, the page and the recovered lines. A reading whose verified lines include all of the
   other's and more is canonical when its shared lines are as close to the ink; coverage that
   differs both ways is reported for review, and the batch names the canonical reading with its
   reason (`overlays.csv` columns `canonical`, `canonical_reason`; D-024: on FC-4A, ticks without a
   grid). Never by smoothness, density of sampling or the affine residual (until 2026-10-14 the
   smaller residual decided: Codex on 14 of 32 panels, 6 of them by less than 3 percent). Both
   submissions are kept under `extractions/`; the canonical points carry `status = agreed` where
   the match held, `one-sided` where the other reading has no point there, `pending-review`
   otherwise. Points only the other reading holds (a marker the canonical reader missed, trace
   samples beyond either end of the canonical trace) are kept too, as `one-sided` with that reading
   as `source`, in its own calibration and numbering: the smaller residual does not make a reading
   complete. A one-sided marker sitting on a marker the other reading filed under another test is
   an identity conflict (`pending-review`), so one symbol never becomes two observations. Trace
   samples of one reader inside a gap of the other's trace (a dashed line interrupted around a
   symbol) stay one-sided: agreement with a straight line across the gap does not show that the
   sample is on the ink or on the right branch (rules agreed with Codex on 2026-10-13, batch
   curves-appc-b1, `docs/decisions.csv` D-023).
5. Disagreements and one-sided points are settled by a page re-read, recorded in
   `qa/<batch>/decisions-<figure>-p<n>.csv` (panel, series_id, point_kind, sequence, source, status,
   use, note) and applied by `tools/diff_curves.py --decisions`: `resolved` (which reading was right,
   with credit; `use` swaps in the other reading's value when it was), `one-sided-verified` (the
   other agent checked the point on the page), `excluded` (not a reading of ink: an interpolation
   across a visible gap, a feature of stray ink). Values are never averaged and never typed in.
   Since 2026-10-14 (Codex's review of D-025): an excluded point is removed from its reading before
   matching and interpolation, and a trace keeps a break where it was, so it supports nothing (75
   agreed trace samples had been compared against stretches holding an excluded sample); a swap
   takes the other reading's whole submitted record, so `source` and `sequence` name the point the
   values come from (a trace value interpolated on the other reading has source `<reader>-interp`
   and the sequence of the canonical sample whose displacement it was taken at); when the canonical
   reading changes, a resolution made on a paired marker or feature of the other reading follows
   the physical symbol through the pairing, while a verification of a trace sample stays with that
   exact sample; and the other reading's trace samples where the canonical trace has no support (a
   drawn gap, a break) are kept as one-sided, in drawing order.
   `--bound-scale` reruns the comparison with every bound multiplied by a factor, as a check of
   how much of the agreement the bounds are buying.
6. **Blind adjudication** (from batch curves-appc-b1 on). Every pending-review and one-sided point
   goes into an adjudication packet: one crop per item with both readings drawn under neutral
   labels, P and Q, shuffled per item, with the key kept outside the packet. A fresh Claude
   adjudicator and a fresh Codex adjudicator answer every item independently, from the page only.
   A disagreement or identity conflict is settled when both name the same reading (or series); a
   one-sided point is verified when the other agent's adjudicator confirms it on the ink and its
   own agent's adjudicator does not deny it, and excluded when both deny it. Items the two
   adjudicators split go to a second round; what stays split keeps its status and is a mandatory
   row of the human audit. Decisions name each point by `source` and `sequence` (a decisions file
   written before 2026-10-13 has no `source` column and means the canonical reading).
   `tools/reconcile_curves.py <batch>` runs the comparison over every figure and panel of a batch
   and assembles `qa/<batch>/canonical.csv`. Besides each point's own columns, a row of it carries
   `status`, `source`, `decision_note` and, where the other reading was compared, that reading's
   value (`other_x_native`, `other_y_native`) and its place on the page (`other_pixel_u`,
   `other_pixel_v`: its own point, or the pixel interpolated along its own samples, the end rule
   included). Audit packets draw the other reading there (since 2026-11-18; the D-027 item).

## 5. What goes into `data/`

`data/experiments/<id>/observations.csv` holds the canonical points in SI with their bounds and
status (`agreed | resolved | one-sided-verified | one-sided | pending-review`), one row per point,
and `series.json` names the figure, panel, series, symbol, both submissions, the calibration
files and the reading rules version. The student's review packet
shows both readings over the page image; a confirmed value replaces a `pending-review` one through
`tools/ingest_review.py`, never by hand.
