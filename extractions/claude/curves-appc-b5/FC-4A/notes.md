# FC-4A, blind reading (Claude), batch curves-appc-b5

Page `packet/p0126.png` (AM-68-1 Vol. II, Figure C-4A, printed C-12, PDF 126), 300 dpi, unrotated.
One upright panel: tau (PSF) 0 to 8000 against sigma (PSF) 0 to 5000. Legend "RC2 Soil": open
square = "gamma = 81.8 Lb./Ft.^3 (Dr = .95)", open circle = "gamma = 58.7 Lb./Ft.^3 (Dr = 0)".
The printed Dr values match the given ids `dr95` and `dr0`; nothing to correct.

## Calibration (`cal-p1/`)

Command: `calibrate_axes.py detect packet/p0126.png --box 900 1145 2400 3510 --x-values
0,1000,...,5000 --y-values 0,1000,...,8000 --frame-frac 0.8`.

1. The figure has no grid, only tick marks, so the four frame lines are the only detected lines and
   every interior line is `predicted`. RMS residual x 0.73 psf, y 0.47 psf (max 1.55, 1.11).
2. A first run with the default `--frame-frac 0.5` took the legend box's bottom edge (v 1485) as
   the 7000 line (y RMS 29 psf). It was discarded; requiring 4 of 5 bands removed the legend edge.
3. By-eye check (`calibration-eye-checks.csv`; all ticks measured, y 2000, 5000, 7000, 8000 and
   x 1000, 3000, 5000 also looked at on zoomed crops). The frame lines carry 0/8000 and 0/5000 (the
   5000 tick continues the right frame line; the 8000 label sits beside the top frame like the
   other labels beside their ticks). The ticks are not all on the frame-interpolated positions:
   - y ticks 1000 to 7000 are evenly spaced (291.8 px per 1000) but the top frame is about 10 px
     lower than that spacing puts 8000. The tool's 7000 line is 9.2 px below the 7000 tick
     (tool reads the tick as 7032, 0.40 percent of span), 6000: 8.3 px (0.36 percent).
   - x ticks 2000, 3000, 4000 are 6.9, 6.0, 5.5 px right of the tool's lines (tool reads them as
     2023, 2020, 2019; 0.47 percent of span at 2000); x tick spacing itself is irregular
     (292, 297, 290, 290, 285 px).
   All are under the 0.5 percent threshold, so the tool map is kept. A tick-based map (checked, not
   used) would shift the markers by -9 to -11 psf in sigma and -4 to -31 psf in tau (largest at the
   top of the Dr .95 series). Whether the frame or the ticks are the truer drawing cannot be told
   from the page.

## Which line carries which angle

1. "53°" (label center u 1587.5, v 2037.5) is printed along the upper line, just above-left of it
   near sigma 2300; that line runs through the squares: **dr95 = 53°**.
2. "43°" (label center u 1802.5, v 2571) is printed along the lower line, above-left of it near
   sigma 3000; that line runs through the circles: **dr0 = 43°**.
3. Check from my own trace samples: slopes 53.3° (dr95) and 43.3° (dr0) in the tool calibration.
   Intercepts: dr95 1672 psf, dr0 122 psf.

## Symbols

5 squares (dr95) and 5 circles (dr0); every symbol matches the legend shape of the line it
belongs to, so no series was assigned against the legend. No other symbol-sized ink in the panel
(connected-component scan): the specks at (948, 2500) and (1080, 2552) are 5 to 9 px dots, not
symbols. No symbol is hidden under a line (no width bulges along either line other than the ones
listed below).

Position of the symbols relative to their own line (tau minus line, tool calibration):
dr95: -181, +454, -16, +464, -580 psf; dr0: -54, +189, -120, +39, +46 psf. The dense line has a
large scatter: the 4th square (sigma 3812, tau 7257) is clearly above the line and the 5th
(sigma 4667, tau 7362) clearly below its dashed extension. Note: the packet's figures index row
says "the two highest dense points lie below the line"; on this page only the highest-sigma one
does, the other is about 460 psf above.

## Drawing of the lines (what is solid, what is dashed)

dr95: five dashes from the shear-stress axis to u 1109 (sigma about 650); solid from u 1126 with
breaks at u 1462-1491 (beside square 2), 1750-1792 (square 3 sits in this break) and 2074-2094
(sigma about 3950-4020, no symbol in it, near the foot of the perpendicular from square 4); then
a solid piece u 2095-2176; then short regular dashes from u 2186 (sigma about 4330) that cross the
top frame and end at u 2381, v 1047, i.e. at sigma about 5000, tau about 8410, outside the frame.
The piece u 2095-2176 (82 px wide) is four times the length of the upper dashes (20 to 25 px), so
I treat it as solid; it could be read as a long first dash. Samples on it are not marked dashed.

dr0: four dashes from the axis to u 1082 (sigma about 550); solid from u 1093, with breaks at
1460-1470 (beside circle 2), 1750-1773 (beside circle 3), 2024-2054 (circle 4 sits in it), a 4 px
break at 2101-2104, and the solid ends at u 2281 against circle 5; then two dashes, the last
running into the right frame line (sigma 5000). Nothing is drawn beyond the frame.

## Trace samples

1. Line center = middle of the vertical ink run in the sampled column. Bound 4.5 px in u and v,
   half the perpendicular line thickness (measured 9.0 px dr95, 8.8 px dr0).
2. Where the 250 psf column falls in a dash gap, a line break, a rounded dash end or on a symbol
   outline, the sample is taken at the nearest full-width ink column and the note says so
   (dr95: sigma 250, 500, 3000, 4000, 4500; dr0: sigma 250, 750 (circle 1), 4750 (circle 5)).
3. Left ends = intercept features: the straight centerline of the left dashes carried to the
   calibrated sigma = 0 line. At the junction the dash ink is a little off that line (dr95: ink
   v 2984-3001, center 2992.5, about 8 px above the extrapolation; dr0: about 3 px above), so the
   v bound of these points is widened to 8 px (dr95) and 6 px (dr0).
4. Right ends: dr95 = tip of the last dash (sigma 5004, tau 8411, above the frame); dr0 = dash
   centerline at the right frame (sigma 5000, tau 4825). Each also serves as the 5000 psf sample.
5. Counts: 21 trace samples per line (left end, 250 to 4750 every 250, right end).

## Ambiguities and stray ink

1. Circle 1 (dr0, sigma 774, tau 792) touches the line from below; its top arc is under the line
   ink. Center from the left, right and bottom arcs and the height of the other circles; bound
   3 px (u), 4 px (v).
2. A thin horizontal stroke (v 2389-2395, u 2054-2112) leaves the dr0 line to the right of circle 4,
   like a short leader. Not a symbol, not read.
3. Small strokes next to symbols: a tick left of square 1 (u 1120-1122, v 2765), an L-shaped foot
   at the end of the last left dash of dr95 (u 1087-1103, v 2787), a tick under the dr0 line start
   right of circle 2 (u 1483-1489, v 2935). Not read.
4. Squares 3, 4, 5 are imperfectly printed (broken top or bottom edges); their sides and corners
   are clear, center bound 2 px.
