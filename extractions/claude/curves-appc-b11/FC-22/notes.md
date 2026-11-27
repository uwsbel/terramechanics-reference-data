# FC-22, blind reading (Claude), batch curves-appc-b11

Page `p0158.png`, printed page C-44. Caption as printed: "Figure C-22. Angle of Internal Friction vs.
Relative Density". In-plot text: "RSM-b Soil". Axis titles: y "phi_DS - Degrees", x "D_r". One upright
panel. There is no printed legend; the series ids are those of `series.csv`, and the page agrees with
them (one soil, RSM-b; circles, one solid curve, two dashed curves).

## Which curve is which

1. `mean`: the solid line. Ink from Dr -0.003 (it starts just left of the Dr = 0 grid line) to Dr 1.005
   (it ends just right of the Dr = 1.0 grid line); phi 38.22 to 51.04 deg. It is interrupted by the two
   circles (the circles are hollow, the line is not drawn through them) and has a small pen break at
   u 2073 to 2079 (Dr about 0.79): a 1 to 2 px gap with a 4 px offset (crops/jog.png).
2. `upper`: the dashed line above the solid one, 10 dashes. Starts at the Dr = 0 grid line (no ink left
   of it) at phi 39.42, ends at the Dr = 1.0 grid line (no ink right of it) at phi 52.10. About 1.1 to
   1.3 deg above the solid line.
3. `lower`: the dashed line below the solid one, 9 dashes. Ink from Dr -0.005 (just left of the Dr = 0
   line) at phi 36.92 to the Dr = 1.0 grid line (no ink right of it) at phi 49.74. About 1.3 to 1.4 deg
   below the solid line.
4. `data`: two open circles, both single (no horizontal joining line on this figure, so no pairs):
   circle 1 at Dr 0.537, phi 45.04, centred on the phi = 45 grid line, which cuts through it, and on the
   solid line (its centre is about 7 px, 0.09 deg, above the solid line's centre there); circle 2 at
   Dr 0.960, phi 50.55, on the solid line near its right end. Neither is cut by the frame. Ring outer
   radius about 20 px, inner about 12 px. Centres from least-squares circles fitted to the inner and outer
   ring edges (rays landing on the grid line or on the curve dropped); bound 3 px (widened from 2 px for
   the overlaps). A search of the whole frame for enclosed hollows found no other circle
   (crops/holes_sheet.png: every other hit is a cell corner closed by a curve or a grid line).

No knee on any curve: the slope changes gradually, so each trace carries features for its first and last
points only (the last point is also its maximum; all three curves rise monotonically). The curves are not
straight: on the solid line phi rises about 0.57 to 0.63 deg per 0.05 of Dr near Dr 0, about 0.70 near
Dr 0.6 to 0.7, and about 0.6 near Dr 1.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect` with box 770 1450 2500 3360, x values 0 to 1.0 by 0.1, y values 30 to 50
   by 5, 10 bands. The box lies inside the frame on purpose (see the frame below) so that the outermost
   tracks are the labelled lines Dr 0 and 1.0, phi 50 and 30. All 11 vertical and 5 horizontal lines
   detected in 10 of 10 bands; none predicted.
2. Affine residuals: x rms 0.0010 (0.10 percent of the 0 to 1 span), max 0.0028 (0.28 percent); y rms
   0.013 deg (0.07 percent of the 30 to 50 span), max 0.022 deg (0.11 percent).
3. Ink check of the piecewise map (`--image`): all 16 lines verified; 12 of 12 ink positions on each
   vertical line, 25 of 25 on each horizontal one; reader line minus ink line at most 1.0 px; location
   errors 0.56 to 1.27 px.
4. Labels checked by eye: y 50, 40, 30 on zoom-3 crops (45, 35 at half scale); x 0, 0.5, 1.0 on zoom-3
   crops (0.1 to 0.9 on the native-scale label strip). Every label sits on or under its own line; the 50
   label is printed about 8 px high of its line, the 1.0 label about 6 px right, both far less than the
   385 px and 155 px spacings (`calibration-eye-checks.csv`).
5. Drafting: the vertical grid lines are unevenly spaced, 151 to 160 px per 0.1 of Dr (about plus or
   minus 3 percent); the horizontal ones 382 to 385 px per 5 deg. The grid is tilted about 0.6 deg
   (vertical lines lean right going down). The piecewise map reads values between the drawn lines; the
   largest piecewise minus affine difference is 0.002 in Dr and 0.024 deg.

## The frame beyond the labelled lines

The frame extends one unlabelled interval past the labelled grid on every side: left frame at Dr about
-0.097, right frame at about 1.098, top frame at phi about 55.0, bottom frame at about 25.0 (measured on
the frame lines with this reader's map). These values are not printed, so the frame lines are not knots.

Consequences in `points-p1-native.csv` (`cal_model`):

1. Values above phi 50 are extrapolated in y from the 45 to 50 interval, at most 2.1 deg past the 50 line
   (upper dashed from Dr about 0.85, circle 2, the solid line from Dr about 0.94). The horizontal
   spacings agree within 1 percent and the same extrapolation puts the top frame at 55.0, so the
   extrapolation should be good to a few hundredths of a degree.
2. The ends at Dr -0.003 and -0.005 and the samples at or past Dr 1.0 are flagged extrapolated in x; all
   are within 0.006 of the outer labelled lines.

## Trace samples

1. Method: column-wise ink centre of each curve (dark below 140; columns on a grid line masked; runs taller
   than 13 px rejected), then a local straight-line fit over plus or minus 20 px of ink inside the same
   ink interval. Ink intervals (dash ends, junctions with the circle outlines) were read on zoom-3 and
   zoom-6 crops and refined to the outermost ink column; the end sample is the centre of the line's end
   cap, about 2 px inside that column. Sample positions at every 0.05 of Dr come from the piecewise x
   map. Helpers in `helpers/` (centerline.py, dashends.py, sample.py, circles2.py).
2. A sample at the crossing with a grid line takes its centre from the ink on either side (noted per row).
3. Bounds: trace samples u 2 px, v 4 px (the line is about 9 px tall measured vertically, 7.5 px across);
   ends u 3 px, v 4 px; an end hidden under the Dr = 0 or 1.0 grid line (upper left end, upper and lower
   right ends) u 4 px, covering the line width.
4. Samples that fall in a gap moved to the nearest end on the ink (rule 7), each with its note and distance:
   upper Dr 0.15, 0.25, 0.50, 0.60, 0.85, 0.95; lower Dr 0.10, 0.35, 0.50, 0.60, 0.70, 0.85, 0.95; solid
   line Dr 0.55 (3 px, to where the line leaves circle 1) and Dr 0.95 (8 px, to where the line meets
   circle 2).
5. Coinciding ends: the upper's left end is at Dr 0.000, so it stands for the Dr 0.00 sample; the upper's
   and lower's right ends are at the Dr = 1.0 line, so they stand for Dr 1.00. The solid and lower lines
   start a few px left of the Dr = 0 line and the solid line ends 8 px past the Dr = 1.0 line, so those
   carry both an end and a 0.00 or 1.00 sample.
6. The upper's first dash ends just above the phi = 40 grid line (its lower edge merges with the grid line
   at u 935 to 945); its end was placed from the crop at u 943, not from the merged ink.

## Specks and other marks

1. Specks of dirt near the upper dashed line at about (1645 to 1649, 1969) and (1252 to 1258, 2220): not
   part of any dash; not read.
2. The "RSM-b Soil" text interrupts the Dr 0.1 and 0.2 grid lines near the top of the plot; outside the
   calibration box, no effect.

## Counts

| series | marker | trace | feature |
|---|---|---|---|
| data | 2 | 0 | 0 |
| mean | 0 | 23 | 2 |
| upper | 0 | 21 | 2 |
| lower | 0 | 22 | 2 |

74 rows in all.
