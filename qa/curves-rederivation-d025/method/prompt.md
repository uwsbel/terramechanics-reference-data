# D-025 is implemented; its first full run raises a tie-break question. Your judgment, please.

You and Claude agreed D-025 on 2026-10-14 (`docs/decisions.csv`, and your answer in
`qa/curves-appc-b5/method/piecewise/codex-answer.md`): piecewise maps between verified lines; bounds
from the point's pixel interval and the bracketing lines' location errors, no global residual; maps
compared at every knot; the canonical reading chosen by independent line-position validation, with
the first-submission tie-break "when validation cannot distinguish them"; existing readings re-derived,
"preserve valid ink and identity decisions by source and sequence; recompute numerical agreement and
canonical selection".

Claude has implemented it (uncommitted, in the working tree; read anything you need):

1. `tools/calibrate_axes.py`: `AxisKnots`, `ink_offset`, `ink_positions`, `compare_knots`,
   `piecewise_rows`. Each reader's line is checked against the page's ink: the darkness-weighted
   centre of the line's core in a profile across it (+-6 px), averaged +-4 px along it, at up to 25
   positions between its anchors (a lone tick: on its stubs 6 to 14 px either side of its anchor,
   because an axis line can be 8 px thick). A line is a knot only if ink is found at a quarter of its
   positions or more (at least 2) and its median distance from the ink is 2 px or less; otherwise it
   is "not on the ink" and is not a knot (like a predicted line). A knot's location error is
   max(0.5 px, anchor scatter, 80th percentile of |distance from ink|).
2. `tools/diff_curves.py --maps piecewise --image`: compares the two readings line by line (lines
   apart, each line's median distance from an ink centre located once between the two lines), the two
   maps on a 9 x 9 grid, and chooses the canonical reading: (a) the one with more verified lines; (b)
   with as many, the smaller mean over common lines of the per-line median distance from the ink;
   (c) if the two means are within 0.25 px, the first submission (Claude, reading A).
3. `tools/reconcile_curves.py`: re-derives every reading from its pixels into
   `qa/<batch>/rederived/<reader>/<figure>/` (with `knots.json`), adds lines recovered in
   `qa/<batch>/knots.csv` (the left frame x = 0 of FC-6B and FC-6D for Claude, measured on the page;
   it matches Codex's x = 0 anchors within 0.5 px), diffs, and writes
   `qa/<batch>/calibration-sensitivity.md`.

Results over the pilot and appc-b1 to b5 (32 panels), against the reconciliation before D-025
(per-panel table in `qa/curves-appc-b1/d025-before-after.txt`):

1. Lines rejected as not on the ink: Claude's x = 50 (both panels) and x = 250 (lower panel) of the
   pilot FC-1B (2.9 to 3.9 px off; the x = 50 line was found in 10 of 24 bands with the wrong tilt,
   16 px off at the top), Claude's y = 5000 on FC-1D (3.1 px), Codex's x = 100 on FC-6D lower panel
   (2.9 px). Where both readers' lines coincide, median distances reach 1.8 px (thick or doubled ink).
2. 12 panels change canonical reader: 3 by coverage (FC-1D p1 and FC-4B p2 to Claude, FC-3C p1 to
   Codex, whose top frame Claude's map lacks), 9 by the tie rule (FC-2B p1 and p2, FC-2C p1, FC-3B p1,
   FC-4C p2, FC-6C p2, FC-1A, FC-2A, FC-3A, all Codex to Claude). On every tie the two means differ
   by less than 0.16 px; the old rule (affine residual) also separated them by 1 to 3 percent only.
3. Consequences: points pending review 10 before, 77 now (18 of them within 15 px of a point that
   already has a decision, on the other reader's point, which no longer applies because decisions are
   keyed by source); unverified one-sided points 83 more than before (mostly Codex trace samples beyond
   the ends of Claude's shorter traces, FC-3B p1 alone 53); canonical point counts drop where Codex,
   which samples traces about twice as densely, loses canonical status (appc-b1: 2757 to 1882 points).
4. On panels that did not flip, bounds without the global residual add a few disagreements (FC-1C p2
   0 to 6 pending, FC-1D p2 0 to 7).

The human audit (wave 1: pilot, b1, b2) is built tomorrow from these canonical files.

Questions:

1. Tie-break. Keep (c) as written (first submission, Claude), or something else (for example, keep the
   canonical reading of the existing reconciliation; a reproducible secondary criterion such as the
   denser trace sampling or the old residual; anything better)? Give your reasons, including
   reproducibility from the submissions alone and the cost of re-adjudication.
2. Decisions made on a point of the reading that is no longer canonical: translate them to the new
   canonical points automatically (how, for markers and for traces), or re-adjudicate the new pending
   and one-sided items blind?
3. The line rules in (1) and (2) above: anything you would change (thresholds, the coverage-first
   rule, the per-line mean)?
4. Anything wrong in the implementation itself that you can see by reading the code.

Be concrete; say plainly where you disagree with the implementation. No edits: this is read-only.
