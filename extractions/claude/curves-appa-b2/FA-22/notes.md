# FA-22, panel 1: Claude's blind reading

Page `p0047.png` (printed A-46), header "GRAIN SIZE ANALYSIS CURVES - LM SMS", caption "Figure A-22.
Average and Range of Six Samples of RC2 Soil" (as in the figures index). Printed sideways: grain size
increases up the page (v decreasing), percent finer to the left (u decreasing).

## Which curve is which

1. `average`: the solid line, the middle curve.
2. `upper`: the dashed curve on the left of the page (higher percent finer at every grain size).
3. `lower`: the dashed curve on the right of the page (lower percent finer).

The three run separately from the fine end (#200 sieve, 0.075 mm) up to about 4 mm. Above that:

1. average and lower run together in one band of ink from the 5.0 mm grid line (v 1438) up to about
   v 1296 (about 7 mm); the lower curve's first separate dash is just below the 5.0 mm line, at
   (871, 1439). The average's #4 circle (865, 1465) sits where they part.
2. upper stays separate, as a strand just right of the 100 percent line, up to v 1296; its last dash
   there ends at v 1387, the next one higher touches the 100 percent line.
3. above v 1296 all three curves and the 100 percent frame line merge into one mass of ink (up to
   35 px wide) that runs up to the 3/8 in. circle at (759.5, 1162).

In the merged zones the samples of the merged series are at the centre of the merged ink with a u bound
of half its width (10 to 18 px), and say so in `note`; no series is assigned a branch by guess.

## Frame and labels (see calibration-eye-checks.csv)

1. Percent: labels 100 to 0 at the top and bottom; the left frame is the labelled 100 line, the right
   frame the labelled 0 line. Lines 60, 70, 80, 90 are hidden under the grain-size parameter table
   (page u 768 to 1367, v 2238 to 3752) and drawn only above it.
2. Grain size: labels 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 9.0 at the right edge.
   The bottom frame is the labelled 0.02 line. The top frame (v 1137) has no label: by log spacing it is
   10 mm, but it is not anchored (rule 5). The label read as 9.0 sits on the solid line at v 1181,
   not on the dashed 3/8 in. sieve line (v 1162.5). Lines 0.05, 0.1, 0.2, 0.5 are hidden under the table.
3. The sieve-number scale, the dashed sieve lines, the parameter table and the classification strip are
   not read as points.

## Calibration (cal-p1)

1. `calibrate_axes.py detect --box 745 1172 2245 3785 --x-direction up --y-direction left
   --x-transform log10 --bands 10 --frame-frac 0.35`, the 12 labelled grain sizes and the 11 labelled
   percent lines. `--frame-frac 0.35` because lines 60 to 90 are drawn on 41 percent of the height only;
   the box top (v 1172) keeps the unlabelled top frame and the 3/8 in. dashed line out.
2. With the raw detect output the ink check rejected x = 0.1, 0.5 and y = 60, 80, 90: each of these lines
   is drawn on one side of the table only, and detect had anchored it across the table (inside it and at
   the far frame), so the check extrapolated the ink over the hidden half. `helpers/restrict_anchors.py`
   drops the 16 anchors inside the table and un-anchors each such line at the far frame (4 x lines at
   y = 100, 4 y lines at x = 0.02), leaving the detected line positions and tilts unchanged, and refits
   the diagnostic affine map. The raw output is kept in `helpers/detect-raw/`.
3. Result: all 12 x lines and all 11 y lines verified on the ink (`cal-p1/knots-check.json`), location
   errors 0.5 to 1.6 px. Affine residuals: x rms 0.0024 in log10 (0.09 percent of the 2.65 decade span),
   max 0.0059; y rms 0.048 percent, max 0.15 percent.
4. For the batch: `calibrate_axes.py recover` is not safe on this page. Tried on the five rejected lines,
   it found the 0.09 mm minor line for 0.1 mm (43 px off) and the table's ruling lines for 60, 80 and
   90 percent. Only 0.5 mm and 70 percent came back right.
5. The lines are hand-drafted and slightly wavy (up to 2 px), and the upper decade (1 to 10 mm) is drawn
   about 1 percent longer than the lower ones, so the piecewise map matters here.

## Points

1. Sampling: first point, then every 0.05 decade from 0.0794 mm (log -1.10) to 7.94 mm (+0.90), then the
   last point. No interval rises by more than 10 percent (largest 6.3 percent, lower curve near 4 mm), so
   no extra 5 percent samples were needed.
2. Traces were measured on the page rows: a tracer and an edge fit, cross-checked, and every disagreement
   and every dash sample checked by eye on pixel rows and check tiles (`helpers/`, `crops/`). Bounds:
   5 px (half the 10 px line) unless noted.
3. Dashed curves: a sample in a dash gap was moved to the nearest dash end (upper -0.70, -0.65, +0.00,
   +0.05; lower -0.80, -0.45, -0.15, +0.40). Upper +0.05 is a tie within 0.4 px between the two ends.
   Upper +0.00 sits on the 1.0 mm grid line, under which the dash may continue.
4. Sampling lines inside a symbol were moved to the line ink just outside it (0.141 mm at #100 on all
   three curves; 0.251 mm at #60 on all three).
5. Not taken: lower -1.10 (0.0794 mm), which falls in the gap below the lower curve's first point and
   would move onto it; +0.95 (8.91 mm) on every curve, which falls on the 3/8 in. circle.
6. First points: where each line's ink starts at the fine end. Upper and average run into their #200
   symbols. The lower curve's last dash ends about 10 px short of its #200 symbol (2105, 3175).
7. Last point, all three: (759, 1191), where the merged ink meets the 3/8 in. circle. It is also the
   maximum of each trace (100 percent). No knee or kink: the curves bend smoothly into the 100 percent
   line.

## Markers

1. Symbols are on the sieve lines #200, #100, #60, #40, #20, #12, #8, #6, #4 and 3/8 in., and the
   converted grain sizes fall on those sieves (0.074, 0.146, 0.248, 0.417, 0.84, 1.66, 2.35, 3.36, 4.66,
   9.5 mm).
2. The 3/8 in. symbol is one large circle (about 47 px) at 100 percent, where all three curves end. It
   is recorded under each series with a note, so it is one symbol in three rows.
3. The lower curve has no visible symbol on the #4 line: it is inside the band it shares with the
   average there. Not recorded.
4. Shapes: the scan is bilevel and fills small open circles, so open and filled cannot be told apart
   reliably. All are `circle` except the upper curve's #40 symbol, two crossing strokes (`x`). The upper
   #100 symbol is a blob that could be a filled circle or an asterisk. Marker bounds are 4 to 6 px.

## Observation, not a correction

The table prints a D50 range of 0.9 to 2.5 mm. The lower curve read here crosses 50 percent at about
1.75 mm (49.0 percent at the #12 symbol, 1.68 mm; 58.2 percent at #8, 2.36 mm), so it does not reach
2.5 mm. The average D50 (about 1.05 mm against the printed 1.1 mm), D10 (about 0.073 mm against 0.07
mm), D95 (about 5.3 mm against 5.0 mm), the upper end of the D10 range (lower curve about 0.098 mm against 0.1 mm) and the D95 range (about 4.0 to 5.5 mm against 4.1 to 5.5 mm) agree with the curves; the lower end of the D10 range is below the drawn curves. The range curves
may not be envelopes of the six samples' D50, or the table may differ from the drawing. Left for review.

## Files

`cal-p1/` (anchors.csv, calibration.json, detect-log.txt, restrict-log.txt, knots-check.json),
`calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv` (piecewise, `--image`),
`overlay-p1.png`, `helpers/` (viewing and measuring aids, the anchor restriction, the point builder with
every manual decision), `crops/` (the views read).
