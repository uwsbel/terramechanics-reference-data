# FB-4 (Fig. B-4, p0110.png, printed page 7): Claude reading, panel 1

Printed caption: "Fig. 4 E VERSUS sigma_3 FOR PS SOIL". Axes: x "Confining Pressure, sigma_3, psi",
0 to 14; y "Modulus, E = rho c^2, kips/in.^2", 0 to 10. One panel, upright, open circles only.

## Series and labels

1. `dr86`: the upper polyline. Its printed label "Dense / D_r = 0.86" (two lines, ink block u 2045 to
   2360, v 1313 to 1447) sits just right of the polyline's right end. Matches series.csv.
2. `dr22`: the lower polyline. Its printed label "Loose / D_r = 0.22" (ink block u 2044 to 2357, v
   1900 to 2027) sits just right of its right end. Matches series.csv.

## Calibration (cal-p1)

1. Hand-made tick calibration (`helpers/calib.py`), layout of `tools/calibrate_axes.py` with `box`
   and `anchors`. The plot has no grid: ticks point inward on the bottom frame (x = 2 to 12) and on
   the left frame (y = 1 to 9); the top and right frames carry no ticks (scanned along their length).
2. Frames fitted on the centre of their ink: bottom v = 3898.87 + 0.007516 u (rms 0.47 px), top v =
   1098.40 + 0.008395 u (0.86 px), left u = 617.45 - 0.006632 v (0.44 px), right u = 2571.96 -
   0.004883 v (0.68 px). The page is turned about 0.4 degrees and the frame is very slightly out of
   square (left and right frames differ in tilt by 0.0017, 4.8 px over the height).
3. The frames are the lines 0 and 14 (x) and 0 and 10 (y): the labels 0, 14, 0, 10 are printed at
   them and the tick spacing confirms each (frame to tick: 282.4 px at x 0 to 2, 279.9 px at x 12 to
   14, 278.5 px at y 0 to 1, 281.2 px at y 9 to 10). No frame extends past a labelled line.
4. Ticks located on their stubs (x: rows 7 to 20 px above the bottom frame centre; y: columns 6 to 20
   px right of the left frame centre), anchored on the frame centre line. Tick widths 3 to 6 px,
   scatter of the stub centres 0 to 0.6 px. Spacing between adjacent ticks: x 277.6 to 283.2 px per
   2 psi, y 278.3 to 283.5 px per 1 ksi, so the drafting is uneven by up to 2 percent per interval and
   the piecewise map is the one to use.
5. Affine diagnostic: x rms 0.0079 psi, max 0.0205 psi (0.15 percent of the span); y rms 0.0046 ksi,
   max 0.0088 ksi (0.09 percent). Both well under 0.5 percent. Affine minus piecewise over all points:
   at most 0.021 psi and 0.008 ksi.
6. Piecewise knots with the ink check (`cal-p1/knots.json`): all 8 x lines and 11 y lines verified,
   none rejected. Drawn frames lie within 0.15 px of their ink's line (ink scatter 0.32 to 0.72 px);
   ticks within a median 0.03 to 0.45 px on their stubs.
7. One artefact: the x = 4 tick gets a location error of 4.39 px. Its stubs above the axis agree with
   the tick within 0.3 px; the two stubs below the axis land on a small bump of the frame's lower
   edge at u 1155 to 1157, v 3912 to 3915 (crops/xt4.png), not on the tick. The tick itself is well
   located; the effect is only a wider x bound (about 0.03 psi more) for points between 2 and 6 psi.
   I kept the conventional anchor on the axis line rather than move it to dodge the bump.
8. Labels checked by eye (calibration-eye-checks.csv, all 8 x and 11 y labels): every label fits
   its sequence and names the nearest line. Hand lettering is offset up to 21 px from its line (x
   labels 6 and 12 left of their ticks, 8 and 14 right; y label 7 is 18 px below its tick), far
   less than the 280 px spacing. Stray marks that are not ticks or labels: the base stroke of the x
   label "2" runs on as a horizontal line to u 1078 below the axis; a dash at v 2455 left of the y
   label "5"; a faint dash at v 2847 left of the frame.

## Markers (15)

Centres of isolated circles from the hole centroid and an outer-edge circle fit (they agree within
0.6 px; outer radius 20.8 px, hole radius 12.75 px), bound 2 px. Overlapping circles from a ring
model fit (`helpers/ringfit.py`: union of rings with the radii of the isolated circles, drawn lines
left out of the comparison), bound 3 px; the centres move by at most 1.25 px when the radii change
by 0.5 px or the line corridor by 2 px.

1. `dr86`, 7 markers: a pair overlapping at about (2.45, 4.94) and (2.45, 4.88), one just below at
   (2.55, 4.75), two at about 4.87 psi (7.43, 7.18), and a double circle at 9.75 psi (9.23, 9.19).
2. `dr22`, 8 markers: one at (1.24, 2.49), a triple at about 2.5 psi (4.12, 4.04, 3.99), two at
   about 4.98 psi (6.27, 5.13), two at about 9.59 psi (7.41, 6.62).
3. Overlaps told apart: the dense pair at 2.5 psi (two holes and the crescents between them; a two
   ring model fits, one ring does not); the loose triple at 2.5 psi (a two ring model leaves 2.7
   times the misfit of three); the dense double circle at 9.8 psi (one ring leaves 3.5 times the
   misfit of two). For the double circle the ink spans v 1310 to 1364, which an edge reading puts at
   1330.3 and 1343.2 against the model's 1330.6 and 1341.5: within the 3 px bound.
4. Identity, where it is a judgement:
   - the circle at (2.55, 4.75) just below the dense pair is 13 px from the extension of the dense
     line and 107 px from the loose line: `dr86`. This also gives each density three tests at 2.5 psi.
   - the circle at (4.99, 6.27) lies between the lines, 157 px from the loose line and 293 px from the
     dense line: `dr22`. The loose corner at 5.00 psi (5.71) sits midway between it and the loose
     circle below (5.13), which supports the assignment.
   - the circle at (9.58, 7.41) is above the loose line's end and far below the dense line: `dr22`.

## Polylines

Each drawn segment is straight: centre line fitted on the ink with circles left out, rms 0.56 to 0.84
px. Perpendicular line thickness 8.1 to 9.6 px; trace bounds are half of it (4.1 to 4.8 px).

1. `dr86` (2 segments, 1 vertex): first point (2.59, 4.90), where the line's ink meets the outline
   of the dense pair at 2.5 psi; vertex (4.84, 7.27) on the ink of the drawn corner, just above the
   circle at (4.87, 7.18), whose upper left outline the first segment crosses; last point (9.66,
   9.13), where the ink meets the outline of the double circle. The line may run on under the pair's
   ring at the start; it does not reach the circle below the pair (that circle's hole is white on the
   line's extension).
2. `dr22` (3 segments, 2 vertices): first point (1.30, 2.56), where the ink meets the outline of the
   circle at 1.24 psi (the line is aimed at that circle's centre, whose hole is white); the first
   segment's ink meets the outline of the triple at (2.38, 3.92); the first vertex is hidden: the
   two fitted segments meet at (2.54, 4.12), 2.1 px from the centre of the top circle of the triple,
   inside its white hole, so it is recorded as a feature only and is not a trace sample (rule 7); the
   second segment's ink leaves that circle's outline at (2.63, 4.17); second vertex (5.00, 5.71) on
   the ink of the corner; last point (9.62, 7.05), the free end of the ink.
3. Trace samples at every whole psi between the ends, on the fitted centre line, all checked to be on
   ink. The loose corner is at 4.999 psi (0.12 px from the 5 psi line), so it stands for the 5 psi
   sample instead of a duplicate point.

## Ambiguities for the comparison

1. The loose line's hidden vertex: the other reading may record it as a trace sample or put the
   vertex elsewhere; on the page the hole of the top circle is white where the segments would meet.
2. Where the dense line starts: its ink is distinguishable down to the outline of the pair (v about
   2537); below that it merges with the ring.
3. Line ends at symbols are taken where the centre line meets the symbol's outline (on ink; at the
   lower edge of the triple a 1 px white notch between line and ring moved that sample 1.8 px back
   onto the line's ink).

## Files

1. `cal-p1/calibration.json`, `cal-p1/anchors.csv`, `cal-p1/knots.json` (piecewise knots with their ink
   checks).
2. `calibration-eye-checks.csv`.
3. `points-p1.csv` (pixels) and `points-p1-native.csv` (piecewise map with the page image, no point
   beyond the outermost verified line).
4. `overlay-p1.png` (the points over the page, cropped to the plot).
5. `helpers/` (frame, tick, circle, segment and assembly scripts; `points-affine-check.csv` is the
   affine diagnostic only) and `crops/` (the zoomed crops looked at).
