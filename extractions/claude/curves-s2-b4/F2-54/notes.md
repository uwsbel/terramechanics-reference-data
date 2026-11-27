# F2-54, Claude reading (batch curves-s2-b4)

Figure 2-54, "Typical DPT Signatures", printed page 2-92, PDF page 117 (`packet/p0117.png`),
printed sideways. Pixel coordinates are those of the unrotated page. Upright, time runs up the page
(v decreasing) and deceleration increases to the left (u decreasing).

## Files

1. `points-p1.csv`, `points-p2.csv`, `points-p3.csv`: the reading (pixels, bounds, notes).
2. `points-p<n>-native.csv`: the same rows through `tools/calibrate_axes.py piecewise cal-p<n> ... --image packet/p0117.png`;
   `x_native` in ms (the task's convention), `y_native` in g.
3. `cal-p1/`, `cal-p2/`, `cal-p3/`: `anchors.csv` and `calibration.json` (hand-made tick calibration in the
   tool's layout, with `box`), `knots.json` (the tool's ink check of every anchored line and tick).
4. `calibration-eye-checks.csv`: every timing line, labeled tick, the minor-tick counts, the dashed lines
   and the scale bar, with the by-eye check and the tool's ink-check result.
5. `overlay-p1.png`, `overlay-p2.png`, `overlay-p3.png`: `tools/plot_grid.py overlay` of each panel.
6. `work/`: helper scripts (`build_cal.py` calibration, `tracer.py` and `trace_panels.py` centerline
   tracking, `sample.py` and `features.py` sampling, `eye_checks.py`, `ink_check.py`, `check_knots.py`)
   and the zoomed crops looked at.

Counts: panel 1, 77 trace samples (10 of them at g levels) and 9 features; panel 2, 80 trace
samples (14 at g levels) and 10 features; panel 3, 96 trace samples (27 at g levels) and 8 features.

## What the page prints, against the task's description

1. Panels, records and labels agree with the task and with `series.csv`: Record No. 53958, 2' Box,
   RS-Loose, 41.1 PCF (top, `r53958`); Record No. 54025, 2' Box, RS-Intermediate, 44.1 PCF (middle,
   `r54025`; the last letter of "Intermediate" is cut by the box edge); Record No. 54-65, LPT No. 26,
   RS-Dense, 52.0 PCF (bottom, `r5465`). Rulers: 0, 10, 20; 0, 10, 20, 30; 0 to 80 by 10, as stated.
2. **The dashed line is not at the rulers' zero.** The task calls it the dashed zero line (0 g). On
   the page, each ruler's "0" label, the end of its spine and the spacing of its ticks all put 0 g on
   the trace's pre-impact baseline, and the dashed line runs 7 to 12 px to the left of it (upright:
   above it). On each panel's own ruler the dashed line sits at +0.72 g (panel 1), +0.91 g (panel 2)
   and +0.94 g (panel 3), constant along its length. Evidence, panel 3: ticks at 10, 8, 6, 4, 2 g are
   at u 2232.5, 2256.5, 2280.5, 2301.5, 2322.5 (22 to 24 px apart); the next 2 g step lands at u 2345,
   where the baseline is (ink center 2346.8) and the "0" label is centered (2344), while the dashed
   line is at u 2335.6. Panels 1 and 2 are alike (2 g tick to baseline 22 px and 16.5 px; to the dashed
   line 14 px and 8 px). I calibrated on the ruler ticks only and did not anchor the dashed line. A
   reading that anchors the dashed line at 0 g will come out lower than mine by about 0.7, 0.9 and
   0.9 g in panels 1, 2 and 3, and its scale between 0 and 2 g will differ. Not from the corpus, an
   interpretation only: a strain-gage accelerometer reads 0 g in free fall and 1 g at rest, so a
   reference line about 1 g above the free-fall baseline could be a rest line; the traces do not all
   settle on it (panel 1 ends near 0.5 g, panel 2 near 0 g, panel 3 near 1 g).
3. The rulers' zero ticks are hidden under the baselines: the trace's baseline runs straight through
   the place of the 0 tick in all three panels and is interrupted by the "0" labels. I anchored the 0 g
   tick at the center of the baseline's ink in the tick band (u 859.6, 1330.0, 2346.8 at v 2650). The
   tool's ink check verifies it (it is the baseline's ink), but its true place is known only to about
   half the 7 to 9 px ink width, 0.3 to 0.4 g. Near-zero values carry that extra uncertainty.
4. Panel 2's ruler is drawn unevenly: 30 to 20 g spans 107 px, 20 to 10 g 112 px, 10 to 0 g 105.5 px,
   the 29 and 28 g ticks are 7 px apart, and the last 2 g step (2 to 0 g) is 16.5 px against 21 to 23 px
   for the others. The "0" label is centered on the baseline (u 1330), so the zero stays where it is
   printed; the affine residual of that tick is -0.42 g (1.4 percent of the 30 g span), above the
   protocol's 0.5 percent, and is drafting, not misplacement (the rms over all 30 ticks is 0.13 g).
5. The tool's ink check rejected three of panel 2's ticks that are clear by eye: 2 g (u 1313.5; the
   check's window reaches the dashed line 6 px away), 11 g and 29 g (short ticks whose stubs found the
   neighboring long tick 7 to 9 px away). By the rule they are not knots, so panel 2 is interpolated
   between the 0 and 3 g ticks there; at the 2 g tick's position that map gives 1.74 g, so panel 2's
   values between 0 and 3 g may read up to about 0.26 g low. This is inside their bounds (0.6 to 0.8 g).
6. Panel 1's main peak (20.08 g) lies just beyond the ruler's top label (20 g) and is flagged
   `extrapolated` by the tool; panel 2's peak (29.4 g) is just inside its 30 g tick; panel 3's (77.8 g)
   between its 78 and 80 g ticks.

## Time: scale bar and convention as applied

1. Scale bar: the arrows marked ".01 sec." (u about 1775) meet two adjacent timing lines, the line at
   v 2105 and the line at v 2256 at that u (my 40 and 30 ms lines); checked by eye on a zoom 3 crop. One
   interval between timing lines is therefore 10 ms.
2. Convention: 0 ms is the timing line on which the three rulers' labels are printed (the line runs
   through "20-10-0", "30-20-10-0" and "80-70-...-0"; at the traces it is at v 2721.8, 2716.5, 2706.6
   in panels 1, 2, 3). Lines up the page are +10, +20, ... ms; down the page -10 and -20 ms. The rulers'
   spines (v 2610 to 2620) lie between my 10 ms and 0 ms lines, and their ticks hang toward the 0 ms line.
   If the convention was meant for the line on the other side of the spines (where all three traces
   leave zero), every time in this reading is 10 ms too large.
3. Twelve lines are anchored in each panel's `cal-p<n>/`: -20 to 80 ms and the top frame line as 90 ms.
   The frame is drawn twice as thick (8 px) but lies 156 to 157 px above the 80 ms line, inside the
   spread of the other intervals (149 to 164 px), so it is taken as the 90 ms line; the traces' ink ends
   in it. The intervals are uneven, the same pattern in all three panels (at the traces, from -20 ms up:
   about 157, 152, 152, 149, 156, 150, 157, 156, 163, 162, 157 px), so it is in the drawing, not a
   misreading; the affine time map therefore has a residual of 0.44 ms rms (max 0.71 ms, 0.65 percent of
   the 110 ms span), and the values come from the tool's piecewise map between the lines, which follows
   the drawing. Every timing line passes the tool's ink check (location errors 0.50 to 0.84 px).
4. The first timing line right of the break marks is the -20 ms line in all three panels (break marks
   at v about 3135 to 3200, the next line above them at v 3017 to 3031). Nothing left of it was read.
5. All three traces leave zero at the 10 ms line (onsets at 10.07, 9.94, 9.92 ms).

## Deceleration calibration

1. The scan is rotated by about 0.7 degrees: page columns are not lines of constant g. The dashed line
   of each panel is straight over its whole length (rms 0.56 to 0.81 px) with du/dv = +0.0120, +0.0127,
   +0.0123; that tilt is taken as the direction of constant g, and the ruler ticks (all at v 2620 to
   2650) are carried up and down the page along it. Without it a value near the top of a panel would
   move by about 12 px, 1 g. The tool's piecewise map then interpolates between the verified ticks.
2. Affine residuals of the tick fits: panel 1, 0.053 g rms (max 0.095 g); panel 2, 0.134 g rms (max
   0.42 g, the 0 tick, item 4 above); panel 3, 0.109 g rms (max 0.23 g). Verified ticks: 11 of 11, 27
   of 30, 23 of 23.

## Sampling as applied

1. Trace samples are crossings of the traced centerline with lines of constant time (and, on the
   rise and fall, of constant g): every 2 ms from -20 to 0 ms, every 0.5 ms from 8 ms (2 ms before the
   onset) to about 5 ms after the main peak (to 17.5, 18.0 and 20.0 ms in panels 1, 2, 3), every 1 ms
   from there to 20 ms, every 2 ms from 22 to 88 ms, and the end at the 90 ms frame. On the rise and fall, a sample
   every 2 g (panels 1, 2) or 5 g (panel 3) where the local rate makes that finer than 0.5 ms.
2. Not sampled: 2, 4 and 6 ms in every panel (the baseline runs under the ruler's 0 tick, spine and "0"
   label); 0 ms in panel 3 (inside the "0" label); 10 ms in panel 1 (a visible white gap in the drawn
   line at the onset, see below).
3. Bounds: half the stroke's normal width where the sample is taken (chord length times the cosine of
   the local slope), 3.5 to 5.5 px typically; +2.5 px where the trace runs on or against the dashed line
   or on a timing line's ink, or is interpolated across a timing line (each such note says which); the
   hand-read tips and corners carry their own bounds (below).
4. The rows of the CSVs are in drawing order, features interleaved with the trace samples at their
   places along the trace; every feature note begins with its role word.

## Where the trace is hard to follow

1. Onsets. Each onset corner sits where the 10 ms timing line and the dashed line meet. Panel 1: the
   corner itself is not inked; the timing line is broken from u 843 to 855 and the baseline's last ink
   (u 856 to 860, v 2574) and the rise's first ink (u 844 to 846, v 2563 to 2566) are separated by a white
   gap of about 10 px. The onset feature is placed in the gap with bounds 6 px by 5 px that cover it, and
   no trace sample is taken there. Panel 2: the baseline's free edge drifts left from u 1332 (v 2592) to
   1324 (v 2570), about 0.5 g in the 1.3 ms before 10 ms, then the trace turns along the timing line's ink;
   the rise runs on the 10 ms line's ink up to about 7 g (center from the free edge). Panel 1's rise runs
   on the same line's ink up to about 4 g. Panel 3's corner is under the 10 ms line, 10 px right of the
   dashed line.
2. Tips. The rise and fall bands merge near each tip. The peak is read as the outer ink edge plus half
   the 9 px stroke (u 647.5 + 4.5, 1005.5 + 4.5, 1458.5 + 4.5). Panel 1's tip is a short flat stretch of
   ink 20 px long (v 2524 to 2544), so its time is uncertain by about 0.7 ms; samples at 12.5 and 13 ms
   there are interpolated through the hand-read tip.
3. Panel 3's fall ends at the junction of the 20 ms timing line and the dashed line; the bend is hidden
   there (feature `knee` at 20.05 ms, bounds 6 px by 5 px).
4. Late parts on the dashed line: panel 1 from about 68 ms, panel 2 from about 60 ms, panel 3 in
   stretches from about 52 ms, and panel 2's whole baseline, run on or against the dashed line, whose ink
   merges with the trace's. There the center is taken from the trace's free edge and the stroke width, and
   the bound is widened.
5. Small steps (about 1 px) at some timing-line crossings look like the trace being drawn in pieces
   between the lines; they are inside the bounds.

## Features and other ambiguities

1. Broad extrema: panel 1's second peak (9.18 g near 31 ms), panel 2's second peak (7.19 g near 29 ms)
   and minimum, panel 3's shallow minimum (-0.37 g near 29 ms, within half a stroke of that level from
   about 22 to 45 ms) and late hump (1.80 g near 84 ms) are flat over several ms; their time bounds are
   wide on purpose (for a peak only the deceleration is an observation).
2. Knees other than the onset and the extrema come from the break of a two-line fit to the centerline
   inside a stated window; they are where the bend is clearest on the page (checked on zoomed overlays),
   placed to a few px along the curve, and their bounds include that.
3. The pre-impact baselines read -0.1 to -0.2 g (panel 1), +0.1 to +0.5 g (panel 2) and -0.1 to 0 g
   (panel 3) on their rulers: the baseline wanders by 1 to 4 px about the hidden 0 tick.
4. Context only, not a reading issue: PDF 115 (printed 2-90) gives a mean peak of 11.76 +/- 0.14 g for
   the first 49 RS-loose beds of the subscale drag test bin; the RS-loose record of this figure peaks
   near 20 g. The figure calls its records typical; a reader comparing the two might suspect the ruler,
   but the ruler of panel 1 reads cleanly (ticks every 2 g, 10.2 px per g, labels on their ticks).
