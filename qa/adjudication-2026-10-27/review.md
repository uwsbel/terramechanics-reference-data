# Re-check of the audit wave 1 points the reviewers disputed (2026-10-27)

Dan asked for the points the student reviewers marked as a problem, split on, or could not tell to be
re-checked on the scans. The 158 such points of wave 1 (flagged by both 40, split 73, cannot tell by
both 12, a single review saying problem 31; after R2-C was accepted) went to a blind two-round
adjudication (D-023): a Claude adjudicator (subagents) and a Codex adjudicator (gpt-6.1-sol, high), each
from the same packet, neither seeing the reviews, the other's answers, or which reading is kept.

## Packet

`scripts/make_audit_recheck.py` builds one item per point: compare rows as two marks under neutral labels
P and Q (shuffled per item, `key.csv`), with the other reading's pixels taken from its own re-derived
submission rather than the global map the student packets used (D-027 deferred item); symbol and curve
rows as the kept reading with its box. 156 items; 2 points were left out because the other reading's
trace does not reach their x (FC-2C/1/n2200/trace/claude/26, FC-2C/1/n734/trace/claude/1). The
2935 psf series is matched through `series-ids.csv` (submitted as n2995).

## Rounds

Round 1 (`round1/`): agreement on 84 of 156. 41 of the 72 splits were trace samples where Claude said
the other reading is on the line and Codex said neither: the line stops at a symbol, and Claude's
adjudicators bridged the gap. The round 1 brief had not quoted the project's settled gap rule; that was
the brief's omission. Round 2 (`round2/`, `scripts/make_round2.py`) gave the 72 split items to fresh
adjudicators with the conventions of the 2026-10-15 adjudication quoted (no bridging; a sample in a
dash/symbol gap or on a symbol's outline is off the line; triangle center between centroid and box
middle) and a straight-line 3 px tolerance with `cannot tell` when the center's own uncertainty
decides: agreement on 58 of 72.

## Result (`final-decisions.csv`, `scripts/finalize.py`)

| decision | points | meaning |
|---|---|---|
| keep | 73 | the kept reading is on the ink |
| switch | 11 | the other reading is on the ink and the kept one is not (all 11 kept readings were Claude's) |
| off-ink trace | 48 | a trace sample neither reading has on the line's own ink (dash/symbol gap or symbol outline) |
| outside box | 2 | a kept symbol center 1 px outside its error box |
| unresolved | 8 | both adjudicators cannot tell (symbols merged with grid lines or other symbols) |
| split | 14 | still disagree after two rounds; nearly all one answer against `cannot tell` within 1 px |

Against the reviewers: of the 40 points both reviewers flagged, the kept reading was wrong on 33
(27 off-ink trace samples, 6 switches), right on 5, outside its box on 1, still split on 1. Several of
the 5 are triangles where one reading is at the centroid and the other at the box middle, both valid
for the data (CURVE-READING.md 8) while the student guide names only the box middle.

Switches change the value by 0.4 to 6 percent on traces (largest FC-1B n587, +63 psf) and by 8.7
percent on one dilation symbol (FC-1B/2/n1760/marker 5, 16.1 to 14.7 mil).

## Not yet done

1. Applying the decisions to the canonical points and `data/` (roadmap 4c, merge step): take the other
   reading on the 11 switches, drop the 48 off-ink trace samples, widen the bounds of the 10 outside-box
   and unresolved points.
2. The off-ink trace samples are a systematic effect, not 48 isolated errors: both readers sampled the
   dashed curves through the gaps at their symbols. A rule in the reconciliation (exclude trace samples
   inside a symbol's footprint or a dash/symbol gap) would catch the ones outside the audit sample.
3. Item 131 (FC-2C/2/n1468/marker 6): Claude's round 2 adjudicator reads the symbol at the kept point as
   the 2200 psf triangle in a merged stack, not the 1468 psf circle; Codex could not tell. To be looked
   at with the stack's neighbours.
4. The student guide's symbol center (box middle) differs from the data's triangle convention (centroid,
   bound including the box middle); compare rows on triangles where the readings sit at the two valid
   centers should not be sampled, or the guide should accept both.

## Applied (2026-10-27, D-030)

Dan approved applying the re-check. `scripts/write_decisions.py` wrote 21 decision rows into the batches'
decision files (3 earlier rows updated in place, their notes kept): the 11 switches (`use` the other
reader) and the 10 widened bounds (new `use span` in tools/diff_curves.py: the value stays, its bounds
take in the other reading; 8 `pending-review`, 2 `resolved`). curves-pilot-b1 and curves-appc-b1 were
re-reconciled (the committed canonical files reproduce byte for byte without the new rows) and their
records rebuilt: 21 observation rows changed, nothing else.

The 48 off-ink exclusions are held. A dry run showed that excluding a kept sample opens a break, and the
other reader's samples inside it (3 to 5 per break, at the symbol) enter as one-sided: about 180
unverified points where the adjudicators found the other line off the ink too. They wait for the
off-ink rule (D-031), which judges both readings. The dry run also turned up an earlier decision this
re-check overturns: FC-1B n2345 Codex trace 67 (u 1949) was resolved for Codex in the pilot review as
part of a group following the curved stroke, but past the square the only ink is the stray straight
stroke; its neighbours past the square probably share this.
