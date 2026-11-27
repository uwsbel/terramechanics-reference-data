# Review of batch pages-vol2-ab-b3: Volume II Appendix A, PDF 49 to 72 (printed A-48 to A-71)

Date: 2026-10-08. Reviewer: Claude (page re-reads and glyph measurements on the scan). No human
audit yet.

## What was transcribed

The end of soil No. 6 (the RC2 friction angle chart and special comments), the three silica sand
specifications (soils No. 7, 8 and 9: SS loose, intermediate and dense) with their chemical
tables, photomicrographs, grain size, density and friction angle charts, and the first page of
soil No. 10 (LSM intermediate). Codex (gpt-6-astra, high) and Claude worked blind from the same
images.

Hints available to each agent: Claude's helpers carried the forms settled in the batch 1 and
batch 2 reviews (numbered items as paragraphs, typewriter digits in formulas, "230°F" without a
space). Codex's prompt predates both reviews. Neither agent saw the other's reading of these
pages.

## Diff results (`diff.md`)

| result | pages |
|---|---|
| agreed | 9 |
| resolved | 15 |
| pending | 0 |

Every printed number agreed: the three silica sand tables (99.9%, 0.1%, four traces), the
grain size parameters (0.42 mm, 0.28 mm, 1.5, 0.6 mm with their ranges), the density chart end
labels (95.4, 95.8 and 110.5, 112.7, 114.9 pcf), the Volcalite rows on PDF 72, and the values in
the text (Dr about zero, 0.53 and 0.69; 29.8°, 36.8° and 39°; 10,000, 18,000 and 24,000 psi; 8
and 24 roller passes).

## Decisions (`decisions.csv`)

1. **Claude was right** on three points:
   - **Figure A-24 is printed "Eigure"**, like Figure A-15 in batch 2. The first letter has a
     full lower bar, unlike Figure A-28 on PDF 56 in the same type. Codex read "Figure".
   - **The silica formula on PDF 51 has a lowered i** ("$S_i0_2$"), as on PDF 11 in batch 1. Codex
     normalized it to SiO2.
   - **"to unavoidable" has no hyphen.** Codex read "to-unavoidable" and marked it `[sic]`. The mark
     between the words is 8 px wide and 3 px tall, inside a 21 px word gap. Typed hyphens on the
     same page are 18 to 20 px wide and 7 px tall. It is a speck.
2. **Marks at the baseline are scan artifacts.** Codex kept short low marks after "Comments",
   after "7.", after "(silica).", after "clay." and after the table values 25.04 and 18.25, each
   with `[?]`. All sit at the baseline (the mark after 18.25 spans rows 3936 to 3939, the digits
   3900 to 3939), where underline remnants fall, and hyphens on these pages sit at mid x-height.
   Rule 10 drops them.
3. **Batch 1 rules applied** again: numbered items as paragraphs, digit zeros in formulas, source
   addresses as one paragraph.
4. **Density and grain size charts are written from Codex's reading, here and in batches 1 and 2.**
   Rule 9 puts text printed outside the plot frame in the body. Codex did that with the density
   end labels and the ASEE classification strip. Claude folded both into the `legend` line, which
   the rule reserves for series keys. The figure-page diff compares numbers and captions, not
   layout, so the difference never showed as a disagreement. The 18 chart pages of batches 1 to 3
   now carry page decisions taking Codex's layout, with two fixes recorded on them: Codex's chart
   title "GRAIN SIZE ANALYSIS CURVES - LM SMS" was a Markdown heading on six pages and is now plain
   text, and the "2 5" cell on PDF 47 keeps Claude's `[?]`. Credit Codex.
5. Codex's notes flag damaged print that both agents read the same way: "(Ca0)" on PDF 65 with the
   opening "(C" lost, "angle" on PDF 67 with central strokes bleached, the first zero of
   "0.58-0.62mm" on PDF 68, and "Maximum Density" on PDF 69 under a white defect. The canonical
   pages keep Codex's `[?]` where its reading was used (PDF 68 and 69) and the plain word
   elsewhere, since the row label or sentence fixes the reading.

## Things worth carrying to the data (feeds roadmap step 3d)

More disagreements between Appendix A and Volume I Table 2-3 (printed 2-16, PDF 41):

| soil | quantity | Appendix A | Table 2-3 |
|---|---|---|---|
| 7, SS loose | friction angle | about 29.8° (A-52, PDF 53) | 29° |
| 7, 8, 9, SS | coefficient of uniformity | 1.5 (Figures A-26, A-30, A-34) | 1.3 |
| 7, 8, 9, SS | coarseness | 0.6 mm, range 0.58-0.62 mm | 0.52 mm |

The friction angles of soils 8 and 9 (36.8° and 39°), the relative densities (0.53 and 0.69) and
the three moduli match the table.

By Claude's arithmetic on the average line of Figure A-27 ($γ_{min}$ 95.4, $γ_{max}$ 112.7 pcf),
the table's unit weights of soils 8 and 9 (104 and 107 pcf) give relative densities of 0.54 and
0.71, close to the stated 0.53 and 0.69. Soil 7's 94.7 pcf lies below every minimum density on
the chart (95.0 to 95.8 pcf), a relative density of about -0.05. "Loose" sand was placed slightly
looser than the chart's minimum-density test produced.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The "Eigure" captions on A-30 and A-48; the lowered i on A-50 (PDF 51); the mark between "to" and
"unavoidable" on A-49; one density chart in its new layout against the scan.
