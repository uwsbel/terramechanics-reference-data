# FA-3, Figure A-3 (Density Versus Relative Density for RS Soil), printed A-7, page image p0008.png

Reader: Claude (blind). Panel 1 only.

## Calibration (cal-p1)

1. `calibrate_axes.py detect`, box 875 1835 2458 3388, 8 bands, `--y-transform reciprocal --y-direction down`,
   x values 0 to 1.0 by 0.1, y values 25 to 61 by 1 and 65.
2. The frame continues above the 25 line: two more horizontal lines and the top frame line (about 24, 23
   and 22 pcf, unlabelled). The box starts below them so that the 25 line is the first line of the list;
   nothing is plotted there.
3. Unlabelled lines: each 5 pcf interval holds exactly four lines, one per pcf. Between 25 and 30, where a
   1 pcf step and an even split differ by 11 to 18 px, the lines sit within 1.1 px of their 1/value
   positions, so they are 26 to 29 without doubt; the same count holds in every interval. They were anchored
   (26 to 34, 36 to 39, 41 to 44, 46 to 49, 51 to 54, 56 to 59, 61) and their source in `anchors.csv` and
   `calibration.json` names that convention. 62, 63 and 64 were not found by the detector (dense lines next
   to the thick bottom frame) and were left out; nothing is read below 55.
4. Residuals: x rms 0.0013 (0.13 percent of the span), max 0.0042 (0.42 percent); y (in q = 1/value)
   rms 0.14 percent, max 0.36 percent of the q span from 25 to 65. All under 0.5 percent.
5. Ink check (`piecewise --image`): all 11 Dr lines and all 38 unit-weight lines verified, ink found at
   25 of 25 positions on each, line-to-ink offsets within 0.75 px; none rejected (`cal-p1/knots-check.json`).
6. Label check by eye: `calibration-eye-checks.csv` (y: 25, 30, 40, 45, 55, 65 on the left and 25, 40, 55
   on the right; x: 0, 0.1, 0.5, 0.9, 1.0). Every label sits on its line or tick.
7. Drafting of the grid: against a smooth reciprocal fit through all 38 lines, the 45 line and the 30 line
   (both labelled, both heavier) sit 4.6 to 5.0 px lower on the page than their neighbours imply (44 and 46
   are within 1.7 px). Because the piecewise map uses every verified line, that misplacement affects values
   between 44 and 46 only. A map on the labelled lines alone spreads it over 40 to 50: it reads the trace
   samples up to 0.22 pcf lower there (larger than the trace bounds of 0.14 to 0.24 pcf); the affine map
   differs from the canonical values by up to 0.16 pcf. Both alternatives are kept in `work/`.

## Which label belongs to which line

The page prints no legend; the series ids follow `series.csv` (solid = mean, dashed above = upper,
dashed below = lower), which matches what is drawn: one solid line between two dashed lines. Whether the
dashed lines are 95 percent confidence limits (figures index) is not stated on this page.

| line | Dr = 0 label | leader | Dr = 1.0 label | leader |
|---|---|---|---|---|
| upper (dashed) | 40.1 | straight, meets the left frame at v 2799 where the upper line starts (v 2794) | 51.8 | straight, from u 2449 at v 3113 where the upper line ends (v 3113) |
| mean (solid) | 41.3 | straight, ends at u 889, v 2840, where the solid line starts (v 2838) | 52.9 | straight, from u 2456 at v 3147, where the solid line ends (v 3147) |
| lower (dashed) | 42.5 | hooked, its horizontal arm meets the frame at v 2879 where the lower line starts (v 2877) | 54.0 | hooked, its horizontal arm starts at u 2450, v 3169, where the lower line ends (v 3170) |

## The drawn ends against the printed values (a finding, not a reading problem)

Read on the canonical map, the drawn lines start and end at:

| line | Dr = 0 read | printed | Dr = 1.0 read | printed |
|---|---|---|---|---|
| upper | 40.32 +- 0.14 | 40.1 | 51.41 +- 0.24 | 51.8 |
| mean | 41.52 +- 0.13 | 41.3 | 52.77 +- 0.21 | 52.9 |
| lower | 42.65 +- 0.14 | 42.5 | 53.87 +- 0.24 | 54.0 |

Every drawn line starts 0.15 to 0.22 pcf denser and ends 0.13 to 0.39 pcf lighter than its printed end
value; the upper line's right end differs by 0.39 pcf, beyond its bound. The leaders point at the drawn
ends, so this is how the lines were drawn, not a mismatch of label and line. The printed values are the
report's numbers; the trace is the drawing.

## Trace samples

1. Each line's ink was measured column by column (`helpers/trace_extract.py`, second pass with the first fit as the guess): a run clear of the grid
   lines gives the centre; a robust straight line per series fits these with rms 0.58 px (upper, 499
   columns), 0.56 px (mean, 624) and 0.60 px (lower, 394). A sample's v is that line plus the median
   residual of the ink within 40 px (20 px first at a line end or a dash end, on the ink's side); where fewer
   than 8 clean columns exist there, columns where the line merges with a grid line on one side were added,
   their centre taken from the free edge and the series' thickness (mean Dr 1.0; upper Dr 0.3, 0.5, 0.9,
   1.0; lower Dr 0.5, 0.7, 1.0).
2. Bounds: half the line's vertical thickness: upper 4.5 px (9 px), mean 4.0 px (8 px), lower 4.0 px (8 px).
3. Every Dr crossing lies under a vertical grid line (its own ink, 5 px wide); a sample there is on the
   trace when the trace's ink reaches that grid line.
4. Gaps (rule 7), lower line only: Dr 0.2 falls in the gap u 1199 to 1224, moved to the dash end at u 1198
   (Dr 0.194); Dr 0.6 in the gap u 1807 to 1846, moved to u 1806 (Dr 0.589); Dr 0.9 in the gap u 2258 to
   2291, moved to the dash start at u 2292 (Dr 0.908).
5. Dashes ending or starting at a Dr grid line, kept at the crossing: upper Dr 0.2 (a dash starts at the
   line), 0.5 (a dash ends just right of it, u about 1668), 0.7 (ends at its left edge, u 1969), 0.9 (ends
   at its left edge, u 2277); lower Dr 0.1 (a dash starts at its right edge, u 1056). The ink under the
   grid line cannot be seen; the sample is within 3 px of the visible dash end.
6. The solid line is unbroken from frame to frame. All three lines touch both frame lines; first and last
   samples are at the frame lines.

## Flags in points-p1-native.csv

18 rows carry `extrapolated`: the 6 end samples and 6 first/last features sit on the Dr = 0 and 1.0 frame
lines (x within 4e-5 of 0 or 1), and the 6 label features are outside the frame. A label feature's x and y
values mean nothing; its pixel position is there to tie the printed value to its line.
