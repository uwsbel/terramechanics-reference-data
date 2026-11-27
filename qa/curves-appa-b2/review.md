# Review of batch curves-appa-b2: Appendix A grain-size curves

Figs. A-2, A-6, A-18, A-22, A-26, A-38, A-46: percent finer against grain size on log paper, printed
sideways; an average curve (solid) and the range of several samples (two dashed curves) per chart.

## Readings

Both agents, blind, from evidence packets written by `tools/make_reading_packet.py` (page images,
figures-index rows, series list, protocol, tools). Codex: gpt-6.1-sol high, one run. Claude: one
subagent per chart; stopped by the account's usage limit on the evening of 2026-10-14 and resumed the
next morning in the same workspaces (`meta.json`). The first real use of the log axis of D-027: both
readers declared `--x-transform log10 --x-direction up --y-direction left` on every chart and gave the
printed grain sizes. The parameter table printed inside each frame lies over several grid lines;
detection followed a table rule instead of a grid line on several charts, and the readers refitted
those lines on the ink outside the table (each says how in its `notes.md`). `calibrate_axes.py recover`
is not safe on this paper: it returned the unlabelled 0.09 mm line for 0.1 mm and table rules for
percent lines (two readers found this independently).

The two maps agree within their line errors at every place compared on six charts and all but two
places on the seventh.

## Agreement and adjudication

First comparison: 942 of 991 matched points agreed. Over much of their length the three curves touch
or run together as one band on these 1-bit scans; the readers placed each curve from the band's edges
and middle, with widened bounds, and their samples differ there. Codex's reading also recorded 168
circles at the sieve sizes that Claude's readers mostly did not see. Two rounds of blind adjudication
(`qa/adjudication-2026-10-15/grain-size-round1`, `-round2`; the first in two halves per adjudicator)
under the conventions of the other batches, plus one more: a circle item is `yes` only when a printed
ring is centred at the mark. Of the circles both adjudicators confirmed 7 (three on A-2, three on A-22,
one on A-6) and excluded 53; 103 on which neither adjudicator saw a ring (most `cannot tell` inside the
merged band) were not asked again, as the same scan cannot settle them. Knee features are judgment on
broad bends: where one adjudicator named a reader's mark and the other said both marks are on the bend,
the named mark was taken (the rule already used for symbol centres; `scripts/apply_adjudication4.py`).

Final canonical points (now 1,203 after the off-ink rule, D-032, and the correction of `some`
answers, D-039: 871 agreed, 85 one-sided-verified, 40 resolved, 5 pending review, 202 one-sided; see
`canonical.csv`): at this review, 1,188 (921 agreed, 91 one-sided-verified, 40 resolved, 5 pending review, 131
one-sided: the 103 unconfirmed circles and 28 points split after the second round, mostly curve ends one
pixel either side of the 2 px rule and knees). Open points stay in the records with their status. With
every bound halved, 838 of 983 matched points agree, the lowest of any batch, as expected where three
curves share one band.

## Findings

`insights/1968-vol2-appendix-a-grain-size-curves-against-their-tables.md`: the drawn curves and the
printed tables agree to a few percent (D50 3 to 6 percent finer on A-2 and A-6, 4 percent coarser on
A-26); A-26's printed Cu (1.5) equals its D50 over D10, not D60 over D10 (1.67 from the curve); the
circles on the curves are few, and the unconfirmed ones are not sieve data.

## Records

`b68-gs-fa-2` to `b68-gs-fa-46` (the experiment rows of `experiments-vol2ab-b1`): grain size in m, percent
finer as a fraction (SI unit one); `series.json` records the log axis.
