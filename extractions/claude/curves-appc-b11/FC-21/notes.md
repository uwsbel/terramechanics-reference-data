# FC-21, Claude's blind reading (batch curves-appc-b11)

Page `p0157.png` (printed C-43), "Figure C-21. Angle of Internal Friction vs. Relative Density",
one upright panel labelled "LSM Soil"; y axis printed "phi_DS - Degrees", x axis "D_r". The page
matches `figures-rows.csv` and `series.csv`: open circles and a cross-hatched band between two lines,
no curves. Series ids are used as given (`data`, `band-top`, `band-bottom`).

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect` on box 640 1200 2420 3440 (inside the frame, so the outermost lines
   found are the labelled ones), x values 0, 0.1, ..., 1.0, y values 30, 35, 40, 45, 50, 20 bands,
   min-frac 0.5. Every line detected in 19 or 20 of 20 bands, none predicted.
2. Affine residuals: x RMS 0.0011 (0.11 % of the 0 to 1.0 span), max 0.0027; y RMS 0.0091 deg
   (0.05 % of the 30 to 50 span), max 0.018 deg. All below the 0.5 % limit.
3. Piecewise map (D-025) with the page image: all 11 x lines and all 5 y lines verified on the ink,
   none rejected; line location errors 0.5 to 1.3 px.
4. The scan is tilted about 1.1 to 1.3 degrees (vertical lines du/dv +0.019 to +0.023, horizontal
   lines dv/du -0.018); the calibration carries each line's own tilt.
5. Labels checked by eye: all 11 x labels and all 5 y labels (`calibration-eye-checks.csv`). Each
   sits on its line; "1.0" is printed 17 px right of its line and "0" and "0.3" 11 px left of
   theirs, which is under a tenth of a division (about 155 px), so none is ambiguous.

## Frame beyond the labelled lines

The frame is not labelled on either axis and was not anchored. By extrapolation of the outer
intervals the left frame is at Dr -0.097 and the right frame at Dr 1.098 (one division beyond 0 and
1.0), the top frame at 55.0 deg and the bottom frame at 25.0 deg (one division beyond 50 and 30).
Twenty rows lie beyond a verified x line and carry `piecewise extrapolated x` in
`points-p1-native.csv`: circle 1 (Dr -0.048), circles 6, 7, 8 (Dr 1.02 to 1.08), and the band
samples and ends left of 0 and right of 1.0.

## Circles (`data`, 8 markers)

Centers fitted with a ring template (outer half-span 18.5 px, inner 12 px; `fit_rings.py`), checked
on zoomed crops. Left to right:

1. pair 1 left, Dr -0.048, 43.89 deg (left of the Dr 0 line, inside the frame).
2. pair 2 left, Dr 0.188, 44.48 deg.
3. pair 2 right, Dr 0.280, 44.43 deg.
4. pair 1 right, Dr 0.398, 43.88 deg. The joining line of pair 1 is long (Dr -0.05 to 0.40), 9 px
   thick and unbroken; it ends on this circle.
5. single, Dr 0.399, 43.73 deg. Circles 4 and 5 overlap: at Dr about 0.4 the page shows a figure
   eight of two rings, 11 px (0.14 deg) apart vertically, with the Dr 0.4 grid line and hatch lines
   through them (`crops/dbl.png`, `crops/double-circle-fit.png`). A two-ring fit explains the ink as
   well as a single ring explains a clean circle (template mismatch 57 px against 30 to 58 for the
   clean circles), so both are recorded, with 3 px (u) and 4 px (v) bounds. The pair 1 line arrives
   at v 2027 (line centre, 9 px thick), 2 px below the upper ring's centre and 9 px above the lower
   one's, and a level line from circle 1 on the tilted page would arrive at v 2023, so the upper
   ring is taken as pair 1 right and the lower one as a single. Alternative reading the page cannot
   exclude: one circle redrawn by the draftsman, in which case only one of 4 and 5 is a data point.
6. pair 3 left, Dr 1.024, 41.31 deg.
7. single, Dr 1.024, 40.78 deg, directly below circle 6, no joining line (the stroke that seems to
   join it to the pair 3 line in the reduced view is a hatch line).
8. pair 3 right, Dr 1.079, 41.36 deg. Its ring ends about 8 px inside the right frame; not cut.

The joining lines sit 2 to 3 px below the circle centres they join. No circle is cut by the frame.
No circle lies outside the band. A ring-template search over the whole frame finds only circles
1, 2, 3, 6, 7, 8 above a score of 0.73 (the overlapping pair 4 and 5 defeats the template's
white-centre test and was read by hand).

Not recorded: a filled, irregular ink spot about 17 by 25 px at u 2078, v 2014 (Dr 0.86, 43.8 deg),
under a hatch crossing, with no white interior and half the size of a circle: a blot, not an open
circle. Two short dashes above the band, about 9 by 3 px, beside the Dr 0.4 and 0.7 grid lines
(u 1365, v 1652: Dr 0.41, 48.8 deg; u 1835, v 1837: Dr 0.71, 46.2 deg; `crops/speck1.png`,
`crops/speck2.png`) are specks, not symbols.

## Band edges (`band-top`, `band-bottom`)

The hatched band is bounded by the 45 and the 40 grid lines themselves: each edge is one line of
grid thickness (median 6 px, the same as the 50 and 35 lines), the hatch lines end on it, and there
is no second line beside it anywhere along the width. So `band-top` reads 45.00 deg and
`band-bottom` 40.00 deg across the whole plot (samples within 45.00 +/- 0.02 and 40.00 +/- 0.02);
note that these are the same ink as the y knots 45 and 40, so they are not independent of the
calibration.

The band and both edges run the full width of the frame. Each edge's ink starts and ends on the
frame lines (inner edges at u 595 and 2443 for the top, 602 and 2452 for the bottom, Dr -0.094 and
1.095); the ends are placed at the frame's inner edge with a 5 px u bound that reaches the frame's
centre line. Trace samples: left end, Dr -0.05 to 1.05 every 0.05 (23 samples), right end; each
sample's v is the centre of the line's ink fitted over columns u-20 to u+20, with crossing grid
lines and hatch vertices set aside. Bounds 3 px (half the 6 px line). Features: first and last
point of each edge; the edges are straight, no knee, and level on the drawing, so no peak is read.

Not traced: the hatching, the joining lines, and several faint broken diagonal strokes inside the
band (broken into dashes and thinner than the hatching, parallel to its rising lines, for example
between u 720 and 820, v 2050 to 2105, near Dr 0 to 0.08 and 43 to 44 deg; `crops/faint.png`),
which look like an underdrawn or partly erased set of hatch lines.

## Calibration sensitivity

Affine against piecewise values: at most 0.0016 in Dr and 0.02 deg in phi over all 62 rows.

## Files

`points-p1.csv`, `points-p1-native.csv` (piecewise, with `cal_model`), `cal-p1/`,
`calibration-eye-checks.csv`, `overlay-p1.png`, `crops/`, helpers `read_fc21.py`, `fit_rings.py`,
`find_circles.py`, `ring_overlay.py`, `ascii.py`, `hprofile.py`, `line_runs.py`, `vruns.py`;
`scratch/` holds a trial calibration that included the frames and the affine conversion.
