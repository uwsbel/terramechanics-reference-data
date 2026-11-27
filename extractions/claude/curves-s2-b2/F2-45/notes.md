# F2-45, panel 1: notes of the Claude reading (batch curves-s2-b2)

Page `packet/p0106.png` (PDF 106, printed 2-81), read as scanned: penetration increases up the page
(v decreasing), load increases to the left (u decreasing). Pixel coordinates refer to the unrotated
page. Values in `points-p1-native.csv` come from the piecewise map (`calibrate_axes.py piecewise
--image`, D-025); the affine values are kept in `r2/points-p1-affine.csv` (largest difference from
the piecewise values 0.005 in and 0.32 lb).

## What the page prints

1. Title: "Figure 2-45. Load-Penetration Curves in Soil No. 1 (RS Loose) (Dr approx 0.0)", as in
   `figures-rows.csv`.
2. Solid line: labeled along its length "Four-Inch Cylinder - LPT No. 95, Gp = 16.2". The text runs
   parallel to the solid line on its high-load side (page left of the line). Series `lpt95`.
3. Dotted line: labeled along its length "Four-Inch Footpad - LPT No. 79, Gp = 15.2". The text runs
   parallel to the dotted line on its low-load side (page right of the dots). Series `lpt79`.
4. Both identities and line styles agree with `series.csv`. No markers (symbols) are plotted; none
   recorded.

## Calibration (`cal-p1/`)

1. Redone, not reused. The earlier reader's calibration (box 380 1415 2320 3640, whose left edge
   cut through the left frame line) is moved to `earlier-reader/cal-p1/`. Mine:
   `calibrate_axes.py detect packet/p0106.png --box 350 1420 2320 3640 --x-values 0,1,2,3,4,5,6,7
   --y-values 0,25,50,...,300 --x-direction up --y-direction left --bands 11 --dark 220
   --min-frac 0.3 --snap 15`. All 21 lines detected in 11 of 11 bands; 104 anchors. The two maps
   agree within 0.7 px.
2. Affine residuals: x RMS 0.0024 in (max 0.0048), y RMS 0.170 lb (max 0.505), that is 0.03 and
   0.06 percent of the spans (limit 0.5 percent). The y residual reflects uneven drafting (150 to
   158.5 px per 25 lb), which the piecewise map follows.
3. Ink check of the piecewise knots (`cal-p1/knots-check.json`, from the tool's `knots_summary`):
   all 8 penetration lines and 13 load lines verified, location errors 0.5 to 1.05 px, none
   rejected, 0 points beyond the outermost verified line.
4. Labels checked by eye (`calibration-eye-checks.csv`, crops `checks/r2-eye-*.png`): penetration
   7, 3, 1 (and 0) and load 25, 100, 250 (and 0, 50) each sit on the line they are assigned to,
   within 7 px against line spacings of 151 to 310 px.
5. Unlabeled load lines. The printed load labels are 0, 25, 50, 75, 100, 150, 200, 250. Lines are
   drawn every 25 lb, so 125, 175 and 225 lie between labeled lines. Two lines lie beyond the last
   label: a drawn line at u 536 and the left frame at u 382. They are taken as 275 and 300 from the
   even spacing (154 px, the same as the rest of the grid). No 300 is printed. The solid trace runs
   beyond 250 lb from about 6.45 in to its end, so these values (samples at 6.50, 6.75, 6.95 in, two
   knees and the peak) rest on that inference. The penetration axis runs to 7 (the top frame), as
   printed.

## Traces

1. They never cross. The solid line (lpt95) lies at higher load than the dotted line (lpt79) at
   every penetration; the two converge only at the origin corner. There, dot 1 of the dotted line
   (u 2230, v 3559) is about 3 px from the upper edge of the solid line; the next dot toward the
   origin appears merged with the solid line near u 2240, v 3573 (a bump on its upper edge) and the
   one after would fall in the bottom frame. Told apart by line style: continuous ink versus
   separate round dots on a pitch of about 17.6 px.
2. Solid line (lpt95), 29 trace samples. Center found row by row (`r2/solid_r2.py`), by column near
   the origin where the line is shallow on the page (`r2/centerline_r2.py`); rows on a grid line, on
   a load-line crossing or widened by a jog are not used for centers. Sample at each 0.25 in: a local
   straight fit of the clean centers meets the line of constant penetration (`r2/sample_r2.py`).
   Bound: half the perpendicular thickness measured there (3.3 to 4.6 px; the line is 7 to 9 px thick
   in the middle and 10 to 12 px near both ends), plus 1 px where the center is fitted across a grid
   crossing.
3. Samples moved off grid lines. At 1, 2, 3, 4, 5 and 6 in the line is hidden in the drawn
   penetration line, and at 2.50 and 5.50 in in the 100 and 225 lb lines; there the sample is taken
   at 0.025 in more (N.025, 2.525, 5.525 in), where the line's own ink is clear of the grid. Each such
   row says so in `note`. Every sample has its own ink, with the grid bands removed, within 1 px
   (`r2/inkcheck_r2.py`).
4. Dotted line (lpt79), 26 trace samples, each on a dot center (the centroid of the dot's ink),
   never in a gap: the dot nearest each 0.25 in step among dots clear of grid lines
   (`r2/dots_r2.py`, `r2/sample_r2.py`), plus the first and last dots. Bound: the half extents in u
   and v of an ellipse with half the dot width across the line and half the local dot spacing along
   it (about 6.5 px in u, 8 px in v; up to 10 px where a dot on a grid line is missing from the
   chain). The chain holds 123 dots; touching dots near the origin (dots 6 to 10, 15, 16) were split
   along the line; two dots lying on grid lines (near u 1962, v 3111 on the 50 lb line and u 1641,
   v 2509 on the 100 lb line) are not in the chain and not used. Some dots touching a grid line have
   centers from the ink outside the grid band; four samples use such dots and say so.
5. The dotted line's label text runs next to the dots from about 3.1 to 6.3 in; no text glyph
   touches a dot used for a sample, and the period of "15.2" (u 1213, v 1687) was not taken for a
   dot.

## Features

1. lpt95 first: (2254, 3583.5), 0.037 in, 4.2 lb, where the solid line separates from the bottom
   frame; its ink below that is merged with the frame, so nothing is read at penetration 0.
2. lpt95 knee at 0.096 in, 12.2 lb: end of the initial steep rise. The bend is gradual; bound
   widened along the line.
3. lpt95 kinks: three distinct load steps at nearly constant penetration, each recorded at the middle
   of its horizontal jog with a u bound spanning the jog: 1.46 in (about 62 to 66 lb), 2.79 in
   (about 109 to 113 lb), 3.13 in (about 122 to 126 lb, the jog crosses the 125 lb line).
4. lpt95 knees at 6.36 in (264 lb) and 6.45 in (273 lb): start and end of a stiff stretch where the
   load rises faster than elsewhere on the trace.
5. lpt95 peak and last: the same point (388, 1476), 6.95 in, 299.0 lb. The solid line runs into the
   left frame (300 lb) just below the top-left corner (7 in). The maximum load is at the end of the
   drawn line; whether the record went on beyond the frame cannot be seen.
6. lpt79 first: dot 1, 0.116 in, 8.1 lb (see Traces, item 1). lpt79 peak and last: the last dot,
   6.22 in, 176.6 lb, just left of the 175 lb grid line; no dots beyond it. No knee or kink is
   visible on the dotted line: it is close to straight from its first dot to its last.

## Ambiguities and judgment calls

1. Kinks: only the clear steps are recorded. Smaller wiggles of the solid line are not: a bend at
   the 75 lb line near 1.78 in, an offset where the line crosses the 2 in line, a small notch near
   5.25 in, and a short vertical stretch near 6.62 in (u 505, v 1566 to 1580).
2. The solid line's center at 2.50 in (sampled at 2.525 in): between about 2.43 and 2.53 in the line
   runs along the 100 lb grid line, so the load there is close to 100 lb, but the line's center
   cannot be separated from the grid line.
3. The 275 and 300 lb values of the two lines beyond the last label (Calibration, item 5).
4. The start of both traces at the origin is hidden by the frame and by the merged dot (Traces,
   item 1); the first points are where the ink becomes readable, not penetration 0.

## Reused and redone

1. Redone: the calibration (`cal-p1/`), the eye checks (`calibration-eye-checks.csv`,
   `checks/r2-eye-*.png`), the tracing of both lines, the dot detection and chaining, every sample,
   feature and bound, and the overlay. My scripts and work files are in `r2/` (run from the workspace
   root with `PYTHONPATH=out/F2-45/r2`, in order: `solid_r2.py`, `dots_r2.py`, `centerline_r2.py`,
   then `sample_r2.py`, which reads `r2/features-r2.csv`, the feature pixels read by eye on zoomed
   crops; then `calibrate_axes.py piecewise` and `plot_grid.py overlay`).
2. Taken from the earlier reader as method only: its helpers (`trace_f245.py`, `dots_f245.py`,
   `chain_dots.py`) showed the approach (row tracking of the solid line, grid masking, dot chaining
   by spacing and direction), which I rewrote with changes (column tracking near the origin,
   splitting touching dots along the line, dot width from area, sampling off grid lines). Its
   `work/solid-rows.csv` and `work/dots.csv` were used only to place my first inspection crops. None
   of its outputs enter my points. Its files (`components.csv`, `track-solid.csv`, `work/`,
   `views/`, `checks/eye-*.png`, the helper scripts) are left as they were, unused.
3. Checked by eye: the overlay `overlay-p1.png` and the inspection crops `r2/vs*.png`, `r2/vd1.png`,
   `r2/dd*.png`, `r2/ds*.png`, `r2/m-jogs*.png` (every trace sample and feature sits on the line's
   ink; every dotted sample on a dot).
