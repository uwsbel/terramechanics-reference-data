FC-8, panel 1, page image p0138.png. Independent reading using only packet/ and the supplied tools; no other reading consulted. Both point CSVs contain the same pixel readings and piecewise values in psf. No SI conversion. Series id retained: rs-loose. Printed group: RS LOOSE (case as in the box); the index identity agrees with the page.

Printed box values, transcribed as printed:
Avg. Density = 40.40
Angle of Friction = 38.63
Tan Theta = .7992
Cohesion = 242.12

Both axis titles print (x 10^1). A printed 100.00 is 1000 psf. Plot range: normal stress 0–7000 psf, shear strength 0–8000 psf. The box top is not the 800.00 grid line. By-eye checks: x 00., 300.00, 700.00; y 00., 400.00, 800.00. Checks identify the actual grid/frame line beside each label, not the label baseline. All 8 vertical and 9 horizontal lines are detected and verified against ink; none predicted or rejected. See cal-p1/knots.json for each ink check and location error. Affine RMS residuals: x 4.008 psf, y 10.432 psf; maximum residuals x 8.801, y 21.370 psf, below 0.5% of the respective spans. Final values use verified piecewise knots with each line's tilt. Bounds propagate pixel intervals and bracketing-line location intervals; the global affine residual is not added. Maximum affine-versus-piecewise sensitivity over this series: x 4.341 psf, y 14.913 psf (diagnostic, not added to bounds).

6 triangle-up markers. Marker numbers identify visible symbols in the inspection crops; they are not individual test identities. Each centroid is the mean of three reconstructed core vertices saved in triangle-vertices.json, excluding fit-line, grid and stray ink. Clean marker bounds: u ±2 px, v at least height/6 (rounded up to 5 px); grid-obscured centroids widened to u ±5, v ±8 px. Symbol/fit-line mergers have half-symbol bounds. No two triangles can be distinguished at the same symbol location, and no extra symbol is inferred. All markers use the sole series in series.csv; rule 9 provides no competing series to resolve, and no unavailable data-sheet reading was consulted.

11 trace samples, in drawing order from left endpoint, at each available 500 psf normal-stress increment, then right endpoint. All submitted samples lie on diagonal stroke ink; grid-crossing centres are reconstructed from nearby visible diagonal ink. Typical stroke cross-section is 15 px vertically: trace bounds are half the local vertical thickness and half the horizontal thickness (vertical thickness / absolute pixel slope). Rounded caps use their observed narrower cross-section. These are reading bounds, not standard deviations. No requested 500 psf location is omitted.

The line reaches the normal-stress-zero axis. Its first point and intercept share the same reconstructed stroke/axis junction, not the nearest triangle. Features: first point, last point (also the maximum of this increasing line), and intercept; no knee is visible.

OLS slope of the submitted piecewise trace samples = 0.799953. Difference (reading − printed Tan Theta .7992) = +0.000753. A conservative first-order slope reading interval from all x/y bounds is ±0.032396; this is not a regression standard error. Fitted y intercept of the samples = 243.226 psf (diagnostic). Direct zero-axis intercept reading = 251.277 ± 27.952 psf. Difference (direct intercept − printed Cohesion 242.12 psf) = +9.157 psf. The printed cohesion is compared directly in psf, not multiplied by the axis-label factor. No coordinates were adjusted to the printed slope or cohesion.

Ambiguities: Marker 4: Vertical and horizontal grid lines touch triangle; vertices reconstructed from visible sides. last point; peak of monotonically increasing straight trace; diagonal endpoint merges with 400.00 horizontal grid, no diagonal ink continues above it

Boundary flags: trace 1, feature 1, feature 3. Zero-axis endpoint/intercept intervals extend across the outermost verified x line, hence the tool conservatively marks them extrapolated even when the centre is on zero. This is a boundary-interval flag, not an unsupported interior grid.
