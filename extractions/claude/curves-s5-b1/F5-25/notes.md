# F5-25, batch curves-s5-b1, Claude reading (reader A)

Figure 5-25, "Strut Axial Load versus Time (NASA Test No. 1)", printed page 5-50, PDF page 330
(`packet/p0330.png`, 300 dpi). The figure is printed sideways: turned 90 degrees clockwise it reads
upright, with time to the right and load upward. All pixel coordinates are those of the unrotated page
image (u right, v down). On the page, time increases upward (t = 0 at v about 3528, t = 0.10 at v about
1820) and the three panels sit side by side: panel 1 (top when upright) at u 990 to 1250, panel 2 at u
1420 to 1675, panel 3 at u 1845 to 2271.

Native units are the printed ones: seconds and pounds (lb). Conversion to SI (1 lbf = 4.4482216152605 N)
is left to the downstream tool, as the protocol requires.

## Series and what is printed

| panel (upright, top down) | series id (given) | axis title as printed | trace |
|---|---|---|---|
| 1 | strut3 | "(Tension)" / "Load on Strut No. 3" (no unit printed in this title) | one solid line |
| 2 | strut2 | "(Tension)" / "Load on Strut No. 2 (lbs.)" | one solid line |
| 3 | strut1 | "(Compression)" / "Load on Strut No. 1 (lbs.)" | one solid line |

Time axis title: "Time - Seconds". The ids of `series.csv` agree with the page.

## Labels as printed, and the slips

Every label is in `calibration-eye-checks.csv` with its line, the line's fitted position at the label
and the label's measured center.

1. Panel 1 load labels: `+60`, `+40`, `+20`, `0`. The `+40` is printed about 5 px toward +60 from its
   line (spacing 86 px), still unambiguous. The `+20` has an incomplete plus (read upright, the lower
   half of its vertical stroke is missing), so at low zoom it can pass for `-20`; at zoom 8 it is a
   damaged plus, and +20 is what the sequence gives either way.
2. Panel 2 load labels: `-60`, `+40`, `+20`, `0`. **Slip:** the outermost label carries a minus sign (a
   bare bar, unlike the full plus of the two labels beside it). The sequence 0, +20, +40 and the
   (Tension) title make it +60; the line is anchored at **+60**.
3. Panel 3 load labels: `-100`, `-80`, `-60`, `-40`, `-20`, `0`. All consistent. Values are recorded
   as printed (negative for compression), as the task requires.
4. Time labels (printed once, right of panel 3, for all panels): `0`, `.01`, `.02`, `.03`, `.04`,
   `.05`, `.06`, `.07`, `.08`, (damaged), `.10`. **The `.09` label is damaged:** only fragments are
   printed (a small hook, a curved stroke and the decimal point at u 2316 to 2323, v 1983 to 2018). Its
   line is drawn (dashes at u 747 to 809 and 2208 to 2239) one spacing above .08 and below .10; it is
   anchored at **0.09** from the sequence.
5. Unlabeled lines, not used as knots: panel 1 has drawn load lines at u 907 and 825 and the left frame
   at u 738 (+80, +100, +120 by the spacing). Panel 2's left boundary is panel 1's 0 line (+100 by the
   spacing; no +80 line is drawn), and panel 3's left boundary is panel 2's 0 line (-140 by the spacing;
   no -120 line is drawn). Panel 3's 0 line is the figure's right frame (6 px thick). The load lines of
   panels 2 and 3 stop at the t = 0.10 line; the frame continues above it around the inset.

## Inset and the drop's conditions (not points)

At the right of the figure (above t = 0.10 on the page) an inset shows the model in plan: an X-shaped
body with four circular footpads, circled instrument callout numbers, axis arrows labeled `-Y` (with
`Vh`) and `-Z`, and four boxed callouts: "Strut No. 2 / Axial Load / No. 2", "No. 1 Footpad",
"Strut No. 1 / Axial Load No. 1", "Strut No. 3 / Axial Load No. 3". The conditions are printed as two
lines:

> Vv = -114.93 in. sec.  Vh = 0
> RS Loose  Level Surface

(V with subscripts v and h; the two "=" print as filled blobs; "in. sec." stands for in./sec.)
Table 5-T3 on the context page (PDF 325, printed 5-45) lists NASA Test No. 1 (Bendix drop 10) with Vv
-114.9 in./sec., Vh 0, RS Loose, Dr 0, 46.9 lb/ft3, phi 41 deg; the inset gives Vv to one more digit
(-114.93). The figures index row says "VV -114.9 in/s, VH 0 (T5-3)", consistent with the table.

## Calibration (cal-p1, cal-p2, cal-p3)

Why a helper and not `calibrate_axes.py detect`: the time lines are dash-dot lines drawn only at the
left of panel 1 (u 738 to 965), as short segments at the right of panel 3 (u 2190 to 2268) and, for
t = 0.01, as dashes across part of panel 3; inside panels 1 and 2 they are absent. `detect` finds lines
in bands across a box and would only predict them. The helpers (`helpers/measure_lines.py`,
`helpers/time_anchors.py`, `helpers/build_cal.py`) measure every line on the ink where it is drawn
and write the same `calibration.json` layout (with `box`) and an `anchors.csv` whose rows are the
measured ink points, one axis per row (the other value blank). Each time line is one straight line
across the whole figure, fitted to its dashes at both ends (a baseline of about 1500 px for its tilt);
each load line is measured in 40 or 60 px bands along its full length. The baseline (t = 0, the bottom
frame) is slightly bent (v 3525 under panel 1, 3531.5 under panel 3), so each panel uses the stretch
of it under that panel.

Knots (all printed and labeled lines, every one verified on the ink by the tool's own check,
`piecewise_maps` with the page image; `cal-p<n>/knots.json`): time 0, .01, ..., .10 (11 lines) in each
panel; load 0, +20, +40, +60 in panels 1 and 2; 0, -20, ..., -100 in panel 3. No line rejected, none
predicted. Line location errors 0.5 to 0.95 px, except t = 0.10 at 1.5 px (its short right-hand
segment carries the end of panel 3's trace, which pulls the ink check by 1.1 px).

Affine diagnostic (intersections of the fitted lines inside each panel):

| panel | s per px | RMS / max residual, time | lb per px | RMS / max residual, load |
|---|---|---|---|---|
| 1 | 5.86e-5 | 4.8e-5 / 9.4e-5 s (0.09 % of 0.10 s) | 0.2337 | 0.12 / 0.25 lb (0.41 % of 60 lb) |
| 2 | 5.86e-5 | 4.4e-5 / 8.3e-5 s (0.08 %) | 0.2356 | 0.19 / 0.28 lb (0.46 % of 60 lb) |
| 3 | 5.86e-5 | 4.4e-5 / 8.9e-5 s (0.09 %) | 0.2343 | 0.12 / 0.20 lb (0.20 % of 100 lb) |

All under 0.5 percent of the span. Panel 2's +60 line sits 83 px from +40 against 85.5 px for the other
intervals, which is most of its residual; the piecewise map reads it as drawn. The affine and piecewise
values of the points differ by at most 0.00009 s and 0.27 lb.

The grid is slightly skewed: time lines run down to the right (dv/du +0.0045 to +0.0074, the spread
being a 0.35 percent difference of the time scale between the left and right ends of the figure), load
lines lean the other way (du/dv -0.0018 to -0.0034). Each knot keeps its own tilt.

## Points

Files: `points-p<n>.csv` (reader columns) and `points-p<n>-native.csv` (the tool's `piecewise` with
`--image`).

| panel | series | trace samples | of which time / 5 lb / ink ends | features |
|---|---|---|---|---|
| 1 | strut3 | 42 | 25 / 15 / 2 | 6 |
| 2 | strut2 | 40 | 25 / 13 / 2 | 7 |
| 3 | strut1 | 58 | 25 / 31 / 2 | 6 |

How the samples were placed: a dense center line of each trace was measured from the ink, as the
midpoint of the trace's chord along lines of constant time (every 0.0001 s) and, on steep stretches,
along lines of constant load (every 0.5 lb); thin time-line dashes were removed first. Samples were
interpolated on that center line at t = 0.002, ..., 0.020 and 0.025, ..., 0.095 s, and at every
multiple of 5 lb where consecutive time samples differ by more than 5 lb. Every sample was checked on
zoomed crops (`crops/chk-*.png`, `crops/cl-p*.png`) and lies on the line's ink. The t = 0.100 sample is
the last ink in each panel (within 1.5 px of the t = 0.10 line), so it is recorded once, as the last
trace sample. Trace samples are in drawing order (time increasing; each trace is a single-valued time
history).

Bounds: half the line width measured at the sample (from the chords and the line's direction; the line
is 5 to 6.5 px wide), with a floor of 2.5 px because a single row of this binary scan shows the line as
4 to 6 px (pixel staircase); 1 px more where the trace overlaps a grid line; 3 px at the ink ends.

Where the trace is hard to follow:

1. Panel 1 start (t below 0.002): the trace runs down along the 0 line into the baseline; its own ink
   is lost in the baseline below v 3524. First sample at (1249.0, 3523.0), about 0 lb, t 0.0002.
2. Panel 2 start: the trace comes down just left of the 0 line (at about +1 lb) into the baseline.
3. Panel 3 start: the ink starts right of the 0 line (the right frame) and beyond the end of the
   baseline, at (2285.5, 3523.0): +3.9 lb on this panel's scale (a small tension on a compression
   panel), t 0.0005; recorded as the scale gives it and flagged `extrapolated` by the tool. The trace
   then crosses the frame (t about 0.002, center from its left edge and width) and bends there.
4. Grid-line overlaps: panel 2 runs along the +40 line for t 0.077 to 0.083 (sample t = 0.080 from the
   ink run with the line inside it); panel 3 lies on the -80 line at its first compression maximum (t
   0.009 to 0.010, center from the trace's right edge and width) and runs along it for t 0.053 to 0.056
   (sample t = 0.055); the 5 lb samples at grid values (20, 40, -60, -80 lb) are read where the center
   line crosses the grid line, from the ink run with the line inside it.
5. Gap in the drawn line: panel 3 at t 0.0137 to 0.0142 (v 3289 to 3297) has no ink; the t = 0.014
   sample is moved to the ink at the gap's upper end (t = 0.0142, v 3288) rather than placed in the gap.
6. Ends: panel 1 ends merged with the top of its 0 line (+0.7 lb), panel 2 ends free at +9.6 lb, and
   panel 3 ends on the t = 0.10 dash, 1.5 px past it (-4.5 lb). Panel 2's trace does not return to 0 by
   t = 0.10.

## Features

Role words begin each note. On panel 3 the recorded values are negative (compression, as printed), and
the roles follow the recorded value literally: the two compression maxima (the most negative values,
the highest points of the panel read upright) are `knee, minimum`, and the least compression between
them is `peak`. Each note says this in words, so a reader using the opposite convention can pair them.

| panel | role | t (s) | load (lb) |
|---|---|---|---|
| 1 | first | 0.0002 | 0.0 |
| 1 | knee (leaves the 0 line, rise starts) | 0.0018 | 1.1 |
| 1 | peak | 0.0149 | 48.5 |
| 1 | knee, minimum (flat stretch) | 0.031 | 41.4 |
| 1 | peak (largest, broad top) | 0.0587 | 52.8 |
| 1 | last | 0.1000 | 0.7 |
| 2 | first | 0.0003 | 1.0 |
| 2 | knee (rise starts) | 0.0043 | 2.4 |
| 2 | knee (end of the steep rise) | 0.0102 | 42.5 |
| 2 | peak (broad) | 0.0207 | 46.7 |
| 2 | knee, minimum (flat stretch) | 0.0333 | 43.5 |
| 2 | peak (largest, broad top) | 0.0601 | 47.6 |
| 2 | last | 0.1000 | 9.6 |
| 3 | first | 0.0005 | +3.9 (beyond the 0 line) |
| 3 | knee (bend at the frame crossing) | 0.0021 | -0.2 |
| 3 | knee, minimum (first compression maximum, on the -80 line) | 0.0096 | -79.7 |
| 3 | peak (least compression between the maxima) | 0.0272 | -53.3 |
| 3 | knee, minimum (largest compression, broad) | 0.0685 | -87.3 |
| 3 | last | 0.1001 | -4.5 |

The time of a broad extreme is not an observation: its v bound is half the stretch over which the
line stays within half a line width (in load) of the extreme, and the note gives that stretch (up to
plus or minus 0.0076 s for panel 2's second peak). Two wiggles of panel 1 (t 0.023 to 0.027 and 0.072
to 0.075, 0.4 to 0.5 lb, 1.5 to 2 px, the size of the scan's pixel steps) are not recorded as features.
Knees are recorded only at clear bends of the drawn line (a turn of 20 degrees or more over 25 px
either side on the page); the gradual rounding into the final decline of panels 1 and 2 (t about 0.08)
is not one.

## Differences from the figures index and the task description

1. The task and index are borne out: three panels, sequence strut3, strut2, strut1 top down, (Tension),
   (Tension), (Compression), time 0 to 0.10, a `-60` printed above `+40` in panel 2, and a damaged `.09`.
2. The title of panel 1 prints no unit ("Load on Strut No. 3"); panels 2 and 3 print "(lbs.)".
3. The inset gives Vv = -114.93 in./sec.; the index row and Table 5-T3 give -114.9.

## Files

1. `cal-p1/`, `cal-p2/`, `cal-p3/`: `anchors.csv`, `calibration.json`, `knots.json` (the tool's ink
   check of every knot).
2. `calibration-eye-checks.csv`: every label as printed, its line, the by-eye verdict.
3. `points-p<n>.csv`, `points-p<n>-native.csv`, `overlay-p<n>.png` for n = 1, 2, 3.
4. `helpers/`: the scripts that measured the lines and the traces (run with the pychrono10 Python from
   `out/F5-25/helpers/`); `crops/`: the zoomed crops used for the checks.
