# Adjudicating disputed points between two readings of scanned plots

Two readers digitized eight load-penetration figures of a 1968 NASA report (AM-68-1 Vol. I,
Section II). Where their readings differ, or where only one of them recorded something, someone has
to look at the page and say what is there. That is your job. You see the readings under neutral
labels, **P** (blue circles) and **Q** (orange squares); which reader is P changes from item to item
and you are not told who is who. Judge only from the ink.

## Blindness rules

1. Work only inside this packet folder. Do not open, list or search anything else on the machine:
   not the project repository (`...\terramechanics`), not any folder named `extractions`, `qa`,
   `keys-private`, `terramechanics-blind` or `dan-codex-from-claude` outside this folder, and no other
   adjudication packet. If you catch yourself about to, stop.
2. Do not try to infer which reader is P or Q; it does not matter.

## The figures

Each figure is one panel: load (lb) against penetration (in) of a penetrator pushed into a soil bed,
recorded by a chart recorder. No plotted symbols (circles, triangles) appear on any of them.

1. **Printed sideways** (penetration increases **up** the page, load increases to the **left**):
   F2-29 (`pages/p0080.png`), F2-32 (`p0088`), F2-33 (`p0089`), F2-34 (`p0090`), F2-45 (`p0106`),
   F2-48 (`p0109`).
2. **Upright** (penetration to the right, load up): F2-46 (`p0107`), F2-47 (`p0108`).
3. Series ids `lptNN` are recorded traces (LPT = load penetration test, numbered), drawn solid, dotted,
   dashed, thin or thick; on F2-45 to F2-48 each figure has one solid and one dotted or dashed trace.
4. On F2-32, F2-33 and F2-34 the authors also drew **straight lines**: series `fit` (labelled
   `Slope = ... lbs./in.`) and on F2-33 series `bce` (labelled `Bearing Capacity Equation`). Their
   points are trace samples on the line, the ends of its ink, a feature noted `intercept` where the
   line meets penetration 0 (only if its ink reaches it), and a feature noted `label: <text>` at the
   center of its printed label.

## Files

- `items.csv`: one row per item: `item`, `kind`, `figure`, `panel`, `series`, the `question`, the
  points of `P` and `Q` (page pixel `px (u,v)`, origin top left, u right, v down; the value read),
  the `crop` (the page around the item, enlarged `crop_scale` times, origin at `crop_origin_px`; P
  drawn as blue circles, Q as orange squares, traces as dots joined by thin lines), and kind-specific
  columns (`note_P`, `note_Q`: the readers' own notes on a feature).
- `crops/item-NNN.png`: the picture of each item. Look at it with your image viewer.
- `pages/pNNNN.png`: the full pages, for context.
- `tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --zoom 4 --out <png>` (run `--help` first)
  makes any other crop with a labeled pixel grid when an item's crop is not enough. Python with
  Pillow: `<local path>`.

## The kinds of item and their answers

1. `feature-disagree`: the readers' first point, last point, peak or another named point (knee,
   kink, intercept, label) of a drawn line differ (their own notes are in `note_P`, `note_Q`). Which
   mark is that point of the drawn line? `p`, `q`, `both`, `neither`, `cannot tell`.
2. `trace-disagree`: which trace sample is on the drawn line? `p`, `q`, `both`, `neither`, `cannot tell`.
3. `feature-only`: only one reader marked this point; is it on the drawn line and is it what its
   note says? `yes`, `no`, `cannot tell`.
4. `curve-start`, `curve-end`, `trace-gap`: a run of trace samples only one reader took (the subject
   label is named in the question), at the start of a curve, at its end, or inside a gap of the other
   reader's trace. Is every subject sample on the ink of that series' drawn line? A sample in white
   space, on another curve, on a label or leader arrow, or on a grid line or the frame with no curve
   under it is off the line. `all yes`, `all no`, `some` (and list the off-line ones by pixel in the
   comment), `cannot tell`.

## Conventions (settled by the project; apply them)

1. A trace sample counts as on the line when it is on the line's ink or within 2 px of it at the
   line's height; within 2 px beyond the end of a dash or a dot also counts. A sample in the white
   gap between dashes or dots is off the line.
2. The first or last point of a drawn line is where its ink starts or ends. A line that runs into a
   grid line or the frame ends where its own ink can no longer be told from the line it meets: at
   the near edge of that line, not at its center. A sample within 2 px of the curve's last visible
   ink counts as on the line; a sample further inside the frame or grid line does not.
3. Where two traces touch or run together, a sample is on the series' line only if the ink it sits
   on can be followed back to that series (by line style, dash or dot pattern, thickness or
   continuity); say in the comment how you told them apart, or answer `cannot tell`.
4. A knee or kink is a judgment on a bend. For a `feature-disagree` knee, answer `both` when both
   marks are on the same bend of the line within its width, and name the mark only when one of them
   is clearly off the bend or on the straight part. For a `feature-only` knee or kink, answer `yes`
   when the line visibly changes direction at the mark.
5. A peak is the highest load of the trace; its height matters, and on a flat top its penetration
   does not.
6. When you answer `neither`, give in the comment the pixel position you would put the point at.
7. **"At the mark" for a knee or kink** means within 8 px of the corner of the bend (about two
   half-widths of the line). A `feature-only` knee or kink is `yes` when the line visibly changes
   direction on a 4x crop and the mark is within 8 px of that corner; `no` when the line runs
   straight through the mark, or the nearest bend's corner is farther than 8 px away (say where it
   is); a change of direction too small to see on a 4x crop is `no`.
8. **Two different bends.** When the two marks of a `feature-disagree` knee sit on two different
   real bends, answer `cannot tell` and write `two bends` and both corners' pixels in the comment.

## A second round

Every item here was answered differently by two adjudicators in a first round, or lost its
counterpart when a neighboring sample of the other reading was excluded there (most `curve-start`
items: the other reading's first samples sat inside the frame). Look again with care; a pixel-level
look at the page (`tools/plot_grid.py`) usually settles it.

## What to write

`answers.csv` in this folder with columns `item,answer,confidence,comment`: `answer` as above,
lower case; `confidence` high, medium or low; `comment` short: what decided it, or what is
ambiguous. One row per item, none skipped; when unsure, `cannot tell` with a reason beats a guess.
Look at every crop; open a larger crop or the page when the crop does not show enough. Write in
US English, with no em-dashes or en-dashes.

Finish with a short report: counts of answers by kind, and the items you found hardest.
