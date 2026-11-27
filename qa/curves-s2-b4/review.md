# Review of batch curves-s2-b4: dynamic penetrometer records (Fig. 2-54, D-050 roadmap step 6d)

Fig. 2-54 (Volume I, printed 2-92, PDF 117, printed sideways): three oscillograph records of the dynamic penetrometer
(DPT) striking a soil bed, deceleration against time, one solid trace per record, stacked in three panels: Record
No. 53958 (2 ft box, RS loose, 41.1 pcf), Record No. 54025 (2 ft box, RS intermediate, 44.1 pcf) and Record No.
54-65 (the bed of LPT No. 26, RS dense, 52.0 pcf). Each panel has its own ruler of G's and a dashed line close to
its zero; the vertical timing lines run across all three, 0.01 s apart by the figure's scale bar; each trace is cut
by break marks on the left.

## Readings

Both agents, blind, from the evidence packet written by `tools/make_reading_packet.py` (`qa/curves-s2-b4/batch.json`),
2026-11-19. Codex: gpt-6.2-sol high, one run (589 s). Claude: one subagent (claude-opus-5-5), writing outside the
repository until Codex had finished. **Hints available:** the batch description stated two conventions: time from
the timing line that carries the rulers (0 ms, the figure prints no origin), and "the dashed zero line is 0 g".
The second was the orchestrating session's assumption, not checked against the page, and it was wrong (below).
Points submitted (trace / feature): Claude 77/9, 80/10, 96/8; Codex 78/9, 90/11, 100/8.

## The zero of deceleration

The dashed line is not 0 g. On each panel's ruler the printed "0" and its stub are centered on the trace's
pre-impact baseline, the ruler's spine ends there, and the evenly spaced positive ticks extrapolate there (panel 3:
ticks 22 to 24 px apart; the next step lands at u 2345, on the baseline at 2346.8, not on the dashed line at 2335.6).
The dashed line lies 0.72, 0.91 and 0.94 g above the printed zero in panels 1 to 3 on each ruler's own scale, the same
along its length (Claude's reading, with the 0.7 degree tilt of the scan taken into account); Codex's review, mapping
Codex's dashed-line anchors through the reconciled maps, gives 0.78, 1.03 and 0.94 g. (A first estimate in this session,
1.1 to 1.8 g, ignored the tilt.)
Claude's reader found this and anchored 0 g on the baseline; Codex's reader anchored the dashed line as the brief
said and flagged the offset in its notes. Dan's decision, 2026-11-19: the printed zero stubs are 0 g. For both
readings the 0 g line is the stub's centre measured on the page by the reconciliation (`knots.csv`: u 860.3, 1330.1
and 2346.7 px, the same points for both readings, within 0.3 px of Codex's own stub measurements), replacing each
reader's 0 g line. On that zero the traces read about 0 g before impact (-0.1, +0.2 and -0.1 g in the three panels),
as a penetrometer in free fall should; on the dashed line they had read about -0.8 to -0.9 g. The dashed line,
unlabeled, is probably the level at rest, near 1 g: late in the records the traces sit at 0.4 to 0.7 g (panels 1 and
2) and 1.1 to 1.8 g (panel 3, still moving). The record panels carry a note on the time origin; the zero is the
printed scale's own.

## Calibration

Both readings anchored the same 12 timing lines per panel (-20 to 90 ms; the scale bar's arrows meet two adjacent
lines, so one interval is 10 ms; the lines are drawn 149 to 164 px apart, the same pattern in all three panels, which
the piecewise map follows; affine time residual about 0.43 ms). Both took the timing line the rulers stand on as 0 ms
and the top frame as 90 ms. Panel 2's ruler is drawn unevenly: Claude's 2, 11 and 29 g ticks and Codex's 2 g tick
fail the ink check (5.5 to 5.8 px from the ink, next to the dashed line or a neighboring tick); Codex's 11 and 29 g
ticks pass. The two maps differ there by up to 0.52 g (at 29 g); Codex's reading is canonical for panel 2 (its lines
include Claude's), Claude's for panels 1 and 3 (the same lines, the first submission).

## Comparison rule for this batch

The traces were sampled by rule at several spacings (0.5 ms on the pulse and every 5 g on panel 3's steep flanks,
2 ms elsewhere), so a reading's median sample spacing fell far below its ordinary steps, and the comparison read
the 2 ms steps of panel 3 as drawn gaps (95 points unmatched). These solid traces have no drawn gaps of their own, only short interruptions the 6 ms threshold bridges: a white gap
of about 10 px at panel 1's rise, the printed "0" over the lead-in near +2 ms, and the stretches under the ruler labels
(2 to 6 ms) that the Claude reader left unsampled. `overlays.csv` sets `max_gap` 6 ms (three times the coarsest spacing; `tools/diff_curves.py --max-gap`, from 2026-11-19), and the
features are paired by their own role (`feature_roles` leading). Earlier batches keep their rules.

## Agreement and adjudication

Before adjudication 282 of 284 matched points agreed within the sum of their bounds; 519 of the 521 trace samples
passed the ink check (2 at a timing line marked for review, not excluded). Blind adjudication in
`qa/adjudication-2026-11-19-dpt/` (12 items): both disagreements were knees placed at different bends, both settled
for Claude's reading; the three last samples one reader placed on the top frame line, 3 to 5 px past the trace's ink,
excluded; 16 one-sided samples and one feature verified. Two one-sided knees split (a bend about 9 px from the mark,
against the 8 px rule, and a turn of about 3 degrees) and stay one-sided as mandatory audit rows.

Final canonical points: 296 (276 agreed, 16 one-sided-verified, 2 resolved, 2 one-sided). After the round, Codex's
review found the end samples the adjudicators excluded shared their place with the other reader's last sample and with
`last` features (nine points in all, excluded by the same criterion; the round's README), and a duplicate of a trace's
end (the other reading's sample within both bounds of the canonical end), which `end_dedup` in `overlays.csv` drops
(`tools/diff_curves.py --end-dedup`; opt-in, see `docs/OPEN-QUESTIONS.md` item 21). Peaks: 20.1 g at 12.5 ms
(Record 53958), 29.0 g at 13.2 ms (54025), 77.8 g at 14.8 ms (54-65). The selected onset knees (the main corner where
the rise begins) fall on the 10 ms timing line; in panel 2 an adjudicator noted an earlier, gentler departure from the
baseline below it.

## Records

`tools/build_batch_records.py curves-s2-b4`: `b68-dpt-r53958`, `b68-dpt-r54025`, `b68-dpt-r54-65`, one panel each
(the figure's panel 1, 2 or 3; `series.json` names the figure panel of the two records where it is not 1), time in s, deceleration in m/s^2 (standard gravity). Setup
incomplete (index rows). Observation: the text (printed 2-90, PDF 115) gives a mean peak of 11.76 g, the average of the means of
49 loose RS beds of the subscale drag tests with four DPT drops each, while Record 53958 is a single signature in a
2 ft box of RS loose (41.1 pcf) and peaks at 20.1 g on its ruler. The two are different setups and levels of
aggregation; the difference is the records', not the reading's.
