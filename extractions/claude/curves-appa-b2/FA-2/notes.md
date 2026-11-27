# FA-2 reading notes (Claude, blind reader, batch curves-appa-b2)

Page `packet/p0007.png`, printed page A-6, scanned bilevel (black and white only), figure printed
sideways: grain size increases up the page, percent finer increases to the left. All pixel
coordinates refer to this image as scanned.

## Identity

1. Printed caption: "Figure A-2. Average and Range of Three Samples of Unused RS Soil", under the page
   header "GRAIN SIZE ANALYSIS CURVES - LM SMS". Matches `figures-rows.csv`.
2. One panel, three curves, no legend on the page. Series as in `series.csv`:
   - `average`: the solid curve, always the middle one (checked on the clean stretch u 1760..2060,
     where the solid stroke is continuous and the two outer strokes are dashed, dashes about 45 px
     with gaps about 13 px).
   - `upper`: the dashed curve on the high-percent side (left on the page at a given grain size).
   - `lower`: the dashed curve on the low-percent side (right on the page).
3. Stroke thickness on this scan is about 10 px (measured 9.5 to 11 across clean strokes), so the trace
   bound is 5 px (half the thickness).

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect` on box 675 1123 2195 3735, `--x-direction up --y-direction left
   --x-transform log10`, 10 bands, frame fraction 0.3 (the parameter table hides the 50 to 90 percent
   lines over more than half of their length). Grain sizes given as printed: 0.02, 0.05, 0.1, 0.2, 0.5,
   1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 9.0 mm; percent 0 to 100 by 10. The raw run is kept in `trial1/`.
2. The top frame line (v about 1085 to 1095) carries no label; by the log spacing it is the 10 mm decade
   line. It was left out (box starts at v 1123, between it and the 9.0 line) so that the labelled 9.0
   line is the outermost x line. The dashed sieve lines and all unlabelled minor lines were not anchored.
3. Frames: bottom frame = 0.02 mm (labelled "0.02" on it); left frame = 100 percent (labelled "100" at
   top and bottom); right frame = 0 percent (labelled "0" at top and bottom); top frame unlabelled, not
   used.
4. `refit_cal.py` (helper, documented in its header) reused detect's band samples but set aside those
   that were not grid ink, then rebuilt anchors and the affine fit in the same layout:
   - the 70 percent track had run onto the table's own vertical border below v 2262 (fitted tilt
     0.0047 against about 0.010 for every other percent line, 9 px off at the bottom labels): its 6
     samples inside the table were set aside;
   - two band samples of the 0 percent frame (v 2820, 3080) were pulled inward by the curves running
     along the frame and were set aside by a straight-line consensus;
   - one sample of the 2.0 line (u 1511, where curves cross it) and the four table-edge samples of the
     0.5 to 0.05 lines were set aside;
   - 20 anchors under the table (u 862..1482, v below 2262) were dropped, since the 50 to 90 percent
     lines are not printed there.
5. Result: 112 anchors; affine residuals x (log10 mm) rms 0.0027, max 0.0064 decade (0.24 percent of the
   2.65 decade span); y rms 0.070, max 0.21 percent finer (0.21 percent of span). All 12 x lines and all
   11 y lines pass the D-025 ink check (`cal-p1/knots-check.json`), location errors 0.5 to 1.1 px; none
   rejected, none predicted.
6. Labels checked by eye: all 12 grain-size labels and all 11 percent labels (top row, and the bottom
   row for 100, 80, 70, 60, 50, 0), each within 7 px of its fitted line, while neighbouring printed lines
   are 25 px or more away (`calibration-eye-checks.csv`). The grain labels sit with their decimal point
   on the line.
7. The values in `points-p1-native.csv` come from the piecewise map (`calibrate_axes.py piecewise
   --image`). The affine map differs from it by at most 0.0030 decade in grain size and 0.17 percent
   finer over these points.
8. 14 points are flagged `extrapolated`: they lie left of the 100 percent frame (percent finer slightly
   above 100, see below).

## Where the curves run together

1. Coarse end (v 1406 to about 1640, grain 2.8 to 4.8 mm): the three strokes form one band along and
   just right of the 100 percent frame. The upper curve lies on the frame itself down to about v 1567,
   and its ink protrudes up to 11 px left of the frame (v 1409 to 1480 and 1541 to 1546), so its
   samples at 4.47 and 3.98 mm read 100.2 to 100.7 percent: that is what is drawn, not a calibration
   effect.
2. Shallow stretch (u 840 to 1135, about 70 to 90 percent finer): one band 17 to 38 px tall; individual
   strokes are not separable.
3. Fine end (below about 0.8 mm, v 2150 to 3163): the band runs along the 0 percent frame; the strokes
   are partly separable down to about 0.35 mm, and below about 0.13 mm the band is a single stroke
   width, so the three curves coincide (about 0.5 to 1 percent finer). The lower curve merges with the
   frame line at several places (v 2590 to 2730, 2780 to 2850, 2928 to 2970).
4. In these stretches I did not guess which stroke is which. The order is fixed by definition (upper at
   or above average at or above lower), so: upper = outer edge of the band on the high-percent side
   plus half the stroke extent, lower = outer edge on the low-percent side minus half the stroke
   extent, average = between them, with bounds widened (up to 9 to 11 px for the hidden average). Notes
   on those rows say so. A few such readings step back by up to 0.4 percent finer from one sample to the
   next; this is within their bounds and was left as read.

## Samples

1. Trace samples at grain sizes 10^(0.05 k) for k = 13 (4.47 mm) down to k = -22 (0.0794 mm), plus the
   first and last points, plus every 5 percent finer between two k samples where the curve rises more
   than 10 percent: upper 35 to 85, average 30 to 90, lower 30 to 90 (the levels each series needs).
2. On the clean stretch (u 1150 to 2160) stroke centres were found column by column or row by row from
   the ink edges (`track.py`, `build.py`), checked on zoomed overlays, and corrected where needed
   (`assemble.py`, OVERRIDE list, each with a note).
3. Dash gaps (rule 7): a sample falling in a gap of a dashed curve was moved to the nearer dash end
   (notes "dash end"): 12 samples, 4 on the upper curve and 8 on the lower.
4. Several sampling lines coincide with printed grid lines, where the stroke is hidden in the grid ink:
   k = 6 (1.995 mm) on the 2.0 mm line, k = 0 on the 1.0 mm line, k = 8 on the 2.5 mm line, k = 12 on
   the 4.0 mm line, k = -6, -14, -20 on the 0.5, 0.2, 0.1 mm lines. Between u 1410 and 1450 the upper
   curve runs inside the 2.0 mm grid line; its centre there is taken from its exposed edges either side.
5. The coarse end: the curves' ink ends at v 1406.5 on the 100 percent frame (about 4.84 mm, near the
   No. 4 sieve line), all three together. The fine end: the ink ends at v 3162 just below the dashed
   No. 200 (0.074 mm) line, on the 0 percent frame (0.073 mm, 0.6 percent), all three together.

## Features

1. First point and last point of each series (shared by the three curves, as drawn).
2. Knee, lower curve only: at (2094, 1986), where it crosses the dashed No. 16 (1.18 mm) sieve line, the
   lower curve turns abruptly from about 35 degrees to nearly vertical on the page. The average and
   upper curves bend gradually there and have no distinct knee.

## Symbols

No plotted symbol could be identified, so no marker rows. Candidates looked at and not counted: humps on
the lower curve at about (1555, 1758) and (1627, 1768), a blob where the three curves and the No. 16
sieve line pile up at (2053 to 2078, 1964 to 1990), and an enclosed white hole at (2098 to 2110, 2128
to 2143) by the No. 20 sieve line. They are consistent with stroke overlaps and dash end blobs; whoever
reviews this should look at them on the page.

## Observation for the reviewer (not used to change any reading)

The printed parameter table gives D50 average 2.2 mm (range 2.1 to 2.3). The drawn curves cross 50
percent at 2.13 mm (average), 2.00 mm (upper) and 2.22 mm (lower), about 0.07 to 0.1 mm finer than the
table. D10 (1.3, range 1.2 to 1.4) agrees with the curves (1.29; 1.21 and 1.36). D95 average 2.8 mm
reads 2.92 mm on the drawn average curve (range ends 2.82 and 3.02 agree with 2.8 to 3.0). The 2.0 mm
line and the 50 percent line near these crossings are labelled and pass the ink check, so this is a
difference between the table and the drawing, not a calibration offset.

## Files

1. `cal-p1/` (anchors.csv, calibration.json, knots-check.json), `trial1/` (raw detect run).
2. `calibration-eye-checks.csv`.
3. `points-p1.csv` (pixels), `points-p1-native.csv` (grain size mm, percent finer, piecewise map).
4. `overlay-p1.png`, this file.
5. Helpers: `refit_cal.py`, `fa2_tools.py`, `track.py`, `band.py`, `merged.py`, `bandB.py`, `build.py`,
   `assemble.py`, `ovl.py`; working crops in `crops/` and `rc/`.
