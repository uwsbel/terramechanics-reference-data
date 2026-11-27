# FC-7A, Figure C-7A, printed page C-21 (packet/p0135.png), Claude reading

Batch curves-appc-b6. Read blind from the packet only. One panel, upright, linear axes in psi:
"Normal Load - PSI" (x, 0 to 30) and "Shear Load - PSI" (y, 0 to 35). Caption as printed:
"Figure C-7A. Failure Envelopes --Maximum Shear Stress vs. Normal Shear Stress".

## Calibration (cal-p1/)

1. The figure has a full grid every 5 psi in both directions (not ticks only), so the tool's grid
   detection applies: `calibrate_axes.py detect --box 600 920 2600 3200 --x-values 0,5,...,30
   --y-values 0,5,...,35 --bands 20 --dark 160 --min-frac 0.5 --snap 10 --frame-frac 0.35`.
2. All 15 lines are `detected`; 56 anchors. RMS residual 0.022 psi in x (0.07 % of the span) and
   0.030 psi in y (0.09 %); max 0.048 and 0.075 psi. Scale 0.0160 psi/px on both axes; the scan is
   rotated by about 0.7 degrees, which the affine map absorbs.
3. `--frame-frac 0.35`: the y = 30 line is hidden behind the legend over most of its length and is
   found in only 8 of 20 bands (right of the legend), which the default 0.5 would have turned into a
   frame-interpolated `predicted` line. With 0.35 it is fitted on its own ink. Its short left stub
   (u 660 to 845, ink center about v 1285) was checked by hand and agrees with the fitted line within
   2 px (0.03 psi).
4. By-eye label checks (calibration-eye-checks.csv): all 7 x labels and all 8 y labels sit on their
   fitted lines. Offsets are within 7 px except the typed "5" on x (12 px left of its line) and "35"
   on y (15 px below the top frame); both are unambiguous, the next line being about 313 px away.
5. The calibration was first produced by an earlier reader of this figure in this workspace, which
   was interrupted before writing points. It was re-run here from the same command and reproduced
   exactly (identical anchors), then checked against the labels as above. The earlier crops were
   replaced; `helpers/rowscan.py` is that reader's and was not used.

## Legend and series

1. Printed legend: "RSM-b Soil"; circle with a center dot: "gamma = 82 Lb/ft3 (Dr = 0.53)";
   triangle with a center dot: "gamma = 89 Lb/ft3 (Dr = 1.0)". This matches series.csv (dr53, dr100)
   and the figures row. The 0.53 entry has a stray stroke through the "=" sign; it reads 0.53.
2. Both legend symbols carry a center dot, and so does every plotted symbol: symbol vocabulary used
   is `dotted circle` (circle with a center dot) and `dotted triangle` (triangle with a center dot).
3. 6 circles and 6 triangles are plotted. Every symbol matches the legend; no symbol was found whose
   shape disagrees with the line it sits on (rule 9 not triggered).

## Which line carries which angle

1. "50.5°" is printed along the upper line (through the triangles, dr100), centered about 70 px
   below-right of it (u 1724, v 1758.5) and about 230 px from the lower line.
2. "45°" is printed along the lower line (through the circles, dr53), centered about 55 px
   below-right of it (u 1717.5, v 2045).
3. Measured from my trace samples, the upper line is at 50.67 degrees (slope 1.2203, intercept
   2.40 psi) and the lower line at 45.53 degrees (slope 1.0188, intercept 1.19 psi). The printed
   50.5 degrees agrees within 0.2 degrees; the line labelled 45 degrees is drawn about 0.5 degrees
   steeper than 45 (slope 2 % above 1.000). The calibration residual (0.03 psi) cannot explain this;
   it is how the line is drawn.

## Symbols relative to their lines (shear above the drawn line at the symbol's normal load)

1. dr100: T1 (3.40, 7.24) +0.69 psi, T2 (5.19, 8.74) 0.00, T3 (6.73, 10.26) -0.36, T4 (10.22,
   15.00) +0.13, T5 (13.91, 20.22) +0.87, T6 (27.11, 33.44) about -2.0 (beyond the line's right end,
   which stops at the top frame at x 26.7; extrapolated). T1 and T5 clearly sit off and above the
   line; T6 sits well below it. The line passes through T2, T3 (apex) and T4.
2. dr53: C1 +0.14, C2 -0.06, C3 +0.01, C4 +0.29, C5 +0.03, C6 -0.37 psi. The line runs into and out
   of C1, C2, C3 and C5 (it is not drawn inside them), passes through the lower right of C4 and over
   the upper-left ring of C6, and ends just beyond C6.

## Marker reading

1. Circles: center fitted to the ring's inner edge and outer edge (helpers/circlefit.py); the center
   dot agrees within 0.5 px where no grid line crosses it. Bound 2 px; 3 px for C4, whose ring is
   partly hidden by the x = 10 grid line and the 45° line.
2. Triangles (rule 8): centroid = mean of the centroid of the outer outline and the centroid of the
   inner hole, which brackets the stroke-centerline triangle; read on ASCII ink maps
   (helpers/ascii.py). v bound 7 px (8 px for T3), which is at least height/6 and contains the
   bounding-box midpoint; u bound 3 px. The center dots fall within 2 px of these centroids.
3. T3 is the least certain triangle: its apex is under the 50.5° line and its base merges with the
   y = 10 grid line; the outer apex was estimated from the hole apex, hence the wider bound.
   T2 (x = 5 grid line and the line through it), T4 (x = 10 and y = 15 grid lines and the line
   through it) and T5 (base merged with the y = 20 grid line) are partly hidden but their apex and
   at least one base corner are clear.

## Trace reading

1. Each line was measured column by column on its ink (helpers/make_points.py), leaving out columns
   inside a symbol's zone, columns where the line merges with a grid line, and the dash gaps. Line
   thickness about 7.5 px perpendicular, so trace bounds are 4 px.
2. Samples: left end, x = 2, 4, ..., 26 psi, right end; 15 per line. Exceptions:
   - dr53 x = 14 falls inside circle C5 (the line is not drawn inside it): sample at the nearest
     clean ink beyond the ring, x = 14.16.
   - dr53 x = 26 falls against the left side of circle C6: sample at x = 25.96.
   - dr100 x = 10 falls where the line crosses the x = 10 grid line, about 14 px below T4's base:
     sample at the last clean column before the crossing, x = 9.98.
   - dr100 x = 2 is 3 px from the lower end of the third dash, where the column runs are cut by the
     dash cap and the y = 5 grid line; read from row centers instead (the column fit sat 2.5 px off).
3. Dashed parts. Upper line: three dashes from the axis (ink u 668 to 713, 727 to 771, 787 to 838),
   solid from u 853 (x about 3.0). Lower line: three dashes (u 668 to 712, 734 to 768, 787 to 823),
   then a segment from u 838 that runs into the first circle C1 and continues solid beyond it.
   Whether that segment is a fourth dash or the start of the solid line cannot be told from the ink
   (its length suits a dash, its start x 2.8 matches where the upper line turns solid). No sample
   falls on it. The left ends and the x = 2 samples are on dashes and marked "dashed".
4. Left ends and intercepts: the first dash of each line reaches the y axis and its ink merges with
   the axis ink, so the end is placed where the first dash's centerline (straight fit over the first
   two dashes) meets x = 0: dr100 at y = 2.42 psi, dr53 at y = 1.21 psi. Bound 5 px. The intercept
   feature is the same point.
5. Right ends: the 50.5° line runs into the top frame line (y = 35) and stops there; the end is
   placed where its centerline meets the frame centerline (x 26.71), with bounds 6 and 7 px that
   take in the last point where the line's ink is distinct from the frame (frame's lower edge, about
   u 2308, v 961). The 45° line ends free at x 26.54, y 28.25, just beyond circle C6.

## Other ink, not symbols

Short stray dashes at about (1365, 2387), (1450, 2387), near both angle labels and near several
symbols (to the right of C1 to C4), a dotted underline under the x-axis labels and short rules near
the y axis below y = 5. None has the shape of a plotted symbol; none was read.

## Counts

dr53: 6 markers, 15 trace samples, 2 features. dr100: 6 markers, 15 trace samples, 2 features.
46 rows in points-p1.csv.
