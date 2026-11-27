F2-48, panel 1 — independent blind reading, batch curves-s2-b2

Evidence: packet/p0109.png, unrotated 300-dpi page; packet/p0105.png for setup only; packet/series.csv and CURVE-READING.md. No other reading or prior reading was consulted. Context describes the 4-inch cylinder/footpad comparison, including footpad shape, cylinder side friction and soil falling above the footpad; it supplies no plotted points.

Printed identity: solid = Four-Inch Cylinder (LPT No. 87), Gp = 45; dotted = Four-Inch Footpad (LPT No. 85), Gp = 46. These match the supplied series IDs. No plotted markers or straight fit lines.

The page is sideways: penetration increases up and load left. The last labelled penetration line is 8 inches; the unlabelled frame beyond it is not treated as a labelled 9-inch anchor. All labelled load lines 0 to 1200 lb in steps of 200 are anchored.

Important drafting irregularity: at the penetration-axis edge the 0-to-1-inch spacing is about 233 px, while 1-to-2 is about 316 px. The printed 0, 1, 2 and 8 numbers have each been checked against their own drawn line. A tighter-box, higher-threshold detection confirms the irregularity; changing a genuine unequal grid to make an affine residual small would change the reading. Consequently the affine penetration residual exceeds the protocol diagnostic threshold of 0.5 percent of span. Values use only verified tilted grid lines and piecewise interpolation; the affine fit is diagnostic, not used for reported values.

The solid trace rises steeply, has a shallow decreasing-load shoulder near 0.6 to 1.1 inches, and then resumes increasing; the decrease stays in drawing order. The dotted trace has a flatter initial shoulder. The traces meet in the obscured origin junction but do not cross later. The solid terminates just beyond the 8-inch line. The last dotted mark joins the 8-inch grid; the endpoint bound covers the unresolved cap rather than extending the curve into white space.

Reading method and bounds

Quarter-inch requests are nominal sampling positions (target_x_in), not observations. For dots/dashes I move to actual ink, so x_native need not equal target_x_in. First and last visible ink points are also trace rows, even when they fall between quarter inches. Each series has separate first, peak and last feature rows; coincident roles are separate rows at the same pixel. Knees include changes in slope and recorder jogs; small recorder roughness is not interpreted as physical soil behavior. There are no penetration unloading loops; the small load decreases are followed in their original traversal order. Sequence includes both trace and feature rows.

On clean solid segments, bounds come from the local normal ink half-width measured near that sample, not a fixed global width. Dot/dash bounds also include half the measured local repeat spacing along the trace, projected to page u/v. Intersections, recorder corners and unresolved frame/trace junctions receive wider bounds. Pixel bounds are symmetric reading bounds, not standard deviations. The native output uses piecewise interpolation with each verified line's tilt and location error; it propagates the pixel rectangle and bracketing-line intervals without adding the global affine residual. Native units: penetration inches; load pounds. No SI output was requested.

Calibration and verification

Final affine diagnostic residuals: penetration RMS 0.062555 in, maximum 0.148786 in; load RMS 0.944158 lb, maximum 2.601416 lb. Verified knots: 9 penetration, 7 load; 0 rejected in the final map. No predicted line is used as a knot. The independent numerical ink check for every grid line, its location error, and its samples are in cal-p1/piecewise-knots.json. Three printed labels per axis (four penetration labels on F2-48) were checked by eye in calibration-eye-checks.csv; calibration-label-crops.png retains the actual number/line evidence. Affine-versus-piecewise differences by series are in cal-p1/calibration-sensitivity.csv. 12 rows have an interval extending beyond a verified outer line, flagged in cal_model, including uncertain endpoints at a boundary.

Every regular sample was visually checked on magnified page crops; feature/endpoints were checked separately, and the final overlay was reviewed. The packet contains only calibrate_axes.py and plot_grid.py; check_trace_ink.py is not supplied. ink-distance-audit.csv is a supplementary raw-darkness/grid-exclusion check, not a claim of the project's D031 symbol/text-removal certification. The visual review is essential to distinguish label lettering, annotation leaders, frame/grid ink and each curve's own ink. No samples intentionally bridge blank dot/dash gaps.

Counts: lpt87: 34 trace, 17 feature, 0 marker; lpt85: 34 trace, 7 feature, 0 marker. Total 92 rows. All rows have panel = 1.

Deliverables: cal-p1/calibration.json, anchors.csv, piecewise-knots.json and calibration-sensitivity.csv; calibration-eye-checks.csv; points-p1.csv; points-p1-native.csv; overlay-p1.png; notes.md. Additional reading grids, labeled zoom crops, contact sheets, label crops and the ink-distance audit retain QA evidence. Helpers are in out/; tools/ is unchanged.
