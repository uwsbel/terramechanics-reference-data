# Blind adjudication of 2026-11-19 (LM model drops)

Curve batch `curves-s5-b1` (Figs. 5-24, 5-25, 5-31 and 5-32: footpad penetration and strut axial loads of NASA Tests
No. 1 and 2; review `qa/curves-s5-b1/review.md`). Each round: the brief, the items (`items.csv`, built by
`qa/adjudication-2026-11-19/scripts/make_disputes5.py` with `ADJ_FEATURE_ROLES=leading` and `ADJ_SEED` 20261123 for
round 1 and 20261124 for round 2; crops not kept), the answers of a Claude adjudicator (one subagent,
claude-opus-5-5, a fresh one each round) and a Codex adjudicator (gpt-6.2-sol high, workspace-write in its own copy of
the packet, a new session each round), the key, the splits and the Codex run's meta. Each adjudicator worked in its
own copy of the packet outside the repository and reports opening nothing else. Answers applied with
`qa/adjudication-2026-10-15/scripts/apply_adjudication4.py`; round 2 rows appended with
`qa/adjudication-2026-11-02/scripts/append_decisions.py`. `items.csv` and `key.csv` are the record of each round
(rerunning the builder reads the batch's current decisions and does not reproduce them).

The brief is that of 2026-11-19 (dynamic penetrometer) with the figure section rewritten for these four figures and
convention 5 stating that peaks and minima are of the signed value (on a compression panel the largest compression is
a minimum), the batch's convention (`qa/curves-s5-b1/feature-roles.csv`).

A first packet of 38 items was withdrawn minutes after it went out: it included ten runs (11 samples) of start and end
samples that duplicated the other reading's end within both bounds, which `end_dedup` (adopted for the batch then)
removes. Both adjudicators of that packet were stopped and their folders deleted; when they were stopped, the Codex
adjudicator's folder held no `answers.csv` (checked before deletion) and the Claude adjudicator had returned nothing.
No record of that packet is kept beyond this paragraph. Round 1 below is the rebuilt packet.

Round 1: 28 items (23 one-sided features, 3 disagreeing knees, 2 runs of start samples); 15 settled (15 decision
rows), 13 split. Twelve of the splits were extra features of Codex's reading (small crests, dips and gentle knees). In
eleven of them the Claude adjudicator measured the line (centerline excursions of 0.5 to 2 px, or corners 11 to 35 px
from the mark) and rejected the feature while the Codex adjudicator accepted it by eye; in one (item 001, a gentle
knee on Fig. 5-24) the Claude adjudicator measured a 5 degree turn 4 px from the mark and accepted it while the Codex
adjudicator rejected it. After round 1 a decision kept Claude's `first` feature on Fig. 5-31 at the pixel of Codex's
first trace sample that both adjudicators had placed inside the frame (item 017), on the ground that its bound reached
the line's ink; Codex's review of the batch showed that the 2 px rule applies to the mark itself, and both readers'
`first` features there were then excluded (`qa/curves-s5-b1/review.md`, "Ends of the lines").

Round 2: the 13 splits and Claude's first Fig. 5-31 sample, left without a partner by round 1 (14 items), with fresh
adjudicators and conventions 5 and 7 made measurable: a crest or dip counts only if the centerline moves back from
it by at least half the line's width on both sides (anything smaller is below a sample's own reading bound), and a
bend's corner is the meeting point of straight fits to the centerline on its two sides, each straight within 1 px
over at least 30 px. (The brief's "about 3 px on these figures" was meant as the half-width; both adjudicators measured
the widths, 4 to 6 px, and used half of them.) 9 settled (9 rows): all five crests and dips excluded by both
adjudicators, with measured retreats of 0.5 to 2 px on one side; two knees excluded; one knee verified (a 16 to 18
degree turn within 5 px of the mark); Claude's first sample verified on the line's ink. 5 split: three of Codex's knees
that the Claude adjudicator rejects (the line straight within 1 px through the mark, or the corner 9 px or more away)
and the Codex adjudicator accepts (corners 1 to 7 px from the mark; its comments give the fits' extents in v, which
are not their lengths along the stroke, so whether they meet the 30 px minimum is not shown either way), one knee one
adjudicator rejects and the other cannot tell, and the disagreeing knee of Fig. 5-32 panel 3, which neither
adjudicator gives to either mark (one puts the corner between them, the other finds two bends too close to define).
The split points keep their status and are mandatory rows of the student audit; no third round for five knees. The
measurable rules were applied to these 14 items only; the features settled in round 1 were judged under round 1's
rules.

After both rounds, Codex's three reviews of the batch led to a check of every start and end of every line on the page
(the review's "Ends of the lines"): seventeen decision rows written by hand, with the evidence in each note, one of them
replacing the Fig. 5-31 row above (exclusions and replacements of `first`, `last` and `peak` features and of end
samples inside a frame, two verifications of end samples by Codex's second review, and the widened time bound of Fig.
5-24's peak on its flat top).
