# Review: Section II inventory, batch inventory-s2-b1

Two blind inventories of every figure and table in AM-68-1 Vol. I Section II (plus Table 1-1):
`extractions/claude/inventory-s2-b1/inventory-claude.csv` and
`extractions/codex/inventory-s2-b1/inventory-codex.csv` (gpt-6-astra, high, read-only, 27.7 min,
thread 01a1175e-2069-7d31-a24a-7e5cc1e73604). Mechanical diff in `diff-report.md`, agreed cells in
`agreed.csv`. Written 2026-10-07.

## Result in one paragraph

Both agents found the same 69 items (65 figures, 4 tables) and agree on every identity fact: kind,
printed page, PDF page and panel count agree on all 69 rows, rotation on 68. The disagreements are
(a) four curve counts, two of which are a counting convention, (b) spelling conventions for units
and axis-type vocabulary, which are not real disagreements, and (c) judgment columns, where Codex
read `in_scope` and `mcc_relevant` far more broadly than Claude did. The judgment split needs a
rule from Dan, not a re-read of the pages.

## 1. Factual disagreements (resolved by re-reading the page)

| id | column | claude | codex | resolution |
|---|---|---|---|---|
| T1-1 | rotation | 0 | 90 | Codex right. Claude had not inspected PDF 20 in this pass and said so. The table is printed sideways. |
| F2-49 | curves | 9 | 10 | Codex right. Nine labeled curves and one unlabeled line ending near Df/D 0.95, ordinate 270 (PDF 110). Which test the unlabeled line belongs to is open; resolve from text at extraction. |
| F2-37 | curves | 10 | 11 | Unsettled. Claude wrote "about ten". At 250 dpi the dense group shows three 2-inch, four 4-inch and one 1-inch curve plus four in the 108 by 36 bin, with two curves labeled only "Dr approx 0.96". Count at 600 dpi during extraction; record 11 provisionally with credit to Codex for the closer look. |
| F2-57 | curves | 3 | 4 | Convention. Codex counts the two boundaries of the "range of unused soil" band as two traces; Claude counted the band as one. Adopt Codex's convention (each drawn line is a trace) and record band membership in `trace_classes`. |
| F2-58 | curves | 5 | 6 | Same convention as F2-57. |

Two further catches by Codex that Claude missed or read differently, both confirmed:

1. **Table 1-1 versus Table 2-3, soil 4 unit weight.** Table 1-1 (PDF 20) prints 50.5 pcf; Table
   2-3 (PDF 41) and `data/materials/materials.csv` carry 50.6. All other unit weights and moduli in
   Table 1-1 match the materials table. Record as a source inconsistency on the materials row, not
   an extraction error; Table 2-3 stays canonical because it is the Section II source table.
2. **LPT 27 state conflict.** Figure 2-29 (PDF 80) captions LPT 27 as "RS Dense" with "Plate
   Compactor" in the inset; Figure 2-43 (PDF 103) plots the same LPT 27 as curve B under "RS
   Intermediate". Claude noted the shared experiment but not the conflicting state labels. The
   experiment row for LPT 27 must carry both labels with status `conflict` until the text or Vol II
   settles it.
3. **"SS Drag Tests" in Figure 2-60.** Claude called the caption a probable error (soil is RS).
   Codex's reading is better: "SS" here means subscale (the subscale drag tests are numbered SSD
   in Figure 2-56), not silica sand. Both agree the soil is RS. Adopt Codex's reading in the
   glossary: SS = silica sand in soil designations, SS or SSD = subscale drag in test numbering.

## 2. Convention differences (not disagreements; settle the vocabulary once)

1. **Units.** Codex copied the printed spelling ("Lbs.", "In.", "G's", "Pounds/Ft.^3"); Claude
   normalized ("lb", "inch", "g", "lb/ft3"). Both are useful: the figures index should carry
   `x_unit_as_printed` and a normalized `x_unit` from a controlled list. Proposed list: inch, lb,
   psf, psi, pcf, g, s, mm, percent, deg, none.
2. **Dimensionless axes.** Codex wrote `normalized` for q/(D gamma), Df/D, Dr and percent axes;
   Claude wrote `linear` with unit `none`. Add `normalized` to the axis-type vocabulary for
   dimensionless axes drawn on a linear scale; it says more.
3. **Reciprocal density axes (F2-15, F2-17).** Claude wrote `reciprocal (1/gamma linear)`; Codex
   wrote `n/a` and explained why in notes. Add `reciprocal` to the vocabulary; Claude's reading
   stands.
4. **test_type for non-test figures.** Codex used `soil model`, `soil properties`, `grain size`,
   `bed preparation`; Claude used `other` and `apparatus`. Codex's finer labels are more useful
   for the question-answering index. Adopt: add `soil model`, `soil properties`, `grain size`,
   `bed preparation`, `density control` to the vocabulary, keep `apparatus` for equipment-only
   pages.
5. **data_form `mixed` (F2-32 to F2-35).** Codex marks load-penetration plots that carry a fitted
   straight line and bearing-capacity annotations as `mixed`; Claude as `curve` with
   `trace_classes` recorded-trace plus author-fit. Either is defensible; keep `curve` as data_form
   and let `trace_classes` carry the mixture, since every curve figure will have some mix.

## 3. Judgment disagreements (need Dan's rule)

### in_scope (23 rows differ)

Claude: in scope means the page carries numbers to extract (data, dimensions, or a setup fact).
Codex: in scope means the page is worth transcribing into the corpus, including photographs of
equipment, flowcharts and conceptual sketches, because the question-answering use needs them.

Rows Codex has in and Claude has out: F2-5, F2-6, F2-7 (conceptual charts), F2-8 to F2-11
(sieve equipment and worksheets), F2-16 (density apparatus), F2-19 (shear photo), F2-24
(conceptual), F2-25 (hypothetical envelopes), F2-26, F2-28, F2-30 (LPT equipment photos), F2-59,
F2-62, F2-64, F2-65 (density scoop, vacuum system, hammer, roller photos). Claude in, Codex out:
T2-1 (estimated lunar soil properties; Claude keeps it as the design target for the soil
selection, Codex excludes it as not a measurement). Maybe versus yes: T2-2, F2-15, F2-31, F2-63.

Recommendation: two columns instead of one. `in_scope` stays Claude's narrow meaning (numbers to
extract into `data/`), and a new `transcribe` column (yes for every page in Section II, since the
transcription phase covers the whole section anyway) carries Codex's meaning. Under that split
there is no remaining disagreement except the F2-37 count.

### priority (30 rows differ)

Claude assigned priority 1 to every load-penetration record, the DPT figures and the DPT
schematic (30 rows); Codex kept priority 1 for 23 rows and moved the rate series (F2-40 to
F2-43), the bin-size figure F2-44, the 18 by 36 bin figure F2-35, the crowded F2-37, the DPT
correlation F2-52 and the DPT schematic F2-53 to priority 2, while raising F2-12 (sieve
worksheet) and F2-13 to 1 and T1-1 to 1. Codex also gives priority 2 to equipment photographs
that Claude put at 3.

Recommendation: priority 1 = needed for the first calibration and prediction protocols (shear
family, LPT records with known bed state, DPT signatures and correlation, materials tables);
priority 2 = needed to set up or interpret those tests (bed preparation, boundary effects, rate
series, bin size, degradation); priority 3 = context only. By that rule the rate series and bin
figures are 2 (Codex right), the DPT correlation and schematic are 1 (Claude right, every Gp in
the LPT figures needs them), F2-12 and F2-13 are 2, T1-1 is 2 (duplicate of T2-3).

### mcc_relevant (23 rows differ)

Claude flagged 7 rows: direct evidence of history dependence or compaction (F2-17, F2-18,
F2-55 to F2-58, F2-60). Codex flagged 30, including every density and materials table, the
shear figures, the crushing hypothesis, the static stepped test and the equipment used to
densify beds. Codex's own notes say most of these "do not establish that MCC alone will explain
the changes" and that F2-23 "does not by itself identify loading-history dependence".

Recommendation: keep the narrow meaning. The column exists to answer one question in the plan,
whether any test demands a history-dependent model. Flag only figures that show the same
material at different states or after different loading histories where the response differs:
F2-18 (compaction duration), F2-56 to F2-58 and F2-60 (degradation and densification across the
campaign), F2-17 and F2-55 (state-to-index maps needed to read those). Add F2-21's dilation
panel as `maybe` (dilatancy is state-dependent but mu(I) with a dilatancy term may cover it).
Everything else stays `no`.

## 4. Audit sample of agreed cells (student)

Rows where both agents agreed on everything compared: F2-14, F2-21, F2-22, F2-27, F2-32, F2-33,
F2-36, F2-38, F2-39, F2-45 to F2-48, F2-50, F2-54, F2-56. Suggested audit (10 percent): F2-21
(panels and curve count 14), F2-36 (6 curves), F2-45 (2 curves, rotation 90), F2-54 (3 traces,
rotation 90), F2-14 (log x axis). Check each against the rendered page.

## 5. Credit

Codex: T1-1 rotation, soil 4 unit weight discrepancy, F2-49 unlabeled tenth line, LPT 27 state
conflict, "SS means subscale" reading of F2-60, finer test_type vocabulary, exposing F2-21's
displacement multiplier and subscript in the row itself. Claude: reciprocal axis type for F2-15
and F2-17, bed preparation numbers per soil attached to F2-65, F2-34 multiplier argued from
F2-48 (same LPT 87), shared-experiment links across LPT figures, narrow and testable
`mcc_relevant`.
