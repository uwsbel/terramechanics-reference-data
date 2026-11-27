# F2-44, panel 1: notes of the Claude reading (batch curves-s2-b3)

Figure 2-44, printed page 2-79, PDF page 104 (`packet/p0104.png`, 3213 by 4508 px, unrotated).
Load on a four-inch cylinder (lb) against penetration (in), RS dense soil, bins of three sizes.
Pixel coordinates (u right, v down) refer to `p0104.png`.

## 1. What the page prints

1. Key box (top, over the middle of the 2000 lb frame line): "A 18 Inch by 36 Inch Bin", "B 36 Inch
   by 36 Inch Bin", "C 54 Inch by 36 Inch Bin", "(117) Gp values in parentheses".
2. Labels along the lines: "A LPT No. 73 (117)" along a dashed line (about 1.4 to 2.3 in);
   "C LPT No. 69 (103)" along a solid line (about 2.3 to 3.3 in); "C LPT No. 64A (112)" along a
   solid line (about 2.4 to 3.6 in).
3. Labels below the curves with an arrow: "B LPT No. 74 (103)", arrow tip at about (1088, 2690) on
   the dotted line near its minimum; "A LPT No. 24 (83)", arrow tip at about (870, 2735) on a
   dashed line at about 0.41 in, 670 lb.
4. Axis titles "Load (Lb.)" and "Penetration (In.)"; load labels 0, 500, 1000, 1500, 2000;
   penetration labels 0 to 5.
5. Everything above agrees with `series.csv` and `figures-rows.csv` (ids, letters, Gp values,
   units). The task's description also agrees with the page: two traces are solid (69 and 64A,
   both bin C), two are dashed (73 and 24, both bin A), one is dotted (74, bin B). No plotted
   symbols (markers) on this figure.

## 2. Calibration (`cal-p1/`)

1. `calibrate_axes.py detect` on the full frame took the bottom edge of the key box (v 1750) for
   the 2000 lb line (y residual 19.8 lb rms, 31.5 lb max): the key box bottom is a long straight
   line 47 px below the frame and covers the middle three of the five bands. That run was discarded.
2. Final map: `detect` on a box below the key box (725 1790 2300 3270; out/F2-44/cal-detect-lower)
   for x = 0 to 5 and y = 0 to 1500, all 10 lines detected in 5 of 5 bands. The 2000 lb frame line
   was then measured by `cal_helper.py` only on the parts that show (u 752 to 1036 left of the key
   box and u 1980 to 2276 right of it, 144 of 147 columns, line centre of a 12 px frame line, rms
   0.54 px about one straight line; the left and right parts alone agree within 0.5 px at mid-span).
   It is anchored at its crossings with x = 0, 1, 4 and 5 only; x = 2 and 3 cross it under the key
   box and are not anchors.
3. Affine residuals on the 28 anchors: x 0.0020 in rms, 0.0043 in max (0.09 percent of 5 in);
   y 1.66 lb rms, 3.07 lb max (0.15 percent of 2000 lb).
4. Piecewise map (D-025): all 6 x lines and all 5 y lines pass the ink check (`cal-p1/knots.json`,
   written by `knot_check.py` with the tool's own check). Location errors 0.64 to 1.39 px. The
   2000 lb line: ink found at 8 of 9 positions; two of the three check positions under the key box
   found key-box lettering, one of them set aside as an outlier, the other within 1 px; the six
   positions on the visible parts carry the fit. All 151 points are inside the verified lines (no
   extrapolation). Piecewise and affine values differ by at most 0.003 in and 2.4 lb.
5. By-eye label checks (`calibration-eye-checks.csv`, all labels, crops `crops/ylabels.png` and
   `crops/xlabels.png`): each load label sits 4 to 9 px above the centre of its own line, the label
   spacing (387 to 392 px) matches the line spacing (387 to 390 px), so no label is shifted by a
   line; the 2000 label sits beside the top frame line, the 0 label beside the bottom frame. Each
   penetration label is centred within 8 px of its line under the bottom frame; 0 and 5 are the
   left and right frame lines. The frame does not extend past the first or last labeled line.

## 3. Which line is which, and how they were told apart

1. **74 (B, dotted)**: the only dotted line, so its identity is never in doubt where its dots
   show. The arrow from "B LPT No. 74" ends on it at its minimum (1.04 in, 727 lb).
2. **69 and 64A (C, both solid)**: the label "C LPT No. 69 (103)" is printed along the upper solid
   line between 2.3 and 3.3 in; "C LPT No. 64A (112)" along the steeper lower solid line between
   2.4 and 3.6 in. Followed back to the start by continuity: from about 0.3 in to 3.9 in the two
   solid lines never touch; 69 stays above 64A through both peaks and both descents (near 1.25 in,
   69 at 975 lb, 64A at 908 lb). So 69 is the solid line with the higher peak (1217 lb at 0.71 in)
   and the sharp minimum at 1.54 in (872 lb); 64A is the one with the lower peak (1120 lb at
   0.70 in) and the rounded minimum at 1.91 in (657 lb). They cross once, at about 3.94 in and
   1580 lb, pixel (1955, 2022): 64A comes in straight at about 55 degrees and leaves at the same slope to its end at
   4.34 in; 69 comes in at about 20 degrees and leaves at about 20 degrees, then bends upward to
   its end at 4.69 in. Slope continuity through the crossing decides it.
3. **73 and 24 (A, both dashed, same dash pattern: period about 63 px, dash about 48 px)**: the
   label "A LPT No. 73 (117)" is printed along the steep dashed line from about 1.4 to 2.3 in. Its
   dashes were followed down by direction to a V-shaped minimum at 1.03 in (798 lb) and on to a
   flat top at 0.43 to 0.60 in (881 lb), which joins the right edge of the solid line of the
   initial rise. The arrow of "A LPT No. 24 (83)" ends on the other dashed line at 0.41 in, the
   line that rises more slowly, clear of the bundle, between about 320 and 830 lb. 24 was followed
   to its flat top at 0.88 in (910 lb), down to 1.50 in (860 lb), where it turns up into the
   underside of 69, and on as the dashed line between 69 and 74 after 2.05 in, to its last short
   dash on the 3 in grid line (3.02 in, 1335 lb). The two dashed lines cross once, at about
   0.69 in, 865 lb, where 24 rises through 73's descending flat top (dash directions continuous).
4. The three solid-line and dashed-line traces of the initial rise were told apart by position in
   the bundle where possible (see section 5); where they coincide no identity is claimed.

## 4. Crossings (approximate, from the page)

1. 73 and 24: about 0.69 in, 865 lb, pixel (955, 2582).
2. 64A with 73 and 24 together: about 1.27 in, 886 lb, pixel (1135, 2565).
3. 73 and 69: about 1.38 in, 929 lb, pixel (1168, 2532).
4. 74 and 64A: about 1.39 in, 797 lb, pixel (1171, 2634).
5. 24 and 74 join the underside of 69 from about 1.53 in (873 lb) to 2.05 in (982 lb); 24 lies
   between 69 and 74 when they separate.
6. 69 and 64A at about 3.94 in, 1580 lb, pixel (1955, 2022); 74 crosses 64A at about 3.8 in and 69 at
   about 3.95 in, all within 1550 to 1620 lb; 74 passes under 64A and then
   under 69 between about 3.70 and 4.06 in.

## 5. Ambiguities and how they are bounded

1. **Starts.** All five traces begin in one blob of ink against the left frame (u 752 to 781,
   v 3092 to 3145, about 140 to 210 lb, 0.02 to 0.11 in). The shared solid line runs into the
   frame at about v 3092; one dash piece (u 765 to 778, v 3101 to 3130) belongs to 73 or 24. The
   `first` rows of 69, 64A and 74 are placed on the solid line's end with a bound of 8 by 25 px;
   those of 73 and 24 on the dash piece with 9 by 16 px. None of the traces starts at the origin.
2. **Initial rise, below about 760 lb (0.27 in).** Only one solid line about 9 px wide is drawn,
   with 73's dashes overlapping its right edge (the run is 8 to 9 px wide in every dash gap). 69,
   64A and 74 are therefore drawn on one line there: the solid line shows no second edge and no
   dot of 74. Their samples are identical, on the solid line's centre (left edge of the run plus
   4 px), bound widened to 6 px, and the note says so. 73's samples are at the right edge of the
   run minus 4 px, bound 6 by 8 px. 24 is a separate dashed line about 20 px to the right from
   about 320 lb up; below that it merges with 73 and the solid line, and its 300 lb sample sits on
   the end of its last separate dash, its 200 lb sample on the unattributed dash piece.
3. **750 to 950 lb (0.27 to 0.37 in).** 64A separates from 69 (side by side at 900 lb, 12 px
   apart; separate above 920 lb). 74 leaves the bundle at about 0.33 in, 847 lb; 73 at about
   0.36 in. The 800 lb samples of 64A and 74 are placed 4 px right of 69 inside a 24 px band with
   widened bounds.
4. **1.55 to 2.05 in.** 24 and 74 run along the underside of 69 as one band up to 22 px tall; the
   dots and dashes are not separable there. The 1.75 in samples are at the top of the band (69),
   inside it (24, bound 10 px in v) and at its bottom (74, bound 9 px in v); the 2.0 in samples of
   24 and 74 are on the protrusion where they leave the band, partly merged.
5. **24's minimum** (`knee`, 1.50 in): its last dash before 69 ends at (1205, 2587); the turn
   upward is hidden under 69's ink; recorded on the end of that dash with a 10 px bound in u.
6. **73's minimum** (`knee`): the bottom of the V (about u 1068) falls in a dash gap; recorded on
   the last ink before the gap, (1060, 2632.5), bound 8 px in u.
7. **74 between 3.70 and 4.06 in** is hidden under 64A and 69; two partly visible dots are sampled
   (3.69 in on the left side of 64A, 3.90 in below the crossing) with notes; the 4.0 in sample is
   the first clear dot after the crossing (4.06 in).
8. **Peaks on flat tops**: 69 (u 945 to 970, 0.66 to 0.74 in), 64A (u 940 to 975, 0.64 to 0.76 in),
   73 (u 875 to 926, 0.43 to 0.60 in), 24 (u 1010 to 1050, 0.87 to 1.00 in), 74 (dots from u 877 to
   910, 0.44 to 0.54 in). The peak rows carry a wide u bound; their x is not an
   observation.
9. **69's two knees** are gradual bends, not kinks: the slope falls from about 45 to about 30
   degrees between 3.0 and 3.3 in, and rises from about 20 to about 55 degrees between 4.2 and
   4.5 in. They are recorded as `knee` with 15 px bounds and a note; a reading that does not count
   gradual bends as knees will not have them. No other trace has a knee besides its minimum.
10. For every trace the last point carries the highest load, so no separate highest-load `peak`
    rows were needed.
11. **Stray strokes, not sampled**: horizontal stroke under "73 (117)" (u 1455 to 1590, v 2049);
    short stroke right of 73's minimum (u 1070 to 1112, v 2634); strokes near the dots of 74 at
    (1540 to 1580, 2397), (1720 to 1735, 2252) and (2081 to 2098, 1906); small marks right of
    "(112)" at about (1805 to 1840, 2342) and after "64A" at about (1715, 2430).
12. The 2 in and 3 in grid lines are drawn broken in places; they were detected in 5 of 5 bands
    and verified on the ink.

## 6. Sampling and bounds

1. Samples every 0.25 in of penetration and, on the initial rise of each trace up to its first
   maximum, every 100 lb of load; plus the features of rule 3 (`first`, `peak, first maximum`,
   `knee, minimum`, other `knee`, `last`). A trace's first and last trace samples are where its ink
   starts and ends (same pixels as its `first` and `last` features). Drawing order = increasing
   penetration; no trace doubles back.
2. Sampling locations were moved 6 to 10 px off a grid line where they fell on one, and off a
   neighboring trace where a profile across the line would have merged with it; the note says so.
   x of a trace sample is a sampling location, so some samples sit up to 0.06 in from the nominal
   quarter inch (on a dash or a dot instead of a gap).
3. Bounds: solid lines half the measured width across the line (about 4.5 to 6 px); dashed lines
   half the width across and half the dash gap (7.5 px) along the line, projected on u and v;
   dots of 74 at the dot centroid, 5.5 px (dot about 10.5 px across, gap about 7 px). Widened
   wherever traces run together (values given in the rows).
4. Values (`points-p1-native.csv`) come from `calibrate_axes.py piecewise --image`.

## 7. Observation, for whoever uses the data

The page text (PDF 99) says the larger bins tend to give higher loads at failure. On this figure
the two bin C traces peak at 1217 and 1120 lb, but the bin B trace (74) peaks at 857 lb, below both
bin A traces (73 at 881 lb, 24 at 910 lb). This is what the curves show; it is not a reading
ambiguity.

## 8. Files

1. `cal-p1/calibration.json`, `cal-p1/anchors.csv`, `cal-p1/knots.json` (ink check of every line).
2. `cal-detect-lower/` (the `detect` run the map is built on), `cal_helper.py` (2000 lb line and the
   final calibration), `knot_check.py`.
3. `calibration-eye-checks.csv` (`eye_checks.py`).
4. `points-p1.csv` (`build_points.py`, which documents each sample's method), `points-p1-native.csv`.
5. `overlay-p1.png` (tool overlay of the whole frame); zoomed check crops under `crops/`
   (`ov_*.png` drawn by `zoom_overlay.py`).
6. Exploration helpers, not needed to rebuild the points: `snap.py` with `guides.json`, `blobs.py`,
   `dots74.py` (`dots74.json`), `dashes.py`, `perp.py` (used by `build_points.py`).
