# FC-10B, panel 1: reading notes (Claude reader, batch curves-appc-b8)

Page `packet/p0143.png` (printed C-29, PDF 143), 3263 x 4558 px. Figure printed upright, one
panel, caption "Figure C-10B. PS Loose". Series `ps-loose` (series.csv); the page prints "PS Loose"
in the box and the caption, as the index says.

## Box above the plot, as printed

```
PS Loose
Avg. Density = 24.60
Angle of Friction = 43.40
Tan Theta = .9459
Cohesion = 169.22
```

The decimal marks of 24.60, 43.40 and 169.22 look like commas in the scan; read as decimal points
(".9459" is clearly a point). atan(.9459) = 43.41 deg, consistent with the printed angle. No unit is
printed for the cohesion; it is compared in psf (read as 1692 psf, in the axis units of x 10^1, it
would be far from the drawn line, which meets the axis near 130 psf).

## Calibration (`cal-p1/`)

`calibrate_axes.py detect`, box 545 1395 2640 3790 (the plot frame only: the text box above the plot
shares the y = 800.00 line and its top edge at v ~923 is outside the box), 10 bands, x values 0 to
7000 psf every 1000 (printed 00 to 700.00), y values 0 to 8000 psf every 1000 (printed 00 to 800.00).
All 8 vertical and 9 horizontal lines detected in 10/10 bands, none predicted. Affine residual: x RMS
3.61 psf (max 8.22), y RMS 10.17 psf (max 18.50), that is 0.05 / 0.13 percent of the spans (max 0.23
percent), under the 0.5 percent limit. The piecewise ink check verifies all 17 lines (none
rejected); location errors 0.5 to 1.2 px. The grid is drafted unevenly in y: the 0 to 1000 cell is
299.6 px tall, the others 287 to 295 px; x cells 285.5 to 295 px.

By-eye label checks (`calibration-eye-checks.csv`): y 800.00, 400.00, 100.00, 00 and x 00, 100.00,
400.00, 700.00 each sit beside or under the line they are anchored to (within 7 px; spacing ~291 px).
The right frame line is the 700.00 line and the frame does not extend past it; the vertical frame
lines extend above the 800.00 line only into the text box, where nothing is labelled.

## Points (`points-p1.csv`, values in `points-p1-native.csv`, piecewise map with the page image)

1. Markers: 3 upright triangles (`triangle-up`), outlines ~33 px tall, ~37 px wide. Centres are
   centroids of the outline (vertices from the outer ink: v_c = (2 v_base + v_apex)/3); u bound 2 px
   (2.5 px for marker 2), v bound h/6 = 5.5 to 5.7 px. Values (psf): (169, 276), (2363, 2450),
   (4408, 4297).
2. Trace: the drawn straight line, 10 samples in drawing order: left end, x = 500 to 4000 every 500,
   right end. Bound 4.7 px in u and v (half the line's perpendicular thickness, 9.4 px; vertical run
   13 px at 43.75 deg). The line is straight on the page: 1085 clean columns fit a straight line
   with 0.76 px RMS. The samples at x = 1000, 2000, 3000, 4000 lie on vertical grid lines; their
   centre is taken from the line's ink 6 to 14 px either side.
3. Features: first point (= left end), last point (= right end, also the maximum), intercept.

Counts: ps-loose marker 3, trace 10, feature 3.

## Line ends and intercept

1. Left end: the line runs into the x = 0 frame line (line ink up to u 579, the frame's right edge;
   no ink left of the frame at u 560 to 567). The left end, the first point and the intercept are
   all taken where the line's centre (extrapolated from its ink right of the frame) meets the frame's
   centre line: (573.6, 3719.7) px, x = 0.1, y = 132.5 psf (bound 18.5 psf).
2. Right end: the line's ink ends at u 1837 (x = 4341 psf, y = 4264 psf), exactly at the lower left
   corner of marker 3; it does not reach that marker's centre (u 1856.8).

## Comparison with the printed values

1. Slope: least squares through the 10 trace samples (piecewise values) 0.9519 against Tan Theta
   .9459: +0.0060 (+0.64 percent; 43.59 deg against 43.41). End to end, (4263.9 - 132.5) / 4340.6 =
   0.9518. The affine map gives 0.9560 (+1.07 percent).
2. Intercept: the line meets the x = 0 axis at 132.5 psf (bound 18.5) against Cohesion 169.22:
   -36.7 psf, about 11 px on the page, well outside the bound. The least-squares intercept of the
   trace samples is 120.4 psf; the affine map puts the intercept at 117.3 psf. Every way of reading
   it, the drawn line meets the axis 35 to 50 psf below the printed cohesion.
3. Nothing was moved to agree with the printed values.

Diagnostic only (not a reading of the line): a least-squares line through the three marker centroids
has slope 0.9490 and intercept 145.5 psf. If the symbols were registered at their bounding-box middle
instead of their centroid (D-024 open question), every marker would read about 19 psf higher (5.5 px)
and that intercept would be about 164 psf, nearer the printed 169.22. This is offered as evidence
about the registration point, not as a correction.

The local slope of the trace in psf rises from 0.936 (0 to 500) to 0.972 (3500 to 4000) although
the line is straight on the page: that is the uneven drafting of the grid (piecewise map), not a
bend in the line.

## Ambiguities

1. The drawn line has no ink inside marker 1 (u 604 to 633): it stops at the symbol's lower left
   corner and resumes at its right side; no trace sample is placed in that gap. A short horizontal
   speck at u 643 to 660, v 3684 beside marker 1 is not part of the symbol or the line.
2. Marker 2's lower right corner merges with the drawn line; its right base corner is taken by
   symmetry about the apex (u bound widened to 2.5 px).
3. The line stops at marker 3's lower left corner (see above). With the line also starting at the
   frame rather than at marker 1, the line's extent does not show where the symbols are registered.

## Files

`cal-p1/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv`, `overlay-p1.png`, `notes.md`, `envhelp.py` (reader's helper: line scan,
triangle outline rows, label centres, trace samples at given x, slope and intercept), `blobcheck.py` (masks the grid and the line and lists the ink clusters left, a check that no symbol was missed), `scan.csv`
(column centres of the line), `crops/` (zoomed crops used for the reading).
