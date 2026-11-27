# FC-11A, panel 1 — independent blind reading

Source: `packet/p0145.png`, unrotated 300 dpi; all u/v values refer to this original image (u right, v down). Only this packet and its protocol were used. Context p0115 describes the CAL-COMP computer envelopes and the final lettered plot as the combined test plot.

Printed box transcription (digits and leading decimal preserved):

- RSM Loose
- Avg. Density = 58.20
- Angle of Friction = 35.92
- Tan Theta = .7244
- Cohesion = 444.69

The page identity agrees with the supplied series id `rsm-loose`. Shape: triangle-up. No subdivision into the earlier test groups is inferred on the combined figure. There are 5 markers, 11 trace samples and 3 features (first, last/maximum, intercept). Marker sequence is a spatial inventory, not a reconstructed test chronology; trace sequence is left-to-right drawing order.

Both axes print PSF (x 10^1). Printed 100.00 = 1000 psf; x spans 0..7000 psf and y 0..8000 psf. The 00 labels belong to the bottom and left frame lines; the upper plot boundary is the 800.00 line, not the top of the parameter box. All axis labels (x 00 through 700.00 and y 00 through 800.00) were checked against their lines on label-sheet.png. The six requested recorded checks are x 100.00/400.00/700.00 and y 100.00/400.00/800.00 in calibration-eye-checks.csv.

Calibration: 72 measured grid intersections; all 8 x lines and 9 y lines detected, then independently ink-verified; no predicted or rejected lines. Affine diagnostic residuals: RMS x=3.841, y=10.016 psf; maximum x=9.685, y=19.496 psf. These are below 0.5% of each axis span. Values and bounds in points-p1-native.csv use the verified piecewise map and line-position errors, not the affine residual. Bounds propagate four corners/centre and bracketing-line intervals per D-025. Boundary features may be flagged extrapolated because their pixel bounds straddle x=0; this is not a claim that the drawn trace continues left of the axis.

Triangle centres are the arithmetic centroid of the reconstructed vertices in triangle-vertices.csv. Clean horizontal centre bounds are 2 px; apex-direction bounds are at least height/6. Touching/overlapping ink is noted per marker and bounds widened. Fits of visible side cores were checked on the enlarged original crops; the shared upper triangle in C-11B was reconstructed from its visible apex, right side and base.

Trace samples are on ink at the left end, each readable 500 psf normal-stress location, and the right end. The line is an increasing straight trace, so its maximum is its last feature. Median clean perpendicular line thickness is 9.50 px (51 clean sections); u/v bounds are 4.75 px, half the stroke thickness rounded upward to a quarter pixel. Endpoints are line ink, not symbol centres. The branch visibly reaches the x=0 axis; its intersection is the intercept feature. The first point was obtained at the measured ink branch/frame intersection. No printed fit parameter was used to position any point. The green overlay marks sampled ink only; a connection between two samples is not evidence of ink through a symbol-associated gap.

Reading against the printed computation: least-squares slope of the calibrated trace samples is 0.726833; printed Tan Theta is .7244; reading minus printed = +0.002433. Read intercept shear stress is 405.722 psf; printed Cohesion is 444.69 psf; reading minus printed = -38.968 psf. The regression intercept of all samples (399.716 psf) is a separate diagnostic and is not substituted for the directly read intercept. Piecewise calibration can introduce small drafting-related changes in the apparent slope at grid knots.

Ambiguities and limitations: Five distinguishable triangles. The fourth triangle is crossed by the y=3000 grid line; sides and base are reconstructed excluding the crossing line, with enlarged bounds. The line ends before the final triangle.

Files: cal-p1/anchors.csv, calibration.json and verified-knots.json; calibration-eye-checks.csv; points-p1.csv (pixels and reading bounds); points-p1-native.csv (same rows plus values/bounds in psf and cal_model); overlay-p1.png (full original page dimensions); notes.md; triangle-vertices.csv; line-thickness-checks.csv; calibration-sensitivity.md. Enlarged label, marker, triangle-fit, trace, endpoint and ambiguity crops/sheets are retained as inspection evidence. Red overlay = marker centroid, green = sampled trace, blue = feature. Pixel bounds are drawn as bars. Duplicate feature/trace coordinates have different roles and are not additional test observations.
