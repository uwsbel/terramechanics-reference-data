# FC-6B blind reading (Claude), AM-68-1 Vol. II, Fig. C-6B, printed C-18, PDF 132

LSM soil, gamma 71.1 to 73 pcf (Dr .19 to .28). Page image `packet/p0132.png`, 3213 x 4221 px,
300 dpi, unrotated. Upper panel: shear stress tau (psf) vs shear displacement (x 10^-3 in.).
Lower panel: dilation displacement (x 10^-3 in.) vs the same shear displacement, "Same Notation As
Above". Context pages p0115 (Appendix C intro), p0129 (Fig. C-5A), p0131 (Fig. C-6A) were looked
at; nothing from them was used in the reading.

## Series and legend

The legend is the column of values printed against the curve ends (sigma PSF, gamma PCF):
4695/73.0 (triangle-up), 3815/71.1 (square), 2934/71.1 (triangle-down), 1761/71.1 (circle),
734/71.1 (plus). These match `packet/series.csv` (n4695, n3815, n2934, n1761, n734). No misprint.

## Calibration

1. Upper panel: `detect --box 900 895 2140 2130 --x-values 50,100,150,200,250
   --y-values 0,1000,2000,3000,4000 --bands 22 --min-frac 0.45 --snap 6`. All 10 lines detected in
   22/22 bands. RMS residual x 0.555 (0.28 % of the 200 span), max 1.146 (0.57 %); y 8.0 psf
   (0.20 % of 4000), max 11.4 psf (0.28 %).
2. Lower panel: `detect --box 900 2225 2145 3300 --x-values 50,...,250
   --y-values=-300,-250,...,0,50 --bands 20 --min-frac 0.45 --snap 6`. x RMS 0.604 (0.30 %), max
   1.013 (0.51 %). y RMS 0.165 (0.05 % of 350), max 0.54: this small value is partly artificial,
   see item 4 below.
3. The x calibration uses only the labeled gridlines 50 to 250. The left frame is not labeled and
   is not at a uniform-spacing position: the first interval (frame to 50) is about 318 px against
   280 to 295 px for the others. By the 50 to 250 calibration the left frame is at x = -4.7 (upper)
   and -4.3 (lower). It was therefore kept out of the box. The x max residual (about 5 px, at the
   150 gridline, 0.45 to 0.49 % of the span) is an irregularity of the hand-ruled grid (the 150 line
   is drawn about 5 px left of uniform spacing in both panels), not something a box or threshold
   change can remove from an affine map. Same for the upper y lines, spaced 289.5, 295.5, 290.5,
   298.5 px.
4. Lower y: only three horizontal lines are drawn: the top frame (+50), the zero line and the
   bottom frame (-300). They agree with one linear scale to 0.7 units. There are no drawn lines at
   -50 to -250; the tool interpolated them (`predicted`) between the two frame lines, which is
   why the y residual is so small. The printed labels -100 and -200 have only short leaders. The
   leaders of +50, 0 and -300 sit about 11.5 px below their lines; correcting for that, the -200
   label sits 8 px (2.9 units, 0.8 % of the span) and the -100 label 38 px (13 units, 3.7 % of the
   span) above the position the drawn lines give. **The -100 label is misplaced on the page.** The
   calibration follows the drawn lines; a reader who put the -100 label at its printed place would
   read the plus row (n734) about 10 units more negative.
5. Eye checks (`calibration-eye-checks.csv`): every labeled line on both axes of both panels, read
   from zoomed crops and row/column scans (gridline centers, tick marks below the lower frame,
   ticks left of the upper frame). Residuals 0.2 to 5.6 px; all within 0.5 % of the span except the
   two unlined lower-panel labels in item 4. The upper frame top (unlabeled) is at about 4480 psf.

## Markers

1. Every symbol in both panels was read. Approximate centers were read by eye from zoom-3 tiles
   (`crops/t-*.png`), then refined: squares, circles and pluses by a matched filter with a
   synthetic symbol template (`match.py`), triangles from their apex, base and side edges
   (`trigeom.py`), and every center checked by eye on contact sheets (`sheets/chk-*.png`,
   `sheets/tri-*.png`, crosshair on the zoomed symbol); a few were corrected by hand.
2. Triangle convention: the center is the centroid of the outline (base minus H/3, H the outer
   height of about 29 to 31 px; for an equilateral outline it is also the center of the inscribed
   and circumscribed circles, where a template's center marks sit). The bounding-box center lies
   H/6, about 5 px, toward the apex. Because the drafting convention is not known, triangles carry
   a 3 px v bound (4 px where the symbol is also obscured). The matched filter put triangle-up
   centers about 1.5 px high, so it was not used for triangles.
3. Clean markers: bound 2 px. Wider (3 px in u and/or 4 px in v) where a symbol sits on a
   gridline or on the frame, or a drawn line runs into it; each such marker has a note.
4. Counts. Upper panel: n4695 11, n3815 12, n2934 12, n1761 12, n734 12. **n4695 has no symbol near
   x = 180**, where every other series has one (checked on the page: only the drawn line and
   stray dashes there). Lower panel: n734 13, n1761 13, n2934 13, n4695 13, **n3815 0: there is no
   square anywhere in the lower panel**; the dilation of the 3815 psf test is not plotted on this
   sheet.
5. Upper and lower x positions differ for the same test, and the lower panel has 13 columns of
   symbols against 12 in the upper. Upper-panel symbols sit at x of about 6 to 8, 26 to 27, 46 to
   48, 66 to 67, 85 to 87, 116 to 117, 137 to 138, 156 to 158, 176 to 178 (absent for n4695), 197
   to 200, 217 to 218, 246 to 248. Lower-panel symbols sit at about -4 (on the left frame), 7 to
   10, 27 to 31, 48 to 50, 67 to 69, 87 to 90, 108 to 110, 127 to 130, 148 to 149, 166 to 170, 187
   to 189, 217 to 220, 250. The first lower-panel column is drawn on the left frame and reads
   x = -3.7 to -4.3 with the 50 to 250 calibration; it is probably meant as x = 0 (frame drawn as
   the zero line with a wide first interval), but the reading is left as measured.
6. Markers on gridlines or the frame (wider bound, noted): upper n4695 #2 (apex on 2000), #5 (3000
   line through it), #11 (near 250); n3815 #10 (200), #12 (250); n2934 #3 (near 50), #10 (200), #12
   (250); n1761 #3 (top on 1000), #10 (200); n734 #10 (vertical bar hidden in 200). Lower: the
   first symbol of every row is on the left frame; symbols #4, #9 and #13 of every row are on the
   50, 150 and 250 gridlines.
7. Markers clearly off the drawn line (the lines are author fits, not joins): n3815 #5 at
   (1162, 1354) lies about 25 px below its line; the n734 pluses #5, #6, #8 sit just below the
   line; most symbols touch or straddle their line.
8. Lower panel: no symbols overlap. The triangle-down and triangle-up rows are about 60 px apart
   and every symbol was identified; none needed a wide unidentified bound.

## Traces (upper panel only; the lower panel has no drawn lines)

1. The drawn lines are heavy dashes interrupted around every symbol. A dense per-column track of
   each line (`track.py`, two passes: a guide through the markers with a 22 px window and runs at
   least 6 px thick, then a running-median guide with an 8 px window) found the line's run in every
   column; columns inside a symbol box, within 8 px of a vertical gridline, or with a partial run
   (under 70 % of the local line thickness: scan dropouts, tapered dash ends) are not used.
2. Samples (`sample.py`): 3 px inside each end of every dash and at most 24 px (4.2 thousandths)
   apart inside a dash; v is the run center (mean over three columns), v_bound half the run's
   vertical thickness (5 to 10 px; up to 20 px in the steep shared band), u_bound 1 px. Drawing
   order = increasing u (no curve doubles back).
3. Intervals wider than 5 thousandths exist only where the line is interrupted around a symbol of
   its own series (sometimes together with a vertical gridline): 6.3 to 9.9 thousandths. No samples
   were put in those white gaps or on the symbols. Every other interval is at most 4.4 thousandths.
4. Line crossing a horizontal gridline at a shallow angle (merged ink): the center was taken from
   the run's free edge (top + tl/2 or bottom - tl/2, tl the line's own vertical thickness nearby),
   bound tl/2 + 2, with a note. Samples: n4695 at u 1138 (3000), 1702, 1720, 1739 (4000); n3815 at
   875, 888 (2000, read by hand), 1361, 1380, 1399 (3000); n2934 at 752 (1000), 1213, 1234 (2000);
   n1761 at 969, 991 (1000).
5. **Shared ink n4695/n3815.** From the upper-right corner of the first n3815 square (u 716,
   v 1717) up to u 797 the two lines are drawn on top of each other: one band about twice the line
   width (vertical run 24 to 42 px). The band samples (u 724 to 794) are recorded for both series
   at the band center with v_bound half the band, noted. At u 800 they separate: n4695 continues
   steeply up the left side of the second n3815 square to its second triangle, n3815 runs into the
   lower-left corner of its second square (hand samples at u 803 for both).
6. **Start of n4695.** The n4695 line leaves the apex of its first triangle (706, 1783) as a short
   stroke, crosses the lower-right corner of the first n3815 square (704, 1739) and emerges from
   that square's upper-right corner into the shared band. The first trace sample is the stroke
   between the two symbols, (708.5, 1762), bound 6 px; the part inside the square is not sampled.
7. First and last samples are where the line's ink starts and ends, not on the end symbols: n2934
   starts at the upper-right corner of its first triangle (730), n1761 just right of its first
   circle (726), n734 against the right arm of its first plus (726). All lines end against their
   last symbol (u 2059 to 2068), which sits next to the 250 gridline; no line continues past it.
8. Features per series: first point, peak, last point (sequence 1, 2, 3; role in the note). Peaks
   are the minimum v of the dense clean track smoothed over 11 columns: n4695 flat top u 2013 to
   2043 (about 4236 psf); n3815 flat top u 2030 to 2064 (about 3750 psf); n2934 rises to its end, so
   peak = end (u 2059 to 2068, about 2921 psf); n1761 flat from u 1999 to 2069 (about 1625 psf);
   n734 flat (within 1 px) from u 967 to 1558 (x about 53 to 155, about 419 psf), then falls to
   about 348 psf at its end. For flat tops the peak u is the middle of the flat part and its u
   bound spans it, since x is not an observation there.
9. n734 has a scan dropout at u 1108 to 1110 (only the upper half of the line is inked); those
   columns were excluded.

## Stray ink (not read as data)

1. Short thin dashes (1 to 4 px thick) beside many symbols in both panels, mostly just below and
   right of a symbol or below a drawn line (for example u 1477 to 1508 below n4695, u 2000 to 2077
   below n3815, u 1630 to 1745 at v 1126). They look like drafting guide marks or show-through and
   are never thick enough to be a drawn line.
2. A straight horizontal line at v 1293 from u 1880 to 2103 (y about 2760 psf) below the n2934
   curve; a thin dotted line at v 1999 from u 1713 to 1830 below the n734 curve; a short dash at
   (680, 1897) inside the frame; a tick at v 1387 left of the upper frame (not at any labeled
   value). None belongs to a series.

## Files

`cal-p1/`, `cal-p2/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`,
`points-p2.csv`, `points-p2-native.csv`, `overlay-p1.png`, `overlay-p2.png`, this file. Helper
scripts: `eyecheck.py` (eye-check table), `rowscan.py` (row scans), `sheet.py` and `check.py`
(contact sheets), `match.py` (matched filter), `trigeom.py` and `extents.py` (triangle geometry),
`markers.py` (all marker readings, writes `markers.csv`), `track.py`, `smooth.py`, `segs.py`,
`sample.py` (trace tracking and sampling), `build_points.py` (assembles the points files, holds
the hand readings), `zoomov.py` (overlay zooms). Working material: `approx.csv`, `matched.csv`,
`tri.csv`, `tracks/`, `guides/`, `samples/`, `crops/`, `sheets/`.
