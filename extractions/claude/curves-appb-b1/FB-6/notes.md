# FB-6 (p0112.png), panel 1: notes of the Claude reading

Pixel coordinates are those of `packet/p0112.png` (3263 x 4558, u right, v down). Values in native units:
x = confining pressure sigma3 (psi), y = modulus E = rho c^2 (kips/in.^2).

## What the page prints

1. Caption: "Fig. 6 E VERSUS sigma3 FOR RC SOIL", printed page 9. The page numbers the figure "Fig. 6", not
   "Fig. B-6"; the id FB-6 is kept as given.
2. Axis titles: "Modulus, E=rho c^2, kips/in.^2" (y) and "Confining Pressure, sigma3, psi" (x).
3. Two polylines, each with its printed label to the right of its upper end:
   - upper, steeper polyline: "Dense / Dr = 0.82" (r subscript; label ink box u 2041 to 2342, v 1052 to 1169),
     series `dr82`;
   - lower polyline: "Loose / Dr = 0.02" (label ink box u 2021 to 2324, v 2640 to 2747), series `dr02`.
   Both agree with `series.csv`.
4. Every symbol is an open circle (outer radius about 20.6 px, hole radius about 12 px).

## Calibration (`cal-p1/`, helper `helpers/tick_cal.py`)

1. No grid lines. Ticks only inside the left frame (y = 7 to 27) and inside the bottom frame (x = 2 to 12);
   none on the top or right frame (searched 9 to 20 px either side of all four frame lines). The labels 0
   and 14 sit at the left and right frame lines, 5 and 29 at the bottom and top frame lines; those four
   frame lines are knots.
2. The frame is skewed: left frame 1.786 deg from vertical, right 1.708 deg, top 1.468 deg from
   horizontal, bottom 1.592 deg (each fitted over its whole length, 357 to 630 samples, RMS 0.54 to
   0.71 px, bow under 1 px). The two frame lines of each axis are not parallel, so each tick line has its
   own tilt, interpolated by value between the two frame lines of its axis (x: du/dv 0.03117 at x = 0 to
   0.02982 at x = 14; y: dv/du -0.02779 at y = 5 to -0.02563 at y = 29). Each tick's position is its stub
   ink (6 px off the frame centre line to 2 px short of its end) fitted with that tilt; its foot on the
   frame centre line is an anchor carrying both values, and a second anchor 22 px along the stub gives
   the line its tilt in `calibrate_axes.py piecewise` and puts the ink check on the stub.
3. The stubs' own tilts were fitted too (in `calibration.json`, `ticks`): y stubs -0.021 to +0.010
   (mean -0.005), x stubs 0.018 to 0.064 (mean 0.046), against 0.026 to 0.031 from the frames. The ticks
   were not drawn square to the frame, and a tilt from 30 px of ink carried across 1900 to 3200 px of plot
   would move a line by 40 px or more, so the stubs' tilts are reported, not used. Over a stub's 22 px
   the two tilts differ by under 0.8 px.
4. The x = 2 tick is under a plotted circle sitting on the bottom frame (the lowest loose symbol, centre
   (1000.0, 4001.4)). It shows only inside that circle's hole, as a 5 px wide vertical bar 18 to 28 px
   above the frame centre line, u about 996.7. It is anchored there (15 and 31 px up the tick), so the ink
   check reads the visible bar, not the ring. Its position is 0.15 px from the midpoint of the x = 0
   frame line and the x = 4 tick, which supports reading the bar as the tick.
5. Ink check (`cal-p1/knots-check.json`, the tool's own check): all 8 x lines (0, 2, 4, ..., 14) and all
   13 y lines (5, 7, ..., 29) verified, none rejected, none predicted. Location errors 0.5 to 1.2 px
   (largest: y = 25, 1.2 px; x = 0, 0.98 px).
6. Tick spacing: 133.80 px per psi, 133.38 px per ksi. Tick feet against a straight line in value: within
   1.1 px on x, within 2.0 px on y (y = 19: +2.0, y = 9: -1.8). Frames against the tick regression:
   x = 0 +1.5 px, x = 14 +2.2 px, y = 5 -1.3 px, y = 29 +3.9 px. The top frame (29) is the least regular:
   the 27 to 29 interval is 261 px against about 267 for the others. Only the top dense symbol (y about
   27.2) lies in that interval; reading it with the regression instead of the frame would change it by
   about 0.01 ksi.
7. Affine diagnostic (least squares on 21 anchors with both values: tick feet and corners): RMS residual
   0.0078 psi in x and 0.0115 ksi in y; max 0.0176 psi (0.13 percent of the 14 psi span) and 0.0285 ksi
   (0.12 percent of the 24 ksi span), all under the 0.5 percent limit. Piecewise minus affine over all
   points: at most 0.015 psi and 0.020 ksi. No point lies beyond the outermost verified line.

## Printed labels (`calibration-eye-checks.csv`, 6 per axis)

Every label 0, 2, ..., 14 and 5, 7, ..., 29 fits its printed sequence and its tick or frame line; none is
misprinted. Labels are typed and placed loosely: y labels sit from 3 px above (29) to 25 px below their
lines (25 is printed about 25 px low, its digits wholly below its tick; 23, 19, 13, 11, 9 are 10 to 23 px
low), 5 sits about
9 px above the bottom frame, 0 about 9 px left of the left frame, 8 about 10 px right of its tick, 14
about 4 px right of the right frame. In every case the tick spacing confirms the value, and the
calibration anchors on the ticks and frame lines, not on the label positions.

## Markers (13): 7 dense, 6 loose

1. Centres from circles fitted to the inner (hole) and outer edges of each ring
   (`helpers/circle_centers.py`); for the single circles the two fits agree within 1.4 px. A search for enclosed white holes
   inside the frame finds every circle below and nothing else except letters and digits of the labels;
   the dense circle at (1034.2, 3308.7) has a ring broken at the bottom, so its hole is open, and was
   found by eye.
2. Series by the line each circle sits beside: every dense circle is 8 to 87 px from the dense polyline
   and 280 px or more from the loose one; every loose circle is 15 to 45 px from the loose polyline and
   300 px or more from the dense one. No symbol's group is in doubt.
3. Loose, near (1960, 2674): two overlapping circles, centres about 16 px apart vertically, told apart by
   three white areas (the upper circle's hole above the lower ring, the part of both holes, the lower
   circle's hole below the upper ring). Recorded as two markers, (1960.3, 2666.5) and (1959.7, 2682.3),
   bound 2.5 px in u and 3 px in v; y 14.99 and 14.87 ksi at x 9.51 and 9.50 psi.
4. Loose, lowest symbol (1000.0, 4001.4): sits on the bottom frame line, with the x = 2 tick inside its
   hole; bound 3 px.
5. Dense (1034.2, 3308.7): the dense line runs along the right side of its ring; bound 2.5 px. Loose
   (997.6, 3942.3): the loose line crosses the right side of its ring; bound 2.5 px.

## Polylines

1. Each group's line is two straight segments (`helpers/trace_lines.py`): row-by-row ink centres, rows
   within 23 px of a circle centre set aside, break row by least squares, robust refit. Residuals: dense
   0.51 and 0.73 px RMS, loose 0.57 and 0.65 px RMS, all under 2 px max. Line thickness about 7.6 to
   8.5 px, so trace bounds are 3.8 to 4.2 px (half the thickness).
2. Vertices: dense (1321.8, 2425.2), x 4.80 psi, y 16.93 ksi (slope change du/dv -0.316 to -0.505);
   loose (1338.8, 3429.1), x 4.70 psi, y 9.39 ksi (du/dv -0.630 to -0.834). The loose slope change is
   gentle, so its vertex is the least certain point of the two lines along the line direction, though
   it stays on the ink.
3. Dense ends: both free. Lower end (999.0, 3448.5), x 2.15, y 9.32; upper end (1978.0, 1116.5),
   x 9.99, y 26.60, which is also the trace's maximum. The last 15 rows of the upper end sit 2 to 3 px
   left of the fitted segment (an oblique pen end); the end point follows the ink.
4. Dense gaps: the line stops at the ring of the circle at (1023.0, 3401.0) and resumes below it (no line
   ink inside the hole), and has a 3-row break (v 3328 to 3330) just below the circle at (1034.2,
   3308.7). No trace sample falls in either.
5. Loose ends: both on rings. The line runs from its vertex down through the right side of the ring at
   (997.6, 3942.3) and the 18 px neck between the two lowest circles (its ink centres there follow the
   fitted line within 1 px), and ends in the top of the ring at (1000.0, 4001.4); at the top it ends in
   the lower-left of the ring of the lower circle of the pair (1959.7, 2682.3). Neither line continues
   inside a hole or past a ring. First and last points are taken on the fitted centre line where it meets
   the ring's outer edge: (989.6, 3983.6), x 1.96, y 5.31; and (1947.6, 2699.0), x 9.41, y 14.75. Bound
   4.2 px across and 5.2 px along v, for the uncertain end.
6. Trace samples: the left end, every integer psi between (dense 3, 4; loose 2, 3, 4), the vertex, every
   integer psi after (5 to 9 for both), the right end; each one moved onto the ink centre of its row.
   The loose sample at 2 psi lies on the neck, 8.6 px from the first point and 27 px or more from both
   circle centres.

## Other ink, not data

Specks and dotted trails inside the frame: a dash right of the dense circle at (1950.4, 1282.0) followed
by a row of dots at v about 1298 (u 2126 to 2320); dots at v about 2575 to 2590 (u 1540 to 1590 and 2280
to 2425); a speck at (1933, 2684) just left of the loose pair; a speck at (2251, 2752) below the loose
label; isolated specks elsewhere (largest under 120 px, a circle's ring is about 900 px). None is shaped
like a symbol.

## Files

`cal-p1/anchors.csv`, `cal-p1/calibration.json`, `cal-p1/knots-check.json`, `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv` (piecewise map, `--image`), `overlay-p1.png`; helpers and crops
under `helpers/` and `crops/`.
