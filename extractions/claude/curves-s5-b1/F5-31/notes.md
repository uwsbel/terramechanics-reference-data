# F5-31, Claude reading (batch curves-s5-b1)

Figure 5-31, AM-68-1 Vol. I, printed page 5-56, PDF 336 (`packet/p0336.png`, 3263 x 4508 px, bilevel).
One panel, one solid line, series `pen`. No symbols, no legend, no inset.

## Labels as printed

1. Caption: "Figure 5-31. Footpad Penetration Depth versus Time (NASA Test No. 2)" (the second line
   in parentheses). Matches `title_as_printed` in `figures-rows.csv`.
2. Time axis title: "Time - Seconds". Labels, from 0: `0`, `.01`, `.02`, `.03`, `.04`, `.05`, `.06`,
   `.07`, `.08`, `.09`, `.1` (the last printed `.1`, not `.10`). Every grid line from 0 to 0.1 is
   labeled; no label is missing from the sequence.
3. Depth axis title: "Footpad Penetration Depth" over "Inches". Labels, from the top of the
   upright figure: `5.0`, `4.0`, `3.0`, `2.0`, `+1.0`, `0`, `-1.0` (`+1.0` carries a plus sign,
   `-1.0` a minus sign, `0` has no decimal).
4. Label slips: none. Every label was checked by eye and by measurement against the line it is
   anchored to (`calibration-eye-checks.csv`); all sit within 13 px (5 percent of a division) of
   their fitted lines. Two things worth knowing:
   - The time label `0` stands 13 px below the bottom frame, the largest offset; it is in step with
     the sequence (250 px below `.01`, the spacing of the others) and labels the frame.
   - The left frame (page u about 590 at the top to 618 at the bottom) lies half a division beyond
     the `5.0` line, at about 5.5 in by the spacing, and carries no label. It is a frame that
     extends past the last labeled line (lesson 2): it was kept out of the calibration box and is
     not a knot. The trace never comes near it (deepest 4.21 in).

## Orientation

The figure is printed sideways. On the page as scanned, time increases upward (v decreasing) and
depth increases to the left (u decreasing): `--x-direction up --y-direction left`. Checked by eye
on the labels (`.1` at the top, `0` at the bottom; `5.0` at the left, `-1.0` at the right).

## Calibration (`cal-p1/`)

1. `tools/calibrate_axes.py detect` on box u 670 to 2235, v 1040 to 3545 (encloses the -1.0 frame
   and the 5.0 line, leaves out the unlabeled left frame), 10 bands, x values 0 to 0.1 by 0.01,
   y values -1 to 5 by 1. All 11 time lines and 7 depth lines detected in 10 of 10 bands; no line
   predicted.
2. Affine residuals: time RMS 6.0e-5 s (0.06 percent of the 0.1 s span), largest 1.2e-4 s
   (0.12 percent); depth RMS 0.0069 in (0.11 percent of the 6 in span), largest 0.012 in
   (0.21 percent). Below the 0.5 percent threshold.
3. Piecewise map (D-025), with the page image: all 18 lines verified on the ink (time lines: ink at
   18 of 18 positions; depth lines: 25 of 25), location errors 0.50 to 0.85 px (time) and 0.50 to
   1.13 px (depth). No line rejected, no recovery needed.
4. The scan is tilted: the time lines run at dv/du of -0.0075 to -0.0088 (about 0.47 degrees), the
   depth lines at du/dv of +0.0117 to +0.0123 (about 0.69 degrees), so the printed grid is about
   0.2 degrees off square on the scan. The piecewise map keeps each line's own tilt.
5. Values in `points-p1-native.csv` come from `calibrate_axes.py piecewise ... --image`. The first
   and last features carry `extrapolated x` only because their pixel intervals reach past the
   frame lines t = 0 and t = 0.1 that they sit on.

## How the line was read

1. Every pixel row v crosses the line once (depth is single valued in time). `helpers/trace_rows.py`
   takes, row by row, the dark run nearest the tracked position (`helpers/rows.csv`). A row is
   `clean` when that run is clear of every grid line: of a depth line by its half width (4.5 px)
   and of a time line by its half width plus the line's half thickness (8.5 px; 10 px at the bottom
   frame, which is 10 px thick). 2090 of 2440 rows are clean.
2. A sample's center is the straight-line fit of the clean run centers over plus or minus 6 rows,
   evaluated at the sample's row; it is always inside the run at that row (checked in
   `helpers/sample.py`). All 36 trace samples have the line's own ink within 2 px once bands of
   plus or minus 5 px around every fitted grid line and frame are removed (my own check, not the
   project's `check_trace_ink.py`, which is not in the packet).
3. Bound (rule 7): half the line's thickness across it, measured at each sample (median run width
   over plus or minus 6 clean rows, times the cosine of the line's angle to the row). The line is 8
   to 11 px thick, so the bounds are 3.9 to 5.7 px, given for both u and v. In values: about
   0.0002 s and 0.021 to 0.026 in (from the piecewise map).
4. Sampling: every 0.002 s to 0.02 s and every 0.005 s after (25 time targets), and on the steep
   part every 0.2 in where that is finer than the time spacing, that is where the slope exceeds
   0.2/0.005 = 40 in/s after 0.02 s (before 0.02 s it would need 100 in/s and never does). That
   gives the depth targets 1.4 to 3.2 in (10). The 0.05 s and 3.0 in targets fall on the same
   clean row and are one sample. With the first and last rows of the line's own ink, 36 trace
   samples in drawing order (time increasing).
5. A target that falls where the line is merged with a grid line is moved along the line to the
   nearest clean row, and its note says how far and why. Time targets on the time lines 0.01 to
   0.09 moved 8 to 9 px (about 0.0004 s); 0.05 s moved 16 px and 0.08 s moved 23 px, because the
   line also runs into the depth lines 3.0 and 4.0 there; the depth target 2.0 in moved 21 px. A
   sample's time is a sampling location, not a measurement, so these shifts lose nothing.

## Features

1. `first` (0.0000 s, 0.009 in): the line runs into the corner of the bottom frame (t = 0) and the
   depth 0 line. Its own ink is distinct down to row v 3495 (t 0.0005 s, 0.045 in, the first trace
   sample); below that it merges with the depth 0 line and then the frame. The first point is where
   the line's center, extended 12 px straight from the last clean rows, meets the frame's center
   line; its v bound is widened to 12.3 px to reach the last row of the line's own ink. The line
   starts at the origin of the plot within the line's width.
2. `knee` (0.0291 s, 1.894 in): the slope drops from about 65 to 54 in/s, a kink just before the time
   line 0.03 (turn of 5 degrees on the page). Mild, but plain once a straight edge is laid along the
   stretch before it: that stretch extended to 0.04 s is about 0.12 in (30 px) deeper than the line.
3. `knee` (0.0584 s, 3.383 in): the clearest bend; the slope drops from about 49 to 29 in/s over
   0.056 to 0.062 s (turn of 10 degrees).
4. `knee` (0.0897 s, 4.172 in): the line rounds over from about 20 in/s toward the flat top over
   0.086 to 0.093 s (turn of 10 degrees). It is on the same row as the 0.090 s trace sample.
5. `peak` (0.0987 s, 4.210 in): the deepest part of the line is a flat top, level within one pixel
   (0.004 in) from about 0.0976 s to the frame at 0.1 s. The line does not turn down before the
   frame, so this maximum is the end of the record, not a turning point, and its time is not an
   observation (placed at the middle of the flat top). Only its depth should be compared.
6. `last` (0.1000 s, 4.209 in): the line runs into the top frame; its own ink is distinct up to row v
   1085 (0.0996 s, the last trace sample); the center line extended 9 px to the frame's center line,
   v bound widened to 8.7 px to reach the last row of its own ink.
7. No local minimum: the trace rises monotonically, then levels off.

The knees of a gradual bend have no sharp vertex. Each is defined mechanically
(`helpers/knees.py`): straight lines fitted to the stretch before and the stretch after the bend
(time windows named in each note), and the knee is the point of the line nearest their meeting.
Another reader's knee may sit somewhat elsewhere along a gradual bend (2 and 3 above); its depth
will still lie on the line.

## Where the line is hard to follow

The line is bold and clean everywhere; it never leaves the ink or breaks. Its own ink is hidden
only where it merges with grid lines (from `helpers/rows.csv`):

1. At the start, rows v 3496 to 3500 (about 0.0005 s and earlier): merged with the depth 0 line,
   then the bottom frame.
2. Crossing the depth line 1.0, rows v 3122 to 3157 (about 0.0145 to 0.016 s).
3. Crossing the depth line 2.0 and the time line 0.03 together, rows v 2735 to 2789 (about 0.030 to
   0.032 s); the line crosses 2.0 in at about 0.031 s, just after the time line 0.03.
4. Crossing the depth line 3.0 and the time line 0.05 together, rows v 2264 to 2308 (about 0.049 to
   0.051 s).
5. Running along the depth line 4.0 at a shallow angle, rows v 1500 to 1583 (about 0.079 to
   0.0825 s), the longest merged stretch; the line crosses 4.0 in at about 0.0805 s, so at 0.08 s it
   is just shallower than 4.0 (3.96 in at the sample moved to 0.0790 s).
6. At the end, rows v 1061 to 1084: the top frame.
7. Each time line crossing hides about 17 rows (0.0007 s).

The line passes close to three grid intersections, (0.03 s, 2.0 in), (0.05 s, 3.0 in) and
(0.08 s, 4.0 in), but not exactly through any of them: at each of those grid times it is 0.01 to
0.05 in shallower than the round depth (about 1.95, 2.99 and 3.98 in, interpolated along the clean
rows on either side), and it reaches the round depth 0.0002 to 0.001 s later.

## Differences from the task description and the figures index

None found. One panel, one solid line, time 0 to 0.1 s, depth in inches, printed sideways, as
described. No inset and no drop conditions are printed on this figure (they are on Figures 5-25 and
5-32). The conditions in `figures-rows.csv` agree with Table 5-T3 (PDF 325, printed 5-45) for NASA
Test No. 2: Bendix drop No. 11, Vv -60.5 in/s, Vh 83.5 in/s, tau .177 s, RS Loose, Dr 0, gamma 46.9
lb/ft3, phi 41 degrees. Section 5.5.4 (PDF 324, printed 5-44) gives the nominal condition of this
test as 5 ft/s vertical and 7 ft/s horizontal, released with a 45 degree yaw (2-2 landing).

## An observation for the data user (not a reading issue)

The initial penetration rate read from this figure, about 65 in/s on average from 0 to 0.027 s (about
70 in/s at the start), is larger than the drop's vertical velocity at touchdown in Table 5-T3,
60.5 in/s. Gravity could add at most about 10 in/s over 0.027 s (386 in/s2 times 0.027 s) if the soil
offered no resistance at all, so the excess is hard to explain by a vertical footpad travel alone:
the plotted "penetration depth" may not be purely vertical (the drop also has 83.5 in/s horizontal
velocity), or the record's time or depth scale may differ slightly from the table's. The page does
not say which; the reading is the same either way. Someone using this record for validation should
settle what "penetration depth" measures before comparing it with a simulated vertical penetration.

## Units

Native values are in the printed units (seconds, inches). SI columns are added afterwards by the
project's conversion tool (1 in = 0.0254 m exactly); nothing here is converted.

## Files

1. `cal-p1/calibration.json`, `cal-p1/anchors.csv`: the calibration.
2. `calibration-eye-checks.csv`: every label as printed, its measured position and the fitted line's
   position at it, plus the unlabeled left frame.
3. `points-p1.csv`: 36 trace samples and 6 features, pixels and bounds.
4. `points-p1-native.csv`: the same with `x_native` (s), `y_native` (in), read bounds and
   `cal_model`, from the piecewise map.
5. `overlay-p1.png`: the points over the page (crop u 560 to 2400, v 1020 to 3720).
6. `helpers/`: `trace_rows.py` (row extraction, writes `rows.csv`), `profile.py` (depth and slope
   along the line, writes `profile.npy`), `knees.py` (bend location), `sample.py` (writes
   `points-p1.csv`), `eye_checks.py` (writes `calibration-eye-checks.csv`), `knot_report.py` (ink
   check of the knots). Run in that order; `profile.py` must run before `knees.py` and `sample.py`.
7. `crops/`: the zoomed crops looked at (labels, corners, crossings, bends, overlay details).
