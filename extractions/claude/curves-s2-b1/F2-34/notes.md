# F2-34 (Figure 2-34, printed 2-65, PDF 90), blind reading, batch curves-s2-b1

Page image `packet/p0090.png`, 3263 x 4558 px, read unrotated. The figure is printed sideways:
penetration increases up the page, load increases to the left. Everything below is in page pixels
(u right, v down).

## Axis label on this figure

The load axis is titled `Load - Lbs. x 100` (printed upside down under the axis, u 1100 to 1480,
v 3800 to 3830). The numbers printed on the axis are 0, 200, 400, ..., 1200. As instructed, the
numbers were given to the tool as plain `lb` and not multiplied. For what it is worth, the printed
analysis beside the curves (`Intercept = 140 lbs.`, `Slope = 54 lbs./in.`) only matches the axis
read in plain pounds; the `x 100` would put the 4 inch cylinder at 70,000 lb at 6.4 in.

## Calibration (`cal-p1/`)

1. Box 600 1280 2280 3700, `--x-direction up --y-direction left`, bands 7, dark 200.
2. x (penetration): values 0 to 9 on the ten drawn horizontal lines. Labels are printed for 0 to 6
   only; the lines at 7, 8 and 9 in (v about 1825, 1565, 1311 at u 1000) are unlabelled, drawn over
   the left part of the frame (u 620 to about 1600, dashed remnants further right where the text
   block sits), and the top frame line is the 9 in line. They were anchored with the values the
   even spacing gives them (262 px per inch, the same as between the labelled lines) because the
   upper part of LPT 88 (6 to 8.1 in) lies there; a reader who drops them reads that stretch as
   extrapolated. All ten lines were found by the tool (7, 8, 9 in 4 of 7 bands, the others in 6
   or 7).
3. y (load): values 0 to 1200 every 200 on the seven drawn vertical lines; all detected (the 1000
   line in 4 of 7 bands, the text block and the trace crossings hide the rest).
4. Affine residuals: x rms 0.012 in, max 0.029 in (0.3 percent of the 9 in span); y rms 2.0 lb,
   max 5.0 lb (0.4 percent of the 1200 lb span). The grid is tilted about 0.35 degrees (vertical
   lines drift 13 px in u over the frame height); the band fit handles it.
5. By-eye checks in `calibration-eye-checks.csv`: penetration 0, 3, 6 and load 0, 600, 1200, all
   consistent with the fitted lines (every label sits within 30 px of its line, lines are 260 px
   apart). Every label is printed slightly above (penetration) or below (load) its line, none is
   ambiguous.
6. `points-p1-native.csv` holds the piecewise values (D-025; the tool verified all 17 lines on the
   ink); `points-p1-affine.csv` the affine values for comparison. The largest difference between
   the two on the data points is 1.5 lb and 0.016 in.

## Which line carries which label

1. `lpt87` (A LPT No. 87): the thick recorded trace that starts at the origin. The text
   `A LPT No. 87` is printed along it (u 1450 to 1610, v 2330 to 2610, just to its right). It runs
   from the origin along the load axis to about 140 lb at 0.3 in, turns sharply (knee at
   u 2039, v 3589), climbs almost vertically (load 140 to 156 lb from 0.3 to 1.0 in), bends
   gradually between 1.0 and 1.8 in into a steady slope of about 110 lb/in, and ends at
   u 1291, v 1991 (6.35 in, 703 lb). Load rises monotonically, so its peak is its last point.
2. `fit` (`Slope = AγNq = 54 lbs./in.`): the thick straight line from the load axis at 139 lb
   (ink meets the axis line at u 2041, v 3652) to u 1529.5, v 1811 (7.04 in, 519 lb). The leader
   arrow of the Slope label (shaft from u 1665, v 2025 to the arrowhead tip at u 1643, v 2151)
   points at this line, 15 px from its right edge; the thin line is 60 px further. Its line style
   (thick, straight) and the arrow agree, and the read slope (53.9 lb/in) and intercept (139 lb)
   match the printed 54 lbs./in. and 140 lbs., so the identity is not in doubt. The label text
   is printed rotated at u 1645 to 1690, v 1392 to 1997; its center (1668, 1695) is the `label`
   feature, written as `label: Slope = A gamma Nq = 54 lbs./in.` (gamma and the subscript q
   transliterated as in `series.csv`). The label feature is the center of a text block, not a
   point on any line.
3. `lpt88` (B LPT No. 88): the thin recorded trace (3 to 5 px) that starts on the load axis at
   the 2 in grid line. The text `B LPT No. 88` is printed along it, 40 px to its left (u 1440
   to 1600, v 1880 to 2200), and does not touch the line. It ends at u 1347, v 1528 (8.14 in,
   658 lb). Load rises monotonically, so its peak is its last point.

No plotted symbols on this figure; no `marker` rows.

## Where the lines cross or run together (bounds widened, noted in `note`)

1. LPT 87 and the fit line cross between v 3010 and 3075 (2.2 to 2.5 in); the 2.25 in sample
   of LPT 87 (v 3065) is on the merged run. Below the crossing the fit is to the left (higher
   load) of LPT 87; above it LPT 87 is to the left.
2. LPT 88 leaves the 2 in grid line at u 2100, bends and joins the fit line at about u 1888,
   v 3060, then runs along the right side of the fit line up to v 2950 (2.25 to 2.7 in). The
   2.5 in sample is on the merged run; at 2.75 in the thin line is 2 px clear of the fit.
3. LPT 88 crosses the fit line from right to left between v 2620 and 2456 (3.9 to 4.6 in),
   hidden under it; the 4.0, 4.25 and 4.5 in samples are read on the merged run with the bound of
   the merged run. From 4.6 in up LPT 88 is left of (above) the fit, 10 to 60 px away.
4. The start of LPT 88 lies on the 2 in grid line from the load axis (u 2216) to u 2100; the
   trace shows above the grid line only at u 2201 to 2216, 2131 to 2148 and 2090 to 2119
   (rows 3122 to 3124). The first point is placed at u 2210, v 3125 with an 8 px u bound. The
   whole shallow stretch (load 0 to about 95 lb at 2.0 in) falls between the 2.0 and 2.25 in
   samples; the 0.25 in sampling does not reach it, and I did not add rows for it.
5. Samples that fall on a vertical grid line (LPT 87 at 1.75 in on 200 lb, at 3.75 in on 400 lb,
   at 5.5 in on 600 lb; the fit at 5 in on 400 lb; LPT 88 at 4.75 in on 400 lb) are noted; at
   3.75 in the merged run was split using the grid line's known position.
6. Samples at whole inches sit on a horizontal grid line; their u was interpolated from the
   runs 9 px above and below the line (noted `interpolated`).

## Features

1. LPT 87: first (origin), knee at the end of the shallow start (u 2039, v 3589, about 0.25 in,
   141 lb), a second, gradual knee where the near-vertical stretch bends into the steady slope
   (placed at u 1995, v 3300, 1.34 in, 173 lb, with a 40 px v bound because the bend spreads
   from v 3400 to 3200), peak = last (u 1291, v 1991).
2. Fit: intercept on the load axis (u 2042.5, v 3657, 139 lb), label center.
3. LPT 88: first (on the axis at the 2 in line), knee where the shallow start turns to run along
   the fit line (u 1888, v 3060; the bend spreads from u 2100 to 1890 so the bound is 10 px),
   peak = last (u 1347, v 1528).

## Bounds

Half the measured line thickness at each sample (LPT 87 and the fit 7 to 10 px thick, so 4 to 5
px; LPT 88 3 to 5 px thick, so 2.5 to 3 px); the half width of the merged run where two lines run
together; a wider u bound where a line is shallow across the sampling row (LPT 87 at 0 in, LPT 88
at 2 in).

## Ambiguities

1. The values of the unlabelled 7, 8 and 9 in lines are inferred from the even spacing (item 2 of
   the calibration section). Without them, LPT 88 above 6 in would be extrapolated.
2. The `Load - Lbs. x 100` axis title (recorded, not applied).
3. The second knee of LPT 87 and the knee of LPT 88 are gradual bends; their locations are
   approximate and the bounds say so.
4. Where LPT 88 is hidden under the fit line (3.9 to 4.6 in and 2.25 to 2.7 in) its samples are the
   merged run's center, which is the fit line's center; the thin line could sit anywhere inside the
   thick line's width there.

## Files written (all under `out/F2-34/`)

`cal-p1/calibration.json`, `cal-p1/anchors.csv`, `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv` (piecewise), `points-p1-affine.csv` (affine, for comparison),
`overlay-p1.png`, `notes.md`, `crops/` (zoomed crops used for the reading), `helpers/`
(`rowscan.py`, `pixdump.py`, `extract.py` with `guides.json`, `build_points.py`).
