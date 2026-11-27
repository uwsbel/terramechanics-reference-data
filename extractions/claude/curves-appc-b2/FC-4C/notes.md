# FC-4C, blind reading (Claude), AM-68-1 Vol. II Appendix C, printed C-14, PDF 128

Page image `packet/p0128.png` (3213 x 4508, 300 dpi, unrotated). Five series, RC2 soil at
Dr .95 (gamma 81.8 pcf): n4695 (plus), n3815 (circle), n2934 (triangle-up), n1761 (square),
n741 (triangle-down). Legend symbols read off the page; the lowest stress is printed 741.

## 1. Axis calibration

Upper panel (panel 1): shear stress, 0 to 8000 psf printed, x 0 to 250 (the frame extends to
about 320 on the right, past the 250 gridline; the legend sits there). The 8000 gridline is
hidden by the legend text between u 1055 and u 1700 and visible on both sides of it; the top
frame line sits at about 9000 psf (not labelled). Four detect runs were made and are kept:

1. `cal-p1-A/`: box including the top frame, y values 0,1000,...,9000. Rejected: a curve
   plateau was taken as the (nonexistent) 1000 line and the y RMS residual was 47.6 psf
   (0.6 percent of the span).
2. `cal-p1-B/`: box from v 1290, y values 0,2000,...,8000, frame-frac 0.2. Rejected: the
   legend text top edge (v 1313) was taken as the 8000 line (4 bands only, wrong slope).
3. `cal-p1-C/` = `cal-p1/` (adopted): box 740 1317 2250 2520, y values 0,2000,4000,6000,8000,
   x values 0,50,...,250, bands 20, min-frac 0.35, snap 6, frame-frac 0.2. The 8000 line was
   found in 17 of 20 bands with the same tilt as the other lines (-0.0038); 30 anchors, RMS
   residual x 0.46 units, y 12.1 psf (0.15 percent of the 8000 span), max 21.8 psf. The
   horizontal gridlines are not perfectly equally spaced on the page (spacings 288.5, 296.5,
   286.5, 293 px), which is what the residual measures.
4. `cal-p1-D/`: narrow box (x 0 and 50 lines only) as a cross-check of the y map: agrees with C
   within 2 px everywhere.

Lower panel (panel 2): dilation displacement, +100 / 0 / -100 printed (frame lines at +100 and
-100), x 0 to 250. `cal-p2/`: box 750 2750 2260 3380, 18 anchors, RMS x 0.46, y 0.15 units.

Eye checks (`calibration-eye-checks.csv`, 12 rows, three labels per axis per panel, read on
zoom-5 crops in `crops/eye/`): all within 1 px of the fitted positions. No predicted lines.

The vertical gridlines are tilted by about +0.0085 du/dv (u grows by about 10 px from the top of
the upper panel to the bottom of the lower one); the horizontal ones by about -0.0036 dv/du.
All pixel coordinates below are page coordinates.

## 2. Markers

Every plotted symbol in both panels was located on zoom-3 crops, then its centre refined
mechanically (`helpers/refine.py`: centroid of the enclosed white hole for hollow symbols,
crossing of the two strokes for a plus) and every refined centre was checked by eye on zoom-6
montages (`work/montage-p*.png`). Nine upper-panel and six lower-panel centres were overridden
by eye on zoom-10 crops (`crops/p1fix/`, `crops/p2-*.png`); the overrides are listed in
`helpers/build_points.py` with their reasons and each carries a note in the CSV. Triangle centres
are the centroid of the hole, which coincides with the centroid of the outline (checked on the
montages); a human reading the triangle's visual centre may sit 1 to 2 px higher for
triangle-up and lower for triangle-down.

Bounds: 2 px for a clean symbol, 3 px for a symbol on a gridline or touching another symbol,
4 px for the crowded clusters described below.

Upper panel counts: n4695 13 plus, n3815 16 circles, n2934 14 triangles-up, n1761 14 squares,
n741 18 triangles-down (75 markers). Lower panel: n4695 15, n3815 16, n2934 12, n1761 14,
n741 14 (71 markers). The lower panel is sampled about every 20 thousandths, the upper about
every 10 up to 130 and every 20 to 30 after that.

### Ambiguities, upper panel

1. n4695 plus at (2226.5, 1743): on the 250 gridline; its horizontal stroke is merged with the
   drawn plateau, v bound 3.
2. n3815 circle at (1278, 1867): the ring is open on its right side; centre from the left arc,
   top and bottom; bound 3.
3. n2934 triangle at (1625.5, 1910): on the 4000 gridline and against the 150 gridline;
   centroid from apex and base corners; bound 3.
4. n2934 triangle at (2207.5, 2066) and n741 triangle-down at (2211, 2374): right corner
   hidden by the 250 gridline, taken by symmetry; bound 3.
5. n1761 square at (2219, 2160.5): cut by the 250 gridline; bound 3.
6. n1761 squares at (1102, 1850) and (1455.5, 2071): drawn line through the square, or outline
   open; centre from the sides.
7. The n4695 plus at (984.6, 1466) overlaps the n3815 peak circle and both drawn lines; bound 3.

### Ambiguities, lower panel

1. The x = 0 stack on the left frame line (u 760 to 770, v 3092 to 3137): square (769, 3093),
   triangle-down (768, 3112), triangle-up (767, 3129), plus (760, 3135.5), all with their right
   parts under the frame line and their outlines merged; bounds 3 to 4. The matching n3815
   circle is drawn LEFT of the frame at (735.5, 3125.8), x about -7 (recorded as a marker with
   a note; it is the only symbol outside the frame).
2. The x = 10 to 30 cluster on the 0 gridline (u 800 to 960, v 3040 to 3140), read on zoom-8
   and zoom-12 crops (`crops/p2-s1.png`, `p2-s2.png`, `p2-s3.png`, `p2-cluster20-30.png`) with
   the enclosed holes listed mechanically (`helpers/holes.py`):
   a. n1761 has two squares 18 px apart: (892, 3072), whose top is hidden under the 0 gridline,
      and (910.4, 3081.4). The first is recorded as n1761 because its hole is flat-bottomed and
      11 px wide (square-like); it could instead be a triangle-down of n741 whose top edge is
      under the gridline (n741 has no other symbol at x about 20). Note on the row.
   b. n741 has two triangles-down at the same x about 30: (949.4, 3073) on the 0 gridline (top
      edge hidden, bound 4) and (949.6, 3044.2) 29 px above it. Both are clear triangle-downs.
   c. The n2934 triangle at (932.2, 3082) has its apex in the 0 gridline and overlaps the
      square at 910; bound 4. The enclosed hole at (924, 3075) between that square, this
      triangle and the gridline is a gap between symbols, not a symbol.
3. The x = 250 stack (u 2210 to 2225): triangle-up (2217.6, 2860.4), triangle-down
   (2218, 2886), square (2216.6, 2903.4); all on the 250 gridline, bounds 3 to 4. The circle
   (2218.4, 2985.4) and the plus (2225.5, 3010.5) of the same column are separate.
4. Pluses whose vertical stroke coincides with a vertical gridline (50, 200, 250 lines): u is
   that of the gridline, bound 3.
5. The lower panel has no drawn lines: markers only.

## 3. Drawn lines (upper panel)

The lines are dashed (dashes 40 to 60 px, gaps 10 to 15 px), 8 to 12 px thick, and nearly
vertical over the first 20 thousandths. Two automatic trackers (`helpers/trace.py`,
`helpers/trace2.py`, kept for the record under `helpers/abandoned/`) lost the steep dashed
segments; the reading was made with `helpers/sample_lines.py`: a guide polyline through each
series' marker centres (plus a few guide points read off the crops where the line leaves the
marker interpolation, at the n4695 crest), and at each sample column the dark run nearest the
guide within 15 px. Sample columns at x = 7.5, 12.5, 17.5, ... thousandths (never on a
vertical gridline; shifted by up to 14 px when the column fell in a dash gap or in a symbol).
Bound: half the vertical thickness of the run (for the steep segments this is 10 to 25 px in v,
which is the honest uncertainty of the centreline's v at a fixed column; the perpendicular
thickness is 8 to 12 px). Where another series' guide is within 20 px, or the run crosses a
horizontal gridline, the bound is widened to the full run thickness and the row says so.
Every sample was checked on zoomed overlays (`crops/ov-*.png`).

Features per series: first ink column after the first symbol the line passes through, the
highest ink column (peak of the drawn line, outside symbol footprints), the last ink column
before the 250 gridline. The lines all end at the 250 gridline (the n4695 line ends at its
plus on the gridline).

Known issues a later reader should look at:

1. n4695 start: no line is drawn between its first plus (807, 1776) and its second
   (864, 1690). The only ink there is the thick dash from (827, 1754) to (861, 1634), which
   runs into the n3815 circle at (862, 1621) and is read as n3815's line (slope -3.5, matching
   n3815's markers; it is thicker, 14 px, than the other dashes, so it may be two strokes on
   top of each other). A short thin stroke from (865, 1680) up to (855, 1634), between the
   second plus and that dash, is unexplained. The n4695 line is therefore read from u 878 on
   (first point (878, 1643.5), x 19.6, 5800 psf) and has no trace sample at x 12.5. The other
   reader may have attributed the thick dash to n4695; this is the first place to compare.
   Crops: `crops/p1-start-lines.png` (zoom 5), `crops/ov-A2.png`.
2. n3815 peak: the drawn line peaks under the circle at (976.2, 1440.8) (it enters from the
   lower left and leaves to the lower right); the feature row gives the circle centre with a
   6 px bound. The n4695 line crosses the n3815 line just right of that circle (u 985 to 1000,
   v 1445 to 1465); the n3815 samples at x 37.5 and 42.5 and the n4695 plus at (984.6, 1466)
   are in that crossing.
3. n4695 crest: the drawn line peaks at (1034, 1424.5), about 7300 psf at x 46.7, well above
   the plus markers at x 40 (6950) and 58 (6950); the guide points for this were read by eye.
4. n3815 and n2934 lines run 10 to 25 px apart from x 150 to 200 and cross at about
   (1935, 1997), x 200; from x 200 to 250 the n3815 line is the upper one (about 2010) and the
   n2934 line the lower (2020 to 2065). Samples of both series between x 185 and 215 carry
   the shared-ink note and full-thickness bounds. The n2934 line also passes through the n3815
   circle at (1095, 1675).
5. n1761 line passes through its own squares at (1102, 1850) and (1044.7, 1867); samples near
   them were shifted away from the symbols.
6. Missing trace samples (dash gap wider than the 14 px shift, or inside a symbol or on a
   gridline crossing): n4695 x 32.5, 37.5, 97.5, 147.5, 167.5, 212.5, 217.5; n3815 x 57.5,
   117.5, 142.5, 177.5; n2934 x 37.5, 87.5, 147.5, 167.5; n1761 x 197.5; n741 x 17.5, 47.5,
   187.5, 217.5. Nothing was interpolated.
7. Five samples sit where a line crosses a horizontal gridline (noted, bound widened to the
   full run): n3815 at x 107.5 and n2934 at x 142.5 (4000 line), n1761 at x 37.5 and 77.5
   (4000 line), n741 at x 67.5 (2000 line). 24 samples carry the shared-or-adjacent-ink note.

## 4. Files

`cal-p1/` (adopted, copy of `cal-p1-C/`), `cal-p1-A/`, `cal-p1-B/`, `cal-p1-D/` (variants,
see section 1), `cal-p2/`, `calibration-eye-checks.csv`, `points-p1.csv` (75 markers, 213
trace samples, 15 features), `points-p1-native.csv`, `points-p2.csv` (71 markers),
`points-p2-native.csv`, `overlay-p1.png`, `overlay-p2.png`, `notes.md`.
Helpers in `helpers/` (refine.py, montage.py, holes.py, sample_lines.py, build_points.py,
zoom_overlay.py; abandoned trackers in `helpers/abandoned/`), intermediate lists and montages
in `work/`, crops in `crops/`. `build_points.py` regenerates both points files from the refined
lists and the overrides; `sample_lines.py` is called by it.
