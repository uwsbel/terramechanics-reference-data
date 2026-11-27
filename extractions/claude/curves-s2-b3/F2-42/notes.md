# F2-42, batch curves-s2-b3: Claude's blind reading (panel 1)

Figure 2-42, printed page 2-77, PDF page 102 (`packet/p0102.png`, 3263 by 4558 px, binary scan).
Load-penetration curves for a four-inch cylinder in dense RS soil at four rates of penetration.
Read from the evidence packet only (page images, `figures-rows.csv`, `series.csv`, `CURVE-READING.md`).

## Files

1. `cal-p1/calibration.json`, `cal-p1/anchors.csv`: calibration (detect, then 2 hidden anchors removed, see below); `cal-p1/knots.json`: the piecewise knots with their ink checks.
2. `calibration-eye-checks.csv`: every printed axis label checked by eye (4 on x, 7 on y), plus the 627 tick and the unlabeled top frame.
3. `points-p1.csv`: the reading (pixels and bounds); `points-p1-native.csv`: the same rows with `x_native` (in), `y_native` (lb), read bounds and `cal_model` from `tools/calibrate_axes.py piecewise --image`.
4. `overlay-p1.png`: `tools/plot_grid.py overlay` of all points over the page (lpt25 red, lpt23 green, lpt22 blue, lpt24 orange). `overlay-p1-rise-zoom.png`: a zoomed check view of the steep rise (gray ink, small crosses with their bound boxes; lpt22 red, lpt23 green, lpt24 blue, lpt25 orange).
5. Helpers (all under `out/F2-42/`): `build_points.py` (the reading itself: every sample with its method and note; rerun to regenerate `points-p1.csv`), `inklib.py`, `runs.py`, `blobs.py` (dot centroids), `pw.py`, `knots_report.py`, `drop_hidden_anchors.py`, `check_overlay.py`. `crops/` holds the working crops and an affine conversion used only as a diagnostic.

## Calibration

1. `detect` on box (800, 1420, 1800, 3380), x values 0,1,2,3, y values 0 to 1200 every 200, 10 bands, frame fraction 0.3 (the 400 lb line is visible on only 4 of 10 bands). The box top (v 1420) leaves out the top frame (v 1332.5), which is unlabeled and not anchored, as the task requires. All 4 vertical and all 7 horizontal lines were `detected`; none `predicted`. Dropped tracks: v 2536 and 2900 (the key box edges), u 866 (the bundle of traces).
2. The 400 lb line is drawn only from the left frame to the left edge of the key box (u 840 to about 1208). `detect` fitted it on that stretch and extrapolated its tilt to x = 2 and 3 in, under the key, where the line is not drawn; the ink check rejected it there ("misplaced: 5.96 px from the ink's line at an end"). `drop_hidden_anchors.py` removed those two anchors (recorded in `calibration.json` under `anchors_removed`) and refitted the affine map on the remaining 26 anchors. The 400 lb line then passes the ink check on its drawn stretch (3 of 3 positions, offsets 0.42 and -0.23 px). No trace sample lies under the key box.
3. Affine residuals (26 anchors): x RMS 0.0063 in, max 0.0097 in (0.21 and 0.32 percent of the 3 in span); y RMS 0.61 lb, max 1.75 lb (0.05 and 0.15 percent of 1200 lb). All below 0.5 percent.
4. Piecewise map (D-025): 4 x lines and 7 y lines, all verified on the ink (location errors 0.5 to 1.45 px). Values come from the piecewise map. The x grid is drawn unevenly: 311.5, 308.5 and 303 px per inch from left to right, so the affine and piecewise x differ by up to 0.009 in near x = 2 in.
5. Rows beyond the outermost verified lines are flagged by the tool: 4 rows above 1200 lb (D at 2.25 in and its last point, C at 2.75 in and its last point; `extrapolated y`), C's first point (its bound reaches below the 0 lb line's center), and D's and A's first points (`extrapolated x`, their pixel intervals reach past the x = 0 line).
6. By-eye label checks: all 11 printed labels sit next to the line they name, within 2 to 13 px, with the neighboring lines 300 px away; the 0 labels are printed off the frame corner (x label 10.7 px right, y label 12.8 px above). The "3" is under the right frame, so the right frame is the 3 in line. The label 627 has a short tick at v 2381 (it crosses the frame and reaches u 858); by the map it sits at 625 lb, so it marks a value as the task says and is not anchored. The top frame is half a spacing above the 1200 line (it would be 1300 lb) and is not anchored.

## Which line is which

The key prints: A LPT No. 22 (130), gamma 51.2 pcf, rate 4"/min; B LPT No. 23 (99), gamma 50.6 pcf, rate 1"/min; C LPT No. 24 (83), gamma 51.5 pcf, rate 1"/min; D LPT No. 25 (130), gamma 51.6 pcf, rate 2"/min; "(130) - Gp values in parentheses". This agrees with `series.csv`; the ids are kept as given (lpt22 = A, lpt23 = B, lpt24 = C, lpt25 = D).

1. **B (lpt23) is the solid line**: the only continuous line; circled B touches it at its knee (about 0.95 in, 1060 lb).
2. **D (lpt25) is the dashed line with circled D**: the circled D (center about 2.18 in, 1259 lb) stands within about 2 px of one of its dashes, and the line reaches the top frame at 2.5 in.
3. **A (lpt22) is the dotted line and C (lpt24) is the other dashed line.** The two circled letters sit on opposite sides of the pair where the two lines rise together after their minima (about 1.6 to 2.0 in, 880 to 960 lb). Measured on the page, ring ink to line ink:
   - circled A (center 1317.5, 1902): 4.8 px from the dotted line, 38.5 px from the dashed line;
   - circled C (center 1433.5, 1984): 5.4 px from the dashed line, 40.8 px from the dotted line.
   Each circle comes within 5 px of one line and stands clear of the other by about 40 px, on its own line's outer side (A on the upper left of the pair, where the dotted line is; C on the lower right, where the dashed line is), the same placement as circled B and D, which touch or nearly touch their own lines. So A = dotted and C = dashed; there is no leader line and no other reading of the placement that fits. LPT No. 24 (C) is therefore the dashed line that peaks at 903 lb at 0.89 in, dips to 855 lb at 1.53 in and reaches the top frame at 2.91 in.

**Line styles as printed, and a difference from the task's description.** The task calls D "long dashes" and A/C "a dotted line and a short-dashed line". Measured on the page, it is the other way round for the two dashed lines: D's dashes are 45 to 50 px long with gaps of 10 to 15 px (for example rows 2266 to 2314, 2328 to 2374, 2392 to 2438 on the rise; (1053, 1888) to (1076, 1852) higher up), while C's dashes are about 110 px long with gaps of 12 to 13 px (rows 2892 to 3004, 3018 to 3128, 3144 to 3254; (1680, 1430) to (1735, 1338) at the top). So C has the long dashes, more than twice as long as D's. This does not change any identity (D is fixed by its circled letter, A/C by theirs) but whoever wrote "D long dashes" was describing the page wrongly. A's dots are 9 to 10 px across with a pitch of 17 to 18 px; B is 10 to 12 px wide.

## Sampling

1. Drawing order from the first ink at the bottom to the end of each trace; one `sequence` per series for traces and features together.
2. Steep rise: one sample about every 100 lb (rows chosen 8 to 22 px off the 200, 400, 600, 800 and 1000 lb lines so that the sample sits on the trace's own ink, not on a grid line), plus one every 0.25 in of penetration everywhere. Where a 0.25 in column falls on a grid line (1 and 2 in) or in a gap of a dashed or dotted line, the sample is moved to the nearest ink of that trace and the note gives the actual x (for example "x about 1.02"). A's samples are dot centroids (`blobs.py`) or, where a dot touches another line, its free edge minus 4.5 px.
3. Bounds (px): B 5 (half its width); D and C 6 (half the gap along the line, which is larger than half their width); A 5 (half a dot, which is larger than half its gap); 7 where two lines run together and 8 for the first points and the knees. Merged cases are said in each row's note.
4. Markers: none. The figure plots no symbols.

## Crossings and overlaps

1. **The rise (0 to about 0.6 in).** From left to right (that is, from the highest load to the lowest at a given penetration) the order is D, B, A, C, about 10 to 15 px apart, and they touch or merge in many rows. They can be told apart by style row by row: D's 60 px dash period, B's continuity, A's 17 px dot pitch and C's 125 px dash period. Where two run together, the sample uses the free edge of the merged run (`row_left`, `row_right`) and the bound is widened to 7 px.
2. **B and D run together further than the task says**: D is on B's left up to about 800 lb, the two coincide (one run 9 to 12 px wide) from about 0.45 to 0.6 in (840 to 900 lb), and D comes out on B's right at about (1040, 1905), x 0.65 in, 930 lb. They cross again on the plateau at about (1372, 1659), x 1.72 in, 1091 lb, where a dash of D passes from below B to above it.
3. **A and C cross twice and then merge.** On the rise A is on C's left (higher load). From about 790 lb (v 2125, x 0.56) to v 2040 (x 0.68 in, 845 lb) A's dots run on top of C's line, and A comes out on C's right (lower load); first crossing about (1030, 2080), x 0.61 in, 819 lb. Both peak (A 877 lb at 0.96 in, C 903 lb at 0.89 in) and dip (A 844 lb at 1.37 in, C 855 lb at 1.53 in) with A below C. A crosses C again at about (1290, 2022), x 1.45 in, 857 lb (one dot hidden under C), and rises on C's upper left, about 20 to 25 px from it. A then closes on C: from about (1585, 1570), x 2.43 in, 1150 lb, its dots touch C; the dot at (1604, 1541) stands in a gap of C and the dot at (1613, 1525) is a bulge on the lower end of C's next dash. Above it no A dot shows beside C (C's run is 10 to 12 px wide there, where an A dot would make it about 22), and none shows in C's gap at about (1672, 1437). A's last point is put at (1613, 1525), x 2.51 in, 1177 lb; A may run on hidden under C to the frame, which the page cannot show.

## Where the traces start (the main uncertainty of this reading)

The four lines converge into a 25 to 35 px wide bundle against the left frame below about 250 lb. They do not all start at the origin:

1. **C (lpt24)** is followed to the bottom by its dash pattern (gaps at rows 2878 to 2890, 3005 to 3016, 3130 to 3142, 3256 to 3268, a 125 px period). Its last dash runs from v 3270 down into the bottom frame line at u about 859, so C starts at x about 0.05 in, 0 lb, not at the origin. Clear.
2. **A (lpt22)** dots descend between the frame and C: isolated dots at (855, 3252), (853, 3269), (851, 3286), (850, 3304), then one merged with the frame's right edge at about v 3325. A's first point is put at (847, 3324), x 0.01 in, 18 lb, bound 8 px: A reaches the frame just above the origin.
3. **D (lpt25)** dashes reach the frame: dash 3076 to 3127 at u about 855, dash 3143 to 3188 at u about 851 against the frame's right edge, dash 3204 to 3230 half inside the frame. Below about v 3232 no D ink shows outside the frame line (the rows between A's dots, 3260 to 3262, 3276 to 3280, 3292 to 3298 and 3310 to 3314, are clear from u 849 to 860). D's first point is put at (848, 3229), x 0.02 in, 79 lb; below it D is either hidden in the 9 px frame line (x = 0) or was not drawn.
4. **B (lpt23)**, the solid line, is last seen at about (857, 3124), x 0.05 in, **146 lb**, where it ends together with the lower end of a dash of D. Rows 3128 to 3142 hold no ink between u 849 (the frame and its ragged edge) and u 861, and rows 3260 to 3262 hold nothing but the frame line (u 838 to 848), so a solid line cannot continue below v 3127 outside the frame; to be hidden in the frame it would have to jump about 15 px left within 5 rows. B's first point is put at (857, 3124) with bound 8 px. Either B was drawn from about 146 lb, or its start runs inside the frame line from the origin; the page cannot tell which. Anyone using B (LPT 23) below about 150 lb should know this.

## Features read

| series | first | knee | peak, first maximum | knee, minimum | knee | last |
|---|---|---|---|---|---|---|
| lpt22 (A, dotted) | 0.014 in, 18 lb (uncertain) | | 0.962 in, 876.8 lb | 1.369 in, 843.6 lb | | 2.508 in, 1176.9 lb (merges into C) |
| lpt23 (B, solid) | 0.048 in, 146 lb (see above) | 0.948 in, 1061.5 lb | | | 1.663 in, 1086.1 lb (end of plateau) | 2.118 in, 1131.2 lb |
| lpt24 (C, dashed) | 0.053 in, 2.5 lb | | 0.890 in, 903.4 lb | 1.526 in, 855.2 lb | | 2.913 in, 1295.8 lb (top frame) |
| lpt25 (D, dashed) | 0.018 in, 79 lb (uncertain) | 0.737 in, 958.6 lb | | | | 2.505 in, 1295.6 lb (top frame) |

1. Each trace's highest load is its last point, so no extra `peak` rows. B and D have no local maximum: B's plateau is flat within 1 px (1086 lb) from 1.2 to 1.66 in; D rises throughout.
2. Knees are judgment: B's at the middle of its bend into the plateau (the tangents of the steep part and of the plateau meet at about (1098, 1666)), the circled B touching the line there; B's second at the end of the plateau; D's at the point nearest the corner of its two tangents (1044, 1845). D also steepens gradually from about 1.3 to 2.0 in (slope 0.5 to 1.4 px per px); that is a smooth bend, not marked as a knee. A and C bend smoothly into their peaks; no separate knee is marked before the peaks.
3. The two last points at the top frame are where the ink meets the frame's lower edge (v 1338 to 1340), so they read 1296 lb rather than 1300; the frame is 12 px thick.

## Other marks on the page (not samples)

1. A short horizontal stroke at u 937 to 951, v 2622 to 2626 (0.33 in, 469 lb), right of the bundle: belongs to no trace.
2. The 627 tick reaches into the plot to u 858 at v 2381 (0.04 in, 625 lb).
3. A small dot (area 47 px, about 8 by 10 px) at (1320, 2010.5), between A's rising dots and C's trough: off A's dot line and not part of C; not sampled.
4. The circled B touches B's line at its knee (u 1105 to 1137, v 1690 to 1712); the B knee sample is placed outside the ring (it is 50 px from the circle's center, radius about 42).

## Counts

lpt22: 17 trace, 4 feature; lpt23: 17 trace, 4 feature; lpt24: 19 trace, 4 feature; lpt25: 18 trace, 3 feature; 86 rows, no markers.
