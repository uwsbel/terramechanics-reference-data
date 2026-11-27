# Task: experiment index for Volume II Appendix C (direct shear test data) of the 1968 Bendix LM Soil Mechanics Study

You are one of two independent readers (the other is Claude, working blind elsewhere); the two
tables are diffed mechanically and every disagreement is settled from the page, with credit to
whichever reading was right. Be precise and say what you could not determine.

## Evidence (source only)

- The page images `corpus/1968-vol2/images/p0115.png` to `p0159.png` (AM-68-1 Vol. II, NASA
  CR-92215, Appendix C, 300 dpi) and the PDF `nasa-reports/` file for Volume II if you prefer.
- The agreed page transcriptions `corpus/1968-vol2/pages/p0115.md` to `p0159.md` and the agreed
  figures index `corpus/1968-vol2/figures.csv` (rows FC-1A to FC-23; its `relation` and
  `relation_target` columns say which Volume II figures reproduce or derive from which).
- The existing Volume I experiment index `data/experiments/index.csv` (for relations only: the
  tests of Figure C-1B are the tests of Volume I Figure 2-21, already indexed as
  `b68-ds-f2-21-n294` and so on).
- Conventions: `docs/DATA-ORGANIZATION.md`, `AGENTS.md`.

Do NOT open anything under `extractions/` or `qa/` (other agents' readings and notes live there; an
inventory must be made from the source so the two inventories cannot share an error), and do not
look for the other reader's table.

## What to produce

One CSV table in the `data/experiments/index.csv` style, one row per physical test, test series or
derived series documented in Appendix C (PDF 115 to 159). The data unit is the experiment (one
physical test on one specimen), not the figure: the same test plotted in two figures is one row
with both figures in `evidence`. A failure envelope or friction-angle curve drawn through points
derived from the tests is kind `derived-series`; a computed (model) curve is kind `correlation`;
a number that exists only in the text is kind `summary`.

Columns, in this order:

```
experiment_id,source_id,kind,test_type,test_label_printed,soil_family,soil_no,soil_no_status,state_printed,dr_printed,unit_weight_printed_pcf,gp_printed_g,apparatus,penetrator_printed,bin_printed_in,loading,rate_printed,start_depth_printed_in,measured_channels,evidence,setup_status,mcc_relevant,priority,relation,relation_target,notes
```

Rules:

1. `experiment_id`: `b68-ds-<figure>-n<normal stress as printed>` for a single direct shear test
   on a data sheet, figure id lower case with hyphens (`b68-ds-fc-1c-n3520`); for the tests of
   Figure C-1B use the existing Volume I ids (`b68-ds-f2-21-n294`, ...) with relation `same-as`
   and relation_target the same id. Derived series: `b68-ds-fc-1a` (envelopes of figure C-1A),
   `b68-ds-fc-16` (friction angle vs relative density), computed plots `b68-ds-fc-9a` and so on;
   when one figure carries several derived series, add the legend label (`b68-ds-fc-1a-dense`).
   Lower case, hyphens only.
2. `source_id`: `bendix-1968-vol2`.
3. `kind`: `single | averaged-series | derived-series | correlation | summary | sample`.
4. `test_type`: `ds`.
5. `test_label_printed`: the legend or caption label as printed (for example `sigma 3520 PSF,
   gamma 49.5 PCF`).
6. `soil_family`: `RS | PS | RSM | RSM-a | RSM-b | RC2 | SS | LSM`.
7. `soil_no`: the Table 2-3 soil number (1 to 12) when family plus state identifies it (Table 2-3
   is Volume I PDF 41; its rows are also in `corpus/1968/pages/p0041.md`); empty when the state is
   not one of the twelve. `soil_no_status`: `reported | inferred | conflict | unknown`.
8. `state_printed`, `dr_printed`, `unit_weight_printed_pcf`: exactly as printed (caption, legend
   inset, text), `approx` for the approximately symbol; empty when not printed; never inferred.
   The unit weight of a single test is its own legend gamma.
9. `apparatus`, `loading`, `rate_printed`: from the figure or the Appendix C text (PDF 115 and the
   figure pages); empty when not stated. `penetrator_printed`, `bin_printed_in`,
   `start_depth_printed_in`, `gp_printed_g` are empty for direct shear.
10. `measured_channels`: in words (`shear stress and dilation vs shear displacement`,
    `peak shear stress vs normal stress`, `friction angle vs relative density`).
11. `evidence`: figure ids separated by `;` (`FC-1C`), plus `text <printed page> (PDF <n>)` where
    the text adds a setup fact.
12. `setup_status`: `complete` when specimen state, apparatus geometry and loading rate are all
    printed; `setup_incomplete` when any is missing (say which in notes); `pending` for derived
    series whose underlying tests are not identified.
13. `mcc_relevant`: `maybe` for single direct shear tests (the dilation panel); otherwise `no`
    unless the figure compares the same material after different histories.
14. `priority`: 1 for the single tests and the envelopes (the shear family is the first calibration
    protocol), 2 for the friction-angle and computed plots, 3 context.
15. `relation`, `relation_target`: `same-as` with the Volume I experiment id when the row is a test
    already in `data/experiments/index.csv`; `derived-from` with the ids it is computed from
    (separated by `;`) for derived series when the figure says so; otherwise empty.
16. `notes`: short; misprints in legends (for example a header printed tau for gamma), stresses
    printed differently in two places, anything you could not read.

Quote every field that contains a comma. Do not use em-dashes or en-dashes. Numbers exactly as
printed. Put the table in a fenced ```csv block in your final answer (and, when your task names an
output file outside the repository, write it there too), followed by a short list of conflicts
between figures and what you could not determine. Do not edit anything in the repository.
Cite as `AM-68-1 Vol. II, Fig. C-1C, printed C-4, PDF 118`.
