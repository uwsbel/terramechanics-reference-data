# F2-33 (Figure 2-33, printed page 2-64, PDF 89), blind reading, panel 1

Page image `packet/p0089.png`, 3213 x 4558 px, read unrotated. The figure is printed sideways:
penetration increases up the page, load increases to the left. Pixel coordinates are page pixels
(u right, v down).

## Calibration (`cal-p1/`)

1. Box 330 2040 2345 3650, `--x-direction up --y-direction left`, penetration lines 0 to 5 (every
   inch), load lines 0 to 2500 (every 500 lb). All 12 lines detected (penetration 1 to 4 in 4 of 5
   bands, the fifth band being the one through the text block at the top left). 36 anchors.
   Affine residuals: x (penetration) rms 0.009 in, max 0.018 in (0.36 percent of the 5 in span);
   y (load) rms 3.5 lb, max 6.2 lb (0.25 percent of 2500 lb).
2. The frame extends one more inch above the last labelled line: a sixth horizontal line at
   v about 1767 to 1776 (the frame top, unlabelled, 308 px above the 5 line like the other
   intervals). It was not used as an anchor because it carries no printed value. A second run with
   it assigned the value 6 (`cal-p1-alt6/`, diagnostic only) gives the same map (x 0.00325 vs
   0.00324 in per px, y 1.2864 vs 1.2866 lb per px). Points above the 5 line (the upper end of
   the bce line at pen 5.26, the label centres) are flagged `extrapolated` by the piecewise map.
3. Grid drafting: the load lines are 386 to 397 px apart (389 average), the penetration lines
   303 to 310 px apart; both axes tilt by 0.2 to 0.4 degrees, slightly differently per line, as
   the piecewise map takes into account.
4. By-eye label checks in `calibration-eye-checks.csv`: all six penetration labels sit centred on
   their lines (within 7 px); all six load labels sit 5 to 15 px left of their lines (the glyph
   block is offset the same way everywhere; lines are 389 px apart, so no ambiguity). Also checked
   that the axis titles read `Load (Lb.)` and `Penetration (In.)`: plain pounds and inches, no
   multiplier.

## What is drawn, and which line carries which label

1. `lpt74`: the thin wavy line (about 6 px thick) labelled `A LPT No. 74, Gp = 103` (the label
   is printed alongside its middle part, between pen 2.3 and 4.0, with no leader). It starts at
   the frame corner (load 0, penetration 0) and ends at (935, 2237), pen 4.48, load about 1770 lb.
2. `lpt75`: the thick wavy line (12 px) labelled `B LPT No. 75, Gp = 105` (label alongside its
   lower part, under it, no leader). It starts at the right frame line on the pen 2 grid line
   (test started two inches below the surface) and ends at (910, 2236), pen 4.48, load about
   1800 lb, 25 px left of the end of lpt74. Both traces end at the same penetration.
3. `fit`: the thick straight line (15 px) from the load axis (intercept 721 lb at pen 0) to
   (544, 2096), just below the pen 5 line (pen 4.94). The leader arrow of the label
   `Slope = AγNq = 316 lbs./in.` points at it from the text block above the frame; the arrow
   head touches the line at about (635, 2170). Line style and arrow agree with series.csv.
4. `bce`: the other thick straight line (12 px) from the load axis (intercept 284 lb at pen 0)
   to (1499, 1994), pen 5.26, above the last labelled line. The leader arrow of the label
   `Bearing Capacity Equation, φ = 49.5°` points at it; the arrow head touches the line at about
   (1830, 2845). Style and arrow agree with series.csv.
5. No plotted symbols on this figure: no `marker` rows.
6. The printed subscript in the slope label reads like a `g` (`AγN_g`); the next line of the
   text block prints `∴ N_q = 316/Aγ`, so it is the same quantity; the id `fit` and the note text
   `Nq` follow series.csv.

## Where lines cross or run together (bounds widened, noted in `note`)

1. lpt74 and the fit line, v 3456 to 3495 (pen 0.4 to 0.53): the thin trace comes in from the
   right at pen 0.4, runs along the right edge of the thick fit line (the merged run is 18 to 24 px
   wide instead of 15) and emerges above it at (1650, 3454). Its first load peak (knee, about
   850 lb at pen 0.53) is at the edge of the thick line, so its u is known only to about 6 px.
   The pen 0.50 sample is inside the merged ink (u bound 10 px).
2. lpt74 and lpt75, v 2896 to 2910 (pen 2.3): the thin trace crosses the thick one; the thin
   line is hidden over 15 rows, its centre there is interpolated (no sample falls in it).
3. lpt74 gap under the label, v 2921 to 2981 (pen 2.05 to 2.25): the thin line stops at
   (1520, 2921), just below the thick lpt75 line, and reappears at (1560, 2982) just above the
   pen 2 grid line; the text `No.` of the lpt75 label sits in between. No ink was found in the gap
   by 2 px row scans. The pen 2.25 sample sits on the last ink before the gap (v 2919). Nothing
   is interpolated across the gap.
4. lpt75 and the fit line, v 2612 to 2730 (pen 2.9 to 3.27): the thick trace joins the fit line
   from the right at (1046, 2725), runs with it (merged run 18 to 24 px) and leaves it to the right
   at (960, 2613). The pen 3.00 and 3.25 samples are the centre of the merged run with half the
   merged width as bound; the fit line's pen 3 crossing is taken from the least-squares line
   through its whole ink (bound 10 px) because no clean rows exist around that grid line.
5. Both straight lines are read locally: the fit line bows by up to 5 px over its length
   (residuals of a single straight fit: +4.8 px at the top band, -2 px in the middle, rms 1.7 px),
   so each crossing of a penetration line is the ink centre fitted through the 48 rows around the
   grid line, and the lower end is extrapolated from the 20 clean rows above the axis. The bce line
   is straight to 0.75 px rms.

## Sampling

1. Trace samples every 0.25 in of penetration, located with the piecewise penetration between
   the detected grid lines (so the integer samples sit on the grid lines; those rows are noted).
2. Bounds: half the row run and half the column run of the ink through each sample, measured
   there (rule 7). On the near-horizontal stretches (lpt74 below pen 0.3, lpt75 below pen 2.6)
   the row run is 30 to 40 px, so the load bound is 15 to 20 px (20 to 27 lb): the load rises
   steeply there and the ink is at a shallow angle to the rows. Where the run is merged with a
   grid line or another line the bound is half the line's typical width and the note says so.
3. lpt74 is monotone in penetration throughout (the hump at pen 0.5 to 1.0 is a drop in load,
   not a return), so drawing order and penetration order agree. lpt75 likewise (its hook at pen
   3.3 to 3.7 is a load drop).
4. The maximum load of both traces is at their last point (lpt74 1770 lb, lpt75 1800 lb at pen
   4.48); `peak` and `last` features are written as two rows at the same pixel.
5. Knees recorded: lpt74 first peak (pen 0.53), local minimum (pen 1.0, rightmost point of the
   hump), two steps at constant penetration (pen 3.5 and 4.0, about 25 to 30 lb each), a short
   vertical run before the final rise (pen 4.2); lpt75 joining the fit line (pen 3.27 on leaving,
   local maximum), the hook minimum (pen 3.65). The traces carry many smaller recorder wiggles
   (5 to 15 lb) that are not listed.

## Ambiguities and remarks

1. The first ink of lpt74 is merged with the load-0 axis line for about 50 px from the corner
   (u 2255 to 2305); the first point is put at u 2290 with a 10 px bound.
2. The first ink of lpt75 is at the right frame line on the pen 2 grid line (load 0, pen 2.01);
   from load 0 to about 300 lb the thick trace is drawn on the grid line itself.
3. The label centres (`feature`, note `label: ...`) are the centres of the rotated text blocks
   (fit label u 598 to 672, v 1240 to 2035; bce label u 1845 to 1885, v 1770 to 2790); the bounds
   are the half extents of the blocks.
4. The fit line's lower end and the bce line's lower end are where their ink meets the axis line
   (the pen 0 grid line centre); the `intercept` features are the same points. Values: fit 721 lb
   (the page prints `Intercept = 720 lbs.`), bce 284 lb.
5. Rows flagged `extrapolated x` by the piecewise tool: the points on the pen 0 axis (0.0002 in
   beyond the verified line, immaterial), the bce upper end and the label centres above pen 5.

## Files

`cal-p1/` (anchors.csv, calibration.json), `cal-p1-alt6/` (diagnostic, frame top as 6),
`calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv` (piecewise values, D-025),
`points-p1-native-affine.csv` (affine `apply`, for comparison), `overlay-p1.png`, `centerlines.csv`
(the traced centrelines, for the overlay check only), `read_f233.py` and `scan_rows.py` (helpers),
`crops/` (zoomed crops and overlays used while reading).
