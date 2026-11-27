# Review: experiment rows for the footpad impact runs and two LM model drops (batch experiments-s3s5-b1)

Date 2026-11-19 (D-050, roadmap step 6). Two blind inventories from the page images of AM-68-1 Vol. I,
Sections III to V (PDF 142 to 212, 280 to 344) and the agreed figures index rows of those sections without the
agents' notes: Claude (a separate Claude agent, `extractions/claude/experiments-s3s5-b1/`, with `setup.md`) and
Codex (gpt-6.2-sol, high, read-only, `extractions/codex/experiments-s3s5-b1/`). Same brief (`prompt.md`). Built
into `data/experiments/index.csv` by `tools/build_experiments.py` as the fourth stacked batch, with
`resolutions.csv` (17 cells of wording).

## Result

Both readings made the same 9 rows with the same ids: seven impact runs with plotted histories
(`b68-imp-4`, `-10`, `-12` with force and displacement against time in Fig. 4-19 and force against displacement in
Fig. 4-20; `-15`, `-16` in Fig. 4-21; `-ii-1` and the full-scale `-fs16` in Fig. 4-22) and the two model drops
with histories (`b68-mdrop-10`, NASA Test No. 1, and `b68-mdrop-11`, NASA Test No. 2). They agreed on every
soil number (inferred from the printed states: Soil 1 for RS loose, 3 for the Dr 0.45 bed, 4 for the Dr 0.65
bed), state, relative density, unit weight, moving weight, loading, measured channels and setup status
(`setup_incomplete` for all nine). The 17 resolved cells differ in wording only (footpad, bed, velocity as
printed).

## What the setup lacks (both readings)

1. Impact velocity: only "about six fps" for every impact run (text 4-22, PDF 207); no per-run value.
2. Moving weight of Runs 10 and 12: not printed (Runs 4 and II-1 31 lb, 15 41 lb, 16 51 lb, full-scale 16
   1,140 lb).
3. Bed density: no unit weight or Gp for any impact run; Dr not printed for II-1 and full-scale 16.
4. The states of Runs 10 and 12 (intermediate, dense) come from matching the text's list to the legend order.
5. Gravity: not printed; terrestrial is implied by the rigs.
6. Model drops: the footpad diameter is not printed in Section V; the loose bed depth is not printed (18 in
   applies to the intermediate beds).

## Printed differently in two places (kept in the rows' notes)

1. Run 12's Dr 0.65 against Soil 4 (RS dense) at Dr 0.80 in Table 2-3; Fig. 4-40 also labels the impact tests
   "RS Dense (Dr = .65)".
2. The model-drop beds print Dr 0 with 46.9 pcf and phi 41 deg; Soil 1 (RS loose) in Table 2-3 is Dr 0 at 41.4
   pcf and phi 40 deg.
3. NASA Test 1: -114.93 in/s in the Fig. 5-25 inset, -114.9 in Table 5-T3, "10" without a unit in Table 5-T2, a
   nominal ten ft/s in the text. NASA Test 2: -60.55 and 83.75 in/s in the Fig. 5-32 inset (degraded scan), -60.5
   and 83.5 in Table 5-T3. A simulator takes its touchdown conditions from Table 5-T3.
4. Run 4 (31 lb) is below and Run 16 (51 lb) above the rig's printed range of about 32 to 50 lb (text 3-22,
   PDF 163).
5. Text 4-22 says Fig. 4-22 shows force against time; it plots force against displacement.

## Correction, 2026-11-19

Codex's review of the impact pilot found that the merge had dropped the unit of the beds printed in feet:
`bin_printed_in` read `18 by 12` for the two model drops (18 ft long and 12 ft wide, maximum depth five feet, text
5-22, PDF 302) and `12 by 18` for full-scale run 16 (the 12 by 18 ft pit, 5 ft deep, text 3-27, PDF 168), and the site
showed them as inches, 12 times too small. Both readings had the feet; `tools/build_experiments.py` (`norm_bin`) now
keeps the unit: `18 by 12 ft` and `12 by 18 by 5 ft`. No other row changes.
