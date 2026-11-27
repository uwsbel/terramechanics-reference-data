# FA-39, panel 1: reading notes (Claude, blind)

Page `p0078.png`, printed A-77, "Figure A-39. Density versus Relative Density for LSM Soil".

## What the page prints

1. The unit-weight axis runs downward from **55 at the top to 115 at the bottom** (labels every 5
   on both sides, left "Minimum Density, gamma min (pcf)", right "Maximum Density, gamma max (pcf)").
   TASK.md describes the density charts as 25 to 65 pcf; this figure is not. Spacing reciprocal,
   so `--y-transform reciprocal --y-direction down` with the printed values.
2. Four light lines between every two labelled (heavy) lines, one per pcf, from 55 to 115. Dr 0.0
   to 1.0, a vertical line every 0.1, each labelled.
3. Three straight lines: a solid one between two dashed ones, as `series.csv` says.

## Calibration (`cal-p1/`)

1. Box u 850 to 2280, v 1826 to 3188: the data region, from the 65 line to the 95 line, with every
   1 pcf line anchored (65, 66, ... 95) and the 11 Dr lines; the same rule as the other figures of
   this batch that I read (all named lines in the data region, so that every value is between two
   drawn lines). All 31 + 11 lines detected in 10/10 bands and verified against the ink (25/25
   positions each, location errors 0.5 to 1.13 px). Affine diagnostic: x rms 1.02 px (0.07 % of
   span), max 2.19 px; y rms 1.84 px (0.14 %), max 4.6 px (0.35 %).
2. Each light line's value is named by count (four light lines between every two labels, 1 pcf
   apart, over the whole chart).
3. Sensitivity (`helpers/cal-labelled-only`, the full frame with the 13 labelled lines, all verified
   including the 115 frame): it changes no value by more than 0.15 pcf (largest at the upper line's
   right end, 88.22 against 88.37, and at the mean line's Dr 0.9).
4. By-eye label checks in `calibration-eye-checks.csv`: y labels 65, 75, 85, 95 within 4 px of their
   lines (ticks on the lines); x labels 0.0 (2 px), 0.5 (9 px left of its line), 1.0 (26 px left of
   the right frame, which is the eleventh line and so 1.0 by count).

## Which label belongs to which line

| series | drawn | left end (Dr 0) | right end (Dr 1.0) |
|---|---|---|---|
| upper | dashed, above | 66.6 | 88.1 |
| mean | solid | 67.8 | 90.2 |
| lower | dashed, below | 69.0 | 92.3 |

Each left leader ends at the frame where its line starts (66.6 at v 1937, 67.8 at v 2009, 69.0 at
v 2084; the lines meet the frame at v 1935, 2008, 2084). Each right leader starts just outside the
frame at the level of its line's end (88.1 at v 2946, 90.2 at v 3024, drawn through the right-axis
label 90; 92.3 at v 3088).

## The drawn ends against the printed values

Read with `cal-p1` (bounds 0.08 to 0.15 pcf):

| series | Dr 0 read | printed | Dr 1.0 read | printed |
|---|---|---|---|---|
| upper | 66.49 | 66.6 | 88.37 | 88.1 |
| mean | 67.68 | 67.8 | 90.42 | 90.2 |
| lower | 68.95 | 69.0 | 92.40 | 92.3 |

The drawn lines start 0.05 to 0.12 pcf lighter and end 0.10 to 0.27 pcf heavier than their printed
values; the upper line's right end is about 9 px (0.27 pcf) below where 88.1 would be, and its
leader is drawn at the same level as the line's end, so this is how the line was drafted, not a
misreading of which line or which grid line (checked on `crops/crop-right.png`: the end sits
between the 88 and 89 lines, a third of the way down). The labelled-only map gives the same
picture (88.22, 90.43, 92.42). The readings report the ink, as drawn.

## How the samples were taken

1. Each line is close to straight but all three bow the same way: from a straight-line fit their
   ink sits about 3 px above at the left end, 1.5 to 1.8 px below in the middle and 0.6 px above at
   the right end (common to the three lines, so the page or the drafting, not the reading). Each
   sample's centre is the straight fit plus the median residual of the clean ink within 50 px, so it
   follows the ink. Vertical thickness 7.5 to 8 px, bound 4 px in u and v; label features 5 px.
2. Dr 0.1 to 0.9: the line's crossing with the Dr grid line. Every crossing is on ink except the
   upper line at Dr 0.7, which falls in a dash gap (u 1838 to 1854, the grid line inside it) and was
   moved to the nearest dash end (u 1837, 7 px away; the next dash starts 11 px away). The upper
   line at Dr 0.3 and 0.9 is on the very end of a dash that runs just past the grid line (to u 1288
   and 2125).
3. Ends: every line runs into the frame; the end samples (and the first/last point features) are on
   the frame lines' centres (Dr 0 and 1.0). The first visible ink is at the frame's inner edge, 5 to
   6 px inside.
4. Labels: one feature per printed end label, at the centre of its characters.

## Ambiguities

1. Upper line, Dr 0.7: a small dark bump on the left edge of the 0.7 grid line, on the line's path
   (u 1841, 3 px tall), is read as part of the grid line, not as dash ink.
2. Nothing else: the dashes are long (80 to 150 px) and well separated from the grid crossings.

## Counts

Per series: 11 trace samples and 4 features (first point, last point, two labels). 45 points.

## Files

`cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv` (piecewise map
with `--image`), `overlay-p1.png`, `crops/`, `helpers/` (scripts, the labelled-only calibration and
`points-p1-native-labelled.csv`).
