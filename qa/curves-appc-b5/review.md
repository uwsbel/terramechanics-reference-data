# Review of batch curves-appc-b5: failure envelopes C-1A, C-2A, C-3A, C-4A

Reconciled with batches b3 and b4 on 2026-10-14; the shared review, with the adjudication, is
`qa/curves-appc-b3/review.md`. The two method exchanges with Codex that this batch prompted are in
`method/` (D-024) and `method/piecewise/` (D-025).

Each envelope plots, per density group of its legend, the peak shear stresses of the data-sheet tests
and the authors' straight fit with its printed friction angle. Series are the groups, named by their
printed Dr range (`dr50-57`). Features: the line's intercept with the shear-stress axis and the
printed angle label (kept as text in each record's `series.json`, not as a data point).

## Calibration

C-2A, C-3A and C-4A have ticks but no grid. Codex calibrated all three on measured ticks; Claude's
C-2A reader did too, its C-3A and C-4A readers used the grid tool, which interpolated every interior
line from the frame. Against the reconciled data-sheet peaks the tick maps are 14 to 17 psf closer
(C-3A: Codex +11 and +16 psf, Claude +25 and +33; C-4A Dr 0: Codex +30, Claude +46). Under D-024
Claude's C-3A reading is re-derived on the tick map its reader saved (`rederived/FC-3A/`; residual
rule then picks Codex, 0.00279 against 0.00316), and on C-4A Codex is named canonical with the reason
in `overlays.csv`. C-1A has a grid, unevenly drafted (286 to 311.5 px per 1000 psf); both readers
agree, and D-025 will map it piecewise.

## Identity

1. **C-1A**: Codex assigned three symbols by the line they sit on, Claude's reader by legend shape.
   The data sheets settle it for Claude's reading: the filled circle at 315 psf matches C-1C (Dr .73
   to .88) within 18 psf against 162 for C-1B; the triangle on the axis at 485 psf is the zero-stress
   test of C-1D (476 psf); the filled circle at 1772 psf matches C-1C within 28 psf. Both round-1
   adjudicators, blind to the sheets, gave the same groups from the symbols' shapes.
2. **C-2A**: the legend is printed swapped (squares are the dense tests, circles the loose), shown by
   the sheets and by Fig. C-17; renamed at the canonical stage (`series-ids.csv`), the submissions and
   the printed legend text untouched. In the records, `b68-ds-fc-2a-dr33-53` (loose) carries the
   46.7-degree line and `-dr115-130` (dense) the 49.5-degree line.

253 canonical points: agreed 228, one-sided-verified 17, resolved 4, one-sided 4.
