My recommendations follow the existing distinction between agreement, agent verification, and human audit. No files were edited.

1. **Keep the gap cutoff; verify the affected segments instead of automatically calling the 196 samples agreed.**

   Use unrestricted bridging as a diagnostic only. The other reader should inspect each affected segment on the scan and verify the retained samples' ink positions and series identity. Record a decision for every covered point: `one-sided-verified` where ink supports it, `excluded` where it is an invented continuation, and `one-sided` where verification remains impossible. One segment overlay can support several explicit point decisions.

   The reason is that sampling density does not establish continuity of the drawing. All 196 passing the interpolated tolerance demonstrates consistency with a chord, but cannot establish which branch the chord follows or whether a retained sample reads ink. The dashed curves visibly have interruptions around symbols (AM-68-1 Vol. II, Fig. C-1C, printed C-4, PDF 118). This approach preserves the pilot's distinction between verified ink and invented bridges. It also follows D-022: verified one-sided points enter its capped audit sample; unverified ones remain mandatory audit rows. [Pilot review](<repository>/qa/curves-pilot-b1/review.md), [D-022](<repository>/docs/decisions.csv:23).

   **I would change my mind** about a numerical exception after source-based validation establishes a safe maximum span and bounds interpolation error near curvature, crossings, and interruptions. These counts alone do not justify a new threshold.

2. **Compare features, but match their meaning before comparing their coordinates.**

   Pair `first` with `first`, `peak` with `peak`, and `last` with `last` within the same series and branch. Closest-position matching alone can pair different features.

   For a uniquely located peak, compare both coordinates using the summed reading bounds. For a flat-topped peak, compare maximum **y** using
   `|yA - yB| <= b_yA + b_yB`; represent peak location by independently read x intervals and compare their overlap. Do not require two arbitrary plateau positions to agree within line-centering bounds. Broad maxima are visible in AM-68-1 Vol. II, Fig. C-2C, printed C-8, PDF 122.

   Canonical data should retain the selected reading's peak y and a source-supported `[x_lo, x_hi]` location interval, without averaging. Any scalar x retained for plotting is a representative location, not a precisely identified peak displacement. Document that representation in the schema and data dictionary.

   First and last points define the drawn domain. Compare **both x and y** within summed endpoint bounds. The slope allowance used for interior trace samples must not erase disagreement about where the drawing starts. Unreadable endpoints need intervals or missing values. Features should not add independent fitting weight to the trace they summarize. [Current protocol](<repository>/docs/CURVE-READING.md).

   **I would change my mind** if the scan showed a sharp peak, a definite endpoint marker, or evidence that the feature belonged to stray ink.

3. **Retain unique points from either reader in the reconciliation output, with their actual provenance.**

   Keep unmatched markers as `one-sided`, then promote them to `one-sided-verified` after the other agent checks position **and identity**. Preserve the contributing reader's pixels, values, bounds, and calibration; `source` names that reader. A panel's smaller calibration residual does not make its reading complete. Preserve original submission identifiers separately when assigning canonical sequence numbers.

   Retain actual curve-end ink samples similarly, after checking that they extend the same branch. Do not append the other reader's redundant interior sampling wholesale, and do not extrapolate endpoints.

   Before unioning FC-2C's lower-panel markers, detect coincident candidates **across series**. Otherwise one physical symbol assigned differently becomes two observations. Keep unresolved identity `pending-review`, with candidate identities recorded; wider coordinate bounds cannot settle identity. The stacked symbols are visible in AM-68-1 Vol. II, Fig. C-2C, printed C-8, PDF 122. The current tool reports other-reader-only markers but omits them from canonical output. [Comparison code](<repository>/tools/diff_curves.py:242).

   **I would change my mind** about retaining a candidate if rereading showed duplicate ink, a grid stroke, or an unrecoverable symbol.

4. **Use `n2935`, scoped by figure and experiment, and correct the index through a recorded build input.**

   Both original legends plainly print 2935: AM-68-1 Vol. II, Fig. C-2B, printed C-7, PDF 121; Fig. C-2C, printed C-8, PDF 122. The packet-imposed `n2995` is a shared input error, not independent confirmation.

   Record source-cited corrections for each complete `legend_entries` cell in a new correction batch. Preserve the old extractions. Extend `build_figures.py` to apply explicit descriptive-field corrections and record their status, provenance, and superseded values in the sidecar. Merely adding resolutions will currently fail: its descriptive-field loop takes `legend_entries` directly from the second submission. [Builder](<repository>/tools/build_figures.py:224).

   Regenerate the index and apply a figure-scoped `n2995 -> n2935` mapping when rebuilding canonical points, series maps, and dependent setup values. Preserve the original submitted ID in provenance and record the shared packet hint in the batch review.

   **I would change my mind** only on stronger source evidence establishing a printing error. Even then, keep the printed legend distinct from the corrected physical stress.

One accounting issue: the 16 current diff files total **4,401 matched, 4,345 agreed, and 56 disagreed**, rather than the supplied totals. Their canonical one-sided total is 301 across all point kinds. Reconcile that ledger before publishing the review. [Batch 1 reports](<repository>/qa/curves-appc-b1), [batch 2 reports](<repository>/qa/curves-appc-b2).