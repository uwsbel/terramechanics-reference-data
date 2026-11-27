# Task: experiment index rows for the subscale drag test tables of the 1968 Bendix LM Soil Mechanics Study (blind)

You are one of two independent readers (the other works blind elsewhere); the two tables are diffed mechanically and
every disagreement is settled from the page, with credit to whichever reading was right. Be precise and say what you
could not determine. US English. No em-dashes or en-dashes. Do not edit anything in the repository.

## Evidence (source only)

- The page images `corpus/1968/images/pNNNN.png`, 300 dpi, of AM-68-1 Vol. I (NASA CR-92208): Section III (test
  equipment, the subscale drag facility) PDF 142 to 185, Section IV (the drag test program and its tables) PDF 186 to
  205. The PDF is `nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf` if you need a page outside these.
- The agreed figures index rows of these sections WITHOUT the agents' notes, in
  `<local path>`.
  Use this file, not `corpus/1968/figures.csv`, whose notes columns hold an earlier step's notes.
- The existing experiment index `data/experiments/index.csv` (its conventions; the drag tables have no rows yet).
- Conventions: `docs/DATA-ORGANIZATION.md` ("Experiments": the index, its kinds and test types).

Do NOT open anything under `extractions/`, `qa/` or `.agent-related/`, and do not look for the other reader's table.

## Scope

Every table of subscale constant-penetration drag test results in Section IV (Figures 4-6a to 4-16, "Subscale Drag
Test Results - Soil No. ..."): **one row per printed table page** (Figs. 4-6a, 4-6b and 4-6c are three pages of Soil
No. 1 and are three rows). Each table lists separate runs (one physical test per printed row); the runs themselves are
transcribed in a later step, not here. Nothing else (the impact runs and model drops already have rows).

## What to produce

One CSV table in the `data/experiments/index.csv` style, columns in this order:

```
experiment_id,source_id,kind,test_type,test_label_printed,soil_family,soil_no,soil_no_status,state_printed,dr_printed,unit_weight_printed_pcf,gp_printed_g,apparatus,penetrator_printed,bin_printed_in,loading,rate_printed,start_depth_printed_in,measured_channels,evidence,setup_status,mcc_relevant,priority,relation,relation_target,notes
```

Rules:

1. `experiment_id`: `b68-drag-<figure id lower case>` (`b68-drag-f4-6a`, `b68-drag-f4-16`).
2. `source_id`: `bendix-1968-vol1`. `kind`: `run-table` (a new kind for this batch: a printed table of separate runs of
   one test type, one physical test per row). `test_type`: `drag`.
3. `test_label_printed`: the caption as printed after the figure number ("Subscale Drag Test Results - Soil No. 1 -
   RS Loose").
4. `soil_family` (`RS | PS | RSM | RC2 | SS | LSM`), `soil_no` as the caption prints it, `soil_no_status` `reported`
   when the caption prints it.
5. `state_printed`, `dr_printed`, `unit_weight_printed_pcf`, `gp_printed_g`: as printed in the caption or, when the
   value is the same in every run of the table, in the table (say so in `notes`); a range when the runs differ
   ("12.0 to 13.8"), empty when not printed.
6. `apparatus` (the rig, as Section III names it), `penetrator_printed` (the footpad as printed: the D column and any
   description of the footpad), `bin_printed_in` (the drag bed's dimensions as printed in Section III, with their
   unit as printed), `loading` (constant penetration drag: how depth and velocity were held), `rate_printed` (the range
   of V_H printed in the table, with its unit), `start_depth_printed_in` (empty unless printed).
7. `measured_channels`: in words (`drag load F_D; vertical load F_V; footpad pitch angle alpha; derived F_D/(d gamma
   A_ft), V_H/sqrt(dg), F_D/A_ft, F_V/A_pt as printed`), adjusted to the table's own columns.
8. `evidence`: figure ids separated by `;` (the table, Fig. 4-4, Fig. 4-5 if relevant, the Section III figures of the
   rig), plus `text <printed page> (PDF <n>)` where the text adds a setup fact.
9. `setup_status`: `complete` only if the runs' setup is printed fully enough to reproduce them (bed and its density,
   footpad geometry, depth, velocity, gravity); otherwise `setup_incomplete`, and say in `notes` what is missing.
10. `mcc_relevant`: `no` unless the runs reload a bed already loaded (say so if the text says beds were reused).
11. `priority`: 1. `relation`, `relation_target`: `same-as` or `derived-from` with ids when a table repeats or is
    computed from another; empty otherwise.
12. `notes`: short; the number of runs, run numbers skipped, anything printed differently in two places.

Quote every field that contains a comma. Put the table in a fenced ```csv block in your final answer (and, when your
task names an output file outside the repository, write it there too), followed by a short section "Setup": where
each setup fact is printed (cite as `AM-68-1 Vol. I, Fig. 4-6a, printed 4-8, PDF 193`) and what a simulator user
would still have to assume.
