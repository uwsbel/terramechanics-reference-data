# Review: Volume II inventory, Appendices A, B and C (batch inventory-vol2-b1)

Date 2026-10-07. Two blind inventories of AM-68-1 Vol. II (NASA CR-92215), PDF 2 to 159, from the
page images: Claude (112 rows, notes under `extractions/claude/inventory-vol2-b1/notes/`) and Codex
(gpt-6-astra, high, read-only, 1048 s; 122 rows, `extractions/codex/inventory-vol2-b1/`). Diff:
`tools/diff_tables.py --key id` after Claude's table ids were mapped to the page-locator scheme
(`id-aliases.json`); report in `diff.md`. Result: `corpus/1968-vol2/figures.csv` and `.json`, built by
`tools/build_figures.py` with `resolutions.csv` (252 cell decisions) and `row-decisions.csv` (10 rows).

## Agreement

| | |
|---|---:|
| rows in both submissions | 112 |
| rows in Codex only (unnumbered tables Claude folded into the specification rows) | 10 |
| cells compared (28 columns) | 3136 |
| cells agreed after typography normalization | 2254 (71.9 percent) |
| disagreements, numeric | 70 |
| disagreements, text (descriptive columns, not reconciled, kept as alternates) | 812 |

All 100 numbered figures were found by both agents with the same ids, PDF pages (except four table
rows) and rotations; every axis type agreed. The disagreements that mattered were about conventions
(what counts as a panel, a curve, a table, a priority) and about relations to Volume I.

## Where each agent was right (page re-reads)

Codex right, Claude wrong:

1. Chemical analysis tables start on the page after the specification heading (soil 5: A-34, PDF 35;
   soils 10, 11, 12 likewise). Claude had recorded the specification's first page.
2. FA-45, the "RSM" photomicrograph under soil 12 (RSM-b), is the same photograph as FA-17 (RSM-a):
   same grains, same ruler position. The report has no RSM-b photomicrograph.
3. The soil 10 copy of the Volcalite analysis (A-72, PDF 73) omits the MgO line and prints 5.58 against
   calcium oxide (master on A-34: CaO 8.11, MgO 5.58). Claude had read that page as clean.
4. The computer-fitted envelopes FC-9A, FC-10A and FC-11A derive from the data sheets FC-1D, FC-2B and
   FC-3B: the printed average density equals the mean of the legend unit weights in each case (54.2,
   25.9, 58.2). Claude had recorded no relation.
5. Ten unnumbered tables (normative mineral analyses, the two clay analyses) deserve rows of their own.

Claude right, Codex wrong:

1. Printed page labels where Codex copied the page map: FB-2 is IITRI page 5 (map said unknown), FB-7
   and FB-8 are 10 and 11 (map said ii), FC-22 is C-44 (map said i), FC-23 is C-45/C-46 (map said
   unknown), and the scrambled binding at PDF 147 to 149 (C-35, C-34, C-33) where the map's per-section
   inference had put C-33 and C-35 the wrong way round. The page map now carries a corrections file
   (`corpus/1968-vol2/page-map-corrections.csv`) for these eight pages.
2. Relations to Volume I: the grain-size averages (F2-14), the density lines (F2-17), the phi curves
   (F2-23 and FC-16 to FC-22) and Table 2-3's moduli (FB-3 to FB-7) all have Volume II originals;
   Codex recorded none.

Both agents caught the soil 11 copy's slip (MgO 1.61, Na2O omitted, A-81) and the iron oxide 1.1
versus 1.2 difference between the two clay analyses.

## Conventions applied (recorded as `rule` or `convention` in the sidecar)

1. Photographs: 0 panels, 0 curves, priority 3 (Volume I precedent).
2. Curves: solid average plus two dashed bounds is 3; markers with range bars are markers; a band is 2.
3. `mixed` for a plot with an inset table or printed fit parameters; `curve` for a data sheet whose
   legend lists the test identities (as F2-21).
4. A reproduction (figure or table printed again under another soil) is `in_scope` no, priority 3,
   relation `reproduces`; the first printing holds the numbers.
5. Chemical analyses priority 2 (material identity, not a simulation input); the normative mineral
   analysis is of a reference rock from the literature, not the test soil: `in_scope` no, priority 3.
6. Per-soil phi versus Dr curves (Appendix A) priority 2: the Appendix C figures they summarize are 1.
7. `mcc_relevant`: density versus Dr maps yes (F2-17 precedent); LSM phi band yes (loose specimens
   densified under the normal load); data-sheet dilation panels maybe (F2-21 precedent).
8. Axis multipliers ("x 10^-3", "(x 10^1)") belong to the quantity, not the unit; `ksi` added to the unit
   list for the IITRI modulus plots.

## Provisional

FB-3 to FB-7 (modulus versus confining pressure, five soils) are priority 1 in the index; the status was
`provisional` until Dan decided for 1 on 2026-10-08. Codex graded them 2 (setup), Claude 1 (the curve behind Table 2-3 E
and the elastic parameters of the CRM model).

## Counts in the index

122 rows: Appendix A 70 (48 figures, 22 tables), B 8, C 44. In scope 77; priority 1: 63 (all of Appendix
C's 44, the seven distinct grain-size and seven density figures of Appendix A, the five IITRI modulus
plots). Relations: 46 reproduces, 37 derived-from, 5 unresolved, 34 none. Codex's count of 85 shear
tests with displacement records (73 with dilation panels) across 15 soil-and-density series matches
Claude's notes.
