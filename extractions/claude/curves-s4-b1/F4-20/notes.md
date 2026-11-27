# F4-20, Claude reading (batch curves-s4-b1)

Figure 4-20, "Force versus Displacement for Vertical Impact Tests on Various RS Soils, Footpad
Diameter = 6.17 Inches", printed page 4-24, PDF page 209 (`packet/p0209.png`). One panel, printed
sideways. Axis titles as printed: "Displacement - Inches" (x) and "Vertical Force - Pounds" (y).
All pixel coordinates are those of the unrotated page image.

## What is on the page

1. Orientation. On the unrotated page, displacement increases upward (x lines are horizontal on
   the page) and force increases to the left (y lines are vertical). Calibrated with
   `--x-direction up --y-direction left`.
2. Grid. Ten displacement lines, 0 to 4.5 in every 0.5 in, the frame lines carrying 0 (bottom) and
   4.5 (top); every one is labelled. Thirteen force lines, 0 to 600 lb every 50 lb, the frame lines
   carrying 600 (left) and 0 (right); labels at every 100 lb only (600, 500, 400, 300, 200, 100,
   0), the 50 lb lines in between unlabelled but evenly spaced. No ticks beyond the frame, no
   markers.
3. Legend (checked on the page, it agrees with `series.csv`): "Run No. 4, D_r = 0" solid line;
   "Run No. 10, D_r = 0.45" dotted line; "Run No. 12, D_r = 0.65" long dashes. Ids kept as given:
   run4, run10, run12.
4. The text introducing the figure (printed 4-22, PDF 207) speaks of a "six-inch diameter footpad"
   and "force versus penetration"; the caption says 6.17 inches and the axis says Displacement.
   Not a conflict, noted only.

## Calibration (`cal-p1/`, `calibration-eye-checks.csv`)

1. `tools/calibrate_axes.py detect` on box 405 995 2305 3835, 7 bands, kept unchanged in
   `cal-p1-detect/`. It took the legend's sample line of Run No. 12 (u about 878, v 1960 to 2300)
   for the 450 lb grid line in one band (450 line fitted with the wrong tilt, 9 px off the ink at the
   top), and its own ink check rejected the 600, 500 and 450 lb lines (2.7 to 3.4 px from the ink at
   one end). The bottom frame was also pulled by the traces that run along it near the origin.
2. So every line was re-measured on the ink with `helpers/refine_cal.py` (profile across the line
   every 6 px away from the crossings, nearest dark run, robust straight-line fit; tools unchanged),
   which writes `cal-p1/` in the tool's layout. The refined lines differ from the detected ones by
   less than 1 px except the 600, 500, 450 lb lines and the bottom frame (up to 9.3 px for 450).
3. Result: affine residuals x RMS 0.0023 in, max 0.0055 in (0.12 percent of 4.5 in); y RMS 0.36 lb,
   max 0.96 lb (0.16 percent of 600 lb). With `piecewise --image` all 10 x lines and all 13 y lines
   pass the ink check (none predicted, none rejected); line location errors 0.50 to 1.28 px. The
   grid is drafted slightly unevenly (600 to 550 lb: 151 px; other 50 lb steps 153 to 158 px), which
   the piecewise map follows. Largest difference between the affine and the piecewise values over all
   points: 0.0024 in and 0.66 lb.
4. By eye, every printed label (7 force labels, 10 displacement labels) sits on the line it is
   anchored to, within 0.6 to 7.4 px of the line (line spacing 154 px for force, 310 px for
   displacement); each check is a row of `calibration-eye-checks.csv`. The force label "0" sits below
   the corner and the displacement label "0" beside it; the frame lines carry the first and last
   values, and no labelled value is missing from either sequence.

## How the traces were sampled

1. Guide polylines in drawing order (`helpers/guides.json`, read from column and row scans of the
   page with the grid erased, `helpers/degrid.py`, only for finding the lines) steer a tracer
   (`helpers/trace.py`) that re-centres every point on the ink across the line, every 1 px of arc,
   on the page ink. A centre counts only where the run across the line is clean (one run, 6 to 14
   px wide). Samples are then picked by `helpers/sample.py` at every crossing of x = 0.1 k in and, where
   the trace is steep (more than 500 lb/in), of F = 50 m lb, on the ink: the nearest clean point on
   the solid line; the centre of the nearest dot on the dotted line; a point at least 3 px inside the
   nearest dash on the dashed line. Bounds are half the measured line width; on the dotted and dashed
   lines the bound along the line is widened to half the adjacent white gap and projected on u and v.
2. Samples that fell where traces run together, on grid lines, or in the scan dropout were read by
   hand on zoomed crops (`helpers/build_points.py`, every one with its reason in `note`); two
   automatic samples were replaced (listed in that script).
3. Values: `calibrate_axes.py piecewise --image`, no point beyond the outermost verified line.
   `points-p1-native.csv` holds the values in the printed units (in, lb).
4. Features: `first` and `last` (each also a trace sample at the same pixel, so the trace runs from
   where its ink starts to where it ends), every local maximum of force (`peak`), the minimum after
   it (`knee, minimum`), and corners and kinks (`knee`).

## The traces

1. Run No. 4 (solid, D_r = 0): rises to a first peak of about 123 lb at x about 0.24 in, falls to a
   flat minimum of about 72 lb at x about 1.0 in, rises steadily to a second peak of about 139 lb at
   x about 4.04 in, turns in a rounded corner at x about 4.12 in, and the force falls to about 35 lb
   at x about 4.15 in. It ends in a small hook: a short diagonal down to about 20 lb (displacement
   decreasing slightly to 4.11 in), then a return stroke back to about 45 lb at nearly constant
   displacement. The return stroke is recorded as drawn (drawing order kept); whether it is the
   footpad settling or a drafting mark cannot be told from the page (it ends near the weight of the
   impacting body, but that is an interpretation, not a reading).
2. Run No. 10 (dotted, D_r = 0.45): loads steeply to a corner at about 283 lb, x about 0.31 in
   (peak), runs nearly at constant force to a second corner at about 275 lb, x about 0.46 in (knee),
   unloads with a kink at x about 1.09 in, about 135 lb (knee; the slope on the page changes from
   about -2.6 to -1.25 at a short stretch of closely spaced dots), reaches a corner at about 60 lb,
   x about 1.52 in (knee, minimum), then runs at nearly constant force up to the scan dropout. After
   it, the force is about 66 lb at x about 1.93 to 1.95 in (second peak), then falls along the x = 2.0
   in grid line to about 26 lb (last dot).
3. Run No. 12 (long dashes, D_r = 0.65): loads to a sharp apex of about 592 lb at x about 0.39 in
   (peak), unloads to a flat minimum of about 8 lb at x about 0.83 to 0.90 in (knee, minimum), then
   rebounds: the force rises to about 62 lb at x about 1.20 in (second peak) and falls to about 23
   lb at x about 1.25 in (last, right end of the last dash).
4. Largest displacements: Run 4 about 4.15 in, Run 10 about 2.0 in, Run 12 about 1.25 in.

## Where traces cross, run together, or are hidden

1. Origin. The three traces start together in one blob of ink at the corner, merged with the frame
   lines; they cannot be separated there. The `first` point of all three series is the same pixel
   (2276, 3793), where the merged ink meets the force = 0 frame line about 6 px above the frame,
   with a 7 px bound (x about 0.012 in, F about 3 lb).
2. Run 4 and Run 10 run together from u about 2050 to the origin (one band of ink, F below about 75
   lb, x below about 0.06 in); their F = 50 lb samples are the same pixel, the centre of the band,
   with a bound covering it (taken at about 60 lb, the nearest clean ink). From u 1955 to 2050 Run
   10's dots touch the Run 4 line from below; Run 10's F = 100 lb sample is read from a dot's lower
   edge.
3. Run 12's loading branch lies on the bottom frame line (displacement 0) from u about 1950 to the
   origin; its F = 50 lb sample is bounded between the dash's upper edge and the frame's upper edge
   (the white dash gaps at u 2086 to 2110 and 2152 to 2168 show the frame alone there).
4. Crossings: Run 10 and Run 12 at (1610 to 1647, 3369 to 3402), where Run 10's dots merge with a
   Run 12 dash (no sample placed in the merged ink; Run 10's x = 0.7 in sample is the next clean
   dot, 14 px away); Run 4 and Run 12 at about (2025, 3348); Run 4 and Run 10 at about (2010, 2930),
   where a Run 10 dot touches the Run 4 line (samples on clean ink either side, noted).
5. Run 4 runs into the 100 lb grid line between v 2580 and 2660 and between v 2700 and 2758; its
   x = 1.9 in sample is centred from the clear left edge, and its x = 1.7 in sample is taken just
   below the merge (x about 1.68 in).
6. Scan dropout: a blank patch about u 1955 to 2240, v 2625 to 2810 has no ink at all, grid lines
   included (the 100 lb and 50 lb lines and the right frame are broken there too). Run 4 has a gap
   from x about 1.78 to 1.84 in (x = 1.8 in cannot be read); the Run 10 dots are missing from x about
   1.60 to 1.93 in (x = 1.7, 1.8, 1.9 in cannot be read). Trace samples mark the last ink before and
   the first ink after each gap; nothing is interpolated across.
7. Small things: a stray thin stroke at u 2069 to 2081, v 2608 to 2610, beside the first Run 10 dot
   after the dropout (not part of the trace); a partial Run 10 dot at (1417, 3624) next to the corner
   (not used as a sample); the last Run 10 dots sit on the x = 2.0 in grid line.

## Files

1. `points-p1.csv` (reader pixels and bounds), `points-p1-native.csv` (with x_native in in,
   y_native in lb, read bounds, cal_model; piecewise map with the ink check).
2. `cal-p1/` (refined calibration used for the values), `cal-p1-detect/` (the tool's detect output,
   kept for traceability), `calibration-eye-checks.csv`.
3. `overlay-p1.png` (all points over the plot, `tools/plot_grid.py overlay`; run4 red, run10 green,
   run12 blue).
4. `helpers/`: the scripts named above, the dense trace (`dense.csv`), the automatic samples
   (`auto.csv`, `unresolved.csv`), and the zoomed crops used for the hand readings (`crops/`).
