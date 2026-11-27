# FC-11B, panel 1: reading notes (Claude reader, batch curves-appc-b8)

Page `packet/p0146.png` (printed C-32, PDF 146), 3213 x 4558 px. Upright, one panel, caption
"Figure C-11B. RSM Loose". Series `rsm-loose` (series.csv); the page prints "RSM Loose" in the box
and the caption, as the index says.

## Box above the plot, as printed

```
RSM Loose
Avg. Density = 58.30
Angle of Friction = 37.38
Tan Theta = .7641
Cohesion = 785.77
```

Decimal marks of 58.30, 37.38 and 785.77 look like commas in the scan; read as points.
atan(.7641) = 37.38 deg, consistent with the printed angle. Cohesion compared in psf.

## Calibration (`cal-p1/`)

`calibrate_axes.py detect`, box 630 1365 2730 3765 (plot frame only, below the text box), 10 bands,
x 0 to 7000 psf (printed 00 to 700.00), y 0 to 8000 psf (printed 00 to 800.00). All 8 vertical and
9 horizontal lines detected in 10/10 bands, none predicted. Page tilt about 0.4 deg. Affine residual:
x RMS 3.48 psf (max 7.23), y RMS 10.90 psf (max 22.55): 0.05 / 0.14 percent of the spans (max 0.28
percent). The piecewise ink check verifies all 17 lines; location errors 0.5 to 1.2 px. y cells 287
to 299 px (bottom cell the tallest).

By-eye label checks (`calibration-eye-checks.csv`): y 800.00, 400.00, 100.00, 00 and x 00, 200.00,
400.00, 700.00 each sit beside or under their lines; the 700.00 label is printed about 18 px left of
the right frame line, which is still unambiguous (spacing 290 px). The frame does not extend past
the 700.00 line; the vertical frame lines above 800.00 belong to the text box.

## Points (`points-p1.csv`, values in `points-p1-native.csv`, piecewise map with the page image)

1. Markers: 5 upright triangles (`triangle-up`), 33 to 35 px tall, 36 to 39 px wide; centroids of
   the outlines. Two stacked pairs: pair A at x ~2480 (markers 2 lower, 3 upper) and pair B at x
   ~4795 (markers 4 lower, 5 upper). In each pair the upper symbol's base touches or overlaps the
   lower symbol's apex, but both outlines can be told apart (both apexes and both bases are seen),
   so each pair is two markers, with u bound 2.5 px and v bound 6.5 px (h/6 = 5.5 plus 1 px for the
   overlap). Marker 1 alone: bound 2 / 5.5 px. Values (psf, x then y): (125, 877), (2476, 2658),
   (2479, 2723), (4796, 4356), (4795, 4473).
2. Trace: 10 samples, left end, x = 500, 1000, 1500, 2000, 3000, 3500, 4000, 4500, right end. No
   sample at x = 2500: it falls at u 1384, inside the gap the drawn line leaves across pair A (no
   line ink at u ~1359 to 1397). Bound 5.2 px (half the perpendicular thickness, 10.4 px; vertical
   run 13 px at 36.9 deg). The line is straight on the page: 1148 clean columns fit with 0.83 px RMS
   (local fits near the two ends have slightly smaller slopes, -0.744 and -0.745 px/px, than the
   global -0.752, so the ends are taken from local fits). Samples at x = 1000, 2000, 3000, 4000 are on
   vertical grid lines, centred from the line's ink 6 to 14 px either side.
3. Features: first point, last point (also the maximum), intercept.

Counts: rsm-loose marker 5, trace 10, feature 3.

## Line ends and intercept

1. Left end: the line runs into the x = 0 frame line through a short stub between the frame and
   marker 1 (no ink left of the frame). Left end, first point and intercept: where the line's
   centre, fitted on its ink at u 747 to 950 (0.52 px RMS), meets the frame's centre line:
   (653.9, 3486.0) px, x = -0.3, y = 807.4 psf (bound 19.9). The stub's own centre agrees within
   1.6 px.
2. Right end: the line's ink ends at u 2038 to 2040 (x = 4734, y = 4395 psf), 4 px short of the left
   side of marker 4 (the lower symbol of pair B), without touching it.

## Comparison with the printed values

1. Slope: least squares through the 10 trace samples 0.7580 against Tan Theta .7641: -0.0061
   (-0.80 percent; 37.16 deg against 37.38). The affine map gives 0.7583 (-0.76 percent).
2. Intercept: 807.4 psf (bound 19.9) against Cohesion 785.77: +21.6 psf, just outside the bound
   (about 6 px on the page). The least-squares intercept of the trace samples is 798.9 psf; the
   affine map gives 810.3 psf (+24.5).
3. Nothing was moved to agree with the printed values.

Diagnostic only: a least-squares line through the 5 marker centroids has slope 0.7555 and intercept
800.7 psf. Unlike FC-10B, FC-10C and FC-11A of this batch, here the drawn line meets the axis above
the printed cohesion and is less steep than the printed tan; a bounding-box-middle registration of
the symbols (about 19 psf higher each) would move the marker fit further from the printed cohesion
(about 820 psf), not nearer.

## Ambiguities

1. The two stacked pairs (see Points); the identity of each symbol of a pair is not in question (one
   series), only the overlap of outlines, covered by the widened bounds.
2. The drawn line has no ink across marker 1 (a stub joins the frame to its lower left corner, and
   the line resumes at its right side) nor across pair A (u ~1359 to 1397).
3. Specks at u 2080 to 2089 to the right of pair B and a short dash right of pair A at u 1428 to 1448,
   v 2952 to 2956 (the "-" seen on the page beside the pair) are not symbols.

## Files

`cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`,
`notes.md`, `envhelp.py` (reader's helper), `blobcheck.py` (masks the grid and the line and lists the ink clusters left, a check that no symbol was missed), `scan.csv` (column centres of the line), `crops/`.
