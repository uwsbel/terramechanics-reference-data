# FC-2B blind reading (Claude), Appendix C data sheet, PDF page 121, printed C-7

Page image `packet/p0121.png`, 3263 x 4508 px, 300 dpi, unrotated. Six direct shear tests on PS
soil (legend: sigma 4400, 3660, 2935 (see item 1 under Ambiguities), 2200, 1468, 734 psf).
Upper panel: shear stress 0 to 6000 psf (gridlines every 1000) versus shear displacement 0 to 250
thousandths of an inch (gridlines every 50). Lower panel: dilation -100 to +100 thousandths with a
single interior gridline at 0, same x axis.

## Method

1. Calibration with `tools/calibrate_axes.py detect`, 22 bands (upper) and 20 bands (lower),
   `--min-frac 0.75`, `--snap 6`, `--frame-frac 0.4` (upper). The default `min-frac 0.4` locked the
   5000 line onto the text line "gamma = 25.6 to 26.8 ..." (fitted 1444 instead of 1377) and bent
   the 1000 line onto the n734 dots; 0.75 fixed both. The 5000 line is `predicted` (the text
   interrupts it) and was checked against the tick at the left frame (v 1377.5 by eye, 1377.3 fitted).
   The lower panel's x=100 and x=250 lines were pulled by markers at `min-frac 0.4`; at 0.75 all six
   vertical lines are found in 18 to 19 of 20 bands.
2. Eye checks of every gridline label (not just three per axis) are in `calibration-eye-checks.csv`;
   all agree with the fitted positions within 1.5 px.
3. Markers read by eye from zoom-3 tiles of the upper panel (`crops/p1-u*-v*.png`), with zoom-4 to
   zoom-8 crops of every ambiguous spot (`crops/z-*.png`). A template-matching helper
   (`helpers/find_markers.py`, outputs `helpers/cand-p1-*.csv`) was run as a hint for the asterisk
   and filled-dot series only; every center in the points files was read by eye, and the template
   list was used to confirm the dots hidden in the thick n734 line. The lower panel was read from
   zoom-8 column crops (`crops/p2z-*.png`, `crops/p2-top-*.png`) and column scans
   (`tools/plot_grid.py scan`) across the zero line.
4. Triangle centers are bounding-box centers (midpoint of apex and base), not centroids. Circle
   and square centers are hole centers. Asterisk and x centers are the arm crossings.
5. Traces (`helpers/build_points.py`): the drawn upper-panel lines were sampled at columns every
   20 px (3.4 thousandths) avoiding vertical gridlines (within 7 px) and marker centers (within
   11 px); the dark run nearest the marker-to-marker chord was taken, rejecting a thin run that
   sits on a horizontal gridline (the bare gridline, 6 to 7 px thick; the curves are 9 to 11 px).
   The near-vertical starts of n4400 and n3660 (v 2330 to 2475) were sampled by rows instead (note
   "row sample"; there the u bound is half the run width). Bound in v is half the run thickness;
   a run thicker than 16 px is flagged "thick run" (curve merged with a gridline, with another
   curve, or with the steep slope itself near the start) and carries half its thickness as bound.
   Because the lines are dashed and the dash gaps coincide with some marker exclusions, a few
   consecutive samples are 40 to 52 px apart (7 to 9 thousandths): n4400 at u 1556 to 1602,
   1662 to 1714, 1779 to 1822; n3660 at 1668 to 1711, 1776 to 1828, 1896 to 1940; n2995 at 1382 to
   1420, 2022 to 2060; n2200 at 1142 to 1182, 2025 to 2062. The sequence is in drawing order (left
   to right; no curve doubles back).
6. Features: first point (left end of the drawn line, by eye), peak (minimum v of a dense 2 px
   scan of the drawn line; the note gives the plateau extent within 3 px of the peak, the u bound
   is half that plateau width) and last point (right end of the drawn line).

## Calibration residuals

1. Upper panel: 42 anchors; x rms 0.35 thousandths (0.14 percent of the 250 span), max 0.84;
   y rms 4.2 psf (0.07 percent of 6000), max 7.8. Scale 0.1723 thousandths/px, 3.432 psf/px.
2. Lower panel: 18 anchors; x rms 0.38 (0.15 percent), max 0.68; y rms 0.83 thousandths
   (0.42 percent of the 200 span), max 1.4. Scale 0.1724 thousandths/px, 0.3443 thousandths/px.
   The y residual is a property of the printed grid, not of the detection: the zero line is 284.5 px
   below the +100 frame and 296 px above the -100 frame, so no affine map fits all three. The
   affine fit puts y = 0 at v about 3272, 4 px below the drawn zero line (v 3268); values read
   near the zero line therefore come out about +1.5 thousandths relative to the printed zero.
   A later user who cares about the sign of small dilations should re-zero on v 3268.

## Ambiguities and things a later reader should know

1. Legend misprint. The printed legend reads "2935 26.8" (checked at zoom 4,
   `crops/z-legend2935.png`); `packet/series.csv` and the figures index give 2995 psf. The
   series id n2995 from series.csv is used here; the number on the page is 2935.
2. Lower axis label is printed gamma_sigma (the figures index already notes the typo for
   delta_sigma).
3. Symbols at the right frame. Five of the six upper-panel curves run to the right frame
   (x = 250) and a symbol sits on or just beyond the frame at each curve's end: asterisk at
   u 2221 (x about 252), x at 2208, square at 2226 (x about 253), triangle at 2210, filled dot at
   2218. The 1468 curve ends at x about 189 and its legend row has no symbol, which suggests these
   frame symbols are legend keys placed at the curve ends. The lower panel, which has no legend,
   does have data symbols at x = 250 (u about 2205) for four series, so the upper tests did reach
   250. The frame symbols are recorded as markers with a note and an 6 to 8 px u bound; a reviewer
   may decide to exclude them.
4. First points of n4400 and n3660. Both curves start at about 1150 to 1200 psf at x about 10 and
   their first markers coincide (`crops/z-first.png`): a 6-arm asterisk is visible at (823, 2492)
   with the 3660 curve passing through it. The x of n3660 could not be separated; it is recorded
   at (823, 2497) with a 6 px bound and a note. The square of n2995 sits just below at (825, 2520).
5. Hidden or absent markers in the upper panel: n4400 has no marker between u 1334 and 1452
   (x 100 to 121), between 1517 and 1575 is normal, between 1798 and 1973 (x 181 to 212) there is
   none; n3660 none between 1230 and 1400 (x 83 to 112); n2200 none between 1002 and 1109 and
   between 1688 and 1865; n1468 none between 1000 and 1112 and between 1512 and 1687; n2995 none
   between 1402 and 1513, 1513 and 1688, 1688 and 1917. These were checked on zoomed crops and
   are gaps in the plotting, not missed symbols. Two knots in the dashed lines that look like small
   symbols are not recorded: a loop in the n2995 line at (910, 2242) on the 2000 gridline
   (`crops/z-sq2000.png`) and a hook in the n2200 line at (1035, 2372) where it meets the x=50
   gridline (`crops/z-tri1025.png`).
6. Markers on gridlines or the frame (noted in the file): n4400 (1334,1730) x=100, (1452,1670)
   on 4000; n3660 (1053,2093) half hidden by x=50, (1230,1957) on 3000, (1915,1699) x=200; n2995
   (995,2249) on 2000, (1053,2197) x=50, (1343,2023) x=100, (1513,1957) on 3000, (1917,1860)
   x=200; n2200 (1632,2087) x=150; n734 dots at 1453, 1518, 1571, 1681 merged with the 1000
   gridline, (1742,2530) is a weak bump.
7. n734 line and the 1000 gridline. From u about 1480 to 1700 and again from 2100 to the frame the
   solid n734 line runs on or within a few px of the 1000 gridline; trace samples there are the
   merged run (12 to 18 px thick), with bound = half thickness, and their center is biased toward
   the gridline by up to 5 px (about 17 psf). The last point of n734 (2202, 2537.5) is such a merged
   run.
8. n3660 near its peak (x 200 to 240) runs 10 to 15 px below the 4000 gridline with a dash gap at
   u 2068 to 2080; a first pass sampled the gridline there and was corrected by the bare-gridline
   rule. The peak of the drawn line is a flat plateau from u 2024 to 2164 at v 1680 (about 3960
   psf); the curve then drops slightly to about 3930 psf at the frame.
9. Peaks (from the drawn lines, native units from `points-p1-native.csv`): n4400 4580 psf at
   x 229 to 250 (still rising to the frame; plateau 2104 to 2202); n3660 3962 at x 223 (plateau
   2024 to 2164); n2995 3351 at x 225 (plateau 1942 to 2138); n2200 2713 at x 194 (plateau 1884 to
   2028); n1468 1898 at x 162 (plateau 1638 to 1730, then falls to 1821 at x 189 where the line
   ends); n734 1066 at x 227 (plateau 1872 to 2078).
10. Lower panel: a stack of up to six small symbols (10 to 13 px) at each of 25 displacements
    (u 817, 871, 930, 985, 1042, 1104, 1162, 1220, 1276, 1334, 1390, 1450, 1507, 1566, 1626, 1684,
    1740, 1801, 1858, 1912, 1975, 2032, 2091, 2147, 2205). From u 1390 on the shapes can mostly be
    told apart (dot, ring, triangle, square, x, asterisk, in that order from the top everywhere
    they are separable); from 871 to 1334 the stack is a single merged blob 40 to 50 px tall and
    the recorded centers are assigned by vertical order with 5 to 6 px bounds and the note "stack
    of symbols merged". In the merged columns 871 to 1162 only five blobs are discernible; the x of
    n3660 is not recorded there (the lowest blob has asterisk-like legs and is assigned to n4400).
    In columns 1390 to 1566 the x is recorded with a 6 px bound as "not seen separately" between
    the square and the asterisk.
11. Lower panel, not found: at u 817 only one ring (assigned to n1468; a second symbol may be
    merged at its right). Dots (n734) are not found at 1450, 1566, 1684, 1801, 1912, 1975, 2091,
    2205; rings (n1468) not found at 1566, 1975, 2032, 2091, 2147, 2205. Column scans show the zero
    line at normal thickness (5 to 6 px) at most of these columns, so these symbols are either
    exactly on the zero line or not plotted; nothing was guessed. The dots that are found rise
    above zero from u 1334 on (+4 at x 108 to +24 at x 239, affine-calibrated).
12. Lower panel, markers on the frame (u 2203 to 2206, x about 249.5): triangle, square, x,
    asterisk, recorded with 5 px u bounds. Markers on the x=50, 100, 150, 200 gridlines are noted
    in the file.
13. The 1468 upper curve ends at its last circle (1865, 2305); there is no symbol at the frame and
    the drawn line stops there.

## Files

`cal-p1/`, `cal-p2/` (anchors.csv, calibration.json, detect-log.txt for p2),
`calibration-eye-checks.csv`, `points-p1.csv` (522 rows: 105 markers, 399 traces, 18 features),
`points-p1-native.csv`, `points-p2.csv` (125 markers), `points-p2-native.csv`, `overlay-p1.png`,
`overlay-p2.png`, `helpers/build_points.py` (marker readings and trace sampler; rerun it to
regenerate both points files), `helpers/find_markers.py` and `helpers/cand-p1-*.csv` (template
hints only), `crops/` (every crop looked at).
