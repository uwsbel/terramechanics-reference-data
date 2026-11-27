# FC-11C, panel 1: reading notes (Claude reader, batch curves-appc-b8)

Page `packet/p0149.png` (printed C-33, PDF 149), 3213 x 4558 px. Upright, one panel, caption
"Figure C-11C. RSM Loose". Series `rsm-loose` (series.csv); the page prints "RSM Loose" in the box
and the caption, as the index says. Per Appendix C's introduction (context page p0115) the last
lettered figure is the combined plot of all tests; this one carries 10 symbols.

## Box above the plot, as printed

```
RSM Loose
Avg. Density = 58.20
Angle of Friction = 37.07
Tan Theta = .7556
Cohesion = 584.29
```

Decimal marks of 58.20, 37.07 and 584.29 look like commas in the scan; read as points. The first
digit of the cohesion is broken at its top in the scan (it reads like a "5" with a gap, the same glyph
as the 5 of 58.20); read as 5. atan(.7556) = 37.07 deg, consistent with the printed angle. Cohesion
compared in psf.

## Calibration (`cal-p1/`)

`calibrate_axes.py detect`, box 575 1395 2705 3800 (plot frame only, below the text box), 10 bands,
x 0 to 7000 psf (printed 00 to 700.00), y 0 to 8000 psf (printed 00 to 800.00). All 8 vertical lines
detected in 10/10 bands; the horizontal lines in 9/10 (their first ~300 px from the left frame are
printed dotted) or 10/10; none predicted. This page is skewed, not just rotated: the vertical lines
lean +0.014 to +0.017 px per px (the left frame runs from u ~600 at the text box to ~635 at the
bottom) while the horizontal lines fall -0.009 to -0.012 px per px to the right. Each line keeps its
own tilt in the piecewise map. Affine residual: x RMS 5.59 psf (max 15.68), y RMS 10.95 psf (max
22.48): 0.08 / 0.14 percent of the spans (max 0.22 / 0.28 percent). The piecewise ink check verifies
all 17 lines; location errors 0.55 to 1.56 px (the left frame the largest). y cells 288 to 300 px
(bottom cell the tallest); the first x cell is 297 px, the others 289 to 293 px.

By-eye label checks (`calibration-eye-checks.csv`): y 800.00, 700.00, 400.00, 00 and x 00, 200.00,
400.00, 700.00 each sit beside or under their lines (within 11 px). The top grid line (800.00) is
also the bottom edge of the text box; it is one line, dotted on the left, and the frame lines above it
belong to the text box. The bottom axis line overshoots the 700.00 frame line by about 20 px with no
label there; the 700.00 label is under the frame line.

## Points (`points-p1.csv`, values in `points-p1-native.csv`, piecewise map with the page image)

1. Markers: 10 upright triangles (`triangle-up`), 33 to 35 px tall, 35 to 39 px wide; centroids of
   the outlines. Markers 4 and 5 are stacked (the upper one's base merges with the lower one's apex;
   both outlines can be told apart): bound 2.5 / 6.5 px. Markers 9 and 10 sit one above the other
   at x ~4790 with a 2 px gap between them: normal bounds. Values (psf, x then y): (144, 882),
   (719, 841), (1751, 1836), (2484, 2653), (2488, 2722), (2931, 2731), (3813, 3005), (4687, 3828),
   (4795, 4354), (4792, 4478).
2. Trace: 11 samples, left end, x = 500 to 4500 every 500, right end. Bound 5.5 px (half the
   perpendicular thickness, 11.1 px; vertical run 14 px at 37.9 deg). The line is straight on the page:
   1120 clean columns fit with 0.72 px RMS. Samples at x = 1000, 2000, 3000, 4000 are on vertical
   grid lines (the x = 3000 one from the right side only, see below); the x = 4500 sample is where the
   line crosses the y = 4000 grid line, centred from the line's ink either side.
3. Features: first point, last point (also the maximum), intercept.

Counts: rsm-loose marker 10, trace 11, feature 3.

## Line ends and intercept

1. Left end: the line runs into the x = 0 frame line (no ink left of it). Left end, first point and
   intercept: where the line's centre, fitted on its ink at u 640 to 820 (0.57 px RMS), meets the
   frame's centre line: (635.0, 3604.4) px, x = 0.5, y = 587.3 psf (bound 20.7).
2. Right end: the line's ink ends at u 2019 to 2020 (x = 4790, y = 4202 psf), well below markers 9
   and 10 (about 30 px below the base of marker 9, the lower one) without touching them.

## Comparison with the printed values

1. Slope: least squares through the 11 trace samples 0.7543 against Tan Theta .7556: -0.0013
   (-0.17 percent; 37.03 deg against 37.07). The affine map gives 0.7544 (-0.16 percent).
2. Intercept: 587.3 psf (bound 20.7) against Cohesion 584.29: +3.0 psf, inside the bound. The
   least-squares intercept of the trace samples is 589.0 psf; with the affine map the intercept point
   reads 584.4 psf at x = -14 (the affine map does not follow the tilted left frame).
3. Nothing was moved to agree with the printed values.

Diagnostic only: a least-squares line through the 10 marker centroids has slope 0.7492 and intercept
590.0 psf.

## Ambiguities

1. The drawn line has no ink across the upper part of marker 3 (u 1124 to 1156) nor across marker 6
   (u 1453 to 1499); it resumes at the x = 3000 grid line (u ~1500 to 1505), so the x = 3000 sample is
   centred from the line's ink 6 to 14 px right of the grid line only. There is also a 2 px break
   in the line at u 1774 to 1775 with no symbol near it; the pieces either side are collinear. No
   other sample lies in a gap.
2. Marker 6: its right base corner merges with the x = 3000 grid line and is taken by symmetry about
   the apex (u bound 2.5 px).
3. Marker 7: the y = 3000 grid line (v 2879 to 2884) runs through the top of its base; apex and base
   bottom are clear (v bound 6 px).
4. Markers 4 and 5 stacked (see Points).

## Files

`cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`,
`notes.md`, `envhelp.py` (reader's helper), `blobcheck.py` (masks the grid and the line and lists the ink clusters left, a check that no symbol was missed), `scan.csv` (column centres of the line), `crops/`.
