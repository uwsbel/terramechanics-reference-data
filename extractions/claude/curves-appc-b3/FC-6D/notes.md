# FC-6D blind reading (Claude), AM-68-1 Vol. II, Fig. C-6D, printed C-20, PDF 134

Page image `packet/p0134.png` (3167 x 4221, 300 dpi, unrotated). The scan is an upsample of a
coarser image: ink comes in 3 px blocks, so no pixel reading here is better than about 1.5 px.
Both panels are tilted the same way (vertical lines lean about 0.9 degree: u grows 0.014 to 0.018
px per px of v; horizontal lines drop 0.011 px per px of u).

## 1. Identity of the series (legend)

The legend is positional: a table right of the 250 gridline with columns sigma and gamma (no
units printed in the header), each row level with the end of its curve. Read at zoom 3:

| curve end symbol | sigma printed | gamma printed | series id |
|---|---|---|---|
| plus | 4695 | 73.0 | n4695 |
| triangle-down | 3814 | 75.2 | n3814 |
| square | 2934 | 66.8 | n2934 |
| circle | 1761 | 70.3 | n1761 |
| triangle-up | 147 | 71.9 | n147 |

The two values flagged as unusual, 3814 and 147, are printed exactly so (crops
`crops/leg3814.png`, `crops/leg147.png`). No legend misprint against `series.csv` was found. The
lower panel says "Same Notation As Above"; its symbols are mapped with the same table.

## 2. Calibration

### Upper panel (`cal-p1/`)
`detect --box 800 990 2258 2245 --x-values 50,100,150,200,250 --y-values 0,1000,2000,3000,4000
--bands 20 --min-frac 0.6 --snap 6 --frame-frac 0.5`. 25 anchors, all lines detected in 19 or 20
of 20 bands, none predicted. x: 0.1702 per px, rms 0.128, max 0.263 (0.05 percent of 250).
y: 3.428 psf per px, rms 8.6 psf, max 12.3 psf (0.17 and 0.25 percent of 5000).

Box choices, and why:
1. Top: the 5000 frame line is hidden behind the legend box for u 795 to 2010, and the legend
   box's lower edge (v 829) and its text were picked up as false tracks, so the box starts below
   it (v 990) and the 4000 line is the top anchor. The 5000 frame was checked by eye instead
   (0.32 percent at the left, 0.45 percent at the right end; table in
   `calibration-eye-checks.csv`).
2. Bottom: the 0 label is printed at the bottom frame, so the frame is an anchor. It is
   crowded by the 147 psf curve and its triangles, and by an extra thin stroke at v 2213 under
   it (u 1100 to 1820). With other thresholds the tool locked on that stroke (slope 0, 10 of 22
   bands); with min-frac 0.6 and 20 bands it follows the frame in 20 of 20 bands
   (v = 2219.4 - 0.0110 u, matching the scans: 2211.0 at u 760, 2193.5 at u 2210).
3. Left: the box starts at u 800 and leaves out the left frame line. See 2.3.

### Lower panel (`cal-p2/`)
`detect --box 800 2320 2266 3255 --x-values 50,100,150,200,250 --y-values=-300,-200,-100,0
--bands 22 --min-frac 0.55 --snap 6 --frame-frac 0.5`. x: 0.1706 per px, rms 0.097, max 0.211.
y: 0.3406 per px, rms 0.065.

The lower panel has NO horizontal gridlines. The y map rests on the two frame lines only: the
bottom frame is -300 (label printed beside it) and the top frame is taken as 0, which is not
printed. Support for 0: the frame is 880 px tall, three times the 293.5 px major division of the
upper panel's grid, and the labels read -100, -200, -300 downward. The -100 and -200 lines are
`predicted` by the tool (interpolated between the frames), so there is no line to confirm them.

### 2.3 The left frame is not at x = 0 of the gridlines (both panels)

The vertical gridlines are evenly spaced (50 to 100 to 150 to 200 to 250: 292 to 297 px), but the
left frame line sits 317 px (upper) and 319 px (lower) left of the 50 line, so the frame is at
x = -3.7 (upper) and -4.3 (lower) on the scale the 50 to 250 lines define. The bottom frame of
the upper panel is likewise 9 px (about 31 psf) above where the 1000 to 4000 gridlines put zero;
the top frame (5000) agrees with them within 1 px.

A first calibration with the frame as x = 0 (tool convention, kept in
`helpers/cal-frame-included/`) had rms 1.07 and 1.16 but missed the printed 50 label by 0.66
percent (upper) and 0.69 percent (lower) of the span, above the 0.5 percent limit, and put the
frame at -1.7 and the 50 line at 51.7. Following the protocol I changed the box: the final
x maps use only the printed labels 50 to 250, which they reproduce within 0.13 percent.

The data support this choice independently. Readings were taken at nearly constant shear
displacement steps. With the 50 to 250 map, the n147 markers fall at 7.2, 17.7, 28.4, 37.1 |
57.1, 67.6, 77.0, 87.3, 96.6, ... (upper panel) and 9.0, 19.2, 29.1, 39.0, 49.2 | 59.1, 69.1,
79.3, ... (lower panel): steps of 10 with one constant offset on both sides of the 50 line. With
the frame taken as 0 and the first cell stretched to fit, the steps inside the first cell would
shrink to 9.8 (upper) and 9.3 (lower) and the offset would drift by 2 to 3 thousandths between
the first reading and the 50 line. So the points appear to have been plotted on the gridline
scale, and the frame line was drawn about 4 thousandths too far left. This is an inference from
the regularity of the readings, not something printed on the page.

Consequence: every marker drawn on the left frame (the zero-displacement readings of the lower
panel, one per series) reads x = -3.1 to -4.3. They are displacement 0 as drawn; their x is the
frame's offset, not a measurement. If the frame-as-zero reading is preferred instead,
`helpers/cal-frame-included/` holds it; the two maps differ by 2.0 to 2.3 thousandths at the
left frame, about 1.5 at the 50 line and under 1 from 100 on.

For y in the upper panel the printed 0 at the frame is kept as an anchor (all label checks are
under 0.5 percent). If the zero of the plotting scale is instead where the 1000 to 4000 gridlines
put it (as the x evidence suggests for the frames generally), every shear stress near zero reads
about 17 psf low here: `helpers/cal-alt-uniform-y/` (box above the frame, 1000 to 4000) gives
+30 psf at the frame against +13 here, and 100.7 against 84.1 psf at an n147 marker. This
matters only for n147 (values 40 to 140 psf), where it is 12 to 40 percent.

### 2.4 Eye checks (`calibration-eye-checks.csv`, 30 rows)
1. Upper y, 6 labels at u 760 and 4 at u 2210: residuals 1.9 to 6.6 px, 0.13 to 0.45 percent.
2. Upper x, 5 labels at v 2130 and 3 at v 890 (labels are printed under the lower panel; the
   lines are the same lines): 0.01 to 0.13 percent.
3. Lower x, 5 labels at v 3190: 0.01 to 0.06 percent; each label text is centered within 8 px
   of its line.
4. Lower y: the two frame lines match exactly (they are the only anchors). The printed label
   texts, with no line to compare: -300 sits 6 px above the frame (0.7 percent), -200 sits
   8 px above its fitted position (0.9 percent), and -100 sits 22 px above (7.6 units, 2.5
   percent). In the upper panel the typed labels sit within 6 px of their lines, so -100 is
   misplaced by about 16 px or the lower y scale is not uniform; nothing on the page decides
   which, and no box or threshold can change it. NOT RESOLVED: lower-panel y values carry an
   extra uncertainty of a few units if the labels rather than the frames are right (a fit through
   the three label texts moves a point at -77 to about -80).

## 3. Markers

Every plotted symbol was read on zoomed crops (zoom 3, 10 px grid) and, where the symbol was
clean, measured with `helpers/sym.py` (dark-pixel extent in a window chosen on the crop),
`helpers/tri.py` (triangle rows from the tip) and `helpers/ystack.py` (stacked symbols). All
centers were checked on the overlays.

Conventions:
1. Circle, square: center of the outline's extent.
2. Plus: crossing of the two bars (vertical bar column, horizontal bar row), not the extent.
3. Triangles: CENTROID (one third of the height from the flat edge, from the outer extent; for an
   equilateral outline this is also its incenter). The bounding-box center would be h/6 (about
   5 px: 16 psf upper, 1.6 units lower) toward the tip. Where the tip or the flat edge is hidden
   (by the frame, a gridline or a stacked symbol) the height was taken as 0.94 times the width,
   measured on the clean triangles of this figure (h 27 to 30 px).

Bounds: 2 px clean; 2.5 px where one edge is hidden; 3 px on a gridline or the frame, or merged
with a curve. Details per point in the `note` column.

Counts. Upper panel: n4695 15 plus, n3814 13 triangle-down, n2934 13 square, n1761 13 circle,
n147 24 triangle-up. Lower panel: n147 25 triangle-up (one beyond the axis), n1761 16 circle,
n2934 16 square (one beyond the axis), n3814 18 triangle-down (one beyond the axis), n4695 17
plus.

Marker ambiguities:
1. Lower panel, stacked symbols: the n3814 triangle-down and the n4695 plus are drawn as 17
   stacked pairs (triangle above, plus directly below, the plus's upper arm running into the
   triangle's tip), always at the same u. Both symbols are identifiable in every pair; none was
   guessed. Triangle centroids come from the top edge and width (tip hidden, v bound 2.5); plus
   centers from the horizontal bar and the lower arm.
2. Markers on the left frame (lower panel, one per series, the zero-displacement readings) and on
   gridlines: bound 3, noted. See 2.3 for their x.
3. Upper panel: the first plus (u 813) has no left arm; center at the crossing of the vertical
   bar and the right arm. The plus at u 1431 is half merged with its curve.
4. Upper panel n147: the first two triangles and the one at u 1105 have their bases merged with
   the bottom frame; centroid from tip and width, bound 3.
5. BEYOND THE AXIS (lower panel), three markers right of the 250 line, x 261 to 263:
   a triangle-up under the printed word "Rebound" (v 2558, y -75.6), a square at y -167.4 with a
   leader stroke from its base to the word "Above" of the note "Same Notation As Above", and a
   triangle-down below that note at y -193.1. Read as markers of n147, n2934 and n3814 by symbol.
   They are either rebound readings (after the normal load was removed) or symbol samples for
   the note; the page does not say which. Their x is a placement, not a shear displacement. If
   they are rebound readings, the square and triangle-down moved up by 34 and 59 units from their
   final readings while the triangle-up moved down by 5.
6. No n147 marker near x 47 in the upper panel (the run of triangles skips one step; checked on
   a pixel map at the 50 gridline: nothing under the line or the gridline).
7. Upper panel: the second n3814 marker (x 27.8) and the second n2934 marker (x 28.7) lie far off
   their drawn curves (by 125 and 167 psf). They are drawn there; recorded as is.

## 4. Traces (upper panel only; the lower panel has no drawn lines)

The five curves are drawn as thick dashes (line about 12 px thick) interrupted at every marker.
Samples were proposed by `helpers/trace.py` (follows one curve column by column from a seed
checked on the crop, skips columns within 9 px of a vertical gridline or inside a marker box,
flags runs merged with a horizontal gridline) and assembled by `helpers/assemble_p1.py` (each
dash: first column, last column, and interior columns at least 15 px apart). Every sample is a
column run on the ink, center = run center, bound v = half the run length, u = 0 (the column is
a sampling location). The ink ends were read with `plot_grid scan` and added by hand. All samples
were checked on zoomed overlays (`crops/ovz_*.png`).

Counts: n4695 68, n3814 73, n2934 75, n1761 71, n147 54 trace samples; 3 features each.

Trace ambiguities:
1. Sampling density: inside a dash the spacing is 15 to 20 px (2.5 to 3.4 thousandths). Across a
   marker the ink is interrupted, so the spacing there is 30 to 55 px (5 to 9 thousandths, the
   wider ones where a marker sits next to a vertical gridline). No sample is placed in those
   gaps; the protocol's 5-thousandths spacing cannot be met there without sampling white paper.
2. Steep parts (n4695, n3814, n2934 below x 60): the column run is 17 to 27 px long, so the v
   bound is 8 to 13 px (30 to 45 psf). The run center is still the line center.
3. Gridline crossings (n4695 at 2000, 3000, 4000 psf; n3814 at 2000 and 3000; n2934 at 1000 and
   2000; n1761 at 1000): one sample per crossing, taken at the column where the gridline lies
   inside the line's band (the run is then the line band); noted. n2934 runs along the 2000
   gridline for u 1305 to 1345 at a shallow angle; samples at u 1315 and 1320 only.
4. n147 from its start to u 920: the dashes rest on the bottom frame. For u 829 to 860 only the
   upper edge of the dash is visible (the lower edge is inside the frame ink); center estimated
   as edge plus half a line width, bound 5 px (17 psf); noted on each row. From u 893 a one-row
   gap separates dash and frame.
5. n147 last ink: the last dash runs into the left side of the triangle on the 250 gridline; the
   last sample is the last clean column (u 2192).
6. Faint dotted lines run parallel to several curves, 8 to 12 px below them (e.g. under n4695 at
   u 1695 to 1777, under n3814 at u 1800 to 1893, under n1761 at u 2010 to 2190). They are 1 to
   3 px specks, not the drawn line; no sample is on them.

Features (first point, peak of the drawn line, last point), native units:
1. n4695: first (10.8, 1650); peak 4646 psf at x about 224 (flat for x 221 to 227; x bound
   3.2); last (246.7, 4574). The line falls about 70 psf after its peak.
2. n3814: first (11.3, 1352); peak 3757 at x 245.6, i.e. at the end (the line still rises
   slightly, flat within 2 px from x 240); last (246.6, 3756).
3. n2934: first (12.2, 810); peak 2656 at x about 244 (flat from x 233 to the end); last (246.8,
   2656).
4. n1761: first (10.3, 497); peak 1604 at the end (x 245.5); last (246.0, 1600).
5. n147: first (10.5, 24, on the frame, see 4.4); peak 138 psf, flat from x 202 to 242 (x not
   defined, bound 19); last (242.2, 130).

## 5. Observations a later reader should know

1. n147, line against markers: from x 57 on, the drawn line runs 18 to 56 psf (5 to 16 px) above
   every triangle centroid; at the end the markers give 84 to 105 psf and the line 130 to 142
   psf. In ratio to the normal stress the line gives 0.88 to 0.97, close to the other four tests
   at their ends (4695: 0.99, 3814: 0.99, 2934: 0.91, 1761: 0.91), while the markers give 0.57 to
   0.71. The line runs through the upper corners of the triangles. If the drafter meant the tip
   of each triangle as the point, the n147 markers would read about 65 psf higher (19 px); with
   the bounding-box center instead of the centroid, about 16 psf higher. The drawn lines do not
   decide the convention: they also run 3 to 6 px below the centers of the squares and pluses on
   average, so a few px of offset between line and symbol is the drafter's fit, not a symbol
   convention. Cross-check from a context page (a coarse read, not part of this reading): in
   Fig. C-6A (printed C-17, PDF 131), the failure-envelope plot of this same LSM series
   (triangles, gamma 66.8 to 75.2), the triangle near sigma 150 sits at about 100 psf with its
   centroid (about 120 with its box center), which agrees with the n147 markers here (maximum
   106 psf) and not with the drawn n147 line (139 psf). The n147 values should be used with this
   in mind, together with the 17 psf zero question of 2.3.
2. The two panels do not share displacement positions, and the counts differ (upper/lower:
   n4695 15/16, n3814 13/16, n2934 13/14, n1761 13/15, n147 24/23, frame and beyond-axis
   markers excluded). Positions (50-250 map):
   - n4695: where both panels have a reading they agree within 1.7 thousandths; each panel also
     has readings the other lacks (upper 47.9, 77.0; lower 17.2, 37.5, 87.2).
   - n147: upper markers sit 0.7 to 3.2 (median 2) thousandths left of the lower ones up to
     x 200; the last two agree.
   - n3814: agree at about 8, 28, 57, 67, 97 and at the last two; between 100 and 230 the upper
     (125, 147, 166, 186, 208) and lower (117, 137, 156, 175, 196, 217) positions differ by 8 to
     10. The lower n3814 positions are those of the lower n4695 pluses they are stacked with.
   - n2934: lower about 2 to 3 right of upper up to 90; beyond 100 the two sets interleave
     (upper 107, 127, 147, 167, 187, 206; lower 100, 119, 140, 160, 180, 200, 219).
   - n1761: upper about every 20 from 8 (8, 29, 49, 68, 88, 107, ...); lower every 10 up to 40,
     then every 20 from 60 (60, 80, 99, 119, ...): the sets interleave by about 10.
   Do not pair upper and lower readings by index.
3. Stray ink that is not data: a horizontal stroke in the upper panel at u 1533 to 1612, v 1420;
   short dashes at (815, 1530) and (903, 1531); a 6 px cross at (855, 2006) (upper) and one at
   (2110, 3133) (lower); short dashes or dots beside several lower-panel markers (noted on those
   rows); a thin line under the upper panel's bottom frame (v 2213, u 1100 to 1820).
4. Context pages: p0115 (Appendix C introduction: Notre Dame tests under B. B. Schimming) and
   p0129 (Fig. C-5A, SS soil) say nothing about this sheet's plotting; p0131 (Fig. C-6A) is used
   only for the cross-check in item 1. Nothing in them explains the word "Rebound".

## 6. Files
1. `cal-p1/`, `cal-p2/`: final calibrations (x on the printed labels 50 to 250).
2. `calibration-eye-checks.csv`.
3. `points-p1.csv`, `points-p1-native.csv` (78 markers, 341 trace samples, 15 features).
4. `points-p2.csv`, `points-p2-native.csv` (92 markers).
5. `overlay-p1.png`, `overlay-p2.png`.
6. `helpers/`: `sym.py`, `tri.py`, `ystack.py`, `trace.py`, `assemble_p1.py`, `fitted_pixel.py`,
   `eye_checks.py`, `zoom.py`; marker lists `markers_p1.txt`, `markers_p2.txt`; raw tracker
   output `tr*_raw.csv`; alternative calibrations `cal-frame-included/` and
   `cal-alt-uniform-y/` (reference only, not used for the native files).
7. `crops/`: the zoomed crops and overlays used for the reading.
