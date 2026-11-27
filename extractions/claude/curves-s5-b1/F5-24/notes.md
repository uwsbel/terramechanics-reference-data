# F5-24, batch curves-s5-b1, Claude reader (blind)

Figure 5-24, printed page 5-49, PDF page 329 (`packet/p0329.png`, 300 dpi, unrotated). Caption as
printed: "Figure 5-24. Footpad Penetration Depth versus Time (NASA Test No. 1)". One panel, one
solid line, series `pen`. No symbols, no legend, no inset on this figure.

## Orientation

The figure is printed sideways (the caption reads bottom to top; turn the page 90 degrees clockwise to
read it). On the unrotated page, time increases up the page (v decreasing) and depth increases to the
left (u decreasing). Calibrated with `--x-direction up --y-direction left`; the by-eye label checks
below confirm both directions.

## Labels as printed

1. Time axis (right of the frame on the page), bottom to top: `0`, `.01`, `.02`, `.03`, `.04`, `.05`,
   `.06`, `.07`, `.08`, `.09`, `.1`. The top label is printed `.1`, not `.10`. Axis title: "Time - Seconds".
2. Depth axis (below the frame on the page), right to left: `0`, `1.0`, `2.0`, `3.0`, `4.0`, `5.0`,
   `6.0`. Axis title: "Footpad Penetration Depth (in.)" (lowercase "in." in parentheses; the left
   stroke of the "n" is broken in the scan, the text is not in doubt).
3. Every label was located on the page and set against its fitted line
   (`calibration-eye-checks.csv`): all 18 sit on their lines, the largest offset 8.1 px for `.07`
   (3 percent of the 245 px spacing; the short "7" glyph makes the label's extent lopsided), all others
   within 4.5 px. No label slip: both sequences are complete and evenly spaced, with no wrong sign or
   digit.
4. The plot frame extends one grid spacing past the last labeled depth line: the left frame line lies
   242 to 243 px beyond the `6.0` line (the grid spacing is 245 to 247 px), where 7.0 would fall, and
   carries no label. It was left out of the calibration box (u 700 to 2340), so the `6.0` line is the
   outermost depth line; the frame is not a knot and no value was assigned to it. The trace never comes
   near it (largest depth 4.43 in).
5. Difference from the figures index: `y_unit_as_printed` is "In."; the page prints "in." (lowercase,
   in parentheses). Everything else in the index row (title, axes, one curve, rotation 90) matches the
   page.

## Calibration (`cal-p1/`)

1. `tools/calibrate_axes.py detect`, box u 700..2340, v 1060..3580, 10 bands, x values 0 to 0.1 by
   0.01 (11 horizontal page lines), y values 0 to 6 by 1 (7 vertical page lines). All 18 lines
   detected in 10 of 10 bands; none predicted. 77 anchors.
2. Affine residuals: time RMS 5.7e-5 s (0.057 percent of the 0.1 s span), max 1.5e-4 s (0.15
   percent); depth RMS 0.0061 in (0.10 percent of the 6 in span), max 0.011 in (0.18 percent). All
   below the 0.5 percent limit.
3. The page is tilted by about 0.8 degree (vertical lines du/dv +0.013 to +0.014, horizontal lines
   dv/du -0.010 to -0.011); each line keeps its own tilt in the piecewise map.
4. Piecewise map (D-025) with the ink check (`cal-p1/knots-ink-check.json`): all 11 time lines and all
   7 depth lines verified (ink found at 18 of 18 and 25 of 25 positions; the fitted line within 0.7 px
   of the ink at both ends); none rejected. Line location errors 0.5 to 1.0 px. Values in
   `points-p1-native.csv` come from this map (`calibrate_axes.py piecewise --image`).

## The trace

1. One heavy solid line, 8 to 11 px wide across the stroke; the bound of every trace sample is half
   the width measured across the stroke at that sample (4.0 to 5.4 px), the same in u and v.
2. Centers come from a row scan (`work/rowscan.py`): for each page row, the midpoint of the trace's
   dark run, then a local quadratic fit of u(v) over the clean rows near the sample (`work/sample.py`).
   All 42 rows were checked to sit on dark ink; at clean rows the sample is within 1.0 px of the run
   midpoint.
3. 37 trace samples in drawing order: every 0.002 s from 0.002 to 0.020 s, every 0.005 s from 0.025 to
   0.095 s, plus 10 samples at 0.2 in steps of depth (2.0 to 3.8 in and 4.0 in) where the 0.005 s
   spacing exceeds 0.2 in (0.020 to 0.055 s); a 0.2 in step within 0.05 in of a time sample was not
   added (3.4 in, next to the 0.040 s sample at 3.396 in). From 0 to 0.02 s the 0.002 s spacing is
   already about 0.2 in (slope 100 to 103 in/s), so no depth steps were needed there.
4. 12 samples fall where the stroke crosses a grid line (the 0.01 s time samples lie on the horizontal
   grid lines; others where the stroke crosses a vertical line, longest at the 4.0 in line, v 2227 to
   2280, where the stroke runs along the grid line for about 50 rows). The stroke is continuous through
   every crossing; the center there comes from the clean rows on both sides. These are noted per row.
5. Start: the stroke runs into the bottom right corner of the frame (t = 0, depth = 0) and its ink
   merges with the frame ink there. The first sample is where the stroke's centerline meets the inner
   edge of the right frame line (depth 0): u 2312.5, v 3527.8, t = 0.00035 s, depth 0.012 in. Its depth
   bound reaches past the depth 0 line, so the tool flags it `extrapolated y`; the value itself is
   inside the frame.
6. End: the stroke runs into the top frame line (t = .1) and merges with it. The last sample is where
   the stroke's centerline meets the frame's inner edge: u 1227.8, v 1110.0, t = 0.0998 s, depth
   4.33 in. No sample was placed at t = 0.1 itself, which lies inside the frame's ink.
7. A small drafting joint: near v 2155 (t about 0.057 s, depth about 4.1 in) the stroke is offset by
   2 to 3 px where two pen strokes meet. No sample sits on it (nearest, 0.055 s at v 2205).
8. The page image repeats about every third pixel row (it appears resampled from a lower resolution);
   this does not affect the centers beyond half a pixel.

## Features

1. `first`: as the first trace sample (t = 0.00035 s, depth 0.012 in).
2. `knee` (t = 0.040 s, depth 3.41 in): the first rounded bend, where the nearly straight initial
   penetration (slope about 100 in/s falling to about 80 in/s by 0.03 s) turns to a gentler, nearly
   straight stretch (about 42 to 48 in/s from 0.044 to 0.052 s). Placed at the largest curvature of the
   centerline. The bend is gradual (curvature above half its largest from v 2452 to 2660, about 0.036
   to 0.045 s), so the bounds span that stretch: 61.6 px in u, 104 px in v (0.26 in, 0.0044 s).
3. `knee` (t = 0.060 s, depth 4.24 in): the second rounded bend, from that stretch to the plateau
   (slope falls from about 37 to about 10 in/s between 0.054 and 0.068 s). Placed at the largest
   curvature, which is the sharpest bend of the curve; bounds span v 1998 to 2150: 18.3 px in u, 76 px
   in v (0.083 in, 0.0031 s). Both knees are soft bends of a smooth curve, not kinks; a reader who
   records only the second, or neither, is reading the same ink.
4. `peak` (t = 0.0805 s, depth 4.43 in): the maximum depth, on a flat top (the centerline is within
   0.5 px of its extreme from v 1535 to 1627, about 0.078 to 0.082 s); u bound half the stroke width,
   v bound 46 px (0.0019 s).
5. No `knee, minimum`: after the peak the depth decreases steadily (about 4 to 7 in/s) to 4.33 in at the end,
   with no local minimum before the frame.
6. `last`: as the last trace sample (t = 0.0998 s, depth 4.33 in).

## Ambiguities and observations

1. The trace's two ends are hidden in the frame's ink; the end samples are at the frame's inner edges,
   within about one bound of the corner (t = 0, depth 0) and of the t = .1 line.
2. The knees are judgment calls on a smooth curve (see Features); their bounds say so.
3. Observation outside the reading: the initial slope of the trace, about 100 to 103 in/s over the
   first 0.008 s, is lower than the vertical touchdown velocity of NASA Test No. 1 in Table 5-T3
   (PDF 325, printed 5-45: Vv = -114.9 In./Sec., Vh = 0, RS Loose, Dr 0, 46.9 Lb./Ft.3, 41 Deg.).
   Footpad penetration rate need not equal the model's vertical velocity; nothing in the reading was
   adjusted for it.
4. Units: the native file is in the printed units (time in s, depth in in.); the SI step (1 in = 0.0254
   m exactly) is downstream, once, by the project's tools.

## Files

1. `cal-p1/anchors.csv`, `cal-p1/calibration.json`, `cal-p1/knots-ink-check.json`
2. `calibration-eye-checks.csv`
3. `points-p1.csv` (pixels, bounds, notes), `points-p1-native.csv` (plus x_native, y_native, bounds,
   cal_model, from the piecewise map)
4. `overlay-p1.png` (the reading over the figure)
5. `work/`: the reader's helpers (`rowscan.py`, `sample.py`, `labels.py`, `profile.py`), the row scan
   (`rows.csv`), and the zoomed crops used for the by-eye checks
