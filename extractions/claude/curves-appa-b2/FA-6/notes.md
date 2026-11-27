# FA-6, blind reading (Claude), batch curves-appa-b2

Figure A-6, "Average and Range for Three Samples of Unused PS Soil", printed page A-13, page image
`p0014.png` (300 dpi, unrotated). The caption, page number and title match the figures index row. The
legend entries of the index (Average; Range) are not printed as a legend on the page; the solid curve is
the average and the two dashed curves the range, as TASK.md says. Series ids used as given: `average`,
`upper`, `lower`.

## Frame, labels and calibration

1. The figure is printed sideways. On the page as scanned, grain size increases up the page and percent
   finer to the left (`--x-direction up --y-direction left`), log grain-size axis (`--x-transform log10`).
2. Grain-size labels printed along the right side: 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0,
   5.0, 9.0. Each sits on a horizontal line whose tick runs out past the frame. These twelve lines are the
   x knots. The bottom frame carries the label 0.02. The topmost label is printed **9.0** (not 10); its line
   is where 9 mm falls on the spacing of the other labelled lines (about 976 px per decade). The top frame
   (v 1127.5) carries **no label**; by the log spacing it is 10 mm. It is not anchored. The dashed line
   just under it (v 1152.5) is the 3/8 inch sieve line, labelled in the sieve column; not anchored. No
   other sieve line or unlabelled subdivision is anchored.
3. Percent labels 0 to 100 every 10 are printed above and below the plot (sideways); the left frame is
   labelled 100 and the right frame 0, at both ends. The labels sit 1 to 7 px off their lines; each is
   nearest its own line (lines 146 px apart).
4. The parameter table covers the plot from about u 1060 to 1697, v 2246 to 3644, and blanks the grid
   there. Its left edge runs 3 to 16 px beside the 80 percent line and its right edge 3 to 8 px beside the
   40 percent line. On the page as scanned the detector followed the table edges inside the table's
   height (80 percent line fitted with the wrong tilt, 13 px off at the bottom, and still passed the ink
   check, because the check found the table edge). So detection was run on a copy of the page with the
   table and its white surround set to white (`p0014-table-masked.png`, written by
   `helpers/mask_table.py`; same size, pixel coordinates unchanged). `calibration.json` names that image.
5. Detection: box 778 1162 2275 3762 (top edge between the 3/8 inch line and the 9.0 line, so the 9.0
   line is the outermost track), 35 bands, min-frac 0.7, frame-frac 0.35. These settings were chosen from
   a scan of bands 15 to 50 and min-frac 0.5 to 0.7 as the run in which every labelled line passes the
   ink check with the smallest offsets; other settings let curve ink pull the 1.5 and 2.0 mm lines or the
   50 percent line (rejected by the ink check). All 23 lines detected, none predicted.
6. Affine residuals: x rms 0.0024, max 0.0056 in log10 units (0.21 percent of the 2.65-decade span);
   y rms 0.060, max 0.18 percent. Ink check (D-025) on the masked page: all 12 x and 11 y lines verified,
   ink-line offsets at most 0.82 px. On the page as scanned the 40 and 80 percent lines are rejected
   ("misplaced", 3.3 and 2.5 px) because the table edges are counted as their ink; values computed with
   that page differ from the delivered ones by at most 0.009 percent finer and 0 in grain size, so it does
   not matter here. `points-p1-native.csv` was written by `calibrate_axes.py piecewise` with
   `--image p0014-table-masked.png`. Piecewise and affine values differ by at most 0.14 percent and
   0.75 percent of grain size.
7. 14 points lie left of the 100 percent line and are flagged `extrapolated y` (see below).

## Which curve is which

The scan is bilevel and the three curves are drawn with a heavy pen (about 11 px across) only 10 to 15 px
apart, so over most of their length they touch. Their order is fixed: `upper` has the higher percent
finer at a given size.

1. Steep part (about 1.0 to 3 mm, curves nearly horizontal on the page): `lower` is the top strand on the
   page, `average` the middle, `upper` the bottom strand. The two dashed curves have dashes about 45 to 55
   px long with their gaps roughly in step, and in those gaps the solid line shows alone (a single 11 to
   12 px run midway between the dashed curves), which is what identifies it.
2. Knee (about 0.9 to 1.3 mm): the three strands separate clearly (rows v 2052 to 2200): `upper` left,
   `average` middle, `lower` right.
3. Tail (fine end, curves nearly vertical, next to the 0 percent frame): `upper` left, `average` middle,
   `lower` right.
4. Coarse end: the curves run up the 100 percent line. `lower` leaves it first (from about 3.6 mm,
   v 1555), `upper` and `average` stay on it to about 3.0 mm (v 1640).

## Where they run together (bounds widened, said in each point's note)

1. Fine end, below about 0.3 mm (v > 2600): the band is under 22 px wide, i.e. the three curves overlap;
   all three series get the band centre with a bound of half the band. Below about 0.16 mm the band is
   one line width (2237 to 2249) and the curves end together at (2241.5, 2945), about 0.134 mm and
   1 percent: the first point of all three traces.
2. Coarse end, above about 3.2 mm: all three on the 100 percent line, merged with the frame. The ink
   extends 8 to 14 px left of the frame (u 776 to 787), so the outer (upper) edge of the curves is drawn
   slightly beyond 100 percent; samples there read 100.3 to 100.7 percent and are flagged `extrapolated y`.
   The ink ends at (780.5, 1514.5), about 4.07 mm: the last point of all three traces.
3. Knee entrance (about 1.25 to 1.3 mm, u 2030 to 2110): the curves cross the dashed 1.18 mm (No. 16) sieve
   line and partly merge; points there carry 7 to 9 px bounds.
4. Where the solid line is not seen on its own (its observations are sparse around u 1240 to 1340 and
   1780 to 1830 and absent in the tail from v 2340), it is placed between the dashed curves with a bound
   of half their distance, noted "solid line not seen on its own".

## Method (aids, not values)

Visual aids under `helpers/` (all keep page pixels): `degrid.png` (grid ink erased where it crosses white,
drawn grey), `steep3.py` (per column: outer edges of the band, robust asymmetric spline envelopes that set
aside dash gaps, the rows of major and dashed grid lines and the two circles not used as edges),
`tail3.py` (the same per row in the tail), `centerlines.py` (dashed centrelines = envelope +- 5.5 px, the
half pen width; solid line = robust spline through its own observations), knee and coarse-end points read
by eye from page row and column runs (listed in `build_points.py`), `build_points.py` (sampling).
Samples: every 0.05 decade from 10^-0.85 to 10^+0.60 mm, plus every 5 percent where a curve rises more
than 10 percent between two of them. A dashed-curve sample that fell in a dash gap was moved to the
nearest dash end (rule 7; 10 for `upper`, 8 for `lower`, said in the note, so the sample's grain size or
percent is not exactly the target). Three samples whose band centre fell in white between two strands
(v 2827) were moved onto the strand on their series' side. Bound: 6 px (half the line) where the curve is
on its own ink, wider where merged or inferred.

## Markers

Five open circles, all on or just outside a dashed curve, none on the solid curve (centres read on crops
`m1`, `m2`, `m3`, `kt`, `ci_2900`):

1. (2162, 2033), about 1.18 mm, 6 percent: on `lower`, at the knee; the curve passes through it.
2. (1714, 1891), about 1.66 mm, 37 percent: touches the outer edge of `lower`, centre about 11 px outside
   its centreline. Assigned to `lower` by position; it is not centred on the line.
3. (1560, 1906), about 1.60 mm, 47 percent: touches the outer edge of `upper`, centre about 8 px outside.
4. (2229, 2179), about 0.84 mm, 1.6 percent: on the right (lower) strand, partly merged; bound 6 px.
5. (2229, 2904), about 0.15 mm, 1.8 percent: on the left edge of the merged band near the fine end;
   assigned to `upper` by its side of the band only. Bound 6 px.

A narrow hollow loop at (812, 1630) on the `lower` curve near the coarse end is not a circle (12 by 23 px):
read as a dash with a white speck, not as a marker.

## Features (per series)

First point (merged, all series), knee on the fine side, knee on the coarse side, last point. The knees are
a construction (where the drawn line runs at 45 degrees on the page between its two straight stretches),
with 12 px bounds; the peak is the last point at 100 percent.

## Check against the printed parameter table (not read as points)

From the delivered average trace: D10 1.17 mm, D50 1.72 mm, D60 1.86 mm, D95 2.60 mm, Cu 1.59. The
table prints D10 1.2, D50 1.8, Cu 1.6, D95 2.7 mm. D10 and Cu agree; D50 and D95 in the table are about
4 percent coarser than the drawn solid curve. At 2.7 mm all ink of the three curves lies above 95 percent
(on the row of 2.7 mm the band's right edge is at u 861, 95.2 percent; the ink just right of it is
the 95 percent grid line), so the printed D95 does not come from the drawn
curves as scanned; the `lower` curve gives 1.80 and 2.66 mm. Reported as found, not adjusted.

## Ambiguities for review

1. Solid-line position where it is not seen alone (notes say so); a reader who places it on one of the
   strands could differ by up to half the band.
2. Tail below 0.3 mm and coarse end above 3.2 mm: the three curves are not separable; all three carry
   the same position there.
3. Markers 2 and 3 are off the centrelines by 8 to 11 px; markers 4 and 5 are partly merged with the
   band.
4. Index row: nothing printed differs from it.
