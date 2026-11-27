# FA-18, Claude reading (batch curves-appa-b2)

Page `p0039.png`, printed A-38. Header "GRAIN SIZE ANALYSIS CURVES - LM SMS"; caption "Figure A-18. Average
and Range of Three Samples of Unused RSM Soil". The plot carries no legend box: the caption names
Average and Range, and the drawing has one solid curve and two dashed curves, which matches
`series.csv` (average = solid, upper and lower = the dashed range). Ids kept as given.

## Axes, frame and labels

1. Printed sideways. Grain size (mm, log) increases up the page; percent finer increases to the left.
2. Grain-size labels on the right: 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 9.0. Each
   was checked by eye against its line (`calibration-eye-checks.csv`); all sit on their lines within
   about 5 px (label centres read to about 5 px).
3. Frames: bottom frame = 0.02 (labelled). Left frame = 100 percent and right frame = 0 percent
   (labelled at top and bottom). The top frame is NOT labelled: the top label 9.0 sits on the line
   45 px below the frame, and the dashed 3/8 inch sieve line (9.5 mm) lies between them. By log
   spacing the top frame is 10 mm, but it is unlabelled and was not anchored. Nothing of the curves
   lies above 5 mm, so no value depends on it.
4. Anchored: the 12 labelled grain-size lines and the 11 labelled percent lines (0 to 100 by 10).
   Not anchored: the top frame, every unlabelled log subdivision (0.03, 0.04, ..., 2.5, 6, 7, 8), the
   2 percent minor lines and all dashed sieve lines.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect` was tried (`try1/`, box 565 1132 2125 3755, log10 x, up/left): the band
   tracker mixed tracks on this dense sheet (many minor and sieve lines, the table hiding the middle
   of lines 50 to 80 percent and 0.05 to 0.5 mm, curves running along the 0 percent frame); max y
   residual 1.87 percent, several lines with wrong tilt. Not used.
2. Instead `helpers/measure_lines.py` measured each labelled line with the tool's own `ink_offset`
   every 10 px along it (seeded from two positions read on the page), set aside outliers (curves,
   table, crossing lines) by a robust straight-line fit, and wrote `anchors.csv` and
   `calibration.json` in the `detect` layout (intersections of the fitted lines, the tool's
   `fit_affine`, x_transform log10, directions up/left).
3. Affine diagnostic residuals: x rms 0.00263 decade (max 0.00635, 0.24 percent of the 2.65 decade
   span); y rms 0.050 percent (max 0.155). Below the 0.5 percent threshold.
4. Ink check (`piecewise --image`): all 12 x lines and all 11 y lines verified, none rejected.
   Location errors 0.5 to 1.2 px except the 60 and 70 percent lines (2.27 and 1.69 px: visible only
   above and below the table, ink offset about 1.2 to 1.5 px at one end).
5. Values in `points-p1-native.csv` come from `calibrate_axes.py piecewise ... --image`.

## The curves, which is which, where they merge

All three curves are drawn with a heavy pen (about 9 px across where separate).

1. Fine end, 0.072 to 1.0 mm (0 to 3 percent): the three curves run down the 0 percent frame
   touching each other (no white between) and the lower one touching the frame. Identity is by
   order (upper leftmost, lower next to the frame) and by the dash gaps: gaps of the upper show as
   the band's left edge stepping right, gaps of the lower as white holes beside the frame; where both
   gaps coincide the solid's two edges are seen. Positions from band edges plus half a line; bound
   5 px in u. From about 0.6 mm down the lower curve overlaps the frame line; below about 0.09 mm the
   solid also lies within about 8 px of the frame.
2. 1.0 to 1.8 mm (3 to 19 percent): three distinct strands at about 45 degrees; middle one
   continuous (solid = average), outer ones dashed. Read directly; bound 4.5 to 5.5 px.
3. Steep part, 2.0 to 2.8 mm (20 to 96 percent): the three curves run together in a band 20 to 35 px
   high, crossed by the 2.5 mm line and the dashed #8 sieve line, which hide its top edge for about
   p 63 to 76 and its bottom edge for about p 61 to 76 (interpolated). Upper = bottom edge minus
   half a line, lower = top edge plus half a line, average = middle of the band; v bound 6 px
   (7 where an edge is hidden). The 2.0 mm crossings lie under the 2.0 mm grid line and are read
   across it.
4. From about 2.8 mm the three curves are one line (run no wider than one line width), then run
   along the 100 percent frame from about 3.3 mm up, merged with it. Same point for all three
   series there (k = 43 to 46 and the last point), bound 6 to 10 px in u.
5. Fine-end first points: upper's last dash visible to v 3160 then hidden under the #200 sieve line
   (about 0.074 mm); ink beside the frame at v 3170 to 3176 taken as the solid (it could be the lower
   dashed curve ending); the lower merges into the frame line, its end not separable (v bound 8).
6. Coarse end: the last curve ink distinguishable from the frame is at v 1466 (about 4.44 mm, 99.4
   percent); between there and the dot the line can only be inside the frame line.

## Marker

One filled dot centred on the 100 percent frame at the #4 sieve line, pixel (592, 1442), about
4.7 mm, 100 percent, where the curves end. Filed once, under `average`, with a note (it is common to
all three curves; one symbol, one observation). No other symbols on the curves.

## Sampling

1. Traces from the fine end: first point, then every 0.05 decade (k = 12 to 46, g = 0.02 x 10^(0.05k)),
   then the last point. k = 11 (0.071 mm) lies beyond the fine ends; k = 47 (4.48 mm) beyond the last
   visible ink.
2. Extra samples every 5 percent where a curve rises more than 10 percent between samples:
   upper k40 to k41 (30 to 45) and k41 to k42 (50 to 85); average k40 to k41 (25 to 40), k41 to k42
   (45 to 80), k42 to k43 (85 to 95); lower k40 to k41 (25 to 35), k41 to k42 (40 to 75), k42 to k43
   (80 to 95). Upper k42 to k43 rises 9.2 percent, so none there.
3. Rule 7, samples in dash gaps moved to the nearest dash end: upper k15, k20, k24, k29, k34, the 40,
   45, 50, 65, 70 percent samples and k42; lower k16, k20, k25, k29, k30, the 25, 30, 50, 80 percent
   samples. Upper k28 under the 0.5 mm line where its dash ends is read on the nearest visible ink.
   Each moved row says so in its note.
4. Samples on grid lines (k = 12, 14, 20, 26, 28, 34, 37, 40, k46) are read across the line.

## Features (per series)

First point; knee at the onset of the steep rise (the 2.0 mm crossing); knee at the rollover toward
100 percent (p = 95, about 2.7 mm, merged); last point, which is also the peak (the maximum percent
finer, along the 100 percent frame, merged).

## Cross-check against the printed table (not used in the reading)

From the traces (log interpolation): average D10 1.53, D50 2.34, D60 2.39, D95 2.75 mm, Cu 1.56;
upper D10 1.46, D50 2.28; lower D10 1.61, D50 2.40. The table prints average D50 2.4 (range
2.3 to 2.4), D10 1.5 (1.4 to 1.6), Cu 1.6, D95 2.7 (2.7 to 2.8). Agreement is close; the average D50
reads 2.34, 0.06 mm below the printed 2.4 (within the steep-part bound of about 0.04 mm plus the
table's rounding). The upper's D95 (2.79) comes out above the average's only because the upper has
no extra samples between 87 and 96 percent; it is an interpolation artifact, not a reading.

## Ambiguities for the reviewer

1. Low band (0.07 to 1 mm): the three curves touch; the per-series positions rest on the order rule
   and dash gaps. Values are within 0.3 to 2.5 percent; the bound is 0.34 percent. The upper trace
   steps back by 0.06 and 0.10 percent twice (sequences 9 to 10 and 14 to 15, both at moved dash
   ends), within its bound; its left edge there runs along the 2 percent minor line.
2. Steep part: individual curves are not separable inside the band; positions by edges, bounds
   widened. The lower's top edge and the upper's bottom edge are hidden under grid lines for about
   p 61 to 76.
3. Fine ends: hidden under the #200 sieve line and merged into the 0 percent frame.
4. Coarse end: three curves merged with each other and the 100 percent frame; same point for all.

## Files

`cal-p1/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv`, `overlay-p1.png`, helpers in `helpers/` (measure_lines, geom, gridmask,
clean_view, scanline, rowruns, lowband, colruns, cruns, steep_band, make_points, check_crop,
profiles), check crops in `crops/`, the failed detect trial in `try1/`, scratch images in `scratch/`.
