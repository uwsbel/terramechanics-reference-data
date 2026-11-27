# FC-14, panel 1 — LSM Loose

Independent blind reading from packet/p0150.png only, together with the supplied protocol, series index and context page p0115.png. No other reader or earlier extraction was consulted. Printed group identity agrees with series.csv; all symbols are upright hollow triangles assigned to `lsm-loose`. Context identifies C-8 through C-15 as Univac 1107 / CAL-COMP computer-plotted failure envelopes.

Printed box, transcribed as printed:

- Avg. Density = 75.20
- Angle of Friction = 43.95
- Tan Theta = .9642
- Cohesion = -109.97

Both axes print PSF (x 10^1). A printed 100.00 means 1000 psf. All native values and native bounds are in psf. The cohesion box is compared directly in psf, without the axis multiplier.

Calibration: 72 intersections; affine RMS residual x = 3.441 psf, y = 10.325 psf; maximum absolute residuals x = 6.082, y = 20.447 psf. All are below 0.5% of axis span. All 8 x grid lines and 9 y grid lines are detected and verified against distributed ink positions; none is predicted or rejected. `cal-p1/knots-verified.json` records the ink checks and line location errors. Numeric values use piecewise interpolation between these verified tilted lines; the affine map is diagnostic only, and its global residual is not added to reading bounds. Bound propagation is the supplied piecewise routine's corner/line-interval calculation. The `extrapolated` flags at frame features include any bound corner lying beyond an outer verified line, not necessarily a center outside the frame.

By-eye checks: x labels 100.00, 400.00, 700.00; y labels 100.00, 400.00, 800.00. Their checked line positions and psf anchors are in calibration-eye-checks.csv. Also inspected both zero labels and the whole frame: the labelled limits are x=0..7000 psf and y=0..8000 psf; the header box above y=8000 is not part of the data frame.

Counts for `lsm-loose`: 8 marker, 11 trace, 3 feature. Marker sequence follows their visible left-to-right placement; trace sequence follows drawing order from the left end. Trace samples are left end, 500..4500 psf every 500 psf, right end. The line has no separate knee or interior maximum; the final endpoint is also its maximum. Features duplicate the two trace endpoints and the x=0 intercept, as required.

Triangle centers are centroids of reconstructed side/base triangles, not bounding-box midpoints. marker-vertices.json records the visual reconstruction, and marker-centroids-inspection.png shows the reconstruction over the ink. Clean-marker x bounds are 2 px; vertical bounds are at least outer triangle height/6. Where another line touches the triangle, x/y bounds are widened to 6/8 px. These are uncertainty intervals, not standard deviations. No additional triangle can be distinguished in a stack, and no duplicate marker was inferred. Every identified symbol has its own visible outline.

Trace centers were read from diagonal ink, using nearby columns to separate the diagonal from a vertical grid line at fixed x. The trace inspection crops show every 500 psf sample. Sample bounds are half the local diagonal stroke thickness measured perpendicular to the stroke (about 4.4–6 px), not half a symbol's size; endpoints use 5.5 px. No sample falls in the white exclusion gap around a triangle.

Least-squares slope of the submitted trace samples (psf/psf) = 0.924592; printed Tan Theta = .9642; reading minus print = -0.039608. This is a diagnostic regression through sampled ink in the piecewise calibration; line grid-spacing irregularities need not produce a perfectly constant numeric slope. Its regression intercept (-12.69 psf) is not substituted for the directly read feature.

Direct intercept shear stress = 0.07 ± 21.14 psf; printed Cohesion = -109.97 psf; reading minus print = +110.04 psf. The point positions were not moved to agree with the printed computation.

Largest |piecewise minus affine| over submitted points for `lsm-loose`: x = 4.754 psf, y = 15.938 psf. This is a correlated calibration sensitivity, not an additional point bound.

Intercept ambiguity: the fitted stroke visibly joins the axes at the lower-left corner. The baseline and axis conceal the center over approximately one stroke width. The first point and intercept are recorded at that junction, y≈0 within the half-stroke bound; no negative shear value or invisible continuation is supplied. The centerline could meet the baseline slightly to the right of x=0 within this bound. This is the main reading ambiguity, and the printed negative cohesion does not settle it.
