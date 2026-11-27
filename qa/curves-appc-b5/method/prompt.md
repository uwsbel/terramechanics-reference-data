# Five method questions from batches curves-appc-b3, -b4, -b5 (data sheets, psi sheets, envelopes)

You are a colleague on this project. Claude has written its own answers to a file you cannot see;
afterwards the two sets are compared and the better reasoning wins, with credit. Dan is away and
asked us to settle method questions between us. Read-only in the repository; useful files:
`docs/CURVE-READING.md`, `docs/decisions.csv` (D-023), `tools/diff_curves.py`,
`tools/calibrate_axes.py`, the readings `extractions/{claude,codex}/curves-appc-b4/`, `-b5/`,
the diffs `qa/curves-appc-b5/diff-FC-*-p1.md`, and the reconciled data sheets
`qa/curves-appc-b1/canonical.csv`, `qa/curves-appc-b2/canonical.csv`, `qa/curves-pilot-b1/canonical.csv`.

## Evidence gathered so far

A. **Calibration of the gridless envelopes (FC-2A, FC-3A, FC-4A).** These figures have tick marks
but no interior grid lines. Codex calibrated on the measured ticks. Claude's FC-2A reader did the
same (its own helper); Claude's FC-3A and FC-4A readers used `calibrate_axes.py detect`, which can
only interpolate interior lines from the frame (all interior lines `predicted`), so their RMS
residuals are tiny (0.25 and 0.47 psf in y) and the canonical rule (smaller residual) picks them.
The two maps differ by 23 to 38 psf at the top corners. An independent arbiter exists: an envelope's
markers are the peak shear stresses of the data-sheet tests, already reconciled. Mean
envelope-minus-sheet differences: FC-3A, Codex +11 and +16 psf, Claude +25 and +33; FC-4A (Dr 0),
Codex +30, Claude +46. Claude's FC-3A reader also measured the printed y ticks 23 to 48 psf off its
own frame map and kept a tick map aside (`extractions/claude/curves-appc-b5/FC-3A/alt-ticks/`).

B. **Triangle centers.** Readers differ: some take the bounding-box center, some the centroid (one
third of the height from the base); the two differ by about 5 px toward the apex on a 20 px symbol,
about the sum of two triangle bounds. Batches b1, b2 (already reconciled) mixed both conventions.

C. **FC-1A: legend versus line.** The brief said a symbol whose shape does not match its line's
legend group is assigned by the line it sits on. Codex followed that; Claude's reader assigned three
symbols by legend shape instead. Data-sheet arbiter: the filled circle at sigma 315 psf matches the
Dr .73 to .88 sheet (FC-1C) peak within 18 psf and the Dr .50 to .57 sheet (FC-1B) only within 162;
the triangle on the axis at 485 psf is the zero-stress test of FC-1D (476 psf); the filled circle at
1772 psf matches FC-1C within 28 psf. Two open circles on the 47-degree line match FC-1C within 13 psf.

D. **FC-2A legend printed swapped.** Both readers read the legend as printed and agree to 2 psf.
Against the sheets: the "Dr .33 to .53" squares sit 150 to 770 psf above the loose FC-2B peaks but
within 8 to 48 psf of the dense FC-2C peaks; the "Dr 1.15 to 1.3" circles sit within 4 to 54 psf of
the loose FC-2B peaks. Friction-angle chart C-17 plots 46.7 degrees at the loose Dr. Proposed: a
series rename at the canonical stage (`qa/curves-appc-b5/series-ids.csv`) with the evidence.

E. **FC-7B/7C rounding.** `calibrate_axes.py apply` rounded to 3 decimals, which on an inch axis
(0 to .32) zeroed the x bounds (fixed since). Claude's two readings were made with the old tool;
Codex worked around it. Proposed: re-derive Claude's values with the fixed `apply` from its own
pixels and calibration (`qa/curves-appc-b4/rederived/`), the submission untouched.

## Questions

1. Which calibration should be canonical on the gridless envelopes, and what should the canonical
   rule say in general when one reading's residual is measured on interpolated lines?
2. Which triangle center should the protocol fix, and what does that mean for the bounds and for
   the readings already made under the other convention?
3. On an envelope, when a symbol's shape (legend group) and the line it sits on disagree, which
   decides, and is the data-sheet comparison a legitimate way to settle identity?
4. FC-2A: is a canonical-stage series rename the right way to record a printed legend error, and
   what else should change (experiment index rows, notes)?
5. FC-7B/7C: is re-deriving the native values from the submission's pixels and calibration sound?

For each: recommendation, reason, what would change your mind. A page or two in all; no edits.
