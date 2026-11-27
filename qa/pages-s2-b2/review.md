# Review of batch pages-s2-b2: Volume I Section II, PDF 48 to 70 (printed 2-23 to 2-45, without 2-40)

Date: 2026-10-08. Reviewer: Claude (page re-reads of every blocking difference). No human audit yet.

## What was transcribed

22 pages: the grain size data sheet of Figure 2-12 and the sieving procedure, the grain size curves
(Figures 2-13, 2-14), the minimum-maximum density test with its equations and nomographs (Figures
2-15 to 2-18), the direct shear apparatus (Figures 2-19, 2-20), the direct shear data and failure
envelope of RS soil (Figures 2-21, 2-22) and the friction angle relation. Printed 2-40 (PDF 65) was
in the pilot batch. Codex (gpt-6-astra, high) and Claude worked from the same images without seeing
each other's text.

## Diff results (`diff.md`)

| result | pages |
|---|---|
| agreed | 10 |
| resolved | 12 |
| pending | 0 |

Every number on the 18 text and figure pages outside the data sheet agreed, including all values on
the Figure 2-12 sieve table except one damaged digit, the legend of Figure 2-21 (seven normal
stresses with unit weights) and the Figure 2-22 annotations. Most of the remaining differences were
equations written with LaTeX macros (Claude) or Unicode (Codex), which rule 5 allows.

## Decisions (`decisions.csv`)

1. **Codex was right** on the circled line references of the data sheet (①, ②, kept as printed;
   Claude used parentheses), the trailing mark in "11.80-", the space in "- #200", the mid-height
   marks in "these-values", "The-values" and "Make-three", the spaced dash in "gradation - a", and
   the raised mark before "0.01 lb." on printed 2-33 (transcribed as it stands, like "=-32.2" in
   batch 1).
2. **Claude was right** on the figure labels: the values printed beside the axes of Figure 2-15
   (64.0, 68.5, 78.0) and of Figure 2-17 (23.8 to 112.7 pcf, the average minimum and maximum
   densities of the six soils) belong in the transcription; Codex left those legends empty. The
   Figure 2-17 values feed the materials table and are an audit candidate.
3. **Unresolved, both readings kept:** the drag test number on the data sheet (#6-1 or #8-1, a
   damaged glyph) and the first symbol after $D_{50}$ on printed 2-26 (mu or ell, its top lost).
   The second symbol there is $μ_s$.

## Findings about the tool

1. On a figure page the canonical copy comes from one reading as a whole. A decision row
   `<page>,<page>-canonical,a|b,note` now picks the reading per page, and `replace: OLD => NEW` in
   its note records a substitution for a cell neither reading has right (used on the data sheet).
   Earlier batches regenerate byte for byte.
2. The circled digits on the data sheet are not digits to the number comparison (Unicode class No),
   so the tool reported Claude's parenthesized references as numbers present in one reading only.
   Harmless here; worth remembering on the next form-like page.

## Credit

Codex: the circled references, five printed marks Claude normalized away, the spaced dash. Claude:
the axis labels of Figures 2-15 and 2-17.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The Figure 2-17 end values against the scan; the two unresolved glyphs; the data sheet's
"TOTAL - 200" weight (62.3, both readers flagged its last digit).
