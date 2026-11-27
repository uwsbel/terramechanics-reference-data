# Review of batch pages-appc-b2: Appendix C, PDF 138 to 159 (printed C-24 to C-45/C-46)

Date: 2026-10-08. Reviewer: Claude (page re-reads of both differences). No human audit yet.

## What was transcribed

The second half of Appendix C of AM-68-1 Vol. II: 14 computer-plotted failure envelopes (C-24 to
C-37; one soil and state each, with the fitted average density, friction angle, tangent and
cohesion printed above the plot), 7 friction-angle-against-relative-density charts (C-38 to
C-44, one soil each) and the combined chart C-45/C-46. Printed C-33 to C-35 are bound out of
order (PDF 147 is C-35, 148 is C-34, 149 is C-33); both agents used the printed numbers. Codex
(gpt-6-astra, high, 4 minutes) and Claude (typed while Codex ran, before opening its files)
followed the figure-block layout fixed after batch 1.

## Diff results (`diff.md`)

| result | pages |
|---|---|
| agreed | 20 |
| resolved | 2 (C-35, C-37) |
| pending | 0 |

Every fitted value on the 14 envelopes (56 numbers: densities, friction angles, tangents,
cohesions), every soil heading, caption and axis label agreed except two damaged digits.

## Decisions (`decisions.csv`)

1. **C-35 (SS Loose), cohesion: unresolved, both readings kept.** The character before 1.87 is a
   full-height 1 overstruck with a mid-height horizontal bar. Codex read a minus sign (-1.87),
   Claude a second 1 (11.87). The 4x crop supports neither over the other; the canonical page
   carries "-1.87 (or 11.87 ...)" with the doubt marker. Audit candidate. Either value is a small
   cohesion for a loose sand whose envelope passes near the origin, so the record for that fit
   should carry an interval rather than a number.
2. **C-37 (LSM Dense), cohesion 213.76 (Codex) against 213.26 (Claude): Codex.** The damaged
   tenths digit shows a top bar and a descending stroke, a 7. Codex's reading keeps its doubt
   marker.

Canonical pages were written from Codex's reading (`--canonical-from b`), as in batch 1.

## Findings

1. With the block layout fixed, the two readings of 22 figure pages differed only where the print
   is damaged. The figure-page comparison (caption, numbers, symbols) reported exactly those two
   spots and nothing else.
2. Codex transcribed the friction-angle symbol as `$φ_{DS}$` (both letters in the subscript), the
   canonical form; Claude wrote `$φ_DS$`. Not flagged by the tool (same Greek letter, no number);
   worth a line in rule 4: multi-letter subscripts in braces.
3. Codex left `legend:` empty on pages with no printed legend key and described the single
   marker style in the description; Claude wrote a parenthetical in `legend:`. Codex's choice is
   the cleaner reading of rule 9 and is what the canonical pages carry.
4. **Printed values worth carrying to the records:** C-36 (LSM Loose) prints a negative cohesion,
   -109.97, from the computer fit; C-35's cohesion is unresolved (decision 1); C-37's tenths digit
   is damaged. The fitted friction angles on C-24 to C-37 differ from the hand-drawn envelope
   angles of C-2 to C-21 for the same series (for example RS loose 38.63 computed against the
   hand-drawn values on C-2), which the figures index should relate as derived-from pairs.
5. Time: Codex 4 minutes; Claude about 25 minutes of typing in four passes; review 20 minutes.
   Appendix C (45 pages) took about four hours in all, as the roadmap estimated.

## Credit

Codex: the 213.76 reading, the braces in `$φ_{DS}$`, the empty-legend convention, the complete
page-number reconciliation against the scrambled map. Claude: catching the overstruck character
on C-35 as unresolvable rather than accepting either reading. Agreement is agreement between two
agents, not confirmation.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The two damaged cohesion values (C-35, C-37); the 56 fitted values on C-24 to C-37 read in full
against the scans (about 20 minutes); the curve labels on C-45/C-46.
