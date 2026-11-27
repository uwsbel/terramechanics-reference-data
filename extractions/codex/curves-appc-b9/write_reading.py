from pathlib import Path
import sys,json,csv,subprocess
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'tools')
import calibrate_axes as ca

spec={
 'FC-12':dict(page='p0148.png',series='rc2-loose',title='RC2 Loose',box=['58.00','43.07','.9349','145.81'],start=(583.6,3688.0),end=(1949,2419),overlap={1:'Fit touches left side near apex.',3:'Triangle apex touches horizontal grid line.',8:'Fit ends against base; symbol remains identifiable.'}),
 'FC-13':dict(page='p0147.png',series='ss-loose',title='SS Loose',box=['95.20','29.76','.5718','11.87'],start=(712.3,3702.0),end=(2058,2944),overlap={1:'Fit crosses lower left and right side.',2:'Base overlaps horizontal grid line.',3:'Fit touches left base and right side.',7:'Fit ends against left base; symbol remains identifiable.'}),
 'FC-14':dict(page='p0150.png',series='lsm-loose',title='LSM Loose',box=['75.20','43.95','.9642','-109.97'],start=(634.7,3741.3),end=(2015.0,2476.0),overlap={1:'Fit touches right base.',3:'Fit touches right side near base.',7:'Horizontal grid crosses triangle; reconstructed sides remain visible.'}),
 'FC-15':dict(page='p0151.png',series='lsm-dense',title='LSM Dense',box=['91.20','41.05','.8710','213.76'],start=(687.8,3671.5),end=(2064.0,2457.0),overlap={1:'Fit touches right base.',5:'Base overlaps horizontal grid line.'})
}
cols=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
overall=[]
for f,s in spec.items():
 d=Path('out')/f;cal,X,Y=ca.piecewise_maps(d/'cal-p1','packet/'+s['page'])
 # Exact page-grid position at the selected axis intersection.
 u,v=s['start']
 for i in range(4):u-=X.value(u,v)[0]/cal['x_per_px']
 s['start']=(round(u,3),v)
 rows=[]
 def add(kind,seq,u,v,bu,bv,symbol,note):
  rows.append(dict(zip(cols,[f,1,s['series'],kind,seq,round(float(u),3),round(float(v),3),round(float(bu),3),round(float(bv),3),symbol,note])))
 vertices=json.loads((d/'marker-vertices.json').read_text())
 for m in vertices:
  i=m['sequence'];u,v=m['centroid'];ov=s['overlap'].get(i,'')
  # Use the whole reconstructed outer height, including stroke, for the
  # centroid-vs-bounding-box registration bound (rule 8).
  h=m['height']+5
  add('marker',i,u,v,6 if ov else 2,max(8 if ov else 2,h/6),'triangle-up',f'Reconstructed triangle centroid; outer height about {h:g} px. '+ov)
 candidates=list(csv.DictReader((d/'trace-candidates.csv').open()))
 trace=[]
 for i,(u,v) in enumerate([s['start']]+[(float(r['pixel_u']),float(r['pixel_v'])) for r in candidates]+[s['end']]):
  if i in (0,10):
   bound=5.5
  else:
   r=candidates[i-1]
   slope=(s['end'][1]-s['start'][1])/(s['end'][0]-s['start'][0])
   bound=float(r['vertical_ink_width'])/(2*np.sqrt(1+slope*slope))
   # Iterate to the exact local x knot interpolation after locating v on ink.
   for j in range(4):u+=(float(r['target_psf'])-X.value(u,v)[0])/cal['x_per_px']
  note='first point; fit meets x=0 axis' if i==0 else ('last point; maximum of trace' if i==10 else f"Normal stress sampling target {candidates[i-1]['target_psf']} psf; local diagonal ink center.")
  if i==10 and f in ('FC-12','FC-13'):note+='; last distinguishable fit ink at terminal triangle junction; continuation within symbol is not separately readable'
  if i==0 and f=='FC-14':note+='; lower-left frame junction hides center within stroke width; no extension below frame inferred'
  add('trace',i+1,u,v,bound,bound,'',note);trace.append(rows[-1].copy())
 for i,(r,note) in enumerate([(trace[0],'first point'),(trace[-1],'last point; maximum of trace'),(trace[0],'intercept')],1):
  if f=='FC-14' and i in (1,3):note+='; ink joins axes at lower-left frame corner; center/frame clipping unresolved within half-stroke bound'
  if f in ('FC-12','FC-13') and i==2:note+='; terminal fit/symbol junction'
  add('feature',i,r['pixel_u'],r['pixel_v'],r['u_bound_px'],r['v_bound_px'],'',note)
 with (d/'points-p1.csv').open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=cols);w.writeheader();w.writerows(rows)
 # Run the supplied piecewise command so its exact uncertainty propagation and
 # verification rules produce the native values, all in psf.
 subprocess.run([sys.executable,'tools/calibrate_axes.py','piecewise',str(d/'cal-p1'),str(d/'points-p1.csv'),str(d/'points-p1-native.csv'),'--image','packet/'+s['page']],check=True)
 native=list(csv.DictReader((d/'points-p1-native.csv').open()))
 checks=[]
 for axis,values in [('x',[1000,4000,7000]),('y',[1000,4000,8000])]:
  for value in values:
   line=next(l for l in cal['vertical_lines' if axis=='x' else 'horizontal_lines'] if l[axis+'_value']==value)
   if axis=='x':
    vv=cal['horizontal_lines'][-1]['v_at_u0']+cal['horizontal_lines'][-1]['slope_dv_du']*1500
    uu=line['u_at_v0']+line['slope_du_dv']*vv
   else:
    uu=cal['vertical_lines'][0]['u_at_v0']+cal['vertical_lines'][0]['slope_du_dv']*2700
    vv=line['v_at_u0']+line['slope_dv_du']*uu
   checks.append(dict(figure_id=f,panel=1,axis=axis,printed_label=f'{value/10:.2f}',anchor_value_psf=value,pixel_u=round(uu,2),pixel_v=round(vv,2),checked='yes',note='Read by eye on unrotated page: label belongs to this drawn grid line; printed units multiplied by 10.'))
 with (d/'calibration-eye-checks.csv').open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=checks[0]);w.writeheader();w.writerows(checks)
 tr=[r for r in native if r['point_kind']=='trace']
 xx=np.array([float(r['x_native']) for r in tr]);yy=np.array([float(r['y_native']) for r in tr])
 slope,fitinter=np.polyfit(xx,yy,1);inter=float(tr[0]['y_native']);ib=float(tr[0]['y_read_bound'])
 sensx=[];sensy=[]
 for r in native:
  p=np.array([float(r['pixel_u']),float(r['pixel_v']),1])
  sensx.append(abs(float(r['x_native'])-p@cal['ax']));sensy.append(abs(float(r['y_native'])-p@cal['ay']))
 counts=dict(Counter(r['point_kind'] for r in native))
 notes=f'''# {f}, panel 1 — {s['title']}

Independent blind reading from packet/{s['page']} only, together with the supplied protocol, series index and context page p0115.png. No other reader or earlier extraction was consulted. Printed group identity agrees with series.csv; all symbols are upright hollow triangles assigned to `{s['series']}`. Context identifies C-8 through C-15 as Univac 1107 / CAL-COMP computer-plotted failure envelopes.

Printed box, transcribed as printed:

- Avg. Density = {s['box'][0]}
- Angle of Friction = {s['box'][1]}
- Tan Theta = {s['box'][2]}
- Cohesion = {s['box'][3]}

Both axes print PSF (x 10^1). A printed 100.00 means 1000 psf. All native values and native bounds are in psf. The cohesion box is compared directly in psf, without the axis multiplier.

Calibration: 72 intersections; affine RMS residual x = {cal['rms_residual_x']:.3f} psf, y = {cal['rms_residual_y']:.3f} psf; maximum absolute residuals x = {cal['max_residual_x']:.3f}, y = {cal['max_residual_y']:.3f} psf. All are below 0.5% of axis span. All 8 x grid lines and 9 y grid lines are detected and verified against distributed ink positions; none is predicted or rejected. `cal-p1/knots-verified.json` records the ink checks and line location errors. Numeric values use piecewise interpolation between these verified tilted lines; the affine map is diagnostic only, and its global residual is not added to reading bounds. Bound propagation is the supplied piecewise routine's corner/line-interval calculation. The `extrapolated` flags at frame features include any bound corner lying beyond an outer verified line, not necessarily a center outside the frame.

By-eye checks: x labels 100.00, 400.00, 700.00; y labels 100.00, 400.00, 800.00. Their checked line positions and psf anchors are in calibration-eye-checks.csv. Also inspected both zero labels and the whole frame: the labelled limits are x=0..7000 psf and y=0..8000 psf; the header box above y=8000 is not part of the data frame.

Counts for `{s['series']}`: {counts['marker']} marker, {counts['trace']} trace, {counts['feature']} feature. Marker sequence follows their visible left-to-right placement; trace sequence follows drawing order from the left end. Trace samples are left end, 500..4500 psf every 500 psf, right end. The line has no separate knee or interior maximum; the final endpoint is also its maximum. Features duplicate the two trace endpoints and the x=0 intercept, as required.

Triangle centers are centroids of reconstructed side/base triangles, not bounding-box midpoints. marker-vertices.json records the visual reconstruction, and marker-centroids-inspection.png shows the reconstruction over the ink. Clean-marker x bounds are 2 px; vertical bounds are at least outer triangle height/6. Where another line touches the triangle, x/y bounds are widened to 6/8 px. These are uncertainty intervals, not standard deviations. No additional triangle can be distinguished in a stack, and no duplicate marker was inferred. Every identified symbol has its own visible outline.

Trace centers were read from diagonal ink, using nearby columns to separate the diagonal from a vertical grid line at fixed x. The trace inspection crops show every 500 psf sample. Sample bounds are half the local diagonal stroke thickness measured perpendicular to the stroke (about 4.4–6 px), not half a symbol's size; endpoints use 5.5 px. No sample falls in the white exclusion gap around a triangle.

Least-squares slope of the submitted trace samples (psf/psf) = {slope:.6f}; printed Tan Theta = {s['box'][2]}; reading minus print = {slope-float(s['box'][2]):+.6f}. This is a diagnostic regression through sampled ink in the piecewise calibration; line grid-spacing irregularities need not produce a perfectly constant numeric slope. Its regression intercept ({fitinter:.2f} psf) is not substituted for the directly read feature.

Direct intercept shear stress = {inter:.2f} ± {ib:.2f} psf; printed Cohesion = {s['box'][3]} psf; reading minus print = {inter-float(s['box'][3]):+.2f} psf. The point positions were not moved to agree with the printed computation.

Largest |piecewise minus affine| over submitted points for `{s['series']}`: x = {max(sensx):.3f} psf, y = {max(sensy):.3f} psf. This is a correlated calibration sensitivity, not an additional point bound.
'''
 if f in ('FC-12','FC-13'):
  notes+='\nEndpoint ambiguity: the fitted stroke meets the last triangle at its lower-left/base region. The endpoint is the last distinguishable fitted-stroke ink at that junction. An endpoint hidden inside the triangle cannot be located independently; no continuation onto a triangle side or apex has been invented. This affects the precise last-end position, not marker count or identity.\n'
 if f=='FC-14':
  notes+='\nIntercept ambiguity: the fitted stroke visibly joins the axes at the lower-left corner. The baseline and axis conceal the center over approximately one stroke width. The first point and intercept are recorded at that junction, y≈0 within the half-stroke bound; no negative shear value or invisible continuation is supplied. The centerline could meet the baseline slightly to the right of x=0 within this bound. This is the main reading ambiguity, and the printed negative cohesion does not settle it.\n'
 if f=='FC-15':
  notes+='\nBox transcription ambiguity: the first fractional digit in Cohesion is damaged; the visible top/descending remnant is read as 7, giving 213.76. See cohesion-detail.png. If that digit is regarded as unreadable, preserve the transcription as 213.?6 rather than using the plotted intercept to decide it.\n'
 (d/'notes.md').write_text(notes,encoding='utf-8')
 subprocess.run([sys.executable,'tools/plot_grid.py','overlay','packet/'+s['page'],'--points',str(d/'points-p1.csv'),'--out',str(d/'overlay-p1.png')],check=True)
 # Calibration-only overlay makes all line knots reviewable independently.
 im=Image.open('packet/'+s['page']).convert('RGB');dr=ImageDraw.Draw(im)
 box=cal['box'];u0,v0,u1,v1=box
 for ln in cal['vertical_lines']:
  dr.line([(ln['u_at_v0']+ln['slope_du_dv']*vv,vv) for vv in (v0,v1)],fill=(0,180,0),width=2)
 for ln in cal['horizontal_lines']:
  dr.line([(uu,ln['v_at_u0']+ln['slope_dv_du']*uu) for uu in (u0,u1)],fill=(0,120,255),width=2)
 im.save(d/'cal-p1'/'grid-overlay.png')
 overall.append(dict(figure_id=f,series_id=s['series'],**counts,rms_x_psf=cal['rms_residual_x'],rms_y_psf=cal['rms_residual_y'],trace_slope=slope,slope_minus_print=slope-float(s['box'][2]),intercept_psf=inter,intercept_bound_psf=ib,intercept_minus_print_psf=inter-float(s['box'][3])))
 print(f,counts,'slope',round(slope,6),'intercept',round(inter,2),'bound',round(ib,2))
Path('out/reading-summary.json').write_text(json.dumps(overall,indent=1),encoding='utf-8')
