# FC-10C, panel 1: reading notes (Claude reader, batch curves-appc-b8)

Page `packet/p0144.png` (printed C-30, PDF 144), 3213 x 4604 px. Upright, one panel, caption
"Figure C-10C. PS Loose". Series `ps-loose` (series.csv); the page prints "PS Loose" in the box and
the caption, as the index says. Per Appendix C's introduction (context page p0115) the last figure of
a lettered series is the combined plot of all tests; this one carries 9 symbols.

## Box above the plot, as printed

```
PS Loose
Avg. Density = 25.40
Angle of Friction = 43.70
Tan Theta = .9558
Cohesion = 359.69
```

Decimal marks of 25.40, 43.70 and 359.69 look like commas in the scan; read as points.
atan(.9558) = 43.71 deg, consistent with the printed angle. Cohesion is compared in psf (the drawn
line meets the axis near 355 psf, so the axis units of x 10^1 do not apply to it).

## Calibration (`cal-p1/`)

`calibrate_axes.py detect`, box 468 1455 2555 3865 (plot frame only, below the text box), 10 bands,
x 0 to 7000 psf (printed 00 to 700.00), y 0 to 8000 psf (printed 00 to 800.00). All 8 vertical and
9 horizontal lines detected in 10/10 bands, none predicted. The page is tilted about 0.5 deg (the
horizontal lines drop 0.0081 to 0.0103 px per px to the right). Affine residual: x RMS 4.12 psf (max
8.39), y RMS 11.18 psf (max 22.46): 0.06 / 0.14 percent of the spans (max 0.28 percent). The
piecewise ink check verifies all 17 lines; location errors 0.5 to 1.3 px. The y cells are uneven
(bottom cell 299 px, 4000 to 5000 cell 288 px).

By-eye label checks (`calibration-eye-checks.csv`): y 800.00, 400.00, 100.00, 00 and x 00, 100.00,
400.00, 700.00 sit beside or under their lines (within 7.3 px). The bottom axis line continues as a
dotted stroke past the 700.00 frame line to u ~2620; it carries no label and does not affect the x
calibration. The vertical frame lines above the 800.00 line belong to the text box.

## Points (`points-p1.csv`, values in `points-p1-native.csv`, piecewise map with the page image)

1. Markers: 9 upright triangles (`triangle-up`), 33 to 35 px tall, 37 to 39 px wide; centroids of
   the outlines (v_c = (2 v_base + v_apex)/3). u bound 2 px (2.5 px where a corner is hidden),
   v bound h/6 = 5.5 to 6.5 px. Values (psf, x then y): (124, 229), (716, 1036), (1441, 1874),
   (2183, 2664), (2332, 2414), (2911, 3274), (3619, 3907), (4368, 4273), (4371, 4552).
2. Trace: 10 samples, left end, x = 500 to 4000 every 500, right end. Bound 5.4 px (half the
   perpendicular thickness, 10.9 px; vertical run 15 px at 43.6 deg). The line is straight on the
   page: 1086 clean columns fit with 0.93 px RMS. Samples at x = 1000, 2000, 3000, 4000 are on
   vertical grid lines, centred from the line's ink 6 to 14 px either side.
3. Features: first point, last point (also the maximum), intercept.

Counts: ps-loose marker 9, trace 10, feature 3.

## Line ends and intercept

1. Left end: the line runs into the x = 0 frame line (no ink left of it). The left end, first point
   and intercept are where the line's centre, fitted on its ink at u 495 to 600 (0.66 px RMS), meets
   the frame's centre line: (485.6, 3713.5) px, x = -0.2, y = 355.0 psf (bound 21.0).
2. Right end: the line's ink runs into the lower left corner of marker 9 (the upper of the two
   symbols at x ~4370) and is not seen beyond it; the symbol's interior is white. End taken where the
   line's centre meets the bottom of that symbol's base: (1750.5, 2509.7) px, x = 4321, y = 4509 psf.
   It stops about 15 px (50 psf) left of that symbol's centroid.

## Comparison with the printed values

1. Slope: least squares through the 10 trace samples 0.9613 against Tan Theta .9558: +0.0055
   (+0.58 percent; 43.87 deg against 43.71). The affine map gives 0.9633 (+0.79 percent).
2. Intercept: 355.0 psf (bound 21.0) against Cohesion 359.69: -4.7 psf, inside the bound. The
   least-squares intercept of the trace samples is 344.6 psf; the affine map gives 345.9 psf
   (-13.8).
3. Nothing was moved to agree with the printed values.

Diagnostic only: a least-squares line through the 9 marker centroids has slope 0.9616 and intercept
333.7 psf. If the symbols were registered at their bounding-box middle (about 19 psf higher each) that
intercept would be about 353 psf. Not a correction; evidence for the registration question.

## Ambiguities

1. The drawn line is interrupted at marker 2 (no ink across the symbol, u ~688 to 710) and has a
   short break at the lower right corner of marker 7 (u ~1551 to 1564). No trace sample is placed in
   either gap.
2. Marker 2: its base lies on the y = 1000 grid line and the drawn line passes through its lower
   corners; the base bottom is taken 8 px below the hollow interior (the base stroke of the clean
   symbols is 7 to 9 px) and the corners by symmetry about the apex; v bound widened to 6.5 px.
3. Marker 7: the apex touches the underside of the y = 4000 grid line (apex v taken 2658 +-1) and
   the lower right corner touches the drawn line; v bound 6 px.
4. Markers 8 and 9 sit one above the other at x ~4370 (u 1764 and 1765), both clearly separate
   symbols. Marker 9's left base corner is merged with the end of the drawn line.
5. Marker 6 sits 4 px left of the x = 3000 grid line; its outline is clear.

## Files

`cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`,
`notes.md`, `envhelp.py` (reader's helper), `blobcheck.py` (masks the grid and the line and lists the ink clusters left, a check that no symbol was missed), `scan.csv` (column centres of the line), `crops/`.
