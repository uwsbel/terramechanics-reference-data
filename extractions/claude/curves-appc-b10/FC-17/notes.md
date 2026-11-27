# FC-17, blind reading (Claude), batch curves-appc-b10

Page `p0153.png` (PDF page 153), printed page C-39. Caption as printed: "Figure C-17. Angle of
Internal Friction vs. Relative Density". One upright panel. Printed inside the plot, upper left:
"PS Soil". Axis titles as printed: y "phi_DS - Degrees" (Greek phi, subscript DS), x "D_r". No legend
is printed on the page (the figures index lists legend entries "circles; average; limits"; on the
page these are only line styles, identified below by the convention in TASK.md).

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect` with box u 775 to 2560, v 1300 to 3555 (inside the frame, so the
   outermost tracks are the labelled lines 0 and 1.0, 30 and 50; the frame lines carry no label and
   are not anchors), 20 bands, x values 0, 0.1, ..., 1.0, y values 30, 35, 40, 45, 50. Every line
   detected (19 or 20 of 20 bands), none `predicted`; 55 anchors.
2. Affine residuals: x rms 0.0014, max 0.0038 (0.38 percent of the 0 to 1.0 span); y rms 0.013 deg,
   max 0.023 deg (0.11 percent of the 30 to 50 span). Both under 0.5 percent.
3. Ink check (`check_knots.py`, the tool's own `piecewise_maps` with the page image): all 11 x lines
   and all 5 y lines verified, ink found at every checked position; location errors 0.5 to 0.8 px
   except x = 0.4 (1.65 px; the ink's line is 1.3 px off the fitted line at both ends, with opposite
   signs, so a slightly different tilt) and x = 0.9 (1.49 px). Record in `cal-p1/knots-check.json`.
4. The grid is drawn unevenly: the spacing of the x lines varies from 148.5 to 159.5 px per 0.1
   (measured near the top of the plot), hence the piecewise map. The scan is tilted: vertical lines
   lean about +0.015 to +0.021 px per px, horizontal lines about -0.014.
5. By-eye label checks: all 11 x labels and all 5 y labels, in `calibration-eye-checks.csv`. The "0"
   on the x axis is printed 14 px left of its line (the nearest other line, the frame, is 148 px
   away, so there is no ambiguity); the others sit within 10 px of their lines.

## Frame beyond the labelled lines

The frame extends past the labelled lines on all four sides, by about one grid interval each, and
none of the frame lines carries a label (values from the piecewise map, extrapolated):

1. left frame at about x = -0.096, right frame at about x = 1.099;
2. top frame at about y = 55.0, bottom frame at about y = 25.0.

The right frame line has a small jog near v 1720 to 1745 (it steps right by a few px).

## Which curve is which

1. `upper`: the dashed curve above the solid one; from (x 0.002, y 44.84) to (x 1.094, y 51.12).
2. `mean`: the solid curve; from (x -0.009, y 42.91) to (x 1.095, y 49.31).
3. `lower`: the dashed curve below the solid one; from (x -0.012, y 41.23) to (x 1.107, y 48.17).

The three curves run the full width of the plot, from about x = 0 to the right frame (about x = 1.1),
rising monotonically with a gentle upward curvature at the left; no knee, no peak other than the
last point. They do not touch or cross one another.

## Markers (series `data`)

Six circles, centres fitted on the ring (`circles.py`, rays every 5 degrees, rms 0.35 to 0.64 px):

1. (0.164, 43.42) single. The solid curve runs over the top of the ring and merges with it; bound 3 px.
2. (0.294, 43.80) single. The x = 0.3 grid line runs through the right part of the ring; bound 2.5 px.
3. (0.314, 46.47) pair 1 left. Joined by a horizontal line to marker 5. The x = 0.3 grid line touches
   its left side; the upper dashed curve passes behind its top. Bound 3 px.
4. (0.382, 43.50) single. Sits in a gap of the lower dashed curve (the curve is interrupted around
   it); the ring does not touch the curve ink.
5. (0.518, 46.49) pair 1 right.
6. (1.141, 49.73) **outside the frame**, 64 px right of the right frame line, beyond every labelled
   line (x extrapolated). Symbol recorded as `circle-dot`: the ring is heavier than the other
   circles and has a dot at its centre. It may be a data point plotted beyond the frame (Dr above
   1.0, between the solid and the upper dashed curves extended) or a mark that is not data (a
   reproduction or registration mark); the page does not tell. Flagged for review; it should not
   enter `data/` as an observation without a person's decision.

No circle is cut by the frame. Pair 1 is the only joining line; one friction angle (about 46.5 deg)
over Dr about 0.31 to 0.52.

## Trace samples

Samples at the left end, every 0.05 of x, and the right end: 23 (upper), 24 (mean), 25 (lower).
Centres are the middle of the curve's ink in each pixel column, a straight line fitted over the
clean columns within 6 px (`track.py`, `sample.py`); bound in v is half the line's vertical run
(3 to 5 px), in u 1 px (2 px at a dash end, 1.5 to 3 px at a curve end).

1. Grid-line crossings: where a sample falls on a vertical grid line (every 0.1 of x), the centre is
   bridged from the curve's ink on both sides of the line, within 14 px. Where a curve merges with a
   horizontal grid line its centre is read from its free edge (the edge outside the grid line) minus
   half its thickness: upper x = 0.05 (merges with the 45 line from u 895 to 950; bound 5 px), mean
   x = 0.4 (the curve crosses the x = 0.4 and the 45 lines at the same place; bound 5.5 px).
2. Dashed curves, samples moved to the nearer dash end (rule 7), on the ink:
   - upper: x = 0.1 (to u 1050, x 0.114), 0.2 (to u 1180, x 0.197), 0.3 (to u 1337, x 0.296), 0.5
     (to u 1634, x 0.492);
   - lower: x = 0.1 (to u 1019, x 0.090), 0.4 (to u 1506, x 0.403), 0.5 (to u 1677, x 0.516).
3. Dash ends that meet a grid line or a symbol:
   - upper: one dash ends at the x = 0.3 grid line just left of circle 3 (u 1337), the next starts
     at the circle's upper right; the gap u 1338 to 1379 is the circle and the grid line. The dash
     ending at u 1180 stops 2 px short of the x = 0.2 line.
   - lower: the dash after circle 4 starts at the right edge of the x = 0.4 grid line (u 1503); the
     dash ending near u 1832 to 1843 runs into the 45 grid line and its end is hidden in that line
     (no sample depends on it).
4. Curve ends:
   - upper starts at the right edge of the x = 0 grid line (u 880); whatever part lies under the
     line cannot be seen, nothing shows left of it. Ends at the inner edge of the right frame
     (u 2570); nothing shows beyond the frame.
   - mean starts 11 px left of the x = 0 line (x -0.009); ends at the inner edge of the right frame
     (u 2573).
   - lower starts 12 px left of the x = 0 line (x -0.012); its last dash runs through the right
     frame line and ends 8 px beyond it (u 2593, x 1.107). Its x = 1.1 sample (u 2583) is inside
     the frame line, bridged from the dash on both sides.
5. Values beyond x = 1.0, beyond y = 50 or left of x = 0 are extrapolated from the outermost verified
   lines and flagged in `cal_model` (22 rows).

## Ink that is not a curve

1. A small cross-shaped speck at about (u 2373, v 1622), in the gap of the upper dashed curve after
   the dash ending at u 2362. Thin (1 to 2 px), not a dash; not used.
2. A speck at (u 1220, v 2271) just above the lower curve; dropped (a 1-column run).
3. A row of small specks below the solid curve near u 2322 to 2390, v 1783; not used.

## Files

`points-p1.csv`, `points-p1-native.csv` (piecewise map with the page image), `overlay-p1.png`,
`calibration-eye-checks.csv`, `cal-p1/` (anchors, calibration, ink check). Helpers: `track.py`,
`sample.py`, `circles.py`, `check_knots.py`, `assemble.py`; intermediate `tr_*.json`, `samp_*.csv`;
zoomed crops in `crops/`.
