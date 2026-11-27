# One method question: affine or piecewise calibration on unevenly drafted grids

Same arrangement as before: Claude's answer is in a file you cannot see; the better reasoning wins.
Read-only in the repository (`docs/CURVE-READING.md` sections 2 and 4, `docs/decisions.csv` D-023 and
D-024, `tools/calibrate_axes.py`, the readings under `extractions/{claude,codex}/curves-appc-b3/`
and their `notes.md`, the diffs `qa/curves-appc-b3/diff-*.md`).

## Evidence

1. `calibrate_axes.py` fits one affine map per panel to the grid intersections. The 1968 grids are
   hand drafted and not uniform: on FC-5B the 0 to 50 thousandths interval is drawn about 314 px wide
   against 291 to 297 px for the others; on FC-6B and FC-6D about 318 px against 293.5; on FC-6C about
   4 percent wider; on FC-1A (an envelope) 286, 287, 294.5 and 311.5 px per 1000 psf. The x residuals
   of these panels reach 0.5 to 0.7 percent of the span at their maximum.
2. On FC-6B and FC-6D the two readings made different choices: Claude's readers fitted only the
   printed gridlines 50 to 250 (the unlabelled left frame then reads x = -4 to -4.7, so symbols drawn
   on the frame, the zero-displacement points of each test, read about -4); Codex took the frame as
   x = 0. Claude's map minus Codex's map at the pixels where Codex reads 0, 50, 150, 250: FC-6B upper
   -2.61, -1.89, -0.46, +0.98 thousandths; FC-6D upper -2.01, -1.46, -0.35, +0.76. On every other data
   sheet both readers took the frame as zero and their maps agree within 0.1 thousandths.
3. The beginning of each shear curve (0 to 50 thousandths) carries the initial stiffness, which the
   simulator calibration will use; an error of 2 to 4 thousandths there is 5 to 10 percent of the
   displacement at the first symbols.

## Question

Should the protocol keep one affine map per panel, or map each axis piecewise linearly between the
printed lines (frame included as the axis value it carries), on the argument that the drafter plotted
each symbol against the drawn lines, so the drawn lines are the scale? If piecewise: when (always,
or when the drawn spacing departs from uniform by more than some amount), how bounds and residuals
work, what happens to the readings already made (both readers' pixels are kept; their values would be
re-derived), and what the canonical rule becomes. If affine: which choice is right on FC-6B and FC-6D
(frame as zero, or gridlines only), and how the bounds should carry the drafting irregularity.
Recommendation, reason, what would change your mind; a page at most; no edits.
