# Blind reading: F2-42, panel 1

Only packet/p0102.png, packet/p0099.png and the supplied protocol/index rows were used. All coordinates refer to the unrotated 3263 by 4558 page. No other reading was consulted.

## Identity and printed key

- A, lpt22, is **dotted**. Circled A lies beside the dotted recovery branch, which can be followed down to the lower of the two modest first peaks. Printed: LPT No. 22 (130), gamma 51.2 pcf, rate 4 inches/minute.
- B, lpt23, is **solid**, the upper shelf-bearing trace beside circled B. Printed: LPT No. 23 (99), gamma 50.6 pcf, rate 1 inch/minute.
- C, lpt24, is **short-dashed**, beside circled C on the steeper recovery branch. Its first peak is above A's. Printed: LPT No. 24 (83), gamma 51.5 pcf, rate 1 inch/minute.
- D, lpt25, is **long-dashed**, identified beside circled D near the top. Printed: LPT No. 25 (130), gamma 51.6 pcf, rate 2 inches/minute. Parentheses contain Gp. No index identity correction was required.

The circles are letter labels, not plotted markers. There are no marker observations. Protocol rules 8 and 9 do not apply to these unmarked recorded traces.

## Calibration

Both axes are linear, penetration right and load up. Verified knots: x = 0,1,2,3 inches; y = 0,200,400,600,800,1000,1200 lb. The 627 tick is a value annotation, not a knot. The upper frame is unlabelled and is not a knot. Accordingly the portions above 1200 lb, including the C and D frame endpoints, have extrapolated y values explicitly flagged in cal_model.

The first detect pass contaminated the 400-lb fit with inset text. The final fit reads its visible segment left of the inset; covered intersections are not y anchors. Curve crossings and inset/frame outliers were excluded from the grid fits. Original detection is retained as cal-p1/calibration-detect.json. Every final knot passed the protocol's image-based ink check; see verified-knots.json. Values and bounds in points-p1-native.csv are piecewise between these knots, with each knot's location interval propagated, and with no global affine residual added. calibration-sensitivity.csv gives the affine-to-piecewise diagnostic by series.

calibration-eye-checks.csv checks **every printed grid label**, exceeding three per axis. Each row records a hand-read line centre on the image and its difference from the fitted line. In particular 1200 belongs to the line near v=1489, not the frame near v=1334; 600 belongs to v=2422, not the adjacent 627 tick.

## Following ink, features and uncertainty

The four initial strokes overlap or are closely interleaved below about 800 lb. Individual centres and starts are not fully resolved. Bounds cover the neighboring strokes there; identical/nearby ink centres do not establish separate observations. The first feature/trace points are the visible ink at the bottom frame, with the slight lateral spread retained rather than forcing native x to exactly zero.

A and C cross near (1295,2020), approximately 1.5 inches and 860 lb. D crosses B near (1360,1666), about 1.7 inches and 1086 lb. These neighborhoods carry explicit notes and widened bounds. D and B are also coalescent along part of the initial rise.

A's dots approach and terminate against C around (1618,1530), approximately 2.52 inches and 1174 lb. No independent dotted continuation can be resolved above this junction. A is ended at the last identifiable dotted ink and is not extended along C to the frame. This termination is an identity ambiguity, not evidence that the two tests became one trace. C continues to (1740,1334); D continues to (1618,1334), where each meets the frame. B stops inside the plot near (1497,1597).

B's shelf changes by less than the stroke width. Its peak and subsequent minimum rows document the first shelf maximum and shallow shelf-end depression, but no distinct load drop is resolved. D is monotone within the reading bounds and has no separate first local maximum/minimum pair. All four highest loads occur at their final points, so no additional global-peak duplicate is needed. First/last points are represented in both trace and feature kinds; counts must not be added as independent tests.

Trace targets are every 0.25 inch, supplemented by every 100 lb on the initial steep rise. A target in a dot/dash gap or grid intersection moves to nearby stroke ink and retains its actual native coordinates; note records the move. Coincident targets use one trace row. Feature rows retain drawing order. No resolved unloading loop or x reversal is present.

Point-local transverse stroke widths were measured on the original scan. Bounds begin with half that width, include half a local dash/dot gap along the stroke, and widen for crossings/overlap. sampling-audit.csv records the measured half-width and half-gap per row. Guides in ../read_curves.py select corridors only; interpolated white-gap positions are never output as observations. An image centre being black is necessary, not a sufficient proof of identity, so label-adjacent points and the two crossings were also visually checked on enlarged pixel-grid crops.

The packet does not supply check_trace_ink.py (D-031/D-032). It could not be run. Local ink checks are in ink-checks.csv and do not claim to reproduce that missing checker. Frame intersections and unresolved initial overlaps are explicitly identified for later comparison. All rows have positive reading bounds. No software was installed.

Overlay colours: A/lpt22 red, B/lpt23 green, C/lpt24 blue, D/lpt25 orange. overlay-p1.png has the original page dimensions; overlay-plot.png is its plot crop. Enlarged grid crops, calibration files, sensitivity and sampling/ink audits are retained alongside the requested outputs.
