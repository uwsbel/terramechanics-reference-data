# FC-20 (Figure C-20, printed C-42, PDF page 156): reading notes, Claude reader

Page image `packet/p0156.png`, 3213 x 4604 px, 300 dpi, unrotated. One upright panel. The scan is
tilted by about 1 degree (vertical grid lines lean +0.018 to +0.023 px of u per px of v, horizontal
lines -0.016 to -0.018 px of v per px of u); every line was fitted with its own tilt.

## What is printed

1. Title: "Figure C-20. Angle of Internal Friction vs. Relative Density". Axis titles "phi_DS -
   Degrees" (y) and "D_r" (x). The only text inside the frame is "SS Soil" (top left). No legend
   is printed: the roles of the three lines come from `series.csv` (solid = `mean`, dashed above
   it = `upper`, dashed below it = `lower`), and they match what is drawn (one solid line between
   two dashed lines over the whole range). Soil SS, as the index says.
2. Seven open circles (no other symbol). One pair joined by a short horizontal line (circles 2 and
   3); the other five are singles. A ring search over the whole frame (radius 15 to 17 px) found
   exactly these seven.
3. One solid curve and two dashed curves, all three S-shaped, rising from Dr about 0 to Dr about
   1.0, with the steepest part near Dr 0.45 to 0.5. No knee or kink on any of them; the maximum of
   each trace is its last point (noted on the last-point feature; no separate peak row).

## Calibration (`cal-p1/`)

1. Box u 700..2420, v 1590..3400, 10 bands: inside the frame, so the outermost lines found are
   the labelled lines Dr 0 and 1.0, phi 50 and 30, not the frame. x values 0, 0.1, ..., 1.0
   (11 lines), y values 30, 35, 40, 45, 50 (5 lines); 55 anchors, every line detected in 10 of 10
   bands, none predicted.
2. Affine residuals: x RMS 0.0019, max 0.0040 (0.40 percent of the 0 to 1 span, under the 0.5
   percent limit); y RMS 0.010 deg, max 0.022 deg (0.11 percent of the 30 to 50 span). The x
   residual is drafting: the spacing of the x lines ranges from 147 px (0.4 to 0.5) to 165 px (0.8
   to 0.9) per 0.1 of Dr. The values come from the piecewise map (D-025), which reads them between
   the lines as drawn.
3. Ink check (`calibrate_axes.py piecewise --image`): all 16 lines verified, ink found at every
   checked position (12 of 12 on the x lines, 25 of 25 on the y lines); the reader's line sits at
   most 1.15 px from the ink's line at an end (x = 0.4), location errors 0.50 to 1.46 px.
4. Labels checked by eye on zoom-3 crops (`calibration-eye-checks.csv`): all eleven x labels and
   all five y labels, each printed under or beside the line it names, the largest offsets 9.5 px
   (x, label "0.8" centre) and 8.2 px ("30" printed slightly below its line), against line
   spacings of 147 to 165 px (x) and 381 px (y).
5. The frame extends past the labelled lines on all four sides, by one unlabelled grid interval
   each: left frame at Dr about -0.095, right frame at about 1.099, top frame at phi about 55.0,
   bottom frame at about 25.0 (affine map extrapolated). None of the frame lines carries a label,
   so none is a knot. Points below the phi = 30 line (lower curve from Dr 0 to 0.25, the pair and
   the circle at Dr 0.01, the left part of the solid curve) and points at or beyond Dr 0 and 1.0
   are flagged `extrapolated` in `cal_model` by the tool (24 rows; for some of them only the
   bound box reaches past the line).

## Circles (series `data`, 7 markers)

Centres fitted on the ink: rays cast from the eye estimate at 72 angles, the midpoint of the ring
on each ray, a least-squares circle through the midpoints (`fit_circles.py`); ring radius 15.8 to
16.3 px, fit RMS 0.4 to 1.0 px. Bound 2 px for a clean circle, 3 px where something touches it.

| seq | Dr | phi (deg) | note |
|---|---|---|---|
| 1 | 0.014 | 29.70 | single; ring touches the Dr 0 grid line on its left |
| 2 | 0.015 | 29.02 | pair 1 left; the solid curve runs over the top of its ring (the line covers the top of the ring) |
| 3 | 0.133 | 28.99 | pair 1 right |
| 4 | 0.297 | 33.06 | single; the Dr 0.3 grid line runs through it |
| 5 | 0.474 | 36.82 | single; ring printed broken; the upper dashed curve passes about 6 px from it |
| 6 | 0.780 | 41.33 | single; the upper dashed curve passes about 10 px above it |
| 7 | 1.000 | 41.23 | single; the Dr 1.0 grid line runs through it; the solid curve ends at its outline |

No circle is cut by the frame. The pair 1 joining line runs at phi about 29.0 from the right side
of circle 2 to the left side of circle 3 (not traced). Circle 3 sits just above the lower dashed
curve, in a gap between two of its dashes (ends at u 976 and 1029), without touching its ink.

## Curves (series `mean`, `upper`, `lower`)

1. Method: each curve was followed column by column on the page (`trace_curves.py`: centre of the
   dark run nearest a straight-line prediction), and the result checked on zoomed overlays
   (`v1.png` to `v5.png`, `chk_*.png`). Samples at every 0.05 of Dr (`sample_curves.py`) are
   where the piecewise x map crosses the target along the usable columns. Line thickness
   (perpendicular) is 7.4 to 7.6 px median on all three curves, so the bound is 4 px (half the
   thickness, rounded up) in u and v; wider where noted.
2. Each curve: left end, Dr 0.00, 0.05 ... 0.95, right end (22 trace samples), plus two features
   (first point, last point).
3. Left ends: all three start at the Dr 0 grid line, their ink showing 1 to 7 px to the left of
   its centre (mean at Dr -0.005, upper -0.002, lower -0.002); the Dr 0.00 samples lie on the grid
   line, interpolated between the ink on either side of it (v bound 5 to 6 px).
4. Right ends: the solid curve ends at the outline of circle 7 (Dr 0.988, phi 41.23) and does not
   enter the ring. Both dashed curves end in the Dr 1.0 grid line (upper at Dr 0.999, phi 43.25;
   lower at Dr 0.998, phi 40.24); no ink right of that line. Whether the last dashes continue
   under the grid line's ink cannot be seen.
5. Samples on a vertical grid line (Dr 0.1, 0.2, ...): the curve's ink is merged with the grid
   line over about 15 px; the centre is interpolated between the ink on either side, and the
   curve is drawn through (not a dash gap) in every case used.
6. Samples where a curve merges with a horizontal grid line: mean Dr 0.80 (phi 40 line), lower Dr
   0.55 (phi 35 line) and Dr 0.95 (phi 40 line, which the lower curve runs along for about 60
   px). The centre is half a line width from the curve's free edge; v bound 5 px.
7. Dashed curves, samples moved to a dash end (rule 7): upper Dr 0.20 (to 0.195), 0.30 (to
   0.307), 0.40 (to 0.415; the two neighbouring ends are at 0.384 and 0.415, almost equally
   near), 0.50 (to 0.508), 0.65 (to 0.649), 0.75 (to 0.752), 0.85 (to 0.860), 0.95 (to 0.947);
   lower Dr 0.25 (to 0.245), 0.35 (to 0.349), 0.45 (to 0.452), 0.75 (to 0.741).
8. Upper dashed curve, Dr 0.41 to 0.48 (next to circle 5): the dash is printed as fragments
   (u 1440..1485, 1491..1500, 1506..1524, 1527..1545), all on the curve's path; the Dr 0.45
   sample is on the fragment at u 1491..1497.
9. Upper dashed curve, Dr 0.93 to 0.97: the dash from u 2119 ends at u 2239 at full width, then
   continues as a thin flat tail to u 2261 that drifts up to 8 px below the stroke's path; the
   last dash (u 2284 to 2336) continues the path, 7 px above where the tail ends. The Dr 0.95
   sample is in the gap and goes to the nearest dash end, the end of the tail (Dr 0.947, phi
   42.97), with a v bound of 8 px so that the stroke's path is inside it. A reader who takes the
   tail as stray ink would put this sample at the full-width end (u 2239, Dr 0.936) instead.
10. Where curves cross or touch: the three curves never cross or touch one another. The solid
    curve overlaps the top of circle 2 between Dr 0.0 and 0.025 (no sample there besides Dr
    0.00) and ends at circle 7.
11. Specks not read as curve ink: a 1 to 3 px speck at u 983..986 just beyond the end of the
    first lower dash (u 976); small specks at u 2066..2076, v 2249..2253 after the upper dash end
    at u 2062; a short mark at u 1554..1560, v 2684 right of circle 5; a row of dots at u
    1295..1330, v 2857 below the upper dash that starts at u 1278.

## Files

`cal-p1/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv` (piecewise map, with the ink check), `overlay-p1.png`, this file; helpers
`fit_circles.py`, `trace_curves.py` (writes `trace-*.csv`), `sample_curves.py` (writes
`samples-*.csv`), `build_points.py`, `view_trace.py`; crops used for the reading (`lab_*.png`,
`c_*.png`, `left_*.png`, `up_*.png`, `low_*.png`, `mean_left.png`, `v1..v5.png`, `chk_*.png`,
`overview.png`).
