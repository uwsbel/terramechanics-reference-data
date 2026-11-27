# Re-checking points read off scanned plots

Two readers digitized the direct shear test figures of a 1968 NASA report (AM-68-1 Vol. II,
Appendix C, Figures C-1B to C-4C). The 72 points in this packet were singled out for a closer look; item numbers are not consecutive. For
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

## This is a second round: settled conventions, apply them exactly

The items here are the ones on which a first round of adjudication did not agree. The project settled
the following conventions earlier (quoted from its adjudication of 2026-10-15); they take precedence
over anything above that seems to say otherwise.

1. A trace sample counts as on the line when it is on the line's ink or within 2 px of it at the
   line's height; within 2 px beyond the end of a dash also counts. A sample on a symbol's outline,
   or in the white gap between dashes or between a dash and a symbol, is off the line.
2. A line that runs into a plotted symbol without a gap: a trace sample in ink the line shares with
   the symbol's outline is off the line (the trace sample belongs on the line's own ink).
3. A curve that runs into a frame or grid line ends where its own ink can no longer be told from the
   line it meets: at the near edge of that line, not at its centre. A sample within 2 px of the
   curve's last visible ink counts as on the line; a sample further inside the frame or grid line
   does not.
4. The center of a triangle is its centroid (one third of the height from the base). A mark between
   the centroid and the middle of the triangle's bounding box is on the center.
5. A circle crossed by a grid line or a curve is still one circle; its center is the center of its
   ring. Two rings that overlap are two symbols only if both rings can be traced.
6. When you answer `neither`, give in the comment the pixel position you would put the point at.

Two measurement rules for this packet:

7. The 3 px tolerance of a symbol center is a straight-line (Euclidean) distance. When the center
   itself cannot be placed to better than about 1 px (a symbol merged with a grid line, the frame,
   its line or another symbol) and the answer would change within that uncertainty, answer
   `cannot tell` and give the distances in the comment.
8. Do not bridge a gap in a drawn line. Where the line stops at a symbol and a reading falls in the
   gap or on the symbol, that reading is off the line (convention 1), whatever the line would do if
   continued; if both readings are off the line, the answer is `neither`.
