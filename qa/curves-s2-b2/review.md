# Review of batch curves-s2-b2: Section II load-penetration records (cylinder against footpad)

Figs. 2-45, 2-46, 2-47, 2-48 (Volume I, printed 2-80 to 2-83; PDF 106 to 109): load against penetration
for a four-inch cylinder and a four-inch footpad in the same soil bed, two recorded traces per figure,
one solid and one dotted or dashed. 2-45 and 2-48 are printed sideways, 2-46 and 2-47 upright. LPT 95
and 79 (RS loose), 98 and 89 (RS intermediate), 101 and 91 (RS dense), 87 and 85 (SS).

## Readings

Both agents, blind, from the evidence packet written by `tools/make_reading_packet.py`
(`qa/curves-s2-b2/batch.json`). Codex: gpt-6.1-sol high, one run, 2026-10-31 02:54. Claude: one
subagent per figure, started 2026-10-30 (claude-fable-5-1) before any Codex reading existed and
interrupted (F2-46 and F2-48 had points, F2-45 and F2-47 calibrations only); finished 2026-11-02 by
fresh subagents (claude-opus-5-5) in the same workspaces. **Hints available:** before launching them,
the orchestrating session had read the Codex run's final summary (counts per series, calibration
residuals and the ambiguities it listed); the briefs carried none of it, and each reader reports
opening nothing outside its workspace and the task (`extractions/claude/curves-s2-b2/meta.json`).
The F2-45 reader redid the whole reading (the earlier calibration box cut the frame); F2-47 reused
the calibration after a byte-identical rerun and redid the tracing; F2-46 and F2-48 checked the
earlier points on the page and finished them.

The packet's own description was wrong on one point: it said the two traces of Figure 2-47 cross near
0.5 in and again near 6 in. Both readers found one crossing, at about 1.3 in, and the dashed trace
ending against the solid one near 6 in; the readings follow the page.

## Calibration

The two maps agree within their line errors on F2-46, F2-47 and F2-48, and on F2-45 wherever both
hold a line. On F2-45 the load frame runs past the last printed label (250 lb): Claude's reader
anchored the unlabelled 275 lb line and the 300 lb frame by the even 25 lb spacing, Codex's map stops
at 250 lb; they differ by 0.30 lb at 300 lb. Claude's reading is canonical on all four figures (the
same lines, or more lines as close to the ink).

**The first inch of Figure 2-48.** Its 0 to 1 in interval is drawn about 233 px tall against 304 to
316 px for every other inch. Both readers read the grid as drawn (the bottom frame is 0 in), and the
two maps agree there within 0.12 px. If the zero line was meant to sit at the regular spacing, every
value below 1 in shifts by up to about 0.25 in; the page cannot say which. Listed in
`docs/OPEN-QUESTIONS.md`.

## Agreement and adjudication

First comparison: 266 of 283 matched points agreed (F2-45 63 of 67, F2-46 62 of 65, F2-47 65 of 71,
F2-48 76 of 80); 64 points were held by one reading only. The off-ink check (D-031) excluded nothing.
Blind adjudication with batch s2-b1 (`qa/adjudication-2026-11-02/`, two rounds). Codex's first trace
sample of every trace but one sat inside the frame line or the frame corner, beyond the last visible
ink, and both adjudicators excluded them under the frame rule; Claude's first samples, left without a
partner, were verified in round 2. For the first point of LPT 79 both round 2 adjudicators placed it
one dot beyond either reading (a dot partly merged with the solid trace near the origin), so neither
reading's point was kept; its trace samples carry the start. Knees that only one reader marked were
checked against a stated rule (round 2 brief, conventions 7 and 8: a visible bend within 8 px of the
mark); most were excluded as marks on straight runs or gradual bends. Two of Codex's LPT 95 end samples, inside the
top-left frame corner, were excluded the same way. What stays open: three knees only Codex marked
(LPT 95 at 1.8 and 4.8 in, LPT 98 at 3.3 in) and Codex's LPT 98 sample at 6 in on the right frame, the knee of LPT 91 at the onset of its steep step near 6.1 in, and three knees of the
second printing of LPT 87 (in no record).

Final canonical points: 317 (258 agreed, 37 one-sided-verified, 14 resolved, 6 one-sided, 2 pending
review). With every bound halved, 258 of 283 matched points agree.

## Records

`tools/build_batch_records.py curves-s2-b2`: seven records, `b68-lpt-079`, `-095`, `-089`, `-098`,
`-091`, `-101`, `-085` (269 points). LPT 87 on Fig. 2-48 is its second printing (first on Fig. 2-34,
batch curves-s2-b1, which holds the record): its row is left out of `series-map.csv`, so its 48 points
stay in `canonical.csv` as a cross-check and enter no record.

## Suggested audit sample

The 8 open points, the F2-48 points below 1 in, the F2-45 points above 250 lb, and the F2-47 samples
near the crossing at 1.3 in.
