# FC-13, Figure C-13, SS Loose (printed C-35, PDF page 147), reader Claude

Series `ss-loose` (series.csv). The page prints "SS Loose" as the box title and the caption
"Figure C-13. SS Loose", which agrees with series.csv and figures-rows.csv (avg density 95.20).

## The box, as printed

    SS Loose
    Avg. Density = 95.20
    Angle of Friction = 29.76
    Tan Theta = .5718
    Cohesion = 11.87

1. The "=" signs print as filled bars; decimal points look like commas in the scan.
2. Tan Theta: a short thin mark sits between the "=" and ".5718" (`box-text.png`). It is much
   thinner and shorter than a printed minus sign; read as a speck. tan(29.76 deg) = 0.5718,
   consistent with a positive .5718.
3. Cohesion: the first character is a "1" (top flag and base serif like the second "1") with an
   extra horizontal stroke at mid-height running to the right of the stem (`box-cohesion.png`). It
   is not shaped like a "4" (whose bar would run left of the stem); read as 11.87, with this
   uncertainty. Taken in psf, as on Figure C-12.

## Calibration (cal-p1/)

1. `calibrate_axes.py detect` on box u 680..2775, v 1350..3755, 8 bands, x 0 to 7000 psf, y 0 to
   8000 psf. The frame continues above the 8000 line (to v 884) around the text box; the detection
   box starts just above the 8000 line.
2. All 8 vertical and 9 horizontal lines detected in 8 of 8 bands; none predicted. Affine residuals:
   x RMS 4.4 psf (max 11.7), y RMS 10.1 psf (max 21.2), at most 0.26 percent of a span.
3. Piecewise map with `--image`: all 8 x lines and 9 y lines verified on the ink, location errors
   0.53 to 1.07 px; nothing rejected (`cal-p1/knots-summary.json`).
4. The grid is slightly sheared on the page: vertical lines lean by +0.0030 to +0.0048 (du/dv),
   horizontal lines tilt -0.0005 to +0.0023. Spacing: vertical lines 289 to 293 px per 1000 psf,
   horizontal lines 287 to 299 px.
5. By-eye label checks, three per axis, in `calibration-eye-checks.csv`: every label sits nearest the
   line it was anchored to. The largest offset is the 700.00 label, centred 18.6 px left of the right
   frame (the next line is 286 px further left).

## Points (points-p1.csv, points-p1-native.csv)

7 markers, 11 trace samples, 3 features; all `ss-loose`, panel 1; psf, piecewise map.

Markers: 7 upright triangles, none overlapping another; centroids of the triangle reconstructed
from its stroke centre lines (rule 8), checked against the ink in `check-tri*.png`. Bounds 2 to 3
px in u, 5.5 to 6.5 px in v (at least height/6, heights 27 to 33 px).

1. Triangle 1 (x 151, y 133): the line's dash ends touch its lower left corner and its upper right
   side (the hole stays white, so the line is lifted across the symbol); each side read on the rows
   clear of the line. Bound 2.5 / 5.5 px.
2. Triangle 2 (x 1724, y 1034): its base coincides with the y = 1000 grid line (merged band v 3417
   to 3425.5, grid line alone 3417 to 3423.5). The base centre is fixed at v 3421.0: hole bottom
   3416.5 plus half the 8 px stroke gives 3420.5, band bottom minus half a stroke gives 3421.5. Bound
   2 / 6 px.
3. Triangle 3 (x 2364, y 1357): dash ends touch its lower left corner and upper right side; the
   right side has only 7 clean rows and its fit put the apex above the ink, so the right side is the
   mirror of the left about the axis through the apex and the hole (u 1399.3), and the edge-inset
   estimate is used (height 29.6, like the other symbols). Bound 3 / 6.5 px.
4. Triangle 4 (x 2921, y 1624): apex merged with the start of the next dash; right base corner
   touches the x = 3000 grid line; small hole. Stroke-centre and edge estimates within 0.5 px. Bound
   3 / 6 px.
5. Triangle 5 (x 3817, y 2174): the start of the next dash touches its upper right side.
6. Triangle 6 (x 4404, y 2619): clear of the line, above it.
7. Triangle 7 (x 4693, y 2668): the drawn line ends in its lower left corner.

Not symbols: dots right of triangle 5 at its base level (u 1843 to 1863, v 3087), a speck right of
triangle 7 (u 2100, v 2941), small specks below the line near u 1310 and 1510. Not recorded.

The drawn line: straight on the page (v = 4102.91 - 0.56330 u over 914 clean columns, RMS 0.63 px,
by thirds +0.23, -0.41, +0.19 px), 11.3 px thick across (13 px vertical run), lifted across
triangles 1, 2, 3 and 5 (gaps u 753 to 760, 1191 to 1232, 1394 to 1402, 1800 to 1836) and touching
triangle 4's apex. Trace samples are the centre of the ink from a local straight fit over clean
columns within 16 px; bound 5.7 px (half the thickness):

1. Left end, x = 0: the line runs into the left frame 15 px above the bottom frame (no ink left of
   the frame). Placed at the frame's centre line, u 712.1, v 3702.6; bound 4.5 px u, 8.5 px v.
2. x = 500 to 4500 psf every 500 (9 samples). x = 1000, 2000, 3000, 4000 fall on vertical grid
   lines, x = 3500 where the line crosses the y = 2000 grid line; their centres come from clean
   columns on both sides.
3. Right end, x = 4641: the line runs into the lower left corner of triangle 7 and ends there (the
   triangle's hole stays white down to its base, so the line stops before u 2066). Placed at the
   corner, u 2061.0, v 2943.0; bound 4.5 px u, 8.5 px v. The line ends about 15 px (50 psf) short of
   the last symbol's centroid.

Features: first point and last point (as trace samples 1 and 11); intercept: the line reaches the
x = 0 axis (left frame), at the frame's centre line, u 712.1, v 3702.6, bound 1 px u, 5.7 px v.

## Comparison with the printed box (not used to move any point)

| quantity | printed | this reading (piecewise) | difference | same reading, affine map |
|---|---|---|---|---|
| slope of the trace samples (least squares, 11) | Tan Theta .5718 | 0.5558 (29.07 deg) | -0.0160 (-2.8 percent) | 0.5612 (-1.9 percent) |
| end-to-end slope | | 0.5559 | -0.0159 | 0.5611 |
| shear stress at the intercept feature | Cohesion 11.87 psf | 50.9 psf, bound 21.0 | +39.0 psf | 37.9 psf (+26.0) |
| intercept of the least-squares line through the trace | | 49.6 psf | +37.7 psf | 41.6 psf |

1. The drawn line does not agree with the printed values within the reading bounds. It is shallower
   than Tan Theta and meets the x = 0 axis about 39 psf (11 px) above the printed cohesion. Against
   the printed line y = 11.87 + 0.5718 x the trace runs from +39 psf at x = 0 to -35 psf at its right
   end: the drawn line is rotated with respect to the printed fit, crossing it near x = 2250 psf.
2. This is not a calibration effect: on the page the line's slope is 0.5633 px/px, 0.562 in value
   units with either map's scale, while Tan Theta .5718 would need 0.573 px/px, a difference of
   about 14 px over the line's 1350 px length. The grid is labelled as expected (eye checks).
3. Diagnostic only: a least-squares line through the 7 markers as read gives slope 0.5673 and
   intercept 31.7 psf (piecewise), 0.5721 and 25.4 psf (affine). The markers' slope is close to the
   printed Tan Theta; the drawn line's is not.
4. If the first character of the cohesion were not a 1, the comparison would change; read as 11.87
   (see the box above).

## Calibration sensitivity (affine minus piecewise)

Markers: x -4 to +2 psf, y -11 to +12 psf. Trace: x -4 to +5 psf, y -13 to +12 psf, smallest in the
lower middle of the plot. The trace through the piecewise map stays straight within +/-3.6 psf of
its own least-squares line.

## Ambiguities

1. Cohesion's first character (see above).
2. Triangle 2's base is under the y = 1000 grid line; triangle 3's right side and triangle 4's apex
   are merged with the line; triangle 3 rests on a symmetry assumption.
3. Right end of the line hidden in triangle 7's lower left corner (u 2058 to 2066); left end hidden
   under the frame (u 708 to 716).
4. Marker registration (bounding-box middle or centroid) not established; the v bound covers both.

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-summary.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, `notes.md`. Working files: `read_env.py`,
`config.json`, `helper-log.txt`, `helper-*.json`, `compare_box.py`, `montage.py`,
`label_centre.py`, `check-tri*.png`, `check-montage.png`, `affine-check.csv`, `eye-*.png`,
`z*.png`, `zoom-montage*.png`, `box-text.png`, `box-cohesion.png`.
