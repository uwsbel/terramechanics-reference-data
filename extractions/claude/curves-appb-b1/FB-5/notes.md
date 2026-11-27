# FB-5, blind reading (Claude), batch curves-appb-b1

Page `p0111.png` (300 dpi, 3213 x 4604 px, binary black and white), printed page 8. The page prints
the caption "Fig. 5 E VERSUS sigma_3 FOR SS SOIL" (no "B-" prefix); one panel, upright. Axes: x
"Confining Pressure, sigma_3, psi" 0 to 12, y "Modulus, E = rho c^2, kips/in.^2" 5 to 40.

## Series and labels

1. `dr84`: the upper polyline. Its printed label, right of the line's upper end, reads "Dense" over
   "Dr = o.84" (the zero is typed small, like a lower-case o). Matches the id.
2. `dr26`: the lower polyline. Its label, right of the line's upper end, reads "Loose" over
   "Dr = 0.26" with the "0." poorly printed: only the top arc of the 0 is inked, no decimal point is
   visible, and the "=" is broken. What is legible ("26") fits the series' Dr; read as 0.26.
3. Every symbol is an open circle. The two groups are far apart on the page (no symbol lies between
   the lines), so every marker's group is clear from the line it sits on.

## Calibration (`cal-p1/`, helper `calibrate_ticks.py`)

1. No grid lines. Ticks only on the bottom frame (x = 2, 4, 6, 8, 10) and on the left frame
   (y = 10 to 35), pointing into the plot, about 31 to 39 px long; none on the top and right frames.
2. Anchored lines: x = 0 the left frame (label "0" under it), x = 2 to 10 the ticks, x = 12 the right
   frame; y = 5 the bottom frame (label "5" beside it), y = 10 to 35 the ticks, y = 40 the top frame
   (label "40" beside it). Each frame line is fitted to its ink every 5 px (rms 0.54 to 0.83 px); each
   tick to its ink on 23 to 30 rows or columns, its anchor where it meets the frame line's centre.
3. The page is turned by about 0.8 deg and the frame is slightly skewed: left and right frames lean
   du/dv = +0.0164 and +0.0175, bottom and top frames dv/du = -0.0145 and -0.0139.
4. Affine map (diagnostic): its lines of constant value take the mean tilt of the two frame lines of
   that axis, scale and offset by least squares on all 25 anchors. Residuals: x rms 0.008 psi, max
   0.024 psi (0.2 percent of the 12 psi span); y rms 0.019 ksi, max 0.048 ksi (0.14 percent of the
   35 ksi span). The largest y residuals are the 30 and 25 ticks (+4 px): uneven drafting, which the
   piecewise map reads as drawn.
   Why the tilt constraint: the ticks sit on one side only, so an unconstrained fit (kept in
   `calibration.json` as `affine_unconstrained`, y rms 0.016 ksi) turns its y lines to dv/du = -0.0154,
   steeper than either horizontal frame line, and `calibrate_axes.py` gives every lone tick the tilt of
   the affine map. Measured effect on the piecewise values: up to 0.022 ksi in y (about 2 px, at the
   right of the plot) and 0.003 psi in x.
5. Piecewise knots (`calibrate_axes.py piecewise --image`): all 15 lines verified on the ink
   (`cal-p1/knots.json`). Frame lines: ink found at every position, within 0.3 px of the reader's line
   at both ends. Ticks: median stub distance 0.01 to 0.56 px. Location errors 0.5 to 0.94 px, except
   the x = 8 tick (2.55 px) and x = 10 tick (1.10 px): one outer stub of each, below the axis, catches
   the ink of the printed label "8" or "10". That only widens the bounds of points between 6 and 10 psi.
6. No point lies beyond the outermost verified line.
7. Label checks (`calibration-eye-checks.csv`, all 15 labels): every label fits its sequence. The
   one-digit x labels sit 13 to 15 px right of their ticks, "10" is centred on its tick, and the
   y labels sit within 12 px of their lines. **"12" is printed off its line**: 33 px left of the right
   frame. The tick spacing confirms the right frame as x = 12 (351 px past the 10 tick, against 354 to
   359 px for the other 2 psi intervals), so it is used. The "40" and "5" labels have no ticks. Their
   frame lines are confirmed by the spacing (447 and 445 px against 443 to 449 px).

## Markers (13)

1. Clean circles (11 of them): each centre is the mean of a circle fitted to the hole's boundary and
   one fitted to the ring's outer edge (they agree within 0.1 to 1.4 px). Hole radius 10.8 to 11.6 px,
   outer radius 18.6 to 19.6 px. Bound 2 px.
2. `dr84` markers 1 and 2: two overlapping circles at the lower left of the dense line, about 16 px
   apart, told apart by their two holes and the white lens between them. The centres come from a
   joint ring-template match (radii 11.2 and 19.2 px) that pins each within about 1 px. Bound 4 px
   for the overlap. The dense line's left end meets the top of the right circle.
3. `dr26` marker 5 (lower of the two at the right end of the loose line): **partly printed**. Only
   the lower-left arc of its ring is inked; at page scale it reads as "(". Two specks sit where the
   top of the ring would be. Its centre comes from a ring-template match to the arc, which pins it
   to about 2 px. It is taken as a marker because it sits at the same u as the circle above it, the
   loose line ends half way between the two, and its arc has the radii of the other rings. Bound 5 px.
4. Not markers: specks at (2128, 2318) (an irregular 12 px blob), (901, 2261), (2209, 3026) and
   (2316, 2444). There is also a broken dotted row inside the frame at v about 3593, u 767 to 959,
   just below the y = 10 tick. It is 2 to 4 px thick with no symbol on it; similar dotted marks sit in
   the page margins outside the frame, so it is taken for a reproduction artifact, not data. A search
   for enclosed holes found no other circle.

## Polylines

1. Each group is two straight segments with one vertex. Each segment is fitted to its ink centres on
   cross-profiles every 2 px, away from the markers. The fit residuals are rms 0.50 / 0.70 px (dense
   lower / upper) and 0.57 / 0.56 px (loose). The lines are 8.5 to 9.5 px wide, so the trace bounds
   (half the width) are 4.25 to 4.75 px.
2. Trace samples lie on the fitted centre lines. Each 1 psi sample was checked against the ink:
   within 0.8 px of the ink centre where the line is clear.
3. Dense vertex (1383.4, 2213.5), about 4.02 psi and 24.97 ksi. It is the intersection of the two fits,
   which meet at 17 deg. The ink confirms it: between the two mid markers the ink follows the
   upper segment (not the lower one) down to the top of the lower marker's ring, where the lower
   segment arrives.
4. Loose vertex (1575.2, 3056.1), about 5.01 psi and 15.46 ksi. It is hidden where the rings of the two
   mid markers touch, so the two fits (11 deg apart) are its only evidence. The feature bound is
   widened to 6 px.
5. Ends:
   - dense left: (1042.0, 2932.4), where the line's ink meets the outer edge of the right circle of
     the overlapping pair. The line may run on hidden under that ring for up to 14 px; the feature
     bound is widened along the line (6, 13 px).
   - dense right: (2395.5, 1100.1), where the ink ends, touching the lower right of the upper top
     marker's ring. The line runs about 0.1 psi past the two top markers.
   - loose left: (1142.3, 3479.3), where the line's ink meets the outer edge of the upper of the two
     lower-left rings, at the point where the two rings touch. The line may run on hidden through
     both joined rings for up to 35 px, to the lower ring's outer edge at (1116.9, 3504.1). **The
     first-point feature bound is therefore wide (26, 25 px).**
   - loose right: (2351.4, 2543.0), a free end half way between the two top markers, touching neither.
6. Two 1 psi samples fall almost on a vertex. Dense 4 psi lies 6 px before its vertex, and loose
   5 psi 1.5 px before its vertex. Both are on the line where it touches a marker ring, and each
   carries a note.

## Values as read (piecewise, for orientation only; the CSV is the record)

- dense markers: x 1.93, 2.02, 2.03 / 4.05, 4.05 / 9.67, 9.68 psi; y 16.73, 16.72, 17.42 /
  25.42, 24.73 / 36.73, 37.48 ksi.
- loose markers: x 2.43, 2.49 / 5.02, 5.05 / 9.40, 9.42 psi; y 10.83, 10.45 / 15.68, 15.31 /
  20.40 (partly printed circle), 21.83 ksi.
- The top markers of the two groups do not share an abscissa: dense at 9.68 psi, loose at 9.41 psi,
  a 48 px difference on the page, well outside the bounds.

## Counts

| series | marker | trace | feature |
|---|---|---|---|
| dr84 | 7 | 10 | 4 (first, vertex, last, label) |
| dr26 | 6 | 10 | 4 (first, vertex, last, label) |

## Files (under `out/FB-5/`)

`points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, `calibration-eye-checks.csv`,
`cal-p1/calibration.json`, `cal-p1/anchors.csv`, `cal-p1/knots.json`; helpers `frame.py`,
`ticks.py`, `calibrate_ticks.py`, `knots_check.py`, `markers.py`, `outer.py`, `template.py`,
`holes.py`, `components.py`, `lines.py` (`lines.json`), `crop_lines.py`, `make_points.py`,
`eye_checks.py`; zoomed crops in `crops/`. `diagnostics/` holds the affine-map values and the
piecewise values from the unconstrained tilt; neither is a deliverable.
