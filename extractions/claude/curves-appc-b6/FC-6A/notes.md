# FC-6A, Claude reading (batch curves-appc-b6), panel 1

Figure C-6A, "Failure Envelopes - Maximum Shear Stress vs. Normal Stress", printed page C-17,
`packet/p0131.png`. LSM soil, three density groups, axes sigma (psf) 0 to 5000 and tau (psf) 0 to 6000,
upright, with full grid lines every 1000 psf.

This reading restarts an interrupted one by the same side. Its calibration (`cal-p1/`, written by
`helpers/calibrate_fc6a.py`) was re-run, reproduced bit for bit, and checked against the page before use.
Everything else (points, traces, overlay, these notes) was read anew. `cal-try1/` and `cal-try2/` are
the earlier reader's trial calibrations (tool default with y = 5000 predicted; 10 bands) and are not used.

## Calibration (`cal-p1/calibration.json`, 42 anchors)

1. Box 895 1215 2425 3025, grid values x 0..5000, y 0..6000 step 1000. All six vertical lines and six of
   the seven horizontal lines are detected by `tools/calibrate_axes.py` (imported unmodified). The
   tau = 5000 line is hidden behind the legend box over most of its length; the tool would interpolate it
   (`predicted`, 5 px below the drawn line at the left). The helper measures it instead on its two visible
   segments (the stub left of the frame, u 900 to 965, and the segment right of the legend, u 2195 to
   2378; 236 columns, rms 0.54 px) and uses that fitted line as a measured line. Both segments were
   checked on zoomed crops (`crops2/yl_top.png`, `crops2/y5000_right.png`).
2. Affine fit residuals: x rms 3.40 psf, max 7.34 psf; y rms 6.09 psf, max 12.16 psf (0.07 and 0.10
   percent of the spans; limit 0.5 percent).
3. The largest y residuals are on the tau = 5000 and 6000 lines (+6 to +12 and -10 to -12 psf): the
   top grid interval is 288 px tall against 293 to 296 px for the others, on both sides of the plot. In
   the data region (tau up to 4730 psf) the residuals are within +-6 psf except toward the top right,
   where they approach +10 psf near tau = 4700.
4. By-eye label checks (`calibration-eye-checks.csv`): all five sigma labels (1000 to 5000) and all six
   tau labels (1000 to 6000) sit on the grid line or frame line they name, within 7 px (lines are 290 to
   296 px apart). The 5000 and 6000 tau labels and the 5000 sigma label name the measured y = 5000 line,
   the top frame and the right frame.

## The drawn lines and which series each one carries

No friction-angle label is printed anywhere on this figure (plot area, margins and legend searched on
crops). No `label:` feature is written. The lines are therefore identified by the reader, not by the page:

| line | drawn as | assigned series | fit to its ink (pixels to psf through cal-p1) |
|---|---|---|---|
| A (top at the right end) | solid from the origin corner to sigma ~4860 | dr5-40 (triangles) | tau = -14 + 0.9745 sigma, phi 44.26 deg |
| M (middle at the right end) | dashed from below the tau = 0 axis to sigma ~850, solid to sigma ~4550 | dr19-28 (circles) | tau = -151 + 0.9866 sigma, phi 44.61 deg (solid part) |
| B (bottom at the right end) | dashed from the tau = 0 axis to sigma ~830, solid to sigma ~4570 | dr103-107 (squares) | tau = -40.5 + 0.8989 sigma, phi 41.95 deg |

The angles are the reader's fits to the drawn ink (rms 0.7 to 0.9 px), not printed values.

Evidence for the assignment:

1. Line A is interrupted exactly where it meets triangles: at the origin triangle T0, beside the
   sigma ~1760 cluster (gap u 1394 to 1440), at T2 (gap u 1736 to 1779, A passes through its apex) and at
   T3 (gap u 2005 to 2047, A passes through its centroid).
2. Least-squares lines through each group's five markers: triangles phi 45.2 deg, c = -126 psf; circles
   phi 44.9 deg, c = -174 psf; squares phi 39.9 deg, c = +136 psf. Rms tau offset of each group from each
   line: triangles A 92, M 109, B 267 psf; circles A 175, M 143, B 243 psf; squares A 377, M 333, B 239 psf.
   The assignment above is the best of the six permutations (sum 474 psf; the next, M to triangles and A
   to circles, 523 psf). The margin between A and M for the circles is not large.
3. A circle printed outside the frame (marker Cx) sits at the height where the dashed extension of M meets
   sigma = 0 (within about 2 px), which reads as an identity or intercept mark for M.
4. The data sheets of these tests (FC-6B to FC-6D) would settle it (rule 9) but are not in the packet.

Finding worth checking against the data sheets: under this assignment the densest group (Dr 1.03 to
1.07) has the lowest drawn angle (41.95 deg), below the two loose groups (44.26 and 44.61 deg), and the
circle group's line has a negative intercept of about -150 psf. The markers scatter widely about all
three lines (rms 92 to 239 psf).

### Line details

1. A runs into the frame corner at the origin (intercept tau ~ -14 psf at sigma = 0, i.e. zero within
   3 px); its ink merges with the frame there. The top end has a thin neck at u ~2320 (a 1 to 2 px
   connection) and is read as solid to its end at u 2345.
2. M: its dashes lie about 2 px below the line fitted to its solid part. The lowest dash crosses the
   sigma = 0 axis below the frame at tau ~ -156 psf (measured on the dash centerline; the solid part
   extrapolated gives -151) and its ink continues to u 926 (sigma ~ -30). Gaps in the solid part: u 1437
   to 1464 (the sigma ~1760 cluster), u 1806 to 1818 (just right of the sigma = 3000 grid line; nothing
   drawn there), u 2065 to 2073 (beside T3's base corner).
3. B: the lowest dash runs into the tau = 0 frame line at sigma ~40, merged with line A and the frame,
   about 12 px short of the sigma = 0 axis; it does not reach sigma = 0. Its intercept feature (tau ~ -40
   psf) is extrapolated on the fitted line and has no ink under it. Gaps in the solid part: u 1328 to 1330
   (a tiny ink loop sitting on the line at (1332, 2655), smaller than any symbol, not a marker), u 1425 to
   1428 (T1 base corner), u 1970 to 1987 (nothing drawn there). B ends 12 px left of square S4.
4. M and B cross at about (1300, 2683) px, sigma ~1257, tau ~1090 psf, and their inks are merged from
   sigma ~850 to ~1700; trace samples there are on the fitted positions over the merged ink (noted per
   sample).

## Markers (15 inside the frame, plus one outside)

Legend as printed: triangle gamma 66.8 to 75.2 (Dr .05 to .40), circle gamma 71.1 to 73 (Dr .19 to .28),
square gamma 91 to 93.3 (Dr 1.03 to 1.07); matches `series.csv`. All symbols are open.

1. Triangles T0 to T4 (sigma ~142, 1763, 2871, 3778, 4587 psf): centroids of the reconstructed
   triangles (base about 40 px, height about 34 px), bounds u 3, v 6 px (rule 8). T0 is at the origin
   corner on lines A and B; T1 is under circle C1 (its apex lies inside the ring) and its base-left corner
   is hidden by line B, so it is reconstructed from the left side at v 2540 and the right side; T4's right
   side is faint below v 1645 and its base-right corner merges with line A.
2. Circles C0 to C4 (sigma ~730, 1742, 2925, 3820, 4664 psf), bounds 2 to 3 px.
3. Squares S0 to S4 (sigma ~741, 1740, 2931, 3800, 4665 psf), bounds 2 to 2.5 px. S2's top edge merges
   with the tau = 3000 grid line; S3's left side coincides with the dashed reference line.
4. Rule 9 (shape against line), series given by shape in every case: T1 sits on line B (3 px) and next
   to M; T2's centroid sits on line M (3 px), 27 px below A; C2 sits on line A (13 px); C3 and S0 are
   nearest to line A (21 and 24 px).
5. Cx, a circle printed outside the plot frame below-left of the origin, at about (-145, -162) psf. Same
   size and shape as the circle symbols. Recorded as a `dr19-28` marker by shape only, with a note: it
   cannot be a test (negative normal stress) and is most likely a mark for line M's intercept.

## Reference lines 3680 and 3820

A dashed horizontal line labelled 3680 (right of the frame) and a dashed vertical line labelled 3820
(below the sigma axis) meet at triangle T3. The horizontal line is drawn at tau ~3671 psf (printed 3680,
agrees within 3 px). The vertical line is drawn at sigma ~3744 to 3752 psf along its length (affine map;
direct interpolation between the 3000 and 4000 grid lines gives 3745 to 3754), and T3's centroid reads
sigma ~3778: the printed 3820 is 45 to 75 psf (13 to 22 px) to the right of where the line is drawn. The
ratio of the printed values gives 43.9 deg; the drawn line A gives 44.26 deg.

## Trace samples

Every 250 psf of sigma from each line's left end to its right end, v measured on a clean single stroke
or the fitted v on merged ink (noted), u bound 0 and v bound 7 px (half the line's vertical thickness of
13 to 15 px); end samples bound 4 to 5 px. Left out because the line passes over a plotted symbol
(rule 7): A at sigma 3750 (T3), M and B at sigma 1750 (the T1 and C1 cluster). Moved along the line:
A at sigma 750 by -2 px (the run at the nominal column touches square S0's bottom edge) and A at sigma
1750 by +1 px (A's segment starts at u 1441).

## Not data

Short thin horizontal tick marks near several symbols and along the vertical reference line (for
example below C0 at v ~2907 and at v ~2950 between u 1060 and 1150), and a dotted segment at v ~1641
from the legend's right edge to triangle T4. They look like typing or reproduction marks and are not read.

## Files

1. `cal-p1/` (calibration.json, anchors.csv), `calibration-eye-checks.csv`.
2. `points-p1.csv`, `points-p1-native.csv` (77 rows: 16 markers, one of them outside the frame, 58 trace samples, 3 intercept features).
3. `overlay-p1.png` (plot area, red dr5-40, green dr19-28, blue dr103-107).
4. `helpers/`: calibrate_fc6a.py (calibration), fit_lines.py (line fits), build_points.py (points),
   eye_checks.py, and the reading aids ascii.py, rowruns.py, colscan.py, along.py, dash_centers.py,
   hough_lines.py, hough2.py, line_extents.py. `crops2/` holds this reader's crops; `crops/` the earlier
   reader's.
