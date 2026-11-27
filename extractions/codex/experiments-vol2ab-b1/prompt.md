# Task: experiment index for Volume II Appendices A and B (soil specifications; wave-velocity moduli) of the 1968 Bendix LM Soil Mechanics Study

You are one of two independent readers (the other works blind elsewhere); the two tables are diffed
mechanically and every disagreement is settled from the page, with credit to whichever reading was
right. Be precise and say what you could not determine.

## Evidence (source only)

- The page images `corpus/1968-vol2/images/p0002.png` to `p0114.png` (AM-68-1 Vol. II, NASA
  CR-92215, Appendix A: the specifications of the twelve soils, PDF 2 to 97; Appendix B: the
  wave-velocity (sonic) moduli, PDF 98 to 114; 300 dpi).
- The agreed page transcriptions `corpus/1968-vol2/pages/p0002.md` to `p0114.md` and the agreed
  figures index `corpus/1968-vol2/figures.csv` (rows FA-*, FB-* and the tables TA-*; its `in_scope`,
  `relation` and `relation_target` columns say which figures repeat or derive from which).
- The existing experiment index `data/experiments/index.csv` (Volume I and Volume II Appendix C, for
  relations only: for example the Volume I grain-size averages `b68-gs-f2-14-rs`, the friction-angle
  charts of Appendix C `b68-ds-fc-16` to `b68-ds-fc-22`, Table 2-3 summaries `b68-gs-t2-3-12`).
- Conventions: `docs/DATA-ORGANIZATION.md` (the experiment index, its kinds and test types),
  `AGENTS.md`.

Do NOT open anything under `extractions/` or `qa/` (other agents' readings and notes live there; an
inventory must be made from the source so the two inventories cannot share an error), and do not
look for the other reader's table.

## What to produce

One CSV table in the `data/experiments/index.csv` style, one row per physical test, sample analysis,
test series or derived series documented in Appendices A and B (PDF 2 to 114), for the figures and
tables marked `in_scope = yes` in the figures index (a repeated figure that is out of scope adds its id
to the evidence of the row it repeats, but no row of its own). The data unit is the experiment, not
the figure: the same analysis plotted in two figures is one row with both figures in `evidence`. A
curve the authors drew through points derived from tests is kind `derived-series`; a curve the report
says is averaged from several samples is `averaged-series`; a computed or nomographic curve drawn
without points is `correlation`; a number that exists only in a table or the text is `summary`; a bin
sample analyzed for grain size and minimum and maximum density is `sample`.

Columns, in this order:

```
experiment_id,source_id,kind,test_type,test_label_printed,soil_family,soil_no,soil_no_status,state_printed,dr_printed,unit_weight_printed_pcf,gp_printed_g,apparatus,penetrator_printed,bin_printed_in,loading,rate_printed,start_depth_printed_in,measured_channels,evidence,setup_status,mcc_relevant,priority,relation,relation_target,notes
```

Rules:

1. `experiment_id`: `b68-<test_type>-<figure or table id>[-<label>]`, lower case, hyphens only:
   grain-size curves `b68-gs-fa-2`; density charts `b68-dens-fa-3`; friction-angle charts
   `b68-ds-fa-4`; Appendix B moduli per density group by printed Dr in hundredths,
   `b68-sonic-fb-3-dr99` (`dr99p5` for Dr 0.995); a table row `b68-<type>-ta-p003-<label>`.
2. `source_id`: `bendix-1968-vol2`.
3. `kind`: `single | averaged-series | derived-series | correlation | summary | sample`.
4. `test_type`: `gs | dens | ds | tx | sonic | smp` (`smp` for a bin sample with grain size and
   density together; see `docs/DATA-ORGANIZATION.md`).
5. `test_label_printed`: the caption, legend or table label as printed.
6. `soil_family`: `RS | PS | RSM | RSM-a | RSM-b | RC2 | SS | LSM`.
7. `soil_no`: the soil number (1 to 12) when the specification it belongs to names it (Appendix A is
   organized as Specification for Soil No. 1 to 12); `soil_no_status`: `reported | inferred |
   conflict | unknown`.
8. `state_printed`, `dr_printed`, `unit_weight_printed_pcf`: exactly as printed, empty when not
   printed, never inferred; `approx` for the approximately symbol.
9. `apparatus`, `loading`, `rate_printed`: from the figure, table or text; empty when not stated.
   `penetrator_printed`, `bin_printed_in`, `start_depth_printed_in`, `gp_printed_g` are empty here.
10. `measured_channels`: in words (`percent finer vs grain size (average and range)`,
    `unit weight vs relative density`, `friction angle vs relative density`, `modulus vs confining
    pressure`).
11. `evidence`: figure and table ids separated by `;`, plus `text <printed page> (PDF <n>)` where
    the text adds a setup fact.
12. `setup_status`: `complete | setup_incomplete | pending` as in the Appendix C index (pending for
    derived series whose underlying tests are not identified).
13. `mcc_relevant`: `no` unless the figure compares the same material after different histories.
14. `priority`: 1 for the soil characterization (grain size, density limits) and the moduli, 2 for
    the friction-angle charts, 3 context.
15. `relation`, `relation_target`: `same-as` with an existing experiment id when the row is an
    analysis already in `data/experiments/index.csv`; `derived-from` with the ids it is computed
    from (separated by `;`); `reproduces` is not a relation of experiments (a figure reproducing
    another is the same experiment: use `same-as`). Empty otherwise.
16. `notes`: short; misprints, values printed differently in two places, anything you could not read.

Quote every field that contains a comma. Do not use em-dashes or en-dashes. Numbers exactly as
printed. Put the table in a fenced ```csv block in your final answer (and, when your task names an
output file outside the repository, write it there too), followed by a short list of conflicts
between figures and what you could not determine. Do not edit anything in the repository.
Cite as `AM-68-1 Vol. II, Fig. A-2, printed A-6, PDF 7`.
