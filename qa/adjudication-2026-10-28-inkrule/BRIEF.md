# Is each marked point on its drawn line?

Two readers digitized curves from scanned plots of a 1968 NASA report (AM-68-1 Vol. II): direct shear
test curves (Appendix C), friction-angle and density charts and grain-size curves (Appendix A), modulus
plots (Appendix B). Each item marks one point a reader took on a drawn line (a "trace sample"). Your job:
look at the page and say whether that point is on the named curve's own ink. Judge only from the ink.

## Blindness rules

1. Work only inside this packet folder. Do not open, list or search anything else on the machine: not
   the project repository (`...\terramechanics`), not any folder named `extractions`, `qa`, `keys`,
   `audits`, `adj` or `adj-*`, and nothing outside this folder. If you catch yourself about to, stop.
2. Do not try to infer which reader took the point or why it was selected; it does not matter.

## Files

- `items.csv`: one row per item: `item`, `figure`, `panel`, `series` (the curve, for example a test's
  normal stress), `legend_symbol` (that curve's plotted symbol, empty when the figure has none),
  `figure_title`, `rotation` (degrees the figure is printed turned), `legend_entries`, the page pixel of
  the point `P` (origin top left, u right, v down), the `crop`, `crop_origin_px` and `crop_scale` (page
  pixel = origin + crop pixel / scale) and the `page`.
- `crops/item-NNN.png`: the page around the point, enlarged 6 times; the point is at the center of the
  gap of the red open cross.
- `pages/pNNNN.png`: full pages; follow a line to its legend or its symbols to know which line is which.
- `tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --zoom 4 --out <png>` (run `--help` first) makes a
  gridded crop. Python: `<local path>`.

## Conventions (settled by the project; apply them exactly)

1. A point counts as on the line when it is on the named line's own ink or within 2 px of it; within 2 px
   beyond the end of a dash also counts.
2. A point on a plotted symbol's outline or arms, inside a symbol's white interior, or in the white gap
   between dashes or between a dash and a symbol, is off the line. Do not bridge a gap: whatever the line
   would do if continued, a point in a gap is off it.
3. A line that runs into a symbol without a gap: a point on ink the line shares with the symbol's outline
   is off the line.
4. A line drawn through an open symbol's interior as its own stroke: a point on that stroke inside the
   symbol is on the line.
5. A curve that crosses a grid line is on its ink at the crossing (its ink continues on both sides). A
   curve that runs into a frame or grid line ends at the near edge of that line; a point further inside
   the frame or grid line is off.
6. A point on another curve's line, on a grid line the named curve does not cross there, on stray ink or
   on text is off the line (say what it is on).
7. Never guess: when the ink does not allow a decision (merged lines, a crossing of two curves, broken
   ink), answer `cannot tell` and say why.

## What to hand back

Fill `answers.csv` (columns `item`, `A`, `confidence`, `comment`): `A` is `yes` (on the named line's own
ink), `no` or `cannot tell`, lower case; `confidence` `high`, `medium` or `low`; `comment` short: what
the point is on (the line, a symbol's outline or interior, a gap, a grid line, another curve) and the
page pixel of the named line's nearest own ink. One row per item, none skipped. Keep CSV quoting valid.
