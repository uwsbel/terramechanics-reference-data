import csv,json
from pathlib import Path
base=Path('out/FC-6B');checks={1:{'x':(2100,[(0,642),(50,958),(100,1247),(150,1528),(200,1821),(250,2115)]),'y':(640,[(4000,925),(3000,1216),(2000,1511),(1000,1802),(0,2102)])},2:{'x':(3278,[(0,647),(50,963),(100,1251),(150,1534),(200,1825),(250,2123)]),'y':(646,[(50,2246),(0,2391),(-300,3277)])}}
rows=[]
for panel,axes in checks.items():
 c=json.loads((base/f'cal-p{panel}/calibration.json').read_text())
 for axis,(ref,pts) in axes.items():
  ls=c['vertical_lines' if axis=='x' else 'horizontal_lines']
  for value,eye in pts:
   l=next(l for l in ls if l['x_value' if axis=='x' else 'y_value']==value);fit=l['u_at_v0']+l['slope_du_dv']*ref if axis=='x' else l['v_at_u0']+l['slope_dv_du']*ref
   rows.append(['FC-6B',panel,axis,value,f'{fit:.2f} at '+('v=' if axis=='x' else 'u=')+str(ref),eye])
with (base/'calibration-eye-checks.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['figure','panel','axis','printed_label','fitted_pixel','eye_pixel']);w.writerows(rows)
(base/'notes.md').write_text('''# FC-6B independent reading

Evidence: packet/p0132.png and supplied protocol/index only. No other extraction consulted. Coordinates on unrotated 3213 x 4221 page.

Legend confirmed: up triangle 4695/73.0; square 3815/71.1; down triangle 2934/71.1; circle 1761/71.1; plus 734/71.1. The upper unlabeled frame is about 4500 psf, not 5000; fit uses labeled 0 through 4000 lines. Lower frame is +50 to -300 thousandths inch. Horizontal lines are drawn only at +50, 0 and -300. The intermediate predicted tool lines are nominal scale positions, not observations: their synthetic anchors were excluded with ../prune_predicted.py. All three actual horizontal lines confirmed. The -100 printed label/leader sits noticeably above its nominal -100 location (roughly 30 px); the -200 label is close to its nominal position. Calibration follows the three drawn horizontal lines, with this printed-label inconsistency flagged.

Eye checks: all six displacement grid lines and 0/1000/2000/3000/4000 upper levels; all six lower displacement grid lines and +50/0/-300 lower levels, recorded in calibration-eye-checks.csv. Displacement grid is intrinsically nonuniform: 0-to-50 is about 318 px, later bays about 280-298 px. Initial upper calibration min-frac .55 gave RMS x 1.452, y 7.916; changing box and min-frac to .4 gives x 1.463, y 8.029. Eye checks show correct lines in both runs. P2 RMS x 1.345, y 0.243 after dropping synthetic intersections. Thus x residual is 0.585% upper and 0.538% lower, above the 0.5% protocol threshold. This cannot be removed with detection thresholds without ignoring the visibly nonuniform printed grid; retain the full-span affine map and include its residual in every native reading bound. This is an explicit calibration limitation requiring later review, not a claim that threshold compliance was achieved.

Every identifiable marker is retained. Upper up-triangle series has 11 markers; other upper series have 12. Lower identifiable series each have 13 markers. No square can be identified in the lower panel: n3815 is omitted, not reassigned from another symbol. Missing square observations are noted for roughly x=0,15,35,50,70,90,110,130,150,170,190,220,250 (whole 0-250 span; potential contraction region -200 to -300). There is no fifth visible horizontal symbol row. If squares are superposed on triangles, their separate outline cannot be resolved on this scan.

Lower up/down triangles are separated enough to identify their orientations. Several lie against the vertical grid lines and frame; widened bounds and row notes cover these. Plus and circle rows are separate. No connecting lower curves are drawn; scattered short dashes near markers are scratches/printing remnants and not sampled as traces.

Markers read from labeled zoom-3 crops, then refined using enclosed white interiors where clean. Upper first up-triangle and square curves share their steep starting stroke near u710-810; individual initial line emergence is uncertain, and feature bounds retain half the thick ink. Upper markers sometimes sit off the fitted curve (e.g. square near u1163); these are kept separately. Endpoint crops at zoom 3/4 locate the last ink before the last marker, not the marker center.

Trace values are actual dark-run centers, with bounds half their vertical thickness. Manually read paths select which run belongs to the curve; no interpolated guide ordinate is written. Sampling every 20 px within ink intervals is finer than 5 thousandths. Intervals interrupted by marker exclusion/dash gaps are not bridged, so spacings over 5 occur around symbols. Vertical grid columns are avoided. At horizontal grid crossings, merged thick ink is retained with its larger thickness bound; especially upper up-triangle crossing 4000 psf near u1700-1760 and circle crossing 1000 psf near u950. These points cannot separate grid ink from curve ink precisely. Peaks on rising series are the last visible ink level; first/peak/last feature records are separate roles even when coincident. Broad flat peaks have wide horizontal bounds.

Files: cal-p1/anchors.csv and calibration.json; cal-p2/anchors.csv and calibration.json; calibration-eye-checks.csv; points-p1.csv, points-p1-native.csv, points-p2.csv, points-p2-native.csv; overlay-p1.png, overlay-p2.png; counts.csv. readings.json, crops, and helper scripts retained for audit/reproduction.
''')
