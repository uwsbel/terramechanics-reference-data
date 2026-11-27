# Re-checking points read off scanned plots

Two readers digitized the direct shear test figures of a 1968 NASA report (AM-68-1 Vol. II,
Appendix C, Figures C-1B to C-4C). The points in this packet were singled out for a closer look. For
each one, look at the page and say what is there. Judge only from the ink.

## Blindness rules

1. Work only inside this packet folder. Do not open, list or search anything else on the machine:
   not the project repository (`...\terramechanics`), not any folder named `extractions`, `qa`,
   `keys`, `audits`, `blind`, `adj` or `adj-*`, and nothing else outside this folder. If you catch
   yourself about to, stop.
2. On compare items you see two readings under neutral labels, **P** (blue circle) and **Q** (orange
   square); which reader is P changes from item to item and you are not told who is who. Do not try
   to infer it; it does not matter.

## The figures

Each figure has an upper panel (shear stress against shear displacement: one drawn line per test,
with the test's symbol printed along it) and a lower panel (dilation against shear displacement:
symbols, mostly without lines). Each test has its own symbol; the legend gives them, and the lower
panel uses the same symbols as the upper one. `figures.md` lists every figure's tests, symbols,
legend position and orientation.

## Files

- `items.csv`: one row per item: `item`, `kind`, `figure`, `panel`, `series` (the test), the
  `legend_symbol` of that test, the `question`, the page pixels of `P` and `Q` (origin top left, u
  right, v down), `box_P` (the half-widths in pixels of P's error box, on check items), the `crop`,
  `crop_origin_px` and `crop_scale` (page pixel = origin + crop pixel / scale), and the `page`.
- `crops/item-NNN.png`: the page around the item, enlarged. Compare items: P is a blue circle, Q an
  orange square, each centered on its reading. Check items: P is a small blue cross inside a blue box,
  the box being its error tolerance.
- `pages/pNNNN.png`: the full pages, for context (follow a line to the legend or to its other symbols).
- `tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --zoom 4 --out <png>` (run `--help` first) makes
  any other crop with a labeled pixel grid. Python with Pillow and numpy:
  `<local path>`.

## Conventions

1. **The center of a symbol** is the middle of its width and its height. For a triangle, its centroid
   (a third of the height in from the wide side) is also a valid center: readings use one or the
   other, and both are acceptable. A mark is at the center when it is within 3 px of a valid center.
2. **On the drawn line** means on the line's ink or within 2 px of it. A mark on a symbol's outline,
   the axis, a grid line or another test's line is not on this test's line.
3. **Identity**: if the symbol at the marks is not the named test's symbol, or the line is another
   test's line, answer `neither` on a compare item (`no` in B on a check item) and say in the comment
   what is there.
4. **Never guess.** When the ink does not allow a decision (overlapping symbols, a symbol on a grid
   line, broken ink), answer `cannot tell` and say why.

## The kinds of item and their answers

1. `compare-marker`: P and Q are two readings of the center of the same symbol. Which mark is at the
   center of the printed symbol? `p`, `q`, `both` (both within 3 px of a valid center), `neither`,
   `cannot tell`.
2. `compare-trace`: P and Q are two readings of the drawn line at the same x. Which mark is on the
   drawn line? `p`, `q`, `both`, `neither`, `cannot tell`.
3. `check-marker`: one reading P with its box. A: is the center of the printed symbol nearest P inside
   the box? B: is that symbol the named test's symbol, on that test's line? `yes`, `no`,
   `cannot tell` for each.
4. `check-trace`: one reading P with its box. A: does the named test's drawn line pass through the
   box? `yes`, `no`, `cannot tell`. Leave B empty.

## What to hand back

Fill `answers.csv` (columns `item`, `A`, `B`, `confidence`, `comment`) for every item: `A` (and `B`
on check-marker items) as above, in lower case; `confidence` `high`, `medium` or `low`; a short
`comment` saying what decided it, with the page pixel of the center or the line you found, for
example "down-triangle box u 1530 to 1552, v 2340 to 2360; middle (1541,2350), centroid (1541,2347);
P 1 px from the centroid, Q 9 px below". Keep the CSV quoting valid.
