# FC-1C (Figure C-1C, printed C-4, PDF 118): blind reading notes

Reader: Claude (blind; only `packet/` and `tools/` were used). Page image `packet/p0118.png`,
3263 x 4508 px, 300 dpi, unrotated. Pixel coordinates below are (u, v) of that image.

## 1. Calibration

1. Upper panel (panel 1): box 595 1085 2115 2870, x values 0..250 step 50, y values 0..6000
   step 1000, `--bands 22 --min-frac 0.4 --snap 6 --frame-frac 0.4`. 42 anchors; x rms
   0.41 (max 0.65) thousandths, y rms 7.2 (max 16.7) psf, i.e. 0.17 and 0.28 percent of the
   spans. The right frame line of the page box (u about 2536) is not a value line: the plot area
   ends at the x = 250 gridline (u about 2086 to 2091) and the legend sits to its right, so
   the box was cut at u 2115 so that the x = 250 gridline is the last vertical line.
2. The 5000 psf line was `predicted` (the legend text "gamma = 49.2 to 51.1 ..." sits on it
   and breaks it). Checked: a column scan at u 1900 and 2050 finds the line at v 1398.5, the
   fit gives 1397 to 1399 there; by eye at u 640 the (faint) line is at v about 1402. Within
   1 px at a 3.5 psf/px scale; accepted.
3. The 4000 psf line was found in 11 of 22 bands only: the n3520 and n2935 curves run along
   it between x 90 and 160 and the detector drops the merged runs. The 11 detections agree
   with the eye.
4. Lower panel (panel 2): box 600 2965 2120 3590, y values -100, 0, 100, same x values,
   `--bands 20`. 18 anchors; x rms 0.37 (max 0.58), y rms 0.22 (max 0.37) thousandths of an
   inch (0.15 and 0.11 percent of the spans). No predicted lines.
5. Eye checks (3 to 4 labels per axis per panel, zoom-4 crops under `crops/eye-*.png`) are
   in `calibration-eye-checks.csv`; all agree with the fit within 3 px (worst: p2 x = 0, 2.3 px;
   p1 y = 5000, 3 px on a faint line). Both panels are tilted: the vertical gridlines drift
   about +0.004 to +0.005 px of u per px of v, the horizontal ones about -0.0015 to -0.0025 px
   of v per px of u (so u of a given gridline differs by about 13 px between the two panels).

## 2. Markers

1. Rough centers were read by eye on zoom-3 crops (400 x 300 px tiles, `crops/p1-*.png`,
   `crops/p2-*.png`), then zoom-4 tiles of the dense band of panel 2 around the zero line
   (`crops/p2z-*.png`), zoom-5/6 crops of the clusters on each vertical gridline (`crops/g*.png`)
   and of ambiguous symbols (`crops/q*.png`, `crops/t-*.png`).
2. `helpers/refine_markers.py` sharpened each center: for x, asterisk, plus, square and
   circle the point of best 180-degree self-overlap of the ink within 13 px (a straight line
   through a symbol is itself centrally symmetric, so it does not bias the center); for
   triangles the mirror-symmetry axis for u and the bounding-box center (base edge to apex)
   for v. Where this moved a center by more than 3 px (clutter pulled it toward a neighbour,
   which happened for 4 markers in panel 1 and 15 in panel 2) the by-eye value was kept with a
   3 px bound (`helpers/finalize_markers.py`); four panel-1 centers were re-read on zoom-6
   crops (`helpers/overrides-p1.csv`). Triangle "center" means the center of the symbol's
   bounding box, not its centroid.
3. Bounds: 2 px for a clean symbol, 3 px when on a gridline, touching another symbol or
   crossed by a line, 4 px for the two uncertain symbols and the x = 0 cluster of panel 2.

### Panel 1 (shear stress), 79 markers

Legend as printed: x = 3520 psf (49.5 pcf), asterisk = 2935 (49.7), square = 2345 (49.2),
plus = 1760 (50.3), triangle-down = 1172 (49.4), triangle-up = 587 (51.1), circle = 294
(49.4). Counts: x 15, asterisk 10, square 12, plus 10, triangle-down 11, triangle-up 12,
circle 9.

1. Markers on gridlines: x at x = 10 (on the 2000 psf line), x = 50, x = 150, and on the 4000
   psf line (x = 91); asterisk at x = 100 and three on or touching the 4000 psf line (x 121,
   141, 160); square at x = 50 and on the x = 250 line; plus at x = 50 and on the x = 250
   line; triangle-down at x = 20 (on 1000 psf) and x = 100; triangle-up at x = 50, x = 150,
   and its second marker (x = 32) has its apex on the 1000 psf line; circle at x = 100.
2. Beyond the axis range: the last x marker (u 2104, x about 252.4) and the last asterisk
   (u 2102, x about 252) sit to the right of the x = 250 gridline, inside the legend area.
3. The first asterisk (x 62, 3486 psf) is drawn on top of the n3520 (x) line; its center was
   read on a zoom-6 crop (`crops/t-ast1.png`).
4. The n2935 (asterisk) series has no markers and no separate drawn line below x about 62:
   its curve begins at the first asterisk, just right of the n3520 line.
5. The fourth triangle-up (x 70) is partly filled by the line ink; bound 3.
6. The n1760 (plus) series has two markers close together at x 50 and x 61 (both clearly
   drawn).

### Panel 2 (dilation), 87 markers

Same symbols. Counts: x 12, asterisk 14, square 13, plus 13, triangle-down 13, triangle-up 13,
circle 9. The lower panel has no drawn lines, only symbols, so no trace points.

1. The symbols crowd around the zero line between x 0 and x 130; many touch or overlap.
   Every such case carries a note and a 3 px bound. Overlapping pairs: square over x at
   x 71, 91, 111 (the x sits just below the square, touching); asterisk beside or over a square
   at x 143, 161, 184, 204, 217, 246; circle over triangle-up at x 141; asterisk between circle
   and triangle-down at x 19.
2. The symbol at (1047, 3293), x 71, has a round-cornered outline and could be read as a
   circle; the circle series already has its nine markers (matching panel 1) and the square
   series has a marker at this x in panel 1, so it is recorded as a square with a note.
3. On the x = 100 gridline, just above the zero line, a symbol at (1219, 3267) is recorded as
   asterisk (its vertical arm merges with the gridline) and one at (1221, 3306) as plus; both
   carry "symbol uncertain" notes and 4 px bounds. Only the asterisk, triangle-down and circle
   series have panel-1 markers at x = 100.
4. At x = 0 the gridline carries a stack: triangle-up (v 3294), triangle-down (v 3325), plus
   (v 3367) and an asterisk just to the right (u 654). There may be more symbols hidden in this
   stack; the x series has only 12 markers in panel 2 against 15 in panel 1 (none found for
   x about 10, 40 and 51), and no square or x was found at x = 0. Not guessed.
5. Several series have panel-2 markers at x values that have no panel-1 counterpart (asterisk
   at x 4, 19, 37, 52; square at x 41; plus at x 0; triangles at x 0), and the square at x 41
   (y about -4) breaks the otherwise smooth square sequence; it is a clear square on the page
   (`crops/q860.png`). The asterisk at x 52 (y about -16) is likewise off the trend of its
   neighbours (about -5); it sits in the cluster on the x = 50 gridline (`crops/g50.png`).
6. Beyond the axis range: plus at u 2122 (x about 254). On the x = 250 gridline: triangle-down,
   square, x; asterisk just left of it.

## 3. Traces (panel 1 only)

1. All seven upper-panel curves are dashed lines, with gaps of about 15 to 20 px on either
   side of every marker and shorter gaps elsewhere. `helpers/read_traces.py` samples each
   curve at x = 2.5, 7.5, ..., 247.5 (every 5 thousandths, never on a vertical gridline),
   moving the column 20 px off any marker of the same series and, when the column falls in a
   gap, stepping away from the nearest marker in 3 px steps until ink is found (noted on the
   point). The curve is identified at each column as the dark run nearest the piecewise-linear
   interpolation of that series' own markers; bare horizontal gridline runs (7 px or thinner
   at a gridline v) and runs thinner than 5 px (dash-end remnants) are skipped. Every sample
   was checked on the overlay (`overlay-p1.png`, zoomed checks `crops/ov-*-z.png`); the first
   pass had put two samples on the edges of the square at x 140 and one in a dash gap at x 205,
   which is why the clearance and the thin-run rule above exist.
2. Bound: 1 px in u; in v half the vertical cut of the line (3 px minimum, 4 to 5 px for the
   9 to 10 px line). On steep segments the vertical cut is longer (15 to 20 px) and the bound is
   half of it (noted "steep segment"). Where the curve runs along a horizontal gridline the two
   merge; the merged run's center is used with a wider bound and the note "merged with the
   horizontal gridline": n2935 along 4000 psf (x 112 to 155), n2345 at the 3000 psf crossings.
3. Shared ink: the n3520 and n2935 curves run within 25 px of each other between x 60 and 75
   (notes "another run within 25 px"); the n3520 trace there is the upper run.
4. Features: first point = the first marker (every line starts at its first marker); peak =
   minimum v of the drawn line on a 1 px column sweep that skips the symbols (the flat-top
   extent, v within 1 px of the minimum, is recorded in the note and as the u bound); last
   point = the last marker for n3520, n2935, n2345, n1760 and n294 (the circle line ends at its
   ninth marker, x 180), and the point where the line meets the x = 250 gridline (read at
   u 2080) for n1172 and n587, whose lines run on past their last marker.
5. Peaks (native): n3520 4312 psf at x 171 (flat 161 to 183); n2935 4023 at x 129 (flat 125
   to 134); n2345 3102 at x 174; n1760 2847 at x 156 (flat 153 to 165); n1172 1812 at x 109
   (flat 105 to 113); n587 1363 at x 94; n294 751 at x 96 (flat 89 to 107). The n2345 curve has a
   second hump at x 173 after a shallow dip at x 110 to 130, and its square marker at x 170 sits
   slightly above the drawn line.
6. Stray ink: a thin horizontal stroke to the right of the first circle (u about 775 to 817,
   v about 2710), below the drawn n294 line; not sampled.

## 4. Files

`cal-p1/`, `cal-p2/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`,
`points-p1.csv` (79 markers, 303 trace samples, 21 features), `points-p1-native.csv`,
`points-p2.csv` (87 markers), `points-p2-native.csv`, `overlay-p1.png`, `overlay-p2.png`,
`crops/` (every crop looked at, including the zoomed overlay checks `ov-*-z.png`), `helpers/`
(`rough-p1.csv`, `rough-p2.csv`: the by-eye reads; `refine_markers.py`, `finalize_markers.py`,
`overrides-p1.csv`, `read_traces.py`, and the intermediate `markers-*.csv`, `traces-p1.csv`).
