# FA-40, blind reading (Claude), batch curves-appa-b1

Page `p0079.png` (printed A-78). Caption as printed: "Figure A-40. Angle of Internal Friction (as
determined by the direct shear test) Versus Relative Density for LSM Soil". It matches the figures
index. One panel, upright, full grid, no legend.

## What is printed

1. A cross-hatched band (two families of diagonal lines at about plus and minus 45 degrees) filling
   the whole width of the plot, from the left frame (Dr 0) to the right frame (Dr 1.0), between the
   grid line labelled 45 and the grid line labelled 40.
2. The band has no edge lines of its own: its upper and lower edges are the y = 45 and y = 40 grid
   lines. Measured in columns every 7 px along each line, the 45 and 40 lines are 8 px thick
   (median; 10th percentile 6 px), the same as the 50 line (8 px) and close to the 35 and 30 lines
   (7 px); their longer runs (90th percentile 12 to 13 px) are where hatch lines join them. No
   second line is drawn over them, and the ink centre of each sits within 0.3 px of the fitted grid
   line.
3. No plotted symbols and no single solid curve. Series used: `band-top` and `band-bottom`; nothing
   in `data` or `curve`.
4. The figures index row says states "Dr .40 to 1.00". The printed band is not limited to that
   range: the hatching and both edges run from Dr 0 to Dr 1.0. Reported as printed; the ids given
   are kept.
5. So the figure reads as phi = 40 to 45 deg, independent of Dr, over the whole Dr range.

## Calibration (`cal-p1/`)

1. `tools/calibrate_axes.py detect`, box u 770 to 2400, v 1450 to 3400, 10 bands, x values 0 to 1.0
   by 0.2 (left frame to right frame), y values 30 to 50 by 5.
2. The top frame (v about 1268) and the bottom frame (v about 3569) carry no printed labels (by
   spacing they would be 55 and 25). Both are left out of the box and are not anchors. The band is
   between the 40 and 45 lines, well inside the anchored range.
3. All 11 lines detected in 10 of 10 bands; none predicted. Affine residuals: x RMS 0.0029, max
   0.0047 (0.47 percent of the span); y RMS 0.019 deg, max 0.035 deg (0.09 and 0.18 percent of the
   20 deg anchored span). The page is turned about 0.6 deg and the horizontal lines are not quite
   parallel (tilts from -0.0106 for the 50 line to -0.0077 for the 30 line), which the piecewise map
   follows line by line.
4. Piecewise ink check (`cal-p1/knots-ink-check.json`): all 6 x lines and all 5 y lines verified,
   ink found at every position, ink line within 0.91 px of the fitted line at both ends; location
   errors 0.50 to 1.27 px (the largest, 1.27 px, on the 40 line, where hatch junctions touch it).
5. Labels checked by eye (`calibration-eye-checks.csv`): all five y labels and all six x labels.
   The "45" label is about 6 px above its line, the others within 3 px; the x labels have their
   decimal point under the line, the "0" is about 5 px left of the frame.

## Points (`points-p1.csv`, `points-p1-native.csv`)

1. `band-top` and `band-bottom`: 21 trace samples each (left end, Dr 0.05 to 0.95 every 0.05, right
   end) and 2 features each (first point, last point). Bounds 4 px in v (half the 8 px line); 4 px
   in u for the inner samples.
2. Samples located with `helpers/trace.py --line`: in each column the dark run around the fitted
   grid line is taken, columns where a hatch line or a vertical grid line joins it (run longer than
   the local median by more than 1 px) are not used, and the centre at the target Dr is a straight
   line fitted to the clean columns within 8 px. Values: band-top 44.99 to 45.01 deg, band-bottom
   39.99 to 40.01 deg, as they must be on the knot lines.
3. Ends: both edges run into the frames. Each end sample is the column next to the frame ink
   (band-top u 794 and 2334, band-bottom u 798 and 2339), with a u bound that reaches the frame
   centre (7, 6, 6 and 5 px). `piecewise` flags the two right ends `extrapolated x` only because
   those bounds reach past the x = 1.0 line.
4. Features: first and last point of each edge. The edges are straight horizontal lines: no peak
   other than the constant value, no knee.

## Ambiguities

1. Whether the band "ends" at the frame or continues beyond it cannot be told; it fills the plot
   from frame to frame.
2. Specks in the plot, not symbols: a dot of about 6 px at u 1223, v 3110 (Dr about 0.28, phi
   about 31); smaller ones at u 2042, v 2456 and u 1418, v 2514; a short dash and a dot inside the
   band near u 935, v 2258 and u 2128, v 2219. Near the lower right of the band (u about 2140 to
   2195, v 2330 to 2400) some hatch lines are faded and broken; the 40 line there is intact.

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-ink-check.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, crops (`crop-*.png`, `eye-*.png`,
`check-*.png`), helpers in `helpers/`.
