# FC-3B blind reading (Claude), AM-68-1 Vol. II Appendix C, printed C-10, PDF 124

Page image `packet/p0124.png`, 3213 x 4508 px, 300 dpi, unrotated. Five direct shear tests on
RSM-a soil, loose (Dr 0 to .15): n4695 (plus), n3815 (circle), n2934 (triangle-down), n1761
(square), n734 (triangle-up), symbols as the legend on the page gives them. All work under
`out/FC-3B/`; helper scripts listed at the end.

## 1. Calibration

Upper panel (panel 1): box 660 1250 2170 2760, x gridlines 0..250 by 50, y gridlines 0..5000 by
1000, `--bands 20 --min-frac 0.4 --snap 6 --frame-frac 0.4`. 36 anchors, all lines detected.
Residuals: x rms 0.30 thou (0.12 percent of the 250 span), max 0.56; y rms 8.7 psf (0.17 percent
of 5000), max 16.9 psf (0.34 percent). The 3000 psf gridline is the weak one: from u about 1790
to 2143 the n3815 curve runs along it a few pixels below (merged ink), so the tool's right-hand
samples of that line sit 5 to 7 px low (v 1864 to 1866 instead of 1858 to 1860) and the fitted
line has a slope of 0.0081 instead of about 0.004. The affine fit absorbs most of it; the eye
check at the left end of the 3000 line is off by 0.5 px and the 0 line by 3.1 px (0.21 percent).
Kept, since every check is under the 0.5 percent limit.

Lower panel (panel 2): box 660 2850 2170 3485, same x gridlines, y values passed as
-150,-100,-50,0,50 (the tool maps the list bottom to top and predicts equally spaced lines). Only
+50 (top frame), 0 and -150 (bottom frame) are drawn on the page; -50 and -100 are `predicted`
(interpolated from the frame lines) and contribute anchors consistent with the frame. The 0 line
was detected (v 3014 + 0.0050 u). 30 anchors; residuals x rms 0.28 thou, max 0.41; y rms 0.04
thou, max 0.11.

Eye checks (`calibration-eye-checks.csv`, 12 rows, zoom-4 crops in `crops/`): all within 3.1 px,
all under 0.21 percent of the axis span.

## 2. Markers

Method: marker interiors (enclosed white regions) were located mechanically (`helpers.py holes`,
`clusters.py`), then every marker was looked at on zoom-3 column crops with the candidate center
drawn (`crops/p1/*.png`, `crops/p2/*.png`) and the hard cases on zoom-6 crops (`crops/z6/`).
Center convention: center of the symbol's outer outline. For circles and squares the hole-bbox
center was used (checked to be within 1 px of the outer-outline center, `measure.py`). For
triangles the hole is offset from the outline (thick apex), so v = hole center + 1.5 px
(triangle-down) and hole center - 1.0 px (triangle-up), the measured offsets; triangles carry a
3 px bound because of this convention. Plus signs were located from the vertical bar (columns
whose dark run through the center is 18 to 40 px long, `plusmeasure.py`), 2 px bound when clean.
Markers on a gridline, on the frame, or merged with dashes carry a 3 to 5 px bound and a note.

Panel 1 counts: n4695 12, n3815 12, n2934 11, n1761 12, n734 11 (56). Panel 2: n4695 13, n3815 12,
n2934 13, n1761 13, n734 13 (64).

Ambiguities and omissions:

1. n734 (triangle-up), panel 1, near x = 150 (u about 1555, v about 2490): the marker is buried
   in the dash ink (the line is 17 to 20 px thick there, v 2483 to 2500, u 1515 to 1600) and the
   150 gridline; its outline cannot be separated. Omitted rather than guessed. The drawn line
   there is sampled as a trace.
2. n2934 (triangle-down), panel 1: no marker at x = 250. The last dash ends at u about 2120
   (v 1952 to 1968) and nothing but the gridline is at u 2143 (`crops/z6/trid2132.png`). 11
   markers for this series.
3. n3815 (circle), panel 2, first station (x about 0, left frame): not visible. The first station
   on the frame shows triangle-up (v 3133), square (3160), triangle-down (3228) and a plus with
   its horizontal arm at v 3330 and extra ink v 3306 to 3345 under the frame line
   (`crops/z6/p2-leftframe.png`). No ring is visible; if the circle exists it is hidden under the
   frame line and the plus. Omitted; the plus row carries a note. 12 markers for n3815.
4. Markers on vertical gridlines (centers read from the outline on zoom-6 crops, bound 4 to 5):
   panel 1, x = 50 station (circle, triangle-down, square), x = 150 (plus, merged with the
   gridline and the dash), x = 250 (circle, square right side merged, triangle-up centered on the
   line); panel 2, every marker at the 100, 200 and 250 stations, where the plus bar coincides
   with the gridline (bound 5).
5. Markers on horizontal gridlines: panel 1 n2934 and n1761 at x = 10 and 30 sit with their top
   edge on the 1000 line; n2934 at x = 70 apex on the 2000 line; n4695 at x = 70 top arm on the
   3000 line; n3815 circles at x = 190, 220, 250 have the 3000 gridline and the dashes passing
   through them.
6. Broken outlines: n3815 circles at x = 130 (u 1440) and 170 (u 1667) are open where dashes
   meet them; n1761 square in panel 2 at x = 80 (u 1150) is open at top left. Centers from the
   visible outline, bound 3.
7. Panel 1 n734 at x = 110 and 130 (u 1330, 1443): the triangles sit 10 to 18 px above the
   drawn line (the author's curve passes below these two points). Real, not a reading error; the
   overlay shows it.
8. Panel 2 n4695 pluses at x = 80 and 140 touch the circle above them (bound 3).

## 3. Traces (panel 1)

Dashed lines, drawn through the marker stations with a gap at each marker (the dashes stop short
of the symbol). Sampled with `traces.py` every 5 thousandths at nominal u = 686.5 + 5.84 x,
x = 10, 15, ..., 245; a column on a marker of the series, within 5 px of a vertical gridline, or in
a dash gap is shifted by up to +-20 px to the nearest inked column and the actual column is
recorded (note `shifted`). Runs along a column (3 columns combined) are assigned to a series by
proximity (28 px) to the piecewise linear interpolation of that series' marker centers; the five
curves never cross and keep their vertical order. Bound: u 1 px, v half the run thickness (4 to
10 px; the steep first dashes give thick vertical runs, noted `steep line`).

1. Merged with the 3000 gridline: n3815 from u 1825 to 2115 (x 195 to 245) runs along the line
   a few px below it, so the dark run is gridline + curve (15 to 17 px). The curve was taken as
   the lower part of the run (run bottom minus 4.5 px, bound 4 px); the marker centers there
   (v 1866, 1865.5, 1863.5) agree within 2 to 4 px. Crossings of a gridline (n3815 at u 920 over
   the 2000 line) use the run center with the full half-thickness bound.
2. Gaps wider than 6 thousandths between consecutive samples, where the dash gap around a marker
   is too wide to reach from the nominal columns: n4695 up to 9.8 (u 1963 to 2020); n3815 up to
   8.2; n2934 up to 10.1 (u 1416 to 1475); n1761 up to 8.7; n734 up to 13.0 (u 1632 to 1708) and
   12.3 (u 1928 to 2000). Stations with no ink within +-20 px (skipped): n2934 x = 70, 110, 130;
   n734 x = 30, 90, 130, 170, 220. The markers carry the data at those stations.
3. Samples per series: n4695 48, n3815 48, n2934 45, n1761 48, n734 43 (232).

## 4. Features (panel 1)

Three per series: first point = left end of the first dash (every line starts at its first
marker, about x = 12), peak = minimum v among the trace samples (every curve is a rising curve
with a plateau; n2934 and n734 decline slightly after the peak; the plateau location is
uncertain along it, bound 3 px in u), last point = end of the last dash (u 2114 to 2121); for
four series the last marker follows on the 250 gridline, for n2934 the line simply ends at
u 2118 (x about 245) with no marker.

## 5. Other things a later reader should know

1. Legend misprint: the legend header reads "tau (PSF)" over the normal stress values 4695 ...
   734; it is sigma (normal stress), as the figures index also records.
2. The lower panel has no -50 or -100 gridline drawn; only +50, 0, -150. All dilation values are
   negative (contraction) and lie between -27 and -133 thou.
3. Vertical gridlines are at u 684.5 (0), 978 (50), 1271 (100), 1564 (150), 1854 (200), 2143.5
   (250); the frame continues to u about 2565 for the legend, so the right frame line is not the
   250 line. The scan tilt is about 0.3 deg (horizontal lines drop 6 to 7 px over the panel).
4. Marker stations: panel 1 at x about 10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 220, 250;
   panel 2 at x about 0, 20, 40, ..., 220, 250 (13 stations). The two panels do not share
   stations.

## 6. Files

`cal-p1/`, `cal-p2/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv` (305 rows: 56 markers, 232 traces, 15 features),
`points-p2.csv`, `points-p2-native.csv` (64 markers), `overlay-p1.png`, `overlay-p2.png`,
`crops/` (eye-check and reading crops), `work/` (candidate lists, raw trace output, skipped
stations, column scans). Helper scripts: `helpers.py` (fitted pixel, hole finder),
`clusters.py`, `measure.py`, `plusmeasure.py`, `annot.py` (annotated zoom crops),
`eyechecks.py`, `markers_p1.py`, `markers_p2.py` (the marker readings), `traces.py`,
`assemble.py`.
