# FC-2C blind reading (Claude), page image packet/p0122.png

Direct shear data sheet, PS soil, dense (Dr 1.15 to 1.3). Upper panel: shear stress (psf, 0 to 6000)
versus shear displacement (thousandths of an inch, 0 to 250 on the labeled grid; the frame extends to
about 326 on the right, past the last label, and that right frame line was excluded from the
calibration box). Lower panel: dilation displacement (-100 to +100 thousandths) versus the same
abscissa. Six series; symbols as read from the curves (the legend lists only sigma and gamma, no
symbols): n4400 asterisk, n3660 x, n2995 square, n2200 triangle-up, n1468 open circle, n734 filled
circle. The lower panel says "Same Notation As Above".

## Legend misprints

1. The legend header reads "tau (PCF)" where gamma (unit weight) is meant.
2. The third legend line reads **2935** psf on the page (zoomed crop `crops/legend.png`), while
   `packet/series.csv` and the figures index give 2995. I kept the series id `n2995` as instructed;
   whoever reconciles should check which value the test tables carry. (The gamma, 31.7, matches.)

## Calibration

1. Panel 1: box 670 1050 2175 2835, x values 0..250 step 50, y values 0..6000 step 1000, bands 20,
   min-frac 0.35, snap 6, frame-frac 0.4. All 13 lines detected (the 4000 and 3000 lines in 15/20 and
   11/20 bands, because curves and the legend cover parts of them; none predicted). 42 anchors;
   RMS residual x 0.47 (0.19 percent of the 250 span), y 2.8 psf (0.05 percent of 6000).
2. Panel 2: box 670 2935 2175 3550, y values -100, 0, 100, bands 12. All 9 lines detected;
   18 anchors; RMS x 0.34 (0.14 percent), y 0.62 (0.31 percent of the 200 span).
3. Eye checks (`calibration-eye-checks.csv`): four labels per axis per panel, read on zoom-4 crops
   with a 10 px grid. Largest difference 1.1 px (panel 2, -100 line at the right end), all under
   0.2 percent of span. The scan tilt is real: horizontal lines drop about 0.4 px per 100 px to
   the right (6000 line at v 1067 on the left, 1072 on the right), so single-row readings would be
   off by up to 6 px across the panel; the band fit handles it.

## Method

1. Markers read by eye on zoom-3 crops (10 px grid) over the whole curve region, then zoom-4,
   zoom-6 and zoom-8/12 crops of every crowded or boundary spot (crops kept under `crops/`).
   Marker center = center of the symbol's bounding box (for a triangle, that is the center of the
   box, not the centroid). Isolated lower-panel symbols were also measured as connected-component
   bounding boxes by `helpers/sweep.py` (grid lines removed), and those centers were used where
   they agreed with the eye to 1 to 2 px.
2. Traces: a column scan cannot follow these curves (the starts are near vertical, the lines are
   dashed, and four curves run within 30 px of one another near the origin), so I wrote
   `helpers/follow.py`, a ridge follower that walks each drawn line in 4 px steps along its local
   direction, re-centering on the ink across the perpendicular, bridging dash gaps by continuing
   straight. Samples were then taken at x = 3, 8, 13, ... thousandths (columns away from the
   vertical gridlines at 0, 50, 100, ...), using the nearest tracked ink point within 6 px of the
   column (its actual u is recorded). Every sample was checked on an overlay, and every place
   where the follower was pulled by a marker or a gridline was re-read by eye on a zoom-5/6 crop;
   those rows say "by eye" in `note`. Bounds: u 2 px (3 where the column was shifted to the
   nearest ink), v half the measured run length (min 2), wider with a note where a marker or a
   gridline shares the ink. On the near-vertical starts the v bound is in pixels of the line, so
   the diff's slope term must carry the rest.
3. Features: first point, peak and last point per series, read by eye (crops `c1` to `c8`,
   `z1` to `z10`). Peaks of all six curves are plateaus; the recorded point is the middle of the
   plateau and the note gives its extent.
4. `points-p1.csv`: 232 rows (70 markers, 144 trace samples, 18 features). `points-p2.csv`:
   53 marker rows. Sequence numbers run 1 up within each (series, point_kind).

## Ambiguities, panel 1

1. **Curves merged with gridlines.** n2200 runs along the 3000 psf gridline from u 1240 to 1470:
   below it (v 1949) from 1238 to 1268, crossing it at about 1275 to 1295, then 3 to 10 px above
   it (v 1930 to 1933) to the end at 1470. n1468 runs along the 2000 psf gridline from u 1000 to
   1162: under it at 1000 (v 2238), merged at 1030, then a thick dash 3 to 6 px above it (v 2219)
   from 1070 to 1147, ending at the circle at 1162. n2995 ends at the square at 1570 whose lower
   edge sits on the 4000 psf gridline; the gridline continues to the right and is not the curve.
   n3660 touches the 4000 gridline at u 1026 (end of a dash). n4400 crosses the 5000 gridline
   between u 1205 and 1240 while passing through the asterisk at 1216.
2. **Dashed lines.** n4400, n3660, n2995, n2200 are drawn dashed; where a sample column fell in a
   gap the nearest dash end within 6 px was used and the note says so. Beyond the last dash the
   drawn line ends at the last marker for n4400 (asterisk 1689), n3660 (x 1637) and n2995
   (square 1570); n2200 ends with a dash on the gridline at 1470; n734 ends with a dash at 1087
   (past its last marker at 1041); n1468 ends at the circle at 1162.
3. **Markers inside which the line position is uncertain.** Samples inside triangles at u 1052,
   1167 and 1401 and inside the squares at 1052, 1102 and 1461 carry a 5 to 7 px v bound.
4. **Possible extra triangle at (965, 2116)**, n2200 marker sequence 6: between the triangles at
   934 and 1052 only a horizontal bar (u 951 to 979 at v 2124) is distinct; its left edge would
   coincide with the drawn line and its right edge with the x=50 gridline. Recorded with a 6 px
   bound and marked UNCERTAIN; it may be a stroke, not a marker. Without it the n2200 series has
   11 triangles.
5. **Markers on gridlines or the frame:** the first circle (705, 2685) is half on the left frame
   line; squares at 821 (3000 line), 988 (x=50), 1283 (x=100), 1570 (x=150); x at 987 and 1282;
   asterisks at 1216 (5000 line), 1285 and 1571; triangles at 874 (base on 2000 line), 1287,
   1344, 1401 (3000 line); circles at 983, 1048, 1162; filled circle at 759 (1000 line). Bound 3
   to 4 px.
6. **Squares with a dash printed under them** at (753, 2069) and (1222, 1661): a short horizontal
   stroke 15 px below the center. Probably a dash of the line or a pen slip; not read as a point.
7. **Stray ink:** specks at about (997, 1960) and (1112, 2556) in the upper panel and
   (1632, 3094) in the lower panel. Not markers.
8. Marker counts per series: n4400 16, n3660 17, n2995 12, n2200 12 (11 certain), n1468 8, n734 5.

## Ambiguities, panel 2 (the whole panel is one)

1. The symbols are 11 to 20 px, drawn at 0 to 25 thousandths of dilation, so at nearly every
   abscissa three or four symbols are stacked and merged (columns at u 708/722, 739/750, 980
   (on the x=50 gridline), 1041, 1101, 1160, 1218, 1277 (on the x=100 gridline), 1334, 1392,
   1450). I separated stacks by their holes and outlines on zoom-8 and zoom-12 crops
   (`crops/p2z-*.png`, `crops/w*.png`). The ordering inside the stacks is consistent where it can
   be seen: filled circle highest (most dilation), then circle, square, triangle, x, asterisk
   lowest.
2. **Symbol identity is uncertain for the small open symbols.** Rounded squares and circles
   differ only by a flat top and a rectangular hole at this size; I called flat-topped symbols
   with rectangular holes squares and round ones circles, and noted "circle or square" where the
   crop does not decide. The second open symbol in the stacks at 1334, 1392 and 1450 is the
   weakest call (notes say so). The symbol at (1393, 3167) has a pointed top and is recorded as a
   triangle with the note "triangle or square".
3. **Abscissae do not line up with the upper panel.** The lower-panel x markers appear only from
   u 1219 onward while the upper-panel x series has 17 markers from u 721; the lower panel has
   circle-like symbols out to u 1450 while the upper n1468 curve ends at 1162; the filled circles
   in the lower panel sit at 722, 750, 804, 862, 980, 1043 versus 723, 759, 814, 928, 1041 above.
   Either the dilation readings were taken at different displacements, or some of my symbol
   calls in the merged stacks are wrong. The reviewer should treat the series assignment in the
   lower panel as provisional and compare it with the other reading symbol by symbol.
4. The two leftmost stacks (u 700 to 760) sit on the zero gridline and the x=0 frame region;
   (708, 3227) and (739, 3217) are squares by shape, (722, 3230) and (750, 3223) solid blobs
   taken as filled circles (an x is 20 px wide here, these blobs are 13 px).
5. The top of the stack on the x=50 gridline (980, 3178) is a dark blob merged with the gridline;
   I inferred a filled circle from the ordering, bound 4 px.
6. No markers below the zero line (no negative dilation) and none above v 3140 except the filled
   circle at (1043, 3149); `helpers/sweep.py` lists every ink cluster in the panel.
7. Lower-panel marker counts: n2995 10, n734 6, n1468 11, n2200 8, n3660 8, n4400 10 (53).

## Files

`cal-p1/`, `cal-p2/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `points-p2.csv`, `points-p2-native.csv`,
`overlay-p1.png`, `overlay-p2.png`, `crops/` (all zoomed crops read), `helpers/`
(`follow.py` ridge follower and its per-series polylines `follow-*.csv`, `samples-auto.csv` and
`overlay-auto.png` from the first automatic pass, `track.py` and `track2.py` the abandoned
column trackers, `sweep.py` ink-cluster sweep, `build_points.py` which writes the two points
files from the readings).
