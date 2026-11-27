# Review: Volume I inventory, the rest of Section V and Section VI (batch inventory-s6-b1)

Date 2026-11-20 (D-050, roadmap step 6f). Two blind inventories of AM-68-1 Vol. I (NASA CR-92208) from the
300 dpi page images, PDF 345 to 440 (printed 5-65 to 6-82): Figs. 5-40 to 5-47 and all of Section VI, Figs. 6-1
to 6-27. Claude (a separate Claude agent, 83 rows, notes and the script that wrote its CSV under
`extractions/claude/inventory-s6-b1/notes/`) and Codex (gpt-6.2-sol, high, in its own workspace, 83 rows,
`extractions/codex/inventory-s6-b1/`). Same brief for both (`prompt.md` in each submission, `TASK.md` here).

Hints available to each reader: the same source-only packet, namely the page images, the report's lists of
illustrations (PDF 9 to 14), the page map, the agreed figures index of the earlier sections without its notes,
and the conventions. The brief itself names the eight detail correlation drops (NASA 1 to 8) and says that
Section VI compares the model drops with the report's computer program. Neither reader saw the other's work or
any earlier batch notes. Claude's submission was written outside the repository until Codex had finished; a first
Codex run stopped at its usage limit after two minutes, before writing an inventory, and was discarded; the run
filed here started fresh in a new workspace. None of Codex's 16 shell commands names a path outside its workspace (checked in its event log).

Diff: `tools/diff_tables.py --key id`, report in `diff.md`. Result: rows appended to `corpus/1968/figures.csv` and
`.json` by `tools/build_figures.py --base qa/inventory-s3s5-b1/figures.csv` with `resolutions.csv` (58 cell
decisions) and `corrections.csv` (10 cells changed on page evidence after Codex's review: 9 the readers had agreed on, and
Fig. 6-27's trace class, descriptive text taken from the first submission). A corrected row's status is `resolved`. Sections III to V now build into `qa/inventory-s3s5-b1/figures.csv` (byte for byte the index as it
was), so no build reads its own output.

## Agreement

| | |
|---|---:|
| rows in both submissions, same ids and PDF pages | 83 |
| rows in one submission only | 0 |
| identity and unit cells (kind, pages, panels, curves, rotation, data form, test type, axes, units, scope, priority, relations) | 1,494 |
| agreed as read | 1,419 (95.0 percent) |
| agreed after the vocabulary rules | 17 |
| settled by a convention (below) | 39 |
| resolved on evidence | 17 |
| provisional (curve counts, recounted when the points are read) | 2 |
| cells corrected on page evidence (`corrections.csv`; 9 agreed, 1 descriptive) | 10 |
| descriptive text cells that differ (kept as alternates in the sidecar, not reconciled) | 288 |

Both agents found the same 35 numbered figures on the same 80 pages, with the same continuation sheets, and
the same map from drop to figure: for each of NASA Drops 1 to 8, a four-sheet figure of measured histories with
the report's computed curves at the original strut damping (Figs. 6-11, 6-13 to 6-19) and a four-sheet figure of
computed curves alone at the higher damping (Figs. 6-12, 6-20 to 6-26). They read the same four tables printed
as figures (Figs. 6-4, 6-6, 6-8, 6-10). The disagreements were about scope, curve counting and how to name a
relation, not about what is on the pages.

## The tool, not the readers

Both readers wrote the controlled unit codes themselves (`ft_s`, `in_s`, `deg_s`); the build's unit table knew
only the printed spellings, so 51 cells where the two readings agree were held as pending. The table now maps
the codes to themselves, and adds `deg_s2` for the vehicle pitch acceleration, printed "Degrees Second^2", which
no earlier batch met. Both readers read that unit on the six sheets where it is the first ordinate; Codex wrote
`n/a` because the vocabulary had no code for it and kept the unit in its notes, and the existing rule (an axis
one reader read keeps the unit read) now applies. The Section II, Sections III to V and Volume II indexes
rebuild byte for byte after the change.

## Conventions applied

1. A computed curve is `in_scope` no (the conventions of the Volume II batch): the 32 sheets of computed curves
   alone. The brief for this batch said "maybe at most" for computed curves, which conflicts with that rule;
   Codex followed the rule, Claude the brief. The brief was at fault.
2. The Section VI stability profiles (Figs. 6-5, 6-7, 6-9) are `in_scope` no: their markers repeat the measured
   outcomes first printed in Figs. 5-20, 5-40, 5-41 and Table 5-T2, the transition band is the authors' drawing,
   and the other profiles are computed (a reproduction is `in_scope` no; a computed curve is `in_scope` no).
   Claude wrote maybe, Codex yes. Priority 2 (Claude), as both readers graded Fig. 6-27: a comparison of the
   report's program with the measurements is interpretation.
3. Curves on a stability profile: each marker class present is one series, as Fig. 5-20 was counted; each edge of
   the hatched transition band is a trace (the curve-count convention: each boundary of a shaded or bracketed
   range); each computed profile, drawn as one patterned line, is a trace. Claude counted marker classes and the
   band once; Codex counted the band's two edges and no markers. A cross or bar through an open circle is a grid
   line, not a symbol (Codex's review; the first version of these notes took them for symbols). Figs. 5-40 and
   5-41 are 5 (open, filled and half-filled markers, two band edges), Fig. 5-42 is 1 (open circles only, "All Drops
   Stable"), Fig. 6-9 is 9 (where the label 77 has no clear leader to a marker; the three classes stand). Figs. 6-5 and 6-7 stay provisional (5, 9): on Fig. 6-5 the class of drops 45, 46 and 50
   cannot be told in their cluster, and on Fig. 6-7 the shared marker of drops 30 and 34, half filled on Fig. 5-40,
   is hidden under the bands.

## Where each reading was right (page checks)

Codex right, Claude wrong:

1. The computed-only sheets are `in_scope` no (convention 1, 32 cells).
2. Fig. 5-41 derives from Table 5-T2's PDF 311 and 312 (drops 63 to 77); Claude named the Section VI reprint,
   Fig. 6-8.

Claude right, Codex wrong:

1. Every history sheet of a drop links to its row of Fig. 6-10. Both readers did so on the sheets with no Section V
   counterpart; Codex left it off the six sheets of Drops 1 and 2 that also point to Section V.
2. Fig. 5-42's markers are one series (Codex 0), and the stability profiles are priority 2 (Codex 1).
3. Fig. 6-27 is `in_scope` maybe, not yes: its curves are computed minus measured depth; its printed Dmax values
   (4.3, 4.2, 4.2, 5.3, 3.4, 3.0, 3.3, 3.7 in) may be the measured maximum penetrations, but the sheet does not
   say. Claude compared them by eye with the measured curves of the panels c; not checked point by point here.

Neither exactly right: Figs. 5-40 and 6-6 (drops 22 to 34) derive from Table 5-T2's PDF 309 alone. Claude named
Fig. 6-6 and the whole table; Codex named PDF 309 and 310, but PDF 310 holds drops 36 to 53. Fig. 5-42 (drops
35 to 44) takes PDF 309 and 310; Claude named the whole table, Codex PDF 310 only (checked on PDF 309: drop 35,
type E, yaw 67.5).

## Found in Codex's review of this step (2026-11-20), and corrected

1. Figs. 6-4, 6-6 and 6-8 reprint the rows and columns of Table 5-T2 (PDF 310 and 311, 309, 311 and 312, compared
   by Codex: the same run rows and measurement columns; the reprints leave out Table 5-T2's Test Type column, and Fig.
   6-4 prints drop 49's yaw as 22.3 where the table prints 22.5). Both readers had marked them in scope, priority 1, `same-as`; the reprint rule makes them
   `reproduces`, `in_scope` no, priority 3 (`corrections.csv`; their printing slips stay in the notes).
2. Fig. 6-27's curves are computed minus measured depth (its ordinate, PDF 440), so its trace class is `computed`,
   not `recorded-trace` (the first submission's text, Claude's; `corrections.csv`). Codex also compared the eight
   Dmax values by eye with the maxima of the measured penetration curves (panels c, PDF 375 to 408) and found them
   matching; `in_scope` stays maybe until that is checked point by point.
3. The marker classes of the stability profiles (convention 3 above).
4. The Section V and Section VI printings of one channel are not the same trace. NASA Drop 1's footpad speed in Fig.
   5-22 (printed 5-47, PDF 327) is a smooth curve that falls to about 2 in/s (0.05 m/s) at 0.1 s; the measured
   trace of Fig. 6-13 panel a (printed 6-26, PDF 384) is stepped and levels off near 12 in/s (0.30 m/s) (checked on
   both pages). `same-as` on a history sheet means the same test and channel.
5. The build kept a reader's unit code (`in_s`) as the printed spelling; the column is now empty in that case, and a
   code is matched before punctuation is stripped, so a printed "Ins." can no longer become inches per second.

## Statements in the report that disagree, found by both readers

1. The repeat pairs. Printed 6-21 (PDF 379): "Drop No. 3 same as No. 1, No. 4 same as No. 2". Fig. 6-10
   (printed 6-15, PDF 373) gives Drops 2 and 3 the same velocities (VV 5, VH 7 ft/s) and Drops 1 and 4 the same
   (10, 0); the histories agree with the table. Already recorded in `qa/tables-s5-b1/review.md`.
2. Fig. 6-10 (printed 6-15, PDF 373) prints NASA Drop 5's relative density as "3" with no decimal point; Drop 6,
   on the same bed type, prints 0.3.
3. Drop 25. Fig. 6-6 (printed 6-9, PDF 367) prints VV 12, VH 5 ft/s, not stable, and so does Table 5-T2 (printed
   5-29, PDF 309, checked); Figs. 5-40 and 6-7 (printed 5-70 and 6-10, PDF 350 and 368) plot it at VH about 6 ft/s
   (about 1.83 m/s against the tables' 1.52 m/s).
4. Bed preparation. Printed 5-68 (PDF 348): "layers about four inches thick, followed by rolling 20 times (10 back
   and forth cycles)"; the drop 22 remark of Fig. 6-6 and Table 5-T2: "10 rolls per two-inch layer".
5. The third group. Printed 5-69 (PDF 349): drops 63 to 77 were made "with the same initial conditions as that of
   the first group" (45 deg yaw); Fig. 6-8 lists drop 63 at 22.5 deg yaw and drop 68 on soil not rolled, and
   neither is plotted in Fig. 5-41 or 6-9. Fig. 5-41's inset says "RS Dense Soil" under a caption that says
   RSM-b.
6. The variable list of printed 6-14 (PDF 372, continued on PDF 374) uses Z for the c.g. vertical position and its derivatives where
   every figure uses X, and its dots on the pitch angle and pitch acceleration are the other way round from the
   captions.
7. Captions that do not match their axes: Fig. 6-15 sheet 3 (PDF 394, panels i to k), Fig. 6-16 sheet 2 (PDF 397,
   e and f), Fig. 6-19 sheet 1 (PDF 408, d), the first sheets of Figs. 6-12 and 6-20 (PDF 380 and 412, a pitch
   angle captioned pitch acceleration), and Fig. 6-21 sheet 2 (PDF 417, pitch acceleration on an axis labeled
   "Inches"). Several computed panels of the drops with VH 0 print every tick as 0 or repeat a tick, so their
   scales cannot be read.
8. PDF 374 prints its folio as 6-18 where the sequence gives 6-16 (Codex adds that PDF 376, Fig. 6-11 sheet 2,
   also prints 6-18).

Codex only:

1. **The Experimental and Computer arrows may be swapped** on Fig. 6-11 panel h (PDF 376) and Fig. 6-14 panels b
   and k (PDF 388 and 390), judged from the neighboring panels. To settle before any point is read from them.
2. Printed 6-14 (PDF 372) says the comparison covers "ground reactions"; no sheet plots one. Printed 5-66 (PDF
   346) says the footpad forces were left out because of strain-gage noise.
3. Fig. 6-13 panel f (PDF 385) prints 1.5 and 1.25 where the grid gives 0.50 and 0.25.
4. Printed 5-78 (PDF 358) cites Figure 5-8 for the geometric difference between the full-scale LM and the model;
   the comparison of configurations is Fig. 5-9.

Claude only:

1. The exploratory model drops of Figs. 5-43 to 5-47 (printed 5-75 and 5-76, PDF 355 and 356) are numbered 2 to 6, the same numbers as NASA Drops 2 to 6,
   which are other tests.
2. Fig. 6-7's legend says "Dr (From DPT Tests) as Marked", but no Dr is printed on the plot.
3. The page map's OCR label is wrong on 15 pages of this range (listed in Claude's notes); the inventory uses the
   labels read on the images.

Found in this review: Fig. 5-42 prints 22.5 deg yaw for drops 35 to 44, as Key E of Table 5-T2 does, where the
table's rows print 67.5 (finding 5 of `qa/inventory-s3s5-b1/review.md`).

## For the extraction (not settled here)

1. Section VI holds the only measured histories of NASA Drops 3 to 8. For Drops 1 and 2 both sections print the
   same channels, but not the same traces (item 4 of Codex's review above): which printing a record takes, or
   both, is decided when they are read.
2. A history panel is identified by its axis and unit, not its caption (item 7 above), and its curve by its arrow
   only after the possible swaps (Codex item 1) are settled.
3. The computed curves are the report's own program at two strut dampings; they are not measurements and stay out
   of `data/`.

## Suggested audit sample (a request; not an audit until recorded in `qa/audits.csv`)

1. Fig. 5-40 (PDF 350): the five curves and the position of drop 25.
2. Fig. 6-10 (PDF 373): the drop to Bendix map and Drop 5's Dr.
3. Fig. 6-11 sheet 2 (PDF 376) and Fig. 6-14 sheets 1 and 3 (PDF 388, 390): the arrow assignments.
4. Fig. 6-15 sheet 3 (PDF 394): which quantity each panel plots.
5. Fig. 6-27 (PDF 440): the Dmax values against the maxima of the measured penetration curves.
