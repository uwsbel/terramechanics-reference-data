# FC-7C reading notes (Claude reader, batch curves-appc-b4)

Figure C-7C, AM-68-1 Vol. II, printed C-23, PDF page 137 (`packet/p0137.png`, 3213 x 4221 px,
300 dpi, unrotated). One panel, horizontal load (psi) against horizontal motion (in), plotted
symbols only. Printed sideways: on the page as scanned, motion increases up the page and load
increases to the left. All pixel coordinates refer to the unrotated page image.

## Calibration (`cal-p1/`)

1. `tools/calibrate_axes.py detect` with `--box 585 1325 2375 3345`, x values 0 to .32 step .04
   (`--x-direction up`), y values 0 to 35 step 5 (`--y-direction left`). 72 anchors.
2. Residuals: x rms 0.00025 in (0.08 % of the 0.32 in span), max 0.0006 in (0.19 %); y rms
   0.017 psi (0.05 % of the 35 psi span), max 0.049 psi (0.14 %). Both under 0.5 %.
3. Directions confirmed by eye on the printed labels (`calibration-eye-checks.csv`): load labels
   30, 25, 15, 0 sit on the fitted lines within 2 px, 0 at the right frame and 30 at the left;
   motion labels .32, .28, .16, .12, .04, 0 sit on the fitted lines within 2 px, 0 at the bottom
   frame and .32 at the top.
4. Two lines were `predicted` by the tool (30 psi and .28 in). Both are drawn on the page and lie
   within 2 px of the predicted positions at the places checked.
5. No 35 label is printed; the left frame line carries 35 psi by spacing (245 px per 5 psi, as
   every other interval).
6. The upper part of the 20 psi grid line bends about 3 to 4 px left of its straight fit above
   v = 1700 (a drawing irregularity). No marker lies near it.
7. Symbols drawn on the .04 in grid rows sit on average about 1 px below the fitted grid line
   (0.0002 in): placement by the drafter, negligible.

## Series and legend

The legend box prints sigma (PSI) and gamma (PCF) only, no symbols: 26.5/82, 13.8/82, 10.2/82,
6.6/82, 5.1/82, 3.4/82. These match the series ids of `series.csv`; no printed number differs.
Each legend entry is printed in line with the last (highest motion) point of one curve, in the
same left to right order, which ties the entries to the symbols:

| series_id | symbol (figure turned upright) | markers | legend entry u | last marker u |
|---|---|---|---|---|
| n26p5psi | quarter-circle | 16 | 1105 | 1126 |
| n13p8psi | star | 17 | 1730 | 1712 |
| n10p2psi | triangle-up (a left-pointing triangle on the page) | 15 | 1875 | 1883 |
| n6p6psi | diamond | 16 | 1995 | 2009 |
| n5p1psi | square | 15 | 2045 | 2066 |
| n3p4psi | circle | 16 | 2140 | 2155 |

Total 95 markers, all `point_kind = marker`, `panel = 1`. Sequence is 1 up in order of
increasing motion (the order of the readings within a test). Every series has readings near
.002 to .005, .01, .02, .03, .04, then every .02 to .20, then near .225 and .25; the star series
continues to about .273 and .30. The values near .225 and .25 are reported as read (they are not
on the .02 spacing). There is no symbol at zero load or zero motion (checked along both frame
lines).

Coarse plausibility check only (not used in the reading): the maximum load of each series (5.0,
6.5, 8.0, 11.9, 15.5, 28.0 psi, in order of normal stress) agrees with the failure envelope
points of Figure C-7A for gamma 82 as seen on `p0135.png`.

## How a center was read

Centers were read on zoomed crops (`tools/plot_grid.py crop`, zoom 2 to 6) and on pixel maps of
each symbol; outer extents were measured with the grid lines masked and checked by eye on
verification sheets (`crops/verify_*.png`). Helpers are in `helpers/` (reader's aids only).

1. circle, square, diamond: center of the outer outline.
2. triangle-up: centroid, one third of the height from the base (on the page the apex points
   left, the base is on the right). The center of the bounding box would be about 5 px toward
   the apex (about 0.1 psi more load); the u bound is 4 px (5 px where the apex or the base is
   hidden in a grid line) to cover this choice of convention.
3. star (one point to the left on the page, so pointing up when upright): geometric center of
   the regular five-pointed star, the mean of (left point + R) and (right edge - 0.809 R), with R
   from the width or the height.
4. quarter-circle: the D-shaped symbol is a quarter disk with straight edges on top and on the
   right of the page and the corner at the top right. Center = area centroid, 0.424 R from both
   straight edges, with the straight edges taken as the median outer boundary (so an arc
   overshoot, as on D08, does not move them). Check on the grid rows: on the five quarter-circles
   that sit on .04, .08, .12, .16, .20 the grid line passes on average 2.4 px above this centroid,
   against 0.5 to 1.5 px for the other symbols on the same rows; if the drafter's reference point
   was nearer the corner, the values are off by about 1 to 2 px (0.0003 in, 0.04 psi), inside
   the 3 px bound.

## Ambiguities and partly hidden symbols (look here first)

1. n26p5psi seq 1 (reader id D16, u 2029.8, v 3293.7, about 0.002 in, 6.6 psi): lower part
   under the bottom frame line, top-right corner overlapped by the left point of the star
   n13p8psi seq 1. Read as a quarter-circle from its straight top edge, straight right edge and a
   left wall that curves right toward the frame. Bound 4 px. If it were not a quarter-circle it
   would be a 96th symbol of unknown series; no other series fits a point at 6.6 psi so near the
   origin, but the identification rests on the shape.
2. n6p6psi seq 1 (M16, u 2218.0, v 3292.5, about 0.002 in, 2.8 psi): top half overlapped by the
   square n5p1psi seq 1, bottom vertex poking out below the frame line. The interior bottom is
   V-shaped and the bottom tip is pointed, so read as a diamond; a circle is the other candidate
   (it would then be a second circle near 0.002 in at a higher load than the circle at 1.2 psi,
   which does not fit that series). Bound 4 px.
3. n13p8psi seq 1 (S17, u 2058.0, v 3285.5): bottom point under the frame line, left point on
   the corner of D16. Center from the right edge and the top point. Bound 4 px.
4. Square and circle pairs that share ink, at about .03, .02, .01 and .005 in (n5p1psi seq 1 to
   4 with n3p4psi seq 2 to 5): the square is the left member (sharp corners, width 29 to 30 px),
   the circle the right member (curved, width 32 to 34 px); where a stroke is shared, the
   strokes were assigned by these sizes. Bounds 3 px in u.
5. n3p4psi seq 1 (C16, about 0.003 in, 1.2 psi): lower part under the frame line; center from
   the widest row and the top. Bound 3 px in u, 4 px in v.
6. Symbols on the .04k grid rows: the left point of stars (S05, S07, S13), the apex of triangles
   (T03, T05, T07, T09, T11) and the side vertices of diamond M07 are hidden in the grid line;
   their centers come from the visible edges (a star's right edge and height, a triangle's
   edges extrapolated to the line). Triangle bounds 5 px in u.
7. n10p2psi T04 (motion .18): the base lies along the 10 psi grid line; its outer edge was taken
   one stroke width (5 px) right of the visible inner edge. Bound 5 px in u.
8. Many symbols carry stray dashes or dots (drafting marks, often a short horizontal tail at the
   lower right); these were excluded from the outlines and are not data.
9. Symbols crossed by grid lines but fully readable are noted per row in `points-p1.csv`; the
   reader id (D01, S01, ...) is in each row's note.

## Files

`cal-p1/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`, `points-p1.csv` (95
markers), `points-p1-native.csv` (from `calibrate_axes.py apply`), `overlay-p1.png`, this file;
working material in `helpers/` (scripts, extents, readings table) and `crops/`.
