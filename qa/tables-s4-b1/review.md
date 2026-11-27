# Review of batch tables-s4-b1: subscale drag runs on Soil No. 1 (Fig. 4-6a, D-050 roadmap step 6e)

Fig. 4-6a (Volume I, printed 4-8, PDF 193, printed sideways), "Subscale Drag Test Results - Soil No. 1 - RS Loose":
32 runs (1-1 to 1-33; 1-9 is not printed) of the 6 in footpad dragged at constant depth through loose RS, 14 columns:
run number, D, d, V_H, the bed's mean dynamic penetrometer reading g_p, D_r, gamma, the drag and vertical loads F_D and
F_V, four derived columns (F_D/(d gamma A_ft), V_H/sqrt(dg), F_D/A_ft, F_V/A_pt) and the pitch angle alpha.

## Transcriptions

Both agents, blind, from the same brief (`TASK.md`) and pages (PDF 191 to 193), 2026-11-19: Claude (one subagent,
two passes with different crop groupings) and Codex (gpt-6.2-sol high, 241 s). Compared by
`tools/diff_tables.py --key run_number` (`diff.md`): **all 416 data cells agree exactly** (32 runs by 13 columns);
the 24 differences are the free-text notes, in which both readers flag the same damaged digits (run 1-21 gamma,
1-22 alpha, 1-33 F_D/A_ft, among others) and read them the same. Nothing to adjudicate; `agreed.csv` holds the table.

Both readers report the definitions: A_ft is the "Total Horizontal Frontal Area" and A_pt the "Vertical Frontal Area"
of the footpad, labels of Fig. 4-4 (printed 4-6, PDF 191), with no formula; g in V_H/sqrt(dg) and the units of the
derived columns are not printed.

## Arithmetic check of the derived columns

`tools/check_drag_table.py` (`arithmetic.md`, `arithmetic-checks.csv`, `arithmetic.json`). It shows the printed columns
consistent with each other or not; it does not show a transcription right. Conventions: a printed number carries half
a unit of its last digit; D and d are nominal set points, taken as exact; F_D/A_ft and F_V/A_pt are in psi, inferred
(no unit is printed).

1. V_H/sqrt(dg), recomputed with d in feet and standard gravity: four rows (1-10, 1-13, 1-23, 1-25) are outside the
   rounding of the one printed decimal by up to 0.1, as truncation or a slip would make; the rest agree.
2. F_D/A_ft against F_D/(d gamma A_ft) times d gamma: printed over computed is 0.972 to 0.979, never 1. Each row
   admits an interval of factors within the printed rounding, and the 32 intervals intersect (0.97377 to 0.97635):
   every row fits one common factor. That is the factor a unit weight of 40.02 to 40.13 pcf, rather than the printed
   41.1, would give in the authors' arithmetic; which input differs, the page cannot say. Both readers found the
   factor independently. (A first version of the check compared rounded values and named run 1-27; Codex's review
   showed the exact intervals intersect.)
3. The areas each row implies (A_ft = F_D / (F_D/A_ft), A_pt = F_V / (F_V/A_pt)) are heuristic flags only: they also
   depend on the pad's pitch (Fig. 4-4), which the check does not model. Grouped by pad diameter (and depth for A_ft),
   a row is flagged when its whole interval lies more than 15 percent from its group's median: A_ft of runs 1-4, 1-23
   and 1-29; A_pt of run 1-28 (57.4 in^2, twice the table's 27.4) and runs 1-29 to 1-31 (21.7 to 22.7 in^2). Both
   readers read those cells the same, cleanly.

## Record

`tools/build_run_table.py tables-s4-b1 --experiment b68-drag-f4-6a --figure F4-6a`: `data/experiments/b68-drag-f4-6a/`
`runs.csv` (32 runs, status `agreed`, every printed value in SI and as printed, the derived columns as printed, and a
`check` note on the 9 runs the arithmetic check names) and `runs.json`. The index row comes from batch
`experiments-drag-b1`. The other twelve drag tables (Figs. 4-6b to 4-16, 240 runs) are indexed and not yet transcribed.
