# Task: inventory of the figures and tables of Volume I, Sections III, IV (start) and V (start) (blind)

You are one of two agents (Claude and Codex) making this inventory blind for Dan, at the same time; the two
are diffed mechanically and the disagreements reviewed against the page images. Work from the source only:
the page images, the PDF, the page map and the agreed indexes named below. Do not open anything under
`extractions/`, `qa/` or `.agent-related/` (other agents' notes are not evidence; `AGENTS.md`, two-agent
protocol). US English. No em-dashes or en-dashes. Do not edit any file in the repository.

## Why

Decision D-050 (`docs/decisions.csv`) brings the dynamic tests of the 1968 report into the data release:
vertical footpad impact, subscale drag and the 1/6-scale LM model drops, each first as a slice. This inventory
is the map of where their figures, tables and setup are printed; later readings work from it.

## Source

AM-68-1 Volume I (NASA CR-92208), `nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf`, 449 PDF pages.
Page images, 300 dpi, already rendered: `corpus/1968/images/pNNNN.png` (NNN the 4-digit PDF page). Page map:
`corpus/1968/page-map.csv` (`inferred_label` is the best printed label; some pages have none). Scope, every
page in these ranges:

1. PDF 142 to 212: Section III (controlled-motion test equipment: subscale drag, subscale oblique impact,
   full-scale oblique impact, full-scale drag facility, vacuum/atmosphere impact tester) and Section IV up to
   Fig. 4-22 (introduction, the drag test program, the impact test program, the drag result tables).
2. PDF 281 to 340: Section V up to Fig. 5-39 (the 1/6-scale LM model, instrumentation, drop facilities, the list
   of model drops, rigid-surface drops, the detailed correlation drops and the NASA Test 1 and 2 histories).

Look at every page in scope, rotating the sideways ones; the report's own lists of illustrations and tables
(PDF 9 to 14) are an index, not the evidence. The agreed index of Section II is `corpus/1968/figures.csv`, and
`docs/DATA-ORGANIZATION.md` ("Figures index") defines the columns and vocabularies.

## What to produce

1. One CSV, one row per figure or table (a page with two figures gives two rows; a figure continued over
   several pages, such as a table printed as Fig. 4-6a, 4-6b, 4-6c, gives a row per printed part), columns:

```
id,kind,title_as_printed,printed_page,pdf_page,section,test_type,soils,states,apparatus,rate_or_dynamics,data_form,panels,curves,trace_classes,x_quantity,x_unit,x_axis_type,y_quantity,y_unit,y_axis_type,legend_entries,rotation,in_scope,transcribe,priority,mcc_relevant,relation,relation_target,notes
```

Rules:

a. `id`: `F<section>-<n>` for figures as printed, with a printed sub-letter kept (`F4-6a`); tables `T<section>-<n>`
   (`TABLE 5-T2` is `T5-2`); an unnumbered table or figure `T-pNNN` or `F-pNNN` with the PDF page.
b. `kind`: figure | table. A numbered "Figure" that is printed as a table of numbers is kind `figure`,
   `data_form` `table`.
c. `section`: the report section the item is printed in (III, IV, V).
d. `test_type` from the vocabulary of DATA-ORGANIZATION.md, plus one new value for this batch: `model drop`
   (the 1/6-scale LM model landings). Footpad impact tests (subscale or full scale) are `impact`; drag
   tests `drag`; equipment drawings and photographs `apparatus`; analysis figures `soil model`.
e. `data_form`: table | curve | schematic | photo | text | mixed. `curves`: every drawn line is a trace;
   markers and the line through them are one series. `trace_classes` from measurement-markers |
   recorded-trace | author-fit | computed | schematic | setup-evidence.
f. Units exactly as printed in `x_unit` and `y_unit` (time in ms or s, force in lb or pounds, and so on);
   `*_axis_type` linear | log | normalized | reciprocal | n/a. For a table, list its column headers and units in
   `notes` instead.
g. `rotation`: degrees clockwise that make the item upright (0, 90, 180, 270).
h. `in_scope` (yes | maybe | no): the item carries measured numbers that could be extracted into `data/`.
   `transcribe`: yes for every page in scope. `priority`: 1 = measured results of a drag, impact or model-drop
   test, or the test parameters needed to set such a test up (velocities, masses, footpad sizes, soil and
   density per run); 2 = setup and interpretation (apparatus dimensions, instrumentation, calibration); 3 =
   context (photographs, analysis). `mcc_relevant`: yes only for history-dependent evidence (the same bed
   loaded again after a first test).
i. `relation`: same-as | derived-from | reproduces | unresolved | none, and `relation_target` another id in
   this batch or in `corpus/1968/figures.csv` (for example a figure that plots the same runs as another, or a
   plot derived from a table). Say in `notes` what you compared.
j. `notes`: short. Run identities, soils, relative densities, footpad diameters, velocities as printed;
   what is measured against what; for a figure that mixes measured and computed curves, which is which;
   legibility; what you could not read.

Quote every field containing a comma. Put the CSV in a fenced ```csv block.

2. After the CSV, a section "Setup" with one subsection per family (subscale drag, subscale impact, full-scale
   impact, 1/6-scale model drops). For each: where the apparatus, the procedure and the run parameters are
   printed (printed page and PDF page), what is given in numbers (footpad diameter and mass, drop or drag
   velocity, path angle, gravity of the test, soil bed size and preparation, density measurement, sampling of
   the recorders, the model's mass and scale factors), and what a simulator user would need that you could not
   find. Cite as `AM-68-1 Vol. I, Fig. 4-19, printed 4-23, PDF 208`.

3. A section "Counts": per drag soil, the number of runs printed (Figs. 4-6 to 4-16); the impact runs per soil
   and footpad that have force histories; the model drops listed in Table 5-T2 and which have histories.
