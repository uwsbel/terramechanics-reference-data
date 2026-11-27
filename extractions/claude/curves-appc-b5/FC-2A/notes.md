# FC-2A, Claude reading (batch curves-appc-b5)

Source: AM-68-1 Vol. II, Figure C-2A "Failure Envelopes - Maximum Shear Stress vs. Normal Stress",
printed C-6, page image `packet/p0120.png` (300 dpi, unrotated, 3263 x 4508, pure black and white).
One panel, upright: tau (PSF) up, sigma (PSF) right.

## Legend as printed, series and lines

Legend box, "PS-Soil":

1. open square: "gamma = 25.6 to 26.8 Lb./Ft.^3 (D_r = .33 to .53)", series `dr33-53` (matches
   `series.csv`).
2. open circle: "gamma = 31.7 to 33.1 Lb./Ft.^3 (D_r = 1.15 to 1.3)", series `dr115-130` (matches
   `series.csv`).

Two straight lines, each solid with a dashed part (two dashes) running down-left into the
shear-stress axis.

3. Upper line, labelled **49.5°** (label just above-left of it, center about u 1698, v 2329). It runs
   through or next to all six squares, so it is the `dr33-53` envelope.
4. Lower line, labelled **46.7°** (label between the two lines, its baseline just above the lower
   line, center about u 1881, v 2285). It runs through or next to all six circles, so it is the
   `dr115-130` envelope.

Check of the label assignment from the reading itself: the trace samples give slopes of
atan(1.1649) = 49.4° for the upper line (x 250 to 4500) and atan(1.0583) = 46.6° for the lower line
(x 250 to 4750), against the printed 49.5° and 46.7°. The pairing is not in doubt.

Symbols against the legend: every square is on or beside the upper line and every circle on or
beside the lower line; no symbol of another shape or fill sits on either line. Nothing was
reassigned.

Observation, not a correction: on this page the loose group (gamma 25.6 to 26.8, Dr .33 to .53,
squares) has the higher envelope and the steeper angle (49.5°), and the dense group (gamma 31.7 to
33.1, Dr 1.15 to 1.3, circles) the lower one (46.7°). That is the reverse of the usual expectation
that the denser state is stronger. The drawing is internally consistent (legend symbol, plotted
symbols and line all agree), so if the legend symbols were swapped relative to the tests, the page
alone cannot show it; it would take the response sheets, which are not in this packet. The figures
index row carries a note to that effect; I have not used it to change anything and kept the series
ids as the legend prints them.

## Calibration (`cal-p1/`)

The frame has tick marks only, no interior grid lines, and its top line (about 6450 psf) is not at a
printed value; part of it is hidden by the legend box. `tools/calibrate_axes.py detect` was run
(box 920 1450 2440 3400, x 0..5000, y 0..6000; record in `helpers/cal-tool-attempt-rejected/`) and
took the legend box's lower edge as y = 6000 with every interior line `predicted`. Its y map is off
by about 180 to 210 psf at the top of the plot against the drawn 6000 tick, while its residual looks
small, so it was rejected.

`cal-p1/` is made by `helpers/tick_calibrate.py` instead, in the tool's JSON layout so that
`calibrate_axes.py apply` uses it. Anchors (13): the axis corner (0, 0); the x ticks 1000 to 4000
carried onto the fitted bottom axis; the right frame line at the bottom axis as x = 5000 (no tick is
drawn there, the "5000" label sits under it, and the 0 to 4000 ticks extrapolate to it within 2 px);
the y ticks 1000 to 6000 on the fitted left axis. Affine least squares.

1. Scale 3.4377 psf/px in x, 3.4140 psf/px in y. The left axis leans 0.72° and the bottom axis 0.94°
   (the axes are 0.22° off square; the affine map takes this up).
2. RMS residual 14.2 psf in x (0.28 % of the 5000 psf span) and 15.0 psf in y (0.25 % of 6000).
3. Max residual 36.7 psf in x at the 1000 tick (0.73 %), 27.6 psf at the 3000 tick (0.55 %), and 33.2
   psf in y at the 5000 tick (0.55 %). These are above 0.5 % of the span. They come from the drawing:
   the tick spacing itself varies (x: 303, 277, 286, 301, 291 px per 1000 psf; y: 282, 300, 288, 293,
   308, 282 px), each tick was looked at on the crops and is where the anchor puts it, so no change of
   box or threshold can remove it. An affine map cannot follow a hand-drafted scale closer than this.
4. Without the right-frame anchor the map moves by at most 9.4 psf over the plot frame.
5. The map places the drawn left axis at x = -5.5 psf near the bottom (residual of the origin anchor);
   see the intercepts below.

By-eye label checks (`calibration-eye-checks.csv`): all 13 printed labels, 6 on x and 7 on y. Each
label sits beside its tick (x labels centered under their ticks within 12 px, y labels 0 to
14 px above their ticks); none is assigned to the wrong tick.

## Points (`points-p1.csv`, `points-p1-native.csv`)

`dr33-53`: 6 markers, 18 trace samples, 2 features. `dr115-130`: 6 markers, 19 trace samples, 2
features. 53 rows.

Markers. All twelve symbols are hollow and isolated; none overlaps another symbol. Centers are the
centroids of each symbol's white interior (`helpers/markers.py`), checked against the outer ink
extents on the central row and column (agreement within 1 px) and on the zoomed crops `crops/m_*.png`.
Bound 2 px. Square 6 (top right) has a broken top edge in print; its center is from its outer extents.
Squares 1 and 3 and circles 1 and 4 sit on their lines (the line enters the symbol at its lower left
and leaves at its upper right); circles 2 and 3 touch their line at the lower right of the ring;
squares 4, 5, 6 and circles 5, 6 are clear of their lines.

Traces (`helpers/build_points.py`). Each line's ink was scanned column by column; both lines are
straight to 0.86 px (upper) and 0.75 px (lower) RMS. Perpendicular thickness 9.9 px (upper) and
10.4 px (lower), so the bounds are 4.9 and 5.2 px. Each sample is a local straight-line fit to the
measured ink centers within 8 px of it, never the global fit.

1. Left end = the intercept: the first dash's centerline (its mean center, carried along the line's
   direction) meets the left axis's center line. Both first dashes run into the axis ink.
2. Then x = 250, 500, ... psf. Skipped under rule 7 because the line's ink is merged with a symbol
   there: upper line x = 750 (square 1) and x = 2250 (square 3); lower line x = 750 (circle 1, merged
   columns 2.5 px away) and x = 3000 (circle 4). Lower x = 1500 and x = 2250 are kept with a note:
   circles 2 and 3 touch the line 9 px and 4 px further along, and those columns were left out of the
   local fit.
3. Right end: the last ink on the solid line's centerline.
4. Dashed parts: upper line, dashes from the axis to u 977 and at u 984 to 1014, solid from u 1018 (x about
   232 psf); lower line, dashes from the axis to u 983 and at u 993 to 1025, solid from u 1032 (x about 283 psf).
   Samples marked "dashed": both left ends and lower x = 250 (on the second dash, 3 px from its end).

Features.

5. Intercepts at the drawn axis: upper (49.5°) y = 400 psf, lower (46.7°) y = 194 psf (bounds about
   32 psf). In the fitted map the drawn axis is at x = -5.5 psf there; at the map's x = 0 the values
   would be about 6 psf higher. Extending the solid part instead of the first dash gives 402 and
   191 psf.
6. Labels: "label: 49.5°" at the center of the label's ink box (u 1657 to 1738, v 2272 to 2385) and
   "label: 46.7°" (u 1838 to 1923, v 2230 to 2340). Their bounds are half the ink box, not a reading
   precision.

## Other things looked at

1. Specks at u 2231 to 2252, v 2156 to 2161 (2 to 6 px) and a dot under the lower first dash (u 984,
   v 3288): print noise, not symbols.
2. The right ends: upper line ends at x about 4713, y about 5899 psf (rounded pen end); lower line at
   x about 4857, y about 5327 psf (square cut). Neither reaches the frame.
3. The y axis label "0" sits at the corner with no tick of its own; the bottom axis line is y = 0.

## Files

`cal-p1/` (calibration.json, anchors.csv), `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv`, `overlay-p1.png`, this file; helpers and crops under `helpers/` and `crops/`.
