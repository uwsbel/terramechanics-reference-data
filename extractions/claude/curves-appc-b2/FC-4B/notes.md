# FC-4B (AM-68-1 Vol. II, Fig. C-4B, printed C-13, PDF 127): blind reading notes

Reader: Claude (blind; only `packet/` and `tools/` were used). Image `packet/p0127.png`,
3263 x 4508 px, 300 dpi, unrotated. Five series, RC2 soil, gamma 58.7 pcf (Dr = 0):
n4695 plus, n3815 circle, n2934 triangle-down, n1761 square, n734 triangle-up (legend at the
right of the upper panel; the lower panel says "Same Notation As Above").

## 1. Calibration

1. Upper panel (`cal-p1/`): box 770 1180 2290 2690, x values 0..250 step 50, y values
   0..5000 step 1000, `--bands 20 --min-frac 0.4 --snap 6 --frame-frac 0.4`. All 12 lines
   detected (the x = 50 line in 17/20 bands, it is interrupted by markers). 36 anchors.
   RMS residual x 0.31 (0.12 percent of the 250 span), y 20.4 psf (0.41 percent of 5000),
   max y residual 34.7 psf (0.69 percent). The y residual comes from the grid itself: the
   horizontal lines are not equally spaced (spacings 277, 291, 294, 295, 298 px from the top),
   so an affine map cannot hit all six; the fit is a compromise. Readers should expect
   about plus or minus 30 psf of calibration-level disagreement in the upper panel.
   The tool dropped a long dark track at v 2441: that is the n734 plateau, not a grid line.
2. Lower panel (`cal-p2/`): box 770 2780 2290 3420, same x values, y values -150,-100,-50,0,50.
   Only +50, 0 and -150 are drawn on the page; -50 and -100 are not drawn and the tool marks
   them `predicted`. They cannot be eye-checked, but the axis is linear and the three drawn
   lines fix the scale (0 is exactly one quarter of the way from +50 to -150: 2952.7 px vs
   2805.3 and 3390.6). A first run with only three y values failed because the tool assumes
   the listed values are equally spaced by index and put "0" at the midpoint; the five-value
   list fixes that. 30 anchors, RMS x 0.22 (0.09 percent), y 0.16 (0.08 percent of 200).
3. Eye checks (`calibration-eye-checks.csv`): every drawn gridline of both panels checked
   on the zoom-3 crops; largest eye-minus-fit 1.4 px (x = 250 in the lower panel), the rest
   within 1.1 px. Both panels pass the 0.5 percent rule on RMS.

## 2. Method

1. Markers: seed centers read by eye on zoom-3 tiles (500 px, grid every 25 px) and zoom-4
   crops of the dense lower-panel row (v 3240 to 3360). Each seed was then refined by
   normalized cross-correlation against a template cut from a clean symbol of the same
   kind on this page (triangle-up at 1502,3097; square 1503,3247; triangle-down 924,3296;
   plus 1442,3331; circle 1782,1651), search window plus or minus 8 px, and corrected by the
   template's bounding-box-center offset (`helpers/template_centers.py`). The lower-panel
   circles are smaller (about 19 px outer diameter, "o" size) than the upper-panel circles
   (22 x 27 px) and were matched with a synthetic ring. Refined centers agreed with the eye
   seeds within 3 px (4 px for a few squares); the one case where the fit moved 7 px (the
   triangle-down on the left frame at 806,3272) was rejected and the eye value kept.
   Bounds: 2 px clean, 3 px on a gridline, 4 px overlapping or on the frame, 5 px in the
   frame cluster.
2. Traces (`helpers/trace_curves.py`): columns every 29 px (5 thousandths), shifted 9 px off
   vertical gridlines and 20 px away from the series' own markers; dark runs along each
   column (3 px wide, min); the run nearest the linear extrapolation of the previous two
   samples, constrained to within 45 px of a straight-line interpolation of the series'
   markers (130 px for n4695 below u 1200, where the curve is strongly concave). Bare
   gridline runs (thin, at a gridline v) are excluded. v bound = half the run length
   (6 px for the 12 px line; 15 px on the steep first segment of n4695 where a column cuts
   the line obliquely). u bound 1 px.
3. Features: first point = the first marker (the drawn line starts under it, bound 4);
   peak = minimum v by a 2 px column scan around the trace minimum, skipping marker columns;
   last point = the line just before the right frame (u 2244, or the nearest column to the
   left where ink exists), or the last marker for n4695 whose line ends at that marker.

## 3. Ambiguities and things a later reader should know

1. Marker abscissae differ between the panels. Upper-panel markers sit at about 10, 30, 50,
   ... 230, 250 thousandths; lower-panel triangles, squares and most circles sit at 0, 20,
   40, ... 220, 250. The lower-panel pluses (n4695) however sit at 10, 30, 50, ... like the
   upper panel. This is how the page is drawn, not a reading error.
2. Marker counts: upper panel 11 plus, 12 circle, 13 triangle-down, 13 square, 12
   triangle-up; lower panel 12 plus, 13 circle, 13 triangle-down, 13 square, 13 triangle-up.
   The upper panel has no plus near x = 50 (the sequence goes 8, 24, 68, 90, ...) and the
   lower panel has a plus at x = 181 (u 1855) that has no upper-panel counterpart (upper
   pluses at 167 and 197); the lower plus sequence is 10, 31, 50, 70, 92, 110, 131, 150,
   171, 181, 221, 247. Not resolved from the page.
3. Lower panel dense row (v 3270 to 3345): the n2934 triangle-down, n4695 plus and n3815
   circle symbols overlap in nearly every column. Pattern: at u 863, 979 and 1093 a small
   circle hangs from the bottom of a plus; at u 1153 to 1736 and 1972 a small circle hangs
   from the apex of a triangle-down; at u 1855 and 2085 a plus hangs from the apex of a
   triangle-down. All such markers carry 4 px bounds and a note. The circles under
   triangles may be read by another reader as part of the triangle; I read them as separate
   n3815 markers because they are closed rings of the same size as the free-standing
   circles at 2116 and 2279.
4. Lower panel, left frame (u 800, v 3260 to 3300): a triangle-down (806,3272) with a ring
   below it (797,3295) on the frame line, plus a horizontal bar through the ring that may be
   the crossbar of a plus whose vertical bar is hidden by the frame. I recorded the triangle
   and the circle only; a plus at x = 0 would be a 13th n4695 marker and is not recorded.
5. Lower panel, two circles beyond or at the right: (2116,3326) is an incomplete ring open
   on the right (drawn like a "c"), recorded as circle with a note; (2280,3327) is right of
   the frame, x = 254, recorded with a note (beyond axis range).
6. Upper panel markers not on the drawn curve (flagged in `note` with the v offset): n4695
   plus at x 24 (938,1957), 90 px below the line; n3815 circles at x 29 (+53 px, below the
   line), x 49 (-23, above) and x 193 (-27, above); n2934 triangles at x 29 (-16) and x 50
   (+37); n1761 square at x 70 (+23). The author's curves were evidently drawn through the
   remaining points.
7. Gaps in the drawn lines where no trace sample exists: n734 is drawn with short breaks
   (around u 1070 to 1110, 1186 to 1227, 1372, 1691, 1765 to 1807, 2054 to 2097, 2228);
   n4695 is broken where its line meets the 3000 psf gridline and the plus at u 1197
   (u 1177 to 1215), and at u 1339, 1682, 1752, 1798, 2080 (near markers). Each gap is
   simply absent from the trace; nothing was interpolated.
8. Trace samples that sit on a horizontal gridline are noted ("run merged with it"); the run
   center is still the best estimate but the bound is the merged run's half length.
9. The n3815 line stops at u 2237, about 10 px short of its last circle on the frame
   (2258,1582); the last-point feature is read at u 2235.
10. Upper-panel right frame markers (x = 250) for n3815, n2934, n1761, n734 sit on the frame
    line; the n4695 line ends at its last plus (2235,1453), which touches the frame, with a
    sharp drop after the peak (4488 psf at x 219 to 4129 psf at x 247).
11. Peaks: n4695 4488 psf at x 219 (sharp, between the pluses at 197 and 224); n1761 1936 psf
    at x 202 (sharp, the square at 200 is on it); n3815 3727 at x 241, n2934 2742 at x 224
    and n734 747 at x 164 are plateaus (several samples within 6 px of the maximum), so the
    peak u carries a 12 px bound.
12. The y residual of the upper-panel calibration (RMS 20 psf) is of the same size as the
    marker bounds (2 px = 7 psf) and dominates `y_read_bound` for clean markers (27 psf).

## 4. Files written (all under `out/FC-4B/`)

`cal-p1/`, `cal-p2/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`,
`points-p2.csv`, `points-p2-native.csv`, `overlay-p1.png`, `overlay-p2.png`, this file,
`helpers/` (seeds.py, refine_markers.py, template_centers.py, trace_curves.py,
build_points.py, markers_refined.csv, traces_p1.csv) and `crops/` (the zoomed crops and
zoomed overlays that were read by eye).
