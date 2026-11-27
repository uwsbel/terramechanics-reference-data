# FC-6C blind reading (Claude), page p0133 (printed C-19)

Figure C-6C, "LSM Soil Dense - Shear Stress vs. Shear Displacement; Dilation Displacement vs.
Shear Displacement", LSM soil, gamma 91 to 93.3 pcf, Dr 1.03 to 1.07. Page image 3213 x 4221 px,
300 dpi, bilevel (every pixel is black or white, so faint strokes cannot be graded by darkness).
Context pages p0115 (Appendix C intro), p0129 (C-5A) and p0131 (C-6A) were looked at; nothing
from them was used in the reading itself.

## 1. Legend and series identities

1. The legend is a column of printed numbers to the right of the 250 gridline, one row per curve,
   aligned with the curve's last marker: sigma (PSF) / gamma (PCF) = 4695 / 91.0, 3815 / 91.0,
   2934 / 91.0, 1961 / 91.0, 714 / 93.3. All five printed stresses match the ids in
   `packet/series.csv` (n4695, n3815, n2934, n1961, n714), including the unusual 1961 and 714. No
   misprint found.
2. The legend has no symbol column; each test's symbol is the marker at the right end of its
   curve next to its number: 4695 plus, 3815 triangle-down, 2934 square, 1961 triangle-up,
   714 circle. The lower panel says "Same Notation As Above" and uses the same five symbols.
3. The last 2934 symbol looks like a square with a plus on its right side at page scale
   ("[]+" next to "2934"). On the zoomed page it reads as a square (top edge v 1547, bottom bar
   v 1574 to 1579) with the 2934 drawn line passing through it at v about 1564 and poking out of
   its right edge by about 10 px; it is not a 4695 marker (the 4695 curve is at about 4040 psf
   there). If the bar at 1574 to 1579 is instead a separate stroke, the square spans v 1547 to
   1567 and its center is v about 1557 rather than 1563; the marker row carries a 6 px v bound and
   a note.

## 2. Calibration

1. Upper panel: box u 625..2150, v 925..2435 (right edge placed between the 250 gridline and the
   right frame, because the frame continues past 250 to hold the legend column), x values
   0,50,...,250, y values 0,1000,...,5000, bands 22, min-frac 0.45, snap 6. All 12 lines
   detected (none predicted); the 150 line in only 13 of 22 bands because markers and curves cross
   it. Fit: x 0.1712 per px, RMS 0.639 (0.26 % of 250), max 1.035 (0.41 %); y 3.403 psf per px,
   RMS 9.30 psf (0.19 % of 5000), max 14.9 psf (0.30 %).
2. Lower panel: box u 638..2160, v 2540..3170, x 0..250, y -100, 0, +100 (only three horizontal
   lines exist: the frame at +100 and -100 and an unlabeled midline at 0), bands 12. All lines
   detected. Fit: x RMS 0.585 (0.23 %), max 0.921 (0.37 %); y RMS 0.080 (0.04 % of 200), max
   0.126.
3. Eye checks (`calibration-eye-checks.csv`): 6 y labels and 5 x gridlines on the upper panel,
   3 y lines and 5 x labels on the lower panel; gridline centers read on 1:1 text crops and zoom 3
   image crops next to each printed label. Largest disagreement with the fitted map: 4.7 px, which
   is 0.80 thousandths or 0.32 % of the x span (the 50 gridline); upper y at most 3.9 px (13.4 psf,
   0.27 %). All below the 0.5 % threshold, so no refit.
4. The residuals are drawing irregularities of the grid, not detection errors: the upper panel's
   horizontal gridline spacings read 286.5, 297, 291, 297, 294.5 px, and the vertical spacings
   vary from about 285 to 304 px. The first x interval (frame to the 50 line) is about 4 % wider
   than the others in both panels, so the left frame maps to x = -1.0 (upper) and -0.9 (lower)
   under the affine fit. Markers drawn on the lower panel's left frame therefore read x about -1,
   not 0.
5. Printed label oddities: the top y label prints as "500" plus a smudge (read as 5000), the 4000
   label prints as "4( 00". The x labels (50 to 250) are printed only under the lower panel; the
   upper panel shares the same vertical gridlines.
6. The 100 vertical gridline of the upper panel shows as two candidates (u 1235 and 1241.5) in
   `plot_grid.py lines`; on the page it is one stroke tilted by about 0.011 px/px, not a doubled
   line.

## 3. Reading conventions used

1. Marker center = center of the symbol's bounding box (outer ink extent), read on 1:1 text crops
   of the page pixels (`helpers/ascii.py`) and checked on zoom 4 crops. For a plus, the crossing of
   the arms (u from the vertical arm, v from the horizontal arm). For triangles the bounding-box
   center differs from the centroid by about one sixth of the height (about 5 px): the bbox center
   lies above the centroid for triangle-up and below it for triangle-down. A reader who uses
   centroids will differ by about 5 px in v on every triangle (about 17 psf upper, about 1.7
   thousandths lower) in a consistent direction.
2. Bounds: 2 px for a clean marker; 3 px where a marker sits on a gridline, the frame, or touches
   another symbol; 6 px in v for the ambiguous last 2934 square.
3. Trace samples: at chosen columns, the center of the dark run (three adjacent columns all dark)
   belonging to the curve; u bound 1 px (the column is chosen), v bound half the run length,
   minimum 2 px. On flat stretches the line is 10 to 12 px thick (bound 5 to 6 px, about 17 to
   20 psf); on steep stretches the run along the column is longer (up to 29 px), and the bound is
   half of it. Columns within 8 px of a vertical gridline or inside any symbol's footprint were
   not used. Candidate runs were found with `helpers/trace_pick2.py` and every sample was checked
   on zoomed overlays; manual drops and additions are listed in `helpers/build_p1.py`.
4. Sampling spacing is about 20 px (3.4 thousandths) wherever ink exists. Every gap above
   5 thousandths is where the drawn line is interrupted by a marker (the upper curves are drawn as
   dashes that stop short of each symbol) or by a vertical gridline: typically 6 to 10
   thousandths, largest 14.2 thousandths (3815 around its 11th triangle, x 211 to 225).
5. Features: first point = where the drawn line's ink starts (never on the first symbol), last
   point = where it ends, peak = highest ink of the drawn line (not of the markers). The first and
   last trace samples are those same ink end points.

## 4. Upper panel, per curve

1. n4695 (plus, 11 markers, 60 trace samples). The steep line starts at (709.5, 1811), about
   12 px up and right of the first plus, without touching it. From x about 152 to the end the line
   runs along the 4000 psf gridline and shares ink with it (23 samples marked in the notes): v is
   the center of the merged run (12 to 17 px long) and the bound is half of it (up to 8.5 px,
   29 psf). Under the line, between u 1630 and 1810 (x about 167 to 198), there is a thin
   separate stroke at v about 1243 (about 30 psf below the line); short faint dashes also run at
   v about 1255 between u 1405 and 1490. These look like pencil guide strokes and were not
   sampled. The line's top edge is flat (v 1217) from u about 1969 to 2062, so the peak is
   flat-topped: peak feature at u 2015 with a 46 px u bound. The line ends at u 2061, about 19 px
   short of the last plus; only the gridline continues to the marker. The plus markers sit at
   x about 8, 20, 40, 78, 99, 126, 147, 168, 188, 218, 247; there is no plus near x 58 (the line
   is plain there) although the other three steep curves have a marker near x 58.
2. n3815 (triangle-down, 12 markers, 60 trace samples). The line starts where it meets the top
   edge of the first triangle. From x about 103 to the end it runs along the 3000 psf gridline and
   shares ink with it (33 samples, merged-run center and half-run bound); near u 2064 to 2080 the
   two separate again and the line reads v 1517. The third triangle is distorted (broken right
   side, specks above). Triangles 9 to 11 touch the 2934 squares directly below them; their apex
   positions are partly hidden (3 px v bounds).
3. n2934 (square, 12 markers, 62 trace samples). Between u 1640 and 1720 there is again a thin
   separate stroke under the line at v about 1562 (not sampled). The line peaks at the right end
   of the dash before the 11th square (u 1889, x 212, about 2965 psf), is hidden by that square,
   then descends to the end. The drawn line passes through the last square and ends just past its
   right edge at u 2126, x about 252.7, i.e. beyond the 250 gridline (still inside the plot frame,
   which extends to the right to hold the legend).
4. n1961 (triangle-up, 12 markers, 62 trace samples). Clean. The line has a gentle hump with its
   highest stretch between the 9th and 10th triangles (x about 176 to 183, about 1398 psf), then
   drops to about 1330 psf at the end. The line runs along the bases of the right-hand triangles
   rather than through their centers.
5. n714 (circle, 14 markers, 61 trace samples). Circles are smaller than the other symbols and
   spaced every 20 thousandths, which gives this curve more markers than the others. The line
   starts about 6 px from the first circle without touching it; it is nearly flat from x about 40
   to 250, and its highest stretch (u 848 to 863, x about 32 to 35) is only about 3 px above the
   plateau.
6. Stray marks, not part of any curve and not sampled: short horizontal dashes to the right of
   squares 2 and 3 and of triangle-down 3, a dash at u 835 to 895, v 1640 (left of the 3815
   curve), and the legend box's bottom edge at v about 1170 above the 4695 curve on the right.
7. Upper-panel curves never merge with one another. At x about 165 to 220 the 3815 and 2934 line
   centers are only 17 to 25 px apart (about 60 to 85 psf) and their symbols touch, but the two
   lines keep a light gap between their inks.

## 5. Lower panel

1. Markers only: 13 circles (714), 13 triangle-up (1961), 13 squares (2934), 12 plus (4695),
   13 triangle-down (3815). There are no drawn lines through the lower-panel markers, so no trace
   or feature points. Faint dotted fragments appear in places (for example a dotted row at v about
   2950 between u 1975 and 2075, near the bottom edge of the 12th square, and dots right of some
   triangles); they are too broken to follow and do not connect marker centers, so they were not
   sampled. Several short stray dashes touch symbols (right of square 2 toward plus 2, below the
   apex of triangle-down 2, right of triangle-up 10); each is noted on the marker row.
2. All 64 symbols were identifiable; none needed a wide-bound unidentified row. The rows are well
   separated: circles near the 0 line, triangles-up about 15 thousandths below, squares and pluses
   about 30 to 40 below, triangles-down about 48 to 59 below.
3. Circle, triangle-up, square and triangle-down markers sit at x = 0 (on the left frame, reading
   about -1 because of the frame offset in section 2 item 4), 20, 40, ..., 220 and 250. The plus
   markers sit at x about 5, 31, 50, 70, ..., 191, 216, 245, i.e. offset from the others, and the
   first plus is right of the frame, not on it. The last two pluses touch the left edges of the
   2934 squares next to them.
4. Markers on gridlines or the frame (3 px bounds): the whole first column on the left frame;
   symbols on the 100, 200 and 250 gridlines; pluses 3 and 8 on the 50 and 150 gridlines (their
   vertical arms are hidden in the gridline, so v comes from the horizontal arm); circles 1 to 4
   touching the 0 midline.

## 6. Observations a later reader should know (stated as read, not judged)

1. The marker x positions differ between the two panels. Upper panel (triangle-up, square,
   triangle-down): x about 9, 20, 39, 58, 79, 98, 118, 147, 167, 188, 218, 248. Lower panel:
   0, 20, 40, ..., 220, 250. Upper circles: about 10, 20, 39, 59, 79, 98, 118, 138, 158, 178, 199,
   217, 238, 250. The upper pluses are listed in section 4 item 1. So the two panels do not plot
   the same displacement readings at the same abscissae.
2. In the lower panel the 3815 (triangle-down) row lies below the 4695 (plus) row, i.e. the
   dilation values are not ordered by normal stress (3815 shows the most contraction). The
   symbols are unambiguous, so this is what the page shows.
3. The lower-panel symbols at x = 0 are not at zero dilation (circle about -6, triangle-up about
   -19, square about -34, triangle-down about -48 thousandths).
4. The 2934 and 3815 upper curves end within about 160 psf of each other (about 2870 and
   3030 psf), with the 2934 curve dropping at the end after a peak near x 212.

## 7. Files

1. `cal-p1/`, `cal-p2/`: anchors and calibration for each panel.
2. `calibration-eye-checks.csv`: figure_id, panel, axis, printed_label, read_at, fitted_pixel,
   eye_pixel, eye_minus_fitted_px, eye_value_minus_label, pct_of_axis_span, note.
3. `points-p1.csv` (381 rows), `points-p1-native.csv`; `points-p2.csv` (64 rows),
   `points-p2-native.csv`.
4. `overlay-p1.png`, `overlay-p2.png`: points over the page, checked by eye.
5. `helpers/`: `ascii.py` (1:1 text crop of page pixels), `calpix.py` (inverse calibration),
   `mosaic.py` and `stack.py` (crop mosaics), `tracker.py` and `trace_pick2.py` (candidate trace
   runs, a reading aid), `build_p1.py` (assembles points-p1 from the reviewed marker readings
   `markers-p1.csv`, the reviewed candidate traces `tr/*.csv`, the drops, additions and features),
   `markers-p2.csv` (lower-panel readings), `eyechecks.py`; `trace_pick.py` is an earlier version
   kept for the record.
6. `crops/`: review crops and overlays used during the reading (not deliverables).
