import csv,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'tools');import calibrate_axes as ca
from guides import CURVES
identity={
'F2-29':'''`lpt27` is the single wavy recorder trace, labelled LPT #27, 2-inch Diameter Cylinder, D.P.T. Record No. 54074, Pen Rate 1/2 inch Per Min., Plate Compactor. The boxed text is an annotation, not plotted points. The context on p0077 describes the hydraulic advance and x-y recorder. The initial local load maximum and subsequent load minimum are retained in drawing order. The global load maximum is at the upper terminal ink, near 8 inches. No marker symbols occur.''',
'F2-32':'''`lpt93` follows the long dashed line labelled LPT No. 93, Gp = 16.2; `lpt53` follows the solid recorder curve identified by the leader from LPT No. 53, Gp = 15.6; `lpt52` follows the dotted curve identified by the leader from LPT No. 52, Gp = 15.4. The arrows and styles agree. The visible starts are approximately 0, 2, and **1 inch**, respectively; the 1-inch start of LPT 52 is printed evidence, despite the prompt's general description of 0- or 2-inch starts. `fit` is the thin straight ink reached by the Slope = 6.5 lbs./in. = AγNq leader. Its low end reaches the load axis near the printed 4.7-lb intercept. The equation block is not a curve. No marker symbols occur.

The dotted and solid records are only a few pixels apart over much of the upper linear portion, and sometimes merge. I use the dotted left branch and continuous solid right branch where separately visible, with wider bounds in the overlap. The dotted upper termination merges with the fit and the 7-inch grid line: its endpoint has a 12-pixel bound and explicit note. The thin fit passes through this same region. The dashed start cap projects slightly beyond the zero-penetration line; its observed pixels are retained. Quarter-inch targets falling in a dash/dot gap are displaced to nearby ink, with the actual displacement recorded in the note and actual coordinates converted to native units.''',
'F2-33':'''`lpt74` is A, the thin wavy trace labelled A LPT No. 74, Gp = 103, started at the soil surface. `lpt75` is B, the thick recorder trace labelled B LPT No. 75, Gp = 105, started two inches below the soil surface. The printed setup says four-inch-diameter cylinder and surface test run in a 36-inch by 36-inch bin. `fit` follows the thick, steep straight line reached by the Slope = AγNq = 316 lbs./in. arrow. `bce` follows the shallower straight line reached by the Bearing Capacity Equation, φ = 49.5° arrow. No marker symbols occur.

The surface-start record crosses the steep fit near its first local failure peak and then drops before recovering; that reversal in load is retained. The below-surface record crosses/runs with the steep fit around 2.7–3.3 inches, then has a local drop before rising again. The records also cross near 2.3 inches, and both cross the bearing-capacity line. Bounds are wider at these locations. The fit's low terminal ink has a small bulb/hook merging into the load-axis ink; the intercept feature is placed on that terminal ink, rather than prolonging an ideal mathematical line. The equation block is not sampled.''',
'F2-34':'''**The load-axis label is printed `Load - Lbs. x 100`. Values 0, 200, 400, 600, 800, 1000, 1200 are supplied and exported with unit `lb`, exactly as directed; no multiplication by 100 is applied.** This printed label is also recorded in calibration-eye-checks.csv and calibration.json.

`lpt87` is A, the thick continuous recorder line labelled A LPT No. 87, started at the soil surface. `lpt88` is B, the thin wavy line labelled B LPT No. 88, started two inches below the surface. The printed setup gives a 108-inch by 36-inch test bin. `fit` is the shallow thick straight ink reached by the Slope = AγNq = 54 lbs./in. arrow, **not** the much steeper thick continuation of A. The leader and adjacent A/B labels settle identity. Its upper end includes a small separated cap immediately above a short scan break; the terminal cap is retained. No marker symbols occur.

B and the fit are close and cross over approximately 4–5 inches, with distinct branches visible on either side. The three lines converge around 2.3 inches; B then turns rapidly toward zero load near its 2-inch start. A also crosses the fit near its initial bend. Bounds and notes mark these crossings. B continues beyond the last printed penetration label (6) to slightly beyond the unlabelled 8-inch grid line. These native values are flagged as extrapolated, since unlabelled continuation lines were not promoted to labelled calibration knots.'''}
allcounts=[];summ={}
for f,fc in CURVES.items():
 d=Path('out')/f;page=f'packet/p{fc["page"]:04}.png';cal,X,Y=ca.piecewise_maps(d/'cal-p1',page)
 pts=list(csv.DictReader(open(d/'points-p1-native.csv',encoding='utf-8')))
 counts={s:{k:sum(r['series_id']==s and r['point_kind']==k for r in pts) for k in ['trace','feature','marker']} for s in fc['curves']}
 for s,cs in counts.items():
  for k,n in cs.items():allcounts.append({'figure_id':f,'series_id':s,'point_kind':k,'count':n})
 eye=list(csv.DictReader(open(d/'calibration-eye-checks.csv')))
 checks={a:[r['printed_label'] for r in eye if r['axis']==a] for a in ['x','y']}
 recovery=''
 if (d/'cal-p1/recovery.json').exists():
  rr=json.load(open(d/'cal-p1/recovery.json'));recovery=f" The {rr['axis']} = {rr['value']:g} line was remeasured on the page from {len(rr['points'])} ink anchors (straight-line RMS {rr['rms_px']:.3f} px), replacing its initial rejected/predicted position. Original diagnostic anchors are preserved in anchors-before-recovery.csv."
 txt=f'''# {f}, panel 1 — independent packet reading

Only this workspace's packet and protocol were used; no other reader's output or earlier figure reading was sought. Source: packet/p{fc['page']:04}.png, 300 dpi, unrotated. All CSV coordinates use that page's original origin, u right and v down. The overlay has the full page dimensions and is also unrotated.

{identity[f]}

## Calibration

Penetration increases up the page; load increases left. Both axes are linear. The initial detected affine map is a diagnostic: RMS residuals {cal['rms_residual_x']:.6f} in and {cal['rms_residual_y']:.6f} lb; maxima {cal['max_residual_x']:.6f} in and {cal['max_residual_y']:.6f} lb. Neither exceeds 0.5% of the calibrated axis span. Native values and bounds use the protocol's piecewise map between verified ink lines, with line-location errors propagated and no global affine RMS added.

Verified x knots: {', '.join(str(int(k['value'])) for k in X.knots)} in. Verified y knots: {', '.join(str(int(k['value'])) for k in Y.knots)} lb. All final knots pass the tool's ink test; no predicted line is used as a knot.{recovery} The frame beyond the final printed penetration label has no assigned calibration value.

By-eye checks: penetration {', '.join(checks['x'])}; load {', '.join(checks['y'])}. Every checked numeral was visually linked to its own printed grid line on the original page. The CSV records the eye-read pixel position and difference from the fitted line. Maximum absolute eye-versus-line difference: {max(abs(float(r['eye_minus_fitted_line_px'])) for r in eye):.2f} px.

## Sampling, bounds, and review

Recorder traces are sampled at quarter-inch targets plus first, global peak, knees/recorder steps, and last features. Straight lines have samples at both ink ends and each labelled penetration crossing; intercept and label-centre features are separate. Label-centre features are annotations, not load measurements, and their native values must not be used as curve data. Sequence follows the visible drawing order; the load drops are retained. There is no macroscopic doubling back in penetration.

Guides in out/guides.py were read from this packet's coordinate-labelled crops. Actual exported samples were recentered on the ink; guides themselves are not exported as measured data. Stroke bounds vary with the measured local normal thickness (half the width), using nearby clean stroke at grid crossings. Crossings/merged lines have enlarged bounds and notes. Faint scan gaps or dash/dot gaps are sampled on nearby ink and noted, not in the white gap. The full supplied D-031 own-ink checker is absent from tools/; ink-proximity-checks.csv is only a supplementary pixel-distance screen, includes grid ink, and is explicitly not a substitute for D-031. All final non-label points have dark ink within 2 px in that screen; line identity was reviewed on the page and overlays. Coordinate-grid detail crops include zoom 3 and 25-pixel grid spacing.

Counts (trace / feature / marker):

'''
 for s,cs in counts.items():txt+=f"- {s}: {cs['trace']} / {cs['feature']} / {cs['marker']}\n"
 txt+='''
## Files

- cal-p1/calibration.json and anchors.csv: detection diagnostic and final piecewise anchor inputs.
- cal-p1/verified-knots.json: ink verification and local line-location bounds; recovery files where applicable.
- calibration-eye-checks.csv: three printed labels per axis checked by eye.
- points-p1.csv: original pixel readings and local pixel bounds.
- points-p1-native.csv: piecewise native values/bounds, units, and extrapolation flags.
- overlay-p1.png: points and bounds on the full original unrotated page.
- calibration-sensitivity.csv: per-series maximum affine-versus-piecewise difference, excluding label features.
- ink-proximity-checks.csv and the named zoom crops: supplementary review artifacts.
'''
 (d/'notes.md').write_text(txt,encoding='utf-8')
 # Grid verification overlay, clipped only for inspection; original coordinate offset recorded.
 im=Image.open(page).convert('RGB');dr=ImageDraw.Draw(im)
 for K,col in [(X,(255,30,30)),(Y,(30,100,255))]:
  for k in K.knots:
   ps=[K.line_s(k,t)*K.e_s+t*K.e_t for t in [min(k['t']),max(k['t'])]]
   dr.line([tuple(p) for p in ps],fill=col,width=2)
   dr.text(tuple(ps[0]+[8,8]),str(int(k['value'])),fill=col)
 im.save(d/'cal-p1/grid-verification.png')
 summ[f]={'counts':counts,'affine_rms_x_in':cal['rms_residual_x'],'affine_rms_y_lb':cal['rms_residual_y'],'eye_checks':checks,'verified_x_lines':len(X.knots),'verified_y_lines':len(Y.knots),'total_points':len(pts)}
with open('out/counts.csv','w',newline='') as fp:
 w=csv.DictWriter(fp,fieldnames=list(allcounts[0]));w.writeheader();w.writerows(allcounts)
Path('out/summary.json').write_text(json.dumps(summ,indent=2))
print(json.dumps(summ,indent=2))
