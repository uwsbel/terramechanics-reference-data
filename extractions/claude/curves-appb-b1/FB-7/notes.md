# FB-7, panel 1: Claude's blind reading (batch curves-appb-b1)

Page `p0113.png` (300 dpi, 3213 x 4604, binary black and white), printed page 10. Printed caption:
"Fig. 7 E VERSUS σ3 FOR LSM SOIL" (printed as Fig. 7, not B-7; the figures index title matches it).
Axis titles as printed: "Modulus, E=ρc², kips/in.²" (y) and "Confining Pressure, σ3, psi" (x).
Pixel coordinates below are page pixels (u right, v down).

## 1. Calibration (`cal-p1/calibration.json`, helper `cal_ticks.py`)

1. No grid lines. Inward ticks on the left side (y = 1 to 10) and the bottom side (x = 2 to 14) only;
   the top and right frame lines carry no ticks. Printed labels sit on the frame lines for x = 0
   (lower left corner), x = 16 (under the right frame), y = 0 (bottom frame) and y = 11 (top frame),
   so the four frame lines are knots, each fitted with its own tilt on its ink (372 to 593 samples,
   RMS 0.46 to 0.81 px). Ticks: centre line measured over 19 rows (x) or 7 to 17 columns (y), SD at
   most 0.73 px.
2. The frame is skewed: the vertical frame lines lean (du/dv = +0.0056 left, +0.0043 right) while the
   horizontal ones are nearly level (dv/du = -0.0019 bottom, 0.0000 top; the top line bows by up to
   2 px). A shear, not a rotation; the piecewise map handles it line by line.
3. The frame is drawn slightly outside the tick grid: from the mean tick spacing (x 280.3 px per 2 psi,
   y 280.1 px per ksi) the frame lines sit 4.1 px (x = 0), 4.5 px (x = 16), 2 px (y = 0) and 5.3 px
   (y = 11) from where the ticks predict them. Every printed label still fits its sequence, and the
   tick spacing confirms the values on the frame lines (the next value would be 280 px away).
4. Tick anchors are placed on the tick's centre line at the middle of the measured stretch of the tick
   (about 17 px inside the frame's centre line), not where the tick meets the frame. The ink check of
   `tools/calibrate_axes.py` reads a lone tick on stubs 6 to 14 px either side of its anchor, and these
   ticks exist on the inside only: with the anchor on the frame, the outer stubs landed on the tops of
   the printed labels and on specks below the frame, x = 14 was rejected ("misplaced: 2.24 px") and
   x = 10 and 12 got 3.5 to 4 px errors from that stray ink. The anchor's position along a tick does
   not change the line's value position.
5. Ink check (piecewise, D-025): all 21 lines verified, none rejected, none predicted. x: 9 lines
   (0, 2, ..., 16), y: 12 lines (0, 1, ..., 11). Location errors 0.5 to 1.71 px (largest: y = 2 tick,
   1.71 px, with a square touching it; y = 11 top frame 1.39 px; x = 0 left frame 1.33 px). Details in
   `cal-p1/knots.json`.
6. Affine diagnostic on the 59 anchors: x RMS 0.0090 psi, max 0.0244 psi (0.15 % of the 16 psi span);
   y RMS 0.0064 ksi, max 0.0153 ksi (0.14 % of the 11 ksi span). Both below 0.5 %.
7. By-eye label checks (`calibration-eye-checks.csv`): x labels 0, 2, 8, 10, 16 and y labels 0, 1, 3,
   6, 10, 11, all agree with their lines. Label offsets: x labels are printed between 22 px left
   ("2") and 15 px right ("10") of their ticks, and "0" sits 13 px right of the left frame line, under
   the corner; y labels sit 3 px above to 10 px below their lines ("11" is 10 px below the top frame).
   None is ambiguous: the nearest other line is always about 280 px away. No label fails its sequence.

## 2. Series identity (read carefully: part of it is an inference)

1. The page prints one legend key only: a square with a diagonal (the `square with x` symbol) left of
   "Dr = 1.04" at (1806, 1314). That key is not a data point and is not recorded as a marker.
2. "Dr = 0.995" and "Dr = 0.77" are curve labels printed at the right ends of the upper and lower
   polylines (text centres (2299, 1588.5) and (2173, 1773.5)), with no key symbol. **The page does not
   say which symbol is Dr = 0.995 and which is Dr = 0.77.**
3. I assigned the open circles to `dr99p5` and the filled circles to `dr77` from the lines: all 7 open
   circles lie on or nearest the upper (0.995) polyline (its two vertices are inside open circles, it
   passes through the open circle at 8.99 psi, and its left end lies between the two open circles at
   sigma3 = 0, on the extension through the lower one); the filled circles scatter around the lower
   (0.77) polyline, 7 of 9 nearest to it. The two filled circles nearer the upper line are at
   (2.01, 5.93) and (5.27, 7.54). This should be confirmed against the tabulated data (the figures
   index gives the figure as derived from T2-3), which was not in the packet.
4. The squares (`dr104`) have no polyline. They sit on both polylines: the lower polyline's first
   vertex is at the bottom edge of the square at (2.02, 5.46) and the lower polyline passes through the
   square at (9.30, 7.53); the upper polyline passes through the squares at (4.29, 6.94) and (4.93,
   7.28). So the squares cannot tell the two lines apart, and the 1.04 group is not plotted above the
   0.995 group (as printed; not a reading problem).
5. The square at (2101.5, 1646.0), (11.45, 8.18), sits between the end of the upper polyline and its
   label. It has the size of the data squares and is not level with the label text (the 1.04 key is
   level with its text), so it is read as a data point of `dr104`, not as a key for 0.995. Two groups
   cannot share a key symbol in any case.

## 3. Markers (25)

1. Positions are bounding-box centres of the symbols, located by template matching against clean
   symbols of the same page (`find_symbols.py`) and checked by eye on zoomed crops and the overlay.
   Circles are 40 x 42 px, squares 36 x 39 px. Bound 2 px unless noted.
2. The symbols at sigma3 = 0 are drawn 3 to 6 px left of the left frame's centre line, so they read
   x = -0.02 to -0.04 psi (flagged `extrapolated x` by the piecewise map). They are tests at
   sigma3 = 0 by intent; the values are reported as read.
3. Overlaps at sigma3 = 0:
   - Open circle (497.5, 3071.0) and square (499.5, 3087.5) overlap (open circle above). Told apart
     by the circle's top edge and the top of its inner hole, and the square's sides and flat bottom;
     v bounds 4 px (circle) and 3 px (square).
   - Two filled circles form one blob 62 px tall and 39 px wide with a waist at v 3490: two markers
     at (501.0, 3482.5) and (501.0, 3502.5), from the blob's top and bottom edges, v bound 3 px. A
     third filled circle hidden between them cannot be excluded.
   - The open circle at (497.5, 3020.5) touches the next open circle and carries the upper polyline
     along its right side; its centre is clean.
4. Counts: `dr104` 9 squares, `dr99p5` 7 open circles, `dr77` 9 filled circles. A search at a lower
   template threshold found no further symbol (only cross-type matches on known symbols and on letters
   of the labels).

## 4. Polylines (`trace_lines.py`, `build_points.py`)

1. Two polylines, each of three straight segments, fitted on their ink (fit RMS 0.42 to 0.58 px;
   median line thickness 7.2 to 9.8 px across the line). Upper polyline: label "Dr = 0.995"
   (`dr99p5`); lower polyline: label "Dr = 0.77" (`dr77`). Each label is printed just right of its
   line's right end. No polyline for Dr = 1.04.
2. Upper (`dr99p5`): vertices (1.91, 6.15) and (5.34, 7.38), both inside open circles (hidden, feature
   only, bound 4 px); right end at (10.96, 8.40). Its last 45 px on the left run along the right side
   of the open circle at (497.5, 3020.5), merged with that outline, and its right edge is seen
   receding into the frame at v 3035 to 3046. The first trace sample is therefore the last clear ink
   at (518.5, 3000.7) = (0.11, 3.36); the first-point feature is where the line's centre line meets
   the frame's centre line, (503.5, 3050.0) = (0.00, 3.18), at the top of the lower open circle at
   sigma3 = 0, whose centre lies on the line's extension (bound 4 x 6 px; on merged ink, not a trace
   sample).
3. Lower (`dr77`): left end where it merges into the left frame, (507.1, 3695.5) = (0.00, 0.87): its
   own ink is clear down to v 3652 and its right edge reaches the frame's edge at v 3702 (v bound
   6 px). Vertices (2.00, 5.38), at the bottom edge of the square at (786.5, 2409) (hidden, feature
   only), and (4.99, 6.55), on clean ink (trace sample and feature). Right end (10.64, 7.74).
4. Trace samples left out because the line is hidden by a symbol at that position (rule 7): `dr99p5`
   at 2 psi (open circle), 5 psi (square at (1190.5, 1899)) and 9 psi (open circle at (1757.5,
   1688.5)); `dr77` at 2 psi (square). `dr77` at 5 psi is 1.2 px from the vertex sample and is not
   repeated. Trace bounds are half the line thickness measured at each sample (3.6 to 4.9 px).
5. Counts: `dr99p5` 9 trace samples and 5 features (first point, 2 vertices, last point, label);
   `dr77` 11 trace samples and 5 features; `dr104` 1 feature (label).

## 5. Files

1. `cal-p1/calibration.json` (tick calibration, anchors inside), `cal-p1/knots.json` (ink check).
2. `calibration-eye-checks.csv`.
3. `points-p1.csv` (56 points), `points-p1-native.csv` (piecewise values, `--image`).
4. `overlay-p1.png` (page box 400..2850 x 780..4060; red `dr104`, green `dr99p5`, blue `dr77`).
5. Helpers: `cal_ticks.py`, `knots_check.py`, `find_symbols.py`, `trace_lines.py` (+
   `trace_lines.json`), `build_points.py`, `eye_checks.py`; zoomed crops under `crops/`.
