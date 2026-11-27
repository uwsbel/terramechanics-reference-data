# Task: inventory of the figures and tables in Volume II, Appendices A, B and C (blind)

You are Codex, working with Claude as colleagues for Dan. Claude is making the same inventory
blind at the same time; the two are diffed mechanically and the disagreements reviewed. Work from
the source only: the PDF, the page map, and the agreed Volume I indexes. Do not use either agent's
notes under `extractions/` (they are not evidence; see `AGENTS.md`, two-agent protocol). No
em-dashes or en-dashes.

## Source

`nasa-reports/volume2/1968-nasa-LunarModule-SoilMechanicsStudy-Vol2.pdf` (NASA CR-92215,
AM-68-1 Volume II, 236 PDF pages). Page map: `corpus/1968-vol2/page-map.csv` (column
`inferred_label` is the authoritative printed label; many pages have none). Scope: Appendix A
(soil specimens, about PDF 2 to 97), Appendix B (tangent modulus, about PDF 98 to 114), Appendix C
(direct shear test data, about PDF 115 to 159). Appendices D and E are out of scope. Render and
inspect every page in scope, rotating the sideways ones; the lists of illustrations are an index,
not the evidence.

## What to produce

One CSV in a fenced ```csv block with the Volume I figures-index columns plus three new ones, one
row per figure or table (a page with two figures gives two rows):

```
id,kind,title_as_printed,printed_page,pdf_page,appendix,test_type,soils,states,apparatus,rate_or_dynamics,data_form,panels,curves,trace_classes,x_quantity,x_unit,x_axis_type,y_quantity,y_unit,y_axis_type,legend_entries,rotation,in_scope,transcribe,priority,mcc_relevant,relation,relation_target,notes
```

Rules (same as `docs/DATA-ORGANIZATION.md`, "Figures index", which you should read):

1. `id`: as printed, `FC-1B`, `FA-12`, `TB-2`; if a figure has lettered sub-figures on separate
   pages (C-1A, C-1B) each is a row. Unnumbered data sheets get `FC-pNNN` with the PDF page.
2. `kind`: figure | table | data-sheet. `appendix`: A | B | C.
3. `test_type` from the vocabulary: grain size, density, bed preparation, direct shear, triaxial,
   load penetration, dynamic penetrometer, drag, impact, sonic, soil model, soil properties,
   apparatus, other. `data_form`: table | curve | schematic | photo | text | mixed.
4. `curves`: every drawn line is a trace, including each boundary of a range band; markers and
   the fitted line through them are one series; construction guides are not counted.
   `trace_classes` from measurement-markers | recorded-trace | author-fit | computed | schematic |
   setup-evidence.
5. Units as printed in `x_unit` and `y_unit` (the normalizer handles spelling). `*_axis_type`:
   linear | log | normalized | reciprocal | n/a.
6. `in_scope` (yes | maybe | no): the item carries numbers to extract. `transcribe`: yes for
   every page in scope. `priority`: 1 needed for the first calibration and prediction protocols
   (shear family, materials); 2 setup and interpretation; 3 context. `mcc_relevant`: yes only for
   history-dependent evidence (same material after different histories, different response).
7. **Relations** (new): `relation` in `same-as | derived-from | reproduces | unresolved | none`
   and `relation_target` the Volume I id (for example `F2-21`) or another Volume II id. Use
   `reproduces` when a Volume II figure repeats a Volume I figure (compare axes, legend and
   values), `derived-from` when it is a reduction of identified tests, `same-as` when two rows are
   one physical test, `unresolved` when you suspect a link but cannot confirm it. Say in notes what
   you compared. The Volume I index is `corpus/1968/figures.csv`.
8. `notes`: short; legibility, damaged print, inset tables (list their values), soil and density
   labels as printed, what you could not read.

Quote every field containing a comma. After the CSV, a short section: how Appendix C is
organized (data sheets per soil and density? failure envelopes? combined plots?), how many direct
shear tests you count and on which soils and densities (a small table: soil, Dr, number of normal
stresses, dilation panel yes or no), what Appendix A holds per soil (gradation analyses, min/max
density determinations, photographs), what Appendix B holds, and anything that bears on the
calibration design. Cite as `AM-68-1 Vol. II, Fig. C-1B, printed C-3, PDF 117`.
