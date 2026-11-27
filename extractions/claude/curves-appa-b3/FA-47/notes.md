# FA-47, panel 1: reading notes (Claude, blind)

Page `p0096.png`, printed A-95, "Figure A-47. Density Versus Relative Density for RSM Soil" (the
figures index gives the soil as RSM-b; the caption prints "RSM").

## What the page prints

1. The unit-weight axis runs downward from **55 at the top to 115 at the bottom** (labels every 5
   on both sides, left "Minimum Density, gamma min (pcf)", right "Maximum Density, gamma max (pcf)").
   TASK.md describes the density charts as 25 to 65 pcf; this figure is not. Spacing reciprocal,
   so `--y-transform reciprocal --y-direction down` with the printed values.
2. Four light lines between every two labelled lines, one per pcf, from 55 to 115. Dr 0.0 to 1.0,
   a vertical line every 0.1, each labelled.
3. Three lines, a solid one between two dashed ones, converging toward the right frame. The page is
   scanned about 1.3 degrees off square (horizontal lines fall 0.021 to 0.025 px per px to the
   right); the tool fits each line with its own tilt.

## Calibration (`cal-p1/`)

1. Box u 840 to 2290, v 1030 to 3700: the whole plot frame, every 1 pcf line named (55 to 115) and
   the 11 Dr lines. A box around the data region alone cannot be used here: with the 1.3 degree tilt
   the 90 and 91 lines drift 34 px across the plot while lying 33 px apart, so no rectangle holds one
   and excludes the other.
2. Result: the lines 55 to 103, 105, 107 to 110 and 115 detected (10/10 or 9/10 bands) and verified
   against the ink (25/25 positions, 17/25 for the thick 115 frame; location errors 0.5 to 1.43 px).
   104, 106 and 111 to 114 fall outside the tool's matching window and stay `predicted`, so they are
   not knots; they are all below the data (the data lie between 73 and 90, where every line is a
   knot). Dr lines 0.0 to 0.9 verified; **the right frame (Dr 1.0) is rejected by the ink check**
   ("misplaced: 2.40 px from the ink's line at an end"): the frame is slightly curved (its ink lies
   3 px left of the straight fit at the top and 2 px right at the bottom). So x beyond 0.9 is
   extrapolated from the 0.8 to 0.9 interval (`cal_model` says so); the right-end samples, on the
   frame, read Dr 0.9987.
3. Affine diagnostic: x rms 1.22 px (0.09 % of span), max 5.07 px (0.37 %); y rms 2.27 px (0.09 %),
   max 6.48 px (0.25 %).
4. Sensitivity (`helpers/cal-labelled-only`, the 13 labelled lines, all verified, the right frame
   rejected the same way): no value changes by more than 0.16 pcf (largest at Dr 0.9).
5. By-eye label checks in `calibration-eye-checks.csv`: y labels 70, 75, 85, 90 within 4 px of their
   lines (ticks on the lines); x labels 0.0 (0.3 px), 0.5 (8 px left of its line), 1.0 (21 px left
   of the right frame, the eleventh line).

## Which label belongs to which line

| series | drawn | left end (Dr 0) | right end (Dr 1.0) |
|---|---|---|---|
| upper | dashed, above | 73.5 | 89.4 (single label, see below) |
| mean | solid | 74.4 | 89.4 (shared, inferred) |
| lower | dashed, below | 75.3 | 89.4 (shared, inferred) |

Left: each leader ends at the frame where its line starts (73.5 at v 2337, 74.4 at v 2383, 75.3 at v
2440; the lines meet the frame at v 2336, 2383, 2434). The axis label 75, with its tick on the 75
line, is printed between 74.4 and 75.3 and belongs to no line.

Right: the page prints **one** value, 89.4, with one horizontal leader (v 2961) starting just
outside the frame. The three lines converge but do not meet: at the frame the upper line ends at v
2959, the mean at v 2967 and the lower at v 2973 (the mean and lower strokes merge from u 2220 on).
The leader is at the level of the upper line's end. I attached the 89.4 label feature to all three
series, because the figure prints a single right-end value for the three converging lines and
TASK.md asks for one label feature per line end; for the mean and lower lines that attribution is an
inference and their notes say so. An adjudicator may prefer to keep it on the upper line only.

## The drawn ends against the printed values

| series | Dr 0 read | printed | Dr 1.0 read | printed |
|---|---|---|---|---|
| upper | 73.57 | 73.5 | 89.27 | 89.4 |
| mean | 74.49 | 74.4 | 89.48 | 89.4 (shared) |
| lower | 75.57 | 75.3 | 89.62 | 89.4 (shared) |

Bounds 0.07 to 0.13 pcf. **The lower line starts 0.27 pcf (12 px) below its printed 75.3**: it meets
the frame 25 px below the 75 line and 18 px above the 76 line, and the 75.3 leader ends at that
level (v 2440), not at the level of 75.3 (about v 2422). So it was drafted there; the reading reports
the ink. The other ends agree with the labels within 0.1 to 0.2 pcf. The labelled-only map gives
the same picture (73.54, 74.47, 75.52 at Dr 0).

## How the samples were taken

1. Each line is straight within 1 px (straight fit to its grid-free ink, rms 0.7 to 0.8 px; every
   100 px stretch within 0.85 px of it, columns where the mean and lower lines merge left out). The
   sample's centre is the fit plus the median residual of the clean ink within 50 px (100 px near the
   right end, where the mean and lower merge). Vertical thickness 6 px, bound 3 px in u and v; label
   features 5 px.
2. Dr 0.1 to 0.9: the crossing with the Dr grid line where the dash covers it. Moved samples (all
   with the distances in their notes): upper Dr 0.1 (dash starts at the grid line; first visible
   ink, u 1031) and 0.2 (gap; next dash start); lower Dr 0.1 (gap; next dash start, 12 px against
   14 px to the previous end), 0.2 (dash ends at the grid line; last visible ink), 0.7 (dash starts
   under the grid line; first visible ink), 0.8 (gap; next dash start) and 0.9 (gap; previous dash
   end). The rest are crossings on ink.
3. Ends: the end samples (and the first/last point features) are on the frame lines' centres; the
   first visible ink is at the frame's inner edge, 3 to 5 px inside. The right frame line used is the
   tool's fit, within 2.4 px of the ink.
4. Labels: one feature per printed end label, at the centre of its characters.

## Ambiguities

1. The single right-end label 89.4 (above).
2. Lower line, Dr 0.1: the crossing is nearly midway in its gap (12 px to the next dash, 14 px to the
   previous); the sample is on the nearer.
3. Lower line, Dr 0.8: a 2-column, 3 px stub on the line's path just right of the 0.8 grid line (u
   2009 to 2010), separated from the next dash by 6 px of white, is read as grid-line ink; if it is
   the start of a dash, the nearest dash end is there (8 px closer).
4. Upper line, Dr 0.1: the first columns of the dash after the grid line (u 1030 to 1034) are thin,
   so the dash start is uncertain by about 4 px.

## Counts

Per series: 11 trace samples and 4 features (first point, last point, left label, right label 89.4).
45 points.

## Files

`cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv` (piecewise map
with `--image`), `overlay-p1.png`, `crops/`, `helpers/` (scripts, the labelled-only calibration,
`points-p1-native-labelled.csv`, and `cal-70-115`, a trial box from the 70 line to the frame that
gave the same lines and the same rejected right frame).
