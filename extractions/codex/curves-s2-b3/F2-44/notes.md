# Blind reading: F2-44, panel 1

Only packet/p0104.png, packet/p0099.png and the supplied protocol/index rows were used. Coordinates refer to the unrotated 3213 by 4508 page. No other reading was consulted. Context page 99 describes bin-size tests in dense RS with mean relative density about 0.96; no point was taken from its text.

## Identity and printed key

The key prints A = 18 inch by 36 inch bin; B = 36 inch by 36 inch bin; C = 54 inch by 36 inch bin. Gp values are in parentheses.

- lpt24: A LPT No. 24 (83), **dashed**, identified by the lower curved arrow pointing to the rightmost initial dashed rise. It reaches the broad first peak near 0.9 inch, has a shallow trough around 1.45 inches, then the shallower dashed recovery ending around 3.02 inches and 1340 lb.
- lpt73: A LPT No. 73 (117), **dashed**, identified by its printed along-line label beside the steep dashed recovery. It has the earlier first peak and minimum around 1 inch; its steep branch ends around 2.96 inches and 1791 lb. It is distinguished from 24 by the arrow, the intervening peak/trough geometry, and continuity through their early crossing, not by assigning them different styles.
- lpt74: B LPT No. 74 (103), **dotted**, identified by the upper of the two lower arrows, pointing beside the dotted trough. Follow its dots through the crossings; its final dot is around (2107,1867), 4.44 inches and 1780 lb. It is not continued up either solid line.
- lpt69: C LPT No. 69 (103), **solid**, identified by the upper solid recovery's along-line label. This is the higher initial peak, then the shallower trough, and finally the rightmost endpoint around (2185,1835).
- lpt64a: C LPT No. 64A (112), **solid**, identified by the label beside the lower solid recovery. This is the lower initial solid peak, the deep trough near 1.87 inches, and the steeper final solid branch ending around (2077,1840).

All supplied ids are retained; no printed-label discrepancy was found. No symbols are plotted. Text/arrowheads, incidental short strokes and grid intersections are not markers. Protocol rules 8 and 9 do not apply to these unmarked recorded traces.

## Calibration

Linear axes, penetration right and load up. Verified knots: x = 0,1,2,3,4,5 inches; y = 0,500,1000,1500,2000 lb. The key covers the middle of the 2000-lb line. Its final fit uses the visible left and right segments, with no key lettering admitted as grid ink. The original detect result is retained separately. Every final grid line passed the image-based verification; see cal-p1/verified-knots.json.

calibration-eye-checks.csv records every printed label (more than three per axis), with two visible-segment checks for the 2000 line. Values and reading bounds use the verified piecewise map with its individual knot location intervals. The affine residual is only a diagnostic and is not added to each bound. calibration-sensitivity.csv records the affine-to-piecewise differences by series.

## Crossings and uncertain parts

Initial curves are closely superposed, particularly the four leftmost strokes. The visible curve ink begins around (747--763,3130--3144), near zero penetration but roughly 140--160 lb, **above the zero-load frame**. No independent continuation to (zero penetration, zero load) is visible. Starts are reported on that visible ink with widened bounds; the separate first points for the overlapping traces are not independently resolved.

The two dashed curves cross around 0.6--0.75 inch, near 850--900 lb; 24 also passes the descending dotted 74 branch nearby. The descending 64A solid branch crosses the steep dashed 73 branch and then dashed 24/dotted 74 in the region about 1.1--1.4 inches. The descending 69 branch crosses the steep dashed 73 branch before reaching its trough. Branch continuity and labels preserve the identities through these crossings, including the crossing between two traces of the same style.

After the trough of 69, the 24/74/69 recovery strokes are nearly coincident over roughly 1.5--2 inches. Individual centres cannot be separated reliably in the thick merged ink. Rows there explicitly say so and carry wider bounds; the hidden dotted/dashed continuation is not treated as a distinct new solid observation.

On the upper recoveries, 64A crosses the dotted 74 branch around 3.7--3.8 inches and crosses solid 69 around 3.8--3.9 inches. Dotted 74 subsequently crosses 69 near 4 inches. These intersections are partly thickened or coincident; samples in that region have widened bounds. Endpoints are followed to their own final dash/dot or solid ink. The small horizontal strokes near the printed labels, and the lower curved arrow shafts, are not continuations.

First local peaks and subsequent troughs are feature rows for all five traces. The apex of dashed 24 falls between adjacent dash ends: its feature is on the high visible dash end with the gap included in the bound, rather than being placed in white space. Broad knees on the recoveries are also recorded. Every trace has its highest load at its endpoint, so a separate global-peak duplicate is unnecessary. First/last ink is represented as both trace and feature, not counted as independent observations.

Trace targets are every 0.25 inch, supplemented by 100-lb targets on the initial steep rise. Targets in dash/dot gaps or a grid stroke move to nearby trace ink and keep the resulting measured coordinates. Coincident targets share a trace row. The final 24 dash supplies both the 3-inch target and the last-ink sample. The sequence follows drawing order; no resolved physical x reversal or unloading loop was found.

Bounds start with half a transverse stroke width measured locally on the original page. A dashed/dotted stroke additionally includes half its neighboring gap along the stroke, and overlap/crossing neighborhoods receive wider bounds. sampling-audit.csv preserves these measurements. The manual guides in ../read_curves.py only select an ink corridor. A black pixel alone does not establish a trace's identity: enlarged pixel-grid crops were inspected for the arrows, same-style crossings and upper endpoints.

check_trace_ink.py is named in the protocol but absent from the supplied tools, so D-031/D-032 could not be executed. ink-checks.csv contains the local ink audit, not a claim to have run that missing program. Initial overlaps and merged strokes remain reading ambiguities, with the wide bounds and notes retained. No software was installed.

Overlay colours: 24 red, 73 green, 74 blue, 69 orange, 64A purple. overlay-p1.png retains the full page dimensions; overlay-plot.png is its plot crop. Calibration, enlarged pixel-grid crops and sensitivity/sampling/ink audits are retained with the requested files.
