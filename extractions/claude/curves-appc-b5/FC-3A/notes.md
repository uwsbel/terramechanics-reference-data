# FC-3A, panel 1: Claude reading (batch curves-appc-b5)

Source: AM-68-1 Vol. II (NASA CR-92215), Figure C-3A "Failure Envelopes - Maximum Shear Stress vs.
Normal Stress", printed C-9, PDF page 123, image `packet/p0123.png` (3213 x 4508 px, 300 dpi,
unrotated, upright figure). Pixel coordinates are (u right, v down) on that image.

## What is on the page

1. One panel, x = sigma (PSF) 0 to 5000, y = tau (PSF) 0 to 6000. No grid: only the axis lines, a
   top and a right frame line, and tick marks (x ticks at 1000 to 5000 crossing the bottom axis; y
   ticks at 1000 to 6000 crossing the left axis). One "0" label under the origin corner serves both
   axes.
2. Legend as printed (box at the top of the plot, it hides the top frame line from u 987 to 2153):
   "RSM-a Soil"; open circle "gamma = 57.9 to 59.4 Lb./Ft.^3 (Dr = 0 to .15)"; open square
   "gamma = 75 Lb./Ft.^3 (Dr = 1.0 to 1.3)". The sign before the Dr values is printed as a bold "="
   (it may be an approximately-equal sign). These match `series.csv`: circles are `dr0-15`, squares
   are `dr100-130`. No id correction needed. The printed relative density above 1.0 ("1.0 to 1.3")
   is as printed.
3. Two straight lines, each solid between its first and last data symbols and dashed beyond:
   1. Upper line, printed label "47°", carries the five open squares, so it is `dr100-130`. The
      label (glyph box u 1594-1643, v 2182-2259, written parallel to the line) sits 65 px above this
      line and about 350 px above the lower one.
   2. Lower line, printed label "38°", carries the five open circles, so it is `dr0-15`. The label
      (glyph box u 1615-1676, v 2462-2538) sits 52 px above this line and about 245 px below the
      upper one.
   The denser group has the steeper envelope, as expected.
4. Every plotted symbol matches its legend shape and fill (all open). No symbol of another shape or
   fill sits on either line. No overlapping or hidden symbols. 5 squares and 5 circles, at the same
   five normal stresses (about 735 to 745, 1736, 2950, 3792, 4661 to 4667 psf).

## Counts in points-p1.csv (56 rows)

| series | marker | trace | feature |
|---|---|---|---|
| dr100-130 (47°) | 5 | 21 | 2 (intercept, label: 47°) |
| dr0-15 (38°) | 5 | 21 | 2 (intercept, label: 38°) |

## Calibration (cal-p1)

`tools/calibrate_axes.py detect packet/p0123.png --box 895 1430 2400 3230 --x-values
0,1000,2000,3000,4000,5000 --y-values 0,1000,2000,3000,4000,5000,6000 --bands 10 --frame-frac 0.2
--min-frac 0.4`

1. Why these settings: the top frame line (y = 6000) is hidden behind the legend for 80 percent of
   its length, so with the defaults it was not found. With 10 bands it is found in 3 bands (u 970,
   2170, 2322), at both visible ends, and its fit agrees with the printed 6000 tick within 1.9 px.
   The box top (1430) excludes the legend's top border; the legend's bottom border (v 1661) and
   text rows were dropped by the tool as not grid lines.
2. Residuals: x RMS 0.70 psf (max 1.51), y RMS 0.25 psf (max 0.61). These are small because every
   interior line is `predicted` (interpolated between the frame lines): there are no grid lines to
   detect, so the residual only measures the non-affinity of the frame, not the agreement with the
   printed scale.
3. Scales: 3.429 psf/px in x, 3.440 psf/px in y.

### Label and tick check (calibration-eye-checks.csv)

Each printed label was checked by eye on zoomed crops to sit beside its tick; the tick centres were
then measured on the pixels and mapped through cal-p1.

1. x axis: all six marks pass. Ticks 1000, 2000, 3000 within 1.5 px; 4000 is 3.7 px (12.6 psf,
   0.25 percent of span) right of the interpolated position; the 5000 tick is 2.9 px left of the
   right frame line.
2. y axis: **two labels fail the 0.5 percent rule.** The printed ticks for 3000 and 5000 sit 14.0
   and 13.1 px above the positions the frame-interpolated calibration gives them (48 and 45 psf,
   0.80 and 0.75 percent of span). The ticks for 1000, 2000 and 4000 are 6.8 to 7.7 px above (24 to
   27 psf, 0.39 to 0.44 percent, pass). 6000 (the tick joins the top frame line) and 0 (the axis
   line) pass. Every interior y tick is above the calibration's position, never below; read against
   cal-p1, the printed y ticks come out 23 to 48 psf high.
3. This is not page distortion. Both drawn lines are straight in pixels to 0.8 px RMS over their
   whole height (mean residual of every 150 px band below 0.9 px); a scan or copy distortion that
   moved the ticks by 7 to 14 px would bend the lines visibly. The y ticks of this hand-drafted
   figure (Appendix C, p0115: C-1A to C-7B are the original sheets, C-8 on are the computer plots)
   are simply placed irregularly: spacings from 0 upward are 298, 291, 297, 284, 296.5, 279.5 px.
4. The protocol asks to change the box or thresholds before reading points when a label fails.
   That cannot help here: the tool only detects lines that span the box, and this figure has no
   grid, so the interior y lines are always interpolated from the frame. I kept cal-p1 (the shared
   method, so the two readings stay comparable) and quantified the alternative instead (next
   section). The pixel readings in points-p1.csv do not depend on the choice.

### Sensitivity to the calibration choice (alt-ticks/, not the reading's calibration)

`alt-ticks/calibration.json` is an affine least-squares map fitted to the printed tick marks where
they meet their axes, plus the origin corner (12 anchors; x RMS 5.1 psf, y RMS 13.1 psf, max 27
psf), written by `helpers/alt_ticks_cal.py`; `alt-ticks/points-p1-native-ticks.csv` is the same
pixel reading converted with it. Against cal-p1:

1. every marker's y is 13 to 20 psf lower (squares 15.7 to 19.7, circles 13.3 to 14.9); x changes
   by 5 psf or less;
2. intercepts are 14 to 15 psf lower (47° line 523 -> 508, 38° line 255 -> 241 psf);
3. the angles of the drawn lines change by less than 0.1°.

Which map the draftsman's symbols follow cannot be decided from this page. Recommendation for the
reconciliation: compare the marker y values under both maps with the peak shear stresses tabulated
on the data sheets this figure is derived from (FC-3B, FC-3C per the figures index; not in my
packet, not looked at). Until then, treat the y values as carrying a possible systematic offset of
about 15 to 20 psf (up to 48 psf at an individual tick), which the `y_read_bound` from cal-p1 (RMS
0.25 psf plus the pixel bound) does not include.

## Points

1. Markers: centre of the outline's bounding box, read on pixel maps (`helpers/ascii.py`); outline
   extents are in each note. Outlines are 30 to 33 px. Bound 2 px for all ten: five symbols touch a
   line (squares 1, 2, 4, 5 and circle 1) but each outline is complete and separable from the line
   ink, so the centre is clean.
   1. Square 1 and circle 1 sit where their lines change from dashed to solid; square 5 sits where
      the 47° line changes from solid to dashed, and the next dash starts on its top edge.
   2. Square 2 and square 4 touch the 47° line with their lower-right corners (centres 19 and 23 px
      above the line); square 5 touches it with its upper-left corner (centre 20 px below).
2. Traces: column centres of the line's own ink, from the line's connected components with the
   touching symbols' outlines masked, using only columns whose ink run has the full line
   cross-section (not a dash tip, not cut by a mask, pin-holes of up to 3 px bridged), smoothed over
   +-5 columns. Line thickness 10.8 px (47° line) and 11.7 px (38° line); bounds 5.5 and 6.0 px.
   1. Left end (sequence 1) is on the shear-stress axis: the first dash of each line runs into the
      axis ink. It is the first dash's own centre line where it meets the x = 0 axis line, and it is
      also the `intercept` feature.
   2. Right end: the tip of the last dash, centre of its cap pulled back 3 px onto the ink. The 47°
      line ends at sigma 4918 psf, about 25 px short of the top-right corner; the 38° line ends at
      sigma 4965 psf, 5 px short of the right frame line.
   3. Samples every 250 psf in between. Where that abscissa fell in a gap, at a dash tip or on a
      symbol, the sample was moved to the nearest usable ink and the note says from where (47°:
      x = 250, 500, 750, 1750; 38°: x = 250, 500, 750, 3000, 4500, 4750). The largest moves are 47°
      x = 750 to 821 (square 1), 47° x = 1750 to 1690 (square 2) and 38° x = 3000 to 3062 (gap).
   4. Dashed parts, marked "dashed" in the notes: 47° line left of square 1 (u < 1118) and right of
      square 5 (u > 2266); 38° line left of circle 1 (u < 1120) and right of u 2237 (sigma about
      4470, before the last circle at 4667).
3. Features: `intercept` per line (above); `label: 47°` and `label: 38°` at the centre of the
   label's glyph box including the degree sign, bound 8 px.

## Ambiguities and other observations

1. Calibration in y (above): the printed y ticks disagree with the frame by up to 14 px. This is the
   main open item of this reading.
2. Drawn angles versus printed angles: fitted to the trace samples in calibrated units, the upper
   line is 47.85° (slope 1.105) and the lower 38.79° (slope 0.804), under either calibration
   (47.79° and 38.76° with alt-ticks). Both drawn lines are about 0.8° steeper than their printed
   labels (47°, 38°). Reported as found; the labels may be rounded down or computed from the data
   rather than from the drawn line.
3. Intercepts: 523 psf (47° line) and 255 psf (38° line) where the drawn dashes meet the axis. The
   straight fit of each line's whole ink meets the axis 1.8 and 3.0 px lower (about 517 and 245
   psf; a fit to the solid-part trace samples gives 515 and 243), so the first dashes sit very
   slightly above the solid line's extension; the difference is within the trace bounds.
4. The "solid" 38° line has three short breaks with no symbol in them, at u 1451-1467, 1779-1806
   (under circle 3) and 1953-1978 (pen lifts or symbol clearance; 15 to 27 px, much longer solid
   runs on both sides). The 47° line is interrupted at squares 1, 2, 4 and 5. These breaks are
   treated as part of the solid line; no trace sample is placed in them.
5. Not recorded as points: a short horizontal stroke at u 1217-1234, v 2969-2972 (sigma about 1040,
   tau about 800 psf, right of circle 1; 18 x 4 px, matches no legend symbol) and specks at
   (1110, 2555), (1438, 2188), (1011, 1873).
6. Small ink bump on the top edge of square 3 (u 1783-1785, v 2168-2169): ignored for its centre.

## Files

1. `cal-p1/` (anchors.csv, calibration.json): the tool's calibration used for the reading.
2. `calibration-eye-checks.csv`: every printed label of both axes against cal-p1.
3. `points-p1.csv`, `points-p1-native.csv` (cal-p1 applied with `calibrate_axes.py apply`).
4. `overlay-p1.png`: the reading drawn on the page.
5. `alt-ticks/`: the tick-anchored sensitivity map and the points converted with it (not for the
   diff; for the calibration question only).
6. `helpers/`: my scripts (components, line fits, traces, label check, points writer, ascii pixel
   maps). Run order: components.py (writes a label array, deleted after use for size), linefit.py,
   traces.py, write_points.py, eyecheck.py, alt_ticks_cal.py. `work/`: crops and intermediate JSON.
