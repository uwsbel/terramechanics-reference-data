# FC-11A, panel 1: reading notes (Claude reader, batch curves-appc-b8)

Page `packet/p0145.png` (printed C-31, PDF 145), 3213 x 4604 px. Upright, one panel, caption
"Figure C-11A. RSM Loose". Series `rsm-loose` (series.csv); the page prints "RSM Loose" in the box
and the caption, as the index says (the index's soil code RSM-a is not printed on the page).

## Box above the plot, as printed

```
RSM Loose
Avg. Density = 58.20
Angle of Friction = 35.92
Tan Theta = .7244
Cohesion = 444.69
```

Decimal marks of 58.20, 35.92 and 444.69 look like commas in the scan; read as points.
atan(.7244) = 35.92 deg, consistent with the printed angle. Cohesion compared in psf.

## Calibration (`cal-p1/`)

`calibrate_axes.py detect`, box 685 1440 2780 3830 (plot frame only, below the text box), 10 bands,
x 0 to 7000 psf (printed 00 to 700.00), y 0 to 8000 psf (printed 00 to 800.00). All 8 vertical and
9 horizontal lines detected in 10/10 bands, none predicted. Page tilt about 0.5 deg. Affine residual:
x RMS 3.89 psf (max 9.83), y RMS 9.97 psf (max 19.28): 0.06 / 0.12 percent of the spans (max 0.24
percent). The piecewise ink check verifies all 17 lines; location errors 0.5 to 1.3 px. y cells 288
to 299 px (bottom cell the tallest), x cells 290 to 295 px.

By-eye label checks (`calibration-eye-checks.csv`): y 800.00, 400.00, 100.00, 00 and x 00, 200.00,
400.00, 700.00 sit beside or under their lines (within 9.5 px; spacing ~292 px). The right frame line
is the 700.00 line; the vertical frame lines above 800.00 belong to the text box.

## Points (`points-p1.csv`, values in `points-p1-native.csv`, piecewise map with the page image)

1. Markers: 5 upright triangles (`triangle-up`), 31.5 to 35 px tall, 36 to 40 px wide; centroids of
   the outlines. u bound 2 px, v bound h/6 = 5.3 to 5.8 px. Values (psf): (726, 796), (1744, 1818),
   (2910, 2722), (3794, 2979), (4691, 3804).
2. Trace: 11 samples, left end, x = 500 to 4500 every 500, right end. Bound 4.9 px (half the
   perpendicular thickness, 9.7 px; vertical run 12 px at 35.8 deg). The line is straight on the page:
   1210 clean columns fit with 0.73 px RMS (its first 200 px sit 1 to 2 px above that global fit, so
   the left end is extrapolated from a local fit). Samples at x = 1000, 2000, 3000, 4000 are on
   vertical grid lines, centred from the line's ink 6 to 14 px either side.
3. Features: first point, last point (also the maximum), intercept.

Counts: rsm-loose marker 5, trace 11, feature 3.

## Line ends and intercept

1. Left end: the line runs into the x = 0 frame line (no ink left of it at u 690 to 702). Left end,
   first point and intercept: where the line's centre, fitted on its ink at u 717 to 900 (0.48 px
   RMS), meets the frame's centre line: (707.1, 3679.8) px, x = 0.3, y = 411.0 psf (bound 19.2).
2. Right end: the line's ink ends at u 2054 to 2055 (x = 4602, y = 3750 psf), 8 px short of the
   lower left corner of the last symbol (marker 5, centroid x = 4691) and below it; it does not touch
   that symbol. A speck at u 2057 to 2059, v 2716 to 2718 is not part of the line.

## Comparison with the printed values

1. Slope: least squares through the 11 trace samples 0.7263 against Tan Theta .7244: +0.0019
   (+0.26 percent; 35.99 deg against 35.92). The affine map gives 0.7298 (+0.75 percent).
2. Intercept: 411.0 psf (bound 19.2) against Cohesion 444.69: -33.7 psf, outside the bound (about
   10 px on the page). The least-squares intercept of the trace samples is 401.7 psf; the affine map
   gives 402.9 psf (-41.8). Every way of reading it, the drawn line meets the axis 34 to 43 psf below
   the printed cohesion.
3. Nothing was moved to agree with the printed values.

Diagnostic only: a least-squares line through the 5 marker centroids has slope 0.7220 and intercept
421.8 psf; with bounding-box-middle registration (about 18 psf higher each) about 440 psf. Not a
correction; evidence for the registration question.

## Ambiguities

1. Marker 4 is crossed at mid-height by the y = 3000 grid line; its apex (v 2910) and base (v 2936 to
   2942) are clear, so the centroid is read normally.
2. Marker 5's base has a small blob at its right corner reaching v 2706; the base bottom is taken at
   v 2705 (+-1).
3. No symbol touches or interrupts the drawn line on this figure.

## Files

`cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`,
`notes.md`, `envhelp.py` (reader's helper), `blobcheck.py` (masks the grid and the line and lists the ink clusters left, a check that no symbol was missed), `scan.csv` (column centres of the line), `crops/`.
