# FC-18, blind reading (Claude), panel 1

Page `p0154.png` (300 dpi, unrotated, 3263 x 4558 px). Printed caption: "Figure C-18. Angle of Internal
Friction vs. Relative Density", printed page C-40. One upright panel. Axis titles as printed: y "phi_DS -
Degrees", x "D_r". The only text inside the plot is "RSM-a Soil" (upper left, around u 1050 to 1340, v
1300 to 1340); there is no legend naming the curves, so the roles below come from the line styles, as the
task describes them. What is printed agrees with `series.csv` (RSM-a soil; open circles, one solid curve,
two dashed curves); nothing to report against the index.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect` on box u 800 to 2560, v 1200 to 3370, 10 bands, x values 0, 0.1, ..., 1.0
   and y values 30, 35, 40, 45, 50. The box is inside the frame on purpose: the frame lies one grid
   spacing beyond the labelled lines on all four sides, so the outermost tracks in the box are the
   labelled lines 0 and 1.0, 30 and 50. All 16 lines detected (x = 0.1 and 0.3 in 9 of 10 bands, the
   rest in 10 of 10); 55 anchors, none predicted.
2. Affine residuals: x RMS 0.0012, max 0.0026 (0.12 and 0.26 percent of the 0 to 1 span); y RMS 0.011
   deg, max 0.022 deg (0.06 and 0.11 percent of the 30 to 50 span). Both under 0.5 percent.
3. Ink check (`piecewise --image`): every one of the 11 x and 5 y lines is verified, ink at 12 of 12
   (x) and 25 of 25 (y) positions, the ink's line within 0.7 px of the fitted line at both ends; knot
   location errors 0.50 to 1.17 px (saved in `cal-p1/knots-check.json`). Values in
   `points-p1-native.csv` are piecewise; they differ from the affine map by at most 0.002 in Dr and
   0.016 deg.
4. The scan is tilted: vertical lines lean by du/dv +0.008 to +0.015 (about 0.7 deg), horizontal lines
   by dv/du -0.007 to -0.009. The x grid is unevenly drafted: 147.5 to 159.7 px per 0.1 of Dr at the
   bottom of the plot (0.7 to 0.8 narrowest); y is even, 383 to 385 px per 5 deg.
5. Labels checked by eye (all 11 x and all 5 y, `calibration-eye-checks.csv`): every label is centred on
   its own line within 11 px, against a spacing of 147 px or more (x) and 383 px (y). The 0.9 label is
   printed about 10 px left of its line, still unambiguous. The x = 0 label is under the first vertical
   line right of the left frame, not under the frame.

### Frame beyond the labelled lines

Left frame at Dr about -0.094 (u 726 to 737 at v 1300, 750 to 761 at v 3300); right frame at Dr about
1.10 (inner edge Dr 1.096 to 1.098); top frame at 55.0 deg, bottom frame at 25.0 deg (affine
extrapolation). The frame carries no label and is not a knot. Everything right of the x = 1.0 line is
flagged `extrapolated` by the piecewise map: the three curves run to the right frame, so samples at Dr
1.05 and the right ends (Dr 1.096 to 1.097) are extrapolated over about 0.1 of Dr, one grid spacing.

## Circles (series `data`, 6 markers)

Centres from the ring's outer and inner edges on 8x to 10x crops (`crops/chk_c*.png`), checked against a
ring-contrast fit (`fit_circle.py`, agreement within 1.5 px). Ring outer diameter about 37 to 40 px.

| seq | pixel (u, v) | Dr, phi (deg) | note |
|---|---|---|---|
| 1 | 891.5, 2418.0 | 0.000, 38.22 | pair 1 left; centred on the x = 0 grid line |
| 2 | 927.5, 2538.5 | 0.023, 36.64 | single; overlaps circle 4 |
| 3 | 931.5, 2616.0 | 0.024, 35.63 | single; the lower dashed curve runs through it |
| 4 | 946.5, 2515.5 | 0.035, 36.94 | single; the solid curve crosses its top; overlaps circle 2; bound 4 px |
| 5 | 1110.0, 2413.0 | 0.140, 38.27 | pair 1 right; the solid curve runs through it |
| 6 | 2447.5, 1727.0 | 1.002, 47.06 | single; the x = 1.0 grid line passes through its centre |

There is one pair: circles 1 and 5 are joined by a horizontal line (v about 2414) running from ring to
ring, so one friction angle (38.2 to 38.3 deg) over Dr 0.00 to 0.14. No other joining line on the page.
No circle is cut by the frame. Circles 2 and 4 touch each other and form a figure-of-eight; both rings
are complete enough to centre (bound 3 and 4 px). Circle 4's opening is slightly wider (27 px) than
tall (22 px) where the solid curve and circle 2 merge with it; circle 6 is slightly taller (42 px) than
wide (37 px). Circle 1's Dr comes out 0.000 and is flagged `extrapolated x` because its centre is a
fraction of a pixel left of the 0 line.

## Curves (traces, 23 samples each)

1. `upper`: the dashed curve above the solid one. Starts at the upper right of circle 1's ring (its first
   dash emerges from the ring at u 905; it may continue under the ring) and runs to the right frame at
   v 1605 (48.6 deg at Dr 1.10). 12 dashes, about 90 to 160 px long (the last one cut by the frame), gaps
   22 to 58 px.
2. `mean`: the solid curve. Starts at the x = 0 grid line (ink meets the grid line's right edge at u
   897; it may begin under the grid line) at 36.8 deg, crosses the top of circle 4, runs through circle
   5 (pair 1 right), crosses the x = 0.3 / y = 40 intersection and the y = 45 line near Dr 0.82, and
   runs into the right frame at 46.9 deg. Slightly concave, no knee.
3. `lower`: the dashed curve below the solid one. Starts at the x = 0 grid line (u 898.5, 35.3 deg),
   its first dash runs through circle 3, and its last dash merges with the y = 45 grid line from about
   u 2560 to the right frame (45.0 deg at Dr 1.10). 11 dashes, up to 180 px long, gaps 27 to 49 px.

Sampling: left end, Dr 0.05 to 1.05 every 0.05, right end. The line is about 8 px thick across (9 px
tall in a column), so the bounds are v 3.5 to 5 px and u 3 to 4.9 px. Column centres were tracked on the
page (`track_curve.py`); each sample is a straight-line fit to clean columns within 15 px (up to 40 px
at grid crossings), on the same dash. Columns within 8 px of a vertical grid line or 10 px of a
horizontal one, and where a circle merges with the line, are not used; a sample on a grid line is read
from the line on both sides of the crossing.

Samples moved (rule 7), each with its note in `points-p1.csv`:

1. upper: Dr 0.25, 0.45, 0.65, 0.75, 0.85 fall in gaps and sit at the nearest dash end (Dr 0.246,
   0.457, 0.661, 0.740, 0.845). The Dr 0.65 sample is the start of the dash just above the y = 45 grid
   line (u 1917.5), read on the page.
2. lower: Dr 0.20, 0.35, 0.45, 0.55, 0.65, 0.85, 0.95, 1.05 fall in gaps (Dr 0.189, 0.353, 0.463,
   0.538, 0.649, 0.847, 0.943, 1.051). The Dr 0.45 sample is the start of a dash that begins on the y =
   40 grid line; its tip shows below that line (u 1611.5, v 2284), read on the page.
3. mean: Dr 0.15 (u 1126) falls where circle 5's ring merges with the line; moved 7 px right to u 1133,
   clear of the ring (Dr 0.154).

Features (rule 3): first and last point of each trace (6). Each curve rises monotonically, so its maximum
is its last point, at the right frame; no knee or kink on any of them.

## Not traced, and things to look at

1. Thin horizontal strokes (2 to 3 px thick) just below some dashes near the right side: u 2397 to 2420
   at v 1685, u 2540 to 2595 at v 1634 to 1640 (both under the upper dashed curve), u 2574 to 2598 at v
   1901 to 1904 (under the lower one). They are level, not along the curves, and do not join circles:
   print debris or a ghost stroke, not part of any series.
2. Three specks left of the x = 0 line at u 815 to 885, v 2834 to 2840: not symbols.
3. The ends at the x = 0 grid line (mean, lower) and at circle 1 (upper) could continue under the grid
   line or the ring; the first samples are where the ink is seen, with u bounds of 3 to 4 px.
4. The lower curve's right end lies on the y = 45 grid line; its centre (v 1884.5, bound 5 px) comes
   from the dash's own line and the ink showing above the grid line.
