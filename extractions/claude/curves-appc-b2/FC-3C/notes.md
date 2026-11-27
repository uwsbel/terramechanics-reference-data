# FC-3C blind reading (Claude), AM-68-1 Vol. II Appendix C, printed C-11, PDF 125

Page image `packet/p0125.png` (3213 x 4508, 300 dpi, unrotated). RSM-a soil, gamma 75 pcf,
Dr 1.0 to 1.3; five direct shear tests, legend symbols read off the page: plus = 4695 psf,
circle = 3815, triangle-down = 2934, square = 1761, triangle-up = 734. The lower panel says
"Same Notation As Above" and uses the same symbols.

## 1. Calibration

1. Upper panel (`cal-p1/`): box 790 1330 2295 2850, x values 0..250 step 50, y values 0..5000
   step 1000, bands 22, min-frac 0.4, snap 6, frame-frac 0.4, dark 160. 36 anchors. Residuals:
   x rms 0.37 thou (max 0.52; 0.15 percent of the 250 span), y rms 4.7 psf (max 7.9; 0.08
   percent of 6000). All 12 lines detected in 17 to 22 of 22 bands, none predicted.
   Why the box stops at the 250 gridline and at the 5000 gridline: the plot frame continues
   right of x=250 (to about x=325 at u 2718) with no printed value, and the top frame (6000) is
   hidden under the legend inset for u < 1760; with the box at the frame the tool took the
   inset's lower edge for the 6000 line (y rms 47 psf, max 97). Fitting on the 0 to 5000
   gridlines and the 0 and 250 gridlines fixed that. Values above 5000 psf and right of x=250
   are extrapolations of the affine map (the n4695 curve peaks near 5560 psf; a few markers sit
   on the x=250 gridline itself).
2. Lower panel (`cal-p2/`): box 805 2960 2300 3580, x 0..250 step 50, y -100,0,100, bands 12,
   min-frac 0.5, snap 6, frame-frac 0.5, dark 128. 18 anchors; x rms 0.31 thou (max 0.43), y rms
   0.28 thou (max 0.45; 0.14 percent of the 200 span). With the default dark threshold the tool
   mistook the stack of markers at x=0 (u 847) and at x=100 for the x=0 and x=100 lines; dark
   128 cured it (all 9 lines in 12/12 bands).
3. Eye checks are in `calibration-eye-checks.csv` (crops in `eyechecks/`, zoom 6, 5 px grid):
   three labels per axis per panel agree with the fit within 3 px (0.5 thou or 6 psf). The one
   larger difference is the upper frame line: the fit extrapolated to 6000 gives v 1079 at u
   1909 where the frame is at v 1087 (8 px, 27 psf, 0.45 percent of the span). The gridline pitch
   (291 px per 1000 psf) predicts 1081, so the frame is drawn about 6 px below where a 6000
   gridline would be. Nothing was read above 5600 psf.
4. The scan is tilted: vertical lines drift +0.011 px per px of v (about 0.65 degrees), so the
   x=0 line is at u 802 near the top of the upper panel and u 827 in the lower panel.

## 2. Method

1. Markers. Zoom-3 tiles of both panels (`crops/`) were read first to inventory every symbol
   per series; the dense left end of the lower panel was read on zoom 6 and 7 crops
   (`crops/p2_zoomA..C.png`). Centers were then refined with `find_markers.py`: a template of
   each symbol is cut from one clean marker on this page (listed in the script; the template
   origin is the bbox center of that marker) and the center is the position where the fraction
   of template ink lying on page ink is highest (plateau centroid). This score ignores extra
   ink, so a dash or gridline through a marker does not pull the center. Every refined center
   was checked by eye on contact sheets (`sheets/p?_NN.png`, zoom 4, crosshair plus the bound
   box); none needed moving. Marker bounds: 2 px for a clean marker, 3 px in the direction of
   a gridline or an overlapping symbol.
2. Traces (upper panel only, there are no drawn lines in the lower panel). `trace_sampler.py`
   samples columns every 14 px (2.4 thou) from the second marker to the last, moving a column by
   up to 18 px when it falls on a vertical gridline, on a marker, or in a gap of the dashed line;
   the dark run nearest the v interpolated between neighbouring markers is taken (runs under
   7 px thick are ignored: the horizontal gridlines are 5 to 7 px, the curves 12 to 15 px).
   The steep first segment (first to second marker) is sampled along rows every 14 px instead,
   where the horizontal run is short. Bounds: half the run thickness across the line, 2 px
   along the sampling direction. A run whose extent reaches a horizontal gridline is noted
   ("run touches the N psf gridline") with the v bound at least 5 px, because the gridline ink
   may be inside the run (33 samples; mostly n3815 and n1761 approaching the 4000 and 2000 lines
   at the right end, n734 at the 1000 line near x=150). Samples closer than 20 px to a marker
   center were accepted only if the run was no thicker than the series' median plus 5 px.
3. Features: first point (the drawn line begins at the first marker in every series, checked on
   the tiles), the peak of the drawn line, the last point (the line ends at the last marker on
   the x=250 gridline; the rightmost ink is 4 to 40 px further right where the line runs into the
   legend symbol). The peak was read on a 2 px column scan: the curves are flat-topped and
   dashed, so the peak is reported as the mean u of all columns within 4 px of the minimum v,
   with the u bound spanning that region (large: 37 to 150 px, i.e. 7 to 26 thou) and v the
   median there. The peak heights are well defined; the peak displacements are not.

## 3. Ambiguities and things a later reader should know

1. **Trace sampling has gaps at every marker.** The drawn line is dashed and is interrupted
   around each marker (white space of roughly 10 px on either side), so no line ink exists
   within about 16 px of a marker center. Consecutive trace samples are therefore up to 7.7 to
   9.4 thou apart at marker columns (5 to 10 such gaps per series); everywhere else they are
   2.4 to 4.8 thou apart. The marker itself gives the line's position in each gap. No value was
   interpolated; columns with no ink were dropped (listed by the script).
2. **Upper and lower panel markers are not at the same displacements.** Upper panel markers
   of all five series fall near x = 8 to 10, 28.5, 48, 67.5, 87, 107.5, 127.5, 147.5, 167, 197,
   221, 249 thou; lower panel markers fall on 0 (or 5), 20, 40, 60, ..., 200, 220, 250 for the
   plus, circle and square, and on 0, 30, 50, 70, ..., 170, 189, 220, 249 for the triangles.
   The x calibrations of the two panels agree with each other and with the eye checks, so this
   is in the drawing, not in the reading.
3. **Marker counts differ by series and panel.** Upper panel: 12 markers for plus, circle,
   triangle-down, triangle-up; 11 for the square (no square between x = 108 and x = 147, the
   dash runs through). Lower panel: plus 13, circle 14, triangle-down 12, square 13, triangle-up
   12. The circle series has lower-panel points at x = 0, 10 and 20 (the others have 0 or 5, then
   20 or 30) and at both 225 and 245 (others have 220 and 250). The two extra circles at 225 and
   245 are clean, unambiguous circles.
4. **The lower panel's x = 0 stack.** On the left frame line (x=0) sit, top to bottom, a
   triangle-up (y -8), a circle (-17) and a plus (-27), touching each other. The square (x 5.3,
   y -9) and the triangle-down (x 4.4, y -18) of the same group are drawn a few px to the right,
   touching each other. The first markers of the upper panel are at x 8 to 10 for all series.
5. **Circle-plus overlaps in the lower panel.** From x = 20 to x = 200 the circle (n3815) sits
   directly above the plus (n4695) and they share ink (the pair looks like a female sign).
   Both centers are read with v bound 3 px. At x = 220 the plus sits under the triangle-down.
6. **Markers on gridlines.** Upper: plus 1 on the 4000 line, circle 12 and square 11 on the
   crossings of the x=250 line with the 4000 and 2000 lines, triangle-up 8 on the crossing of
   x=150 and 1000, several on vertical gridlines (noted per row). Lower: everything at x = 50,
   100, 150, 200, 250 sits on a vertical gridline; square 2, triangle-up 2, triangle-down 3 and
   plus 5 sit on the 0 line. Bounds widened to 3 px in the affected direction.
7. **The last marker of each upper-panel series doubles as the legend symbol.** The legend text
   (sigma, gamma) is printed right of the curve ends at x=250, and the symbol at the end of each
   curve is both the last plotted point and the legend key. The lower panel has markers at
   x=250 for all five series, so these are taken as data points, with the note on each row.
8. **Curves merging with gridlines.** n3815 runs into the 4000 gridline from x about 235 to 250
   and n1761 into the 2000 gridline from about 240 to 250; the sampled runs there contain both
   inks (noted, v bound 5 px). n4695 crosses the 5000 line near x = 195 to 200 where its plus
   10 sits just under the line.
9. Plus 5 of n4695 (x 86.6) is almost swallowed by a thick dash; only the ends of its arms show.
   Bound 3 px.
10. The templates' center convention is the bbox center of the symbol's ink; for the triangles
    this is the midpoint between apex and base, not the centroid (2 px lower for a triangle-up,
    higher for a triangle-down). A reader using the centroid would differ by about 2 px in v.
11. Points right of the x=250 gridline or above 5000 psf are extrapolated by the affine map (see
    section 1). The largest such extrapolation is 560 psf above the last fitted line.

## 4. Counts

Upper panel (`points-p1.csv`, 537 rows): markers 59 (12, 12, 12, 11, 12 for n4695, n3815, n2934,
n1761, n734), trace samples 463 (97, 91, 96, 90, 89), features 15 (3 per series).
Lower panel (`points-p2.csv`, 64 rows): markers 13, 14, 12, 13, 12 in the same order; no traces,
no features (no drawn lines).

## 5. Files

`cal-p1/`, `cal-p2/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`,
`eyechecks/*.png`, `points-p1.csv`, `points-p1-native.csv`, `points-p2.csv`,
`points-p2-native.csv`, `overlay-p1.png`, `overlay-p2.png`, `notes.md`. Helpers: `make_crops.sh`
(tiles), `measure_cc.py` (symbol sizes), `find_markers.py` (search, refine, contact sheets),
`markers_list.py` (the marker inventory with notes; writes `markers-p1.csv`, `markers-p2.csv`),
`trace_sampler.py` (traces and features; writes `traces-p1.csv` and assembles `points-p1.csv`),
`search-p1.txt`, `search-p2.txt` (raw template-search candidates, including false positives at
gridline crossings), `crops/`, `sheets/`.
