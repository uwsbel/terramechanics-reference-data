import sys,csv,json,math
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca

def writecsv(p,rows):
 with Path(p).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

EYES={
'F2-42': [('x',x,u,3200) for x,u in [(0,843),(1,1152),(2,1462),(3,1764)]]+ [('y',y,1600,v) for y,v in [(0,3354),(200,3041),(600,2422),(800,2111),(1000,1801),(1200,1489)]]+[('y',400,1100,2732)],
'F2-44': [('x',x,u,3250) for x,u in [(0,748),(1,1057),(2,1363),(3,1674),(4,1981),(5,2292)]]+[('y',y,2250,v) for y,v in [(0,3250),(500,2860),(1000,2470),(1500,2084)]]+[('y',2000,800,1704),('y',2000,2200,1697)]
}

NOTES42='''# Blind reading: F2-42, panel 1

Only packet/p0102.png, packet/p0099.png and the supplied protocol/index rows were used. All coordinates refer to the unrotated 3263 by 4558 page. No other reading was consulted.

## Identity and printed key

- A, lpt22, is **dotted**. Circled A lies beside the dotted recovery branch, which can be followed down to the lower of the two modest first peaks. Printed: LPT No. 22 (130), gamma 51.2 pcf, rate 4 inches/minute.
- B, lpt23, is **solid**, the upper shelf-bearing trace beside circled B. Printed: LPT No. 23 (99), gamma 50.6 pcf, rate 1 inch/minute.
- C, lpt24, is **short-dashed**, beside circled C on the steeper recovery branch. Its first peak is above A's. Printed: LPT No. 24 (83), gamma 51.5 pcf, rate 1 inch/minute.
- D, lpt25, is **long-dashed**, identified beside circled D near the top. Printed: LPT No. 25 (130), gamma 51.6 pcf, rate 2 inches/minute. Parentheses contain Gp. No index identity correction was required.

The circles are letter labels, not plotted markers. There are no marker observations. Protocol rules 8 and 9 do not apply to these unmarked recorded traces.

## Calibration

Both axes are linear, penetration right and load up. Verified knots: x = 0,1,2,3 inches; y = 0,200,400,600,800,1000,1200 lb. The 627 tick is a value annotation, not a knot. The upper frame is unlabelled and is not a knot. Accordingly the portions above 1200 lb, including the C and D frame endpoints, have extrapolated y values explicitly flagged in cal_model.

The first detect pass contaminated the 400-lb fit with inset text. The final fit reads its visible segment left of the inset; covered intersections are not y anchors. Curve crossings and inset/frame outliers were excluded from the grid fits. Original detection is retained as cal-p1/calibration-detect.json. Every final knot passed the protocol's image-based ink check; see verified-knots.json. Values and bounds in points-p1-native.csv are piecewise between these knots, with each knot's location interval propagated, and with no global affine residual added. calibration-sensitivity.csv gives the affine-to-piecewise diagnostic by series.

calibration-eye-checks.csv checks **every printed grid label**, exceeding three per axis. Each row records a hand-read line centre on the image and its difference from the fitted line. In particular 1200 belongs to the line near v=1489, not the frame near v=1334; 600 belongs to v=2422, not the adjacent 627 tick.

## Following ink, features and uncertainty

The four initial strokes overlap or are closely interleaved below about 800 lb. Individual centres and starts are not fully resolved. Bounds cover the neighboring strokes there; identical/nearby ink centres do not establish separate observations. The first feature/trace points are the visible ink at the bottom frame, with the slight lateral spread retained rather than forcing native x to exactly zero.

A and C cross near (1295,2020), approximately 1.5 inches and 860 lb. D crosses B near (1360,1666), about 1.7 inches and 1086 lb. These neighborhoods carry explicit notes and widened bounds. D and B are also coalescent along part of the initial rise.

A's dots approach and terminate against C around (1618,1530), approximately 2.52 inches and 1174 lb. No independent dotted continuation can be resolved above this junction. A is ended at the last identifiable dotted ink and is not extended along C to the frame. This termination is an identity ambiguity, not evidence that the two tests became one trace. C continues to (1740,1334); D continues to (1618,1334), where each meets the frame. B stops inside the plot near (1497,1597).

B's shelf changes by less than the stroke width. Its peak and subsequent minimum rows document the first shelf maximum and shallow shelf-end depression, but no distinct load drop is resolved. D is monotone within the reading bounds and has no separate first local maximum/minimum pair. All four highest loads occur at their final points, so no additional global-peak duplicate is needed. First/last points are represented in both trace and feature kinds; counts must not be added as independent tests.

Trace targets are every 0.25 inch, supplemented by every 100 lb on the initial steep rise. A target in a dot/dash gap or grid intersection moves to nearby stroke ink and retains its actual native coordinates; note records the move. Coincident targets use one trace row. Feature rows retain drawing order. No resolved unloading loop or x reversal is present.

Point-local transverse stroke widths were measured on the original scan. Bounds begin with half that width, include half a local dash/dot gap along the stroke, and widen for crossings/overlap. sampling-audit.csv records the measured half-width and half-gap per row. Guides in ../read_curves.py select corridors only; interpolated white-gap positions are never output as observations. An image centre being black is necessary, not a sufficient proof of identity, so label-adjacent points and the two crossings were also visually checked on enlarged pixel-grid crops.

The packet does not supply check_trace_ink.py (D-031/D-032). It could not be run. Local ink checks are in ink-checks.csv and do not claim to reproduce that missing checker. Frame intersections and unresolved initial overlaps are explicitly identified for later comparison. All rows have positive reading bounds. No software was installed.

Overlay colours: A/lpt22 red, B/lpt23 green, C/lpt24 blue, D/lpt25 orange. overlay-p1.png has the original page dimensions; overlay-plot.png is its plot crop. Enlarged grid crops, calibration files, sensitivity and sampling/ink audits are retained alongside the requested outputs.
'''

NOTES44='''# Blind reading: F2-44, panel 1

Only packet/p0104.png, packet/p0099.png and the supplied protocol/index rows were used. Coordinates refer to the unrotated 3213 by 4508 page. No other reading was consulted. Context page 99 describes bin-size tests in dense RS with mean relative density about 0.96; no point was taken from its text.

## Identity and printed key

The key prints A = 18 inch by 36 inch bin; B = 36 inch by 36 inch bin; C = 54 inch by 36 inch bin. Gp values are in parentheses.

- lpt24: A LPT No. 24 (83), **dashed**, identified by the lower curved arrow pointing to the rightmost initial dashed rise. It reaches the broad first peak near 0.9 inch, has a shallow trough around 1.45 inches, then the shallower dashed recovery ending around 3.02 inches and 1340 lb.
- lpt73: A LPT No. 73 (117), **dashed**, identified by its printed along-line label beside the steep dashed recovery. It has the earlier first peak and minimum around 1 inch; its steep branch ends around 2.96 inches and 1791 lb. It is distinguished from 24 by the arrow, the intervening peak/trough geometry, and continuity through their early crossing, not by assigning them different styles.
- lpt74: B LPT No. 74 (103), **dotted**, identified by the upper of the two lower arrows, pointing beside the dotted trough. Follow its dots through the crossings; its final dot is around (2107,1867), 4.44 inches and 1780 lb. It is not continued up either solid line.
- lpt69: C LPT No. 69 (103), **solid**, identified by the upper solid recovery's along-line label. This is the higher initial peak, then the shallower trough, and finally the rightmost endpoint around (2185,1835).
- lpt64a: C LPT No. 64A (112), **solid**, identified by the label beside the lower solid recovery. This is the lower initial solid peak, the deep trough near 1.87 inches, and the steeper final solid branch ending around (2077,1840).

All supplied ids are retained; no printed-label discrepancy was found. No symbols are plotted. Text/arrowheads, incidental short strokes and grid intersections are not markers. Protocol rules 8 and 9 do not apply to these unmarked recorded traces.

## Calibration

Linear axes, penetration right and load up. Verified knots: x = 0,1,2,3,4,5 inches; y = 0,500,1000,1500,2000 lb. The key covers the middle of the 2000-lb line. Its final fit uses the visible left and right segments, with no key lettering admitted as grid ink. The original detect result is retained separately. Every final grid line passed the image-based verification; see cal-p1/verified-knots.json.

calibration-eye-checks.csv records every printed label (more than three per axis), with two visible-segment checks for the 2000 line. Values and reading bounds use the verified piecewise map with its individual knot location intervals. The affine residual is only a diagnostic and is not added to each bound. calibration-sensitivity.csv records the affine-to-piecewise differences by series.

## Crossings and uncertain parts

Initial curves are closely superposed, particularly the four leftmost strokes. The visible curve ink begins around (747--763,3130--3144), near zero penetration but roughly 140--160 lb, **above the zero-load frame**. No independent continuation to (zero penetration, zero load) is visible. Starts are reported on that visible ink with widened bounds; the separate first points for the overlapping traces are not independently resolved.

The two dashed curves cross around 0.6--0.75 inch, near 850--900 lb; 24 also passes the descending dotted 74 branch nearby. The descending 64A solid branch crosses the steep dashed 73 branch and then dashed 24/dotted 74 in the region about 1.1--1.4 inches. The descending 69 branch crosses the steep dashed 73 branch before reaching its trough. Branch continuity and labels preserve the identities through these crossings, including the crossing between two traces of the same style.

After the trough of 69, the 24/74/69 recovery strokes are nearly coincident over roughly 1.5--2 inches. Individual centres cannot be separated reliably in the thick merged ink. Rows there explicitly say so and carry wider bounds; the hidden dotted/dashed continuation is not treated as a distinct new solid observation.

On the upper recoveries, 64A crosses the dotted 74 branch around 3.7--3.8 inches and crosses solid 69 around 3.8--3.9 inches. Dotted 74 subsequently crosses 69 near 4 inches. These intersections are partly thickened or coincident; samples in that region have widened bounds. Endpoints are followed to their own final dash/dot or solid ink. The small horizontal strokes near the printed labels, and the lower curved arrow shafts, are not continuations.

First local peaks and subsequent troughs are feature rows for all five traces. The apex of dashed 24 falls between adjacent dash ends: its feature is on the high visible dash end with the gap included in the bound, rather than being placed in white space. Broad knees on the recoveries are also recorded. Every trace has its highest load at its endpoint, so a separate global-peak duplicate is unnecessary. First/last ink is represented as both trace and feature, not counted as independent observations.

Trace targets are every 0.25 inch, supplemented by 100-lb targets on the initial steep rise. Targets in dash/dot gaps or a grid stroke move to nearby trace ink and keep the resulting measured coordinates. Coincident targets share a trace row. The final 24 dash supplies both the 3-inch target and the last-ink sample. The sequence follows drawing order; no resolved physical x reversal or unloading loop was found.

Bounds start with half a transverse stroke width measured locally on the original page. A dashed/dotted stroke additionally includes half its neighboring gap along the stroke, and overlap/crossing neighborhoods receive wider bounds. sampling-audit.csv preserves these measurements. The manual guides in ../read_curves.py only select an ink corridor. A black pixel alone does not establish a trace's identity: enlarged pixel-grid crops were inspected for the arrows, same-style crossings and upper endpoints.

check_trace_ink.py is named in the protocol but absent from the supplied tools, so D-031/D-032 could not be executed. ink-checks.csv contains the local ink audit, not a claim to have run that missing program. Initial overlaps and merged strokes remain reading ambiguities, with the wide bounds and notes retained. No software was installed.

Overlay colours: 24 red, 73 green, 74 blue, 69 orange, 64A purple. overlay-p1.png retains the full page dimensions; overlay-plot.png is its plot crop. Calibration, enlarged pixel-grid crops and sensitivity/sampling/ink audits are retained with the requested files.
'''

def main(fig,page,notes):
 folder=Path('out')/fig
 cal,X,Y=ca.piecewise_maps(folder/'cal-p1','packet/'+page+'.png')
 checks=[]
 for axis,val,u,v in EYES[fig]:
  ln=next(z for z in cal['vertical_lines' if axis=='x' else 'horizontal_lines'] if z[axis+'_value']==val)
  fitted=ln['u_at_v0']+ln['slope_du_dv']*v if axis=='x' else ln['v_at_u0']+ln['slope_dv_du']*u
  eye=u if axis=='x' else v
  checks.append(dict(figure_id=fig,panel=1,axis=axis,label_printed=str(val),grid_value=val,eye_pixel_u=u,eye_pixel_v=v,fitted_coordinate_px=round(fitted,3),eye_minus_fit_px=round(eye-fitted,3),result='checked by eye; matches line',note=('2000 line checked on visible segment outside key' if axis=='y' and val==2000 else 'printed label checked against grid ink; coordinates on unrotated page')))
 writecsv(folder/'calibration-eye-checks.csv',checks)
 (folder/'notes.md').write_text(notes,encoding='utf-8')
 rows=list(csv.DictReader((folder/'points-p1.csv').open()))
 count=Counter((r['series_id'],r['point_kind']) for r in rows)
 writecsv(folder/'counts.csv',[dict(series_id=s,point_kind=k,count=n) for (s,k),n in count.items()])
 g=np.array(Image.open('packet/'+page+'.png').convert('L'))
 audit=[]
 for r in rows:
  u,v=float(r['pixel_u']),float(r['pixel_v']);uu,vv=round(u),round(v)
  patch=g[vv-2:vv+3,uu-2:uu+3]
  b=np.argwhere(patch<150)
  dist=min([math.hypot(uu+q[1]-2-u,vv+q[0]-2-v) for q in b] or [float('inf')])
  audit.append(dict(series_id=r['series_id'],point_kind=r['point_kind'],sequence=r['sequence'],center_gray=int(g[vv,uu]),nearest_original_ink_px=round(dist,3),on_ink_within_2px=dist<=2,identity_check='manual corridor and overlay; overlap ambiguous where noted',limitation='local image audit; D-031 checker absent'))
 writecsv(folder/'ink-checks.csv',audit)
 assert all(r['on_ink_within_2px'] for r in audit)
 assert all(float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0 for r in rows)
 for sid in sorted(set(r['series_id'] for r in rows)):
  rr=[r for r in rows if r['series_id']==sid]
  assert [int(r['sequence']) for r in rr]==list(range(1,len(rr)+1))
  assert sum(r['point_kind']=='feature' and r['note'].startswith('first;') for r in rr)==1
  assert sum(r['point_kind']=='feature' and r['note'].startswith('last;') for r in rr)==1
 # Retain a high-resolution plot crop for review; the primary overlay is full-page.
 im=Image.open(folder/'overlay-p1.png')
 box=(810,1300,1790,3380) if fig=='F2-42' else (710,1780,2320,3280)
 im.crop(box).save(folder/'overlay-plot.png')
 print(fig,'rows',len(rows),'ink checks',len(audit),'eye checks',len(checks),'largest eye deviation',max(abs(z['eye_minus_fit_px']) for z in checks),'rms',cal['rms_residual_x'],cal['rms_residual_y'],'max',cal['max_residual_x'],cal['max_residual_y'])

if __name__=='__main__':
 main('F2-42','p0102',NOTES42)
 main('F2-44','p0104',NOTES44)
