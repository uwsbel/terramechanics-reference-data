# FC-23, panel 1: reading notes (Claude reader, batch curves-appc-b11)

Figure C-23, "Angle of Internal Friction Versus Relative Density (From Direct Shear Test Results)",
printed page C-45/C-46, PDF page 159 (`p0159.png`, 300 dpi, unrotated, upright figure). One panel:
phi_DS (Degrees) against Dr. Six curves, each identified by a printed label, no plotted symbols.

## Calibration (`cal-p1/`)

1. `tools/calibrate_axes.py detect` on the box u 815..2620, v 1345..3570, which lies inside the
   frame so that the outermost grid lines found are the labelled ones (the frame lines are not
   labelled). 20 bands, dark 200, min-frac 0.5. x values 0, 0.1, ..., 1.0 (11 vertical lines), y
   values 30, 35, 40, 45, 50 (5 horizontal lines). Every line was detected (16 to 20 of 20 bands);
   no line is `predicted`. The same result came from 10 bands and from dark 160 / min-frac 0.6.
2. Affine residuals: x RMS 0.0023, max 0.0051 (0.51 percent of the 0 to 1.0 span, just above the
   0.5 percent mark); y RMS 0.039 deg, max 0.065 deg (0.32 percent of the 30 to 50 span). The x
   residual comes from uneven drafting of the vertical lines (149 to 160 px per 0.1 of Dr: 156,
   151, 154, 157, 160, 160, 149, 151, 153, 158), not from a misplaced line: the piecewise map
   reads the values between the drawn lines, so it does not affect the data.
3. Ink check of every line (`cal-p1/knots-check.json`, made with the unmodified
   `calibrate_axes.py` functions): all 16 lines verified, ink found at 12/12 positions on each
   vertical line and 22 to 25 of 25 on each horizontal line; location errors 0.5 to 2.0 px.
4. By-eye label check (`calibration-eye-checks.csv`): all 11 x labels and all 5 y labels were
   checked against the line each belongs to. Every label sits under (x) or beside (y) its own line
   within 9 px, with lines 150 px (x) and 380 px (y) apart, so no label is ambiguous. Two labels
   sit a little off their lines: "0.3" is 8.5 px right of its line, and "35" is printed about
   7 px above its line.
5. The 50 deg line is faint and missing between about u 2210 and 2335 (the fitted straight line
   crosses that stretch); it still passed the ink check.
6. Scan tilt: vertical lines lean about +0.008 px/px (u grows downward), horizontal lines about
   -0.008 px/px; each line keeps its own tilt in the piecewise map.

### Frame beyond the labelled lines

The frame is not a labelled line and is not a knot. Located on rows and columns and converted with
the piecewise map (extrapolated): left frame at Dr about -0.10 (u about 792 at v 2450), right frame
at Dr about 1.10 (u about 2653 at v 1700), top frame at about 55.1 deg (v about 1311 at u 1700),
bottom frame at about 25.0 deg (v about 3600 at u 1700). The frame lines are about 11 px thick.
So the plot runs 0.1 of Dr beyond 0 and 1.0 on each side, and 5 deg beyond 30 and 50, with no
labels there. Values outside 0 to 1.0 in Dr and outside 30 to 50 deg are extrapolated from the
outermost verified lines and are flagged in `cal_model` of `points-p1-native.csv` (49 of 160 rows,
mostly the ends at Dr just below 0 or above 1.0, RC2 and RSM-b above 50 deg, SS below 30 deg).

Unused marks: two short horizontal strokes left of the y axis at v about 2359 and 2757 (between
the 40 and 45 labels and between the 35 and 40 labels) are not at any printed value and carry no
label; they were not used. Short horizontal specks inside the plot (for example near (846, 2543),
(1005, 2585), (1355, 2267), (1815, 2275)) belong to no curve and were not traced.

## Which curve is which

Identity is from the printed label next to each curve and from the line style, which is constant
along each curve (dash lengths measured column by column):

1. `rc2`, label "RC2": solid line. Label above the line near Dr 0.45. From Dr -0.015 (42.70 deg)
   to Dr 1.014 (53.05 deg), the topmost curve from Dr 0.10 on.
2. `ps`, label "PS": short dashes, about 22 px long with gaps of about 12 px. Label above the line
   near Dr 0.46. From Dr -0.016 (42.85 deg) to the right frame at Dr 1.10 (49.17 deg).
3. `rs`, label "RS": medium dashes, about 40 px long with gaps of 13 to 24 px. Label above the
   line near Dr 0.27. From the left frame at Dr -0.10 (39.00 deg) to Dr 1.098 (49.73 deg), its last
   dash ending about 3 px short of the right frame.
4. `rsm-b`, label "RSM-b": a long dash (about 95 to 135 px) followed by two short dashes (about
   25 px), gaps about 11 px. Label above the line near Dr 0.17; the letters "R" and "S" touch the
   40 deg grid line and come within a few px of the line. From Dr -0.010 (38.21 deg) to Dr 1.009
   (51.07 deg).
5. `rsm-a`, label "RSM-a": very long dashes (about 250 to 290 px) alternating with dashes of about
   50 px, gaps 13 to 37 px. Label above the line near Dr 0.54. From Dr -0.012 (36.77 deg) to the
   right frame at Dr 1.10 (46.94 deg).
6. `ss`, label "SS": solid line, S-shaped (steepest near Dr 0.45). Label left of the steep part
   near Dr 0.54. From Dr -0.009 (29.08 deg) to Dr 1.012 (41.36 deg). The ink is nearly broken
   (two thin runs of 3 and 4 px) where it crosses the Dr 1.0 grid line, and continues about 18 px
   beyond it.

The printed labels agree with `series.csv` (RC2, PS, RS, RSM-b, RSM-a, SS); no id was changed.

RC2, RSM-b and SS end 15 to 25 px right of the Dr 1.0 line (Dr about 1.01); PS, RS and RSM-a run on
to the right frame (Dr about 1.10). All curves except RS start 15 to 25 px left of the Dr 0 line
(Dr about -0.01); RS starts at the left frame (Dr about -0.10).

## Where curves cross or touch

1. RC2 and PS start together (PS 42.85 deg just above RC2 42.70 deg, about 11 px apart) and their
   ink touches or overlaps from Dr 0.03 to 0.14 (u 1000 to 1160). They cross near u 1094, v 2213
   (Dr 0.096, 43.25 deg): PS is above RC2 to the left of that point and below it to the right.
2. RS and RSM-b: their ink joins from Dr 0.56 to 0.62 (u 1814 to 1906). RSM-b crosses RS from below
   near u 1850, v 2024 (Dr 0.58, 45.61 deg), inside a gap of RS (RS has no ink from u 1835 to 1865;
   the single 10 px run there has RSM-b's slope, -0.75, not RS's, -0.44).
3. RSM-b and PS cross near u 1984, v 1931 (Dr 0.67, 46.83 deg); a short dash of each overlaps the
   other between u 1964 and 1998.
4. RS and PS cross near u 2430, v 1801 (Dr 0.96, 48.50 deg). Between u 2405 and 2468 (Dr 0.94 to
   0.98) their ink forms one 10 to 12 px band that cannot be split: the band's edges follow PS's
   slope at its left end, and RS's dash (about u 2417 to 2458) lies inside it. RS is below PS to the
   left of the crossing and above it to the right, up to the frame.
5. RSM-a and SS touch no other curve. RC2 touches no other curve after Dr 0.15.

## How the traces were read

1. Each curve was measured column by column (`helpers/measure.py`) along a guide polyline that I
   wrote from the ink pieces and the column runs (`helpers/guides.json`); the guide only says which
   run belongs to which curve. In a clean column the centre of the run is the line's centre. Where
   another curve or a horizontal grid line joins the run, the centre is taken from the edge on the
   curve's own side (edge plus half the line's vertical thickness) with a wider bound; where two
   curves coincide, the centre of the joint ink.
2. Samples (`helpers/sample.py`): the left end, every 0.05 of Dr, the right end, in drawing order.
   The sample column is where the piecewise x value equals the target at the curve's height. The
   samples at Dr 0, 0.1, ..., 1.0 fall on a vertical grid line; where the curve's ink runs through
   the grid line, the centre there is the straight line through the curve's ink within 15 px on
   both sides. Ends are where the ink starts and ends (the first and last column with a run of 4 px
   or more), with the centre from the 10 columns inward.
3. Rule 7 moves (sample in a gap, moved to the nearest dash end on the ink): PS Dr 0 (-4 px), 0.05
   (+2), 0.6 (-4), 0.65 (-3), 0.7 (-4), 0.8 (-4), 0.85 (-2), 0.9 (+4); RS Dr 0.05 (-7), 0.25 (+1),
   0.4 (+4), 0.5 (-8), 0.7 (-4), 0.75 (+5), 0.9 (-4), 0.95 (+3); RSM-b Dr 0.1 (-4), 0.5 (-4),
   0.55 (-3); RSM-a Dr 0.7 (+5). The note of each sample says how it was placed.
4. Bounds: u 4 px (half the 8 px line thickness across the line); v half the line's vertical run
   in that column, never less than half the line's vertical thickness (4 to 7 px), and wider
   where the centre comes from an edge of joined ink. In data units the y bounds are 0.07 to 0.12
   deg and the x bounds about 0.003 to 0.004.
5. Samples that rest on joined ink and deserve a look: RC2 and PS at Dr 0.1 (same point, the two
   lines coincide at the 0.1 line); PS at Dr 0.05 (dash start on top of RC2); RS and RSM-b at Dr 0.6
   (joined ink, RS from the bottom edge, RSM-b from the top edge, 8 px apart); RS at Dr 0.95 and PS
   at Dr 0.95 and 1.0 (inside or next to the RS and PS band of item 4 above).

## Features

Per curve: sequence 1 the first point (left end), 2 the last point (right end), 3 the label centre
("label: <printed text>", the middle of the text's bounding box, bound 5 px). Each curve rises
monotonically, so its maximum is its last point; no separate peak row. No curve has a knee or kink;
SS has an inflection (steepest stretch) near Dr 0.45, which is not a kink.

## Files

1. `cal-p1/calibration.json`, `cal-p1/anchors.csv` (55 grid intersections), `cal-p1/knots-check.json`.
2. `calibration-eye-checks.csv`.
3. `points-p1.csv` (160 rows: 142 trace, 18 feature) and `points-p1-native.csv` (piecewise map,
   `tools/calibrate_axes.py piecewise --image`).
4. `overlay-p1.png`.
5. Working files: `helpers/` (the reading scripts and guides), `tracks/` (per-column
   measurements), `samples/` (sample records), `crops/` (zoomed crops used to read).
