# FB-3, batch curves-appb-b1: reading notes (Claude, blind)

Page `p0109.png` (300 dpi, 3263 x 4558 px, a binary scan whose ink comes in blocks of about 3 px).
Printed caption "Fig. 3 E VERSUS σ3 FOR RS SOIL", printed page 6. Axis titles as printed: x
"Confining Pressure, σ3, psi", y "Dynamic Modulus, E=ρc², kips/in.²". One panel, upright. All of this
agrees with the figures index row and with `series.csv`.

## Which polyline carries which label

1. `dr99`: the upper polyline (two straight segments, rising from 2.2 to 9.7 psi). Its label, printed
   on two lines "Dense" over "Dr = 0.99" (r subscript; the "=" printed as a solid block, a dotted
   underline of specks below "0.99"), sits just right of the polyline's upper end, below the two
   symbols at 9.9 psi. Label centre (2145, 1056).
2. `dr30`: the lower polyline (two straight segments, rising from 3.9 to 13.8 psi). Its label,
   "Loose" over "Dr = 0.30", sits below the upper segment near 11 to 12 psi. Label centre (2184.5, 2739.5).

The printed texts match `series.csv` ("Dense, Dr = 0.99", "Loose, Dr = 0.30"). The assignment is not
ambiguous: each label is next to one polyline only, and the other polyline is 600 px or more away.

## Calibration (`cal-p1/`, helper `tick_cal.py`)

No grid lines: ticks only, on the bottom frame (x, rising about 24 px into the plot) and on the left
frame (y, running about 30 px into the plot); none on the top or right frames.

1. Frames, each fitted with its own tilt to the centre of its ink core every 20 px (ticks skipped):
   left u = 560.59 - 0.00329 v (rms 0.47 px), right u = 2520.66 - 0.00226 v (rms 0.59 px), bottom
   v = 3914.55 + 0.00456 u (rms 0.59 px), top v = 826.77 + 0.00623 u (rms 1.03 px, ragged ink). The
   frame is rotated by 0.13 to 0.36 degree depending on the side, i.e. slightly out of square (the top and bottom
   tilts differ by 0.0017, the left and right by 0.0010); not large, but the piecewise map keeps every
   frame line with its own tilt.
2. Frames are knots only where a printed label sits on them: x = 0 (left frame, label "0" at the
   corner), x = 14 (right frame, label "14", no tick), y = 7 (bottom frame, label "7" 12 px above it,
   no tick), y = 18 (top frame, label "18", no tick).
3. Ticks: x = 2 to 12 (6 ticks), y = 8 to 17 (10 ticks). Each tick's ink centre was measured in every
   row (x) or column (y) of the tick, 22 to 29 per tick, fitted with the tick's own tilt (straightness
   rms 0.14 to 0.46 px), and the anchor is where that line meets the frame centreline. The ticks' own
   tilts (x ticks du/dv -0.023 to +0.015; y ticks dv/du -0.020 to +0.049) scatter about the frame tilt
   by about the standard error a 24 px tick allows (about 0.01, i.e. 30 px over the 3085 px plot), so a
   tick's own tilt cannot be extended across the plot; each tick is a lone-tick knot with the direction
   of the affine map (du/dv = -0.0029 for x lines, between the left and right frames' -0.0033 and
   -0.0023; dv/du = 0.0048 for y lines), as `calibrate_axes.py` does for ticks.
4. Affine map (diagnostic), least squares on 482 anchors: x rms 0.0060 psi, max 0.034 psi (0.24 % of
   the 14 psi span); y rms 0.0051 ksi, max 0.026 ksi (0.23 % of the 11 ksi span). Both under the
   0.5 % threshold. The residuals are systematic, not noise: the tick spacing is uneven by hand
   drafting. x spacings (px per 2 psi, 0 to 14): 277.6, 279.3, 280.0, 283.4, 279.8, 283.1, 280.9. y
   spacings (px per ksi, 7 to 18): 280.3, 279.9, 276.9, 281.4, 280.4, 278.3, 282.4, 277.0, 282.1, 281.7,
   and 286.5 for the last interval (17 tick to the top frame). The top frame therefore sits about
   6.5 px (0.023 ksi) farther above the 17 tick than one mean spacing; it carries the printed 18, so it
   is kept as the 18 line and the 17 to 18 interval is read as drawn (piecewise). If the top frame were
   instead taken from the tick spacing, values near 17.8 ksi would read about 0.02 ksi higher.
5. Ink check of the piecewise knots (`tools/calibrate_axes.py`, recorded in `cal-p1/knots-check.json`):
   all 8 x lines and all 12 y lines verified, none rejected. Frames: ink at 25 of 25 positions, ink
   line within 0.2 px of the fitted line at both ends. Ticks: median stub distance 0.06 to 0.61 px.
   Location errors: frames 0.6 to 1.1 px; y ticks 0.5 to 0.66 px except y = 17 (2.0 px); x ticks
   0.5 to 1.8 px for x = 4 and 8, but 2.3 to 4.8 px for x = 2, 6, 10 and 12. Those larger errors are
   not a property of the ticks (their ink is straight within 0.14 to 0.33 px rms): the tool's stub
   check also probes 6 to 14 px below the anchor, where the 10 px thick bottom frame has a ragged lower
   edge and the label digits start, and finds ink there 3 to 6 px off the tick. The resulting x read
   bounds (0.02 to 0.07 psi) are conservative for that reason; I left the anchors at the frame
   centreline, where the tick meets the axis line, rather than move them to dodge the check.
6. Piecewise against affine values over all 42 points: largest difference 0.034 psi in x and 0.023 ksi
   in y.

## Labels that do not fit their sequence, and other printing defects

1. The y label at the second tick from the bottom is printed "3" (with a speck after it), in the
   sequence 7, 3, 9, 10, ..., 18. It is most likely an "8" whose left half did not print. The tick
   spacing confirms 8 (280.3 px above the 7 frame, 279.9 px below the 9 tick; interior spacings 276.9
   to 282.4 px), so the tick is used as the 8 knot.
2. The x label "4" is preceded by specks along v 3970 to 3974 (u 1044 to 1100) that look like "-4" or
   a dotted rule in the overview. They are dirt below the digits' baseline, not a minus sign; the
   sequence 0, 2, 4, 6 and the tick spacing confirm 4. Similar specks follow the "2".
3. Labels are typed slightly off their lines (x: -26 to +19 px; y: -12 to +20 px), always far less
   than the 280 px spacing, so every label attaches to one line without doubt. Two-digit x labels (10,
   12, 14) sit with their last digit under the line.
4. Every ink component inside the frame was listed (8-connected): apart from the two polylines with
   their symbols, one isolated circle (the upper loose symbol at 13.5 psi), the label glyphs and the
   tick tips, there are only specks of 1 to 49 px (a circle is about 850 px): (2068, 2050) an 11 x 8 px
   dash, (2253, 2300), (1546, 2577), (1612, 3464), (1372, 2236), (1079, 1809), (1425, 1730), (2354,
   2354). None is a symbol.

## Markers (12, all open circles; symbol size: outer diameter about 42 px, hole about 25 px)

Clean circles: centre = centroid of the enclosed white hole (`circles.py`; a circle fitted to the hole
boundary agrees within 0.05 px, a ring-model fit within 0.5 px). Bound 2 px.

`dr99` (6): 2.25 / 9.84 and 2.34 / 10.39 (the pair at about 2.3 psi); 4.89 / 13.91 and 4.90 / 13.87
(the overlapping pair); 9.86 / 17.67 and 9.87 / 17.82 (two touching circles at 9.9 psi). Values are
psi / ksi from `points-p1-native.csv`.

`dr30` (6): 3.92 / 7.46, 3.99 / 7.53 and 4.01 / 7.24 (three symbols at about 4 psi); 5.98 / 9.46;
13.49 / 12.87 and 13.48 / 13.16.

Overlapping symbols, each recorded as two markers because they can be told apart:

1. Dense, 4.9 psi: one double-outlined blob, 42.5 px wide and 47.5 px tall with a hole 22 x 17 px
   (a single circle is 41 x 41 with a 25 x 25 hole). A two-ring model (annulus 12.5 to 21 px, fitted
   on the clean circles; `ringfit.py`) puts two circles 9.3 px apart, almost vertically: (1235.25,
   1987.00) and (1236.00, 1996.25). The two-ring model mismatches 4.3 % of the judged pixels, one ring
   21.6 %. Bounds widened to 4 px (u) and 5 px (v), about half their separation, instead of the
   protocol's default of half the symbol size (about 21 px): the model separates them better than that,
   and a 21 px bound would make them indistinguishable from each other. An adjudicator who prefers the
   default can widen them; the centres do not change.
2. Loose, 4 psi: three symbols. The lowest (C, 4.01 / 7.24) is clean. Above it, two circles overlap
   (A upper, B lower left, 22 px apart): B's ring crosses A's hole, and the loose line runs over the
   right side of both rings. Two-ring model: A (1103.75, 3770.50), B (1094.00, 3789.75), mismatch
   6.1 %. Bounds 4 px. All three sit on or at the end of the loose line, so their series is not in
   doubt.

No symbol's group is unclear: the two polylines are 400 px or more apart wherever there are symbols.

## Traces (`trace.py`, `merge_ends.py`, `build_points.py`)

Each polyline is two straight segments. Every segment was traced on its ink every 2 px (profile across
the line, centre of the dark run) and fitted with a straight line: thickness 8.2 to 9.6 px, straightness
rms 0.32 to 0.76 px. Trace bounds are half the measured thickness: dense 4.1 px (lower segment) and 4.8
px (upper), loose 4.5 px and 4.6 px.

Samples, in drawing order from the left end: the left end, every integer psi that falls on clean line
ink, the ink ends on either side of the symbol at the vertex, and the right end.

1. Ends next to a symbol are the last position, walking along the centreline towards the symbol,
   where the ink across the line is still the line alone (no wider than the line + 3 px, centred
   within 2 px). They are on the line's ink just before it merges into the ring, never on the ring.
2. The loose line's right end (13.76 psi, 13.09 ksi) is a free, rounded tip short of the right frame
   (frame at u 2513, tip at u 2483); the sample is the last ink on the centreline. It extends 0.27 psi
   beyond the last loose symbols (13.48 to 13.49 psi).
3. The vertices are hidden under symbols and are therefore `feature` points only, not trace samples
   (rule 7: a trace sample is on the drawn line's ink). Each is the intersection of its two fitted
   segments. Dense vertex (1246.9, 1990.9) = 4.98 psi, 13.89 ksi, under the overlapping pair, 11 px
   right of the pair's centres (segments meet at 13.4 degrees). Loose vertex (1394.2, 3233.3) = 6.05
   psi, 9.46 ksi, inside the white hole of the 6 psi circle, where no line ink is drawn, 10 px right of
   its centre (20.4 degrees). The integer psi under each vertex symbol (dense x = 5, loose x = 6) falls
   in that gap and has no sample.
4. Loose lower segment, x = 4 skipped: from v 3814 to 3762 the line runs over the rings of the
   overlapping circles A and B, and x = 4 falls at v 3807, on B's ring. The segment's left end
   (3.93 psi) is where its ink meets the upper left of circle C; the clean stretch between C and B is
   only v 3814 to 3828.
5. Dense lower segment: the line touches the right side of the upper circle at 2.3 psi (v 2976 to
   2986); no sample there. Its left end (2.21 psi, 9.94 ksi) is where it meets the top of the lower
   circle at 2.3 psi.
6. Dense upper segment: its right end (9.73 psi, 17.62 ksi) is where it meets the lower left of the
   lower circle at 9.9 psi; the line does not continue to the upper circle.
7. Segment slopes (from the fitted lines, piecewise map): dense 1.44 then 0.79 ksi per psi; loose 1.00
   then 0.47 ksi per psi.

A drafting observation, for whoever uses the lines: the authors' segments do not pass through the
symbol centres. The dense lower segment passes 12.8 px from the lower 2.3 psi circle and 10.6 px from
the 4.9 psi pair; the dense upper segment 9.4 px from that pair and 6.2 px from the lower 9.9 psi
circle; the loose lower segment 20.8 px from C (it only grazes C's outline) and 17 px from A and B; the
loose upper segment 7.4 px from the 6 psi circle and passes between the two 13.6 psi circles (20 px and
41 px). The lines are drawn near the symbols, not through them, so the polyline and the markers carry
slightly different information; the vertices sit about 0.07 to 0.08 psi to the right of their symbols.

## Counts

| series | marker | trace | feature |
|---|---|---|---|
| dr99 | 6 | 10 | 4 (first, vertex, last, label) |
| dr30 | 6 | 12 | 4 (first, vertex, last, label) |

The `last` features are also each trace's maximum (both traces rise monotonically).

## Files

`cal-p1/calibration.json`, `cal-p1/anchors.csv`, `cal-p1/knots-check.json`, `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv` (piecewise, `--image`), `overlay-p1.png`, `segments.json`,
`labels.json`, helpers `tick_cal.py`, `knot_check.py`, `trace.py`, `merge_ends.py`, `circles.py`,
`ringfit.py`, `build_points.py`, `eye_checks.py`, and the zoomed crops in `crops/`.
