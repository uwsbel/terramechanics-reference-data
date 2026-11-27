# Review: experiment index rows for Table 5-T3, the detail correlation drops (batch experiments-t5-3-b1)

Date 2026-11-20 (D-050, roadmap step 6f). Two blind readings made in the same pass as the table's cells (batch
`tables-s5-b1`, whose `TASK.md` is this batch's `prompt.md`, Part 2), from the same source-only packet: Claude (a
separate agent) and Codex (gpt-6.2-sol high). One row per soil family of the table's beds, kind `run-table`:
`b68-mdrop-t5-3-rs` (NASA Tests No. 1 to 6, RS loose and intermediate) and `b68-mdrop-t5-3-ss` (Tests No. 7 and 8, SS
loose). Built into `data/experiments/index.csv` by `tools/build_experiments.py` as the sixth stacked batch.

## Result

Both readings made the same two rows with the same ids and agreed on every identity and number cell: kind, test type,
label, soil family, soil number (empty and `unknown` for the RS row, whose drops are on two states; 7, `inferred`, for
SS loose), printed state, D_r and unit-weight ranges, velocity ranges, setup status, priority, and the relation
`same-as` `b68-mdrop-10;b68-mdrop-11` on the RS row. The 14 differing cells are text (`diff-report.md`): apparatus,
footpads, bed, loading, channels, evidence and notes, where Claude's reading is fuller and the substance is the same.

Ten cells are resolved (`resolutions.csv`), every value checked on the pages cited:

1. The bed, both rows. Both readings give the 18 by 12 ft bed (printed 5-22, PDF 302). Claude's "18 by 12 by 5 ft" is
   not kept as the dimension: the text says the bed has "a maximum below ground depth of five feet" and that "the
   depth of soil used was adjusted to suit the varying test conditions", so five feet is the pit, not the bed. The RS
   row adds the 18 in RS intermediate beds (printed 5-44, PDF 324), checked on the page; the loose beds' depth is not
   printed.
2. The footpads, both rows: merged, in the wording resolved for `b68-mdrop-10` and `b68-mdrop-11` (batch
   `experiments-s3s5-b1`) plus "round" (printed 5-33, PDF 313).
3. Apparatus, loading and channels, both rows (after Codex's review). The builder takes these descriptive columns from
   the first reading and lists the other as an alternate, so a fact only Claude's reading stated (a sensor count, for
   one) would have entered the index unchecked. Each is now a resolution in the wording both readings support,
   checked on printed 5-22, 5-43 and 5-44 (PDF 302, 323, 324) and Fig. 6-10 (printed 6-15, PDF 373): the model and
   rig; the free landing, model weight, attitude, level surface and nominal velocities (in fps, the unit Fig. 6-10
   prints); the table's contents, with the velocities "calculated using the measured interval" rather than "from
   tau". The channels also say where the report plots the measured histories: Section V for Tests No. 1 and 2,
   Section VI for all eight against its simulation (Figs. 6-11, 6-13 to 6-19, PDF 375 to 411), which the readers'
   Section V packet did not hold (`qa/tables-s5-b1/review.md`). `tools/build_experiments.py` now lets a resolution
   replace the one-reader default of a descriptive column; no existing row has such a resolution, and none changed.

## A fault in the builder, found and fixed here

An agreed cell is stored in its normalized form, and the rate normalizer kept only the text before the first ";" (it
was written for the static tests' rates in in/min). Both rows' "V_v ... In./Sec.; V_h ... In./Sec." lost their V_h
half. `norm_rate` now truncates only an in/min rate and writes In./Sec. as in/s, the unit the site converts. Rebuilt
from all six batches, no existing row of the index changed. D_r is stored as "0 to 0.3" (the normalizer's leading
zero; printed ".3").

## What the setup lacks (both readings)

1. The depth of the loose beds (RS and SS); only the RS intermediate beds' 18 in is printed.
2. The footpads' diameter and mass (not printed in Section V).
3. The test gravity (Earth is implied; the text does not state it).
4. The release height, translational velocity and rig settings of each drop (the release attitude and angular
   rates are printed), and how the velocities of the drops with a horizontal component were calculated using tau
   (`qa/tables-s5-b1/arithmetic.md`).

No person has reviewed these rows yet: `qa/audits.csv` has no row for either batch, so agreement here is between the
two agents.
