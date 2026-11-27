# Review of batch pages-s2-b1: Volume I Section II, PDF 26 to 47 (printed 2-1 to 2-22)

Date: 2026-10-08. Reviewer: Claude (page re-reads of every blocking difference). No human audit yet.

## What was transcribed

22 pages: the section opening and abbreviation list (2-1 to 2-3), the discussion of soil properties
affecting dynamic strength with the equations of motion (2-4 to 2-11), Table 2-1 (estimated lunar
soil properties, rotated), the soil selection text, Table 2-2 (potential test soils, 33 rows),
Table 2-3 (the twelve test soils), the flow chart of Figure 2-7, the grain size procedure and the
equipment photographs (2-18 to 2-22). Codex (gpt-6-astra, high) and Claude worked from the same 300
dpi images, page-map rows and figures-index rows, without seeing each other's text.

## Diff results (`diff.md`)

| result | pages |
|---|---|
| agreed word for word | 10 |
| resolved | 12 |
| pending | 0 |

Outside Table 2-2 the two readings agreed on every number. The blocking differences there were a
sign on printed 2-2, a capital against lowercase phi on 2-10 and 2-11, and the display equations
on 2-6 written with LaTeX macros (Claude) or Unicode (Codex), which rule 5 allows.

## Decisions (`decisions.csv`)

1. **Table 2-2 (printed 2-14) is the weak spot of the batch.** The page is a 200 dpi bilevel (CCITT)
   scan; in this table 5, 6 and 8 print as the same blob. Seven cells could not be settled from the
   image and carry both readings with `[?]`: the Salt-Fine density (40-85 or 40-65), the third
   CAB-O-SIL density (5 or 6), three volcanic cinder densities (60-65 or 50-65; 55-60 or 55-80;
   40-55 or 40-65), the supplier name (AGSCO or AASCO), the trade name ("ISO-Balls" or
   "ISO-Fills") and the last column head. The Foamglas strength was settled at 50 psi because its
   first digit is the same glyph both readers took as 5 in "5-15 psi". These numbers are the
   approximate densities of candidate materials that were not used, so none of them enters the
   data; they are audit candidates all the same.
2. **Codex was right** on the raised stroke in "earth =-32.2 fps²" (printed 2-2; transcribed as it
   stands, its meaning is not ours to decide), the hyphen in "Oblique-Impact" on the SSIMP line
   (2-3), the `[sic]` on "refers to in In-Place" (2-2), the table structure for the braced
   CAB-O-SIL and sugar-bonded rows, and the group head "Grain Size Parameters" in Table 2-3.
3. **Claude was right** on "terrestial [sic]" (2-7, Codex normalized the spelling), the lowercase
   phi in the force-displacement relation and its symbol list (2-10, 2-11), "Is Highly Vesicular",
   and the underline fragment in "perimeter-shear type" (2-13).
4. Short marks after cell text in Table 2-2 (after "Charcoal", "Chips", "Crushed",
   "Satisfactory") were omitted: on this scan they cannot be told from specks.

## Findings about the protocol and the tool

1. `tools/diff_pages.py` now treats a Markdown table's separator row as layout (`|---|` and
   `| --- |` are the same row) and keeps table row breaks as tokens so the canonical page keeps
   its table; the earlier canonical writer flattened tables into one line. The pilot and Appendix C
   canonical pages regenerate byte for byte under the change.
2. Lone Greek letters in prose: Codex wraps them in dollars, Claude leaves them plain. Both are
   allowed; the difference is classed as markup and does not block.
3. Codex marked more doubt (`[?]`) on damaged glyphs than Claude did; on this scan quality that is
   the better habit.

## Credit

Codex: the sign on 2-2, the SSIMP hyphen, the In-Place slip, the table structures, a careful
inventory of doubtful glyphs in Table 2-2 and Table 2-3. Claude: "terrestial", the phi case, two
underline fragments, the tool fixes.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The seven unresolved Table 2-2 cells (with the warning that the scan may not settle them either);
Table 2-3 read in full against the scan (it feeds `data/materials/`); the "=-32.2" on 2-2.
