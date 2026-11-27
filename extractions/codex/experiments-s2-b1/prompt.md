# Task: experiment index for Volume I Section II of the 1968 Bendix LM Soil Mechanics Study

You are working with Claude as a colleague on the same team, for Dan. Claude has written its own
version of this index blind; yours is produced blind too, then the two are diffed mechanically
and the disagreements reviewed by a student. Be precise and say what you could not determine.
Do not look for Claude's version; it is not in the repository.

## What to produce

One CSV table, `data/experiments/index.csv` style, in a fenced ```csv block in your final answer,
one row per physical test, test series or derived series documented in Section II (PDF 26 to 138)
of `nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf`. The repository's figures index
`corpus/1968/figures.csv` (agreed by both agents today) tells you which figures carry data and the
page map `corpus/1968/page-map.csv` gives printed labels. Read `docs/DATA-ORGANIZATION.md` and
`AGENTS.md` for conventions. Render and inspect every figure you derive a row from; the notes
columns of the figures index are hints to verify, not evidence.

The data unit is the experiment (one physical test on one bed), not the figure. The same test
plotted in two figures is one row with both figures in `evidence`. A curve that the report says is
averaged from several tests is one row of kind `averaged-series`. A correlation or fit the authors
drew without the underlying points is kind `correlation` or `derived-series`. A number that exists
only in the text (triaxial results, DPT bed statistics) is kind `summary`. A bin sample analyzed
for grain size and min/max density is kind `sample`.

Columns, in this order:

```
experiment_id,source_id,kind,test_type,test_label_printed,soil_family,soil_no,soil_no_status,state_printed,dr_printed,unit_weight_printed_pcf,gp_printed_g,apparatus,penetrator_printed,bin_printed_in,loading,rate_printed,start_depth_printed_in,measured_channels,evidence,setup_status,mcc_relevant,priority,notes
```

Rules for the columns:

1. `experiment_id`: `b68-<type>-<label>`. Type codes: `lpt` load-penetration, `ds` direct shear,
   `tx` triaxial, `dpt` dynamic penetrometer, `dens` density (min/max, compaction, in place),
   `gs` grain size, `smp` bin sample (grain size and MMDT together), `sonic`. Label: the report's
   own test number when printed, zero padded to three digits for LPT (`b68-lpt-027`, `b68-lpt-064A`),
   DPT record numbers as printed (`b68-dpt-r53958`), direct shear tests by normal stress
   (`b68-ds-f2-21-n3520`), subscale drag bin samples as printed (`b68-smp-ssd-4-18`). Series without a
   printed test number: figure id plus a sequence number in legend order (`b68-lpt-f2-36-s01`) or
   the legend label (`b68-dpt-f2-55-rs`, `b68-ds-f2-23-ss`). Lower case, hyphens only.
2. `source_id`: `bendix-1968-vol1` (the id in `sources/register.csv`). The `b68` prefix in experiment ids is a short alias for it.
3. `kind`: `single | averaged-series | derived-series | correlation | summary | sample`.
4. `test_type`: the type code above; two codes joined by `;` for a sample with both analyses.
5. `test_label_printed`: the label as the report prints it (for example `LPT 27`, `F2-36 Dr approx
   0.95 2 in cyl`).
6. `soil_family`: `RS | PS | RSM | RSM-a | RSM-b | RC2 | SS | LSM | all`, or `RS;SS` for a figure
   covering two.
7. `soil_no`: the Table 2-3 soil number (1 to 12) when the figure names it ("Soil No. 4") or when
   family plus state identifies it; empty when the state is not one of the twelve (dense PS, used
   soil) or unknown. `soil_no_status`: `reported` (number printed), `inferred` (from family and
   state), `conflict` (two figures give different states for the same test), `unknown`.
8. `state_printed`, `dr_printed`, `unit_weight_printed_pcf`, `gp_printed_g`: exactly as printed next
   to the test (caption, legend, inset or the text paragraph that describes the figure), with
   `approx` written out for the printed approximately symbol. Empty when not printed; never
   inferred from another test.
9. `apparatus`, `penetrator_printed`, `bin_printed_in`, `loading`, `rate_printed`,
   `start_depth_printed_in`: from the figure or the text describing it; empty when not stated.
   `start_depth_printed_in` is 0 for a test started at the surface, 2 for one started two inches
   below, as the figures say.
10. `measured_channels`: what was recorded, in words (for example `load vs penetration`,
    `shear stress and normal displacement vs shear displacement`, `deceleration vs time`).
11. `evidence`: figure and table ids separated by `;`, or `text <printed page> (PDF <n>)` for
    text-only evidence.
12. `setup_status`: `complete` when bed state, apparatus geometry, bin and loading rate are all
    printed; `setup_incomplete` when any is missing (say which in notes); `pending` for averaged
    and derived series whose underlying tests are not identified.
13. `mcc_relevant`: `yes` only for rows showing the same material after different loading or
    handling histories with a different response, plus the state maps needed to read them
    (DPT correlation, compaction time study, used-soil samples, density by test number);
    `maybe` for the direct shear tests because of the dilation panel; otherwise `no`.
14. `priority`: 1 = needed for the first calibration and prediction protocols (shear family,
    LPT records with a printed bed state or Gp, DPT signatures and correlation, materials and
    gradation); 2 = needed to set up or interpret those tests (bed preparation, boundary and bin
    effects, rate series, degradation, averaged series, correlations); 3 = context.
15. `notes`: short; mention conflicts between figures, damaged print, and what you could not read.

Quote every field that contains a comma. Do not use em-dashes or en-dashes anywhere. Numbers
exactly as printed (no unit conversion). After the CSV block, add a short section listing
conflicts you found between figures (same test, different labels) and anything you could not
determine. Cite as `AM-68-1 Vol. I, Fig. 2-43, printed 2-78, PDF 103`.
