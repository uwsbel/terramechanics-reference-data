# Review of batch pages-vol2-ab-b2: Volume II Appendix A, PDF 25 to 48 (printed A-24 to A-47)

Date: 2026-10-08. Reviewer: Claude (page re-reads and glyph measurements on the scan). No human
audit yet.

## What was transcribed

The end of soil No. 3 (placement and special comments) and the specifications of soils No. 4 (RS
dense), No. 5 (RSM-a loose) and No. 6 (RC2 loose): numbered specification items, three chemical
tables, two normative mineral tables, three photomicrographs, three grain size charts with their
parameter tables, three density charts and two friction angle charts (the RC2 friction chart,
Figure A-24, falls in batch 3). Codex (gpt-6-astra, high) and Claude worked blind from the same
images.

Hints available to each agent: Claude typed the pages with helpers that carry the forms settled in
the batch 1 review (numbered items as paragraphs, typewriter digits in formulas, starred notes as
footnotes). Codex's prompt was written before batch 1 was reviewed, so it did not have those
rulings; that is why it again wrote numbered items as headings and normalized the formulas.
Neither agent saw the other's reading of these pages.

## Diff results (`diff.md`)

| result | pages |
|---|---|
| agreed | 10 |
| resolved | 14 |
| pending | 0 |

Every number agreed: the three Volcalite tables (each sums to the printed 99.25), the mineral
percentages, the grain size parameters with their ranges, the density chart end labels (RS 40.1,
41.3, 42.5 and 51.8, 52.9, 54.0 pcf; RSM 57.3, 57.9, 58.5 and 65.1, 70.3, 75.5 pcf; RC2 53.6,
61.4, 69.2 and 71.2, 83.1, 94.0 pcf) and the values stated in the text (16 roller passes for soil
No. 4, Dr about 0.8, 47.9°, 10,900 psi, 37°, an estimated 7800 psi, 43°, 8000 psi).

## Decisions (`decisions.csv`)

1. **Batch 1 rules applied.** Numbered specification items stay list paragraphs. Formula zeros
   are digits: re-measured on PDF 35, the zero of "(Ca0)" is 24 px wide against 34 px for the
   capital O of "Oxide" on the same line. "(Na0)" keeps the `[sic]` both agents gave it. A source
   address printed on two lines stays one paragraph.
2. **Codex was right** on two points:
   - **"230°F" has no typed space.** Measured on PDF 29, 38 and 46, the gap after the degree sign is
     12 to 14 px, against 5 to 8 px between letters and 23 to 27 px between words. The gap is the
     width of the degree glyph. Claude typed a space, and in batch 1 Claude's re-read of PDF 6
     accepted the space without measuring. That batch 1 decision is revised, and PDF 6 is
     regenerated with "230°F", matching PDF 12 and 21.
   - **The caption of Figure A-15 prints "Eigure".** On PDF 31 the first letter has a full lower
     bar, unlike "Figure A-19" and "Figure A-23" in the same type. It is kept as printed with
     `[sic]`.
3. **Claude was right** on "crystaline" on printed A-34. Codex corrected the spelling to
   "crystalline". It is kept as printed with `[sic]`.
4. **Kept with doubt: the RC2 coefficient of uniformity.** Figure A-22 prints the average as
   "2 5", with a gap and no decimal point. Both agents read the two digits. Claude marked the cell
   `[?]`. Codex kept "2 5" without a marker but flagged it in its notes. Neither reading of it
   fits the printed range of 15-25: 2.5 lies outside it, and 25 is its upper end, which an
   average of six samples could reach only if all six were 25. Volume I Table 2-3 gives 17.0
   (see below).
5. Codex marked "California[?]" on PDF 43, where the middle letters are erased. The surviving
   letters and the same address on the other sheets leave no doubt, so the canonical page has no
   marker.

## Findings about the tool

`tools/diff_pages.py` writes a figure page whole from one reading. It applied typed-text decisions
to such a page, but it ignored a decision that picked the other agent's reading of one cell. The
"Eigure" decision on PDF 31 was recorded and then dropped. The tool now swaps the chosen reading in.
Every earlier batch was regenerated into a scratch folder with the patched tool: all 158 canonical
pages came out identical. No earlier decision had been lost.

## Things worth carrying to the data (feeds roadmap step 3d)

Appendix A and Volume I Table 2-3 (printed 2-16, PDF 41) disagree on several soil properties:

| soil | quantity | Appendix A | Table 2-3 |
|---|---|---|---|
| 3, RS intermediate | friction angle | about 43.9° (A-20, PDF 21) | 44.5° |
| 4, RS dense | friction angle | about 47.9° (A-28, PDF 29) | 47.3° |
| 1, 3, 4, RS | mean size, coarseness | $D_{50}$ 2.2 mm, $D_{95}$ 2.8 mm (Figures A-2, A-10, A-14) | 1.8 mm, 2.7 mm |
| 2, PS | coefficient of uniformity | 1.6 (Figure A-6) | 1.7 |
| 6, RC2 | coefficient of uniformity | "2 5", range 15-25 (Figure A-22) | 17.0 |
| 6, RC2 | coarseness | 5.0 mm, range 4.1-5.5 mm (Figure A-22) | 4.7 mm |

Table 2-3 prints the same gradation for rows 1 to 4 (1.8, 1.7, under 3%, 2.7). Appendix A gives
different values for RS and PS, and the PS values match the table's mean size and coarseness. For
RSM-a and RC2 the table's mean size equals the Appendix A $D_{50}$. The pages cannot settle which
source is right. The Appendix A charts are the measured curves, so reading $D_{50}$, $D_{60}$,
$D_{10}$ and $D_{95}$ off them in step 3b will check both sources directly.

One more check, by Claude's arithmetic, not printed: on the average line of Figure A-15
($γ_{min}$ 41.3, $γ_{max}$ 52.9 pcf), the Table 2-3 unit weight of soil 4, 50.6 pcf, corresponds
to a relative density of 0.84, not the stated 0.80. That is inside the dashed 95 percent band,
whose two lines give 0.75 and 0.92. The same check on soils 1, 3, 5 and 6 agrees with the table
within 0.03.

Correction to the batch 1 review: it said the friction angles in the text match Table 2-3 except
for soil No. 1. Soil No. 3 does not match either (43.9° against 44.5°). The batch 1 review now
carries that correction.

## Correction (2026-10-08, from the batch 3 review)

The density and grain size chart pages (PDF 30, 31, 39, 40, 47, 48) are now written from Codex's
reading, which follows rule 9 (end labels and the classification strip as body text). The "2 5"
cell keeps Claude's `[?]`. See `qa/pages-vol2-ab-b3/review.md`, decision 4. Credit Codex.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The "2 5" cell on A-46; the caption on A-30; the 47.9° on A-28 against Table 2-3; one of the
"230°F" lines.
