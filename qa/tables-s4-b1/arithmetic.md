# Arithmetic check of the derived columns

Table: `qa/tables-s4-b1/agreed.csv`; 32 runs.

F_D/A_ft against F_D/(d gamma A_ft) x d gamma (psi, inferred): printed over computed ranges from 0.9722 to 0.9793. Every row admits a common factor of 0.97377 to 0.97635 within the printed rounding (the rows' intervals intersect): the printed columns are consistent with each other if the derived column used a unit weight of 40.022 to 40.128 pcf instead of the printed 41.1. Which input differs, the page does not say.

Rows outside the printed rounding:

| run | check | computed | printed | tolerance or factor interval | verdict |
|---|---|---|---|---|---|
| 1-10 | VH/sqrt(dg) | 3.2979 | 3.2 | 0.0531 | off |
| 1-13 | VH/sqrt(dg) | 2.3535 | 2.3 | 0.0522 | off |
| 1-23 | VH/sqrt(dg) | 11.0724 | 11.0 | 0.0543 | off |
| 1-25 | VH/sqrt(dg) | 6.0436 | 6.1 | 0.0525 | off |

## Areas implied by each row (square inches), heuristic flags

Grouped by pad diameter, and by depth for A_ft (three rows or more). A row is flagged when its whole interval lies more than 15 percent from its group's median. The areas also depend on the pad's pitch, which is not modeled: a flag is a place to look, not an error.

| group | rows | median | min | max | flagged |
|---|---|---|---|---|---|
| implied A_ft (D 6, d 0.5 in) | 7 | 12.16 | 11.07 | 16.20 | 1-23, 1-29 |
| implied A_ft (D 6, d 1 in) | 5 | 15.18 | 12.16 | 15.59 | 1-4 |
| implied A_ft (D 6, d 1.5 in) | 6 | 15.20 | 13.54 | 16.35 | none |
| implied A_ft (D 6, d 2 in) | 5 | 14.78 | 13.87 | 15.79 | none |
| implied A_ft (D 6, d 3 in) | 4 | 15.65 | 14.78 | 16.08 | none |
| implied A_pt (D 6, all depths) | 32 | 27.39 | 21.65 | 57.38 | 1-28, 1-29, 1-30, 1-31 |
