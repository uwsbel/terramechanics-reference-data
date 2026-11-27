# Task: inventory of the figures and tables of Volume I, the end of Section V and Section VI (blind, batch inventory-s6-b1)

You are one of two agents (Claude and Codex) making this inventory blind, at the same time; the two are diffed
mechanically and the disagreements reviewed against the page images. Work from the source only: the page images, the
page map and the agreed index in `packet/`. Work only inside this workspace (the folder holding this file) and write
everything under `out/`; do not open any other folder on the machine (no repository, no `extractions/`, `qa/` or
`.agent-related/` folder, no other agent's work). US English. No em-dashes or en-dashes.

## Why

The project brings the dynamic tests of a 1968 NASA report (Bendix AM-68-1, Lunar Module soil mechanics study) into a
public data release, starting with the 1/6-scale LM model drops. The figures index already covers Sections II to V up
to Fig. 5-39. This inventory extends it to the end of Section V and through Section VI, which compares the model drops
with the report's computer simulation. It is a map of where things are printed; later readings work from it.

## Source

AM-68-1 Volume I (NASA CR-92208). Page images, 300 dpi, in `packet/pages/pNNNN.png` (NNNN the 4-digit PDF page):
every page from PDF 345 to 440, that is Section V from printed 5-65 to its end (PDF 358) and all of Section VI (PDF 359
to 440). Look at every page, rotating the sideways ones. `packet/lists/` holds the report's lists of illustrations
and tables (PDF 9 to 14): an index to cross-check against, not evidence. `packet/page-map.csv` gives the printed label
of each PDF page (`inferred_label` is the best one; some pages have none). `packet/figures-index-agreed.csv` is the
agreed index of the earlier sections (without its notes): the conventions to follow, and the targets for relations.
`packet/figures-conventions.md` defines the columns and vocabularies.

`tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --zoom 3 --out <png>` (in the workspace) makes a zoomed crop with
a pixel grid (run `--help` first). Python: `<local path>`. Install nothing.

## What to produce

1. `out/inventory.csv`: one row per figure or table (a page with two figures gives two rows; an item printed over
   several pages, such as a figure in four sheets, gives a row per page), columns:

```
id,kind,title_as_printed,printed_page,pdf_page,section,test_type,soils,states,apparatus,rate_or_dynamics,data_form,panels,curves,trace_classes,x_quantity,x_unit,x_axis_type,y_quantity,y_unit,y_axis_type,legend_entries,rotation,in_scope,transcribe,priority,mcc_relevant,relation,relation_target,notes
```

Rules:

a. `id`: `F<section>-<n>` for figures as printed, with a printed sub-letter kept; tables `T<section>-<n>`; an
   unnumbered table or figure `T-pNNN` or `F-pNNN` with the PDF page. A figure printed over several pages: the first
   page keeps the printed id, each later page gets `<id>-pNNN` with its PDF page (`F6-11-p376`), as the agreed index
   does (`T5-2-p309`).
b. `kind`: figure | table. A numbered "Figure" printed as a table of numbers is kind `figure`, `data_form` `table`.
c. `section`: V or VI.
d. `test_type` from the vocabulary in `figures-conventions.md` and the agreed index (`model drop` for the 1/6-scale
   LM model landings, `apparatus` for equipment drawings and photographs, `soil model` for analysis and computer
   program figures).
e. `data_form`: table | curve | schematic | photo | text | mixed. `panels`: the number of plotted panels on the page.
   `curves`: every drawn line is a trace; markers and the line through them are one series; give the total over the
   page's panels. `trace_classes` from measurement-markers | recorded-trace | author-fit | computed | schematic |
   setup-evidence, every class present, `;` separated (a panel with an experimental and a computed curve has both).
f. Units exactly as the vocabulary writes them, the printed spelling in `notes` when it differs; `*_axis_type` linear
   | log | normalized | reciprocal | n/a. For a page of several panels with different axes, give the first panel's
   axes and list every panel's quantity and unit in `notes`. For a table, list its column headers and units in
   `notes`.
g. `rotation`: degrees clockwise that make the item upright (0, 90, 180, 270).
h. `in_scope` (yes | maybe | no): the item carries measured numbers that could be extracted into `data/` (a curve
   computed by the report's program alone is not a measurement: `maybe` at most, say why). `transcribe`: yes for every
   page in scope. `priority`: 1 = measured results of a model drop, or the parameters needed to set one up; 2 = setup
   and interpretation; 3 = context (photographs, program flow charts, computed-only results). `mcc_relevant`: yes
   only for history-dependent evidence (the same bed loaded again after a first test).
i. `relation`: same-as | derived-from | reproduces | unresolved | none, and `relation_target` ids in this batch or in
   `figures-index-agreed.csv` (for example a Section VI figure whose experimental curves are the same drop's histories
   printed in Section V, or a figure that repeats a table's conditions). Say in `notes` what you compared.
j. `notes`: short. Drop identities as printed (LM model drop number, NASA or Bendix), soils, velocities, which curves
   are experimental and which computed (and the strut damping of the computation), the panels by letter, legibility,
   what you could not read.

Quote every field containing a comma.

2. `out/notes.md`, with a section "Counts": for each of the eight detail correlation drops (NASA 1 to 8), the figures
   and PDF pages where Section VI plots its measured (experimental) histories, the panels per sheet and their
   quantities, and whether a computed-only figure exists for it; then the other figures with measured data (stability
   profiles, tables of drops), with what they plot. Add anything a careful reader should know: printing quirks, the
   prose's statements about these figures that disagree with the figures or the tables (quote with printed and PDF
   page), pages you could not read.

When you finish, report briefly: rows written, the ids and pages covered, and anything you could not read.
