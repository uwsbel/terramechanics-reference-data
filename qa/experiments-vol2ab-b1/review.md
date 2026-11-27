# Review of batch experiments-vol2ab-b1: experiment rows for Volume II Appendices A and B

Date: 2026-10-15. Both agents read Appendices A and B (PDF 2 to 114) blind from the page images, the
page transcriptions, the figures index and the existing experiment index (for relations only);
neither opened `extractions/` or `qa/`. Codex: gpt-6.1-sol high, read-only. Claude: one subagent,
864 s, written outside the repository until both had finished (it looked at Volume II PDF 152 and 157
and Volume I PDF 41, 52 and 53 to decide relations). Prompt: `extractions/*/experiments-vol2ab-b1/prompt.md`.

## Result

Claude 36 rows, Codex 37; 32 ids agree: seven grain-size charts (averaged series), seven density
charts, seven friction-angle charts (derived from Appendix C's Figs. C-16 to C-22; FA-40 the same
band as FC-21) and eleven sonic modulus series of Appendix B. `data/experiments/index.csv` now stacks
the three batches: 324 rows, none pending.

## Decisions (with Codex, run `20261015-inventory-ab-decisions`; Claude's answers were written first)

1. **Chemical analyses** (Claude 4 rows with a new test type `chem`, Codex 5 with `gs`): excluded
   from the index (`row-decisions.csv`). Composition is material metadata, not a soil-mechanics test;
   it belongs with the soils in `data/materials/` (a composition table from the specification pages,
   with their reprints and typesetting slips, is open). Codex's position, adopted.
2. **soil_no of a chart printed under several specifications** (FA-2, 3, 4 under soils 1, 3, 4;
   FA-26, 27, 28 under 7, 8, 9; FA-38, 39, 40 under 10, 11): empty, status `unknown`, as for the
   Volume I averages; the specifications are in the evidence and notes. Both agreed on this answer.
3. **FA-47** (RSM-b density chart): `correlation`, `pending`. Its text (A-93, PDF 94) does not say
   the solid line averages several tests, as the other density charts' texts do; calling it an
   average was Claude's inference by analogy. Codex's reading, adopted.
4. **FB-5 dr_printed**: `o.84` as printed (a letter o for the zero); a `*_printed` column is literal.
   Codex's reading, adopted; the note gives 0.84.
5. **Density-chart unit weights**: `41.3 to 52.9` and so on, the index's normalized range (Claude's
   spelling; Codex wrote `41.3;52.9`).

## Findings the inventories raise (to check, not yet settled)

1. Table 2-3 of Volume I (PDF 41) prints RS mean size 1.8 mm and D95 2.7 mm, the PS values, against
   2.2 and 2.8 mm on Fig. A-2 (PDF 7) (Claude's inventory).
2. Volume I Fig. 2-14 (PDF 52): the arrows labelled PS and RSM-a may be swapped; the PS-labelled curve
   crosses 50 percent near 2.4 mm, the RSM-a D50 of Fig. A-18, and the other near 1.8 mm, the PS D50
   of Fig. A-6 (Claude's inventory, read at page scale; the same-as links follow the family names).
3. The text's friction angles of soil 11 (about 38.3 degrees, A-84, PDF 85) and soil 12 (about 37,
   A-93, PDF 94) disagree with the charts (the FA-44 band of 40 to 45; FA-48 about 48 at Dr .75) and
   with Table 2-3 (42 and 48).
4. FA-40 and FA-44 draw the LSM band over Dr 0 to 1.0; the text limits it to Dr .40 to 1.00.
5. FB-7 keys only the Dr 1.04 symbol; which circles are Dr 0.995 and which 0.77 is inferred from the
   lines they lie on (both inventories and both curve readings agree on the inference).
