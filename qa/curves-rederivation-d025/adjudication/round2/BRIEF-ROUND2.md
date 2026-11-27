# Second round: items the first two adjudicators split

Read `BRIEF.md` first (the figures, the files, the blindness rules, the answer vocabulary per kind);
everything there still applies. This round has only the items on which two independent first-round
adjudicators disagreed: `items-round2.csv`, with both of their answers and comments (`answer_1`,
`comment_1`, `answer_2`, `comment_2`; who they are does not matter). Where only some samples of a run
are still in question, the `focus` column names them.

For each item, look at the crop and the page yourself, weigh the two comments as evidence (they may
point at something you would have missed, or be wrong), and give the answer the ink supports, in the
brief's vocabulary. For a run, answer for the samples in question only: `all yes`, `all no`, or
`some` with the off-line ones listed by pixel. When the ink cannot settle it, `cannot tell` is the
right answer: the item then goes to a person.

Conventions both first-round adjudicators were unsure about, settled for this round:
1. A trace sample counts as on the line when it is on the line's ink or within 2 px of it at the
   line's height. A sample on a symbol's outline, or in the white gap between a dash and a symbol,
   is off the line, even if its height is close.
2. The first or last point of a drawn line is where its ink starts or ends. When the line runs
   into a plotted symbol without a white gap, the point is the symbol's center; when a white gap
   separates the line's end from the symbol, it is the end of the ink.
3. For an identity item, `both` means two separate symbols are printed there (name them in the
   comment); a white pocket enclosed by the strokes of neighbouring symbols is not a symbol.
4. The white-gap rule in 1 is for samples placed across a gap. A sample within 2 px of the line's
   own ink, including 1 or 2 px beyond the end of a dash, is on the line unless it sits on a
   symbol's outline.
5. Where a line runs into an axis (its ink merges with the axis stroke), the line continues into the
   stroke: a first or last sample inside the axis stroke and within 2 px of the line's band extended
   into it is on the line, as a line running into a symbol ends at the symbol's center.
6. When neither mark is the point asked about (`neither`), say in the comment where it is (page
   pixels), as the first round did.

Write `answers-round2.csv` (`item,answer,confidence,comment`), one row per item, none skipped.
