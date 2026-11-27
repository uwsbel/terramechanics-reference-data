# Task: experiment index rows for the footpad impact runs and two LM model drops of the 1968 Bendix LM Soil Mechanics Study (blind)

You are one of two independent readers (the other works blind elsewhere); the two tables are diffed mechanically
and every disagreement is settled from the page, with credit to whichever reading was right. Be precise and say
what you could not determine. US English. No em-dashes or en-dashes. Do not edit anything in the repository.

## Evidence (source only)

- The page images `corpus/1968/images/pNNNN.png`, 300 dpi, of AM-68-1 Vol. I (NASA CR-92208): Section III
  (test equipment) PDF 142 to 185, Section IV PDF 186 to 212, Section V PDF 280 to 344. The PDF is
  `nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf` if you need a page outside these.
- The agreed figures index rows of these sections WITHOUT the agents' notes, in
  `<local path>`.
  Use this file, not `corpus/1968/figures.csv`, whose notes columns hold an earlier step's notes.
- The existing experiment index `data/experiments/index.csv` (for its conventions and for relations: the drop
  penetrometer records `b68-dpt-*` of Section II).
- Conventions: `docs/DATA-ORGANIZATION.md` ("Experiments": the index, its kinds and test types; "Figures index").

Do NOT open anything under `extractions/`, `qa/` or `.agent-related/`, and do not look for the other reader's table.

## Scope

1. **Footpad impact (Section IV):** every distinct run that has a measured history plotted in Figs. 4-19 to 4-22
   (force or displacement against time, or force against displacement), subscale and full scale. One row per
   physical run; a run plotted in several figures is one row with all of them in `evidence`.
2. **1/6-scale LM model drops (Section V):** the two drops with measured histories in Figs. 5-22 to 5-39, NASA
   Test No. 1 and NASA Test No. 2, one row each, with their row of Table 5-T2, Table 5-T3 and the histories in
   `evidence`.

Nothing else (the drag tables, the other model drops and the rigid-surface drops come later).

## What to produce

One CSV table in the `data/experiments/index.csv` style, columns in this order:

```
experiment_id,source_id,kind,test_type,test_label_printed,soil_family,soil_no,soil_no_status,state_printed,dr_printed,unit_weight_printed_pcf,gp_printed_g,apparatus,penetrator_printed,bin_printed_in,loading,rate_printed,start_depth_printed_in,measured_channels,evidence,setup_status,mcc_relevant,priority,relation,relation_target,notes
```

Rules:

1. `experiment_id`: impact runs `b68-imp-<run label>` with the subscale run number as printed (`b68-imp-4`,
   `b68-imp-ii-1` for a label "II-1"), full-scale tests `b68-imp-fs<number>` (`b68-imp-fs16`); model drops
   `b68-mdrop-<Bendix drop number>` (the number in Table 5-T2's first column; say in `notes` which NASA test it
   is). Lower case, hyphens only.
2. `source_id`: `bendix-1968-vol1`. `kind`: `single` for each of these.
3. `test_type`: `imp` (footpad impact) or `mdrop` (1/6-scale model drop; a new value for this batch).
4. `test_label_printed`: the legend or table label as printed (`Run No. 4`, `NASA Test No. 1`).
5. `soil_family` (`RS | PS | RSM | RC2 | SS | LSM`), `soil_no` when the report names it, `soil_no_status`
   (`reported | inferred | conflict | unknown`; `inferred` when you map a printed state to a soil number yourself).
6. `state_printed`, `dr_printed`, `unit_weight_printed_pcf`, `gp_printed_g`: exactly as printed for that run,
   empty when not printed, never inferred. When two places print different values for the same run, put the one
   beside the history in the column and both in `notes`.
7. `apparatus` (which rig), `penetrator_printed` (footpad diameter and kind as printed), `bin_printed_in` (soil bed
   or pit dimensions as printed, in the printed units), `loading` (vertical or oblique, path angle, moving weight
   as printed), `rate_printed` (impact or touchdown velocity as printed, with its unit), `start_depth_printed_in`
   (empty unless printed).
8. `measured_channels`: in words, one per plotted history (`vertical force vs time; displacement vs time;
   vertical force vs displacement`; for the model drops list the plotted histories).
9. `evidence`: figure and table ids separated by `;` (ids of the figures index, for example `F4-19;F4-20`,
   `T5-2;T5-3;F5-24`), plus `text <printed page> (PDF <n>)` where the text adds a setup fact for that run.
10. `setup_status`: `complete` only if the run's setup is printed fully enough to reproduce it (bed and its
    density, footpad, mass, velocity and angle, gravity); otherwise `setup_incomplete`, and say in `notes` what
    is missing.
11. `mcc_relevant`: `no` unless the run reloads a bed already loaded (say so).
12. `priority`: 1 for these rows.
13. `relation`, `relation_target`: `same-as` or `derived-from` with experiment ids when a row is the same test as,
    or computed from, another row or an existing index row; empty otherwise.
14. `notes`: short; moving weight, velocities, numbers printed differently in two places, anything you could
    not read or find.

Quote every field that contains a comma. Numbers exactly as printed. Put the table in a fenced ```csv block in
your final answer (and, when your task names an output file outside the repository, write it there too),
followed by a short section "Setup" per row group: where each setup fact is printed (cite as `AM-68-1 Vol. I,
Fig. 4-19, printed 4-23, PDF 208`) and what a simulator user would still have to assume.
