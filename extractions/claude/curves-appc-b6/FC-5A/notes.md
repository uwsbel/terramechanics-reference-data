# FC-5A, batch curves-appc-b6: Claude reading

Figure C-5A, "Failure Envelopes - Maximum Shear Stress vs. Normal Stress", printed page C-15,
page image `packet/p0129.png` (3213 x 4221 px, bilevel). One upright panel, panel = 1.

## Calibration (`cal-p1/`, `calibration-eye-checks.csv`)

1. The panel has a full drawn grid every 1000 psf on both axes (not ticks only), so
   `tools/calibrate_axes.py detect` was used directly: box 790 1500 2310 3060, 8 bands,
   x values 0 to 5000, y values 0 to 5000. All 12 lines were detected in 8/8 bands; none is
   `predicted`. 36 anchors on drawn grid intersections.
2. Residuals: x RMS 4.97 psf (max 8.4), y RMS 4.30 psf (max 7.8), about 0.1 percent of the
   5000 psf span on each axis, well under the 0.5 percent limit. The residual comes from slightly
   uneven printed grid spacing (291 to 298 px per 1000 psf), not from a missed line.
3. The top frame line (about v 1260, would be 6000 psf) is unlabelled and was left out of the box.
4. By-eye label check, all printed labels: y labels 1000 to 5000 sit level with their tick and
   horizontal grid line (offsets -4.5 to +0.7 px); x labels 1000 to 5000 sit centered under their
   tick and vertical grid line (offsets -7 to +6 px). The corner "0" is printed just left of the
   sigma = 0 frame line (12 px), as usual for a corner label. All agree; no direction problem.
5. Restart note: `cal-p1/` was left by the interrupted reader of this figure. I re-ran the same
   detect command and the output was byte-identical, then made the label check above myself before
   using it.

## Legend and series

1. The legend prints: circle, gamma = 95.2 to 97.6 Lb./Ft.^3 (Dr = .02 to .13); square, 100 (Dr = .30);
   triangle-down, 103 (Dr = .48); triangle-up, 107 (Dr = .77). The last three are bracketed with
   "Bendix Report No. MM-65-2, Interim Report of Lunar Landing Dynamics Specific Systems
   Engineering Study". The ids in `series.csv` (dr2-13, dr30, dr48, dr77) match the printed groups.
2. Index discrepancy: the figures index row (apparatus field) says "Bendix MM-66-2"; the page
   prints "MM-65-2".
3. Units on the page are "PSF" on both axes, sigma (PSF) and tau (PSF), as indexed.

## Which line carries which printed angle

Four straight lines, all drawn solid from the origin corner. Each label is written along its line,
just above it (glyph bottoms facing the line, about 14 to 18 px clear of its upper edge):

1. 41.5° (text center u 1593.5, v 2292.5) on the steepest line, through the triangle-up symbols: dr77.
2. 36.9° (1817.5, 2233.5) on the second line, through most triangle-down symbols: dr48.
3. 32.8° (1832, 2316.5) sits between the 36.9° and 32.8° lines, about 15 px above the third line
   and 30 px below the second, baseline toward the third: dr30 (squares).
4. 29° (2070, 2271.5) above the flattest line, through the circles: dr2-13.

The order is the order of density (steeper for denser), so labels, lines and legend agree.

Angles of the drawn lines, from their straight fits in calibrated units: 41.2°, 36.4°, 33.2°,
29.6°, against the printed 41.5°, 36.9°, 32.8°, 29°. The drawn lines differ from their printed
angles by 0.3° to 0.6° (two steeper, two flatter). This is a property of the drawing, not of the
reading; the trace samples follow the ink.

## Markers (5 per series, 20 in all)

Read by eye on zoomed crops and pixel dumps; triangle centers are centroids (rule 8), squares and
circles box centers. Identity is by shape throughout; where shape and line disagree it is said:

1. dr77, triangle-up, at about sigma 307, 697, 1300, 1788, 2475 psf. The lowest one (307 psf,
   344 psf) is 22 px above the 41.5° line; the others are on or within 16 px of it.
2. dr48, triangle-down, at about 697, 1321, 1792, 2483, 3684 psf. The one at 1792 psf
   (tau 1454 psf) sits midway between the 41.5° and 36.9° lines, about 34 px from each, stacked
   base to base under the triangle-up of the same normal stress (an hourglass shape). Shape decides
   (rule 9). The one at 3684 psf is 21 px below its line.
3. dr30, square, at about 699, 1328, 1803, 2488, 4071 psf. The one at 1803 psf (tau 1108) is 20 px
   below the 32.8° line and 30 px above the 29° line; by shape it is dr30.
4. dr2-13, circle, at about 743, 1733, 2918, 3793, 4663 psf. The circle at sigma 743, tau 850 psf
   is far off its group's line: 130 px above the 29° line and even 60 px above the 41.5° line
   (tau/sigma 1.14). It is a clean, isolated circle of the same size as the other circles, so it is
   recorded as dr2-13 with that note. The authors' 29° line ignores it.
5. The stacked group at about 700 psf (triangle-up over triangle-down over square, u 1007 to 1041,
   v 2821 to 2904) is crowded: the triangle-down's apex reaches into the square's top side and the
   lines run through the group. Each symbol's interior is visible, so all three are identified;
   their bounds are 3 px horizontally and 4 to 6 px vertically.
6. Rule 9 data-sheet check: only the circle group has data sheets in this appendix and they are not
   in this packet, so no identity was settled from data-sheet peaks. None of the identities above
   needed it, since every symbol's shape is readable.

## Traces

1. Samples at the left end, every 250 psf of normal stress, and the right end. Left ends at the
   origin corner (u 825, first column right of the sigma = 0 frame line), where the four lines and
   both frame lines merge into one wedge; their v is the line's straight fit, bound 8 px.
2. At sigma 250 psf (u 894) the four lines are one merged band (v 2959 to 3000). The samples there
   use each line's straight fit (bound 8 px); the band's upper edge confirms the 41.5° line and its
   lower edge the 29° line. From 500 psf on, the lines are separate.
3. Where a sample column is a grid line (multiples of 1000 psf) or the line crosses a horizontal grid
   line, the center is a straight fit of the line's clean ink within 30 px on both sides (on one side
   only for the 29° line at 3000 psf, where its ink starts at the grid line). Elsewhere it is the
   center of the dark run in that column.
4. Bounds: u 2 px (sampling column), v half the line's vertical run (7.5, 6.5, 6, 6 px for the
   41.5°, 36.9°, 32.8°, 29° lines); ends u 3 px.
5. Right ends: 41.5° line at u 1680 (sigma 2943); 36.9° at u 1966 (3919); 32.8° at u 2154 (4560),
   just below the 3000 psf horizontal grid line; 29° at u 2280 (4988), where its last dash meets
   the right frame.
6. Dashed part: only the 29° line has one, to the right, beyond its last circle: two dashes, u 2212
   to 2235 and u 2246 to 2280 (sigma about 4757 to 4835 and 4875 to 4990). Its only sample on the
   dashed part is the right end (marked "dashed"). No line has a dashed extension to the shear
   axis; all are drawn solid into the origin.
7. The lines are drawn with breaks around many symbols: the 29° line is interrupted around every
   circle (u 1310 to 1359, 1640 to 1693, 1906 to 1957, 2164 to 2212), the 32.8° line around the
   squares at 700, 1300, 2450 and 4050 psf (u 1022 to 1037, 1199 to 1220, 1538 to 1557, 2001 to
   2021), the 36.9° line inside the triangle-down at 2450 psf (u 1538 to 1550).

Samples left out (rule 7: on a symbol or in a white gap):

1. dr77 (41.5°): 750 (line merged with the base-right corner of the triangle-up at 700), 1250 (meets
   the base-left corner of the triangle-up at 1300), 1750 (on the left side of the triangle-up at
   1800), 2500 (on the right side of the triangle-up at 2450).
2. dr48 (36.9°): 750 (meets the top-right corner of the triangle-down at 700), 2000 (white gap: both
   this line and the 2000 psf grid line are interrupted at their crossing, u 1398 to 1410,
   v 2584 to 2598), 2500 (inside the triangle-down at 2450, line broken).
3. dr30 (32.8°): 750 (on the right side of the square at 700), 1750 (at the top-left corner of the
   square at 1800), 2500 (inside the square at 2450, line broken).
4. dr2-13 (29°): 750 (touches the bottom-right corner of the square at 700), 1750 and 3750 (gaps
   around circles), 4750 (white, 2 px before the first dash starts at u 2212).

## Features

1. Intercept, one per series: the line's straight fit (its own ink from u 1000 to its right end)
   met with the sigma = 0 grid line. tau at sigma = 0: -1, +16, -6, -20 psf for dr77, dr48, dr30,
   dr2-13, each with a bound of about 31 psf, so all four are consistent with zero cohesion. The
   intercept is not separately visible on the page: the four lines and both frame lines merge into
   one wedge of ink at the corner (v 3012 to 3033).
2. Label, one per series, at the center of the printed angle's text box (bound 5 px).

## Ambiguities for the adjudicator

1. A small white slot with vertical edges at u 903 to 908, v 2953 to 2962 (sigma about 290 psf,
   tau about 230 to 260 psf), inside the merged ink of the converging lines just below the
   triangle-up at 307 psf. A line cannot have a hole, so the lines may be broken around something
   there; it could be the remnant interior of a hidden symbol (a square or triangle-down at the
   lowest normal stress), or an ink dropout. No outline is identifiable, so it is not recorded as a
   marker. Each Bendix group already shows five symbols, and so does the circle group.
2. A thin streak (3 to 4 px) parallel to the 29° line and just below it, about u 960 to 990,
   v 2950 to 2966. It is treated as a drafting or scan artifact and was not sampled.
3. The circle at sigma 743, tau 850 psf (see Markers, item 4) is an outlier for its group; it is a
   reading of the ink, not an error.

## Files

1. `cal-p1/anchors.csv`, `cal-p1/calibration.json`: calibration (tool output).
2. `calibration-eye-checks.csv`: printed labels against the fitted lines.
3. `points-p1.csv`, `points-p1-native.csv`: 20 markers, 57 trace samples, 8 features.
4. `overlay-p1.png`: all points over the page (box 790 2120 2310 3060).
5. `crops2/`: my zoomed crops and overlay zooms; `crops/` is from the interrupted earlier reader.
6. `helpers/`: `linefit.py`, `dump.py`, `runs.py` (earlier reader, reused after checking);
   `colruns.py`, `samples.py`, `ring.py`, `comps.py`, `build_points.py`, `eye_checks.py`,
   `show.py` (this reading). `build_points.py` regenerates `points-p1.csv`.
