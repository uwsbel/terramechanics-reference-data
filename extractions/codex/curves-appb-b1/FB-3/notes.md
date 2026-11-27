# FB-3: independent blind reading

Only packet/p0109.png, packet tables, and packet/CURVE-READING.md were used. Coordinates refer to the original unrotated 300 dpi image. No other reading was consulted.

## Calibration

All 8 x and 12 y knots are measured printed ticks or labelled frame lines. Tick stubs were sampled at 1 px intervals, each fitted independently with its own tilt. Opposite frame lines were also fitted independently. No interior knot was predicted from frame spacing. The native conversion is piecewise between these independently tilted lines; the affine map is diagnostic only.
Affine residual RMS: x=0.011262 psi, y=0.007383 kips/in.^2; maxima x=0.029842, y=0.024696. Every short tick is ink-checked at five positions along its actual stub; full frame lines use the protocol ink check. verified-knots.json records these checks and position errors. Bounds propagate the pixel rectangle and the bracketing line position intervals; global affine residual is not added.
Short tick strokes give limited leverage on their extended direction. Their independently fitted slopes are retained literally, rather than forcing parallel lines. calibration-sensitivity.csv reports affine minus piecewise values so the effect is visible. No inferred interior grid is treated as printed ink.
By-eye checks: x labels [0, 6, 14]; y labels [7, 13, 18]. All printed tick labels were also inspected in labels-all.png. See calibration-eye-checks.csv for the six requested checks.

## Series, symbols, and drawn lines

- dr99: printed "Dense; Dr = 0.99"; circle; polyline through 1 internal vertices.
- dr30: printed "Loose; Dr = 0.30"; circle; polyline through 1 internal vertices.

Markers were recorded before trace extraction. Clean marker centers have 2 px bounds; overlaps, missing arcs, or axis crossings have wider bounds stated per row. Legend symbols are not counted as measurement markers. Trace bounds are half the measured ink thickness (at least 3.5 px for the rasterized line core), without using symbol rims to extend a stroke. Features locate each first/last point, every bend, and the printed group label center. Hidden bends are features with wider bounds, not trace samples in white symbol interiors.

Requested samples blocked by symbols or missing line ink are listed in trace-omissions.csv (3 omissions). Rule 7 takes precedence over placing a trace sample on a symbol or in a white gap. trace_segment changes across a symbol obstruction; interpolation must not cross that break.

## Ambiguities

The y tick between 7 and 9 prints as "3" (not 8). Its measured spacing is approximately one unit from both neighbours, confirming 8; it is used as 8, never as 3.
Dense knee around (1237,1988) is a thick, unresolved circle cluster. One marker is retained with a 20 px bound; additional coincident circles cannot be counted reliably. The two top circles and the two overlapping loose circles near (1090,3775) are distinguishable.

## Files

points-p1.csv; points-p1-native.csv; overlay-p1.png; calibration-eye-checks.csv; trace-omissions.csv; cal-p1/calibration.json; cal-p1/anchors.csv; cal-p1/tick-fits.csv; cal-p1/verified-knots.json; cal-p1/line-fits.csv; cal-p1/labels-all.png; cal-p1/calibration-sensitivity.csv. Helpers and enlarged coordinate crops are retained under out/.

Counts: {"dr99": {"marker": 5, "feature": 4, "trace": 9}, "dr30": {"marker": 6, "feature": 4, "trace": 12}}

Axis-label registration: several y-label glyph centers sit modestly below their tick, and terminal x labels can sit inward of the frame corner. Values were assigned from the printed ordered sequence and measured tick ink, never from the text center. Frame label checks use the actual bottom/left frame intersections.

Final QA: enlarged trace-ink-checks.png reviewed against the source; all stored trace centers lie on dark line ink. Clean closed-circle centers were checked against their white interior extents (out/center-refinements.json); this check did not infer additional symbols.
