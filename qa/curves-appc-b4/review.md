# Review of batch curves-appc-b4: Figures C-7B and C-7C (RSM-b, psi, printed sideways)

Reconciled with batches b3 and b5 on 2026-10-14; the shared review, with the adjudication, is
`qa/curves-appc-b3/review.md`.

Both figures are printed sideways and calibrated on the page as scanned (`calibrate_axes.py detect
--x-direction up --y-direction left`, confirmed by both readers' label checks). Symbols only, six
tests each; the legend prints the stresses beside each curve's end, not symbols. 107 markers on C-7B
and 95 on C-7C in each reading. 198 of 201 matched markers agree; 202 canonical points.

Claude's values were made with `calibrate_axes.py apply` before its decimals were fixed (three fixed
decimals zeroed the x bounds of the inch axis: 89 zero bounds on C-7B); they are re-derived from
Claude's own pixels and calibration with the fixed tool in `rederived/` (same pixels, same
calibration; checked independently by Codex), and `overlays.csv` points there.

Codex's reading had one symbol it could not identify on C-7C (series `unidentified`); both
second-round adjudicators read it as the half-hidden diamond of 6.6 psi that Claude's reading
recorded, so that row is excluded.
