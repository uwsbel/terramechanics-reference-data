# Review: experiment index rows for the subscale drag tables (batch experiments-drag-b1)

Date 2026-11-19 (D-050, roadmap step 6e). Two blind readings (`prompt.md`) from the page images of AM-68-1 Vol. I
Sections II to IV and the agreed figures index rows without the agents' notes: Claude (a separate agent, with
`setup.md`) and Codex (gpt-6.2-sol high, read-only, 322 s). One row per printed table page, Figs. 4-6a to 4-16 (13
rows, kind `run-table`, a new kind: a printed table of separate runs, one physical test per row). Built into
`data/experiments/index.csv` by `tools/build_experiments.py` as the fifth stacked batch.

## Result

Both readings made the same 13 rows with the same ids, and agreed on every identity and number cell (soil, state,
D_r, unit weight and g_p ranges, kind, setup status). Of the 91 differing cells, all text, 39 (the footpad, bed and
velocity range of each table) are resolved in `resolutions.csv`: the substance is the same in both (the same nine
tables list a 4 in pad, the same velocity ranges, the same 10 by 3 ft bins with 11 to 12 in of soil). Notes,
evidence, loading and channels merge by the builder's rule for descriptive columns. No existing row changed.

## What the setup lacks (both readings)

1. The fill depth of each bed (only the bins' 11 to 12 in is printed), how many runs shared a bed, where across the
   bin the pad ran.
2. The footpad's contour and mass; the 4 in pad (nine tables) is not described at all; A_ft and A_pt are not printed.
3. Whether the pad's pivot was free or locked (alpha varies from run to run, which suggests free; not stated).
4. The density of each run: g_p varies from run to run while D_r and gamma are mostly one value per table; the
   tabulated D_r differs from the Section II preparation averages for soils 4, 8 and 9.
5. Gravity (Earth is implied).

## Printed differently in two places, or worth knowing

1. The tables hold 272 runs; the text gives 363 drag tests in all (printed 4-4, PDF 189). Soil No. 1 has 67 printed
   runs numbered up to 1-114.
2. Run 2-20 (Fig. 4-7) is the run of the Fig. 4-5 record: 14.20 fps in the table, 15 fps in the record's header,
   14 fps in the text.
3. Fig. 4-6b: D_r stays 0 while gamma rises from 41.1 to 58.3 pcf from run 1-84, consistent with the degradation of
   the soil after vacuum loading began at test 1-75 (printed 2-101, PDF 126).
4. Fig. 4-16 prints two D_r values (0.81 for runs 11-1 and 11-2, 0.70 for the rest) with one gamma, 82.0; run 11-2's
   0.63 fps is below the 1.5 fps lowest speed of Fig. 4-2.
