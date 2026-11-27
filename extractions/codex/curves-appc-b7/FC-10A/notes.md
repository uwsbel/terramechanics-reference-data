FC-10A, panel 1, page image p0142.png. Independent reading using only packet/ and the supplied tools; no other reading consulted. Both point CSVs contain the same pixel readings and piecewise values in psf. No SI conversion. Series id retained: ps-loose. Printed group: PS Loose (case as in the box); the index identity agrees with the page.

Printed box values, transcribed as printed:
Avg. Density = 25.90
Angle of Friction = 43.44
Tan Theta = .9471
Cohesion = 488.69

Both axis titles print (x 10^1). A printed 100.00 is 1000 psf. Plot range: normal stress 0–7000 psf, shear strength 0–8000 psf. The box top is not the 800.00 grid line. By-eye checks: x 00, 300.00, 700.00; y 00, 400.00, 800.00. Checks identify the actual grid/frame line beside each label, not the label baseline. All 8 vertical and 9 horizontal lines are detected and verified against ink; none predicted or rejected. See cal-p1/knots.json for each ink check and location error. Affine RMS residuals: x 3.457 psf, y 10.235 psf; maximum residuals x 6.137, y 18.713 psf, below 0.5% of the respective spans. Final values use verified piecewise knots with each line's tilt. Bounds propagate pixel intervals and bracketing-line location intervals; the global affine residual is not added. Maximum affine-versus-piecewise sensitivity over this series: x 5.120 psf, y 14.859 psf (diagnostic, not added to bounds).

6 triangle-up markers. Marker numbers identify visible symbols in the inspection crops; they are not individual test identities. Each centroid is the mean of three reconstructed core vertices saved in triangle-vertices.json, excluding fit-line, grid and stray ink. Clean marker bounds: u ±2 px, v at least height/6 (rounded up to 5 px); grid-obscured centroids widened to u ±5, v ±8 px. Symbol/fit-line mergers have half-symbol bounds. No two triangles can be distinguished at the same symbol location, and no extra symbol is inferred. All markers use the sole series in series.csv; rule 9 provides no competing series to resolve, and no unavailable data-sheet reading was consulted.

10 trace samples, in drawing order from left endpoint, at each available 500 psf normal-stress increment, then right endpoint. All submitted samples lie on diagonal stroke ink; grid-crossing centres are reconstructed from nearby visible diagonal ink. Typical stroke cross-section is 16 px vertically: trace bounds are half the local vertical thickness and half the horizontal thickness (vertical thickness / absolute pixel slope). Rounded caps use their observed narrower cross-section. These are reading bounds, not standard deviations. No requested 500 psf location is omitted.

The line reaches the normal-stress-zero axis. Its first point and intercept share the same reconstructed stroke/axis junction, not the nearest triangle. Features: first point, last point (also the maximum of this increasing line), and intercept; no knee is visible.

OLS slope of the submitted piecewise trace samples = 0.958199. Difference (reading − printed Tan Theta .9471) = +0.011099. A conservative first-order slope reading interval from all x/y bounds is ±0.036764; this is not a regression standard error. Fitted y intercept of the samples = 499.441 psf (diagnostic). Direct zero-axis intercept reading = 508.241 ± 29.040 psf. Difference (direct intercept − printed Cohesion 488.69 psf) = +19.551 psf. The printed cohesion is compared directly in psf, not multiplied by the axis-label factor. No coordinates were adjusted to the printed slope or cohesion.

Ambiguities: Marker 5: 400.00 horizontal grid line crosses apex; centroid reconstructed. Marker 6: Left side merges with rounded fit-line endpoint; widened to half symbol extent. last point; peak of monotonically increasing straight trace; rounded cap is left of final triangle apex; triangle outline excluded

Boundary flags: trace 1, feature 1, feature 3. Zero-axis endpoint/intercept intervals extend across the outermost verified x line, hence the tool conservatively marks them extrapolated even when the centre is on zero. This is a boundary-interval flag, not an unsupported interior grid.
