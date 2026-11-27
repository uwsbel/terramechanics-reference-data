# Transcription notes: pages-vol2-ab-b3

All 24 pages, p0049 through p0072, were read directly from the supplied images and the resulting page files were read through against those images. Enlarged and rotated reading copies are retained in this folder. No OCR or network source was used.

## Printed page numbers

The image's printed number was used in every header. These differ from `printed_label` in `page-map-rows.csv`:

| PDF page | Map printed_label | Printed number read from image |
| --- | --- | --- |
| 56 | 4 | A-55 |
| 60 | unknown | A-59 |
| 62 | unknown | A-61 |
| 63 | 50 | A-62 |
| 65 | unknown | A-64 |
| 69 | 9 | A-68 |
| 70 | unknown | A-69 |
| 72 | unknown | A-71 |

All printed numbers agree with the map's inferred labels.

## Uncertain readings and retained odd marks

- p0050, heading 14: `Special Comments- [?]`. An enlarged crop shows a short low horizontal mark immediately after `Comments`, above and separate from the long heading underline. Retained as a dash; uncertain whether it is a typed mark or a scan streak.
- p0050, paragraph: `to-unavoidable [sic]`. Enlargement shows a distinct mid-height hyphen between `to` and `unavoidable`; preserved rather than changing it to a space. This is the only `[sic]` in the page files.
- p0060, heading 7: `_ [?]` after `7.`. The isolated short mark lies at the baseline, unlike a normal mid-height hyphen. Retained as an underscore with doubt; it may be a stray underline fragment.
- p0060, first paragraph: `(silica).- [?]`. A short horizontal mark follows the period. Preserved as a doubtful dash; the enlargement does not establish whether it is print or a streak.
- p0065, chemical table, Calcium Oxide formula: `(CaO) [?]`. The opening parenthesis and most of the C are lost; `aO)` and a small upper remnant remain. The full reading is tentative, based on the visible remnants and row label.
- p0067, section 11, first sentence: `angle [?]`. Several central strokes are bleached out. The remaining letters support this reading, but the whole word is not cleanly legible.
- p0068, grain-size table, Coarseness range: `0.58-0.62mm [?]`. The first zero is broken on its right side and resembles a c in the enlargement. Read as zero with doubt. The digits 58 and 62 are legible.
- p0069, right vertical axis: `Maximum [?] Density [?]`. A white scan defect removes much of the end of the first word and the beginning of the second. `Max` and most of `ensity` survive. Both restored words are marked doubtful.
- p0072, description: `clay.- [?]`. A small low horizontal mark follows the period; retained as a doubtful dash.
- p0072, Aluminum Oxide row: `25.04- [?]` and `18.25- [?]`. All digits are readable in enlarged crops. Both numbers have low trailing horizontal marks. The first also has a dotted streak farther to its right. The short marks are preserved as doubtful dashes; the farther dotted streak is treated as an artifact.

There are no `[illegible]` entries in the page files.

## Other reading decisions

- p0050 says `with a soil bed`, not `within a soil bed`; retained as printed.
- p0051's table says `Ferric` and `Aluminum Oxide`; p0058 says `Ferric Oxide` and `Aluminum`; p0065 says `Ferric Oxide` and `Aluminum Oxide`. These differences were checked in enlarged crops and retained.
- p0053's prose gives `29.8°` and `10,000`; p0060 gives `0.53`, `36.8°`, and `18,000`; p0067 gives `0.69`, `39°`, and `24,000`. The prose readings were checked independently of the plotted curves.
- The Coefficient of Uniformity range cell contains four dashes on p0054, three on p0061, and four on p0068. Enlargements establish these differences. All inset table numbers were read from the respective images.
- The density-axis labels print `γ min` and `γ max` with baseline letters, not visibly lowered subscripts. These were retained as baseline text. The x-axis does visibly use the subscript in `$D_r$`.
- Long underlines, horizontal streaks through or below words, border damage, and marginal dark bars were omitted as scan artifacts or underlining. Isolated doubtful short marks are recorded above instead of silently discarded.

## Protocol accommodations

- The numbered specification items are treated as first-level headings, with their printed item numbers in `sections`. The protocol does not specify a heading depth for single-part numbers.
- The chemical analyses have no printed table number or separate table caption; their supplied `TA-pNNN` locator appears in the header. Empty Markdown header cells preserve the absence of printed column titles.
- Grain-size inset tables and classification strips are transcribed as Markdown tables outside the figure block. Their merged headers/cells are represented once, with empty cells for the remainder of each span. No new table IDs were invented.
- The grain-size plots have a second horizontal axis, recorded as `x2 U.S. Std. Sieve No.`. Numeric sieve ticks and all other axis ticks are omitted under the figure rule. No curve values were estimated.
- The density charts' five separately printed leader-line annotations outside the frame are included as body text. These are printed labels, not readings taken from curves; ordinary axis ticks are omitted.
- No separate line-key legend is printed on the plots, so their blocks use `legend: none`. The photomicrographs' printed `SS` identification is retained in the legend field; the scale statement remains outside the figure block.
- p0072 ends after two rows of the volcanic-cinder analysis and its footnote. Only those rows are present in this image. No continuation content from outside the packet was supplied, and no paragraph is visibly broken across this page boundary.
