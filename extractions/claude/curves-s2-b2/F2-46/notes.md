# F2-46, panel 1: notes of the Claude reading

Figure 2-46, "Load-Penetration Curves in Soil No. 3 (RS Intermediate) (Dr approx 0.29)", printed
page 2-82, PDF page 107 (`packet/p0107.png`, 3213 x 4558 px, 300 dpi, upright). One panel, load (Lb.)
up, penetration (In.) to the right, two recorded traces, no markers, no fit lines.

This reading was started on 2026-10-30 by an earlier Claude reader under the same protocol and
interrupted before the write-up. It was checked and finished on 2026-11-02 from the page image only
(section "Kept and changed" below). Both sessions were blind: nothing outside this workspace and
TASK.md was opened.

## Which line carries which label

1. **lpt98, solid line**: printed label "LPT No. 98 : Four-Inch Cylinder, Gp = 27.3", set along the
   solid line just above it, from about (1150, 2790) to (1990, 1960) px. The upper of the two
   traces everywhere.
2. **lpt89, dotted line**: printed label "LPT No. 89 : Four-Inch Footpad, Gp = 22.4", set along the
   dotted line just above it (15 to 35 px above the dots), from about (1370, 2870) to (2250, 2150)
   px, between the two traces but parallel and close to the dotted one. The lower trace everywhere.

Both match `series.csv` (ids, line styles, Gp values); nothing printed differs from the index.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect`, box 560 1480 2480 3500, x values 0 to 6 by 1, y values 0 to 600 by
   100, defaults otherwise. Rerun on 2026-11-02: anchors and map identical to the earlier ones.
2. All 14 lines detected (13 in 5/5 bands; x = 3 in 4/5, the line is broken around the label text
   between v 2380 and 2760). None predicted. 49 anchors.
3. Affine residuals: x RMS 0.0064 in (max 0.014), 0.11 percent of the 6 in span; y RMS 0.53 lb (max
   1.08), 0.09 percent of 600 lb. The grid is drawn slightly unevenly (interior spacing 301 to 312 px
   per inch, 309 to 319 px per 100 lb) and the horizontal lines tilt by about 0.004 while the vertical
   ones tilt by under 0.002, so the piecewise map (D-025) is used for the values;
   `calibrate_axes.py piecewise --image` verified all 7 x and 7 y lines as knots.
4. Frames: left frame = x 0 (u 602, 9 px thick), bottom frame = y 0 (v 3438 at the left, 10 px
   thick), right frame = x 6 (u 2445, 10 px thick): each carries a printed label and both traces
   start at the bottom-left corner. The penetration axis ends at 6 at the right frame; the "short
   tick beyond" is a 15 px horizontal stub to the right of the bottom-right corner (u 2462 to 2477,
   v 3446 to 3450) with no value. A stray rule on the label baseline runs from the 5 to the 6 (u 2150
   to 2441, v 3504 to 3510); it is not a tick.
5. **Top frame**: the load frame top (v 1409, 9 px thick) is 152 to 159 px above the 600 lb line,
   half a grid interval, so it sits at 650 lb by spacing, but no label is printed there. Per
   CURVE-READING section 2 step 4 a frame is a knot only with a value the page supports, so it is
   not used, and the box stops below it. The solid trace ends above the 600 line, so 4 rows
   (trace samples 24 and 25, features 11 and 12, the last two at one location) are flagged
   `extrapolated` in `cal_model`. Using the
   frame as a 650 knot would change them by 0.01 lb at most (`work/points-p1-with650frame.csv`).
6. By-eye label checks (`calibration-eye-checks.csv`, crops in `work/r2/`): x labels 0, 3, 5, 6 and
   y labels 0, 300, 600 against their fitted lines. Every x label is centered within 10 px of its
   line (all seven measured by script in `work/r2/labels.py`, four also by eye; lines about 305 px
   apart). Every load label is printed 6 to 17 px above its line (lines about
   312 px apart); the 0 label is the highest, 17 px above the bottom frame center, but no other line
   is near it. No label is ambiguous.

## Points (`points-p1.csv`, `points-p1-native.csv`)

Counts: lpt98 25 trace + 12 feature; lpt89 25 trace + 4 feature; no markers (no symbols are plotted;
none seen).

1. **Drawing order**: both traces run left to right, penetration never decreases, so `sequence`
   follows u. The solid line's near-vertical step at 5.10 to 5.14 in and its 1 lb dip at 5.56 to
   5.59 in do not double back in penetration.
2. **lpt98 (solid)**: trace samples every 0.25 in from the first ink to the last ink. Each sample is
   the center of the column's run of ink, on the line itself. Where a 0.25 in location falls on a
   grid line (1, 2, 3, 4, 5 in, and 5.75 in, where the trace crosses the 600 lb line) the sample is
   moved 7 to 14 px along the trace onto clean ink, and the note says so. Bound: half the line's
   thickness across the line (column run times the cosine of the local angle), 3 to 4.5 px; the line
   is 5 to 9 px thick across.
3. **lpt89 (dotted)**: each sample is the centroid of the dot nearest the 0.25 in target among dots
   clear of the grid lines (a dot touching a grid line has a biased centroid), never in a gap. Where the
   target falls on or next to a grid line (1, 2, 3, 4, 5 in, and 1.5 in on the 100 lb line) the
   chosen dot is 0.03 to 0.093 in from the target; elsewhere within 0.021 in (the dot spacing is
   about 0.056 in). The note gives each offset. Dots are 10 to 15 px
   wide, spaced 17.3 px (median) along the line. Bound: half the dot spacing along the line and
   half the dot width across it, projected onto u and v, 9 to 11 px.
4. **Ends**. lpt98: the solid ink leaves the inner edge of the left frame at about 16 lb (v 3384 to
   3392); below that, between the frame and the origin, there is no ink of this line outside the
   frame, so any start at the origin is hidden in the frame. First point at u 610 (3 px inside the
   ink), bounds 8 px in u (to the frame center) and 4.5 px in v. The line runs into the right frame
   at about 624 lb; last point at u 2439, 3 px left of the frame's inner edge, bounds 8 px. lpt89:
   first dot at 0.04 in, 8 lb, with no ink between it and the corner (one dot spacing, so a dot may be
   hidden in the frame corner); last dot at 5.97 in, 457 lb, about 11 px left of the right frame center
   (the next dot would fall inside the frame ink).
5. **Features**. First, peak, last for both traces; the peak of each is at its last point (both
   rise to the right frame). Knees and kinks were located on the column runs of the raw ink and a
   turning-angle scan over 15 and 40 px of arc, then looked at on zoomed crops. A kink is recorded
   where the line's direction changes by about 35 degrees or more within about 15 px of arc on
   each side, away from grid crossings (a crossing makes a false turn in the track). Recorded:
   lpt98 knee at 0.34 in (end of the initial steep rise, gradual), kinks at 4.60 and 4.65 in (start
   and end of a short flat shelf, about 1 lb), 5.05, 5.10, 5.14 in (flat, start and top of the
   near-vertical step of about 16 lb), 5.56 and 5.59 in (local load maximum and minimum of a 1 lb dip),
   5.72 in (top of the steep rise below the 600 lb line); lpt89 knee at 0.43 in (end of the initial
   steeper rise, gradual). Bends seen and **not** recorded, below the threshold: lpt98 near 0.63 in
   (about 20 degrees), 4.93 in (about 20 degrees), 5.30 to 5.38 in (a shelf with turns of about 25
   and 15 degrees), 5.78 in (a 16 degree turn hidden in the 600 lb line). The dotted trace has no
   kink; it is concave up between about 1.2 and 2.5 in (slope rising from about 50 to 80 lb per in), a gradual curve.

## Where the traces cross or run together

They do not cross or touch. The dotted trace stays below the solid one over the whole record; the
closest approach is at the very start, where the solid line leaves the left frame at 16 lb and the
first dot sits at 8 lb, about 25 px apart; from 0.25 in on they are 50 px or more apart. They are
told apart by line style (continuous line against separate dots) everywhere, and by the label set
along each. No bound was widened for proximity.

## Other ink, not points

1. Short horizontal strokes inside the plot, off the grid lines and off both traces, at about
   (2020 to 2070, 2400), (2260 to 2300, 2205), (2300 to 2340, 2145) and (1700 to 1830, 2740) px, plus
   the grid lines' interruptions around the label text: paste-up remnants, not data and not markers.
2. Periods and colons of the label text (for example the period of "No." at about (1540, 2730))
   lie 30 px or more off the dotted line; the dot chain rejects them by their offset across the line.
3. A 2 px white break in the solid line at u 823 to 825 (0.72 in) is a print defect, not a gap in
   the record.

## Kept and changed (check of 2026-11-02)

1. **Kept**: the calibration `cal-p1/` (rerun, identical); all 50 trace samples and the 14 earlier
   features. Every dotted sample was matched to an independently labeled dot component (same
   centroid within 0.1 px) and every solid sample to the center of its column's ink run, and every
   point was looked at on zoomed overlay crops (`work/r2/o1.png` to `o6.png`): all on the ink, none
   in a gap, ends and features where the ink shows them.
2. **Changed**: added the two kinks of the shelf at 4.60 and 4.65 in (lpt98 features 3 and 4,
   direction changes of about 54 and 46 degrees within 15 px, sharper than the 1 lb dip at 5.56 in
   that was already recorded); the later lpt98 features are renumbered 5 to 12. `points-p1-native.csv`
   regenerated with `calibrate_axes.py piecewise --image` (the other 64 values unchanged) and
   `overlay-p1.png` redrawn and inspected.
3. **The `work/` alternatives**, settled from the page: `work/points-p1-affine.csv` is the same
   points through the affine map (`apply`), a diagnostic only (differs by at most 0.011 in and 0.67
   lb); `work/points-p1-with650frame.csv` (with `work/cal-650-earlier/`) uses the unlabeled top
   frame as a 650 lb line, which the page does not support (calibration, item 5). Neither is used.
   The earlier final files are kept as `work/points-p1-earlier.csv`,
   `work/points-p1-native-earlier.csv` and `work/overlay-p1-earlier.png`.
4. Helpers of the check are in `work/r2/` (`verify.py`, `track_r2.py`, `chaincheck.py`,
   `dotnear.py`, `rows.py`, `labels.py`, `altdiff.py`, `finalize.py`, which writes `points-p1.csv`
   from `work/points-p1-earlier.csv`); the earlier reader's helpers are in `work/`.

## Ambiguities to look at

1. Where the solid trace starts: its first 16 lb would lie inside the left frame, so the record
   below 16 lb is not readable.
2. Values above 600 lb (the last 0.2 in of the solid trace) are beyond the last labeled load line.
3. Which small bends count as kinks on this wiggly record is a judgment; the threshold and the bends
   left out are listed above, so another reading that records them can be matched.
