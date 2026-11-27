# Review of batch curves-appc-b6: failure envelopes C-5A, C-6A, C-7A

Read 2026-10-14 by both agents, blind, from evidence packets written by `tools/make_reading_packet.py`
from `batch.json` (page images, the figures-index rows without the agents' notes columns, the series
list, the protocol and the two reading tools). Reconciled under D-025 and D-026 with every other curve
batch (`qa/curves-rederivation-d025/review.md`), with the same blind adjudication.

## Readings

1. **Interruption.** A machine restart stopped all four readers early: each had calibrated its figure
   and written check images, none had written points. The Codex thread was resumed with
   `prompt-resume.md`; one new Claude reader per figure continued in the same workspace, told to verify
   the earlier calibration before relying on it (all three re-ran it and reproduced it exactly). Both
   submissions record this in `meta.json`.
2. **Calibration.** All three figures have drawn grids (1000 psf on C-5A and C-6A, 5 psi on C-7A), so
   both readers used detected grid lines; no line is predicted. On C-6A the 5000 psf line is hidden by
   the legend over most of its length; on C-5A the top frame carries no label and its value, 6000 psf,
   follows the spacing (Codex's note), which the frame's position confirms (no symbol is above
   2700 psf). Codex's affine residuals: 5.0 and 7.6 psf (C-5A), 3.0 and 6.3 psf (C-6A), 0.026 and
   0.031 psi (C-7A).
3. **Agreement.** 203 points matched, 202 agreed; canonical 223 points (agreed 202,
   one-sided-verified 18, resolved 1, open 2).

## Identity

Each envelope's symbols were checked against the peaks of their own data sheets, both readings
(`insights/1968-vol2-appendix-c-envelopes-against-data-sheets.md`, findings 4 to 7):

1. **C-7A**: dotted circles are the tests of C-7C (Dr 0.53) and dotted triangles those of C-7B (Dr 1.0),
   every symbol within 0.4 psi of its test's peak. Printed angles 45 and 50.5 degrees; Claude's reader
   measures the drawn lines at 45.5 and 50.7.
2. **C-6A** prints no friction angle and no line label. Circles are the loose tests of C-6B (within 4 to
   35 psf), squares the dense tests of C-6C (5 to 51 psf), triangles those of C-6D (24 to 90 psf below).
   A mark Codex's reader recorded as an unlisted downward triangle, without a series, is the circle of
   C-6B's 2934 psf test (both adjudicators, item 261). The dense group's flatter line is in the data
   sheets themselves. C-6C's legend prints its second test at 1961 psf; C-6A plots it at about 1740 psf
   with its peak to 1 psf.
3. **C-5A**: only the circles (Dr .02 to .13) have data sheets here (C-5B); three are within 25 psf of
   their tests' peaks, the 734 psf one 55 psf above and the 3815 psf one 104 psf below, in both
   readings. The other groups are credited on the figure to Bendix Report No. MM-65-2; the figures index
   read MM-66-2, corrected (`qa/inventory-vol2-b1/corrections.csv`, with the two documents that had
   repeated it). Printed angles 41.5, 36.9, 32.8 and 29 degrees; Claude's reader measures 41.2, 36.4,
   33.2 and 29.6.

## Points for the human audit

1. C-5A: a possible symbol hidden in the merged lines near the origin (sigma about 300, tau about
   240 psf), which Codex's reader recorded without a series and Claude's reader noted as a white pocket;
   both adjudicators in both rounds: cannot tell. It stays one-sided and enters no record.
2. C-6A: where the dense group's dashed line starts at the origin (Claude's sample 1), split in both
   rounds.
3. C-6A: a circle printed outside the frame at sigma about -141, tau about -156 psf, on the dashed
   extension of the loose group's line. Both adjudicators confirm a circle (Codex's reader took it for
   the axis zero; it is round and of the data circles' size, while this page's digits are taller
   ovals). A test cannot have negative stresses, so Claude excluded it from the data as not an
   observation; a person should confirm.
