# Review: Volume I inventory, Sections III, IV (to Fig. 4-22) and V (to Fig. 5-39) (batch inventory-s3s5-b1)

Date 2026-11-19 (D-050, roadmap step 6a). Two blind inventories of AM-68-1 Vol. I (NASA CR-92208) from the
300 dpi page images, PDF 142 to 212 and 281 to 340 as briefed; both readings went on to PDF 344 to finish
the NASA Test 2 histories (Figs. 5-36 to 5-39). Claude (a separate Claude agent, 101 rows, notes under
`extractions/claude/inventory-s3s5-b1/notes/`) and Codex (gpt-6.2-sol, high, read-only, 102 rows,
`extractions/codex/inventory-s3s5-b1/`). Same brief for both (`prompt.md` in each submission); neither saw the
other's work; Claude's submission was written outside the repository until Codex had finished. Diff:
`tools/diff_tables.py --key id` after the page-qualified aliases (`id-aliases.json`), report in `diff.md`.
Result: rows appended to `corpus/1968/figures.csv` and `.json` by `tools/build_figures.py --base
qa/inventory-s2-b1/figures.csv` with `resolutions.csv` (72 cell decisions) and `row-decisions.csv` (1 row).

## Agreement

| | |
|---|---:|
| rows in both submissions (after aliases) | 101 |
| rows in Codex only (second frame of the Fig. 5-2 foldout, PDF 285) | 1 |
| identity and unit cells (kind, pages, panels, curves, rotation, data form, test type, axes, units, scope, priority, relations) | 1,836 |
| agreed as read | 1,683 (91.7 percent) |
| agreed after the vocabulary rules (unit spellings, test type) | 65 |
| settled by a convention or a rule (below) | 57 |
| resolved on evidence | 13 |
| provisional | 2 |
| from the one-sided row | 16 |
| descriptive text cells that differ (kept as alternates in the sidecar, not reconciled) | 338 |

Both agents found the same items with the same ids, pages and rotations, including the five printed pages of
Table 5-T2 (PDF 308 to 312) and the three parts of Fig. 4-6 (Soil No. 1, PDF 193 to 195). The disagreements
were about conventions, scope and priority, not about what is on the pages.

## Conventions and rules applied

1. A drawing or flow chart with no plotted data has 0 panels (31 cells; Codex counted drawing frames).
2. A load cell calibration or cross-talk plot (Figs. 3-8, 3-9, 3-16 to 3-18, 3-24, 3-25) is in scope `maybe`:
   numbers about the instrument, not a test result.
3. A bar chart counts one curve per bar series (Figs. 4-3, 4-18; new in this batch).
4. Priority follows the brief's rule: run parameters and footpad sizes are 1 (Figs. 3-26, 4-2, 4-17, 5-10),
   measured results are 1 (Fig. 4-20), program counts and the full-scale drag facility design are 3.
5. A printed item continued over several scanned pages gets one row per page, the first keeping the printed
   id, the others `-pNNN` (T5-2-p309 to -p312, F5-2-p285); page-qualified aliases (`<id>@<pdf_page>`) map
   Codex's repeated `T5-2` ids.

## Where each agent was right (page checks)

Codex right, Claude wrong:

1. Figs. 5-25 and 5-32 are `mixed`, not `curve`: an inset prints the touchdown velocities and the surface
   (checked by Claude on PDF 330: V_v = -114.93 in/s, V_h = 0, RS Loose, level surface). Figs. 4-5 and 5-10 also
   carry printed values (channel sensitivities; full-scale values in parentheses).
2. The Fig. 5-2 foldout is two scanned frames, PDF 284 and 285; the label 5-5 is printed on the second only.

Claude right, Codex silent:

1. **Fig. 4-19's time axis has a label slip**: ticks printed 0 to 100, then 120, 130, 140 at the same spacing,
   no 110 (AM-68-1 Vol. I, Fig. 4-19, printed 4-23, PDF 208; confirmed by Claude on the page). It must be
   settled before anyone reads points: either the last three labels are misprinted (the grid runs to 130), or
   the spacing changes. Fig. 4-20 plots the same three runs against displacement and can arbitrate.
2. Fig. 5-39's angle axis prints 0, .5, 1.0, 2.0, 2.5 (no 1.5), the same kind of slip.
3. Fig. 5-20's markers are three series plus the author's boundary (4 curves; Codex 1).

Both noted: the captions of Figs. 3-16 and 3-17 appear swapped with their plots.

## Findings the readings raise (for the extraction, not settled here)

1. Fig. 4-19's legend gives the "dense" impact bed Dr 0.65; the RS dense drag table (Fig. 4-9) has Dr 0.80.
2. Fig. 5-32's inset prints V_h = 83.75 in/s; Table 5-T3 gives 83.5.
3. Fig. 4-5's record header says 15 fps; the text says 14 ft/s and the table prints 14.20 for run 2-20.
4. In the LSM dense drag table (Fig. 4-16) Dr changes from 0.81 to 0.70 while the unit weight stays 82.0 pcf.
5. Key E of Table 5-T2 says 22 1/2 deg yaw; its rows print 67.5.
6. In the Soil No. 1 drag tables (Figs. 4-6b, 4-6c) the unit weight at Dr 0 rises from 41.1 to 58.3 pcf over
   the runs; it may be the soil degrading with reuse. `mcc_relevant` maybe until checked against Fig. 2-60.
7. Counts: the drag tables print 272 constant-penetration runs over 11 soils (Soil No. 1: 67) against 363 tests
   in the text; force histories exist for RS soil only (runs 4, 10, 12 against time; runs 4, 10, 12, 15, 16,
   II-1 and full-scale Test 16 against displacement); Table 5-T2 lists 81 model drops, of which only NASA Tests 1
   and 2 (Bendix drops 10 and 11) have histories in these pages.
8. Not printed in these pages: the model's footpad diameter and mass as labeled values, the impact mass of runs
   10 and 12, the gravity of the tests (terrestrial is inferred from the rigs, not stated), the recorders'
   readout intervals except the 1/1000 s digitizing of the model-drop tapes.

The setup of each family, with page citations, is in both submissions (`notes/setup-and-counts.md`, and the
"Setup" section of Codex's `codex-answer.md`); the experiment rows of the slice are built from them in the
next step.
