# Claude's answer (written before Codex ran)

Piecewise, per axis, between the printed lines including the frame as the value it carries, for
every panel, not only the uneven ones. Reason: the 1968 drafter placed each symbol by eye between
the lines drawn on that sheet, so the drawn lines are the scale; an affine map averages the drafting
irregularity over the whole axis and puts a systematic error where the drawing is uneven, which is
exactly at the origin on FC-5B, FC-6B, FC-6C, FC-6D. On a uniform grid piecewise and affine coincide,
so applying it always costs nothing and avoids a threshold.

Mechanics: `calibrate_axes.py` already locates every line with its tilt; `detect` would also store,
per axis, the fitted lines (value, intercept, slope) and `apply` would locate a point between the two
neighbouring lines along each axis (bilinear in the cell, which keeps the tilt) instead of the global
affine. Residuals: the affine residual remains a diagnostic of how uneven the drafting is (reported,
not used to pick); the piecewise map has zero residual at the lines by construction, so the
calibration check becomes the by-eye label check plus agreement of the two readers' line positions
(the diff compares the two readings' lines, within one line width). Canonical rule: with both readers
on piecewise maps from printed lines, the calibrations agree within a line width and the residual
rule no longer distinguishes them; the canonical reading becomes the one whose points are kept by the
existing rules (unchanged), and calibration disagreement beyond a line width is a disagreement to
settle on the page. Readings already made: re-derive both readers' values from their pixels with
their own detected lines (each submission's `cal-p*/calibration.json` holds them), under
`qa/<batch>/rederived/`, rerun the diffs and carry the decisions over by point identity (they name
points by source and sequence, which do not change). Bounds: the pixel bound times the local scale
of the cell, plus a term for line-location uncertainty (half a line width in value units).

Change my mind: evidence that the symbols were plotted with a uniform scale (for example a template
or a plotting machine) and the grid drawn separately, in which case the grid irregularity would not
be in the data and the affine map (with the frame as zero) would be the better model.
