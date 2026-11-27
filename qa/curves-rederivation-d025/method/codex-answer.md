**Keep the first-submission tie-break. Preserve adjudicated physical points and identities, but do not transfer verification to nearby trace samples. I would fix the reconciliation and bound issues below before freezing tomorrow's audit files.**

I read the implementation and ran read-only, in-memory checks. No edits or regeneration.

**1. Tie-break**

I stand by the D-025 first-submission rule when independent validation cannot distinguish the maps. I would retain 0.25 px as a declared provisional tolerance, without adjusting it to recover particular canonical readers.

The alternatives have weaker justifications:

- **Previous canonical reader:** minimizes disruption, but makes selection depend on reconciliation history. Reproduction requires either the frozen previous result or its complete historical algorithm and inputs.
- **Denser trace sampling:** measures sampling effort, not accuracy. Additional samples of a drawn trace are not additional physical observations.
- **Old affine residual:** reintroduces the criterion D-025 deliberately replaced. A uniform-looking fit can sacrifice genuine nonuniform scale positions.

First-submission selection needs no previous reconciliation state. Strictly, the complete D-025 result still requires the source image, recovered anchors and versioned validation rules alongside the submissions. Submission order should be recorded explicitly; the general CLI currently treats input A as first submission. [Selection implementation](<repository>/tools/diff_curves.py:227).

The re-adjudication cost matters, but some of the apparent cost is avoidable: existing categorical decisions are currently being lost unnecessarily. Fix that before deciding that the tie-break itself creates excessive work.

**2. Decisions after a canonical flip**

I recommend **automatic preservation of established decisions, followed by blind adjudication of genuinely new questions**. A 15 px neighborhood is insufficient for transferring a decision.

For **markers**, establish a unique correspondence to the same physical symbol using page position, symbol, panel and adjudicated series identity. Preserve the adjudicated winner's own source and sequence, and rederive its numbers using that reader's corrected map. If correspondence is ambiguous, send it to blind review. Features need their role as well as position.

For **traces**, preserve verification and exclusion of the exact submitted samples. A verified sample does not verify adjacent samples, an interpolated location, or an entire trace segment. Transfer a segment-level decision only where the original adjudication explicitly checked that segment's extent and branch. Otherwise, new pending and one-sided samples need blind review.

Known exclusions must affect both readings **before matching and interpolation**. Preserve explicit breaks where the decision concerns a gap or wrong branch; simply deleting a point and reconnecting its neighbors can recreate the rejected interpolation.

There is already a concrete avoidable loss: FC-3B p1, `n1761`, first feature was resolved in favor of Claude, but after the flip Claude's feature is pending again. Conversely, the established Codex winners for `n2934` and `n3815` should remain the retained physical features. These can be carried through the existing feature correspondence without asking adjudicators to repeat their judgment. [Original decisions](<repository>/qa/curves-appc-b2/decisions-FC-3B-p1.csv), [current canonical file](<repository>/qa/curves-appc-b2/canonical-FC-3B-p1.csv).

**3. Line validation and selection**

I disagree with treating **quarter coverage plus a 2 px median** as sufficient verification of an entire fitted line. The detector searches near the proposed line, so a badly tilted line can find ink near its middle and find nothing near its ends. Missing detections then disappear from the distance statistic.

An in-memory synthetic example demonstrated this: a proposed line displaced by **12 px at both ends** passed verification, with a reported location error of about **5 px**. This establishes a failure mode, not another identified bad line in these panels. [Verification code](<repository>/tools/calibrate_axes.py:337).

I would:

- Keep quarter coverage as a **minimum visibility requirement**, then require spatially distributed support sufficient to validate tilt over the domain where the line is used.
- Retain sample positions, missing detections and signed offsets. Distinguish insufficient visible evidence from positive evidence that the line is misplaced.
- Treat the 80th percentile as a robust diagnostic. It is not automatically a location bound covering the remaining positions. Contamination exclusions need recorded reasons; the supported remainder needs an error envelope.

I also disagree with **raw total knot count across both axes as an unconditional first criterion**. More interior lines on x should not automatically outweigh missing boundary support on y. Independently recover omitted supported lines where possible, then compare equivalent identities and coverage. A strict coverage superset can justify preference when the shared lines are comparably validated; incomparable coverage needs review. My original protocol explicitly required matching knot identities and coverage. [Original recommendation](<repository>/qa/curves-appc-b5/method/piecewise/codex-answer.md).

The equal-weight mean of per-line medians is reasonable as a summary after those gates. Keep it, but report each axis separately and retain per-line failures so an acceptable overall mean cannot hide a poorly located boundary. I would not change its weights merely to reduce flips.

**4. Implementation findings**

These are the material issues I found, including some inherited behavior exposed by D-025:

1. **Excluded samples still support numerical agreement.** Decisions are loaded after comparison, and exclusions only suppress output rows. In a read-only check following the current interpolation logic, **75 current `agreed` trace rows used a segment containing an excluded sample**; another five were pending. This does not prove those 75 canonical positions are wrong, but their agreement evidence includes a rejected reading. Apply exclusions before interpolation and recompute. [Interpolation](<repository>/tools/diff_curves.py:346), [late decision application](<repository>/tools/diff_curves.py:456).

2. **Swapping readings corrupts source/sequence identity.** The swap changes values, pixels and `source`, but retains the evaluating reader's sequence, pixel bounds, note and calibration flag. In FC-4B p1, `n1761`'s resolved last feature is labeled **Codex sequence 3**, while its retained pixels exactly match **Codex sequence 4**. That breaks audit identity. Retain the winner's complete point record and a separate link to the decision's original target. Interpolated replacements need explicit derived provenance because they have no submitted sequence. [Swap code](<repository>/tools/diff_curves.py:480), [affected row](<repository>/qa/curves-appc-b2/canonical-FC-4B-p1.csv:4).

3. **Bounds do not propagate the line-position intervals.** The implementation adds `abs(scale) * max(ea, eb)`. This can underbound extrapolation and locations near uncertain outer knots. For example, nominal lines at pixels 0 and 10 carrying values 0 and 10, each uncertain by 1 px, produce **9.5 ± 1** at pixel 9.5. Allowed line positions 1 and 9 produce **10.625**, outside that bound. Evaluate admissible endpoint positions, changing brackets where necessary, and reject overlapping or reversed scale intervals. [Bound calculation](<repository>/tools/calibrate_axes.py:368).

4. **A 9 by 9 grid does not implement comparison at every knot.** The line table compares only common knot identities, while map evaluation uses fixed grid positions. Evaluate both maps at the union of knot locations and within every resulting interval, including domain boundaries and tilt effects. Keep the grid as a supplementary diagnostic. [Map comparison](<repository>/tools/diff_curves.py:210).

5. **`compare_knots` mixes coordinate frames.** Its overlap limits and sampling positions combine A's and B's `t` coordinates directly, although each reader has a different `e_t`. Convert anchors into one common page frame before constructing the shared sampling domain. The present error may be small for these scans, but it contaminates a subpixel ranking. [Coordinate handling](<repository>/tools/calibrate_axes.py:415).

6. **Interior one-sided trace coverage can disappear.** Other-reader samples inside the canonical trace's overall x range are discarded, even when they occupy a gap with no canonical support. Keep unsupported interior segments as one-sided, respecting branch and drawing order. [Discard rule](<repository>/tools/diff_curves.py:376).

I would fix these, rerun reconciliation, carry established decisions through explicit physical correspondences, and then adjudicate the remaining new items. Freeze the resulting canonical files and their input versions before building wave 1. The current 77 pending items should not yet be treated as the final review workload.