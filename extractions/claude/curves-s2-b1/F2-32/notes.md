# F2-32 (Figure 2-32, printed 2-63, PDF 88): blind reading notes

Page image `packet/p0088.png`, 3213 x 4508 px, read unrotated. The figure is printed sideways:
penetration increases up the page, load increases to the left. One panel.

## Axes and calibration

1. Penetration axis (vertical on the page): labelled 0 to 9 at every inch, 12 horizontal lines in all
   (v = 3689.0, 3476.5, 3274.5, 3066.5, 2861.0, 2653.5, 2446.0, 2239.5, 2034.5, 1827.5, 1618.5, 1416.0).
   The two top lines (pen 10 at v 1618.5 and the top frame at v 1416) carry no printed label; the
   frame is the pen 11 line (spacing 206.7 px per inch holds to the frame). The top three lines are
   interrupted by the equation text block between u 800 and 1600 and were only found with 10 bands
   (`--bands 10 --frame-frac 0.4 --min-frac 0.5`); with the default 5 bands the tool took the pen 8
   line as the top frame and dropped half of the grid.
2. Load axis (horizontal on the page): labelled 0 to 70 every 10 lb, 8 vertical lines
   (u = 1988.5, 1782, 1575, 1369, 1167, 958, 749.5, 541); the right frame line is load 0, the left frame
   load 70. Unit printed `Load (Lb.)`.
3. Calibration `cal-p1/`: 96 anchors, all 20 lines detected (none predicted). RMS residual
   0.009 in (0.08 percent of the 11 in span) and 0.079 lb (0.11 percent of 70 lb); max 0.029 in and
   0.217 lb. The pen 2 grid line is drawn crooked: v = 3263.5 at u 600 to 3274.5 at u 1700
   (slope 0.0080 against 0.001 to 0.003 for the other lines); the piecewise map should keep its own
   tilt. The column scans at u 600 / 900 / 1200 / 1500 / 1700 give v 3263.5 / 3266.5 / 3269.5 /
   3272.5 / 3274.5 for it.
4. By-eye checks (`calibration-eye-checks.csv`): pen 0, 1, 9 and load 0, 10, 20 all sit on the
   lines the tool fitted, within 0.5 px.

## Which ink is which

1. `lpt93` (LPT No. 93, Gp = 16.2): the thick dashed line (dashes about 8 px thick, 40 to 45 px
   long with 8 to 15 px gaps; the dash ends taper). Its label is written along the line on its
   upper-left side between v 2570 and 3049; the dashes continue beside the text. Starts on the
   load axis at pen 0 (first dash is a blob lying on the frame line from u 1951 to 1985), rises almost
   parallel to the load axis to about 5 lb at pen 0.17 (knee), then runs straight up-left to its top
   end at (914, 2270), pen 6.84, load 52.1. It is the leftmost (highest load) trace.
2. `lpt53` (LPT No. 53, Gp = 15.6): the thick solid line (about 7 px). Its label is printed in a
   column at u 1610 to 1667, v 2653 to 3059; the curved leader arrow ends on the solid line at
   about (1678, 3200): label and line style agree. Starts on the pen 2 grid line at the load axis
   (the first 80 px of its ink lie on the grid line, so the start is given as an interval
   u 1895 to 1985), leaves the grid line near u 1900, bends smoothly and runs straight (just right
   of the LPT 52 dots) to its top end at (981.5, 2216), pen 7.11, load 48.8.
3. `lpt52` (LPT No. 52, Gp = 15.4): the dotted line (dots about 6 px, 12 px apart). Its label is
   printed in a column at u 1815 to 1869, v 2856 to 3259; the leader arrow ends on the dots at about
   (1868, 3445): label and line style agree. Starts with a dot on the pen 1 grid line next to the
   load axis at (1973.5, 3475), rises steeply in load, bends and joins the straight line at about
   (1703, 3377) (knee), then runs straight to its top end at (965.5, 2222), pen 7.08, load 49.6.
   From the knee to about v 3115 the dots sit on a thin continuous line (a beaded look); from v 3115
   up to the top the dots run immediately left of the LPT 53 solid line, touching it on many rows.
4. `fit` (Slope = 6.5 lbs./in. = A gamma Nq): the thin straight line (3 to 5 px). Its label is the
   rotated text column at u 838 to 884, v 1349 to 1949, with a leader arrow from (856, 1977) to the
   line at (862, 2042). Visible ink: thin solid from its top end (761, 1925) down to (905, 2150), thin
   dashes (915 to 952, 2165 to 2222), then thin pieces at (969 to 979, 2246 to 2258); from there to
   about v 3115 the line is not drawn separately: it lies under the LPT 52 dots, which are its
   straight part; from v 3115 to 3390 it is the thin line joining the dots; thin dashes from (1722,
   3408) to (1776, 3500); thin solid from (1788, 3516) to the load axis at (1893, 3683). Its ends
   give slope 6.44 lb/in and intercept 4.75 lb at pen 0 (the page prints 6.5 and 4.7).

## How the samples were taken

1. Trace samples every 0.25 in, on ink, by a row-by-row tracker along hand-read guide polylines
   (`helpers/track.py`), with the grid masked. A nominal sample on an integer-inch grid line, in a
   dash gap, between dots, or where the line crosses a load grid line was moved to the nearest row
   with the line's own ink (the shift in px is in the note). Bounds: half the run width in u and
   half the line thickness in v, measured at the sampled row; dots at least 3 px; a merged run
   (two lines touching) has the merged half width.
2. Dots: in the stretch beside the solid line (v 2222 to 3115) a dot was accepted only where it is a
   run of its own with the solid line's run 2 to 20 px to its right; where a dot is merged into the
   solid line it was not used and the sample moved to the nearest separate dot.
3. The fit line's crossings of the pen 1 to 8 grid lines are interpolated between its ink just above
   and below the line (on the grid line itself the line's own ink is hidden). At pen 2 to 7 the fit
   line has no ink of its own (it coincides with the dots), which the notes say.
4. The trace rows at the ink ends duplicate the `first` and `last` features; the `peak` of each
   trace is its last point (load rises to the end of every record).

## Where lines cross or run together

1. The thin fit line and the LPT 93 dashed line cross near (1870, 3636), pen 0.25; the LPT 93 sample
   at pen 0.25 is a merged run (bound widened).
2. The LPT 52 dots lie on the fit line from pen 1.5 up; the LPT 53 solid line runs 9 to 14 px right
   of the dots from pen 3.5 up and touches them on many rows (merged runs flagged on the LPT 53
   samples at pen 3.25, 5.75 and 6.0).
3. The LPT 53 trace passes the LPT 52 label's leader (its arrowhead ends on the dots at
   (1868, 3445)); the LPT 53 label's leader crosses nothing.

## Ambiguities

1. The start of LPT 53 is on the pen 2 grid line: given as an interval (u bound 45 px).
2. The start of LPT 93 is a blob on the frame line (u 1951 to 1985): given as an interval.
3. The fit line's identity between v 2222 and 3115 is inferred from its straightness and the two
   visible ends; the ink there belongs to the dots.
4. The exact knee of LPT 52 is spread over pen 1.1 to 1.5; two knee features are given (gentle bend
   at (1850, 3447) and the join with the straight part at (1703, 3377)).
5. Where the LPT 93 dashed line crosses the load 30 and load 50 grid lines, and where the pair
   LPT 52 / LPT 53 crosses the load 40 and load 50 lines, the samples were moved up to 13 px off the
   nominal penetration.

## Figures index

`series.csv` ids and printed labels agree with the page. No plotted symbols (markers) on this
figure.
