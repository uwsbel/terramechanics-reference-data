F2-45, panel 1 — independent blind reading, batch curves-s2-b2

Evidence: packet/p0106.png, unrotated 300-dpi page; packet/p0105.png for setup only; packet/series.csv and CURVE-READING.md. No other reading or prior reading was consulted. Context describes the 4-inch cylinder/footpad comparison, including footpad shape, cylinder side friction and soil falling above the footpad; it supplies no plotted points.

Printed identity: solid = Four-Inch Cylinder, LPT No. 95, Gp = 16.2; dotted = Four-Inch Footpad, LPT No. 79, Gp = 15.2. These match the supplied series IDs. No plotted markers or straight fit lines.

The page is sideways: penetration increases up and load left. Penetration labels run 0 through 7. Load labels checked against their own lines include 0, 25, 50, 75, 100, 150, 200 and 250; the intervening 25-lb subdivisions are drawn. Calibration stops at the verified 250-lb line. The frame and cylinder continue beyond it; their load values are explicitly extrapolated from the final verified interval, rather than assigning 250 to the far frame. The cylinder reaches about 300 lb at the 7-inch end. The dotted trace ends just above 6 inches, around 177 lb.

The two records coalesce at the origin, then separate, with the solid cylinder carrying more load. Their origin location is hidden in the thick axes/trace junction and has widened bounds. The cylinder's terminal ink merges with the far frame; its endpoint bound includes that junction. The slight jagged shoulders on the solid line are recorder features, not fitted segments. The dotted line is sampled on actual dots, shifted from nominal quarter inches as necessary.

Reading method and bounds

Quarter-inch requests are nominal sampling positions (target_x_in), not observations. For dots/dashes I move to actual ink, so x_native need not equal target_x_in. First and last visible ink points are also trace rows, even when they fall between quarter inches. Each series has separate first, peak and last feature rows; coincident roles are separate rows at the same pixel. Knees include changes in slope and recorder jogs; small recorder roughness is not interpreted as physical soil behavior. There are no penetration unloading loops; the small load decreases are followed in their original traversal order. Sequence includes both trace and feature rows.

On clean solid segments, bounds come from the local normal ink half-width measured near that sample, not a fixed global width. Dot/dash bounds also include half the measured local repeat spacing along the trace, projected to page u/v. Intersections, recorder corners and unresolved frame/trace junctions receive wider bounds. Pixel bounds are symmetric reading bounds, not standard deviations. The native output uses piecewise interpolation with each verified line's tilt and location error; it propagates the pixel rectangle and bracketing-line intervals without adding the global affine residual. Native units: penetration inches; load pounds. No SI output was requested.

Calibration and verification

Final affine diagnostic residuals: penetration RMS 0.002501 in, maximum 0.005604 in; load RMS 0.175352 lb, maximum 0.473953 lb. Verified knots: 8 penetration, 11 load; 0 rejected in the final map. No predicted line is used as a knot. The independent numerical ink check for every grid line, its location error, and its samples are in cal-p1/piecewise-knots.json. Three printed labels per axis (four penetration labels on F2-48) were checked by eye in calibration-eye-checks.csv; calibration-label-crops.png retains the actual number/line evidence. Affine-versus-piecewise differences by series are in cal-p1/calibration-sensitivity.csv. 13 rows have an interval extending beyond a verified outer line, flagged in cal_model, including uncertain endpoints at a boundary.

Every regular sample was visually checked on magnified page crops; feature/endpoints were checked separately, and the final overlay was reviewed. The packet contains only calibrate_axes.py and plot_grid.py; check_trace_ink.py is not supplied. ink-distance-audit.csv is a supplementary raw-darkness/grid-exclusion check, not a claim of the project's D031 symbol/text-removal certification. The visual review is essential to distinguish label lettering, annotation leaders, frame/grid ink and each curve's own ink. No samples intentionally bridge blank dot/dash gaps.

Counts: lpt95: 30 trace, 25 feature, 0 marker; lpt79: 26 trace, 5 feature, 0 marker. Total 86 rows. All rows have panel = 1.

Deliverables: cal-p1/calibration.json, anchors.csv, piecewise-knots.json and calibration-sensitivity.csv; calibration-eye-checks.csv; points-p1.csv; points-p1-native.csv; overlay-p1.png; notes.md. Additional reading grids, labeled zoom crops, contact sheets, label crops and the ink-distance audit retain QA evidence. Helpers are in out/; tools/ is unchanged.
