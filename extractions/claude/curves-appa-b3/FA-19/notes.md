# FA-19, Figure A-19 (Density Versus Relative Density for RSM Soil), printed A-39, page image p0040.png

Reader: Claude (blind). Panel 1 only.

## The page differs from TASK.md

The unit-weight scale of this figure runs from **55 pcf at the top to 115 pcf at the bottom** (labels 55,
60, ... 115, on both sides), not 25 to 65 as TASK.md describes for the batch. It is still reciprocal and
still runs downward: the labelled lines sit within 8.5 px of their 1/value positions between the 55 and 115
frame lines, where a linear scale would misplace the middle labels by about 500 px. The Dr labels read 0.0, 0.1, ... 1.0. The title prints "RSM Soil"; `series.csv` names the
soil RSM-a (an index reading, kept as given).

## Calibration (cal-p1)

1. `calibrate_axes.py detect`, box 738 790 2340 3775, 10 bands, `--y-transform reciprocal --y-direction down`,
   x values 0 to 1.0 by 0.1, y values 55 to 111 by 1 and 115.
2. Unlabelled lines: four per 5 pcf interval in every interval, one per pcf; each within 7.2 px of its
   1/value position in its interval. Anchored 56 to 111 (except the labelled ones); 112 to 114 were not found
   by the detector and were left out. Their source names the convention.
3. The page is warped. The grid is not a parallelogram: the vertical lines lean 0.017 to 0.019 px per px
   except the right frame line (0.012), and the horizontal lines' slopes run from -0.011 to -0.014. The right
   frame line sits about 9 px farther right at the top than the regular Dr spacing would put it (last
   interval 160 to 163 px against about 154). All three data lines show the same bow against straight lines:
   about -2 px at the left, +1 px near Dr 0.25, -1 px at the right.
4. Residuals of the affine diagnostic: x rms 0.0013 (0.13 percent), **max 0.0071 (0.71 percent, above the 0.5
   percent of protocol section 2)**, at the top of the right frame line (x = 1.0, y 55 to 60); y (in q) rms
   0.09 percent, max 0.32 percent of the q span from 55 to 115. The x maximum comes from the drawing (the
   right frame's lean), not from detection: the frame line was found in 10 of 10 bands, is straight within
   1.2 px and lies within 1.1 px of the ink. A different box cannot remove it, so none was tried; the values
   come from the piecewise map, which follows each line's own position and tilt.
5. Ink check: 11 Dr lines and 57 unit-weight lines verified (ink at 25 of 25 positions, offsets within
   1.1 px). Rejected: the 115 bottom frame line (insufficient ink: the frame is too thick for the check's
   window); nothing is read below 76.
6. Label check by eye: `calibration-eye-checks.csv` (y: 55, 60, 65, 70, 75, 115 left; 55, 65, 70, 75 right;
   x: 0.0, 0.5, 1.0). The 1.0 label is printed 27 px left of the right frame line, 125 px right of the 0.9
   line: it belongs to the frame.
7. Sensitivity (in `work/`): labelled lines only, up to 0.050 pcf; affine map, up to 0.059 pcf; both below
   the trace bounds (0.06 to 0.13 pcf).

## Which label belongs to which line

No legend on the page; ids follow `series.csv` (solid = mean, dashed above = upper, dashed below = lower).
That the dashed lines are 95 percent confidence limits is not stated on this page.

| line | Dr = 0 label | leader | Dr = 1.0 label | leader |
|---|---|---|---|---|
| upper (dashed) | 57.3 | straight, v 1068, ends at u 731 just left of the frame where the upper line starts (v 1063 at the frame) | 65.1 | hooked, leaves the right frame at about v 1691 just below the upper line's end (v 1680, on the 65 line) |
| mean (solid) | 57.9 | straight, v 1120, ends at u 733 where the solid line starts (v 1114 at the frame centre, 1118 at its edge) | 70.3 | hooked, leaves the frame at about v 2028 just below the solid line's end (v 2024.5) |
| lower (dashed) | 58.5 | straight, v 1175, ends at u 741 where the lower line starts (v 1170 at the frame centre, 1176 at its edge) | 75.5 | hooked, leaves the frame at about v 2342 just below the lower line's end (v 2331) |

## The drawn ends against the printed values

| line | Dr = 0 read | printed | Dr = 1.0 read | printed |
|---|---|---|---|---|
| upper | 57.28 +- 0.06 | 57.3 | 65.05 +- 0.07 | 65.1 |
| mean | 57.82 +- 0.06 | 57.9 | 70.20 +- 0.08 | 70.3 |
| lower | 58.44 +- 0.07 | 58.5 | 75.45 +- 0.13 | 75.5 |

All within 0.1 pcf of the printed values (the mean's ends 0.08 and 0.10 pcf light, about one bound).

## Trace samples

1. Ink measured column by column (`helpers/trace_extract.py`, window 16 px, second pass); straight reference
   lines fit with rms 0.88 px (upper), 0.92 px (mean), 1.11 px (lower), larger than on the other figures
   because of the bow above. A sample's v is the reference line plus the median residual of the ink within
   40 px (20 px first at a line end, on the ink's side; all clean columns within 6 px of the line, so the
   bow is followed); half-edge columns at the mean's two ends and the upper's right end, where the line runs
   along a grid line.
2. Bounds: half the vertical thickness: upper 4.5 px (9 px), mean 4.5 px (9 px), lower 5.0 px (10 px; the
   lower line is the steepest).
3. Every Dr crossing lies under a vertical grid line; a sample there is on the trace when its ink reaches
   that grid line. No sample needed moving under rule 7.
4. Dashes ending or starting at a Dr grid line, kept at the crossing: upper Dr 0.6 (a dash starts at its
   right edge, u 1684; gap u 1665 to 1677 to its left); lower Dr 0.2 (the dash ends at its left edge, u
   1060), Dr 0.5 (a dash starts 3 px left of it, u about 1525), Dr 0.7 (the dash ends at its left edge,
   u 1843). Upper Dr 0.1 has a 3 px break in the ink at u 910 to 912, just right of the grid line; the
   sample is on ink to the left.
5. The upper line runs along the 65 grid line over its last 40 px and ends on it at the frame; its centre
   there is taken from its upper edge, which shows above the grid line. The solid line is unbroken. All three
   lines touch both frame lines.

## Flags in points-p1-native.csv

18 rows carry `extrapolated`: the 6 end samples and 6 first/last features sit on the Dr = 0 and 1.0 frame
lines, and the 6 label features are outside the frame. A label feature's values mean nothing; its pixel
position ties the printed value to its line.
