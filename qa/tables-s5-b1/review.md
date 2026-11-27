# Review of batch tables-s5-b1: the detail correlation drops of the LM model (Table 5-T3, D-050 roadmap step 6f)

Table 5-T3 (Volume I, printed 5-45, PDF 325, printed sideways), "Detail Correlation Drops": the eight drops of the
1/6-scale LM model chosen for the detailed correlation (NASA Tests No. 1 to 8, Bendix drops 10, 11, 12, 13, 16, 17, 20
and 21), nine columns: NASA Test No., Bendix Drop No., V_v and V_h (In./Sec.), tau (Sec.), Soil, D_r, gamma
(Lb./Ft.^3) and phi (Deg.). This pass answers the data part of open question 22: the friction angle of each bed and
the table's velocities were in the notes of batch curves-s5-b1 only.

## Transcriptions

Both agents, blind, from the same brief (`TASK.md`), 2026-11-20: Claude (a separate agent, every cell read twice with
crops grouped differently) and Codex (gpt-6.2-sol high, 268 s). Each worked in its own folder outside the repository
from the same source-only packet: the page images of Section V (PDF 280 to 344) and of Table 2-3 (PDF 41), a page map
of Section V (figure ids and titles only), the experiment index without its notes columns and without the two model
drop rows, and the index conventions. The brief named the records `b68-mdrop-10` and `b68-mdrop-11` (their ids only,
for the relation column). Neither reader saw an earlier step's notes; Codex's event log shows no access outside its
folder.

Compared by `tools/diff_tables.py --key nasa_test_no` (`diff.md`): **all 72 printed cells agree exactly** (8 drops by
9 columns: the 8 NASA test numbers, the key, and 64 values). The 7 differences are the free-text notes, in which both readers flag the same damaged glyphs (the broken
4s of gamma and phi in rows 1 to 4, the split middle 1 of row 6's -117.1, a broken letter of row 3's RS) and read them
the same. Nothing to adjudicate; `agreed.csv` holds the table.

## What the page and the text say (both readings agree)

1. The legend: V_v vertical velocity, V_h horizontal velocity, tau the "Time interval between model release to
   touchdown", D_r soil relative density, gamma "Soil density" (in Lb./Ft.^3), phi internal angle of friction.
2. "The velocities shown in Table 5-T3 were calculated based on the exact time interval between the instant of model
   release to the instant of ground contact. This time interval could be measured very precisely from the readings of
   the accelerometer in the x direction" (printed 5-44, PDF 324). At release a pulse was injected into the output of
   the CG accelerometer in the X direction (printed 5-39, PDF 319). No formula is printed.
3. Two nominal conditions: a pure vertical drop at a nominal "teen" (ten) feet per second for NASA Tests No. 1, 4, 6
   and 8, and five feet per second vertical with seven horizontal for the others; zero angular rates, zero pitch and
   roll, 45-degree yaw (2-2 landings) (printed 5-44, PDF 324), on a level landing surface (printed 5-43, PDF 323). The
   table agrees: V_h is 0 for those four.
4. The beds: placed by the spreader in layers of about four inches; the RS and SS loose beds needed nothing more; the
   RS intermediate beds were rolled after each pass "until the desired soil depth (18 inches thick) was achieved". A
   new bed was prepared for every drop; dynamic penetrometer readings were taken after each drop, away from the
   footpads, and the text points to Section II for the methods and to Paragraph 2.7.1 for the correlation of D_r with
   those readings (printed 5-43 and 5-44, PDF 323 and 324). How gamma and phi were obtained for each bed is not said.
5. Test No. 4 duplicates Test No. 1 and Test No. 3 duplicates Test No. 2; Tests No. 5 and 6 repeat the two conditions
   on RS intermediate soil and 7 and 8 on SS loose (printed 5-46, PDF 326). Section V prints time histories for Tests
   No. 1 and 2 only (Figs. 5-22 to 5-39). Codex's notes add that Bendix drops 14, 15, 18 and 19 are repeats lost to bad
   recordings or a bad release (Table 5-T2, printed 5-28 and 5-29, PDF 308 and 309).

## Section VI: the measured histories of all eight drops (after Codex's review)

The readers' packet held Section V only, and both said, correctly for Section V, that it prints histories for Tests
No. 1 and 2 only. Codex's review of this step found that Section VI plots the measured histories of all eight drops
against the report's computer simulation, and the first version of the records and pages wrongly said the report
prints none for Tests No. 3 to 8. Checked on the captions of PDF 375 to 411 and on the sheets of Figs. 6-11, 6-13 and
6-14 (curves labeled Experimental and Computer): "Detail Correlation Results" for LM Model Drop No. 2 (Fig. 6-11,
printed 6-17 to 6-20, PDF 375 to 378), No. 1 (Fig. 6-13, printed 6-26 to 6-29, PDF 384 to 387) and Nos. 3 to 8 (Figs.
6-14 to 6-19, printed 6-30 to 6-53, PDF 388 to 411), four sheets each (footpad velocity, angle and penetration,
vehicle pitch and center of gravity motion); Fig. 6-12 (PDF 380 to 383) gives computer results only, for No. 2 with
high strut damping. Fig. 6-10 (printed 6-15, PDF 373) lists the eight drops again with their conditions. Section VI
is not yet in the figures index; the records now say the histories of Tests No. 3 to 8 are not yet extracted and
where the report plots them. Section VI's prose swaps the repeat pairs: "Drop No. 3 same as No. 1, No. 4 same as No.
2" (printed 6-21, PDF 379), where Section V (printed 5-46, PDF 326), Table 5-T3 and Fig. 6-10 make No. 3 the repeat
of No. 2 and No. 4 the repeat of No. 1 (their velocities and beds agree). The records follow the tables.

## Printed differently in two places (both readings, and Fig. 6-10)

1. Fig. 5-25's inset (PDF 330) prints V_v -114.93 in./sec. for Test No. 1; the table, -114.9.
2. Fig. 5-32's inset (PDF 337, a degraded scan) prints V_v -60.55 and V_h 83.75 in./sec. for Test No. 2; the table,
   -60.5 and 83.5. Claude reads the leading digits of the inset as broken (-?0.55, ?3.75); Codex reads them as
   distinguishable. 83.75 does not round to 83.5, so the inset is not the table's value to more digits.
3. Table 5-T2 prints the nominal velocities (10 and 0, or 5 and 7, no unit) and D_r "0.3" where Table 5-T3 prints ".3".
4. The beds differ from the soils of Table 2-3 (PDF 41): RS loose at D_r 0 is 46.9 and 47.1 pcf with phi 41 here,
   41.4 pcf and 40 deg for soil No. 1; RS intermediate is D_r .3, 53.0 pcf and 42.5 deg here, D_r .45, 45.9 pcf and
   44.5 deg for soil No. 3; SS loose is 96.0 pcf and 30 deg here, 94.7 pcf and 29 deg for soil No. 7. Recorded as
   printed; the report does not explain the differences.
5. Fig. 6-10 (printed 6-15, PDF 373, a third printing of the eight drops, seen by Claude in this review) prints D_r
   "3" for NASA drop 5 and "0.3" for drop 6, the nominal velocities in fps, and gamma as "Absolute Density Lb./Ft.^3";
   its other values match Table 5-T3.

## Arithmetic check

`tools/check_mdrop_table.py` (`arithmetic.md`, `arithmetic-checks.csv`, `arithmetic.json`), our arithmetic, not the
report's. All four vertical drops are consistent with |V_v| = g tau (g standard gravity, the speed of a free fall
from rest over tau) within the rounding of both printed numbers. Of the four drops with a horizontal velocity only
NASA Test No. 3 is, at the edge of the rounding (60.0 against 60.04 to 60.42 in./sec.); Tests No. 2, 5 and 7 are
inconsistent with that equation (g tau 68.34, 56.37 and 59.46 in./sec. against 60.5, 60.8 and 60.0). This shows
consistency, not the authors' method: the report says the velocities were calculated using the measured interval and
prints no formula. Claude's reader made this check first; it is now a tool. The verdicts (`consistent`, `differs`)
do not mark a run in `runs.csv` `check`: the report does not claim the equation.

Afterwards (2026-11-20, Codex's review of the site): the report does give g for Earth, 32.2 ft/s^2, in its glossary
(AM-68-1 Vol. I, printed 2-2, PDF 27; checked on the page). With that value (386.4 in./sec.^2 against standard
gravity's 386.0886) the verdicts change: three of the four vertical drops are consistent (Test No. 1 misses by 0.004
in./sec.: 114.9 plus its half unit, 114.95, against an interval starting at 114.954) and none of the four with a
horizontal velocity (Test No. 3 falls just outside, 60.0 against 60.09 to 60.47). The two values of g differ by 0.08
percent, about the rounding of a printed tau, so this check cannot tell them apart and its verdicts depend on the g
used. The tool now reports both, the report's g first, and the record pages say so.

## Records

`tools/build_run_table.py tables-s5-b1 --family mdrop --soil-family RS --experiment b68-mdrop-t5-3-rs --figure T5-3`
and the same with `SS` and `b68-mdrop-t5-3-ss`: 6 and 2 drops, status `agreed`, every printed value in SI and as
printed. `same_test_as` links NASA Tests No. 1 and 2 to `b68-mdrop-10` and `b68-mdrop-11`, whose record pages now give
the table's velocities, tau and friction angle where they read "not yet extracted". One record per soil family because
the index and the site group records by soil family and the table mixes RS and SS beds. The index rows come from batch
`experiments-t5-3-b1`, read in the same blind pass (`qa/experiments-t5-3-b1/review.md`).

## Credit

Both readings were right on every value. Claude's reading gave the fuller setup (the 18 inch RS intermediate beds, the
instrumented No. 1 pad) and the g tau arithmetic; Codex's gave the four repeated drops and full quotations of the
bed preparation. Codex's review of the step found the Section VI histories, the free-fall wording, the one-reader
descriptive cells of the index rows and the contradictory fill depth on the RS page; all fixed before the commit.
