# FA-7, Figure A-7 (Density Versus Relative Density for PS Soil), printed A-14, page image p0015.png

Reader: Claude (blind). Panel 1 only.

## Calibration (cal-p1)

1. `calibrate_axes.py detect`, box 600 1710 2200 3520, 8 bands, `--y-transform reciprocal --y-direction down`,
   x values 0 to 1.0 by 0.1, y values 23 to 61 by 1 and 65. The page is tilted about 0.7 degree (horizontal
   lines fall 17 px from left to right, vertical lines lean 0.011 px per px); the tool fits each line's tilt.
2. The data start above the 25 label: the left ends are printed 23.3, 23.8 and 24.3. Above the 25 line the
   frame holds two unlabelled lines and then the top frame line. They are 24 and 23: every labelled interval
   of this chart holds one line per pcf, and the two lines sit 100.6 and 111.4 px apart going up (at u 1400),
   the growing steps of 1 pcf on a reciprocal scale (about 104 and 113 px predicted from the 25 to 30
   interval; a half-pcf grid would put lines about 50 px apart). Against a smooth reciprocal fit through all
   40 lines they sit within 1.1 px. They were anchored, so the left ends are interpolated, not extrapolated.
   The top frame line (about 22) was left out of the box. Their source in `anchors.csv` and
   `calibration.json` names the convention, as for the other unlabelled lines (26 to 34, 36 to 39, 41 to 44,
   46 to 49, 51 to 54, 56 to 59, 61; within 6.3 px of their 1/value positions in their 5 pcf intervals).
   62, 63, 64 were not found by the detector and were left out; nothing is read below 32.
3. Residuals: x rms 0.0014 (0.14 percent of the span), max 0.0043 (0.43 percent); y (in q = 1/value) rms
   0.14 percent, max 0.40 percent of the q span from 25 to 65. All under 0.5 percent.
4. Ink check (`piecewise --image`): all 11 Dr lines and all 40 unit-weight lines verified, ink at 25 of 25
   positions each, line-to-ink offsets within 0.97 px; none rejected (`cal-p1/knots-check.json`).
5. Label check by eye: `calibration-eye-checks.csv` (y: 25, 30, 40, 50, 65 left; 25, 30, 40, 65 right;
   x: 0, 0.1, 0.5, 1.0). Every label sits on its line or tick.
6. Grid drafting: the same pattern as on Fig. A-3 (the grid is a printed form): the 30 and 45 lines sit 4.5
   and 5.2 px low against a smooth reciprocal fit. Only the 30 line lies in the range read here (23 to 31).
   Sensitivity of the canonical values (all in `work/`): labelled lines only, up to 0.034 pcf; without the
   23 and 24 lines (left ends extrapolated from 25 and 26), up to 0.058 pcf at the left ends; affine map, up
   to 0.056 pcf. All are about the size of the trace bounds (0.05 to 0.08 pcf).

## Which label belongs to which line

The page prints no legend; ids follow `series.csv` (solid = mean, dashed above = upper, dashed below =
lower), which matches the drawing. That the dashed lines are 95 percent confidence limits is not stated on
this page.

| line | Dr = 0 label | leader | Dr = 1.0 label | leader |
|---|---|---|---|---|
| upper (dashed) | 23.3 | straight, meets the left frame at v 1786.5 where the upper line starts (v 1786.0) | 29.3 | straight, from the right frame at v 2357, where the upper line ends (v 2357.0) |
| mean (solid) | 23.8 | straight, v 1844, where the solid line starts (v 1845.1) | 30.2 | hooked, leaves the right frame at about v 2430 just below the solid line's end (v 2424.8) and turns down to the label |
| lower (dashed) | 24.3 | straight, v 1908, where the lower line starts (v 1908.0) | 31.1 | hooked, leaves the right frame at about v 2482 just below the lower line's end (v 2479.2) |

## The drawn ends against the printed values

| line | Dr = 0 read | printed | Dr = 1.0 read | printed |
|---|---|---|---|---|
| upper | 23.18 +- 0.05 | 23.3 | 29.24 +- 0.08 | 29.3 |
| mean | 23.70 +- 0.05 | 23.8 | 30.21 +- 0.08 | 30.2 |
| lower | 24.29 +- 0.05 | 24.3 | 31.08 +- 0.08 | 31.1 |

The drawn ends agree with the printed values within 0.12 pcf; at Dr = 0 the upper and mean lines start
0.10 to 0.12 pcf lighter than printed, about twice their bounds.

## Trace samples

1. Ink measured column by column (`helpers/trace_extract.py`, second pass with the first fit as the guess);
   robust straight line per series, rms 0.75 px (upper, 916 columns), 0.63 px (mean, 1142), 0.70 px
   (lower, 958). A sample's v is that line plus the median residual of the ink within 40 px (20 px first at a
   line end or a dash end, on the ink's side); half-edge columns added only at the mean's right end; the
   lower's right end needed an 80 px window.
2. Bounds: half the line's vertical thickness: upper 4.5 px (9 px), mean 4.0 px (8 px), lower 4.0 px (8 px).
3. Every Dr crossing lies under a vertical grid line; a sample there is on the trace when its ink reaches
   that grid line.
4. Gaps (rule 7), lower line: Dr 0.3 falls in a gap (u 1080 to 1103; the line runs along the 31 grid line
   there; no trace ink shows above the grid line from u 1080 nor below it before u 1104): moved to the
   dash start at u 1104 (Dr 0.308); the other dash end, u 1079, is 1.4 px farther. Dr 0.7 falls in the gap
   u 1682 to 1709: moved to the dash start at u 1710 (Dr 0.704).
5. Dashes ending at a Dr grid line, kept at the crossing: upper Dr 0.3 (ink to about u 1092; a white notch
   in the grid line at the trace's height at u 1095 to 1096), upper Dr 0.7 (ink to about u 1707).
6. The solid line is unbroken. All three lines touch both frame lines; first and last samples are there.

## Flags in points-p1-native.csv

18 rows carry `extrapolated`: the 6 end samples and 6 first/last features sit on the Dr = 0 and 1.0 frame
lines, and the 6 label features are outside the frame. A label feature's values mean nothing; its pixel
position ties the printed value to its line.
