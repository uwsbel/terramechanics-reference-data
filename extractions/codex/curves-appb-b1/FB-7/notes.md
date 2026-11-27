# FB-7: independent blind reading

Only packet/p0113.png, packet tables, and packet/CURVE-READING.md were used. Coordinates refer to the original unrotated 300 dpi image. No other reading was consulted.

## Calibration

All 9 x and 12 y knots are measured printed ticks or labelled frame lines. Tick stubs were sampled at 1 px intervals, each fitted independently with its own tilt. Opposite frame lines were also fitted independently. No interior knot was predicted from frame spacing. The native conversion is piecewise between these independently tilted lines; the affine map is diagnostic only.
Affine residual RMS: x=0.009927 psi, y=0.006620 kips/in.^2; maxima x=0.023697, y=0.019822. Every short tick is ink-checked at five positions along its actual stub; full frame lines use the protocol ink check. verified-knots.json records these checks and position errors. Bounds propagate the pixel rectangle and the bracketing line position intervals; global affine residual is not added.
Short tick strokes give limited leverage on their extended direction. Their independently fitted slopes are retained literally, rather than forcing parallel lines. calibration-sensitivity.csv reports affine minus piecewise values so the effect is visible. No inferred interior grid is treated as printed ink.
By-eye checks: x labels [0, 8, 16]; y labels [0, 6, 11]. All printed tick labels were also inspected in labels-all.png. See calibration-eye-checks.csv for the six requested checks.

## Series, symbols, and drawn lines

- dr104: printed "Dr = 1.04"; square with x; symbols only; no polyline was drawn for this group.
- dr99p5: printed "Dr = 0.995"; circle; polyline through 2 internal vertices.
- dr77: printed "Dr = 0.77"; filled circle; polyline through 2 internal vertices.

Markers were recorded before trace extraction. Clean marker centers have 2 px bounds; overlaps, missing arcs, or axis crossings have wider bounds stated per row. Legend symbols are not counted as measurement markers. Trace bounds are half the measured ink thickness (at least 3.5 px for the rasterized line core), without using symbol rims to extend a stroke. Features locate each first/last point, every bend, and the printed group label center. Hidden bends are features with wider bounds, not trace samples in white symbol interiors.

Requested samples blocked by symbols or missing line ink are listed in trace-omissions.csv (6 omissions). Rule 7 takes precedence over placing a trace sample on a symbol or in a white gap. trace_segment changes across a symbol obstruction; interpolation must not cross that break.

## Ambiguities

The isolated square-with-x immediately before "Dr = 1.04" at approximately (1805,1315) is the printed legend symbol, not a measurement. All other square-with-x marks, including ones touching the upper and lower polylines, belong to dr104 by the printed legend identity. The upper line carries Dr = 0.995 and open circles; the lower line carries Dr = 0.77 and filled circles.
At the left frame there are two open circles near v=3019 and 3067, a square near v=3091, a square near v=3364, two overlapping filled circles near v=3474 and 3495, and one filled circle near v=3848. The two filled lobes are separately identifiable but their centers have 10 px bounds. The line origins merge with the axis/symbol ink and their hidden continuation cannot be separated; the trace starts at the first identifiable diagonal stroke.
The printed 7 on the y axis is thin/broken but the 6–8 spacing confirms it. The ticks at y=1, 2 and 3 were measured on their clear right tips beyond the overlapping oblique line/square symbols.

## Files

points-p1.csv; points-p1-native.csv; overlay-p1.png; calibration-eye-checks.csv; trace-omissions.csv; cal-p1/calibration.json; cal-p1/anchors.csv; cal-p1/tick-fits.csv; cal-p1/verified-knots.json; cal-p1/line-fits.csv; cal-p1/labels-all.png; cal-p1/calibration-sensitivity.csv. Helpers and enlarged coordinate crops are retained under out/.

Counts: {"dr104": {"marker": 9, "feature": 1}, "dr99p5": {"marker": 7, "feature": 5, "trace": 10}, "dr77": {"marker": 9, "feature": 5, "trace": 12}}

Axis-label registration: several y-label glyph centers sit modestly below their tick, and terminal x labels can sit inward of the frame corner. Values were assigned from the printed ordered sequence and measured tick ink, never from the text center. Frame label checks use the actual bottom/left frame intersections.

Final QA: enlarged trace-ink-checks.png reviewed against the source; all stored trace centers lie on dark line ink. Clean closed-circle centers were checked against their white interior extents (out/center-refinements.json); this check did not infer additional symbols.

Both origin features use 70 px bounds to cover concealed endpoint extents. Their trace first points are separate, visible diagonal ink; they do not assert the hidden origin location.
