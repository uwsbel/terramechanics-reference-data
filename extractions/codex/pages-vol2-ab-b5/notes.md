# Transcription notes

Read directly from the 17 supplied page images, with Pillow crops/enlargements for uncertain characters. No OCR, network source, or other transcription was used. All 17 page transcriptions were read through against their images. All pages are upright (rotation 0).

## Printed page labels versus the map

- p0098: the image prints `A-97/A-98`; the map says `unknown`. Used the printed label. This page is the end of Appendix A, although the batch primarily covers Appendix B.
- p0101: the map says `i`, but no printed page number is visible on the title page. Used `unknown` rather than supplying an inferred number.
- p0102: the image prints `ii`; the map says `1`. Used `ii`.
- p0104: the image prints Arabic `1`; the map says lowercase `l`. Used `1`.
- p0099 and p0100 have no visible printed page number; retained `unknown`.
- p0103 and p0105-p0114 agree with the supplied page-map rows.

## Uncertain readings and unusual print

- p0098, heading: `Special. Comments [sic]`. Enlargement shows a small separate baseline dot after `Special`; retained it as a period.
- p0099, opening sentence: `modulus_of [sic]`. Enlarged the short horizontal mark between the words; it lies at the baseline and spans the intervening space. Retained it as an underscore rather than silently replacing it with a space or a hyphen.
- p0099, opening sentence: `scils[?]`. Enlargement shows an open, c-shaped second letter in the word following `test`. Transcribed the visible shape; it might be a damaged `o` in `soils`.
- p0101, recipient address: `South, Bend, Indiana [sic]`. Enlargement confirms the comma immediately after `South`; retained it.
- p0111, FB-5 dense label: `o.84 [sic]`. Enlarged the label; the first character is a small lowercase `o`, shorter than the adjacent digits. Retained it rather than substituting numeral `0`.
- p0111, FB-5 loose label: `0.26[?]`. Enlargement resolves the final digits as `26`, but the leading character is only an upper arc and the decimal point is lost. The complete numeric reading remains uncertain.
- p0100, `P.O. No. 5800191M`: enlarged and retained `O` despite a break at its lower right edge.
- p0104, footnotes: enlarged and confirmed `Strauss`, `Selig, E. T.`, `91`, `SM3`, `4332`, `1965`, and `19-49`.
- p0113, FB-7: enlarged and confirmed the labels `1.04`, `0.995`, and `0.77`. Used `⧅` to represent the square with a descending diagonal printed immediately before the `1.04` label. The other labels have no separate legend symbol; nearby plotted markers were not converted into additional legend entries.
- Small baseline tails/streaks attached to characters (for example, after `for` on p0100 and after `values` and `soil` on p0105), faint dotted lines, underlining, border damage, and isolated specks were treated as scan/printing artifacts rather than extra punctuation.

There are two `[?]` markers and four `[sic]` markers in the page files, all listed above. No `[illegible]` markers were needed.

## Protocol applications

- The repeated `IIT RESEARCH INSTITUTE` bottom imprint was omitted as a report footer. The same wording in the title and foreword body was retained.
- The handwritten signatures on p0102 were not duplicated as printed text; the printed names and titles below them were transcribed.
- The table of contents on p0103 is represented as a Markdown table. It has no numbered table caption or supplied table locator, so `tables` remains empty. Dot leaders were treated as layout, not words or punctuation belonging to the titles.
- Alphabetic section headings A-D and the numbered heading 14 use level-one Markdown headings. Unnumbered title headings have no section entry; the Appendix B heading has `sections: [B]`.
- Footnote numbers on p0104 are represented by the printed superscript markers `¹` and `²`, repeated under `Footnotes:`.
- The photographs FB-1 and FB-2 use the required figure-block fields with `axes: none` and `legend: none`.
- Figure axes retain the printed labels and units; tick values and curve values are omitted. Direct series labels inside the plot frames are recorded in the legend field.
- The stacked fraction in the FB-8 vertical axis is represented linearly as `(1+ν)(1-2ν)/(1-ν)`; the numbered display equations retain fraction layout through LaTeX.
