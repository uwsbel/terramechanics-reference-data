# Review packet: materials batch 1 (Table 2-3)

Source: Bendix AM-68-1 Vol. I, Table 2-3 "Test Soils and Properties", printed page 2-16, PDF
page 41. Page image: `corpus/1968/images/p0041.png` (300 dpi, rotated 90 degrees clockwise so the
table reads upright; regenerate with `python tools/render_pages.py
nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf corpus/1968/images --pages 41 --dpi 300
--rotate 90`).

Two independent readings (Claude; Codex gpt-6-astra): 192 cells compared, 187 identical, all 144
numeric cells identical. Full report: `diff-report.md`.

## Items for the reviewer

Write your decision in the `confirmed` column of `confirmed.csv` (same folder), one row per item,
and leave a note if the scan does not support a single value.

| item | soil_no | column | reading A (Claude) | reading B (Codex) | why it is here | what to check on the scan |
|---|---|---|---|---|---|---|
| 1 | 1 | percent_passing_200 | <3% | <3% | Both agents read the same value but both flagged the glyph before "3%" as damaged. Codex notes "<5%" cannot be excluded; Claude notes "<.3%" is possible. | Zoom on row 1, column "% -200". Decide between "<3%", "<5%", "<.3%", or record an interval. |
| 2 | 7 | description_verbatim | White Silica Sand (Wedron 4040 narrowly graded) | White Silica Sand (Wedron 4040-narrowly graded) | Hyphen at a printed line break; resolved by rule to "Wedron 4040-narrowly graded". | Is there a printed hyphen after 4040? Confirm or correct the rule's result. |
| 3 | 8 | description_verbatim | same as item 2 | same as item 2 | same | same |
| 4 | 9 | description_verbatim | same as item 2 | same as item 2 | same | same |
| 5 | 10 | description_verbatim | Mixture of RC and Air-Floated Clay | Mixture of RC and Air- Floated Clay | Space after a hyphen at a line break; resolved by rule to "Air-Floated". | Confirm "Air-Floated" is one hyphenated word in print. |
| 6 | 11 | description_verbatim | same as item 5 | same as item 5 | same | same |

## Audit sample (agreed cells to spot-check)

Pick any three rows and check every numeric cell against the scan. Suggested: rows 4, 9 and 12
(they have the most digits). Record the result in `confirmed.csv` with item ids `audit-4`,
`audit-9`, `audit-12` and `confirmed` = `ok` or the corrected value.
