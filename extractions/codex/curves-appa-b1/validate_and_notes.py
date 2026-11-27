import json,csv,sys
from pathlib import Path
import numpy as np
from PIL import Image
cfg=json.loads(Path('out/config.json').read_text());sm=json.loads(Path('out/summary.json').read_text()); findings=[]
soil={'FA-4':'RS','FA-8':'PS','FA-20':'RSM','FA-24':'RC2','FA-28':'SS','FA-40':'LSM','FA-48':'RSM'}
extra={
'FA-4':'The first curve point merges with both the left frame and the 40-degree grid line. Its centre is followed from the adjoining rising stroke. The main slope becomes shallower through a rounded knee near Dr 0.55. No symbols are printed.',
'FA-8':'The initial shallow segment turns gradually into the main rising segment near Dr 0.2. Small scan breaks occur near u=1990, away from the requested sample columns. No symbols are printed. The maximum affine x residual exceeds 0.5% of the x span; the RMS does not. All six measured vertical lines pass the ink check: uneven drawn spacing is retained by the piecewise map, not forced to an affine scale.',
'FA-20':'The curve is monotonic with only a broad change of slope near Dr 0.5, not a sharp corner. Small white defects in the stroke near u=1590 are scan loss, not identifiable hollow symbols. The Dr 0.8 point was rechecked on adjoining curve ink at the grid junction. No plotted symbols are identified. Caption prints RSM Soil; series id curve and index soil RSM-a are retained.',
'FA-24':'The rounded lower knee is near Dr 0.2. A scan defect near u=2180 to 2200 cuts the curve; the Dr 0.9 sample is on its surviving left-side stroke, not the white interruption. The final part rises above the highest labelled y line (50 degrees); its native values are explicitly extrapolated using the verified 45-50 interval. The top frame has no printed numeric label and is not a knot. Caption prints RC2 Soil; id retained. No symbols are identified.',
'FA-28':'The first connected curve cap starts at (770,3223), after three white columns between it and the left frame. Its extreme left is worn down to a one-pixel strand connected to the thicker cap. The recorded bound is half the adjoining 12-pixel stroke. Its native Dr is slightly positive; there is no invented trace sample at zero. The sigmoid has two rounded knees, near Dr 0.3 and 0.65, recorded with broad feature-location bounds. No symbols are identified. The unlabelled top frame is excluded.',
'FA-40':'The page prints a cross-hatched band bounded by the 45- and 40-degree horizontal lines, extending over the full labelled Dr 0 to 1 range. This differs from the index states field Dr .40 to 1.00. Read band-top and band-bottom; no single curve and no distinct data symbols are printed. Crosses and diamonds are intersections of the repeated hatching, not plotted markers. White scars and stray short dashes in the band cannot be identified as symbols and are not counted. No triangle or test identity is inferred. Both edges are flat in native coordinates, so the peak extends along the edge and has no unique x. An initial box clipped the right frame at its bottom and failed its ink check (2.54 px); the final widened box includes its whole stroke, and all six x lines pass. The hatch vertex at bottom sample 20 is excluded from the line-thickness estimate.',
'FA-48':'The curve rises monotonically and has a broad upper shoulder near Dr 0.8. At Dr 0.85, scan loss removes the lower part of the stroke; the point is centred on the remaining upper ink, with half the adjoining full stroke width (7 px) as its bound. The last segment exceeds the highest labelled y line (50 degrees); those native values are explicitly extrapolated from verified 45-50. The unlabelled top frame is excluded. Maximum affine x residual exceeds 0.5% of span but RMS does not: all measured x lines pass the ink check and the piecewise map retains their uneven spacing. Caption prints RSM Soil; index soil RSM-b and series id curve are retained. No symbols are identified.'}
for s in sm:
 f=s['figure_id'];root=Path('out')/f;c=cfg[f];rs=list(csv.DictReader((root/'points-p1-native.csv').open()));g=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'));bad=[];maxdev=0
 for r in rs:
  u,v=float(r['pixel_u']),float(r['pixel_v'])
  if g[round(v),round(u)]>=160:bad.append((r['series_id'],r['point_kind'],r['sequence'],u,v))
  if r['point_kind']=='trace' and 1<int(r['sequence'])<21:maxdev=max(maxdev,abs(float(r['x_native'])-(int(r['sequence'])-1)*.05))
 assert not bad,(f,bad)
 assert maxdev<.00002,(f,maxdev)
 knots=json.loads((root/'cal-p1'/'knots-verified.json').read_text());assert not knots['rejected_x'] and not knots['rejected_y']
 checks=list(csv.DictReader((root/'calibration-eye-checks.csv').open()));assert len([r for r in checks if r['axis']=='x'])>=3 and len([r for r in checks if r['axis']=='y'])>=3
 text=f'''# {f}: blind page reading, panel 1

Source: packet/{c['page']}.png, unrotated 300-dpi page. Only this evidence packet was used; no other reading or earlier extraction was consulted. Caption soil: {soil[f]}. x is relative density Dr, unit `none`; y is internal friction angle phi, unit `deg`, direct shear test.

Counts: {s['counts']}. Marker count: 0. Samples are in drawing order from the left endpoint, with interior samples every 0.05 Dr, then the right endpoint. Feature rows repeat the first and last positions; the last point is also the peak of each increasing curve. Rounded knees are not sharp observed corners: their feature bounds span the visually plausible transition region. Trace bounds are half the local line thickness; at grid/frame/hatch junctions that thickness is read on the adjoining curve or edge, not the merged junction ink. Scan defects are noted on affected records.

## Calibration and by-eye checks

All six printed x labels 0, 0.2, 0.4, 0.6, 0.8 and 1.0 were checked by eye against their own vertical lines. Printed y labels {c['ys']} were each checked against their own horizontal line at the left axis. See calibration-eye-checks.csv and cal-p1/label-checks.png for the line associations and enlarged source snippets. No value was assigned to an unlabelled frame. The lower frame is excluded unless explicitly labelled (25 degrees on A-28).

Affine diagnostic residuals: RMS x = {s['rms_x']:.8f} Dr, y = {s['rms_y']:.6f} deg; maximum absolute x = {s['max_x']:.8f} Dr, y = {s['max_y']:.6f} deg. RMS residuals are below 0.5% of each calibrated axis span. The final ink-verified map uses {len(knots['x'])} x lines and {len(knots['y'])} y lines, with no predicted or rejected knots. Each verified line and its ink offsets/location error is saved in cal-p1/knots-verified.json. Native values and bounds use tools/calibrate_axes.py piecewise --image (D-025), including line-position errors and the pixel rectangle, without adding the affine residual. {s['extrapolated']} rows have an extrapolation flag; the tool also flags an endpoint when its uncertainty rectangle crosses an outer knot, even if its centre is on that knot.

Per-series maximum absolute difference, piecewise minus affine, among trace samples: {s['sensitivity']}. These are correlated calibration sensitivities, not added random error bars.

## Ambiguities and page evidence

{extra[f]}

## Files

cal-p1/ contains anchors.csv, calibration.json, knots-verified.json, and label-checks.png. calibration-eye-checks.csv records the by-eye checks. points-p1.csv stores page-pixel readings; points-p1-native.csv adds piecewise native values and reading bounds. overlay-p1.png is the full unrotated page overlay; overlay-detail.png is a plot crop for review. trace-grid-*.png (or band-grid.png) are enlarged pixel-grid crops, and samples-check*.png show every trace sample against the page ink. Full-page pixel coordinates apply to all CSVs, including those reviewed on crops.
'''
 (root/'notes.md').write_text(text,encoding='utf-8')
 findings.append(dict(figure_id=f,rows=len(rs),all_centres_on_dark_ink=True,max_interior_sampling_error_Dr=maxdev,verified_x=len(knots['x']),verified_y=len(knots['y']),eye_checks=len(checks)))
Path('out/validation.json').write_text(json.dumps(findings,indent=2));print(json.dumps(findings,indent=2))
# Human-facing short batch report.
lines=['# Blind reading: curves-appa-b1','', '| Figure | Series: trace / feature / marker | Affine RMS Dr / deg |','|---|---|---|']
for s in sm:
 f=s['figure_id'];counts='curve: 21 / '+str(s['counts']['curve/feature'])+' / 0' if f!='FA-40' else 'band-top: 21 / 2 / 0; band-bottom: 21 / 2 / 0; data: 0'
 lines.append(f"| {f} | {counts} | {s['rms_x']:.6f} / {s['rms_y']:.5f} |")
lines+=['','Every printed x label (0 through 1.0 in 0.2 steps) and y label (30 through 50 in 5-degree steps; A-28 additionally 25) was checked by eye. All final knots pass the protocol ink verification.','', 'A-40 is a band over Dr 0–1, with no distinct symbols. A-28 starts inside the frame. A-24 and A-48 require flagged y extrapolation above 50 degrees. Rounded knee locations have broad feature bounds; trace bounds remain half stroke thickness. A-48 Dr 0.85 is on surviving ink after scan loss. See each notes.md for exact ambiguities, affine maximum residuals and piecewise sensitivity.','', 'Each figure directory contains cal-p1/, calibration-eye-checks.csv, points-p1.csv, points-p1-native.csv, overlay-p1.png and notes.md, plus source crops and sample/overlay review images. Machine-readable batch summaries: summary.json and validation.json.']
Path('out/README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
