# FC-5B blind reading (Claude), AM-68-1 Vol. II, Fig. C-5B, printed C-16, PDF 130

Page image `packet/p0130.png`, 3213 x 4221 px, 300 dpi, unrotated. SS soil, Dr .02 to .13.
Upper panel: shear stress tau (psf) vs shear displacement (x 10^-3 in.). Lower panel: dilation
displacement (x 10^-3 in.) vs shear displacement. Five tests, one series each.

## 1. Calibration

| panel | box (u0 v0 u1 v1) | values | bands / min-frac / snap | rms x | max x | rms y | max y |
|---|---|---|---|---|---|---|---|
| 1 | 645 955 2180 2475 | x 0..250 step 50; y 0..5000 step 1000 | 22 / 0.45 / 6 | 0.952 (0.38 %) | 1.696 (0.68 %) | 3.59 psf (0.07 %) | 5.77 psf |
| 2 | 652 2580 2185 3212 | x 0..250 step 50; y -100, 0, +100 | 20 / 0.45 / 6 | 0.905 (0.36 %) | 1.547 (0.62 %) | 0.132 (0.07 %) | 0.314 |

All lines `detected` (none `predicted`). The 1000 psf line of panel 1 was found in 14 of 22 bands
only, because three curves run along it; its fitted position agrees with the eye reading to 0.3 px.

Box choice. The upper panel's top frame (v~841, about 5470 psf) and right frame (u~2570, the
legend column) carry no printed value, so both are outside the box: the box runs from the left
frame (x = 0) to the 250 gridline and from the bottom frame (0 psf) to the 5000 psf line. The lower
panel's box likewise stops at the 250 gridline (its right frame at u~2585 bounds the "Same Notation
As Above" area).

Eye checks (`calibration-eye-checks.csv`, 19 rows: 4 labels on the upper y axis, 6 on each x axis,
3 on the lower y axis). Every gridline read by eye on a zoomed crop lies within 1.6 px of the
fitted line (largest: lower x = 100, eye 1284 vs fitted 1282.4; a row scan gives 1282.5).

**The x grid is not uniform, and the affine map cannot absorb it.** In both panels the first
interval (x = 0 to 50) is drawn about 314 px wide and the other four about 291 to 297 px. The
printed "0" sits under the left frame just as "50" sits under the 50 line, so the frame is the
x = 0 line as drawn. The affine fit therefore puts x = 0 about 8 px right of the frame and x = 50
about 10 px left of its line: x errors of -1.3 to -1.5 at the frame and +1.3 to +1.7 at the 50 line,
under 0.9 elsewhere. The RMS residual (0.38 % and 0.36 % of the span) is under the 0.5 % limit; the
maximum (0.68 %, 0.62 %) is over it. No box or threshold change can remove this, since it is in the
drawn grid, not in the line detection. Consequences a later reader should know:

1. Points between x = 0 and 50 carry a systematic x error of up to about 1.5 thousandths in the
   `-native` files (for example the first upper markers at u~707 come out at x = 5.0; a
   piecewise-linear map between the detected gridlines would give about 6.1).
2. The first column of lower-panel symbols is drawn on the left frame (x = 0), but the affine
   map gives x = -1.3 to -1.9 for it: these five points fall outside the axis range only because of
   the fit.

y axes are uniform (upper: 292 to 296 px per 1000 psf; lower: 295 to 296 px per 100).

Label oddities: the upper panel's "0" is printed about 53 px below the bottom frame (v~2506,
between the panels); the bottom frame is the 0 psf line (it continues the uniform spacing). The
lower panel's y-axis label is printed "delta_tau x 10^-3 (in.)", the same symbol as the x axis,
although the quantity is the dilation (vertical) displacement.

## 2. Series identity and legend

The legend is text at the right end of each curve (sigma PSF, gamma PCF): 4695 / 96.4 (plus),
3815 / 96.4 (triangle-down), 2934 / 97.6 (circle), 1761 / 96.4 (square), 734 / 95.2 (triangle-up).
All five printed normal stresses match the series ids given; no misprint. The heading reads
"gamma = 95.2 to 97.3 Lb./Ft.3 (Dr = .02 to .13)": its last digit is a broken glyph (97.3, possibly
97.8) and does not match the inset's highest value, 97.6.

## 3. Markers

Counts: upper panel 13 per series except n2934 with 12; lower panel 13 per series (13 columns of
five stacked symbols). Centers read by eye on zoom 3 to 9 crops (`crops/`), then checked against
column/row scans through each symbol (outer extents) and against the symbol's enclosed white hole
(`helpers/holes.py`); where the checks moved a center by more than about 1.5 px the scan value was
taken and the bound widened if the two methods still differed.

Conventions:
1. Plus: crossing of the two bars (vertical-bar center for u, arm center for v).
2. Square, circle: center of the outer outline.
3. Triangles: centroid of the triangle (one third of the height from the flat side), not the
   center of the bounding box. A reader using the bounding-box center would sit about 5 px
   (about 17 psf, or 1.7 thousandths in the lower panel) toward the apex.
4. Upper-panel triangles: centroid from the outer apex and outer flat side along the center column.
   Where the hole-based centroid differs by 2 px or more the v bound is 3 (4 for n734 at u~1558,
   whose base is drawn thick).
5. Lower-panel triangles: each column has a triangle-up (n734) stacked on a triangle-down (n3815),
   forming a diamond that shares its middle stroke, so the outer extents are ambiguous there; the
   centroid comes from each triangle's hole. Bound 3 px for all of them.

Ambiguities (each also in the row's `note`):
1. n4695 marker 7 (u~1314, x~108) is faint and broken: only its vertical bar shows above and below
   the drawn line. Read as a plus from that bar and the 13-point spacing; bounds 3 / 4 px.
2. n4695 marker 6 (u~1229) is small and asymmetric (bar 1673-1694, arms 1685-1690); center at the
   crossing, v bound 3.
3. n4695 markers 8 and 9: horizontal arms merged with the drawn line; centers from the vertical bars.
4. First column of the upper panel (u~707 to 713): n734's triangle-up sits on n1761's square (the
   triangle's base and the square's top edge are one dark band) and both lines start from this
   cluster; square center from its hole and bottom edge. Bounds 3.
5. Second column: n1761's square bottom merges with n734's triangle apex; bounds 3 in v.
6. Markers on gridlines: n4695 4 (arm touches 50), n3815 4 and 9, n2934 4, 8 and 12, n1761 4, 9 and 13,
   n734 4, 9 and 13 (vertical gridlines); n1761 7 to 12 sit on or straddle the 1000 psf line;
   n3815 5 has its apex in the 2000 psf line.
7. n2934 circles 4 (u~972) and 5 (u~1088) lie below the drawn line, touching its lower edge; the
   line is drawn above them, so these two markers are off the curve by about 22 and 16 px (about
   75 and 55 psf).
8. n2934 has no circle between x~69 and x~98 nor near x~110 in the upper panel, while the lower
   panel has a circle in every column; the upper panel has 12 circles.
9. Lower panel, column 1: all five symbols are drawn on the left frame line (bounds 3). Columns 4,
   9, 13 are on the 50, 150, 250 gridlines (bounds 3).
10. Lower panel, column 6: the n1761 square is drawn about 28 px (4.7 thousandths) left of the
    other four symbols of the column.
11. The upper-panel first markers of every series are at x~5, while the lower panel's first column
    is on the x = 0 frame. The other columns agree between panels only roughly (lower panel at
    about 21, 31, 51, 70, 90, 110, 129, 149, 169, 189, 218, 249; upper panel within a few thousandths
    of these, n2934 differing most).

No symbol in either panel was unidentifiable; no marker was omitted.

## 4. Traces (upper panel; the lower panel has no drawn lines)

Drawn lines are 10 to 14 px thick. Samples every 10 to 20 px (1.7 to 3.4 thousandths) on clean ink,
in drawing order (left to right; no curve doubles back). Column samples: v = center of the dark run,
v bound = half its length, u bound 1. The steep starts of n4695, n3815 and n2934 are sampled along
rows: u = center of the horizontal run, u bound = half its length, v bound 1. Each sample location
was chosen on the crops and in `helpers/trace_scan.py` listings (which flag gridlines and nearby
symbols); `helpers/build_points.py` measures the run there.

Gaps: no sample within a symbol or within the white gap between a line end and a symbol, and none
where a plus's arms coincide with the line. The line stops at most symbols, so successive samples
are 5.4 to 10.1 thousandths apart across each marker (largest: n4695 10.1 at u 1200-1260 and
1940-2000; n3815 10.1 at 1290-1350, 1530-1590, 1930-1990; n2934 10.1 at 1530-1590; n1761 and n734
9.5). Between markers the spacing is under 5 thousandths.

Ends: first and last trace samples are where the line's ink starts and stops, not on a symbol:
1. n4695: ink starts at u~722-729, v~1892, clear of the first plus (which is a separate symbol to
   its left); ends at u~2106, about 24 px short of the last plus's center (11 px short of its left arm).
2. n3815: starts at the top-right corner of the first triangle-down (row 2110, just above the
   corner); the first segment stops at v~2000 below the second triangle; the line ends at u~2114
   before the last triangle.
3. n2934: starts at the top of the first circle (row 2206); ends where it meets the last circle
   (u 2136).
4. n1761: starts at the top-right corner of the first square (u 730 is the first column clear of the
   square; the run may include the corner); ends at u 2138 at the last square.
5. n734: starts from the right side of the first triangle-up (u 727, the first column clear of it);
   ends at u 2136 at the base of the last triangle.

Merging and shared ink:
1. **n1761 and n734 cross at u~735 to 765 (x~11 to 16).** n734 starts higher (first markers 666 vs
   576 psf) and runs nearly flat; n1761 rises from its square to the second square above n734. In
   this stretch the two lines are one dark band 13 to 21 px tall. One sample at u 748 (the crossing,
   run 2244-2256) is filed under both series with a note; columns 732 to 742 and 754 to 760, where
   the band holds both lines without a separable center, are not sampled.
2. **n1761 runs on the 1000 psf gridline from u~1415 to ~1990 (x~126 to 223).** The dark run there
   is the gridline (about 2155-2160) plus the line; the line's upper edge is hidden. Rule used:
   center = lower edge of the run - 5.5 (half the 11 px line width measured where the line is
   clear, e.g. 2162-2173 at u 1994); v bound 7. 18 samples carry this rule in their note. A reader
   taking the band center instead would read 1.5 to 3 px (5 to 10 psf) higher.
3. n3815 crosses the 2000 psf gridline at u~1020 to 1080; samples at 1030 and 1060 include gridline
   ink (bound 7). At u 1050 to 1060 the line fully covers the gridline.
4. n2934's line passes above circle 4 without a gap; samples at u 960 and 970 are on the line, with
   white between them and the circle.

Stray ink not used (thin strokes and dashes, probably construction lines or erasure remnants):
1. short dashes at v~1887, u 747-792 (right of the first plus) and small marks near (810, 1825);
2. a thin dotted line at v~1768, u 873-963, under the n4695 curve;
3. a thin dashed line at v~2020, u 1148-1270, under the n2934 curve (visible on the page as a short
   horizontal rule under the curve near x~85 to 105);
4. a thin stroke at v 1820-1822, u~1815 to 1855, under the n3815 line after its 11th marker;
5. lower panel: short horizontal dashes and dotted rules near v~2975 (u~1523-1553), v~3078 to 3082
   (u~1225-1290, ~1495-1545, ~2002-2125), dots right of several squares near v~2970, and a small
   mark at (2006-2016, 2968-2973).

## 5. Features

First and last points repeat the first and last trace samples. Peaks are the minimum v of the
line center from a 2 px column sweep (markers and gridlines excluded); every curve has a flat top,
so the x of the peak is not determinate and its u bound spans the flat stretch:

| series | peak u, v (px) | approx. x, tau | flat stretch (within 1 px) |
|---|---|---|---|
| n4695 | 1475, 1676.5 | 135, 2638 psf | u 1400-1498; within 3 px from ~1340 to ~1830 |
| n3815 | 1520, 1796.0 | 142, 2231 psf | u 1464-1594 |
| n2934 | 1320, 1980.0 | 108, 1607 psf | u 1310-1500 |
| n1761 | 1800, 2162.0 | 189, 985 psf | u 1714-1896 (merged with the 1000 psf line; rule of section 4) |
| n734 | 1970, 2216.5 | 218, 799 psf | u~1816-2128; the line rises only about 1 px over its last 600 px |

## 6. Observations from the reading (not reading problems)

1. n734 ends at about 795 psf of shear under 734 psf normal stress (tau/sigma about 1.08), against
   0.54 to 0.57 for the four other tests, and its curve starts above n1761's. Worth a look when the
   failure envelope of these tests is read.
2. Lower panel: every test shows contraction from the first column on (already at its full value
   at x = 0) and almost no change over the shear (spread 2 to 8 thousandths per test): n1761 about
   -16 to -24, n734 -34 to -39, n3815 -40 to -45, n4695 -50 to -53, n2934 -58 to -60. n2934, the
   middle normal stress, contracts the most.

## 7. Files

1. `cal-p1/`, `cal-p2/`: anchors.csv, calibration.json.
2. `calibration-eye-checks.csv`: fitted and eye pixel per label, plus the affine pixel and the
   affine error in axis units.
3. `points-p1.csv` (402 rows), `points-p1-native.csv`; `points-p2.csv` (65 rows), `points-p2-native.csv`.
4. `overlay-p1.png`, `overlay-p2.png` (cropped to each panel).
5. `helpers/`: `markers_final.py` (marker centers and notes), `trace_scan.py` (listing of runs
   along a curve with gridline and symbol flags), `holes.py` (symbol holes, a cross-check),
   `build_points.py` (assembles the CSVs from the chosen sampling plan), `peaks.json`,
   `eye_checks.py`, `markers_p1_eye.py` (first eye reading, kept for the record), `overlay-full.png`.
6. `crops/`: the zoomed crops the reading was made from.
