# Review of batch curves-s5-b1: LM model drops, NASA Tests No. 1 and 2 (Figs. 5-24, 5-25, 5-31, 5-32; D-050 roadmap step 6f)

Four figures of Volume I, Section V, all printed sideways, record two drops of the 1/6-scale Lunar Module model onto
loose RS soil (the detail correlation drops of Section 5.5.4, printed 5-44, PDF 324; Table 5-T3, printed 5-45, PDF
325): NASA Test No. 1 (Bendix drop 10, a vertical drop, Vv -114.93 in./sec. in the Fig. 5-25 inset) and NASA Test No.
2 (drop 11, Vv -60.55 and Vh 83.75 in./sec. in the Fig. 5-32 inset, 83.5 in Table 5-T3). Figs. 5-24 (printed 5-49,
PDF 329) and 5-31 (printed 5-56, PDF 336): the No. 1 footpad's penetration depth against time, one line each. Figs.
5-25 (printed 5-50, PDF 330) and 5-32 (printed 5-57, PDF 337): the axial loads of struts No. 3, 2 and 1 against time,
three panels sharing the time axis, one line each. The penetration depth is a computed output: the report's data
reduction program took the 13 tape-recorded signals every 1/1000 s and calculated the footpad's penetration by
numerical integration (Section 5.5.2, printed 5-41, PDF 321).

## Readings

Both agents, blind, from the evidence packet written by `tools/make_reading_packet.py` (`qa/curves-s5-b1/batch.json`),
2026-11-19. Codex: gpt-6.2-sol high, one run for the four figures (745 s). Claude: one subagent (claude-opus-5-5) per
figure, writing outside the repository until Codex had finished. **Hints available:** the batch description named
the panels, the sign convention of the printed labels, and the label slips a first look at the pages had shown
(`-60` above `+40` on a tension panel, a damaged `.09`), with the instruction to anchor such a line from the panel's
own sequence and report it. Points submitted (trace / feature), panels in figure order: Claude F5-24 37/5, F5-25
42/6, 40/7, 58/6, F5-31 36/6, F5-32 34/9, 35/6, 36/6; Codex F5-24 38/6, F5-25 44/12, 41/8, 59/10, F5-31 36/6, F5-32
35/11, 37/12, 34/7. Codex's notes (`notes.md`) contain a few en dashes; the submissions are kept as written, as in the
earlier batches, and none reaches `data/`.

Both readers found the same labels as printed: on both Strut No. 2 panels the top load label is printed `-60` (a
minus with no vertical stroke) above `+40`, and both anchored that line at +60 from the panel's sequence and its
(Tension) title; the `.09` time label is damaged on both strut figures and anchored from the sequence on its drawn
line. On Fig. 5-32 the `.10` time line is a 3 px speck that neither reader could anchor (Claude's was rejected by the
ink check, Codex flagged it), so every time past 0.09 s on that figure is extrapolated; the three strut traces end at
about 0.103 s. Both read the Fig. 5-32 inset as Vh = 83.75 in./sec., against 83.5 in Table 5-T3. These notes are on
the record pages.

## Calibration

Penetration figures: all 11 time and 7 depth lines detected and verified by both readers (affine residuals 0.06
percent of the time span and 0.1 percent of the depth span). Codex's reading also anchors each figure's unlabeled
left frame by the grid spacing (7.0 in on Fig. 5-24, 5.5 in on Fig. 5-31; the Claude readers saw the frames and left
them out). Those lines make Codex's reading canonical by the rule (its lines include Claude's and more, as close to
the ink); no value uses them (both traces stay below 4.5 in), and the two maps differ at the data by at most 0.000016 s
and 0.002 in.

Strut figures: the time lines are drawn only in part (ticks or dashes at the right frame, dots inside the panels), so
both readers anchored them where they are drawn and carried them across the panels; the load lines are drawn and
verified. On Fig. 5-25 the two maps differ at the canonical trace samples by up to 0.00013 s, within the samples' time
bounds (about 0.0002 s). On Fig. 5-32 they differ at the 0.02 s line by up to 0.419 ms in panel 1 and 0.271 ms in
panel 2 at the canonical (Claude's) trace samples, 0.433 and 0.276 ms over both readings' samples, about twice the
bounds; elsewhere the median difference is 0.00001 s. Both readers anchored that line only on its 80 px tick at the
right frame, Claude with the panel's common tilt and Codex with its own fit to the tick. The line's surviving dots
inside the panels, in panel 2 (u 1718 px) and panel 3 (u 1853 and 2022 to 2091 px), read 0.01999 to 0.02004 s on
Claude's map and 0.01974 to 0.01996 s on Codex's, Codex's departing further from 0.0200 s the farther the dot lies
from the tick; panel 1 has no dot of that line, and the evidence there is the trend. Claude's map is named canonical
for panels 1 and 2 (`overlays.csv`, with the measurement); it was canonical there already, by the tie rule.
`calibration-sensitivity.md`: piecewise and affine values differ by at most 0.27 lbf and 0.0003 s; its two large
secant changes (+44 percent on Fig. 5-32 Strut No. 3, -8.1 percent on Fig. 5-25 Strut No. 3) are ratios of near-zero
slopes (a trace starting near 0 lbf, a trace ending at 0.7 lbf).

## Comparison rules for this batch

1. **Feature roles by the signed value.** The brief's rule 3 names a local maximum of the value a peak. On a
   compression panel that makes the largest compression a minimum. Codex and the Claude reader of Fig. 5-25 followed
   it; the Claude reader of Fig. 5-32 named the extremes of its two compression panels by the curve as drawn, which
   reverses them. `feature-roles.csv` renames those ten features for the comparison (a new input of
   `tools/reconcile_curves.py`, checked against the submissions before anything is written; the rederived note reads
   `<role> (role renamed by ...; submitted note: <the note verbatim>)`, so a phrase of the submitted note such as
   "t of the minimum ill defined" now sits inside the quoted note of a feature renamed a peak; the submission is not
   touched; `docs/DATA-ORGANIZATION.md`).
2. Features are paired by their role (`feature_roles` leading): first, last and peak each in their own group, knees
   and minima together in one group.
3. `max_gap` 0.0075 s (the sampling rule's 0.005 s steps, with room for a sample moved off a grid line). Without it,
   Codex's 0.005 s steps on Fig. 5-25 panel 3 read as drawn gaps against its denser 5 lb samples, and 11 of Claude's
   samples there went unmatched.
4. `end_dedup` yes: 11 of Codex's start and end samples, in ten runs, duplicated the canonical reading's own within
   both bounds (`tools/diff_curves.py --end-dedup`, opt-in since curves-s2-b4).

## Agreement and adjudication

Before adjudication 365 of 368 matched points agreed within the sum of their bounds; the three disagreements were
knees. 635 of the 642 trace samples passed the automated ink check; the other 7 sit where the line merges with the
frame or runs along a grid line and are marked for review, none excluded by the check.

Two blind rounds (`qa/adjudication-2026-11-19-mdrop/`, README there). Round 1 (28 items): 15 settled, 13 split. Round
2 (14 items, fresh adjudicators, conventions made measurable: a crest or dip counts only if the centerline moves back
from it by at least half the line's width on both sides; a corner is where straight fits on its two sides meet): 9
settled, including all five crests and dips excluded on measured retreats of 0.5 to 2 px; 5 split (four of Codex's
knees and the disagreeing knee of Fig. 5-32 panel 3, which neither adjudicator gives to either mark). The split points
keep their status and are mandatory rows of the student audit. The new rules were applied to the split items only.

## Ends of the lines (after Codex's reviews)

Codex's reviews found ends of lines that sit inside a frame, which the rounds had not all asked about. Every start and
end of every panel was then drawn on the page with both readings' samples and features, the line's own ink told apart
from the frame (the automated ink check counts a row of a frame's edge as line ink, so it cannot decide at a corner),
and convention 2 applied: a mark more than 2 px past the line's last ink is off the line (decision rows in
`decisions-F5-24-p1.csv`, `-F5-25-p2.csv`, `-F5-31-p1.csv`, `-F5-32-p1.csv`, `-F5-32-p3.csv`, each citing the review
and the crop).

1. Fig. 5-24, end: Codex's last trace sample and `last` feature are 3 px inside the top frame; the sample is excluded,
   the feature replaced by Claude's at the frame's near edge, and Claude's last trace sample is one-sided-verified
   (item 7 below).
2. Fig. 5-31, start: both readers' `first` features are inside the bottom frame, 5 px past the line's ink, where both
   adjudicators put Codex's first trace sample (round 1 item 017); both excluded. (A first decision had kept Claude's
   `first` there because its widened bound reached the ink; the review showed that the 2 px rule applies to the mark,
   and the dynamic penetrometer round of 2026-11-19 had excluded co-located points the same way.) The line starts at
   Claude's first trace sample, verified in round 2.
3. Fig. 5-31, end: Codex's last trace sample and `last` feature and Claude's `last` feature are 3 to 4 px inside the top
   frame; all excluded. The line ends at Claude's last trace sample, on the ink 5 px below the frame, verified on the
   page by Codex's second review (the stroke distinguishable to about v 1080). The `peak` features at this end: item 6.
4. Fig. 5-32 panel 3, start: Claude's `first` feature sits on the bottom frame past the end of the trace's ink; it is
   replaced by Codex's, where the ink ends (both adjudicators verified Codex's first trace sample there, round 1 item
   028).
5. Figs. 5-25 panel 2 and 5-32 panel 1, starts (Codex's second review): Codex's first trace sample and `first` feature
   are about 3 px inside the bottom frame, past the line's last distinguishable stroke. The published points are
   Claude's, at the frame's near edge, but Codex's marks still made them `agreed`; they are excluded, and Claude's
   start sample and `first` are now one-sided. Fig. 5-32 panel 2's start is at the cutoff (Codex's mark at v 3499,
   the stroke followable to about v 3497, 2 px) and is left as it is.
6. Fig. 5-31, the `peak` (Codex's second review): the line is level within a pixel from about 0.0976 s to the end of the
   record, so neither reader's `peak` is a local maximum by the batch's round 2 rule (the line must fall back from a
   crest on both sides); a peak time there would be a locator on a plateau, not an observation. Both `peak` features
   are excluded, and the record page reports the record's largest retained sample (106.9 mm at 99.6 ms, the record's
   last sample; the stroke goes on about 5 px to the frame). Fig. 5-24's flat top, from about 0.078 to 0.082 s with the
   line falling after it, is a peak; the canonical mark (Codex's, 81.3 ms) carried a time bound of 0.2 ms, and after
   Codex's third review a `span` decision widens it to 3 ms to take in Claude's reading of the flat top (and the depth
   bound to 0.026 in, rounded up so that it covers Claude's): the height is the observation, the time a locator.
7. Fig. 5-24's last trace sample of Claude's is verified on the page by Codex's second review (on the distinct stroke at
   the frame's near edge).

## Breaks in the drawn lines

Three short breaks, where the drawn line has no ink for about 4 px along the stroke and resumes (one about 1.5 px to
the side), seen by the Claude readers and Codex's review and measured on the page: Fig. 5-25 panel 3 at about 0.0138 to
0.0140 s, Fig. 5-32 panel 1 at about 0.0089 to 0.0091 s and panel 3 at about 0.0261 to 0.0263 s. They are in
`breaks.csv` with the two ends of each gap in pixels (`gap_u1` to `gap_v2`), so the records carry them (`series.json`
`breaks`), the plots lift the pen there and the record pages name them.

The comparison honors them too (`docs/DATA-ORGANIZATION.md`). A first version of this review kept the comparison as it
was; Codex's second review showed that two of Claude's samples on Fig. 5-32 panel 3 agreed only through Codex's line
drawn straight over 4.5 ms across the break. A second version cut every step of Codex's reading that overlapped the
gap, located in time on Claude's map; Codex's third review showed that this misplaced the gap on Codex's map and cut
samples that a Codex sample on the same side, within the bounds, supports. Now the gap's pixel ends are mapped on each
reading's own calibration, the other reading is never interpolated across it, and a sample beside it is compared
directly with the other reading's end sample on the sample's own side of the break, within both bounds, as at a
trace's end (`tools/diff_curves.py --break-a`, `--break-b`; Codex's fourth review found that a first version could take
the end sample on the far side; `tools/tests/test_breaks.py`). One of Claude's samples, Fig. 5-32 panel 3 sample 18, has no such
support and is one-sided; everything else beside the breaks agrees. The rule leaves batch curves-s4-b1 unchanged once
its two dropouts carry their measured pixels (that batch's review says so).

## Records

`tools/build_batch_records.py curves-s5-b1`: `b68-mdrop-10` (NASA Test No. 1, 207 points: 196 agreed, 4
one-sided-verified, 3 resolved, 4 one-sided) and `b68-mdrop-11` (NASA Test No. 2, 170 points: 156 agreed, 6
one-sided-verified, 2 resolved, 5 one-sided, 1 pending review), each with four panels from two figures: panel 1 the
footpad penetration depth (m), panels 2 to 4 the axial loads of struts No. 3, 2 and 1 (N), all against time (s). Signs
as printed: tension positive, compression negative. In all 377 points; the 10 open ones (four split knees and one
pending knee, four start points and one sample beside a break) are mandatory rows of the student audit. 41 decision
rows: 24 from the two adjudication rounds, 17 written by hand after Codex's three reviews, each with its evidence. Setup incomplete (index rows; the fill depth of the loose beds is not printed).

| | NASA Test No. 1 | NASA Test No. 2 |
|---|---|---|
| peak footpad penetration | 4.43 in (112.6 mm) at 0.080 s; 4.33 in at 0.100 s | 4.21 in (106.9 mm), level from about 0.098 s to the last retained sample at 0.0996 s |
| Strut No. 3 | tension, up to 52.8 lbf (235 N) at 0.059 s | compression, to -26.6 lbf (-118 N) at 0.095 s |
| Strut No. 2 | tension, up to 47.6 lbf (212 N) at 0.060 s | tension, 50.5 lbf (225 N) at the end, 0.103 s |
| Strut No. 1 | compression, to -87.3 lbf (-388 N) at 0.069 s | compression, to -60.5 lbf (-269 N) at 0.072 s |

The record pages' setup tables give the soil's average friction angle at this density (40 deg, Table 2-3) and, from
Codex's review, a row each for the bed's own friction angle and the touchdown velocities printed in Table 5-T3 (41 deg
for both beds in the Claude reader's notes of batch `experiments-s3s5-b1`; -60.5 and 83.5 in./sec. for Test No. 2 in
both readers' notes), marked not yet extracted: those values were never read into a field by two readers, and a single
reading does not enter `data/`. `docs/OPEN-QUESTIONS.md` item 22.

## Observation for users of the data (not a reading issue)

Both Claude readers noted, and the reconciled values confirm, that the early penetration rate differs from the
vertical velocity in Table 5-T3: about 96 to 100 in/s over the first 0.01 s against 114.9 in/s for NASA Test No. 1,
and about 66 to 70 in/s against 60.5 in/s for NASA Test No. 2. The table's velocities "were calculated based on the
exact time interval between the instant of model release to the instant of ground contact" (Section 5.5.4, printed
5-44, PDF 324): the model's velocity at contact, computed from the free fall. The plotted penetration is the footpad's,
computed by the data reduction program from the recorded signals (Section 5.5.2, printed 5-41, PDF 321), and its
early rate is an average over a finite interval. The two need not be equal; the pages do not say more. Nothing in the
data is adjusted for this.

## Remaining in step 6f

Table 5-T1 (the model's scale factors, PDF 281) is indexed as setup evidence and not transcribed into a record;
Table 5-T3 (the eight detail correlation drops: bed state, friction angle, velocities) is cited on the index rows but
its friction angle and velocities are not fields (item 22); the other histories of the two drops (footpad velocity and
heading, CG motion, pitch; Figs. 5-22, 5-23, 5-26 to 5-30, 5-33 to 5-39) are indexed on the index rows and not read.

## Afterwards (2026-11-20): Table 5-T3 read, and a correction

Table 5-T3 was read by two blind readers (batch `tables-s5-b1`, `qa/tables-s5-b1/review.md`); all 64 printed values
agree. Its drops are the records `b68-mdrop-t5-3-rs` and `b68-mdrop-t5-3-ss`, and the setup tables of `b68-mdrop-10` and
`b68-mdrop-11` now give the table's velocities, tau and friction angle (41 deg for both beds) where "Records" above says
they are not yet extracted. Item 22 of `docs/OPEN-QUESTIONS.md` is narrowed to the two printed velocities.

Correction to "Observation for users of the data" above: it calls the table's velocities the model's velocity at
contact "computed from the free fall". The report says only that they were calculated using the measured interval
from release to ground contact and prints no formula. Test No. 1's printed V_v is consistent with |V_v| = g tau (114.9
in./sec. against 115.05 for tau .298, within the rounding of both); Test No. 2's is not (60.5 against 68.34 for tau
.177) (`qa/tables-s5-b1/arithmetic.md`). Consistency does not show the method. The comparison of the early penetration
rates with the table's velocities stands as written. Section VI of the report also plots the measured histories of
both tests against its simulation (Figs. 6-13 and 6-11, PDF 384 to 387 and 375 to 378), not read here.
