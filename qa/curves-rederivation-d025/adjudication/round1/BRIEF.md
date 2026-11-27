# Adjudicating disputed points between two readings of scanned plots

Two readers digitized twenty-two figures from a 1968 NASA report (AM-68-1 Vol. II, Appendix C). Where their readings differ, or where only one of
them recorded something, someone has to look at the page and say what is there. That is your job.
You see the readings under neutral labels, **P** (blue circles) and **Q** (orange squares); which
reader is P changes from item to item and you are not told who is who. Judge only from the ink.

## Blindness rules

1. Work only inside this packet folder. Do not open, list or search anything else on the machine:
   not the project repository (`...\terramechanics`), not any folder named `extractions`, `qa`,
   `keys-private`, `blind`, `adj` (an earlier adjudication) or `dan-codex-from-claude`. If you catch yourself about to, stop.
2. Do not try to infer which reader is P or Q; it does not matter.

## The figures

Three kinds of figure from AM-68-1 Vol. II, Appendix C (page images in `pages/`, 300 dpi, PDF pages
116 to 137):

1. **Direct shear data sheets** FC-1B to FC-1D, FC-2B, FC-2C, FC-3B, FC-3C, FC-4B, FC-4C, FC-5B,
   FC-6B, FC-6C, FC-6D: upper panel shear stress (psf) against shear displacement (thousandths of
   an inch), one hand-drawn curve per test through its symbols, often dashed and interrupted around
   every symbol; lower panel dilation against the same displacement, symbols only, stacked tightly.
   Each test (series `n<normal stress psf>`) has its own symbol (legend at the right).
2. **Psi data sheets printed sideways** FC-7B (p0136), FC-7C (p0137): load (psi) against motion
   (inches), symbols only. The crops show the page as scanned, so these read rotated by 90 degrees;
   a triangle pointing left on the page is a triangle pointing up on the figure.
3. **Failure envelopes** FC-1A, FC-2A, FC-3A, FC-4A, FC-5A, FC-6A, FC-7A: maximum shear stress
   against normal stress (psi on FC-7A); per density group of the legend, symbols and a straight
   fitted line, sometimes with a dashed extension to the axis. The symbols are the peaks of the
   tests of the data sheets (also in `pages/`).

## Files

- `items.csv`: one row per item: `item`, `kind`, `figure`, `panel`, `series`, `legend_symbol`, the
  `question`, the points of `P` and `Q` (page pixel `px (u,v)`, origin top left, u right, v down;
  the value read; in brackets the test and symbol where it matters), the `crop` (the page around the
  item, enlarged `crop_scale` times, origin at `crop_origin_px`; P drawn as blue circles, Q as
  orange squares, traces as dots joined by thin lines), and kind-specific columns.
- `crops/item-NNN.png`: the picture of each item. Look at it with your image viewer.
- `pages/pNNNN.png`: the full pages, for context (the legend, where a curve goes, which symbol
  belongs to which test).
- `tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --zoom 4 --out <png>` (run `--help` first)
  makes any other crop with a labeled pixel grid when an item's crop is not enough. Python with
  Pillow: `<local path>`.

## The kinds of item and their answers

1. `marker-disagree`: both readers put the same symbol of the same test here at different centers.
   Which mark is on the center of the printed symbol? `p`, `q`, `both` (both inside the symbol),
   `neither`, `cannot tell`. Say in the comment if the symbol is not this test's.
2. `feature-disagree`: the readers' first point, last point or peak of a drawn line differ (their
   own notes are in `note_P`, `note_Q`). Which mark is that point of the drawn line? For a peak the
   height matters; on a flat top its x does not. `p`, `q`, `both`, `neither`, `cannot tell`.
3. `trace-disagree`: which trace sample is on the drawn line? `p`, `q`, `both`, `neither`, `cannot tell`.
4. `identity`: one symbol was recorded under two different tests. Answer the series id it belongs
   to (from its shape and the legend), `both` if there really are two symbols there, or `cannot tell`.
5. `marker-only`: only one reader recorded a symbol at the subject mark (the question says whether
   that is P or Q; the other reader's marks within 45 px are drawn under the other label). Is there
   a printed symbol of that test, centered there? `yes`, `no` (say in the comment what is there, for
   example another test's symbol), `cannot tell`.
6. `feature-only`: only one reader marked this point; is it on the drawn line and is it what its
   note says? `yes`, `no`, `cannot tell`.
7. `curve-start`, `curve-end`, `trace-gap`: a run of trace samples only one reader took (the subject
   label is named in the question), at the start of a curve, at its end, or inside a gap of the other
   reader's trace. Is every subject sample on the ink of that test's drawn line? A sample on a plotted
   symbol rather than the line, in white space, on another test's curve or on a grid line with no
   curve under it is off the line. `all yes`, `all no`, `some` (and list the off-line ones by pixel in
   the comment), `cannot tell`.

## Conventions (settled by the project; apply them)

1. A trace sample counts as on the line when it is on the line's ink or within 2 px of it at the
   line's height. A sample on a symbol's outline, or in the white gap between a dash and a symbol,
   is off the line, even if its height is close.
2. The first or last point of a drawn line is where its ink starts or ends. When the line runs into
   a plotted symbol without a white gap, the point is the symbol's center; when a white gap
   separates the line's end from the symbol, it is the end of the ink.
3. For an identity item, `both` means two separate symbols are printed there (name them in the
   comment); a white pocket enclosed by the strokes of neighbouring symbols is not a symbol.
4. The center of a triangle is its centroid (one third of the height from the base). A mark between
   the centroid and the middle of the triangle's bounding box is on the center. In a tight stack of
   symbols, make sure the mark is on the symbol of the named test and not on its neighbour.

## What to write

`answers.csv` with columns `item,answer,confidence,comment`: `answer` as above, lower case;
`confidence` high, medium or low; `comment` short: what decided it, or what is ambiguous. One row per
item in your range, none skipped; when unsure, `cannot tell` with a reason beats a guess. Look at
every crop; open a larger crop or the page when the crop does not show enough.

Finish with a short report: counts of answers by kind, and the items you found hardest.
