# Blind reading of Figures C-7B and C-7C (direct shear data sheets printed sideways), batch curves-appc-b4

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right.

## Evidence packet (folder `packet/`)

Page images from AM-68-1 Vol. II (NASA CR-92215), Appendix C, 300 dpi, unrotated: `p0136.png`
(Figure C-7B, printed C-22) and `p0137.png` (Figure C-7C, printed C-23); context `p0115.png`
(Appendix C introduction) and `p0135.png` (Figure C-7A, the failure envelopes of these tests).
`figures-rows.csv` (the figures index rows), `series.csv`, `CURVE-READING.md` (the protocol;
follow it, including rule 7).

## These figures

Figures C-7B and C-7C (RSM-b soil, Dr 1.0 and Dr 0.53): one panel each, horizontal load (psi,
0 to 35) against horizontal motion (inches, 0 to .32), one series per direct shear test, plotted
symbols only (no drawn curves, no dilation panel). They are **printed sideways**: on the page as
scanned the horizontal-motion axis runs up the page and the load axis runs from right (0) to left
(35). Read them on the page as scanned (pixel coordinates of the unrotated image, protocol rule 5)
and calibrate with `tools/calibrate_axes.py detect ... --x-direction up --y-direction left`
(check that the printed labels confirm these directions: a wrong direction still fits with a small
residual, only your by-eye label check catches it).

Series ids are in `series.csv` (`n<normal stress in psi with p for the point>psi`, for example
`n27p1psi`); the ids come from the figures index, which has been wrong before: if the legend prints
another number, keep the id given and report the printed number in notes.md. Symbol names for these
figures, as seen with the figure turned upright: `quarter-circle` (the open D-shaped symbol of the
highest stress), `star`, `triangle-up`, `diamond`, `square`, `circle`; describe any other shape in a
note. Many symbols crowd near the origin and sit on grid lines: bound and note them, never guess.

What to produce, under `out/<figure_id>/`: `cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`
and `points-p1-native.csv` (every plotted symbol as `marker`, `panel = 1`; no trace or feature rows,
there are no drawn lines), `overlay-p1.png`, `notes.md`.

## Tools (folder `tools/`)

Python with Pillow and NumPy: `<local path>`. Run each
script with `--help` first. `tools/calibrate_axes.py detect|apply`, `tools/plot_grid.py
lines|crop|scan|overlay`. Write your own helpers under `out/`; do not modify `tools/`.

Finish with a short answer: per figure the marker counts per series, the calibration residuals,
the by-eye label checks, the ambiguities, and the files written. Do not paste the CSVs.

## For the Claude reader

You read ONE figure (named in your task) in your own workspace; write under `out/<figure_id>/`.
Blindness: do not open anything under the project repository, the dan-codex-from-claude folder,
or any other folder of the scratchpad than your workspace and this TASK.md. Look at PNGs with the
Read tool; make zoomed crops with `tools/plot_grid.py crop` (zoom 3 to 6).
