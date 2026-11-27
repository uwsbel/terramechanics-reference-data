# Figure 2-29 (F2-29), printed page 2-55, PDF page 80: blind reading notes

## Page and figure

1. The page is printed sideways: penetration increases up the page, load increases to the left.
   Calibrated as scanned with `--x-direction up --y-direction left`; no rotation.
2. Axis titles as printed: `Penetration (in.)` (labels 0 to 8, every inch) and `Load (Lbs.)`
   (labels 0 to 1200, every 200 lb). Plain pounds, nothing to rescale.
3. One curve, the recorded trace of `LPT #27`. Printed label box: `LPT #27 / 2" Diameter
   Cylinder / D.P.T. Record No. 54074 / Pen Rate 1/2" Per Min. / Plate Compactor`. This matches
   `series.csv` (series_id `lpt27`). No straight lines, no markers, no symbols on this figure.
4. The frame extends one grid spacing past the last labelled penetration line: the top frame
   line (v about 1016 at u 1000) sits 308 px above the 8 in line and carries no label (it would
   be 9 in). It was kept out of the calibration box (box top v = 1100) so that the tool's
   "outer line = last value" rule put 8 in on the labelled line. The trace ends at the 8 in line,
   so nothing depends on the unlabelled frame.
5. The bottom frame is the 0 in line and the right frame is the 0 lb line, both labelled; the
   left frame is the 1200 lb line, labelled.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect`, box 440 1100 2370 3830, 10 bands, dark 160, min-frac 0.5. All 9
   penetration lines and all 7 load lines detected (the 1000 lb line in 7 of 10 bands: it passes
   behind the legend box; the 1 in and 2 in lines in 8 of 10). No predicted line.
2. 63 anchors. Residuals: penetration rms 0.006 in, max 0.015 in (0.07 percent of the 8 in span);
   load rms 0.88 lb, max 1.80 lb (0.07 percent of the 1200 lb span).
3. Scale about 308.6 px per inch and 308.0 px per 200 lb. The scan is tilted: horizontal lines
   drop about 0.011 px per px to the right, vertical lines lean 0.014 px per px downward (about
   0.7 degree).
4. Six printed labels checked by eye on zoomed crops (`calibration-eye-checks.csv`): all six sit
   beside the line the tool assigned them. The 600 lb label is centred 25 px right of its line,
   normal typesetting offset.
5. `points-p1-piecewise.csv` (extra, D-025 map, `--image`) agrees with the affine values to
   within 1.2 lb and 0.006 in; the first point (0.03 in, on the 0 lb frame) and the two points at
   or just beyond the 8 in line are flagged `extrapolated` by the piecewise tool because they sit
   on or outside the outermost verified line.

## The trace (`lpt27`)

1. Ink starts at the right frame (load 0) about 10 px (0.03 in) above the bottom frame, merging
   with the frame corner (crop `crops/start-zoom.png`). The 0 in sample and the `first` feature are
   this point, with wide bounds (8, 5 px).
2. From there the load rises to a local maximum of about 216 lb at 0.36 in (`knee` feature),
   falls back to a trough of about 144 lb at 0.9 in (`knee`, flat bottom, v bound 12 px), then rises
   with a wavy line to the end of the record at about 1130 lb at 8.0 in. The maximum load is at
   the end of the trace, so `peak` and `last` are the same pixel (574, 1335): the ink stops about 5 px
   above the 8 in grid line, merged with it (crop `crops/end.png`).
3. Between 0.2 and 0.55 in the trace runs on or beside the 200 lb grid line (samples at 0.25 and
   0.50 in, u bounds 11 and 10 px, flagged `merged`); it crosses that line again at 1.5 in (bound
   6 px) and the 600 lb line at 3.25 in (bound 8 px).
4. Samples at the integer inches fall on the horizontal grid lines; their centres were taken from
   the ink in the rows 13 px above and below the line and interpolated (noted per row). The crossings
   at 2, 3 and 4 in are at a shallow angle to the line (u bound 12 px); the rest are 5 to 7 px.
5. Knees recorded: the S-shaped step at 2.5 to 2.6 in (load about constant at 480 lb for 0.1 in),
   the start (5.91 in) and end (6.38 in) of a stretch where the load stays near 980 lb. Smaller
   wiggles (1 to 4 px, e.g. at 2.3, 4.3 to 4.8, 6.8 to 6.9 in) are the texture of the recorder line
   and were not recorded as features; a reviewer who wants them can locate them on `overlay-p1.png`.
6. The two bounds are half the ink run along the row (u, the load direction, so an oblique run
   gives a wider load bound) and half the line thickness across it (v, 4 px; the line is 6 to 9 px
   thick everywhere). Samples at 0.25 in steps, 33 in all, in drawing order.
7. No crossings with other curves (single trace). No markers.

## Ambiguities

1. Where the trace rides on the 200 lb line (0.2 to 0.55 in) the trace centre cannot be
   separated from the grid line's ink; the load there is 190 to 200 lb within about 7 lb.
2. The exact end of the ink at 8 in: the trace ink crosses the 8 in line and stops 4 to 5 px
   above it, so the last point is 0.01 in beyond 8 in (affine) and flagged extrapolated by the
   piecewise map.
3. The first point is in the frame corner; whether the record begins exactly at (0, 0) or at
   0.03 in cannot be told from the ink.

## Files written (under `out/F2-29/`)

`cal-p1/calibration.json`, `cal-p1/anchors.csv`, `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv` (apply), `points-p1-piecewise.csv` (extra, D-025 map), `overlay-p1.png`,
`notes.md`, `crops/*.png` (label checks, start, end, kinks, overlay details), `helpers/*.py`
(scan_trace.py, scan_trace2.py, write_points.py).
