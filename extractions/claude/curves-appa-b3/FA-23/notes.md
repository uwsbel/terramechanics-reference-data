# FA-23, Figure A-23 (Density Versus Relative Density for RC2 Soil), printed A-47, page image p0048.png

Reader: Claude (blind). Panel 1 only.

## The page differs from TASK.md

The unit-weight scale of this figure runs from **55 pcf to 100 pcf** (labels 55, 60, ... 100 on both sides),
not 25 to 65 as TASK.md describes for the batch. It is reciprocal and runs downward (every 1 pcf line lies
within 5.1 px of a smooth reciprocal fit through all of them). The Dr labels read 0.0, 0.1, ... 1.0.

## Calibration (cal-p1)

1. `calibrate_axes.py detect`, box 815 1440 2265 3752, 10 bands, `--y-transform reciprocal --y-direction down`,
   x values 0 to 1.0 by 0.1, y values 55 to 96 by 1 and 100.
2. Unlabelled lines between labels: four per 5 pcf interval, one per pcf, each within 3.3 px of its 1/value
   position in its interval; anchored (56 to 96 except the labelled ones), source naming the convention.
   97 to 99 were not found by the detector and were left out (nothing is read below 95).
3. **Above the 55 line** the frame holds one unlabelled horizontal line (v 1413 at u 900, 1407 at u 1500,
   1402 at u 2100) and the top frame line (v about 1100, near 51 pcf on this scale). If that line were 54 it
   would lie 12.6 to 14.3 px below where 54 belongs on this chart's reciprocal scale (smooth fit through the
   43 lines below it), while every other line on the chart is within 5.1 px of that fit; and no lines for
   53 or 52 are drawn. Its value cannot be named without doubt, so it was **left out**, with the top frame
   line. The upper line starts above the 55 line (printed 53.6), so its first sample is **extrapolated**
   from the 55 and 56 lines and flagged so.
4. Residuals of the affine diagnostic: x rms 0.0021 (0.21 percent), **max 0.0057 (0.57 percent, above the 0.5
   percent of protocol section 2)**; y (in q) rms 0.10 percent, max 0.24 percent of the q span from 55 to 100.
   The x residual is drafting: the Dr lines are unevenly spaced (at the top the intervals run 132.5 to 146 px
   around a mean of 138; residuals x = 0 at -0.003, x = 1.0 at -0.003 to -0.006, x = 0.4 to 0.6 at
   +0.001 to +0.004). All 11 Dr lines were found in 10 of 10 bands and lie within 0.7 px of the
   ink; no box removes uneven drafting. Values come from the piecewise map, which reads each Dr grid line
   as its printed value.
5. Ink check: 11 Dr lines and 42 unit-weight lines verified (offsets within 0.7 px); rejected: the 100
   bottom frame line (insufficient ink: too thick for the check's window).
6. Label check by eye: `calibration-eye-checks.csv` (y: 55, 60, 70, 80, 100 left; 55, 70, 80, 95 right;
   x: 0.0, 0.5, 1.0).
7. Grid drafting in the range read: lines 88 and 89 sit 5 px high against the smooth fit (spacings 85 to 90:
   34, 32, 34, 36, 38 px where a reciprocal scale shrinks them steadily). Sensitivity (in `work/`): labelled
   lines only, up to 0.20 pcf (lower line at Dr 0.8, between 85 and 90); affine map, up to 0.15 pcf.

## Which label belongs to which line

No legend on the page; ids follow `series.csv` (solid = mean, dashed above = upper, dashed below = lower).
That the dashed lines are 95 percent confidence limits is not stated on this page.

The Dr = 0 labels have no leaders: each is printed against the left frame at the height where its line
starts. The Dr = 1.0 labels have short leaders from the right frame.

| line | Dr = 0 label | where | Dr = 1.0 label | leader |
|---|---|---|---|---|
| upper (dashed) | 53.6 | centred at v 1378.5; the upper line starts at v 1379.7 | 71.2 | horizontal at v 2624, u 2242 to 2280; the upper line ends at v 2622.1 |
| mean (solid) | 61.4 | centred at v 2012; the solid line starts at v 2015.7 | 83.1 | slanted, from (2252, 3163) up to the label; the solid line ends at v 3164.4 |
| lower (dashed) | 69.2 | centred at v 2503.5; the lower line starts at v 2515.4 | 94.0 | slanted, from (2257, 3537) up to the label; the lower line ends at v 3543.8 |

## The drawn ends against the printed values

| line | Dr = 0 read | printed | Dr = 1.0 read | printed |
|---|---|---|---|---|
| upper | 53.86 +- 0.07 (extrapolated) | 53.6 | 71.52 +- 0.10 | 71.2 |
| mean | 61.46 +- 0.07 | 61.4 | 83.36 +- 0.14 | 83.1 |
| lower | 69.28 +- 0.08 | 69.2 | 94.28 +- 0.14 | 94.0 |

1. All three right ends read 0.26 to 0.32 pcf heavier than printed, beyond their bounds; the leaders point at
   the drawn ends. A straight line in 1/gamma through all eleven samples of each line ends at 71.41, 83.25
   and 94.17, still 0.15 to 0.21 pcf heavier; the rest is the local drafting of the grid near the right frame.
2. The upper line's start depends on the line above 55 that was left out. Extrapolated from 55 and 56
   (canonical): 53.86. Labelled lines only: 53.82. Affine map: 53.77. **If the unlabelled line at v about 1410
   is taken as 54, the start reads 53.56, matching the printed 53.6**: the draftsman may have plotted the end
   against that line. The tool's bound (0.07 pcf) does not cover this spread of 0.3 pcf; treat the upper's
   first sample as uncertain by about 0.3 pcf.

## Trace samples

1. Ink measured column by column (`helpers/trace_extract.py`, window 20 px, second pass); straight reference
   lines fit with rms 1.10 px (upper), 0.92 px (mean), 0.99 px (lower). All three lines share a bow against
   straight lines (about -2 px near the left frame, up to -5 px for the solid line at the frame itself, +1 px
   near Dr 0.3, -1.5 px at the right): a warped page. A sample's v is the reference line plus the median
   residual of the ink within 40 px (20 px at a line end or dash end, on the ink's side), so the bow is
   followed.
2. Bounds: half the vertical run of the ink: upper 4.5 px (9 px), mean 4.5 px (9 px), lower 4.0 px (8 px).
   These lines are steep (slopes 0.74 to 0.89), so the line's own thickness across it is about 7 px.
3. Every Dr crossing lies under a vertical grid line; a sample there is on the trace when its ink reaches
   that grid line.
4. Gaps (rule 7): upper Dr 0.2 (gap u 1103 to 1120) moved to the dash end at u 1102 (Dr 0.195); upper Dr 0.6
   (gap u 1657 to 1679) moved to u 1656 (Dr 0.595); lower Dr 0.2 (gap u 1115 to 1136) moved to the dash start
   at u 1137 (Dr 0.208), **a tie**: the other end, u 1114, is 0.2 px farther; lower Dr 0.3 (gap u 1260 to
   1279) moved to u 1259 (Dr 0.296).
5. Dashes ending at a Dr grid line, kept at the crossing: lower Dr 0.5 (ink to its left edge, u 1538) and
   Dr 0.9 (ink to u 2097). Lower Dr 0.7: the dash ends 2 to 3 px right of the grid line.
6. The solid line is unbroken. All three lines touch both frame lines.

## Flags in points-p1-native.csv

18 rows carry `extrapolated`: the 6 end samples and 6 first/last features sit on the Dr = 0 and 1.0 frame
lines (and the upper's first sample and first feature are also beyond the 55 line in y), and the 6 label
features are outside the frame. A label feature's values mean nothing; its pixel position ties the printed
value to its line.
