# FA-27, panel 1: reading notes (Claude, blind)

Page `p0055.png`, printed A-54, "Figure A-27. Density Versus Relative Density for SS Soil".

## What the page prints

1. The unit-weight axis runs downward from **55 at the top to 115 at the bottom** (labels 55, 60, ...
   115 on both sides, left "Minimum Density, gamma min (pcf)", right "Maximum Density, gamma max
   (pcf)"). TASK.md describes the density charts as 25 to 65 pcf; this figure is not. The spacing is
   reciprocal (checked: the labelled lines sit within 7 px of an even division in 1/gamma between
   the frames), so `--y-transform reciprocal --y-direction down` with the printed values.
2. Between every two labelled (heavy) lines there are four light lines, one per pcf, all the way
   from 55 to 115. Dr runs 0.0 to 1.0 with a vertical line every 0.1, each labelled.
3. Three straight lines, as `series.csv` says: a solid one between two dashed ones.

## Calibration (`cal-p1/`)

1. Box u 650 to 2235, v 3122 to 3680: the data region, from the 95 line to the 114 line, with every
   1 pcf line anchored (95, 96, ... 114) and the 11 Dr lines. All 20 + 11 lines detected in 10/10
   bands and all verified against the ink by the piecewise tool (25/25 positions each, location
   errors 0.5 to 1.45 px). Affine diagnostic: x rms 1.06 px (0.07 % of span), max 2.67 px; y rms 2.2
   px, max 5.1 px (0.96 % of the 95 to 114 span, 0.18 % of the printed 55 to 115 span).
2. Why the light lines and why this box, decided before reading values and then confirmed:
   - the bottom frame (115) is 12 to 15 px thick and fails the tool's ink check (core found at 5 of
     25 positions), so it cannot be a knot; with only the labelled lines every value below 110 (all
     three right ends) is extrapolated from the 105 to 110 interval;
   - the light lines are not where an even division between the heavy lines puts them: the heavy
     labelled lines sit 3 to 4 px low relative to the light-line lattice (95 to 100), and 111 to 114
     sit 6 to 9 px above the positions a reciprocal division between the 110 and 115 line centres
     gives. Reading "as drawn" (D-025) needs them as knots;
   - each light line's value is named without doubt by count (four light lines between every two
     labels, 1 pcf apart, over the whole chart);
   - the tool's evenly-in-1/gamma prediction misses 111 to 114 by more than its quarter-spacing
     window when the frame is 55 to 115 (they come out `predicted`, not knots); between 95 and 114
     every line is matched.
3. Sensitivity, kept under `helpers/`: `cal-labelled-only` (full frame, labelled lines only: 11 x and
   12 y lines verified, 115 rejected) gives values lower by 0.10 to 0.16 pcf at Dr 0.1 to 0.2 and by
   up to 0.49 pcf at the right ends, where it extrapolates (mean line at Dr 1.0: 112.10 against
   112.59). `cal-all-lines-full-frame` (55 to 115, every line) verifies 55 to 110 and leaves 111 to
   114 predicted. The printed end labels favour `cal-p1` (next section).
4. By-eye label checks in `calibration-eye-checks.csv`: y labels 95, 100, 105, 110 sit within 4 px
   of their lines (ticks on the lines); x labels 0.0 (1 px), 0.5 (10 px left of its line), 1.0 (26 px
   left of the right frame, which is the eleventh line and so 1.0 by count).

## Which label belongs to which line

| series | drawn | left end (Dr 0) | right end (Dr 1.0) |
|---|---|---|---|
| upper | dashed, above | no label of its own; it starts on the 95 line (axis label 95, no leader) | 110.5 |
| mean | solid | 95.4 | 112.7 |
| lower | dashed, below | 95.8 | 114.9 |

Evidence: the 95.4 leader ends at u 675, v 3152 to 3155, on the mean line's extension (mean 3152,
lower 3159, upper 3139 there); the 95.8 leader ends at v 3165 to 3168, nearest the lower line. On the
right the 110.5 and 112.7 leaders start just outside the frame on the extensions of the upper and
mean lines (within 1 px); the 114.9 leader starts behind the right-axis label 115 and points back to
the lower line's end. The lines have increasing slopes from top to bottom and do not cross, so the
order is the same at both ends.

Values at the ends with `cal-p1` against the printed labels (all within the read bounds, 0.15 to
0.25 pcf): upper 95.07 / 110.59 (110.5); mean 95.51 (95.4) / 112.59 (112.7); lower 95.76 (95.8) /
114.81 (114.9). With the labelled-only map the right ends read 110.43, 112.10, 114.42, that is 0.6
and 0.5 pcf below the printed 112.7 and 114.9.

## How the samples were taken

1. Each line is a ruled straight line (straight-line fit to its grid-free ink: rms 0.6 to 0.7 px;
   every 100 px stretch within 1.1 px of it except the first, where the lines merge, 1.5 px). A sample's
   centre is the fit plus the median residual of the clean ink within 50 px. Vertical thickness 8 px,
   bound 4 px (half the thickness) in u and v; label features 5 px.
2. Dr 0.1 to 0.9: the line's crossing with the Dr grid line where the dash covers it. On the dashed
   lines, where the crossing is in a gap the sample moved to the nearest dash end; where a dash end
   is hidden under the grid line (white on one side, ink on the other) the sample is on the first or
   last visible ink beside the grid line (rule 7). Each case is in the sample's note: upper Dr 0.3,
   0.4, 0.5, 0.6, 0.8 and lower Dr 0.3, 0.4, 0.5, 0.6, 0.7 are moved; the rest are crossings.
3. Ends: every line meets the frame; the end samples (and the first/last point features) are on the
   frame lines' centres (Dr 0 and 1.0), where each line's ink runs into the frame. Its first visible
   ink is at the frame's inner edge, 5 to 6 px inside.
4. Labels: one feature per printed end label, at the centre of the label's characters.

## Ambiguities

1. Upper line, Dr 0.6: the crossing is almost midway in its gap (13 px to the end of the previous
   dash, 15 px to the start of the next); the sample is on the nearer one (u 1596). The other end lies
   28 px further along the line (about 0.18 in Dr and 0.3 pcf), equally on the ink.
2. Near Dr 0.8 a thin white streak (scan defect) cuts the grid lines, the mean and the lower line at
   u 1898 to 1903 and the upper line at u 1907 to 1909. It is not a dash gap. The mean line is solid
   everywhere; an automatic gap at u 1509 to 1516 is the line running exactly along the 104 grid line.
3. Left end: the mean and lower lines are 6 px apart at the frame and overlap; their centres there
   come from the clean ink 30 to 100 px to the right. The upper line merges with the 95 grid line
   for its first 25 px.
4. The upper line has no printed Dr 0 value. It reads 95.07 on the page; by symmetry with the mean
   (95.4 +- 0.4) it was probably meant to be 95.0, but that is not printed.

## Counts

Per series: 11 trace samples; features: upper 3 (first point, last point, label 110.5), mean 4 and
lower 4 (first, last, two labels). 44 points in all.

## Files

`cal-p1/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv` (piecewise map with `--image`), `overlay-p1.png`, `crops/` (zoomed crops),
`helpers/` (the scripts and their outputs, the two sensitivity calibrations,
`points-p1-native-labelled.csv` with the labelled-only map).
