# FA-26, Figure A-26, printed page A-53, PDF page 54 (Claude reading, blind)

Caption as printed: "Figure A-26. Average and Range of Five Samples of SS Soil" (matches the figures
index). Page header: "GRAIN SIZE ANALYSIS CURVES - LM SMS". Read on `packet/p0054.png` as scanned
(3213 x 4558 px, bilevel); the figure is printed sideways: grain size increases up the page, percent
finer increases to the left. One panel, three curves, no plotted symbols (no markers).

## Frame and labels

1. Percent finer (vertical page lines): labelled 100 at the left frame (u 575) to 0 at the right
   frame (u 2032), every 10 percent; all eleven labels checked by eye below the plot, each 1.4 to 3.9 px
   left of its line. Both side frames carry labels (100 and 0).
2. Grain size (horizontal page lines, log paper): labels 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0,
   3.0, 4.0, 5.0, 9.0 printed to the right of the plot. The bottom frame (v 3797) carries 0.02 (label
   centre 9 px below it, no other line within 90 px). The label "9.0" sits on the line at v 1218, not on
   the top frame: the top frame (v 1172) is unlabelled (about 10 mm by extrapolation) and was not
   anchored. The U.S. sieve-number scale on the left, the dashed sieve lines and the unlabelled
   subdivision lines were not anchored. As a check only, the calibration places the unlabelled minor
   lines at 0.25, 0.35, 0.4, 0.6, 0.7, 0.8, 0.9 mm within 0.5 percent, and the dashed #40 and #20 sieve
   lines at 0.419 and 0.837 mm.

## Calibration (cal-p1)

`calibrate_axes.py detect --x-transform log10 --x-direction up --y-direction left`, run twice:

1. `cal-full-box/`: box 565 1207 2042 3810 (top edge below the top frame and the 3/8 in. sieve line so
   that the outermost tracks are the 9.0 and 0.02 lines). All 12 grain-size lines and 11 percent lines
   detected, but the percent lines 90, 80, 70, 60 are covered by the parameter table for v 2560 to 3770;
   their fits there picked up the table border and text (90 found 4.5 px off at the bottom, rejected by
   the ink check, 2.34 px from the ink at one end).
2. `cal-upper-box/`: box 565 1207 2042 2452, above the table, where 90, 80, 70, 60 are drawn in full
   (10 of 10 bands).

`cal-p1/` takes every line from the full-frame run except 90, 80, 70, 60, which come from the upper
run (`helpers/merge_cal.py`; a row that would mix the two runs anchors one axis only). All 23 lines
pass the ink check (`cal-p1/knots-check.json`), line location errors 0.5 to 1.6 px. Affine diagnostic
residuals: x (log10 mm) rms 0.0024, max 0.0056 (0.21 percent of the 2.65-decade span); y rms 0.053,
max 0.186 percent. Values come from the piecewise map (`points-p1-native.csv`, `--image`); 20 points
whose read interval reaches past the 0 or 100 percent frame are flagged `extrapolated y`.

## Which curve is which

Three thick lines (about 10 px across) run touching each other for most of their length:

1. The middle line is continuous (solid): `average`.
2. The two outer lines are dashed (dashes about 50 px, gaps 10 to 15 px, period about 62 px along u).
   The line lower-left on the page (higher percent at a given grain size) is `upper`; the line
   upper-right is `lower`. The order holds at every sample (upper > average > lower in percent).
3. In the flat middle (u 690 to 1850) the three lines touch with no white between them (band 30 to
   34 px when all three are present, 21 to 24 px when one dashed line is in a gap). The average is
   placed at the middle of the band, or half a line from the edge exposed by a dash gap; the dashed
   lines half a line inside the band edges. Band edges lie on grid rows in many columns: the 0.5 mm
   line near u 900 to 1050, and the dashed #40 sieve line (v 2514 to 2522), which runs along the band
   for u 1230 to 1460 under the upper series. Bounds there are 6 px.

## Where they run together (bounds widened, identities not separable)

1. Coarse end (v 2220 to 2320): `lower` is a separate stroke on the right; its top runs up along the
   left edge of the 100 percent frame to the #20 sieve line (last point (566, 2222), 100.6 percent as
   drawn). `average` and `upper` share one stroke from v 2269 to 2315 (16 to 17 px wide, two lines);
   the average ends at the top of that stroke (566, 2269). The upper series continues above as one dash
   drawn left of the 100 percent frame, so its last two samples read 101.2 and 101.6 percent: as drawn,
   not corrected.
2. Fine end (v 2780 to 2977): the band merges on the 0.2 mm grid line; below v about 2955 all three
   curves run together into one stroke along the left side of the 0 percent frame, ending at about
   (2026, 2977). The first point and the 0.1413 mm sample of all three series are that common stroke
   (bound 8 px across, 6 px along). At 0.1585 mm average and lower are still merged beside the frame.

## Sampling

Every 0.05 decade from 0.1413 to 0.7943 mm (0.8913 mm is above the ink of all three curves), plus
5-percent samples where a curve rises more than 10 percent between two of them: lower 35 to 45, 55 to
70, 75 to 85; average 25 to 35, 40 to 50, 55 to 75, 80 to 90; upper 30 to 35, 45 to 55, 60 to 80, 85
to 90. Two 5-percent samples coincide with a grain-size sample and were not repeated: upper 40 percent
(the 0.3981 mm sample is 40.2 percent, 3 px away) and lower 50 percent (the 0.4467 mm sample is 49.9
percent, 1 px away). Samples that fell in a dash gap were moved to the nearest dash end (rule 7), each
said in its note: lower at 0.3981 mm, 40, 45, 70, 75 percent and 0.7943 mm; upper at 0.1585 and 0.3548
mm, 30, 50, 55, 80, 85 percent. Features: first and last point of each trace (the last point is also
the maximum); no knee.

## A check against the parameter table (not used in the reading)

From the traces as read: D10 = 0.262 / 0.275 / 0.285 mm (upper / average / lower), D50 = 0.424 /
0.438 / 0.447, D95 = 0.578 / 0.603 / 0.621, Cu (D60/D10) of the average 1.67. The table prints D10 0.28
(range 0.27 to 0.29), D50 0.42 (0.40 to 0.43), D95 0.6 (0.58 to 0.62), Cu 1.5. D95 and D10 agree; D50
does not: the drawn average crosses 50 percent at about 0.438 mm (u 1302, v 2499), about 19 px above
the 0.42 mm (#40 sieve) line, and the drawn range at 50 percent is 0.424 to 0.447 mm. Either the curves
as drawn differ from the tabulated values near the middle, or my identification of the lines in the
middle band is wrong; the dash pattern supports the identification (the middle line has no gap from
u 690 to 1850), so I report the disagreement as found.

## Files

`cal-p1/` (merged map, `knots-check.json`), `cal-full-box/`, `cal-upper-box/`,
`calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`; helpers and
zoomed crops under `helpers/` and `crops/`.
