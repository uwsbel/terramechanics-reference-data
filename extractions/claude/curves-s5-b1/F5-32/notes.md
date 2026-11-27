# F5-32, Claude reading (batch curves-s5-b1)

Figure 5-32, "Strut Axial Load versus Time (NASA Test No. 2)", printed page 5-57, PDF page 337
(`packet/p0337.png`). Pixel coordinates are those of the unrotated page (u right, v down). Values in the
native files are in the printed units (lb, s); SI conversion (1 lbf = 4.4482216152605 N) is left to the
project's tools.

## 1. Orientation and panels

1. The figure is printed sideways: the caption and the time axis read bottom to top, so the page is turned
   90 degrees clockwise to read it. Time grows up the page (v decreasing); 0 is the bottom frame
   (v about 3496 at u 2240, 3503 at u 1357; the frame is tilted, slope dv/du = -0.0081).
2. Panels, upright top to bottom, as in `series.csv`: panel 1 Strut No. 3 (`strut3`, load lines at u about
   1100 to 1357), panel 2 Strut No. 2 (`strut2`, u about 1524 to 1780), panel 3 Strut No. 1 (`strut1`,
   u about 1951 to 2288). One solid line per panel, no symbols.
3. Load grows to the left on the page for every label sequence as printed: panel 1 labels 0, -20, -40,
   -60 leftwards, panel 2 0, +20, +40, (-)60 leftwards, panel 3 0, -20, -40, -60, -80 leftwards. In the
   upright view the compression panels plot compression upwards with negative numbers; values are recorded
   as the scale gives them (compression negative, tension positive).

## 2. Labels as printed (all in `calibration-eye-checks.csv`)

1. Axis titles as printed: "(Compression) Load on Strut No. 3 (lbs.)", "(Tension) Load on Strut No. 2
   (lbs.)", "(Compression) Load on Strut No. 1 (lbs.)" (the 1 is damaged and reads like a t), and
   "Time - Seconds". These agree with the figures index.
2. **Slip, panel 2:** the top label is printed "-60" (a short dash, no vertical stroke; the +40 and +20
   below it carry clear plus signs). The panel's own sequence 0, +20, +40 and its (Tension) title make it
   +60. The line is anchored at **60**, not -60. The digits 60 are clear.
3. **Slip, time axis:** the ".09" label is damaged (the point and the 0 are broken; it reads like "(,9").
   Anchored at 0.09 from the sequence; its tick is drawn and sits 170 px from the 0.08 and 0.10 ticks like
   every other interval.
4. The ".07" label has a slightly malformed 7 (reads like a ?), legible in the sequence.
5. Panel 3's "0" is printed about 9 px off its line, towards the -20 line (85 px away); the line is the
   figure's right frame, which the panel's own sequence (-80 to -20 at 85 px spacing) puts at 0. Every
   other load label sits within 4.2 px of its line, every time label within 5.6 px.
6. Lines without labels: panel 1's grid continues past -60 with three more unlabeled lines (u about 842,
   928, 1013 at the bottom frame) and the figure's left frame (u about 755). They are not used; the trace
   never goes beyond -27 lb. The figure's frame also extends past the 0.10 time line up to v about 1029, to
   hold the inset; no time label is printed there.
7. The 0.10 line is printed as a label, but its line is only a 3 px speck at u 2233 and 2 px stubs on the
   frame and on the -20 line of panel 3 (v about 1792.5). The tool's ink check rejects it ("tick found at 0
   of 6 stub positions"), so it is not a knot: all values beyond t = 0.09 are extrapolated from the 0.08
   and 0.09 lines (flagged `extrapolated x` in `cal_model`). The 0.10 line measured on its speck is 0.5 px
   from where that extrapolation puts it (the map gives 0.10003 s at the speck).

## 3. Calibration (`cal-p1`, `cal-p2`, `cal-p3`)

1. **Why a helper and not `detect`:** the time grid lines are drawn only as dashes at the right frame
   (and as longer dashes across panel 3 for 0.01 to 0.03 and 0.07); across panels 1 and 2 only remnants
   survive (dots, and thickenings where they cross the load lines). `calibrate_axes.py detect` fails on
   every panel ("h: fewer than two grid lines span 50% of the bands"). The calibration directories were
   written by `helpers/build_cal.py` in the layout of `detect` (anchors.csv, calibration.json with `box`),
   from lines measured on the page by `helpers/measure_grid.py` and `helpers/fit_time_lines.py`.
2. **Time (x) knots, every panel:** t = 0 is the bottom frame, a solid 6 px line fitted in 286 columns
   (rms 0.54 px), anchored at its crossings with the panel's load lines. t = 0.01 to 0.09 are **ticks**:
   one anchor each, at the centre of the dash drawn at the right frame (13 to 52 columns of ink each,
   scatter 0.07 to 0.59 px); like any lone tick in `calibrate_axes.py` they take the tilt of the panel's
   affine map. All ten pass the tool's ink check on every panel; 0.10 is rejected (item 2.7).
3. **Load (y) knots:** every labeled load line is a drawn (dashed) line, its ink centre fitted in 135 to
   420 rows over v 1790 to 3482 (rms 0.36 to 0.84 px, width 3 px), anchored (y only) at its crossings
   with the time lines. All 13 pass the ink check (found at 16 to 25 of 25 positions).
4. **Affine residuals** (on the crossings of the panel's load lines with the time lines fitted across the
   figure, `affine_anchors` in calibration.json):
   - panel 1: x rms 2.4e-5 s (0.024 percent of 0.10 s), max 5.9e-5 s; y rms 0.072 lb (0.12 percent of
     60 lb), max 0.147 lb
   - panel 2: x rms 2.3e-5 s, max 5.3e-5 s; y rms 0.075 lb (0.13 percent), max 0.129 lb
   - panel 3: x rms 2.7e-5 s, max 5.0e-5 s; y rms 0.108 lb (0.14 percent of 80 lb), max 0.187 lb
   - scales: 5.86e-5 s per px; 0.235 lb per px (panel 3: 0.237)
5. **The time lines fan out across the page.** Fitted to their own ink across the whole figure, their
   tilt changes steadily from dv/du = -0.0081 (t = 0, the frame) through -0.0075 (0.01) to -0.0043
   (0.08, 0.09); the load lines tilt by du/dv = +0.0090 to +0.0104. This looks like a distortion of the
   printed page or the scan, not of the drafting. The ticks extended to panels 1 and 2 with the panel's
   single affine tilt (-0.0056) therefore sit up to 2.2 px (panel 1, t = 0.01) from the lines fitted to the
   ink across the figure. Measured on the samples, the tick map and a map between the full-width lines
   differ by at most 0.00011 s on panel 1, 0.00009 s on panel 2, 0.00005 s on panel 3, under the samples'
   x bounds (0.00015 to 0.00034 s). This extension error is **not** in the tool's knot location error
   (0.5 px for a tick). A design anchoring the full-width lines as drawn lines was tried and rejected by
   the ink check (too little ink across panels 1 and 2), as expected.
6. Each directory holds `knots-checked.json`, the tool's own ink check of every line (verified and
   rejected, with reasons).

## 4. Points

1. Samples per panel: panel 1 (`strut3`) 34 trace, 9 feature; panel 2 (`strut2`) 35 trace, 6 feature;
   panel 3 (`strut1`) 36 trace, 6 feature. Drawing order is time order (each page row crosses each trace
   once).
2. Trace samples: the first ink, every 0.002 s to 0.02 s, every 0.005 s to 0.10 s, the last ink, plus a
   sample at every multiple of 5 lb crossed on steep parts (where two time samples differ by more than
   5 lb): panel 1 at 0.003 to 0.0105 s (the first pulse), panel 2 at 0.003 to 0.0114 s, panel 3 at 0.0004
   to 0.0025 s and 0.026 to 0.033 s. Samples are placed on a centre line extracted row by row (columns on
   panel 3's initial rise, which runs almost along the page's rows), see `helpers/`.
3. Bounds: half the trace's thickness across the line where the sample is (the trace is 4 to 7 px thick,
   bounds 2.0 to 3.7 px), plus 1 px where the trace runs over a load grid line or merges with the frame
   (largest trace bound 4.4 px).
4. Five samples that fell on a grid line crossing (three 5 lb level samples and two time samples) were
   moved 1 to 6 px along the trace to where the trace has ink of its own once the grid line is removed
   (the note says so): panel 1 sequences 12 (0 lb level), 14 (t = 0.014 s), 23 (t = 0.05 s); panel 2
   sequence 7 (+20 lb level); panel 3 sequence 4 (-20 lb level). Their values are then near, not at, the
   nominal level or time.
5. **Feature roles follow the curve as drawn upright:** `peak` is a local maximum of the plotted curve,
   `knee, minimum` a local minimum, where up is the direction in which the panel's printed labels grow in
   magnitude. On panels 1 and 3 (compression, labels 0, -20, -40 upwards) a `peak` is the most negative
   signed value (largest compression) and a `knee, minimum` a local maximum of the signed value; on panel 2
   (tension) the roles match the signed value. Each note gives the signed value. A reader who assigned the
   roles on the signed value would swap peak and minimum on panels 1 and 3.
6. Features:
   - panel 1: first (0 lb at t = 0); peak -18.4 lb at 0.0057 s (sharp vertex); knee, minimum +4.7 lb at
     0.0119 s (below the 0 line); peak -4.5 lb at 0.0174 s; knee, minimum -2.2 lb at 0.0264 s; peak
     -4.2 lb at 0.0328 s; knee, minimum about 0 lb at 0.048 s (flat, on the 0 line, t ill defined); peak
     -26.6 lb at 0.0949 s; last -24.0 lb at 0.1031 s
   - panel 2: first (0 lb at t = 0); peak +32.6 lb at 0.0084 s; knee, minimum +21.7 lb at 0.0140 s; peak
     +46.5 lb at 0.075 s (broad, within 1 lb from 0.054 to 0.086 s); knee, minimum +45.0 lb at 0.091 s
     (shallow, 1.4 lb, about 6 px across the grid); last +50.5 lb at 0.1030 s
   - panel 3: first (hidden in the frame, see 5.3); knee -39.1 lb at 0.0037 s (end of the initial rise);
     peak -43.0 lb at 0.0112 s; knee, minimum -37.3 lb at 0.0213 s; peak -60.5 lb at 0.072 s (flat top on
     the -60 line, within 0.5 lb from 0.063 to 0.079 s); last -50.6 lb at 0.1031 s
7. All three traces end at t about 0.103 s, beyond the printed 0.10: extrapolated in t (item 2.7).

## 5. Where the trace is hard to follow

1. Panel 1, t about 0.043 to 0.056 s: the trace runs on top of the 0 lb grid line (merged run 5 to 8 px);
   its centre is known to about 1.5 px there (bounds widened by 1 px). Short merges also at the -20 line
   near t = 0.08 s.
2. Panel 1, t about 0.0101 s (v 3347 to 3351): a break of about 7 px in the drawn line on the steep
   return of the first pulse; no sample sits in it.
3. Panel 3 start: the trace's ink runs into the bottom frame at u about 2252 (t about 0.0003 s, -8.7 lb)
   and is hidden in the 6 px frame line from there to the corner with the 0 lb line (u 2288). Extrapolating
   its slope it reaches the frame's centre line near u 2263 (about -6 lb); whether the drawn line starts
   there or runs along the frame to 0 lb at the corner cannot be seen. The first trace sample is at the
   last visible ink (2252, 3491.5); the `first` feature is placed mid stretch (2270, 3495) with a u bound
   of 18 px covering both.
4. Panels 1 and 2 start: the last 15 px of each trace before the frame run over the 0 lb grid line; the
   first point is where the trace's ink meets the frame at that line (bulge just right of the line).
5. Panel 3, t about 0.004 to 0.009 s and 0.013 to 0.017 s: the trace runs along and across the -40 lb
   line; t about 0.063 to 0.081 s it lies on the -60 lb line (merged run 4 to 6 px). Bounds widened by
   1 px there.
6. Panel 3, t about 0.027 s (v 3049 to 3054): a break of about 5 px in both the trace and the -40 lb line;
   the -40 lb level sample that fell in it was moved to the ink just above (sequence 18).
7. Panel 2 is clean except where it crosses the +40 line near t = 0.04 s.

## 6. Inset and the drop's conditions (not points)

1. At the right of the figure (upright view; the top of the page) a plan-view sketch of the model: an X of
   four legs with a footpad circle at each end, arrows to the measuring points and circled numbers
   (legible as 3, 4, 5, 6, 7, 9, 10, 11, 12; several damaged), with the labels "No. 1 Footpad", "Strut
   No. 1 Axial Load No. 1", "Strut No. 3 Axial Load No. 3", "Strut No. 2 Axial Load No. 2" and an arrow
   "-Z".
2. Conditions as printed: **"Vv = -60.55 In. Sec.   Vh = 83.75 In. Sec."** and **"RS Loose   Level
   Surface"** (V with subscripts v and h; "In. Sec." without a slash).
3. Legibility: the typewritten digits are degraded. In Vv the first digit could be read 5 or 6 (its lower
   left is open like a 5, its top curls like a 6) and the second is a broken 0; -60.55 is the most likely
   reading, -50.55 possible. In Vh the first digit is most likely 8 (a closed lower loop with a broken
   upper one); the 7 and 5 are clear.
4. **Difference from Table 5-T3** (PDF 325, NASA Test No. 2, Bendix drop 11: Vv -60.5 in/s, Vh 83.5 in/s,
   tau .177 s, RS Loose, Dr 0, 46.9 lb/ft3, 41 deg) and from the figures index ("VV -60.5 in/s,
   VH 83.5 in/s (T5-3)"): the inset prints Vh = 83.75, not 83.5 (0.25 in/s more), and Vv = -60.55, not
   -60.5. In SI: inset -1.538 m/s and 2.127 m/s; table -1.537 m/s and 2.121 m/s. The index took the table's
   numbers; the figure's own inset differs in the horizontal velocity.

## 7. Differences from the task description and the index

1. None in the panel order, series, axis titles or units. The task's "a -60 above +40" is panel 2 (item
   2.2) and its "damaged .09" is the time label (item 2.3); both found as described.
2. The index's states field ("loose (Dr 0, 46.9 pcf)") comes from Table 5-T3; the figure prints only "RS
   Loose".
