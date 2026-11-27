# F2-48, batch curves-s2-b2: Claude's blind reading, panel 1

Figure 2-48, PDF page 109 (`packet/p0109.png`), printed page 2-84: "Load-Penetration Curves for
Four-Inch Cylinder and Four-Inch Footpad in Soil No. 9 (SS Dense) (Dr approx 0.76)". Printed sideways:
read on the page as scanned, penetration (in) increasing up the page, load (lb) increasing to the left
(`--x-direction up --y-direction left`). The image was never rotated.

This reading was begun by an earlier Claude reader (2026-10-30, interrupted before writing it up) and
checked and finished by a second Claude reader on 2026-11-02 under the same protocol, equally blind.
Everything below was checked against the page on zoomed crops by the second reader, who is responsible
for the final output.

## 1. Which line carries which printed label

1. **lpt87, solid line**: "Four-Inch Cylinder (LPT No. 87) Gp = 45". The label is printed along the
   solid line on its lower-load side (to the right of it on the page), running from about 3.8 in
   ("Four", whose "F" nearly touches the line near the 400 lb line) to about 6.7 in ("Gp = 45").
2. **lpt85, dotted line**: "Four-Inch Footpad (LPT No. 85) Gp = 46". The label is printed along the
   dotted line on its higher-load side (to the left of it on the page), from about 5 in ("Four") to the
   end of the dots ("Gp = 46" next to the last dots, just below the 8 in line).

Both labels sit between the two curves, each one hugging its own curve; the printed text matches
`series.csv` exactly (ids, LPT numbers, Gp values, line styles). The footpad curve lies below the
cylinder curve at every penetration past the start, as the context page (PDF 105) says it generally
does.

## 2. Where the traces cross or run together, and how they were told apart

1. The traces never cross. They run together only at the start, in the bottom-right corner of the
   plot (penetration 0, load 0), below about 0.13 in (solid) and 0.15 in (dotted): the last three dots of
   lpt85 (near u 2227, 2240 and 2253, v 3732 to 3752) sit on the upper edge of the solid line where it
   bends down into the bottom frame. They were told apart by shape and spacing: the dots are round
   blobs about 12 px across that continue the dot chain at its regular spacing (16 to 18 px), while the
   solid line's lower edge stays continuous into the frame. The first point of each trace and the
   lpt87 toe knee carry notes saying so and have widened bounds.
2. Past about 0.15 in the two traces are 60 to 150 px apart and are identified by line style alone.

## 3. Calibration (`cal-p1/`, `calibration-eye-checks.csv`)

1. `tools/calibrate_axes.py detect` with box `380 1200 2320 3820`, x values 0 to 8 in by 1, y values 0
   to 1200 lb by 200, `--bands 12 --dark 160 --min-frac 0.5 --snap 10`. Re-run on 2026-11-02 into a
   scratch folder: identical result. All 16 lines (9 penetration, 7 load) are `detected in 12/12
   bands`; none predicted. The piecewise map's ink check verifies all 16 (location errors 0.5 to 0.99 px,
   ink found at 17 or 18 of 18 positions on the x lines and 23 or 24 of 24 on the y lines; a few positions
   set aside where traces or labels cross); none rejected.
2. Affine residuals: x (penetration) RMS 0.0625 in, max 0.149 in; y (load) RMS 0.96 lb, max 2.55 lb.
   **The x residual is 0.78 percent of the 8 in span, above the 0.5 percent the protocol flags.** The
   cause is the drawing, not the detection: the 0 to 1 in interval is drawn 233 px tall, while every
   other inch is 304 to 316 px (mean about 310). Fitting the affine map without the 0 line gives RMS
   0.010 in. Changing the box or the thresholds cannot remove this; the values are taken from the
   piecewise map (D-025), which reads each interval as drawn.
3. **The short first interval is the main calibration ambiguity of this figure.** Checked by eye on
   crops at zoom 3 and 4: the "0" label is printed on the bottom frame line (v 3767), the "1" label on
   the first interior line (v 3534), and both traces start on the bottom frame. Read as drawn, a point
   at the frame is 0 in. Had the zero been drawn at the regular spacing of the 1 to 8 in lines, it would
   lie about 71 px below the frame and the frame would read about 0.23 in; every value below 1 in would
   then shift by up to about 0.25 in (for example the lpt87 plateau knee, 0.42 in as drawn, would read
   about 0.56 in). This reading follows the page as printed; a student should know that the first inch
   of both curves rests on this drafting.
4. The frame extends about 309 px (one more inch, about 9 in) above the 8 in line, to v 1052, with no
   label and no grid line in between. That top frame is not a knot. The last labelled penetration line
   is 8 in; the solid trace ends 9 px above it, so its last point (8.03 in) is flagged `extrapolated` in
   `cal_model` (by 0.03 in). On the load axis the left frame is the 1200 lb line and the right frame the
   0 lb line.
5. Label checks by eye (`calibration-eye-checks.csv`): penetration 0, 1, 4 and 8; load 0, 200, 600 and
   1200. Every label sits on or straddles its own line (offsets 1 to 12 px, against 233 to 316 px to the
   next line), so no label is ambiguous. The load labels sit 3 to 12 px to the left of their lines
   (sideways text), the penetration labels 6 to 9 px below theirs (except 0, centered on the frame).

## 4. Points (`points-p1.csv`, `points-p1-native.csv`)

Counts: lpt87, 34 trace and 7 feature; lpt85, 33 trace and 6 feature. No markers (no symbols are
plotted). Values from `tools/calibrate_axes.py piecewise out/F2-48/cal-p1 ... --image packet/p0109.png`.

1. **Trace samples** every 0.25 in of penetration, in drawing order, from where the ink starts to where
   it ends. Neither trace doubles back: each is single valued in penetration (the solid centerline was
   scanned row by row and column by column without a fold, and the dot chain runs monotonically up the
   page), so drawing order is the order of increasing penetration.
   - lpt87 (solid): the centerline of the line where the constant-penetration line crosses it. On a
     whole-inch grid line the sample is taken 7 px below it (x about n - 0.023 in) on the trace's own
     ink, not on the grid line's. Bound: half the line's thickness across itself (median thickness 5.8
     px, so 2.5 to 3.5 px).
   - lpt85 (dotted): the center of the whole dot nearest each 0.25 in step; dots cut by a grid line are
     skipped, so a few samples sit up to 0.07 in from the step (1.06, 1.96, 6.68 in). Bound: half the
     local dot spacing along the line (spacing 16 to 18 px) and half the dot diameter (about 12 px)
     across it, projected on u and v (6 to 8 px in u, 7.5 to 9 px in v).
   - First and last trace samples: at the start and end of each trace's ink (the same pixels as the
     first and last features).
2. **Features** (rule 3):
   - lpt87: first (0.04 in, 15 lb, where the solid line meets the bottom frame just left of the corner;
     whether it continues inside the frame to the corner cannot be seen); knee (toe) at 0.12 in where the
     line bends from the steep run into the corner to the fast initial rise; knee at 0.42 in where the
     rise turns onto the plateau (a rounded turn, bound covers about 0.38 to 0.46 in); knee at the local
     maximum of the plateau (157 lb, a flat top from 0.45 to 0.68 in, bound covers all of it; x is not an
     observation there); knee at the plateau's lowest load (146 lb at 1.10 in, flat within 1 px from about
     1.07 to 1.11 in), after which the second rise begins; peak = last (839 lb at 8.03 in, the end of the
     line, 9 px above the 8 in line).
   - lpt85: first (0.06 in, 11 lb, the lowest dot visible above the bottom frame, merged with the solid
     line); knee at 0.64 in where the dots turn onto the plateau (about 86 lb); knee at 1.27 in where the
     second rise begins; knee at 4.90 in where the slope rises from about 78 to 99 lb/in; peak = last
     (740 lb at 7.97 in, the last dot, just below the 8 in line).
3. **Knee criterion used** (so the other reading can be compared fairly): a knee is recorded where the
   slope changes by about 20 percent or more between two stretches that are each nearly straight over
   0.5 in or more, so that the bend is visible against a ruler on the page and a two-line fit puts the
   corner at a stable place. The solid trace also has gentle undulations of about plus or minus 10 lb
   about a straight line between 2 and 8 in (steeper from about 4.85 to 5.6 in, flatter after about
   6.25 in); its local slope varies between about 85 and 150 lb/in on a 0.1 in scale, two-line fits
   place a break anywhere from 4.66 to 4.69 in (and 6.0 to 6.1 in) depending on the window, and the
   stretches on either side are not straight, so these are recorded only through the 0.25 in trace
   samples, not as knees. The rounded start of the solid trace's second rise (1.1 to 1.6 in, corner
   anywhere from 1.24 to 1.56 in depending on the fit window) is marked only by the plateau minimum at
   1.10 in for the same reason. On the dotted trace the corresponding corner is stable (1.28 to 1.35 in)
   and is recorded.

## 5. Other ambiguities a reviewer should look at

1. On the dotted trace 20 dots touch or merge with grid lines; no sample or
   feature is taken on a merged dot. Between 6.6 and 6.9 in the dots run along the end of a broken
   stretch of the 600 lb grid line next to the "(LPT" of the footpad label, so the 6.75 in sample is
   the whole dot at 6.68 in.
2. The 4.90 in knee of lpt85 has its corner (by two-line fits, 4.87 to 4.89 in) on the 400 lb grid line,
   where the dots merge with the line; the knee is on the nearest dot that keeps its own ink, which
   touches the grid line on its right, so its center may be biased by about 1 px toward lower load
   (within the 6.5 px bound).
3. The last lpt85 dot (7.97 in) sits under a gap in the 8 in grid line and touches the line's band at
   its top; the 6 px fragment on the line at u 1124 to 1129 is grid-line ink (the height of the line),
   and there is no dot above the line, so the dotted trace ends there.
4. Both traces have a bend near 4.9 in, close to where the labels start and to the 400 lb and 5 in grid
   lines. It is in the ink as printed; whether it is in the original record or came from redrawing
   cannot be told from the page.

## 6. What was kept and what was changed (second reader, 2026-11-02)

Kept, after checking each point on zoomed crops (zoom 4 to 9) and with an ink self-check (every sample
has its own line's ink within 2 px after the grid and frame bands, widened by 1 px, are removed):
the calibration (`cal-p1/`, unchanged), all 63 trace samples of the first reading, the first, toe, peak
and last features, and the lpt85 second-rise knee position.

Changed:
1. lpt85 knee onto the plateau moved from the dot at 0.715 in to the dot at 0.643 in. The dots run in
   two straight stretches that meet at about v 3612 (0.66 in); the slope is 78 lb/in up to the dot at
   0.643 in and 21 lb/in after it, and two-line fits put the corner at 0.62 to 0.65 in. The first reading
   had the knee on the next dot, past the corner (its bound did not reach the corner).
2. lpt85 knee at 4.90 in added (see section 4, item 3, and section 5, item 2). The first reading had no
   knee there; the bend is clear (two-line fit RMS 0.13 to 0.30 lb against 1.0 to 3.1 lb for one line).
3. lpt87 local maximum of the plateau moved from v 3648 (0.50 in, v bound 10 px) to v 3634 (0.56 in) with a
   v bound of 27 px, so the bound covers the whole flat top (0.45 to 0.68 in); the first reading's bound
   left out its upper half.
4. Bounds widened where the first reading was tighter than the ink supports: lpt87 knee onto the plateau
   (u 6, v 10 px, a rounded turn), lpt87 plateau minimum (v 12 px, a flat minimum), lpt87 toe knee (u 5 px,
   dots on the line's edge), lpt85 second-rise knee (v 10 px, fitted corner 1.28 to 1.35 in against dots
   0.05 in apart).
5. Trace rows added at the start and end of each trace's ink (rule 7: a curve's first and last trace
   samples are where its ink starts and ends); the first reading had these points only as features, so
   its traces began at 0.25 in and ended at the last 0.25 in step.
6. Notes rewritten for the features above; sequences renumbered in drawing order.

## 7. Files and how they were made

Run from the workspace root with `<local path>`:

1. `tools/calibrate_axes.py detect` as in section 3, item 1, written to `cal-p1/`.
2. `out/F2-48/dots.py` (dot chain, `dots.csv`), `out/F2-48/solid_centerline.py` (`solid-centerline.csv`),
   with helpers in `out/F2-48/trace_lib.py`; then `out/F2-48/sample_points.py`, which now writes the first
   reading to `points-p1-prev.csv` (re-run on 2026-11-02, identical to the file found in the workspace).
3. `out/F2-48/finalize_points.py`: applies the changes of section 6, writes `points-p1.csv`.
4. `tools/calibrate_axes.py piecewise out/F2-48/cal-p1 out/F2-48/points-p1.csv out/F2-48/points-p1-native.csv
   --image packet/p0109.png`.
5. `tools/plot_grid.py overlay packet/p0109.png --points out/F2-48/points-p1.csv --box 900 1300 2320 3800
   --out out/F2-48/overlay-p1.png`, inspected by eye in full and zoomed at both ends of both traces and
   at the changed features.

The check crops, rulers and fits of the second reader are in `check/` (with the files as found:
`points-p1-asfound.csv`, `points-p1-native-asfound.csv`, `overlay-p1-asfound.png`). `crops/`, `tmp/`,
`components.csv`, `ink-nogrid.png`, `labels.npy` and `dot-labels.npy` are the first reader's working files.
