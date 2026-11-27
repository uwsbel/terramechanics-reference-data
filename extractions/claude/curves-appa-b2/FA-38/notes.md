# FA-38, panel 1: reading notes (Claude, blind reader)

Page `p0077.png` (3213 x 4558 px, 300 dpi), printed page A-76. Caption as printed: "Figure A-38. Average
and Range of Seven Samples of LSM", matching `figures-rows.csv`. The running head of the page reads
"GRAIN SIZE ANALYSIS CURVES - LM SMS". There is no legend box on the page: the identities below come
from the line styles (one solid curve, two dashed curves) and `series.csv`.

## Calibration (`cal-p1/`)

1. Run as scanned, sideways: `calibrate_axes.py detect --box 672 1157 2185 3762 --x-direction up
   --y-direction left --x-transform log10 --bands 20 --frame-frac 0.4 --dark 128`, printed values
   x = 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 9.0 mm and y = 0 to 100 by 10 percent.
   Only labelled lines were given. The unlabelled log subdivisions (6, 7, 8, 0.6 to 0.9, and so on)
   and the dashed U.S. sieve lines were left out.
2. The box starts at v 1157 so that it leaves out the top frame (v 1119 to 1127). That frame has no
   label. The 9.0 label sits on the heavy line 46 px below it (v 1166 at u 2150), and the frame falls
   where 10 mm would on the log spacing. The bottom frame carries the 0.02 label and is anchored. The
   left frame is labelled 100 and the right frame 0, at both ends, and both are anchored.
3. The Grain Size Parameters table is printed inside the plot frame (u 1345 to 1925, v 1262 to 2735).
   Its own rules lie close to grid lines: a vertical rule 8 to 10 px right of the 50 percent line,
   another near the 40 percent line, a row rule 3 to 8 px below the 3.0 mm line and one near the
   1.0 mm line. detect's band tracks picked these up inside the table. Its 50 percent line came out
   with tilt 0.0019 against about 0.0065 for clean lines (12 px off at the top), and the ink check
   rejected its 1.0 mm, 20 and 30 percent lines. detect's own output is kept in `cal-p1-detect/`.
   `refit_lines.py` (reader helper, in this folder) refits every line on the ink outside the table
   (`calibrate_axes.ink_offset`, unmodified tool, every 10 px, robust fit). Anchors are the
   intersections where both lines are printed: the 28 intersections inside the table are left out.
   The 50, 40, 30 and 20 percent lines also get two one-axis anchors each on their own ink above the
   table (v about 1195 and 1225), so the ink check has support above the table.
4. Result: 112 anchors. Affine diagnostic RMS residual 0.0024 log10 units in x (max 0.0050; 0.09
   percent of the 2.65-decade span, about 2.3 px) and 0.069 percent in y (max 0.20). The x residual
   reflects uneven drafting of the log paper: 963 to 993 px per decade between labelled lines. The
   piecewise map follows that unevenness. The tool's ink check verifies all 23 lines (12 x, 11 y).
   Location errors are 0.50 to 0.75 px, except 1.25 px for the 1.0 mm line and 1.27 px for the
   60 percent line, where the curves cross.
5. By eye (`calibration-eye-checks.csv`): every printed label lies on its line within 6.4 px, against
   a 145 px spacing in y and 80 px or more between x lines.
6. Values in `points-p1-native.csv` come from `calibrate_axes.py piecewise cal-p1 ... --image`.
   Piecewise and affine values differ by at most 0.8 percent (relative) in grain size and 0.11 in
   percent finer.

## Which curve is which

1. In the bottom part (v 2750 to 3190, grain size 0.075 to 0.2 mm) the three curves are drawn
   separately, 15 to 35 px apart. The middle stroke shows ink on every clean row from v 3125 to 3189
   and is continuous through the stretches checked above that. The left and right strokes break into
   dashes about 25 to 45 px long with gaps of about 6 to 14 px. Middle = solid = `average`. Left
   (higher percent finer) = `upper`. Right = `lower`. The ids in `series.csv` match the page.
2. From about v 2740 up to the top (grain size 0.22 to 6.3 mm), the three curves run together in one
   black band 21 to 45 px wide. Each line is 10 to 12 px across, so this is three lines side by side
   or overlapping. Wherever the band shows two groups split by a thin white gap, or a single stroke
   where both dashes are in a gap, those are used. Elsewhere, upper = band left edge + 6 px,
   lower = band right edge - 6 px and average = band middle, with u bound 6 px. The notes of those
   rows say "run together".
3. Near the top (above v 1373, grain size above about 5.6 mm) the average and lower run together as
   one stroke 11 to 12 px wide. Both series get the same pixel there, with the bound widened to 9 px
   at the 5.62 mm sample. A short stub at u 719, v 1373 may be the top end of a separate lower dash.
   It is not distinguishable from a grid stub (u 721 to 723), so it is not read as one.
4. The upper curve's last dash runs to the left of the 100 percent frame line (u 689 to 697). It
   crosses the frame at about v 1358 and ends at u 684.5, v 1325, which is 100.5 percent as drawn. It
   is read as drawn, and those values are flagged `extrapolated y` in `cal_model`.

## Sampling

1. Samples are taken every 0.05 decade from 0.0794 mm (k = -22) to 6.31 mm (k = 16): 39 per curve.
   The fine-end first point and the coarse-end last point are added. No step rises by more than
   10 percent, so no extra samples were needed. Each sample row is the line of constant grain size
   from cal-p1, evaluated at the sample's own u.
2. Dashed curves (rule 7): when the sample row falls in a visible dash gap, the sample moves to the
   nearest visible dash end. The dash end is hidden under a grid line for some samples: upper at
   0.1, 1.0, 2.0 mm; lower at 0.0794 (end under the line at v 3158 to 3163), 0.1, 0.2, 1.0, 2.0,
   5.0 mm. Those samples sit on the line through the dash, with v bound 4.5 to 5 px, and the note
   says the end position is hidden.
3. Ends: all three curves end at the fine end at the #200 sieve line (0.075 mm, v 3191 to 3198). No
   ink lies below v 3199. The upper ends in a visible dash tip at v 3189. The average and lower run
   into the grid line, so their v bound is 4. At the coarse end all three end at the #3 sieve grid
   line (6.35 mm, v 1317 to 1324). Their tips are visible at v 1325.
4. Bounds: u 5 / v 5 px (half the line thickness) on separate strokes. u 6 px where a stroke touches
   a grid line or another curve, or inside the merged band. 9 px for the lower curve at 5.62 mm.
   Smaller v bounds are used at dash ends.
5. Features: first point and last point for each curve. The last point is also the maximum. The
   curves rise steadily with no knee.
6. Markers: none. No plotted symbols are on the curves.

## Counts

Per series (upper, average, lower): 41 trace samples, 2 features, 0 markers; 129 rows in all.

## Observation (not a reading)

The table on the page gives average D50 = 0.07 mm and range 0.06 to 0.08 mm. The curves as read
start at 0.074 to 0.075 mm, at 53.0 (upper), 49.8 (average) and 48.7 (lower) percent finer. The
average therefore reaches 50 percent only at its fine end. The table's D50 values are consistent
with that.

## Files

`cal-p1/` (calibration.json, anchors.csv), `cal-p1-detect/` (detect's unrefitted output),
`calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, this file.
Reader helpers (not tools): `refit_lines.py`, `calmap.py`, `rowprof_lib.py`, `rawprof.py`,
`rowsraw.py`, `probe.py`, `make_points.py` (the readings and their per-sample notes), `knotcheck.py`,
`sheet.py`, `viz.py`, `viz2.py`, `tracker.py`, `tracks.py`, `rowink.py`, `rowcrops.py`. Crops
(`r_*.png`, `s_*.png`, `g_*.png`, `ov_*.png`) were used for the by-eye checks. `affine-check.csv`
is the affine diagnostic of the same points.
