# Independent reading: FC-1B, curves-pilot-b1

Source: `packet/p0117.png`, 3213 x 4508 pixels, unrotated, Figure C-1B,
printed C-3 / PDF 117. Every coordinate in the CSVs, this note, helper scripts,
and crop labels is an original-image coordinate: u right, v down. Only the
provided packet was used. No other reader's curve extraction was sought or
consulted. The two preceding page images were inspected for context; their
curves were not used as numerical constraints.

## Units and printed legend

The heading reads `RS Soil`, gamma `46.7 to 47.4 Lb./Ft.^3`,
`(Dr = .5 to .57)`. The inset columns read sigma `(PSF)` and gamma `(PCF)`.

| Series | Symbol seen on the upper curve | sigma, psf | gamma, pcf |
|---|---|---:|---:|
| n3520 | x | 3520 | 46.7 |
| n2935 | asterisk | 2935 | 46.8 |
| n2345 | square | 2345 | 46.7 |
| n1760 | plus | 1760 | 46.7 |
| n1172 | triangle-down | 1172 | 46.8 |
| n587 | triangle-up | 587 | 47.2 |
| n294 | circle | 294 | 47.4 |

The lower inset reads `Same Notation As Above`. Symbols were assigned by their
outline, then checked against this inset and their upper-panel identities.
The scan makes some small asterisks resemble solid blobs; separated examples
show the additional spokes. They are distinguishable from the larger four-arm
pluses and diagonal x marks. The open circles, squares and two triangle
orientations are distinguishable in the enlarged crops.

Upper ordinate: tau `(PSF)`, 0 to 6000. Lower ordinate: dilation displacement,
delta_sigma x 10^3 `(in.)`, -100 to +100. Shared abscissa: shear displacement,
delta_tau x 10^3 `(in.)`, 0 to 250. Thus x_native, and panel-2 y_native, are
numbers in **thousandths of an inch**, not inches. Panel-1 y_native is psf.
No SI conversion was requested or applied.

The n2935 unit weight on this page is **46.8**, despite the 46.5 value in the
supplied experiment row. The extraction uses the printed Figure C-1B identity;
it does not alter the experiment table.

## Calibration and visual checks

Both final calibrations were generated independently with the supplied
`tools/calibrate_axes.py detect`, dark threshold 200. The legend extension to
the right was excluded from the calibration frame: the vertical line at
x=250, rather than the far-right legend border, is the abscissa endpoint.

Final commands (with the supplied Python interpreter):

```
tools/calibrate_axes.py detect packet/p0117.png --box 750 1080 2280 2865 --x-values 0,50,100,150,200,250 --y-values 0,1000,2000,3000,4000,5000,6000 --bands 24 --min-frac 0.55 --snap 6 --frame-frac 0.4 --out out/cal-p1
tools/calibrate_axes.py detect packet/p0117.png --box 795 2965 2290 3575 --x-values 0,50,100,150,200,250 --y-values=-100,0,100 --bands 4 --min-frac 0.35 --snap 15 --frame-frac 0.5 --out out/cal-p2
```

The initial upper run at min-frac 0.35 mistook heading ink for the 5000-psf
line, producing RMS y=54.430 psf, above 0.5% of the 6000-psf span. That run
was rejected before reading points. At 0.55, the genuine short 5000-psf line
does not cover enough bands and is marked **predicted**. I checked the visible
segment by the 5000 label, approximately (800,1420), and the visible right-hand
segment: both support that grid identity. Its actual scan position differs by
several pixels from perfect equal spacing; this is not evidence of a different
label. All other final upper grid lines are detected.

Initial lower calibrations with many narrow bands fragmented vertical tracks
around markers and gave visibly wrong line slopes. Four wider bands follow
each short-panel vertical line across its full height. All final lower lines
are detected in 4/4 bands; none is predicted. The final tilted lines were
checked against the frame and the interior grid.

| Panel | Anchors | RMS x | Max abs x | RMS y | Max abs y |
|---|---:|---:|---:|---:|---:|
| 1 | 42 | 0.173767 | 0.356628 | 9.239412 psf | 15.896224 psf |
| 2 | 18 | 0.268507 | 0.556634 | 0.374777 | 0.602729 |

x residuals and lower y residuals are in thousandths of an inch. Both final
RMS residuals, and also their maximum residuals, are below 0.5% of their
respective axis spans. Residuals describe agreement of the affine map with
the fitted grid intersections, not uncertainty in every curve point.

I read at least three labels on each axis by eye and checked their grid
positions against the fit. The upper panel does not repeat x labels: the
printed shared x labels below panel 2 were read, then the corresponding
upper-panel vertical lines were checked independently. These are approximate
by-eye positions, not added fitting anchors:

| Panel / axis | Label read | Checked pixel (u,v) | Fitted native value |
|---|---:|---|---:|
| 1 x | 0 | (800,2854) | -0.091 |
| 1 x | 100 | (1390,2843) | 100.257 |
| 1 x | 250 | (2270,2828) | 249.923 |
| 1 y | 6000 | (766,1127) | 6007.166 |
| 1 y | 5000 | (800,1420) | 4985.908 |
| 1 y | 4000 | (778,1709) | 3981.909 |
| 1 y | 3000 | (783,1992) | 2997.169 |
| 1 y | 0 | (800,2854) | -2.392 |
| 2 x | 0 | (812,3566) | -0.269 |
| 2 x | 100 | (1402,3556) | 99.849 |
| 2 x | 250 | (2285,3541) | 249.688 |
| 2 y | +100 | (800,2995) | 99.646 |
| 2 y | 0 | (806,3278) | 0.528 |
| 2 y | -100 | (812,3566) | -100.339 |

These checks are also in `calibration-eye-checks.csv`. The labeled crops
`cal-labels-*.png` preserve the visual evidence for the checks.

## Reading method and sequence

Markers were placed first from the supplied crop tool's labeled pixel grids,
at zoom 3 or 4, and revisited in individual 4x contact sheets. The origin
cluster was also inspected at 6x. `components.py` lists isolated ink-component
bounding boxes as a center check; connected grid/curve components were not
treated as symbols automatically. Manual symbol identification remains the
basis for inclusion. The final marker corrections are explicit in
`read_points.py`; `markers-p*-*.png` show every retained marker centered under
a crosshair (green tick interval = 5 original pixels).

Upper traces were read only after marker placement. Manually read guide knots
identify the author-drawn line for each series; they are search guides, not a
polynomial or mechanical model. At each chosen column, nearby dark pixel runs
are found across the column and its two immediate neighbors, at threshold
128. The appropriate run is selected by the visible branch and its continuity.
The seven curves retain their vertical order after the close early
plus/square region. Horizontal grid runs and marker edges are checked against
the cropped image and guide, rather than assigned by darkness alone.

The base sampling increment is 20 original pixels, approximately 3.4
thousandths of displacement. Each series starts at its first visible line
segment: u=880,936,875,925,869,920,920 for n294 through n3520 respectively.
Columns are shifted away from tilted vertical grid lines, and additional
columns near the safe edges are included where required to keep calibrated
trace spacing <=5. The exact chosen columns are the `trace` CSV records.
No sampled trace column is deliberately placed on a vertical grid line.

Small interruptions at marker rims are bridged locally using the visible
line flanks, with wider bounds and a point-level note naming the two flank
columns. These are estimates of the drawn curve's continuation, **not new
measurements**. Long interruptions are not bridged. In particular the
n2345 gap described below remains missing.

Every series has first-point, drawn-line peak, and last-point features. End
features use the plotted end-symbol locations because the ink line ends at
the symbol rim. Peak selection compares calibrated ordinates of visible
line-center runs, accounting for page tilt; it does not select the highest
marker. Flat summit intervals have broad horizontal bounds. Additional
features record the n2345 stroke end/restart, the shallow n2935 trough and
the rounded transition into the n587 residual tail. Other curves have smooth
bends rather than identifiable sharp kinks.

The drawings were checked for reversals: none contains an unloading loop.
Records are interleaved in the inspected forward drawing progression;
`sequence` is consecutive within each panel and series across all point
kinds. The original manual marker lists and forward trace lists are retained
in the helper. No reversal is removed by reordering. Features duplicate
locations already represented by markers/traces and are not extra test
observations. Panel 2 contains only marker records.

## Reading bounds

Pixel bounds are half-width **reading bounds**, not standard deviations.
Manually located clean centers normally have 3-pixel bounds (a conservative
allowance for the coarse raster and symbol asymmetry). Grid-line/frame
overlaps normally have 12-pixel bounds; touching circles/down-triangles
near the origin have 15-pixel bounds. More specific exceptions appear in the
point notes. Trace v bounds use the full detected line thickness (at least
6 pixels), rather than an unrealistically precise centerline. Bridges use
at least 15 pixels; doubled/merged traces use 24 pixels. First/last features
include symbol extent. Peak u bounds include the stated broad summit interval.

The supplied `apply` tool adds native coordinates and bounds: each native
bound is the sum of the absolute affine coefficients times the two pixel
bounds, plus that axis's RMS calibration residual. Extra decimal places in
native values reflect the transform, not additional reading precision.

## Ambiguities, interruptions, and omitted locations

* **Lower n1760 origin:** a definite plus is visible at about (780,3293), just
  left of the frame. It is provisionally included as n1760, with u bound
  30 pixels and v bound 8, and a note. It could be a displaced origin symbol
  or a reference glyph rather than a separate measured datum. It has negative
  fitted x; it has not been moved to zero. The oval farther left at about
  (750,3285) is the printed numeric zero label and is not counted as a circle.
* **Lower n1172 near x=0:** I cannot resolve a separate down-triangle beneath
  the circle/frame at about (807,3295). A conjectural overlapping duplicate
  was removed on close review. It is **omitted**, not asserted to be absent
  from the original experiment. The first separable down-triangle is near
  (874,3309), x about 11.
* **Lower early circle/down-triangle pairs:** near u=874, 990, 1107, 1223 and
  1344 their outlines touch or overlap, with the zero line crossing some of
  them. Upper arcs identify circles and lower angled sides identify inverted
  triangles. Both centers carry broad bounds and explicit notes. The frame
  circle near u=807 is itself partly obscured.
* **Lower frame/grid overlaps:** symbols near x=0,50,100,150,200,250 often
  merge into vertical ink. Centers were read from their exposed sides, with
  enlarged bounds. Squares and asterisks near the zero line need the same
  treatment. This includes the final symbols at the x=250 frame.
* **Lower touching pair near u=2105:** the down-triangle around v=3107 touches
  the plus at v=3137. Both are retained with 12-pixel bounds. The asterisk at
  about (1928,3234) is broken into pieces; the square at (2222.5,3225.5) has an
  interrupted right side. Neither was split into multiple observations.
* **Lower irregular sampling / unfilled gaps:** no separate n2935 marker was
  located near x=180 between its x~160 and x~190 symbols; no n2345 marker was
  found around x=60--70 between its x~50 and x~80 symbols. No n587/n1760/n3520
  marker was found around x=240 before their final x~250 symbols. These are
  location checks, not assertions that regularly spaced markers must exist.
  Nothing was inserted to regularize these series. The n1172 markers near
  x=190 and x=200 are both visible and were both retained.
* **Upper early n1760/n2345:** the two rising lines approach and share/merge
  ink near u=900--1100; the first two pluses sit on or near the square-series
  line. Wider bounds and branch-assignment notes cover this region. The
  outgoing distinct curves determine which continuation is followed.
* **Upper horizontal-grid contacts:** n2935 near (1258,1986) meets the
  3000-psf line; n3520 near (1726,1697) and its adjacent drawn segment meet
  the 4000-psf line. The n587 descending line also crosses the 1000-psf grid.
  Grid/curve superposition receives larger bounds. The dark grid itself was
  not followed as a curve plateau.
* **Upper n2345 doubled stroke and gap:** from roughly u=1830 to 1965, a
  short almost horizontal lower stroke at v~2044 accompanies the curved
  stroke above it. Its meaning cannot be settled from this raster. The
  selected path follows the curved upper continuation into the square/lower
  segment; bounds include the alternative ink. The lower stroke stops at
  approximately (1965,2045). There is no connecting curve across approximately
  u=1966--2045; a square stands separately near (2026,2024.5), and the curve
  resumes near (2046,2033). The gap is **not interpolated**. Consecutive trace
  samples at u=1949 and 2049 differ by 17.052 native x units; the drawing gap
  itself is about 14 native x units. This is the sole exception to the <=5
  trace-spacing requirement, because no line can be read there.
* **Upper markers need not lie on the drawn fit:** this is particularly
  evident for the plus near (1612,2168), below the smooth curve, and several
  squares/triangles. Marker positions and trace positions were kept separate.
  The circle around (1675,2678) is partially erased/merged with a vertical
  grid line; it is retained with broad bounds.
* **Curve endpoints and peaks:** there is no visible continuation to x=0 in
  the upper panel; none was extrapolated. The final symbols abut or slightly
  cross the x=250 line, so raw fitted x values can differ slightly from 250.
  Broad summits and raster roughness do not support a sharply determined
  peak displacement; feature notes and horizontal bounds reflect this.

## Counts and verification

| Series | Panel 1 markers | Panel 1 traces | Panel 1 features | Panel 1 total | Panel 2 markers |
|---|---:|---:|---:|---:|---:|
| n294 | 13 | 70 | 3 | 86 | 14 |
| n587 | 12 | 69 | 4 | 85 | 13 |
| n1172 | 13 | 70 | 3 | 86 | 13 |
| n1760 | 12 | 70 | 3 | 85 | 13 |
| n2345 | 13 | 66 | 5 | 84 | 14 |
| n2935 | 12 | 70 | 4 | 86 | 13 |
| n3520 | 8 | 69 | 3 | 80 | 13 |
| Total | 83 | 484 | 25 | 592 | 93 |

The CSV schema, symbol vocabulary, positive bounds, consecutive sequences,
native transforms, required features, calibration limits and trace spacing
were checked with `validate_reading.py`. Results are in `validation.json` and
`counts.csv`. Overlays and all individual marker sheets were inspected;
marker corrections were followed by regeneration of the CSVs and overlays.

Required deliverables: `cal-p1/anchors.csv`, `cal-p1/calibration.json`,
`cal-p2/anchors.csv`, `cal-p2/calibration.json`, `points-p1.csv`,
`points-p1-native.csv`, `points-p2.csv`, `points-p2-native.csv`,
`overlay-p1.png`, `overlay-p2.png`, and this file. The official overlays retain
the full original-page dimensions. `review-overlay-p1.png` and
`review-overlay-p2.png` are enlarged-panel review crops; their crop origins
are (825,1615) and (750,2950), respectively. Other PNGs are labeled reading
crops or marker contact sheets. Helper scripts, component listings and
validation files are supplementary, all under `out/`; `tools/` was unchanged.
