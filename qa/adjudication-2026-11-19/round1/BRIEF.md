# Adjudicating disputed points between two readings of scanned plots

Two readers digitized two figures of a 1968 NASA report (AM-68-1 Vol. I, Section IV) that record
vertical impacts of a footpad on soil. Where their readings differ, or where only one of them recorded
something, someone has to look at the page and say what is there. That is your job. You see the readings
under neutral labels, **P** (blue circles) and **Q** (orange squares); which reader is P changes from item
to item and you are not told who is who. Judge only from the ink.

## Blindness rules

1. Work only inside this packet folder. Do not open, list or search anything else on the machine:
   not the project repository (`...	erramechanics`), not any folder named `extractions`, `qa`,
   `keys-private`, `terramechanics-blind` or `dan-codex-from-claude` outside this folder, and no other
   adjudication packet. If you catch yourself about to, stop.
2. Do not try to infer which reader is P or Q; it does not matter.

## The figures

Three runs (series ids `run4`, `run10`, `run12`) appear in both figures with the same line styles: `run4`
solid, `run10` dotted, `run12` dashed (long dashes with short dashes between). The legend printed on the
figures says which line is which run; read it on the page. No plotted symbols appear on either figure.

1. **F4-19** (`pages/p0208.png`), printed **upright**, has two panels sharing a time axis (milliseconds,
   increasing to the right): panel 1 (top) is the vertical force on the footpad (lb, increasing up), panel 2
   (bottom) the footpad's displacement into the soil (in, increasing up). In the first few milliseconds the
   three lines rise together beside the left frame; later they cross and, near the end, run close together.
2. **F4-20** (`pages/p0209.png`) has one panel, force (lb) against displacement (in), and is printed
   **sideways**. Crops and pixel positions are of the page as scanned, not turned: on them displacement
   increases **up** (smaller v) and force increases to the **left** (smaller u); the origin is at the bottom
   right of the plot. The three lines start together in that corner. The scan has a blank strip near 1.6 to
   1.9 in of displacement where the dotted line and the grid are missing; a sample in that strip with no ink
   under it is off the line. Run 4 ends in a sharp hook near 4.1 in where its line doubles back.
3. Some traces run together or cross; where they do, convention 3 below applies.

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
5. A peak is a local maximum of the force or displacement (a trace here has several); its height
   matters, and on a flat top its time or displacement does not. A minimum likewise: its depth matters.
6. When you answer `neither`, give in the comment the pixel position you would put the point at.
7. **"At the mark" for a knee or kink** means within 8 px of the corner of the bend (about two
   half-widths of the line). A `feature-only` knee or kink is `yes` when the line visibly changes
   direction on a 4x crop and the mark is within 8 px of that corner; `no` when the line runs
   straight through the mark, or the nearest bend's corner is farther than 8 px away (say where it
   is); a change of direction too small to see on a 4x crop is `no`.
8. **Two different bends.** When the two marks of a `feature-disagree` knee sit on two different
   real bends, answer `cannot tell` and write `two bends` and both corners' pixels in the comment.

## What to write

`answers.csv` in this folder with columns `item,answer,confidence,comment`: `answer` as above,
lower case; `confidence` high, medium or low; `comment` short: what decided it, or what is
ambiguous. One row per item, none skipped; when unsure, `cannot tell` with a reason beats a guess.
Look at every crop; open a larger crop or the page when the crop does not show enough. Write in
US English, with no em-dashes or en-dashes.

Finish with a short report: counts of answers by kind, and the items you found hardest.
