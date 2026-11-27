# F2-47, panel 1: notes of the Claude reader (batch curves-s2-b2)

Figure 2-47 (PDF page 108, printed page 2-83), "Load-Penetration Curves in Soil No. 4 (RS Dense)
(Dr approx 0.69)". Read on `packet/p0108.png` (3263 x 4558 px), upright: penetration (in) to the
right, load (lb) up. Read on 2026-11-02 under `packet/CURVE-READING.md` and TASK.md, by a second
Claude reader that took over the workspace of an interrupted one (see "Reused and redone").

## Reused and redone

1. **Calibration (`cal-p1/`): reused after checking.** I reran `tools/calibrate_axes.py detect` with
   the same box (470 1660 2670 3255), values (x 0..7 every 1, y 0..2000 every 500) and 7 bands;
   the output is byte-identical to the earlier reader's `cal-p1/calibration.json` (my run is kept in
   `work/cal-redo/`). I checked nine printed labels by eye on my own crops
   (`calibration-eye-checks.csv`, crops in `crops3/lab-*.png`), and
   `calibrate_axes.py piecewise --image` verifies all 8 x lines and all 5 y lines against the ink
   (no line rejected, none predicted).
2. `cal-check/` (earlier reader) is an identical copy of `cal-p1/`; not used.
3. The earlier reader's `crops/`, `crops2/` and `helpers/` (with its column tracks) were **not used**:
   every trace was read anew with my own helpers in `helpers2/` and crops in `crops3/`. (A column
   tracker of the kind it left follows the dashed line, not the solid one, past the crossing at
   1.34 in; I met that failure in my own first run and split the tracking there.)

## Calibration

1. Affine fit on 40 grid intersections: RMS residual 0.0031 in in x (0.04 percent of the 7 in span)
   and 1.69 lb in y (0.08 percent of 2000 lb); largest 0.0055 in and 3.5 lb. All 13 lines detected
   (x = 2 in 6 of 7 bands, y = 1000 in 6 of 7), none predicted.
2. The scan is tilted by about 0.9 degree (vertical lines lean 0.014 to 0.016 px per px), which the
   per-line fit absorbs.
3. The frame is the outermost lines: top frame = 2000 lb, right frame = 7 in, as printed.
4. Labels checked by eye: load 2000, 1500, 500, 0; penetration 0, 1, 5, 6, 7. The load label "0"
   is printed 13 px above the bottom frame line and the penetration label "7" 12 px left of the
   right frame line; both are unambiguous (no other line near).
5. Values in `points-p1-native.csv` come from `calibrate_axes.py piecewise --image` (D-025). The
   affine map differs from it by at most 0.005 in and 2.4 lb on these points. Four rows are flagged
   `extrapolated x`: the first points of both traces, whose bound interval reaches left of the x = 0
   line; their values are inside the frame.
6. Not a grid line: a short horizontal line outside the frame on the left, at about the 715 lb
   level (u 297 to 497, v 2692), touching the "L" of the axis title. There is no line at that level
   inside the frame.

## Which line carries which label

1. **Dashed line = LPT No. 101, Four-Inch Cylinder, Gp = 63.9 (`lpt101`).** The label "Four-Inch
   Cylinder - LPT No. 101, Gp = 63.9" has a leader arrow whose head ends on the dashed line at
   u 718 to 731 (x about 0.72), on the hump of the dashed trace (`crops3/arrow.png`). Line style and
   arrow agree with `series.csv`.
2. **Solid line = LPT No. 91, Four-Inch Footpad, Gp = 62.8 (`lpt91`).** Its label is printed along
   the solid line, just above it, from about 1.8 to 5 in; it has no arrow. Agrees with `series.csv`.
3. Printed text matches `series.csv` and `figures-rows.csv` (the caption's figure number is damaged
   in the scan, "Figure 2-4'." followed by the title; the page number 2-83 is clear).

## Where the traces cross or run together, and how I told them apart

The positions in TASK.md ("cross near 0.5 in and again near 6 in") do not match what the page
shows. What I read:

1. **0 to 0.07 in.** Both start at the origin. The solid leaves the corner of the frame (its first
   pixels merge with both axis lines). The dashed line's first dash is visible only from about
   37 to 40 lb up, where its right edge emerges from the 9 px left frame line; below that it is
   hidden in the axis line (it cannot be followed to the origin).
2. **0.07 to 0.29 in (about 95 to 240 lb): the two run side by side and touch, without crossing.**
   Their strokes merge into one 15 to 20 px wide stroke. Told apart by position and line style: in
   every row the dashed line is on the upper left (higher load) side, the solid on the lower right;
   in the two dash gaps of this stretch (rows 3128 to 3116 and 3072 to 3062) the solid shows alone on
   the right and the dash ends show on the left. At 0.29 in they separate: the dashed line keeps
   rising steeply to its hump, the solid bends onto its plateau.
3. **One true crossing at about 1.34 in, 359 lb (pixel 910, 2965).** The rising solid passes
   upward through the left end of a dash of the descending dashed line. Before it the dashed line
   is above the solid, after it below. Told apart by the direction of each stroke on either side and
   by the dash pattern (period about 57 px, dashes about 46 px long). Just before the crossing
   (u 891 to 902) only the lower 3 to 6 px of the solid line are inked.
4. **1.34 to 6.0 in:** the dashed line stays below the solid. The gap narrows from about 5.4 in
   (edges 5 to 7 px apart at 5.5 and 5.75 in).
5. **6.0 to 6.05 in:** the last dash touches the underside of the solid (edges merged, one white
   hole at pixel 2343, 2253) and ends at about 6.05 in, 1242 lb. It does not cross the solid, and
   there is no dashed ink beyond it (columns checked to 7 in). So "near 6 in" is where the dashed
   line ends against the solid, not a second crossing.

## Sampling and bounds

1. Trace samples every 0.25 in of penetration, in drawing order, from where the ink starts to where
   it ends: `lpt91` 29 samples (start at the frame corner, 0.25 to 6.75 in, end at the right frame
   line, x = 6.98, which serves as the 7.0 in sample); `lpt101` 26 samples (visible start, 0.25 to
   6.0 in, end at 6.05 in).
2. The sample is the center of the line's column run at the column of the target penetration
   (piecewise between the drawn x lines at the trace's row). Where that column was on a grid line,
   in a dash gap, at a dash end (within 4 columns), merged with the arrowhead, or touching the other
   trace's ink, the nearest clean column of the same line was taken (at most 0.031 in away; said in
   `note`). Every sample was checked to have its own ink within 2 px once the grid lines are removed.
3. Bound (rule 7): half the line thickness measured across the line at the sample (run length times
   the cosine of the local angle, median over 7 columns): 2.9 to 4.7 px on the solid line. Dashed
   line: the same, widened along the line by half the gap between dashes (gaps 15 to 20 px measured
   end to end, median 17.8; the mean of the two gaps beside the sampled dash), projected on u and
   v, giving 8 to 12 px. I read "half the dot spacing" for a dashed line as half the undrawn gap
   between dashes, the stretch over which the line is not observed; half the full dash period
   (about 30 px) would cover whole dashes. Samples touching the other trace get 2 px more, and the
   0.25 in samples in the run-together stretch are widened by hand.
4. Two first points sit on partly hidden ink: the solid's at the frame corner (505, 3239), the
   dashed line's at (506, 3215) on the visible right edge of its first dash (its center about 3 px
   further left, inside the frame line and inside the bound).

## Features (`feature` rows, `note` starts with the role)

1. `lpt91`: first (frame corner); knee at 0.51 in, 289 lb (onset of the plateau; gradual);
   knee at 0.86 in, 295 lb (end of the plateau, flat from about 0.52 to 0.85 in); minor kink at
   3.97 in, 882 lb (slope halves for about 0.15 in); minor kinks at 4.97 and 5.05 in (a small step of
   about 20 lb across the x = 5 grid line); knee at 6.13 in, 1286 lb (onset of a steep step; the line
   already steepens gradually from about 6.05 in) and a sharp knee at 6.20 in, 1326 lb (end of the
   step); peak = last point, 6.98 in, 1440 lb, where the trace runs into the right frame line (the
   load is still rising there, so the record's own maximum may lie beyond the frame).
2. `lpt101`: first (visible start, about 0.01 in, 40 lb); knee at 0.54 in, 365 lb (end of the steep
   initial rise; the bend falls in a dash gap and is placed at the start of the next dash); local
   maximum of the hump, 0.83 in, 397 lb (flat top from 0.79 to 0.86 in; recorded as a knee, it is
   not the trace's peak); local minimum, 1.44 in, 352 lb (flat bottom from 1.39 to 1.55 in, just
   after the crossing); peak = last point, 6.05 in, 1242 lb.
3. Peak and last are written as two rows at the same pixel for each trace, so that each role can be
   matched.

## Other ink and ambiguities

1. Stray marks near the dashed line, not part of either trace and never sampled: a horizontal mark
   under the dash at u 1551 to 1590 (v 2702 to 2707, about 3.4 in); one under the dash at u 1166 to
   1181 (v 2905 to 2909, about 2.2 in); one below the curves at u 2313 to 2329 (v 2339 to 2344,
   about 5.95 in); a small blob left of the start at u 563 to 572 (v 3165 to 3168).
2. The arrowhead of the LPT No. 101 label lies on the left end of the dash at 0.71 to 0.79 in; there
   the dash was read from its bottom edge and its own band only.
3. The solid line thins to 4 to 6 px at u 2106 to 2112 (about 5.25 in) and at the crossing; samples
   avoid the thinnest columns.
4. The grid lines have dropouts near the curves (x = 2 line around v 2969 to 2985, the 1000 lb line
   between u 2060 and 2115); they do not affect the calibration (band detection, ink check passed).
5. The knees of `lpt91` at 0.51 and 0.86 in and the flat extrema of `lpt101` are gradual: their
   position along the line is uncertain by 10 to 25 px, given as the u bound.

## Files

1. `points-p1.csv` (71 rows: `lpt91` 29 trace + 10 feature, `lpt101` 26 trace + 6 feature; no
   markers: the figure plots no symbols), `points-p1-native.csv` (piecewise values and bounds).
2. `calibration-eye-checks.csv`, `cal-p1/` (reused, checked), `overlay-p1.png` (red `lpt91`, green
   `lpt101`; checked by eye, overall and on zoomed crops in `work/ov/`).
3. Helpers: `helpers2/` (common.py, track_solid.py, track_dash.py, comps.py, centerlines.py,
   samples.py, assemble.py, rows.py, cols.py); intermediate files in `work/`; crops in `crops3/`.
