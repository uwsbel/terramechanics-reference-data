# Adjudicating disputed points between two readings of scanned plots

Two readers digitized thirty-four figures of a 1968 NASA report (AM-68-1 Vol. II, Appendices A, B
and C). Where their readings differ, or where only one of them recorded
something, someone has to look at the page and say what is there. That is your job. You see the
readings under neutral labels, **P** (blue circles) and **Q** (orange squares); which reader is P
changes from item to item and you are not told who is who. Judge only from the ink.

## Blindness rules

1. Work only inside this packet folder. Do not open, list or search anything else on the machine:
   not the project repository (`...\terramechanics`), not any folder named `extractions`, `qa`,
   `keys-private`, `blind`, `adj`, `adj-*` other than this one, or `dan-codex-from-claude`. If you
   catch yourself about to, stop.
2. Do not try to infer which reader is P or Q; it does not matter.

## The figures

Two kinds of figure (page images in `pages/`, 300 dpi):

1. **Computer-plotted failure envelopes** FC-8 to FC-15 (PDF pages 138 to 151): shear strength
   against normal stress, both axes printed "(x 10^1)" psf, so the values read are in psf (ten times
   the printed tick numbers). One test group per figure: triangle symbols (the peak shear stresses of
   its tests) and one straight least-squares line. A box above the plot prints the group's average
   density, friction angle, tan theta and cohesion.
2. **Friction angle against relative density** FC-16 to FC-23 (PDF pages 152 to 159): phi_DS in
   degrees against Dr. FC-16 to FC-20 and FC-22: open circles (some joined in pairs by a short
   horizontal line), a solid curve (series `mean`) and two dashed curves (`upper`, `lower`). FC-21:
   circles and a cross-hatched band whose edges are `band-top` and `band-bottom`. FC-23: six curves
   labelled with soil names (series `rc2`, `ps`, `rs`, `rsm-b`, `rsm-a`, `ss`), in different line
   styles, no symbols. On these figures the frame extends one grid interval beyond the labelled
   lines on every side.

Also:




3. **Appendix B modulus plots** FB-3 to FB-7 (PDF pages 109 to 113): modulus E = rho c^2 (kips/in.^2)
   against confining pressure sigma_3 (psi), one soil per figure; per density group (series `dr<Dr in
   hundredths>`, `dr99p5` for Dr 0.995) open circles (FB-7: squares with an x, open and filled
   circles) and a polyline of straight segments drawn by the authors, labelled with the group's Dr.
   The frames carry ticks, not grid lines. Features: first point, vertices, last point, and the
   group's printed label.
4. **Appendix A friction-angle charts** FA-4, FA-8, FA-20, FA-24, FA-28, FA-40, FA-48 (PDF pages 9
   to 97): angle of internal friction (degrees) against relative density Dr, one solid curve per
   figure (series `curve`); FA-40 a cross-hatched band whose edges are `band-top` and `band-bottom`.
   Features: first point, last point and knees (a knee is a bend where the slope changes; readers
   may disagree on whether a gentle bend is one).

## Files

- `items.csv`: one row per item: `item`, `kind`, `figure`, `panel`, `series`, `legend_symbol`, the
  `question`, the points of `P` and `Q` (page pixel `px (u,v)`, origin top left, u right, v down;
  the value read; in brackets the series and symbol where it matters), the `crop` (the page around
  the item, enlarged `crop_scale` times, origin at `crop_origin_px`; P drawn as blue circles, Q as
  orange squares, traces as dots joined by thin lines), and kind-specific columns.
- `crops/item-NNN.png`: the picture of each item. Look at it with your image viewer.
- `pages/pNNNN.png`: the full pages, for context.
- `tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --zoom 4 --out <png>` (run `--help` first)
  makes any other crop with a labeled pixel grid when an item's crop is not enough. Python with
  Pillow: `<local path>`.

## The kinds of item and their answers

1. `marker-disagree`: both readers put a symbol of the same series here at different centers.
   Which mark is on the center of the printed symbol? `p`, `q`, `both` (both inside the symbol),
   `neither`, `cannot tell`. Say in the comment if the symbol is not this series'.
2. `feature-disagree`: the readers' first point, last point or another named point of a drawn line
   differ (their own notes are in `note_P`, `note_Q`). Which mark is that point of the drawn line?
   `p`, `q`, `both`, `neither`, `cannot tell`.
3. `trace-disagree`: which trace sample is on the drawn line? `p`, `q`, `both`, `neither`, `cannot tell`.
4. `identity`: one symbol was recorded under two different series. Answer the series id it belongs
   to, `both` if there really are two symbols there, or `cannot tell`.
5. `marker-only`: only one reader recorded a symbol at the subject mark (the question says whether
   that is P or Q; the other reader's marks within 45 px are drawn under the other label). Is there
   a printed symbol of that series, centered there? `yes`, `no` (say in the comment what is there),
   `cannot tell`.
6. `feature-only`: only one reader marked this point; is it on the drawn line and is it what its
   note says? `yes`, `no`, `cannot tell`.
7. `curve-start`, `curve-end`, `trace-gap`: a run of trace samples only one reader took (the subject
   label is named in the question), at the start of a curve, at its end, or inside a gap of the other
   reader's trace. Is every subject sample on the ink of that series' drawn line? A sample on a
   plotted symbol rather than the line, in white space, on another curve or on a grid line with no
   curve under it is off the line. `all yes`, `all no`, `some` (and list the off-line ones by pixel in
   the comment), `cannot tell`.

## Conventions (settled by the project; apply them)

1. A trace sample counts as on the line when it is on the line's ink or within 2 px of it at the
   line's height; within 2 px beyond the end of a dash also counts. A sample on a symbol's outline,
   or in the white gap between dashes or between a dash and a symbol, is off the line.
2. The first or last point of a drawn line is where its ink starts or ends. When the line runs into
   a plotted symbol without a white gap, the point is the symbol's center; when a white gap separates
   the line's end from the symbol, it is the end of the ink. A line that runs into a grid line or the
   frame ends where its own ink can no longer be told from the line it meets.
3. For an identity item, `both` means two separate symbols are printed there (name them in the
   comment).
4. The center of a triangle is its centroid (one third of the height from the base). A mark between
   the centroid and the middle of the triangle's bounding box is on the center.
5. A circle crossed by a grid line or a curve is still one circle; its center is the center of its
   ring. Two rings that overlap are two symbols only if both rings can be traced.
6. When you answer `neither`, give in the comment the pixel position you would put the point at.

## This is a second round

Every item here is a sample or point that only one reader recorded and that is still unconfirmed:
either the first round's two adjudicators disagreed on it, or it became unpaired when the other
reader's nearby sample was excluded in the first round. Two conventions decided most of the first
round; apply them exactly:

7. **A curve that runs into a frame or grid line** ends where its own ink can no longer be told
   from the line it meets: at the near edge of that line, not at its centre. A sample within 2 px
   of the curve's last visible ink counts as on the line; a sample further inside the frame or
   grid line does not.
8. **A line that runs into a plotted symbol** (a circle or triangle) without a gap: a trace sample in
   ink the line shares with the symbol's outline is off the line (the trace sample belongs on the
   line's own ink; the end of the line is carried by its first or last point feature).

## What to write

`answers.csv` with columns `item,answer,confidence,comment`: `answer` as above, lower case;
`confidence` high, medium or low; `comment` short: what decided it, or what is ambiguous. One row per
item in your range, none skipped; when unsure, `cannot tell` with a reason beats a guess. Look at
every crop; open a larger crop or the page when the crop does not show enough.

Finish with a short report: counts of answers by kind, and the items you found hardest.
