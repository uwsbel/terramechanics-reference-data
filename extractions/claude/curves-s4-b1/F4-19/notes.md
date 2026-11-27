# Figure 4-19, blind reading by Claude (batch curves-s4-b1)

Figure 4-19 (AM-68-1 Vol. I, printed page 4-23, PDF page 208, `packet/p0208.png`, upright): "Force and
Displacement versus Time for Vertical Impact Tests on Various RS Soils". Two panels share the time axis
("Time-Milliseconds"): panel 1 (top) "Vertical Force - Pounds", panel 2 (bottom) "Displacement - Inches".
Values below are in the printed units (ms, lb, in). Pixel coordinates refer to the unrotated page image.

## 1. What the page prints, and the series ids

1. Legend (panel 1, top right): "Footpad Diameter = 6.17 Inches"; a solid line "Run No. 4, D_r = 0"; a dotted
   line "Run No. 10, D_r = 0.45"; a dashed line "Run No. 12, D_r = 0.65" whose legend sample is a long dash,
   two short dashes and a long dash. This agrees with `series.csv` and TASK.md (run4 solid, run10 dotted, run12
   long dashes); the ids are kept. On the plot the run 12 dashes vary in length (about 15 to 150 px) with gaps
   of 10 to 40 px.
2. The same three line styles appear in panel 2; there is no legend there. Identity in panel 2 follows the
   line style. No plotted symbols (markers) on either panel.
3. Context (printed 4-22, PDF 207): vertical tests at an impact velocity of about six fps with a six-inch
   footpad (the legend says 6.17 in); Figure 4-20 shows the same results as force against penetration.

## 2. Calibration (cal-p1, cal-p2)

1. Method. The grid lines were measured with the reader's helper `measure_lines.py` (same `calibration.json`
   and `anchors.csv` layout as `tools/calibrate_axes.py detect`), not with `detect` itself: in panel 1 the left
   frame (t = 0) is touched from about v = 1250 down by the near-vertical rising branches of all three runs, and
   `detect` merged frame and trace ink and placed the frame 15 to 20 px right of the ink (its trial fit had a
   tilt of -0.0009 against +0.008 to +0.010 for every other vertical line). The helper reads the profile across
   each line every 10 px, keeps only isolated runs no wider than the line, fits a straight line with outlier
   rejection, and skips the stretches where a line is not drawn (inside the legend box of panel 1). Every line
   was then checked by `tools/calibrate_axes.py piecewise --image` (ink check, `knots-check.json`).
2. Panel 1. Anchored: time lines 0 to 100 (11 lines; the frame is the 0 line), force lines 0 to 600 every 50
   (the 50 lb lines are unlabeled, midway between labeled lines of an even grid; 600 is the labeled top frame).
   Affine residuals over 143 intersections: time RMS 0.095 ms, max 0.28 ms (0.09 and 0.28 percent of the
   anchored 100 ms); force RMS 0.36 lb, max 0.99 lb (0.06 and 0.17 percent of 600 lb). The tool's ink check
   rejects two force lines: 500 lb (dashed, and absent inside the legend box: ink at 5 of 25 positions) and
   550 lb (absent inside the legend box, where the text "Footpad Diameter = 6.17 Inches" lies on its path, so
   the check finds the text 3.3 px off). Both are drawn and measured (positions in `calibration.json`), but the
   piecewise map uses 450 and 600 as the knots between them; with the even spacing measured (120.0, 121.2 and
   122.6 px for 450 to 500, 500 to 550, 550 to 600 at u = 770) the difference at the run 12 peak is below
   0.5 lb. The 0 ms frame carries a location error of 2.5 px (0.2 ms) because the traces touch it at the bottom.
3. Panel 2. Anchored: time lines 0 to 100, displacement lines 0 to 4.0 every 0.5 (0.5, 1.5, 2.5, 3.5
   unlabeled, midway). Affine residuals over 99 intersections: time RMS 0.078 ms, max 0.24 ms; displacement RMS
   0.0036 in, max 0.0086 in (0.09 and 0.22 percent of 4.0 in). All 20 lines pass the ink check.
4. Panel 2 top frame not anchored. It is unlabeled and not parallel to the grid: it is level (v = 2172 across
   the panel) while every line of constant displacement falls about 0.007 px per px to the right, so it lies
   128 px above the 4.0 line at the left and 117 px at the right, against 120 to 122 px between labeled lines.
   The map gives it 4.53 in at the left and 4.48 in at the right. Run 4's plateau (4.11 to 4.15 in) is above the
   4.0 line, so those values are extrapolated from the 3.5 to 4.0 interval (`cal_model` says so).
5. Label checks by eye: every printed label of both axes in both panels, against the line it stands beside
   (`calibration-eye-checks.csv`, 53 rows). All labels 0 to 100 stand under their lines within 13 px (a grid
   interval is 122 px). In panel 1 the "300" label is printed 10 px above its line; in panel 2 the time label
   "50" is 13 px left of its line and "0" is 9 px left of the frame. None is ambiguous.

## 3. The time axis beyond 100 ms (the main ambiguity of this figure)

1. What is printed. Both panels have 15 evenly drawn vertical lines (frame, 13 interior lines, frame), 119.5 to
   124.2 px apart with no break mark. The labels under the first 14 lines read
   `0 10 20 30 40 50 60 70 80 90 100 120 130 140`: 110 is missing, "120", "130" and "140" stand under the
   11th, 12th and 13th interior positions (lines 11, 12, 13), and the right frame (line 14) has no label. Same in
   both panels. Checked by eye under each line (`calibration-eye-checks.csv`).
2. Two readings are possible. (A) The grid is uniform at 10 ms per interval and "110" was left out of a typed
   label strip, shifting 120, 130, 140 one line to the left: lines 11 to 14 are then 110, 120, 130, 140, and the
   axis runs 0 to 140 with 140 at the frame. (B) The labels are right as printed: lines 11, 12, 13 are 120, 130,
   140, the frame is 150, and the single interval from 100 to line 11 spans 20 ms although it is drawn the same
   width as the others. I find (A) more likely (an even grid with no break mark, and a frame that is the natural
   140 end of a 0 to 140 axis), but the page does not settle it, so lines 11 to 14 are NOT anchored.
3. How values were assigned. Times beyond the 100 line are the piecewise map extrapolated from the 90 to 100
   interval (`cal_model` = `piecewise extrapolated x`). On this map the drawn lines 11, 12, 13 and the frame read
   109.97, 119.95, 129.81, 139.87 ms in panel 1 and 109.71, 119.33, 129.00, 138.86 ms in panel 2 (the panel 2
   intervals beyond 100 are drawn 2 to 5 px narrower than the 90 to 100 interval). Every point beyond 100 ms
   carries in its note three numbers: the extrapolated value (the one in `x_native`), the value interpolated
   between the drawn lines read as 110, 120, 130, 140 (reading A, differs by up to 1.1 ms in panel 2), and the
   value read as printed, 120, 130, 140, frame 150 (reading B: about 10 ms later beyond line 11, and stretched by
   two between 100 and line 11). The time bound (`x_read_bound`) is the reading bound only and does not include
   this label ambiguity.
4. Points affected: panel 1, run4 8, run10 9, run12 11; panel 2, run4 8, run12 9 (run 10's displacement trace
   ends at 78 ms).
5. Checks of the time axis that were possible. (a) Figure 4-20 was NOT used: `p0209.png` is not in this
   workspace's packet (the brief said it would be). Beyond about 90 ms run 4's displacement is constant, so that
   cross-check would not separate (A) from (B) anyway. (b) Initial displacement rate in panel 2 (runs together,
   0 to 8 ms): about 0.08 in per ms at the start (0.41 in at 5 ms), 0.072 in per ms between 8 and 12 ms, that is
   6 to 7 fps, in line with "about six fps" (text, printed 4-22) and with 10 ms per interval near zero (20 ms per
   interval would give 3 fps). (c) Run 4's force falls from 142 lb to 38 lb between 75 and 95 ms while its
   displacement levels off at 4.15 in at 88 to 90 ms; run 12's force falls to about 26 lb by 90 ms while its
   displacement levels at 1.24 in from about 75 ms. Both panels are consistent with each other below 100 ms;
   nothing on the page tests the scale beyond 100 ms.

## 4. Sampling

1. Time samples at every 1 ms to 10 ms, every 2 ms to 30 ms, every 5 ms after, on the line of constant time of
   the reader's map, moved to the center of the ink across the line (the ink read on the original page at 17
   positions within 8 px along the line, grid bands left out; a run end inside a grid band is not taken as the
   trace's edge: the center then comes from the other edge and the line width). On a near-vertical stretch (the
   rising branches, steeper than about 80 degrees on the page) a time sample is not defined and none is taken.
2. Force samples every 50 lb where 50 lb is a finer spacing than the time spacing in effect (rate above 50 lb per
   ms to 10 ms, 25 lb per ms to 30 ms, 10 lb per ms after): the rising branches of all three runs (run4 50, 100;
   run10 50 to 200; run12 50 to 500), the falling branch of run 12 (450 to 150 lb; the 350 lb target lands on the 10 ms sample and is merged with it) and
   run 4's fall at 88 ms (100 lb).
3. Dotted trace (run 10): a sample is taken at the center of a dot (the dot nearest the target along the line);
   its time is then that of the dot, written in the note ("taken at t = ..."). Long-dash trace (run 12): a target
   that falls in a dash gap is moved along the line to the nearest dash. No sample is in a gap.
4. Bounds: half the line width measured at the sample (solid and dashed lines 11 to 13 px, dots 8 to 11 px), and
   on the dotted and dashed traces also half the local gap along the line (TASK.md). Stretches where traces or
   frames merge carry a wider bound read from the page and a note (section 5).
5. Features: first and last (where the ink starts and ends, also given as trace samples), every local maximum of
   the trace (`peak`) and the local minimum after it (`knee`, minimum). On a broad top or flat bottom the x bound
   covers the flat stretch; a peak's x is not an observation. Panel 2 run 12 also has `first` marked as a kink
   (where its own ink leaves the bundle).
6. Counts (trace / feature): panel 1, run4 42 / 6, run10 43 / 6, run12 54 / 8; panel 2, run4 41 / 4,
   run10 31 / 3, run12 32 / 3. Total 273 points. Median read bounds: 0.62 ms and 2.7 lb (panel 1), 0.65 ms and
   0.028 in (panel 2).

## 5. Where traces cross, run together, or are hard to read

1. Panel 1, first 3 ms (the rise): the left frame and the rising branches of all three runs form one bundle
   (u about 726 to 762). Run 4's rising branch is separate from the rest by about 3 px between 40 and 105 lb
   (v 1730 to 1895) and merged below; run 10's dots are separate above about 220 lb (v < 1460); run 12's dashes
   are separate above about 300 lb (v < 1265). Below those levels each trace's position inside the bundle is read
   from the bundle's extent (run 12 against the frame's right edge, run 10 in the middle, run 4 at the right) with
   bounds of 6 to 7 px (0.5 to 0.6 ms) and a note; the three `first` points (0.2 to 0.7 ms, about 2 lb) are inside
   the bottom-left corner, merged with both frames.
2. Panel 1 peaks: run 12's apex is a short separate dash (768 to 781, 549 to 576 px) between the rising and
   falling dashes: 588 lb at 4.5 ms. Run 10's highest dot is at 772.5, 1295.5 (285 lb at 3.7 ms); the drawn apex
   lies in the 25 px gap to the next dot, x bound widened. Run 4's first peak 127 lb at 2.4 ms.
3. Panel 1 crossings: run 10 and run 12 cross near 14 to 16 ms (u 893 to 915); run 4 and run 12 near 18 ms (u 935
   to 955); run 4 and run 10 near 22 to 24 ms (u 1005 to 1025). Samples there carry bounds of 6 to 8 px and a
   note.
4. Panel 1 tail, 95 to 130 ms (u 1870 to 2322): all three traces touch. Reading of the band, from column scans:
   from 100 to 110 ms a continuous bar on top (v 1901 to 1912, run 12's dash), a row of dots below it (v about
   1913 to 1922, run 10) and a bar at the bottom (v 1925 to 1936, run 4 at its minimum); from 117 ms to the end
   the dots (v 1904 to 1912) sit on a continuous bar (v 1913 to 1925); run 4 rises above both from about 110 ms.
   So runs 10 and 12 change places between about 110 and 117 ms (u 2068 to 2156), where run 4 also crosses them;
   that stretch is a tangle and its samples carry wide bounds and a note. The identification rests on the dot
   pattern (a 17 px pitch, white holes between dots) against a continuous dash; it is a reading, and the
   student should look at it. Run 12 has a dash gap from 1873 to about 1911 px (93 to 96 ms) and another at 2145
   to 2155 px.
5. Panel 1 run 4 between 22 and 50 ms is a solid line with small drop-outs (breaks of 3 to 6 px at u about 1112
   and 1140), not a dashed line; and a hole in its ink at 834 to 840 px (9 ms) splits the stroke, so that stretch
   was read from column scans (note on the points).
6. Panel 1 run 4 and run 10 end under the line labeled 140 (u about 2310 to 2316, the grid line hides the exact
   end); run 12's dash ends 4 px right of it.
7. Panel 2, origin to about 9 ms: the three traces form one bundle (20 to 29 px wide along a row, against 14 to 16 px for run 4 alone);
   run 10's dots run along run 4's stroke, on its upper-left side near the origin and on its lower-right side from
   about 6 ms, where they leave it. Run 4 and run 10 are given the same path (the bundle's center) with bounds of
   11 px in u and 7 px in v. Run 12 is not drawn separately before about 9 ms: its first ink is a dash end at
   856.9, 3134.1 (0.566 in at 9.0 ms), touching the bundle; recorded as `first` (a kink), and its first 9 ms are
   not in this reading.
8. Panel 2 run 10 (dotted) stops at about 78 ms (last dot 1692, 2781.5, 1.99 in), well before the other two,
   which run to the line labeled 140 (run 4 ends under it, run 12 11 px beyond it).
9. Panel 2 run 4 reaches 4.15 in at about 89 ms, dips to 4.11 in at about 106 ms and returns to 4.12 in; the dip
   is about 9 px on the page, twice the line half width, so it is recorded as peak and knee.

## 6. Files

1. `cal-p1/`, `cal-p2/`: `calibration.json`, `anchors.csv`, `knots-check.json` (the tool's ink check of every
   line); `cal-p1-config.json`, `cal-p2-config.json` (the helper's input).
2. `calibration-eye-checks.csv`: every printed label of both axes in both panels, plus the unlabeled lines.
3. `points-p1.csv`, `points-p2.csv` (pixels, bounds, notes) and `points-p1-native.csv`, `points-p2-native.csv`
   (from `tools/calibrate_axes.py piecewise --image`: `x_native`, `y_native`, read bounds, `cal_model`).
4. `overlay-p1.png`, `overlay-p2.png` (`tools/plot_grid.py overlay`).
5. Helpers (reader's own, under `out/`): `measure_lines.py` (grid lines), `trace_tools.py` (grid removal, ink
   following), `guides.py` with `segments.json` (ink following per stretch, `guides.json`), `series_def.py` (the
   guide of each trace: followed stretches and waypoints read by eye where traces merge, with their bounds and
   notes), `sample.py` (sampling on the ink, `samples.json`), `finalize.py` (features, CSV files), `check.py`,
   `sheet.py`, `show.py`, `runs.py` (checks and row or column scans). `crops/` holds the zoomed crops and contact
   sheets used to check the points by eye. `clean.npy` and `bandmask.npy` are the grid-removed page used by
   `sample.py` (regenerate with `trace_tools.py`).
