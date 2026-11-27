# Blind transcription of a printed table: Table 5-T3 of a 1968 NASA report (batch tables-s5-b1)

You are one of two independent readers of a printed table from a 1968 NASA report (Bendix AM-68-1 Vol. I, Lunar
Module soil mechanics study, NASA CR-92208). The other reader works elsewhere; do not look for or use any other
reading. Your transcription will be compared with the other cell by cell; every number must match the page exactly,
and disagreements are settled from the page image with credit to whichever reading was right. Read carefully, and say
what you could not read rather than guess. US English; no em-dashes or en-dashes.

Work only inside this workspace (the folder holding this file); write everything under `out/`. Do not open any other
folder on the machine, in particular no repository, no `extractions/`, `qa/` or `.agent-related/` folder.

## Evidence (folder `packet/`)

- `pages/pNNNN.png`: the 300 dpi page images of Section V of AM-68-1 Vol. I (1/6-scale LM model drop tests), PDF
  pages 280 to 344, plus `pages/p0041.png` (Table 2-3, the soils, printed 2-16). Table 5-T3, "Detail Correlation
  Drops", is on `p0325.png` (printed 5-45) and is printed **sideways**: turn it to read it (the scan is unrotated).
  The text before it (PDF 322 to 324) describes these drops; Table 5-T2 (PDF 308 to 312) lists all model drops.
- `section5-pages.csv`: printed page label of each PDF page, and the figures and tables printed on it (id and title).
- `index-conventions.csv`: the project's experiment index (one row per test or table of tests), without its notes,
  as an example of the conventions. It already holds `b68-mdrop-10` and `b68-mdrop-11`, the records of the time
  histories of NASA Tests No. 1 and 2 (Figs. 5-22 to 5-39); those two rows are left out of this copy.
- `experiments-conventions.md`: the index's columns, kinds and test types.
- `tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --zoom 3 --out <png>` (in the workspace, not in `packet/`)
  makes a zoomed crop with a pixel grid (run `--help` first). Python:
  `<local path>`. Look at crops with your image viewer.

## Part 1: the table

1. `out/table.csv`: one row per printed drop, in printed order, with these columns:

   ```
   nasa_test_no,bendix_drop_no,VV_in_s,Vh_in_s,tau_s,soil,Dr,gamma_pcf,phi_deg,note
   ```

   They are the table's nine columns from left to right: NASA Test No.; Bendix Drop No.; V_v (In./Sec.); V_h
   (In./Sec.); tau (Sec.); Soil; D_r; gamma (Lb./Ft.^3); phi (Deg.). If the page's columns differ from this list,
   follow the page and say so.

2. Rules for cells:
   - Every value **exactly as printed**: keep the sign and the decimals printed ("-60.0", "84.0", ".298" with no
     leading zero if none is printed); the Soil column as printed, words and capitals ("RS Loose"); do not compute,
     round or convert.
   - A cell printed blank, or with a ditto mark, is written as printed (empty, or the mark) and explained in `note`;
     never filled in from the row above.
   - A blurred or broken digit you can still read with confidence: write the digit and say in `note` which cell and
     why. A digit you cannot read: write `?` in its place (for example `-11?.3`) and explain in `note`. Never guess.
   - `note`: anything about that row (a cell damaged, a mark on the page); empty otherwise.

3. `out/notes.md`:
   - the table's caption and header as printed, column by column (units and symbols as you read them);
   - the legend printed under or beside the table, quoted line by line;
   - what the text says about these drops (PDF 322 to 324, and any other page of Section V that speaks of them):
     how the velocities V_v and V_h and the time tau were obtained (measured, or computed, and from what), what
     "release" and "touchdown" mean, how the beds were prepared and how D_r, gamma and phi were obtained for each bed.
     Quote each statement with its printed page and PDF page; say plainly when the text does not say;
   - every number printed elsewhere in Section V for one of these drops that differs from the table (for example a
     velocity printed in a figure's inset, or the nominal velocities of Table 5-T2), with its location;
   - every cell you were unsure of, with its pixel position on the scan;
   - anything else a careful reader should know (stray marks, the scan's quality).

## Part 2: the index rows

`out/experiments.csv`: index rows for the table, in the `index-conventions.csv` style, columns in this order:

```
experiment_id,source_id,kind,test_type,test_label_printed,soil_family,soil_no,soil_no_status,state_printed,dr_printed,unit_weight_printed_pcf,gp_printed_g,apparatus,penetrator_printed,bin_printed_in,loading,rate_printed,start_depth_printed_in,measured_channels,evidence,setup_status,mcc_relevant,priority,relation,relation_target,notes
```

Rules:

1. **One row per soil family in the table**: `b68-mdrop-t5-3-rs` for the drops on RS beds, `b68-mdrop-t5-3-ss` for
   the drops on SS beds (another family, if the table has one, gets `b68-mdrop-t5-3-<family lower case>`).
2. `source_id`: `bendix-1968-vol1`. `kind`: `run-table` (a printed table of separate runs of one test type, one
   physical test per row). `test_type`: `mdrop`.
3. `test_label_printed`: the table's caption as printed after the table number.
4. `soil_family` (`RS | PS | RSM | RC2 | SS | LSM`). `soil_no`: the soil number of Table 2-3 (PDF 41) only when every
   drop of the row is on one numbered soil there (same family and state); `soil_no_status` `reported` when the report
   prints that number for these drops, `inferred` when you matched it by family and state, and `soil_no` empty with
   `unknown` when the row's drops are on more than one state.
5. `state_printed`: the row's distinct Soil-column values as printed, in printed order, separated by `; `.
   `dr_printed`, `unit_weight_printed_pcf`: one value as printed when every drop of the row has it, else the range
   `<low> to <high>` in printed digits. `gp_printed_g`: empty unless printed.
6. `apparatus` (the model and the drop rig, as Section V names them), `penetrator_printed` (the footpads as printed),
   `bin_printed_in` (the soil bed's dimensions as printed, with their unit as printed), `loading` (how the drop was
   made: free drop, the model's weight, attitude, surface slope, as printed for these drops), `rate_printed` (the
   ranges of V_v and V_h printed in the table for the row's drops, with the unit as printed),
   `start_depth_printed_in` (empty unless printed). Cite where each is printed in the "Setup" section below.
7. `measured_channels`: in words, what the table gives for each drop, and which responses (loads, penetration,
   accelerations) Section V prints for the row's drops elsewhere (name the figures), or that it prints none.
8. `evidence`: figure and table ids separated by `;`, plus `text <printed page> (PDF <n>)` where the text adds a fact.
9. `setup_status`: `complete` only if the drops' setup is printed fully enough to reproduce them (model, bed and its
   density and depth, touchdown velocities and attitude, gravity); otherwise `setup_incomplete`, and say in `notes`
   what is missing.
10. `mcc_relevant`: `no` unless the text says beds were reused or reloaded (say so).
11. `priority`: 1. `relation`, `relation_target`: when the row's drops include a test that already has its own record
    in the index (the two records named above), `same-as` with those ids separated by `;`; empty otherwise.
12. `notes`: short; the number of drops, NASA and Bendix numbers, anything printed differently in two places.

Quote every field that contains a comma. After the CSV, write a section "Setup" at the end of `out/notes.md`: where
each setup fact is printed (cite as `AM-68-1 Vol. I, Table 5-T3, printed 5-45, PDF 325`) and what a simulator user
would still have to assume.

When you finish, report briefly: rows and columns transcribed, the cells you were unsure of, what the text says about
how V_v, V_h and tau were obtained, and the index rows written.
