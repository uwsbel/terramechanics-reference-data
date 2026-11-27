# FA-46, blind reading (Claude), batch curves-appa-b2

Page `p0095.png` (printed A-94, PDF 95), Figure A-46 "Average and Range of Sample of Unused RSM-b Soil".
The page is bilevel (0/255) and the plot is printed sideways: grain size increases up the page (v down = finer),
percent finer increases to the left (u left = more). One panel.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect --box 712 1151 2205 3755 --x-transform log10 --x-direction up --y-direction left
   --bands 8 --snap 7`, x values 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 9.0 (the labelled
   grain-size lines), y values 0 to 100 by 10. All 23 lines detected, none predicted. Residuals: x rms 0.0026,
   max 0.0064 (log10 units, 0.24 percent of the 2.65-decade span); y rms 0.082, max 0.30 percent finer.
2. The box top (v 1151) leaves out the top frame (v 1117), which carries no label (10 mm by log spacing), and the
   dashed 3/8 in. sieve line (9.5 mm, v 1141). The label "9.0" belongs to the thick line at v 1158 to 1165. The
   bottom frame is the labelled 0.02 line; the labels 0.05 and 0.02 are printed about 16 to 18 px below their
   lines (on the finer side), which log spacing (970 px per decade) confirms. Left frame = 100, right frame = 0,
   both labelled. Details in `calibration-eye-checks.csv` (all 12 grain-size labels and all 11 percent labels).
3. `--snap 7` (default 10) was needed: with 10, the 0.1 mm line picked up the parameter table's Average|Range
   column rule (v 3070) in the three bands under the table and got the wrong tilt.
4. The piecewise ink check (D-025) rejects two lines although both are on the ink where they are visible:
   x = 0.1 (its check positions under the parameter table find the table rule 5.5 to 6 px away; outside the table
   the offsets are within 0.9 px) and y = 60 (one check position inside the table, at v 3554, sits on table text
   5.9 px away). Values between 0.05 and 0.2 mm and between 50 and 70 percent are therefore interpolated across
   the gap; the effect is well under a pixel because the grid is regular there. `calibrate_axes.py recover`
   gives a good y = 60 line (23 points, rms 0.65 px, u 1305.5 to 1314) but for x = 0.1 it locks onto the
   unlabelled 0.09 mm line at v 3103: do not use that recovery for 0.1.
5. `points-p1-native.csv` is from `calibrate_axes.py piecewise --image`; the affine map (`points-p1-affine.csv`,
   kept for comparison) differs by at most 0.0028 in log10 x and 0.09 percent in y.

## Which curve is which

Three curves, drawn with the same pen width (about 10 to 11 px across the stroke): the solid one is `average`
(B); the two dashed ones are `upper` (A, more percent finer at a given size: left of B in a row, below B in a
column) and `lower` (C, right of / above B). Dash period about 62 px along the curve, gaps about 14 px. Where a
dash gap crosses a printed grid line, the grid line is white too (the gaps look erased), which helped locate
gaps hidden in grid lines. The order A, B, C never changes.

1. Fine part (0.074 to about 0.6 mm, nearly vertical on the page): the three strokes lie side by side and
   touch, A at about 2.0 to 2.4 percent, B 1.3 to 1.7, C 0.7 to 1.1; C also touches the 0 percent frame below
   about 0.2 mm. B is located from its own edges where a neighbour is in a gap; A from its outer (left) edge; C
   from its right edge where a white channel separates it from the frame, otherwise one stroke width from B
   (wider bound, noted).
2. Knee (0.6 to 1.3 mm): A runs as a separate stroke; B and C are merged into one double-width stroke (about 19
   px across, two strokes); B is read as its left half, C as its right half.
3. Steep and flat parts (1.3 to 3 mm, 5 to 95 percent): the three strokes touch and form one band about 33 to 46
   px tall in a column. A (bottom edge) and C (top edge) are read from the band edges, B from the middle or from
   its own edge where A or C is in a gap; the band crosses the 1.5, 2.0 and 2.5 mm grid lines and the #8 and #12
   sieve lines at shallow angles, so several samples sit under grid ink (noted, bound 7 px). The curves run
   together here: the bound is widened to 7 px rather than guessing beyond what the band edges show.
4. Coarse end (above about 3 mm): the curves bend up to 100 percent near the left frame. A reaches the frame
   first and continues as a dashed line on or just outside the frame line (u 712 to 722, i.e. 100.4 to 100.6
   percent as read) up to just below the #4 sieve line (v 1453); B merges into the frame at about v 1501 (4.1 mm);
   C can be separated from B only up to v 1553 (3.6 mm), above which it cannot be told from B and the frame.
   Whether B and C also continue along the frame to the #4 sieve cannot be seen (they would lie on the frame line).
5. Fine end: all three curves start at the dashed #200 sieve line (0.074 mm, v 3184 to 3191), which merges with
   their ends; first points are put at v 3186 with a 5 px v bound.

## Samples

Trace samples follow TASK.md: first point, every 0.05 decade (0.0796 ... 3.99 or 4.48 mm), plus 5 percent
samples where a curve rises more than 10 percent between two of those (A: 35 to 85, B: 30 to 95, C: 40 to 90),
then the last point. Samples whose crossing falls in a dash gap are moved to the nearest dash end (note "moved").
Bounds: 5.5 px where the stroke is read cleanly, 7 px where strokes merge or a grid line covers the stroke,
8 px on and beside the 100 percent frame. Features per curve: first point, lower knee (about 0.8 mm), upper knee
(at the 2.83 mm sample), last point (the curves are monotonic, so the peak is the last point). No plotted symbols,
so no markers.

Sanity check, not used to set any value: the printed parameter table gives D50 2.15 (range 2.1 to 2.2), D10
1.23 (1.2 to 1.3), Cu 1.87, D95 2.9; this reading gives D50 2.17 (A 2.14, C 2.22), D10 1.21 (A 1.16, C 1.27),
D60/D10 1.88, D95 2.79 (A 2.76, C 2.85). D95 comes out about 0.1 mm below the printed 2.9; D10 of A slightly
below the printed range. Either the table was taken from the data rather than the drawn curve, or this reading
of the 95 percent region (coarse bend, merged strokes) is low by a few pixels; worth a look in review.

## Things to look at in review

1. The 2.0 mm grid line (v 1796 to 1810) hides B and A for u 1540 to 1670 (35 to 45 percent); the x = 2.0 samples
   of all three curves are under it.
2. The k = 0.0796 to 0.14 mm samples of C rely on C sitting one stroke width right of B (it merges with the 0
   percent frame there).
3. Coarse end identities (item 4 above), especially C above v 1553 and the dashed line outside the frame, which is
   read as A (it could equally be both dashed curves at 100 percent).
4. Helpers written for this reading are in this folder (`ascii.py`, `insp.py`, `colsum.py`, `fine_measure.py`,
   `env2.py`, `centers_col.py`, `assemble.py` and others); `assemble.py` holds every read pixel position with its
   note.
