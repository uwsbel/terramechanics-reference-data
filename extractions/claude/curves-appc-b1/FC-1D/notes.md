# FC-1D blind reading (Claude), page image packet/p0119.png

Direct shear data sheet, RS soil, Dr 1.0 to 1.16, seven tests (3520, 2935, 2345, 1468, 587, 294
and 0 psf). Upper panel: shear stress 0 to 6000 psf vs shear displacement 0 to 250 (frame runs to
about 325); lower panel: dilation -100 to +100 vs the same displacement. Scan tilted about 1.1
degrees (horizontal gridlines drop 25 px over the panel width, vertical ones shift 47 px over the
upper panel height); the affine calibration absorbs it.

## 1. Calibration

1. Upper panel: `calibrate_axes.py detect --box 530 1120 2110 2950 --x-values 0..250 --y-values
   0..6000 --bands 22 --min-frac 0.3 --snap 6 --frame-frac 0.4`. The box ends just right of the
   x=250 gridline so that line is the right "frame" (the printed frame is at x about 325, not a
   labeled value). Residuals: x rms 0.345 (max 0.50) thousandths, y rms 7.2 (max 15.9) psf, i.e.
   0.14 and 0.12 percent of the spans. With min-frac 0.4 the x=50 line (interrupted by legend text
   and curves) was fitted with a wrong tilt (slope 0.010 vs 0.021 for the others), so min-frac 0.3
   was used; the y=5000 and y=1000 lines were found in only 10 to 12 of 22 bands (curves run along
   them) and their fitted tilts differ a little (-0.012 to -0.013 vs -0.018), which the eye checks
   below show is harmless.
2. Lower panel: `--box 530 2990 2110 3665 --x-values 0..250 --y-values -100,0,100 --bands 12
   --min-frac 0.4 --snap 6 --frame-frac 0.4`. Residuals: x rms 0.35 (max 0.61), y rms 0.44
   (max 0.63) thousandths of dilation (0.2 percent of the span). The x=250 line was fitted with a
   smaller tilt than its neighbours (0.008 vs 0.021); its position checks by eye to 2 px.
3. Eye checks (`calibration-eye-checks.csv`): three labels per axis per panel read on zoom-6 crops
   (`crops/eye/`). All within 1.5 px except lower-panel x=250 (2.2 px, 0.4 thousandths). No
   `predicted` lines in either calibration.

## 2. Markers (both panels)

Read by eye on zoom-4 tiles (`crops/tiles/`, 20 px grid) and zoom-6 detail crops (`crops/detail/`,
10 px grid) where symbols overlap, sit on gridlines or straddle tile edges. Center = center of
the symbol's bounding box (for triangles too). Bounds: 2 px for x, asterisk and filled dots,
3 px for open squares, circles and triangles, wider with a note where a symbol sits on a gridline,
on another symbol or merged with the drawn line.

Legend as printed: 3520 x, 2935 asterisk, 2345 square, 1468 triangle-down, 587 triangle-up. The
294 and 0 psf rows of the legend have NO symbol; from the curves, 294 is the open circle and 0 the
filled dot. The vocabulary has no "filled circle", so the 0 psf test is recorded as `circle` with
the note "filled circle (dot)" on every row. The legend "symbols" for 3520, 2935, 2345 and 587 are
simply the last data marker of each curve, which ends on the x=250 gridline next to the legend
text; they are recorded as data markers with a note. The 1468 row has no symbol next to it at all
(its line ends at the gridline without a marker there).

Counts, upper panel: n3520 12, n2935 10, n2345 12, n1468 12, n587 12, n294 7, n0 7.
Counts, lower panel: n3520 13, n2935 12, n2345 15, n1468 12, n587 12, n294 8, n0 7.
The two panels do not have the same displacements per test (e.g. the lower panel has squares at
x about -6, 7, 20, 28, 39 where the upper has only 19 and 39), so the lower panel was read on its
own, not by matching the upper.

## 3. Traces (upper panel only; the lower panel has no drawn lines)

`trace_helper.py` follows each drawn line as a ridge from its first marker (3 px steps, dark
segment on a line normal to the local direction, thin ink on a gridline rejected, points far from
the marker polyline rejected so a neighbouring curve cannot capture it). The n2345 tail beyond
u=1600 (x > 160), where that line runs 30 to 75 px below its squares and the follower was pulled
off it, was taken from column scans instead (`build_points.py: scan_n2345_tail`). Samples every
5 thousandths at the nearest tracked point not on a vertical gridline and not within 17 px of a
marker center; bound = half the line thickness (lines are 10 to 14 px thick, so 5 to 7 px), 8 px
where the line merges with a gridline or symbol. Trace samples therefore sit at x = 5k plus or
minus up to 2.5 thousandths; the diff interpolates. Everything checked on `overlay-p1.png`.

Features: first point = first marker (every line starts at its first marker); peak = minimum v
of the drawn line (the plateaus of n3520, n2935, n2345 and n1468 are within 4 px of the maximum
over 60 to 150 px, noted on the row); last point = end of the ink (the five long lines end on the
x=250 gridline, n294 ends at x about 158 just before its last circle, n0 ends at x about 145, well
past its last dot at 130).

## 4. Ambiguities and things a later reader should know

Upper panel:

1. n3520 has an x marker at x about 50 ON the x=50 gridline (857.5, 1667) that is invisible in
   the page overview; found on `crops/detail/U1-x50-gridline.png`. Twelve x markers in all.
2. n2935 may have a marker hidden where the x=50 and y=4000 gridlines cross (853, 1753): the line
   passes exactly through the intersection and nothing can be told apart there. Not recorded.
3. n3520, n2935 and n587 markers on the x=150, x=200 and x=250 gridlines; n2345 on x=100, x=200,
   x=250; n1468 on x=50 and x=200; n294 on x=100 and along the y=1000 gridline (two circles sit on
   it). Bounds widened to 4 px.
4. n2345: the squares at x about 39 (794, 1930), 181 (1625, 1844) and 200 (1737, 1840) sit 30 to
   75 px ABOVE the drawn line; the line is a smooth fit through the others. Read as drawn.
5. n1468: the triangle at x about 181 (1632, 2140) is 25 px above the line; the triangle at
   x about 159 (1506, 2145) is merged with the line (bound 4 px).
6. n3520: the plateau between x 100 and 130 lies within a few px of the y=5000 gridline; the line
   is heavier than the gridline and was followed by thickness. n294: plateau x 60 to 100 runs on
   the y=1000 gridline (bound widened).
7. Stray ink, not recorded: short dash at (976, 2532), specks at (1633, 1810) and (2000, 2250).

Lower panel:

1. Dense cluster at x 0 to 15 around the zero line. Three symbols are LEFT of the x=0 frame line:
   square (565.8, 3364, x about -6), triangle-down (585, 3344, x about -2) and triangle-up (592.5,
   3376, x about -1); the two triangles share an apex region. Recorded with 4 px bounds.
2. n3520 first lower marker (598, 3402.5) sits on the x=0 frame line; it looks like an x with the
   frame line through it, so it could also be read as an asterisk. Recorded as x with a note.
3. At x about 68, 89 and 120 the triangle-up (587) and triangle-down (1468) overlap into a
   "diamond" sharing a horizontal bar; centers taken from the free apex and the shared bar
   (bounds 4 and 5 px). At x about 48 to 52 the two triangles overlap partly on the x=50 gridline.
4. Squares printed incompletely: x about 120 (1298, 3241, left side open) and x about 219 (1879,
   3134, only top, right and part of the base; bound 4 px).
5. Points above the +100 frame line, calibration extrapolated: n0 at x 110 (+115) and 130 (+131),
   n294 at x 159 (+106), n587 at x 220 (+103, center on the frame line) and 250 (+112).
6. Several symbols sit on the zero line (squares at x 7, 28, 39; circle at x 20; x at x 69): bound
   4 px in v.
7. Stray ink, not recorded: specks at (912, 3444) and (765, 3315).

## 5. Files

`cal-p1/`, `cal-p2/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `points-p2.csv`, `points-p2-native.csv`,
`overlay-p1.png`, `overlay-p2.png`, helpers `make_tiles.sh`, `trace_helper.py` (marker
coordinates for the upper panel live in its MARKERS table), `build_points.py` (lower-panel marker
table, notes, subsampling), `trace-raw.csv` (every ridge-follower step with flags), and the crops
under `crops/` (eye checks, tiles, detail).
