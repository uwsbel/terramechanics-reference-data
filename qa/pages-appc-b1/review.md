# Review of batch pages-appc-b1: Appendix C, PDF 115 to 137 (printed C-1 to C-23)

Date: 2026-10-08. Reviewer: Claude (page re-reads of every difference). No human audit yet.

## What was transcribed

The first 23 pages of Appendix C of AM-68-1 Vol. II: the appendix text page (C-1) and 22 figure
pages: 7 failure-envelope plots, 13 direct shear data sheets (shear stress and dilation against
shear displacement, legend table of normal stress and unit weight per test) and the two RSM-b
sheets printed rotated in psi (C-22, C-23). Both agents worked from the 300 dpi images, the
page-map rows and the agreed figures index; Codex (gpt-6-astra, high, 20 minutes) and Claude
(typed while Codex ran, before opening its files) did not see each other's text.

## Diff results (`diff.md`)

First run, text comparison as for prose pages: 23 pages pending, 153 "number" differences.
Almost all were layout, not reading: Claude had folded the soil heading, tick ranges and long
descriptions into the figure block, Codex had kept the heading as body text and the block to
caption, axis labels, symbol-value legend pairs and one sentence. The tool now compares figure
pages on what is printed (caption tokens, the multiset of numbers outside axis and description
lines, the Greek symbols) and ignores phrasing. Second run:

| result | pages |
|---|---|
| agreed | 19 |
| resolved | 4 (C-1 header, C-3, C-16, C-21) |
| pending | 0 |

Every legend-table value (about 130 numbers), every density range, every friction angle label
and every caption word agreed except the four items below. Both agents independently read the
same printing slips: tau for sigma or gamma in two legend heads (C-8, C-10), gamma for delta on
one dilation axis (C-7), tau for sigma on one (C-16), a missing gamma before the equals sign on
C-20, 741 instead of 734 on C-14, 1961 and 714 on C-19, 3814 and 147 on C-20, 36.9° and MM-65-2
on C-15, "Normal Shear Stress" in the caption of C-21, "LSM Soil Dense" in the caption of C-19.

## Decisions (`decisions.csv`)

1. **C-16 heading, 97.3 (Codex) against 97.6 (Claude): Codex.** The heading prints 95.2 to 97.3;
   the legend row for 2934 psf prints 97.6. Claude copied the legend value into the heading. The
   two printed values disagree with each other on the page, which the record for that test must
   say.
2. **C-3 and C-16 caption mark, "= [sic]" (Codex) against "-" (Claude): Codex.** Two strokes of
   unequal length where the other sheets print a clean hyphen. Rule 10: transcribe the odd mark
   as it stands. Audit candidates; a person may well call them hyphens with a speck.
3. **C-1 header, `sections: ["C"]`: Codex.** Rule 9 clarified.
4. **C-21 caption, Claude's `[sic]` after "Normal Shear Stress": dropped.** The caption is the
   same either way; the oddity is noted here.

Canonical pages were written from Codex's reading (`--canonical-from b`) because its block layout
is the one the protocol now prescribes; the content agreed.

## Findings about the protocol and the tool

1. **Figure pages need their own comparison.** Prose alignment of figure blocks reports every
   phrasing choice as a difference. `tools/diff_pages.py` now detects figure blocks and compares
   captions, numbers and symbols; descriptions are free text.
2. **The block layout had to be fixed.** Rule 9 now shows the exact shape (headings as body text,
   `axes` without tick ranges, `legend` as symbol-value pairs, one-sentence description) and says
   the unnumbered appendix title goes in `sections`. Codex's layout was adopted.
3. **Two sheets are a different kind of figure.** C-22 and C-23 (RSM-b) are rotated, in psi, with
   no dilation panel, no drawn curves and no soil heading; their legend heads carry units only.
   The experiment index should mark them as a separate series.
4. **Printed inconsistencies worth carrying to the records:** the heading-versus-legend unit
   weight on C-16; the 3814 against 3815 and 147 psf lowest normal stress on C-20; the 741 on
   C-14; the 1961 and 714 on C-19; the fourth series reads 1468 instead of 1760 on C-5; the C-19
   caption names the soil and state instead of the standard title.
5. Time: Codex 20 minutes for 23 pages; Claude about 40 minutes of typing in four passes; the
   tool work and review about an hour.

## Credit

Codex: the 97.3 reading, the two-stroke caption marks, the appendix letter in `sections`, the
block layout now in the protocol, the observation that the C-2 axis labels print without their
Greek letters, and a careful misprint inventory. Claude: the figure-aware comparison and the
protocol fixes. Agreement is agreement between two agents, not confirmation.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The two caption marks (C-3, C-16); the C-16 heading value; the five legend tables with printing
slips (C-7, C-8, C-10, C-16, C-20) read in full against the scan; one envelope page (C-15) in full.
