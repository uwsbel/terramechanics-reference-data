# Review of batch pages-vol2-ab-b4: Volume II Appendix A, PDF 73 to 97 (printed A-72 to A-96)

Date: 2026-10-08. Reviewer: Claude (page re-reads and glyph measurements on the scan). No human
audit yet.

## What was transcribed

The rest of soil No. 10 (LSM intermediate), soil No. 11 (LSM dense) and soil No. 12 (RSM-b dense):
the Volcalite and clay chemical tables, normative mineral tables, three photomicrographs, three
grain size charts, three density charts and three friction angle charts. Codex (gpt-6-astra,
high) and Claude worked blind from the same images.

Hints available to each agent: Claude's helpers carried the forms settled in the reviews of
batches 1 to 3, including the rule 9 chart layout. Codex's prompt predates those reviews. Neither
agent saw the other's reading of these pages.

## Diff results (`diff.md`)

| result | pages |
|---|---|
| agreed | 13 |
| resolved | 12 |
| pending | 0 |

Every number agreed, including the two misprinted Volcalite tables described below, the clay
analyses, the LSM and RSM-b grain size parameters, the density chart end labels (66.6, 67.8, 69.0
and 88.1, 90.2, 92.3 pcf for LSM; 73.5, 74.4, 75.3 and 89.4 pcf for RSM-b) and the values in the
text.

## Decisions (`decisions.csv`)

1. **Codex was right** that a bare φ in prose takes no dollars. Rule 4 puts only subscripted
   symbols in math, and every Volume I page writes φ bare. Four cells on PDF 80 and 89.
2. **Claude was right** on spacing and specks:
   - "(e.g.,magnetite" on PDF 74 has no space after the comma.
   - "Cinders-", "Marble-" and "Cinders-Volcalite" on PDF 90 have no spaces around the hyphen.
   - Three dots Codex kept as periods (after "cinders" on PDF 81, after "Albite" on PDF 83, before
     "(Continued)" on PDF 91) measure 3 x 3, 6 x 6 and 7 x 3 px. A typed period in the same type
     is 10 x 12 px. They are specks.
   - "175-177" on PDF 94 is a hyphen. A pixel dump shows a mid-height bar with a baseline streak
     fused to the foot of the 5 below it. Codex flagged it as possibly an equals sign.
3. **Both flagged the same damaged digit** in the page reference on PDF 90 ("456-466", one digit
   uncertain on the bilevel scan). The canonical keeps Claude's marker on the first number.
4. **Not compared by the tool, checked by eye.** On the three density charts Codex wrote
   $γ_{min}$ and $γ_{max}$ as subscripts, unlike its own batches 1 to 3. The labels print "γ min"
   on the baseline, and the canonical pages keep that form.
5. Batch 1 rules applied as before: numbered items as paragraphs, digit zeros in formulas.

## Things worth carrying to the data (feeds roadmap step 3d)

1. **The two reprints of the Volcalite analysis are wrong, and the first printing is right.** The
   first printing (A-2, PDF 3) sums to its printed 99.25. On A-72 (PDF 73) the calcium oxide row
   carries the magnesium values (5.58, 4.07) and there is no magnesium row. On A-81 (PDF 82) the
   magnesium row carries the sodium values (1.61, 3.29) and there is no sodium row. With the
   silica and alumina rows of the page before, the printed Volcalite columns sum to 91.14 and
   93.67, yet both reprints still print the total 99.25.
2. **The two printings of the clay analysis differ in iron oxide.** A-72 prints 1.1% and A-81
   prints 1.2%. With 1.1% the column sums to the printed total of 100.0%. With 1.2% it sums to
   100.1%. The first printing is the consistent one.
3. **Friction angles in the text disagree with the charts beside them**, as the insights note
   already records for Table 2-3. Soil No. 11's text gives about 38.3° (A-84), while its own
   special conditions (A-88) and Figure A-44 give a band of 40° to 45°. Soil No. 12's text gives
   about 37° (A-93) at Dr 0.75, while Figure A-48 rises from about 38° at Dr 0 to about 51° at
   Dr 1.0.
4. **The densities agree.** By Claude's arithmetic on the average lines of Figures A-39 and A-47,
   the Table 2-3 unit weights give relative densities of 0.50 (soil 10, 77.5 pcf), 0.70 (soil 11,
   82 pcf) and 0.74 (soil 12, 85 pcf), against the stated 0.5, 0.70 and 0.75.
5. **Mix proportions, needed to rebuild a bed**: LSM is RC2 cinders and kaolin-type clay 1:1 by
   weight (A-73, A-82). RSM-b is cinders and crushed marble 1:3 by weight (A-90). RSM-a is 5:7
   (A-34, batch 2).

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The calcium and magnesium rows on A-72 and A-81 against A-2; the two iron oxide values; the dot
after "Albite" on A-82; the "175-177" on A-93.
