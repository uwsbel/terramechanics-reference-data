# Review of batches curves-appc-b7 to -b11: the last figures of Appendix C

Computer-plotted envelopes Figs. C-8 to C-15 (`curves-appc-b7` C-8, 9A, 9B, 9C, 10A; `-b8` C-10B, 10C,
11A, 11B, 11C; `-b9` C-12 to C-15) and friction-angle charts Figs. C-16 to C-23 (`-b10` C-16 to C-19;
`-b11` C-20 to C-23). With these, every in-scope figure of Appendix C has been read by both agents.

## Readings

Read 2026-10-14 by both agents, blind, from evidence packets written by `tools/make_reading_packet.py`
from each batch's `batch.json` (the figures' page images and the Appendix C text page, the figures-index
rows without the agents' notes, the series list, the protocol, the two reading tools). Codex: one run
per batch, gpt-6.1-sol high, 6 to 15 minutes each. Claude: one subagent per friction-angle chart and
one per computer-plot batch (the plots are simple: one line and five to eleven triangles), each in a
workspace outside the repository, filed after the Codex runs had finished; runs in each submission's
`meta.json`. The computer-plot readers were also asked to compare their traced line with the printed
box (tan theta, cohesion) without moving any point toward it.

## Calibration

Every grid line of every figure was found by the grid tool (none predicted) and passed the ink check.
The computer plots' grid is drafted unevenly (about 299 px for the first 1000 psf of shear strength,
287 px for the fifth; read as drawn by the piecewise map, D-025); their axes print "(x 10^1)" and both
readers calibrated in psf. The friction-angle charts' frame runs one grid interval beyond the labelled
lines on every side; both readers anchored only labelled lines. The two maps agree within their line
errors at every place compared, on all twenty-two figures (on the computer plots the largest
difference is 4 psf).

## Agreement and adjudication

First comparison: 941 points agreed of 946 matched; 5 disagreed (four FC-23 samples where the PS and
RS curves cross, one FC-21 band end) after the comparison was taught that a text label agrees by its
words (`diff_curves.py`, commit 0f551d2: the soil names of C-23 had counted as disagreements). The
one-sided points were curve ends that only one reader sampled. Four rounds of blind adjudication (a
Claude and a Codex adjudicator, neutral labels, `qa/adjudication-2026-10-15/`) settled them under the
project's conventions, two of which decided most items and are now written into the briefs:

7. a curve that runs into a frame or grid line ends where its own ink can no longer be told from that
   line (its near edge, not its centre); a sample within 2 px of the curve's last visible ink is on it;
8. a trace sample in ink the line shares with a symbol's outline is off the line.

Both readers had put many curve ends at a frame's centre; those samples were excluded (56 in these
batches), and each exclusion unpaired the other reader's neighbouring sample, which then needed its own
round. The comparison now matches a sample lying beyond the other trace's end by no more than the two
samples' x bounds with that end (commit 4cc4fd6; no change to any earlier batch's data).

Final canonical points (b9 now 85, with 74 agreed, 10 verified and one open, and b11 379, with 345
agreed, 26 verified, 5 resolved and 3 open, after the correction of `some` answers, D-039; see each
`canonical.csv`): b7 92 (80 agreed, 12 one-sided-verified), b8 101 (90, 11), b9 84 (74, 9, one
open), b10 341 (315, 26), b11 380 (349 agreed, 25 verified, 5 resolved, one open). The five resolved
points are the FC-23 samples at the PS/RS crossing (credit Claude: dash length tells the two curves
apart). With every reading bound halved, 85 of 94, 99 of 99, 87 of 87, 329 of 331 and 362 of 375
matched points still agree (`sens-*.md`).

Still split after the last round, for the human audit: FC-13 Codex's last trace sample at the triangle
it runs into (its convention-8 status turns on one pixel); FC-20 Codex's last mean sample at a circle's
outline; FC-22 Claude's first upper and last lower samples at the frame (one pixel either side of the
2 px rule). They stay in the records with status `one-sided` (read by one agent, not verified).

## Findings

1. **The computer plots do not plot their own printed fits**: the drawn lines' intercepts miss the
   printed cohesion by -58 to +96 psf on most of the fourteen plots, both readings agreeing within 6 psf,
   while the printed fits reproduce from the data sheets where the tests are identified (C-9A from
   C-1D, C-10A from C-2B, C-12 from C-4B, the last supporting the relation the index had marked
   unresolved). `insights/1968-vol2-appendix-c-computer-plots-against-printed-fits.md`.
2. **Fig. C-17** (printed C-39, PDF 153) has a heavier circle with a dot at its centre printed 64 px
   right of the frame (Dr about 1.14); both readers recorded it. Whether it is a data point is not
   settled by the page; a person should look.
3. **Fig. C-21** (printed C-43, PDF 157): the hatched band's edges are the 45 and 40 degree grid lines
   themselves, not separate lines; the band reads 45.00 and 40.00 degrees across the frame.
4. **Fig. C-9C** (printed C-27, PDF 141), the combined plot of C-9A and C-9B, carries eleven triangles
   to their ten; Claude's reader noticed (and did not use) that most sit 10 to 70 psf lower than their
   counterparts on C-9A and C-9B. To check against the data sheets.

## Records

`tools/build_batch_records.py` for each batch: the computer plots under `b68-ds-fc-8` to `b68-ds-fc-15`,
the friction-angle charts under `b68-ds-fc-16` to `-fc-22` and the six curves of C-23 under the Volume I
ids of Fig. 2-23 (`b68-ds-f2-23-<soil>`; C-23 reproduces F2-23, which has not been read yet; when it is,
it is diffed against these readings rather than read twice).
