# Transcription notes: pages-s2-b2

All 22 page files were read through against the supplied images, including a final visual review. Transcription is from the images; no OCR, network source, or other transcription was used. Crops and rotated reading copies are retained in this directory. All headers remain `review_status: single-reading`.

## Uncertain readings and illegible text

- p0048, Soil Type entry: `#8-1 [?]`. The digit after the damaged number sign looks like an 8 in the enlarged crop; 6 is also possible. The number-sign strokes are damaged too. See `p0048-test.png`.
- p0048, TOTAL - 200, weight retained: `62.3 [?]`. The last digit has lost most of its upper portion and visually resembles a 3. A damaged 6 is possible; the visible value is not silently corrected from the arithmetic. See `p0048-total.png`.
- p0049, paragraph f: `Figure [?]`, `The [?]` immediately after the parenthesis ending "example.)", `The [?]` following "linear scale.", and `below [?]` following "Also shown,". All four words are partly erased at the right edge. Surviving letters and sentence context support these readings. See `p0049-detail.png` and the whole-page image.
- p0051, first paragraph: `$ℓ$ [?]` and `$μ_S$ [?]` in the parentheses after `$D_{50}$* are damaged. The first appears to be a small italic ell; its top is missing. The second is mu with a subscript resembling capital S; lowercase s is possible. See `p0051-symbols.png`.
- p0066: `[illegible]` represents the small equipment nameplate below and to the right of the large C label, above the G label. Its lettering cannot be reliably separated after enlargement. The seven large component labels are legible. See `p0066-sign.png`.

## Printed peculiarities and resolved hesitations

- p0048: circled calculation references are represented by Unicode circled digits; the circled plus sign used for sieve selection is `⊕`. RC2 and Grams are circled in the form; their text is retained without adding explanatory words to the page transcription.
- p0048: the first sieve entry visibly reads `3 8"`, with no discernible slash. The next entry is `3`, not an inferred fractional size. Those visible forms are retained. See `p0048-sievefirst.png`.
- p0048: `11.80- [sic]` in the No. 8 row preserves a definite trailing typewriter hyphen. The enlarged cumulative value in the preceding row reads `20.68`; the retained weight there reads `77.7`. See `p0048-numbers.png`.
- p0048: the oven-drying footnote reads `110 C (230 F)`; no distinct degree marks could be seen, so none were supplied.
- p0051: `these-values [sic]` in the first paragraph and `The-values [sic]` before the example values preserve short horizontal marks at hyphen height. See `p0051-these-values.png` and `p0051-the-values.png`.
- p0051 and p0053: the printed word "interpolated" is retained, even where nearby prose says "extrapolation". No terminology was corrected.
- p0054: the uneven descending trace after the final equals sign in the gamma definition was treated as an extraneous mark, not a sequence of typed minus signs. See `p0054-gamma.png`.
- p0055: the parentheses around the discussion of relative density and reciprocal unit weight are retained as printed; no parenthesis was moved after "relative density".
- p0058: `(sensitivity: -0.01 lb.)` preserves the visible horizontal mark immediately before 0.01. See `p0058-sensitivity.png`.
- p0059: `Make-three [sic]` in the last body paragraph preserves a definite mid-height hyphen. The mark after "When" in the opening paragraph is low, like the many short underlining artifacts on these scans, and was omitted. See `p0059-make.png` and `p0059-when.png`.
- p0063: "adapted" is clearly printed and was retained. See `p0063-adapted.png`.
- p0064: the x-axis separator is a tilde, transcribed `Unit Weight ~ pcf`.
- p0068: both displacement labels visibly have sigma as the subscript: `$δ_σ$`. The shear-displacement label was not changed to tau. The second unit-weight legend entry reads `46.5`, not 46.6 or 46.8. See `p0068-axis.png` and `p0068-legend.png`. Short isolated strokes within the legend area align with broken grid lines or sit above the text and were treated as figure-line artifacts.
- p0070: the printed equation equates the angle expression with "slope of failure envelope"; the equation is preserved without mathematical correction. The reference reads "Figure C-1b".

The four `[sic]` markers in the page files are the trailing `11.80-`, `these-values`, `The-values`, and `Make-three` noted above. No other `[sic]` markers were added.

## Page numbers and rotation

The printed numbers on all images agree with the map's `inferred_label`. These differ from the map's `printed_label` entries:

| PDF page | Map printed_label | Number visible on image and used in header |
| --- | --- | --- |
| 50 | unknown | 2-25 |
| 56 | i | 2-31 |
| 58 | 9 | 2-33 |
| 59 | 1 | 2-34 |
| 64 | unknown | 2-39 |
| 69 | 4 | 2-44 |

Pages 50, 52, 64, 66, and 67 require a clockwise quarter-turn for the figure and caption and have `rotation: 90`. The other pages have `rotation: 0`.

## Protocol adaptations

- Figure 2-12 is a worksheet, not a plot. Its fields, calculations, and complete numeric table are transcribed as body text and a Markdown table, followed by the required F2-12 figure block. Its header has no invented table ID. Unnumbered calculations have no invented equation number.
- The ASEE classification bands under Figures 2-13 and 2-14 are represented by Markdown tables. The printed SAND cell spans three size columns; its text appears once, with the other two cells blank. No table IDs were invented.
- Plot tick labels and numerical curve-endpoint labels were not copied, following the prohibition on curve values. No curve was sampled. Headings, test-condition annotations, the compaction-duration guide text, the failure-envelope angle, and the apparent-cohesion label are body text outside the figure blocks.
- Schematic and photographic component labels are body text in approximate top-to-bottom reading order. Non-plot figures use `axes: none` and `legend: none`.
- Figure pages interrupt the running prose. Continuation markers follow the prose across those interruptions. Page 63 ends mid-sentence; its continuation falls outside this packet because PDF 65 is not supplied. Page 70 begins with continued symbol definitions and ends mid-sentence. No missing-page wording was invented.
