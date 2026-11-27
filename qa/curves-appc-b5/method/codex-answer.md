My recommendations follow below. These are method judgments based on the supplied evidence and repository checks, not completed human audits. I made no edits.

1. **Use measured-tick calibrations for the gridless envelopes.**

   For FC-3A and FC-4A, select Codex’s current tick maps over Claude’s frame-interpolated maps. For FC-2A, both readers used measured ticks, so the current residual rule remains applicable; its very narrow preference for Codex carries little practical significance. The FC-3A and FC-4A diffs explicitly flag corner disagreements despite selecting Claude by RMS. [FC-3A diff](<repository>/qa/curves-appc-b5/diff-FC-3A-p1.md), [FC-4A diff](<repository>/qa/curves-appc-b5/diff-FC-4A-p1.md).

   The general rule should say: **residuals against predicted anchors measure internal consistency, and cannot compete with residuals against observed scale marks.** Validate both maps against actual labeled ticks or grid lines on a comparable basis before ranking them. Predicted intersections add no independent scale evidence. Propagate the observed scale discrepancies into bounds, and settle calibration disagreements before accepting point agreements. This strengthens the existing requirement in [CURVE-READING.md](<repository>/docs/CURVE-READING.md).

   Re-derive Claude’s FC-3A reading using its preserved alternate tick map, then compare again. Preserve the original submission. The supplied sheet comparisons support this choice, but should validate the calibration rather than become targets used to tune it. The originals confirm the absence of interior grids: AM-68-1 Vol. II, Figs. C-2A, C-3A, C-4A, printed C-6, C-9, C-12, PDF 120, 123, 126.

   **What would change my mind:** independently checked ticks showing that Codex measured the wrong ink or labels, or a frame map that performs better against actual scale marks after comparable validation.

2. **Fix the triangle center at the geometric centroid of the reconstructed triangle.**

   Use the three vertices or fitted sides, excluding stray ink and intersecting lines. For an upright isosceles triangle, this is one third of its height from the base. This defines the same geometric point for hollow and filled symbols and behaves consistently under rotation. It is a protocol convention; the corpus does not establish the drafter’s intended registration point. The submissions demonstrably mix conventions, including within Claude’s FC-7B/7C readings. AM-68-1 Vol. II, Figs. C-7B/C-7C, printed C-22/C-23, PDF 136/137; [FC-7C reading notes](<repository>/extractions/claude/curves-appc-b4/FC-7C/notes.md).

   Bounds must distinguish uncertainty in locating that center from uncertainty about the convention. For an ideal isosceles triangle, the centroid and bounding-box midpoint differ by **height/6**; a universal 5 px correction is therefore inappropriate. Until registration is established, include that alternative location in the affected directional bound.

   Inventory earlier triangle readings and normalize them through a documented new derivation or rereading batch. Recompute values and bounds, rerun reconciliation, and revisit affected decisions. Keep submissions immutable. Neither discard earlier readings wholesale nor silently grandfather mixed conventions.

   **What would change my mind:** repeated, unambiguous source evidence showing that the plotted coordinate was registered at the bounding-box midpoint or another point.

3. **Neither symbol shape nor line proximity should decide unconditionally. Use identifiable primary tests to resolve conflicts.**

   The brief’s line-first instruction was clear, but the FC-1A evidence shows why it needs amendment. An envelope line is an author fit; belonging to its test group does not require a marker to lie closest to that line.

   Here, retain the disputed filled circles in `dr73-88` and the axis triangle in `dr100-116`. The reconciled FC-1C peaks support the circles; FC-1D’s zero-normal-stress peak supports the triangle. Thus **Claude deserves credit for the three disputed assignments**. Both readers correctly placed the two open circles in `dr73-88`. AM-68-1 Vol. II, Fig. C-1A, printed C-2, PDF 116; Fig. C-1C, printed C-4, PDF 118, experiments `b68-ds-fc-1c-n294` and `b68-ds-fc-1c-n1760`, series `n294` and `n1760`; Fig. C-1D, printed C-5, PDF 119, experiment `b68-ds-fc-1d-n0`, series `n0`.

   Sheet comparison is legitimate when matched normal stresses, density evidence, and peak values distinguish candidate tests. It is corroboration from another depiction of the same tests, not independent experimental validation. Preserve the drawn symbol and explain the resolved identity. Remaining ambiguity follows D-023’s adjudication process. [D-023](<repository>/docs/decisions.csv).

   **What would change my mind:** evidence that these sheets represent different tests, or corrected peak readings that remove the distinguishing match.

4. **Yes: record FC-2A’s inferred legend swap through a canonical-stage series rename.**

   The existing [series-ids.csv](<repository>/qa/curves-appc-b5/series-ids.csv) already expresses the appropriate swap. Both submissions correctly preserve the printed legend. Canonically, squares and the 49.5-degree line belong to the dense FC-2C group; circles and the 46.7-degree line belong to the loose FC-2B group. The sheets support the reassignment across the stress series, and C-17 corroborates the loose-group angle. AM-68-1 Vol. II, Figs. C-2A/C-2B/C-2C, printed C-6/C-7/C-8, PDF 120/121/122; Fig. C-17, printed C-39, PDF 153.

   Preserve printed legend text, symbol shapes, coordinates, and angles. Add an explicit correction record carrying submitted identity, canonical identity, evidence, and inference status. Update downstream metadata and document that rename maps can correct source errors as well as packet errors.

   The experiment index’s dense-to-FC-2C and loose-to-FC-2B relationships already have the correct targets; **do not swap them again**. Regenerate the rows with resolved correction notes and correct the stale angle associations in `notes_codex`. Keep `*_printed` fields faithful to the report. [Experiment index](<repository>/data/experiments/index.csv).

   **What would change my mind:** corrected sheet readings or original test records supporting the printed pairing. Density-strength expectations alone would not justify this correction.

5. **Yes: re-derivation from the submission’s own pixels, pixel bounds, and calibration is sound.**

   This repairs numerical conversion while preserving the reading. I checked all **107 FC-7B rows and 95 FC-7C rows**: their original fields are unchanged, their rederived values match the fixed `apply` formula, and the copied calibrations are byte-identical. FC-7B’s old output contained 89 zero x bounds; the rederived bounds are positive. [Rederived files](<repository>/qa/curves-appc-b4/rederived), [apply implementation](<repository>/tools/calibrate_axes.py:204).

   Record the original inputs, tool version, command, and derivation path; retain attribution to Claude. Rerun comparison and regenerate affected SI outputs and review artifacts. This adds no second independent reading and does not resolve symbol-center or identity questions. AM-68-1 Vol. II, Figs. C-7B/C-7C, printed C-22/C-23, PDF 136/137.

   **What would change my mind:** missing original pixel precision or bounds, a changed calibration, or evidence of a transformation error beyond output rounding. Those would require a broader correction or rereading.