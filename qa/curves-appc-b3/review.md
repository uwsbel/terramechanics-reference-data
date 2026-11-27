# Review of batches curves-appc-b3, -b4, -b5: the remaining Appendix C data sheets and four envelopes

Date: 2026-10-14. Reconciliation by Claude and Codex together (Dan away; method questions settled
between the two agents, `docs/decisions.csv` D-024 and D-025). No human audit yet. This file covers
the three batches; `qa/curves-appc-b4/review.md` and `qa/curves-appc-b5/review.md` add what is
particular to each.

## What was read

| batch | figure | printed | PDF | what | tests or groups |
|---|---|---|---|---|---|
| b3 | FC-5B | C-16 | 130 | SS, Dr .02 to .13, data sheet | 5 (734 to 4695 psf) |
| b3 | FC-6B | C-18 | 132 | LSM, Dr .19 to .28, data sheet | 5 |
| b3 | FC-6C | C-19 | 133 | LSM, Dr 1.03 to 1.07, data sheet | 5 (printed 1961 and 714) |
| b3 | FC-6D | C-20 | 134 | LSM, Dr .05 to .40, data sheet | 5 (printed 3814 and 147) |
| b4 | FC-7B | C-22 | 136 | RSM-b, Dr 1.0, psi, printed sideways, symbols only | 6 |
| b4 | FC-7C | C-23 | 137 | RSM-b, Dr 0.53, psi, printed sideways, symbols only | 6 |
| b5 | FC-1A to FC-4A | C-2, C-6, C-9, C-12 | 116, 120, 123, 126 | failure envelopes | 9 density groups |

Codex: gpt-6.1-sol high, one run per batch (b3 1869 s, b4 852 s, b5 1192 s). Claude: one subagent
per figure. Neither saw the other's output. Hints available to both alike: the figures-index rows of
the packets still carried the inventory agents' notes columns (`docs/CURVE-READING.md` section 1);
rule 7 (trace samples on the line's ink) was given to both readers of b3 to b5 (the first Codex run of
b3 was stopped and restarted so that both had it).

## Diff and adjudication

| batch | matched | agreed | disagreed | canonical points | agreed | resolved | verified by the other agent | one-sided | pending |
|---|---|---|---|---|---|---|---|---|---|
| b3 | 1803 | 1754 | 49 | 1854 | 1754 | 42 | 51 | 3 | 4 |
| b4 | 201 | 198 | 3 | 202 | 198 | 3 | 1 | 0 | 0 |
| b5 | 232 | 228 | 4 | 253 | 228 | 4 | 17 | 4 | 0 |

(At this review. b3 now has 1,924 canonical points, after the re-derivation of D-025, the off-ink rule of
D-032 and the correction of `some` answers of D-039: `qa/curves-rederivation-d025/review.md`, Totals.)

With rule 7 in force no trace sample fell in a gap of the other reader's trace (b1 and b2 had 196).
The 122 disputed or one-sided items went through the blind two-round adjudication of D-023 (two
Claude and two Codex adjudicators in round 1, one of each in round 2; `adjudication/`); 13 stay
split (`adjudication/still-split.csv`): three features neither reader marked right (dropped), the
rest one-sided or pending and mandatory rows of the human audit.

On disputes where one reading had to be right, Claude's reading was right 49 times and Codex's
in none (the other settled disputes were `both`: the two marks within the same symbol). The disputes were concentrated: in the stacked lower panels of FC-5B and FC-6B, Codex's reader
placed one test's symbols on the neighbouring glyph (the pluses of 4695 psf on the circles printed
under them, the down-triangles of 2934 psf on the band where up- and down-triangle pairs meet), 35
markers in all, 5 to 8 thousandths of dilation off; both adjudicators, both blind, put the other mark
on the symbol every time (checked by eye on item 014). This is the counterpart of Claude's FC-3C
slip in b2 (trace samples on triangle bases): each reader has one systematic weakness in crowded
symbol fields, and the adjudication catches both.

## Findings about the figures

1. **Fig. C-2A's legend is printed swapped** (with Codex, D-024). Both readers read it as printed and
   agree to 2 psf. Its "Dr .33 to .53" squares sit 150 to 770 psf above the peaks of the loose tests
   of C-2B and within 8 to 48 psf of the dense tests of C-2C; its "Dr 1.15 to 1.3" circles sit within
   4 to 54 psf of the loose peaks. Corrected by a canonical rename (`qa/curves-appc-b5/series-ids.csv`):
   dense PS 49.5 degrees, loose PS 46.7 degrees, as Fig. C-17 also plots. `insights/` note.
2. **Envelope points against the data sheets.** With the tick-based calibrations, the envelope
   points of C-3A sit 11 to 16 psf above the data-sheet peaks on average, C-4A's loose group 30 psf;
   two points of C-4A's dense group sit 150 to 200 psf below C-4C's peaks in both readings, a
   difference in the report itself. C-1A's three disputed symbols are settled by the sheets (D-024).
3. **C-9A's printed fit** (tan 1.3059, cohesion 634.20 psf) is reproduced within 0.3 and 0.1 percent
   by the C-1D peaks read in b1, only with the zero-stress test (`qa/experiments-vol2c-b1/review.md`).
4. On C-6D the drawn line of the 147 psf test runs 18 to 56 psf above its own symbols beyond 57
   thousandths; C-6A's envelope point agrees with the symbols. On C-6B the lower panel has no squares
   (no dilation points for 3815 psf). C-5B's heading prints a unit weight 97.3 (or 97.8) against 97.6
   in its legend.

## Method changes made on the way

1. `tools/calibrate_axes.py` reads figures printed sideways (`--x-direction`, `--y-direction`) and
   keeps enough decimals on small-valued axes (its three fixed decimals zeroed the x bounds of an
   inch axis; Claude's FC-7B and FC-7C values re-derived from their pixels, `qa/curves-appc-b4/rederived/`).
2. Gridless figures: calibration on measured ticks; a residual over lines predicted from the frame
   cannot win the canonical choice (D-024). Claude's FC-3A reading re-derived on its own tick map
   (`qa/curves-appc-b5/rederived/`); Codex named canonical on FC-4A with the reason in `overlays.csv`.
3. Triangle centers: the centroid, with the box midpoint inside the bound (D-024); earlier readings
   to be normalized. Envelope features: intercept and printed label, the label kept as text in
   `series.json`, not as a data point.
4. D-025 (with Codex): piecewise calibration between verified lines, frame as zero; on FC-6B and
   FC-6D the two readers' affine maps differ by up to 2.6 thousandths at the origin. To be
   implemented, then every batch re-derived (roadmap 3a2). The values in `data/` from these batches
   are on the affine maps until then.
5. Evidence packets no longer carry the agents' notes columns.

## Records

41 records written to `data/experiments/b68-ds-fc-*`: 20 tests from b3, 12 from b4, and the 9
density groups of the envelopes from b5. The Codex reading's one unidentified FC-7C symbol is the diamond
of 6.6 psi (both adjudicators, round 2) and is not a series.
