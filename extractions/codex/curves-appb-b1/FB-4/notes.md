# FB-4: independent blind reading

Only packet/p0110.png, packet tables, and packet/CURVE-READING.md were used. Coordinates refer to the original unrotated 300 dpi image. No other reading was consulted.

## Calibration

All 8 x and 11 y knots are measured printed ticks or labelled frame lines. Tick stubs were sampled at 1 px intervals, each fitted independently with its own tilt. Opposite frame lines were also fitted independently. No interior knot was predicted from frame spacing. The native conversion is piecewise between these independently tilted lines; the affine map is diagnostic only.
Affine residual RMS: x=0.009276 psi, y=0.004752 kips/in.^2; maxima x=0.020104, y=0.016664. Every short tick is ink-checked at five positions along its actual stub; full frame lines use the protocol ink check. verified-knots.json records these checks and position errors. Bounds propagate the pixel rectangle and the bracketing line position intervals; global affine residual is not added.
Short tick strokes give limited leverage on their extended direction. Their independently fitted slopes are retained literally, rather than forcing parallel lines. calibration-sensitivity.csv reports affine minus piecewise values so the effect is visible. No inferred interior grid is treated as printed ink.
By-eye checks: x labels [0, 6, 14]; y labels [0, 5, 10]. All printed tick labels were also inspected in labels-all.png. See calibration-eye-checks.csv for the six requested checks.

## Series, symbols, and drawn lines

- dr86: printed "Dense; Dr = 0.86"; circle; polyline through 1 internal vertices.
  - left trace end: first separable stroke is 31.5 px inward of estimated symbol junction; hidden endpoint not guessed
- dr22: printed "Loose; Dr = 0.22"; circle; polyline through 2 internal vertices.
  - left trace end: first separable stroke is 1.0 px inward of estimated symbol junction; hidden endpoint not guessed

Markers were recorded before trace extraction. Clean marker centers have 2 px bounds; overlaps, missing arcs, or axis crossings have wider bounds stated per row. Legend symbols are not counted as measurement markers. Trace bounds are half the measured ink thickness (at least 3.5 px for the rasterized line core), without using symbol rims to extend a stroke. Features locate each first/last point, every bend, and the printed group label center. Hidden bends are features with wider bounds, not trace samples in white symbol interiors.

Requested samples blocked by symbols or missing line ink are listed in trace-omissions.csv (1 omissions). Rule 7 takes precedence over placing a trace sample on a symbol or in a white gap. trace_segment changes across a symbol obstruction; interpolation must not cross that break.

## Ambiguities

The low dense triplet and loose bend triplet have merged rims; individual residual arcs support the separate markers. The dense rightmost cluster has one main hole and tiny upper/lower crescents: two overlapping circles are recorded with 12 px bounds. The two widely scattered loose observations near each of x˜5 and x˜10 are assigned to the loose line, which passes between each pair; neither pair lies on the dense line.

## Files

points-p1.csv; points-p1-native.csv; overlay-p1.png; calibration-eye-checks.csv; trace-omissions.csv; cal-p1/calibration.json; cal-p1/anchors.csv; cal-p1/tick-fits.csv; cal-p1/verified-knots.json; cal-p1/line-fits.csv; cal-p1/labels-all.png; cal-p1/calibration-sensitivity.csv. Helpers and enlarged coordinate crops are retained under out/.

Counts: {"dr86": {"marker": 7, "feature": 4, "trace": 10}, "dr22": {"marker": 8, "feature": 5, "trace": 11}}

Axis-label registration: several y-label glyph centers sit modestly below their tick, and terminal x labels can sit inward of the frame corner. Values were assigned from the printed ordered sequence and measured tick ink, never from the text center. Frame label checks use the actual bottom/left frame intersections.

Final QA: enlarged trace-ink-checks.png reviewed against the source; all stored trace centers lie on dark line ink. Clean closed-circle centers were checked against their white interior extents (out/center-refinements.json); this check did not infer additional symbols.
