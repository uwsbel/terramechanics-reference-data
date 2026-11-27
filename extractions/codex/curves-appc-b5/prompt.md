# Blind reading of Figures C-1A, C-2A, C-3A, C-4A (failure envelopes), batch curves-appc-b5

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right.

## Evidence packet (folder `packet/`)

Page images from AM-68-1 Vol. II (NASA CR-92215), Appendix C, 300 dpi, unrotated: `p0116.png`
(Figure C-1A, printed C-2), `p0120.png` (C-2A, C-6), `p0123.png` (C-3A, C-9), `p0126.png` (C-4A,
C-12); context `p0115.png` (Appendix C introduction).
`figures-rows.csv` (the figures index rows), `series.csv`, `CURVE-READING.md` (the protocol;
follow it, including rule 7).

## These figures

Figures C-1A, C-2A, C-3A and C-4A are **failure envelopes**: maximum shear stress (psf) against
normal stress (psf), one panel each, upright. Each density group of the legend is one series: its
plotted symbols are the peak shear stresses of the direct shear tests of that group, and a straight
line drawn through them (solid, extended to the shear-stress axis by a dashed part) is the authors'
fit, labelled with a friction angle. Series ids are in `series.csv`, named by the printed Dr range of
the group (`dr50-57` for Dr .50 to .57); the index the ids come from has been wrong before: if the
legend prints something else, keep the id given and report what is printed in notes.md.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`:
   - every plotted symbol as `marker`, with `symbol` (`circle`, `filled circle`, `square`,
     `triangle-up`, `triangle-down`, `x`, `plus`, `asterisk`, or a described shape) and its series.
     The legend gives each group's symbol; where the drawing does not match the legend (a symbol of
     another shape or fill on a group's line), assign the series by the line it sits on and say so
     in the note. Overlapping or hidden symbols: wide bound and a note, never a guess.
   - each drawn line as `trace` samples in drawing order from its left end: its left end (on the
     shear-stress axis if the dashed part reaches it), then every 250 psf of normal stress, then its
     right end. Mark samples on the dashed part with "dashed" in the note. Bound: half the line
     thickness (rule 7: on the line's ink, not on a symbol).
   - per series one `feature` with note "intercept": the point where the line (dashed or solid)
     meets the normal-stress-zero axis; and one `feature` with note "label: <the printed angle>"
     placed at the printed angle label (the label's center), so the label can be matched to its line.
3. `overlay-p1.png`, `notes.md` (which line carries which printed angle, symbols that do not match
   the legend, anything ambiguous).

## Tools (folder `tools/`)

Python with Pillow and NumPy: `<local path>`. Run each
script with `--help` first. `tools/calibrate_axes.py detect|apply`, `tools/plot_grid.py
lines|crop|scan|overlay`. Write your own helpers under `out/`; do not modify `tools/`.

Finish with a short answer: per figure the counts per series and kind, the printed angles, the calibration residuals,
the by-eye label checks, the ambiguities, and the files written. Do not paste the CSVs.
