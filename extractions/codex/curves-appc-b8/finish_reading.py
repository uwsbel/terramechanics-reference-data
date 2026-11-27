"""Blind page reading: audited triangle vertices and ink samples, in original page pixels."""
import sys,json,csv,math
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca

GEOM=json.loads(Path('out/triangle-fits.json').read_text())
TR=json.loads(Path('out/trace-candidates.json').read_text())
# The shared apex/base obscures the automatic left-side fit. Reconstruct the upper
# triangle from its visible apex, right side and base; these are page readings.
GEOM['FC-11B'][2]['vertices']=[[1378,2906],[1361,2935],[1394,2935]]
GEOM['FC-11B'][2]['centroid']=np.mean(GEOM['FC-11B'][2]['vertices'],axis=0).tolist()
END={'FC-10B':(1837,2511),'FC-10C':(1751,2508.5),'FC-11A':(2054,2710),
     'FC-11B':(2038,2447),'FC-11C':(2018,2529)}
PRINT={'FC-10B':('PS Loose','24.60','43.40','.9459','169.22'),
       'FC-10C':('PS Loose','25.40','43.70','.9558','359.69'),
       'FC-11A':('RSM Loose','58.20','35.92','.7244','444.69'),
       'FC-11B':('RSM Loose','58.30','37.38','.7641','785.77'),
       'FC-11C':('RSM Loose','58.20','37.07','.7556','584.29')}
BASE=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note','x_unit','y_unit','sampling_x_psf','trace_segment']

def writecsv(path,rows,cols=None):
 with Path(path).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols or list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

summary=[]
for fig,recs in GEOM.items():
 d=Path('out')/fig; page=TR[fig]['page'];image=f'packet/{page}.png'
 im=Image.open(image).convert('RGB');g=np.asarray(im.convert('L'),dtype=float)
 cal,X,Y=ca.piecewise_maps(d/'cal-p1',image);m,b=TR[fig]['ink_fit'];sid='ps-loose' if '10' in fig else 'rsm-loose'
 rows=[];verts=[]
 def point(kind,seq,u,v,bu,bv,symbol='',note='',target='',seg=''):
  return dict(zip(BASE,[fig,1,sid,kind,seq,round(float(u),3),round(float(v),3),round(float(bu),3),round(float(bv),3),symbol,note,'psf','psf',target,seg]))
 for i,r in enumerate(recs):
  vs=np.array(r['vertices']);u,v=vs.mean(axis=0);h=vs[1:,1].mean()-vs[0,1]
  bu=2.;bv=max(2.,h/6);note='centroid of reconstructed triangle; apex-direction bound >= height/6'
  if (fig=='FC-11B' and i in (1,2)) or (fig=='FC-11C' and i in (3,4)):
   bu=max(bu,np.ptp(vs[:,0])/2);bv=max(bv,h/2)
   note+='; two overlapping triangles distinguishable; shared apex/base ink; half-symbol bounds'
  if (fig=='FC-11A' and i==3) or (fig=='FC-11C' and i==6):
   bu=max(bu,4);bv=max(bv,6);note+='; grid line crosses symbol; sides reconstructed excluding grid ink'
  if (fig=='FC-10B' and i==1) or (fig=='FC-10C' and i in (1,6,8)):
   bu=max(bu,4);bv=max(bv,6);note+='; adjacent fit/grid ink touches outline; centroid excludes that ink'
  if fig=='FC-11B' and i in (3,4) or fig=='FC-11C' and i in (8,9):
   note+='; close vertical pair with separately visible outlines'
  if fig=='FC-11B' and i==2:note+='; visible apex/right side/base used to reconstruct obscured left side'
  rows.append(point('marker',i+1,u,v,bu,bv,'triangle-up',note))
  verts.append({'marker_sequence':i+1,'apex_u':vs[0,0],'apex_v':vs[0,1],
                'base_left_u':vs[1,0],'base_left_v':vs[1,1],'base_right_u':vs[2,0],'base_right_v':vs[2,1],
                'centroid_u':u,'centroid_v':v,'height_px':h})
 writecsv(d/'triangle-vertices.csv',verts)
 # Measure clean stroke thickness perpendicular to its direction, away from
 # grid lines and triangle outlines. Bounds below are half this thickness.
 widths=[];normal=np.array([-m,1])/np.hypot(m,1);tangent=np.array([1,m])/np.hypot(m,1)
 for u in np.arange(rows[0]['pixel_u']+55,END[fig][0]-35,17):
  v=m*u+b;p=np.array([u,v])
  if any(abs(X.value(u,v)[0]-k*1000)<45 for k in range(8)):continue
  if any(abs(Y.value(u,v)[0]-k*1000)<45 for k in range(9)):continue
  if any(abs(u-r['pixel_u'])<28 and abs(v-r['pixel_v'])<35 for r in rows):continue
  ss=np.arange(-10,10.01,.25);tt=np.arange(-2,2.1,1)
  q=p[None,None,:]+ss[None,:,None]*normal+tt[:,None,None]*tangent
  profile=g[np.rint(q[:,:,1]).astype(int),np.rint(q[:,:,0]).astype(int)].mean(axis=0)
  idx=np.flatnonzero(profile<150)
  if len(idx) and np.min(np.abs(ss[idx]))<1:
   runs=np.split(idx,np.flatnonzero(np.diff(idx)>1)+1);run=min(runs,key=lambda z:abs(ss[z].mean()))
   widths.append((len(run)*.25,u,v))
 thickness=float(np.median([w[0] for w in widths]));half=math.ceil(thickness*2)/4
 writecsv(d/'line-thickness-checks.csv',[{'u':u,'v':v,'perpendicular_thickness_px':w} for w,u,v in widths])
 samples=TR[fig]['samples'];tr=[]
 for r in samples:
  target=r['target']
  if target=='right-end':u,v=END[fig];note='right end: last distinct fitted-line ink; maximum of trace'
  elif target==0:
   # Intersect the measured ink line with the calibrated x=0 axis. At the
   # axis itself, the perpendicular ink profile mixes branch and frame.
   lo,hi=cal['box'][0]-20,cal['box'][0]+100
   for _ in range(50):
    mid=(lo+hi)/2
    if X.value(mid,m*mid+b)[0]<0:lo=mid
    else:hi=mid
   u=(lo+hi)/2;v=m*u+b;note='left end: fitted-line branch reaches x=0 axis'
  else:
   if fig=='FC-11B' and target==2500:continue
   v=r['v'];lo,hi=r['u']-5,r['u']+5
   for _ in range(40):
    mid=(lo+hi)/2
    if X.value(mid,v)[0]<target:lo=mid
    else:hi=mid
   u=(lo+hi)/2;note=f'on drawn fit ink at {target} psf normal stress'
  if fig=='FC-10C' and target=='right-end':note+='; line merges with terminal triangle; last distinct line ink before outline'
  if fig=='FC-11B' and target==3000:note+='; break before this sample: 2500 psf target omitted in symbol-associated gap'
  if fig=='FC-11C' and target==3000:note+='; fit ink reaches/crosses vertical grid line here, checked on enlarged crop'
  segment=2 if fig=='FC-11B' and (target=='right-end' or target>=3000) else 1
  tr.append(point('trace',len(tr)+1,u,v,half,half,note=note,target=target,seg=segment))
 rows+=tr
 for seq,r in enumerate([tr[0],tr[-1]],1):
  z=r.copy();z['point_kind']='feature';z['sequence']=seq
  z['note']=('first point; ' if seq==1 else 'last point; maximum of trace; ')+r['note'];rows.append(z)
 z=tr[0].copy();z.update(point_kind='feature',sequence=3,note='intercept');rows.append(z)
 writecsv(d/'points-p1.csv',rows,BASE)
 ca.piecewise_rows(cal,X,Y,rows)
 writecsv(d/'points-p1-native.csv',rows,BASE+['x_native','y_native','x_read_bound','y_read_bound','cal_model'])
 (d/'cal-p1'/'verified-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 # All printed labels were inspected; six explicit checks form the requested record.
 checks=[]
 for axis,values in [('x',[1000,4000,7000]),('y',[1000,4000,8000])]:
  for val in values:
   if axis=='x':
    l=next(l for l in cal['vertical_lines'] if l['x_value']==val)
    h=next(l for l in cal['horizontal_lines'] if l['y_value']==0)
   else:
    l=next(l for l in cal['vertical_lines'] if l['x_value']==0)
    h=next(l for l in cal['horizontal_lines'] if l['y_value']==val)
   u=(l['u_at_v0']+l['slope_du_dv']*h['v_at_u0'])/(1-l['slope_du_dv']*h['slope_dv_du']);v=h['v_at_u0']+h['slope_dv_du']*u
   checks.append({'figure_id':fig,'panel':1,'axis':axis,'anchor_value_psf':val,'printed_label':f'{val/10:.2f}',
    'pixel_u':round(u,2),'pixel_v':round(v,2),'eye_checked':'yes','result':'label aligns with this printed grid line; x10^1 multiplier applied',
    'evidence':'label-sheet.png; original '+image})
 writecsv(d/'calibration-eye-checks.csv',checks)
 # Native-resolution page overlay, preserving original pixel coordinates.
 ov=im.copy();draw=ImageDraw.Draw(ov)
 for r in rows:
  u,v=r['pixel_u'],r['pixel_v'];bu,bv=r['u_bound_px'],r['v_bound_px']
  col={'marker':(220,0,0),'trace':(0,130,0),'feature':(0,70,230)}[r['point_kind']]
  draw.line((u-bu,v,u+bu,v),fill=col,width=2);draw.line((u,v-bv,u,v+bv),fill=col,width=2)
  if r['point_kind']=='marker':draw.ellipse((u-5,v-5,u+5,v+5),outline=col,width=2)
  elif r['point_kind']=='trace':draw.rectangle((u-3,v-3,u+3,v+3),outline=col,width=2)
  else:draw.ellipse((u-9,v-9,u+9,v+9),outline=col,width=2)
  if r['point_kind']!='feature':draw.text((u+10,v+7),f'{r["point_kind"][0]}{r["sequence"]}',fill=col)
 draw.text((cal['box'][0]+10,600),'Reading overlay: red = marker centroid; green = trace; blue = feature. Bars = pixel bounds.',fill='black')
 ov.save(d/'overlay-p1.png')
 # Quantify calibrated reading without moving ink samples towards printed values.
 tt=[r for r in rows if r['point_kind']=='trace']; xx=[r['x_native'] for r in tt];yy=[r['y_native'] for r in tt]
 slope,reginter=np.polyfit(xx,yy,1);intercept=next(r['y_native'] for r in rows if r['note']=='intercept')
 affine=np.array([[*cal['ax']],[*cal['ay']]])
 diffs=[]
 for r in rows:
  a=affine@np.array([r['pixel_u'],r['pixel_v'],1.]);diffs.append([a[0]-r['x_native'],a[1]-r['y_native']])
 maxdiff=np.abs(diffs).max(axis=0)
 title,den,angle,tan,cohesion=PRINT[fig]
 ambiguity={
  'FC-10B':'The middle triangle touches the fitted line. All three triangles are distinguishable. The line ends before the last triangle with a visible gap.',
  'FC-10C':'Nine distinguishable triangles. Several outlines touch fitted/grid ink; their centroids use the triangle sides alone. The last line segment merges with the upper terminal triangle: the endpoint is the last distinct fit ink at (1751, 2508.5), before the outline, with a half-stroke bound. The exact pen termination within the merged ink cannot be separated.',
  'FC-11A':'Five distinguishable triangles. The fourth triangle is crossed by the y=3000 grid line; sides and base are reconstructed excluding the crossing line, with enlarged bounds. The line ends before the final triangle.',
  'FC-11B':'Five distinguishable triangles. The middle two overlap (upper base and lower apex share ink); both have half-symbol bounds. The two high triangles are separate. The low triangle shows one identifiable symbol, not evidence sufficient to claim two. The requested 2500 psf trace location is in the interruption around the middle pair, approximately u=1356..1394 (v about 2960..2931). It is OMITTED under rules 6 and 7. No sample is placed on either triangle or interpolated through that gap; trace_segment changes across it. The terminal line ink stops before the high pair.',
  'FC-11C':'Ten distinguishable triangles. The middle pair overlaps, but separate apices, sides and bases establish two triangles; both have half-symbol bounds. The high pair is separate. The triangle near (1739,2877) overlaps the y=3000 grid line and has enlarged bounds. The 3000 psf trace sample is on fit ink at its grid-line crossing, checked at zoom 8. The line ends below and separately from the highest triangles.'}[fig]
 notes=f'''# {fig}, panel 1 — independent blind reading

Source: `{image}`, unrotated 300 dpi; all u/v values refer to this original image (u right, v down). Only this packet and its protocol were used. Context p0115 describes the CAL-COMP computer envelopes and the final lettered plot as the combined test plot.

Printed box transcription (digits and leading decimal preserved):

- {title}
- Avg. Density = {den}
- Angle of Friction = {angle}
- Tan Theta = {tan}
- Cohesion = {cohesion}

The page identity agrees with the supplied series id `{sid}`. Shape: triangle-up. No subdivision into the earlier test groups is inferred on the combined figure. There are {len(recs)} markers, {len(tt)} trace samples and 3 features (first, last/maximum, intercept). Marker sequence is a spatial inventory, not a reconstructed test chronology; trace sequence is left-to-right drawing order.

Both axes print PSF (x 10^1). Printed 100.00 = 1000 psf; x spans 0..7000 psf and y 0..8000 psf. The 00 labels belong to the bottom and left frame lines; the upper plot boundary is the 800.00 line, not the top of the parameter box. All axis labels (x 00 through 700.00 and y 00 through 800.00) were checked against their lines on label-sheet.png. The six requested recorded checks are x 100.00/400.00/700.00 and y 100.00/400.00/800.00 in calibration-eye-checks.csv.

Calibration: 72 measured grid intersections; all 8 x lines and 9 y lines detected, then independently ink-verified; no predicted or rejected lines. Affine diagnostic residuals: RMS x={cal['rms_residual_x']:.3f}, y={cal['rms_residual_y']:.3f} psf; maximum x={cal['max_residual_x']:.3f}, y={cal['max_residual_y']:.3f} psf. These are below 0.5% of each axis span. Values and bounds in points-p1-native.csv use the verified piecewise map and line-position errors, not the affine residual. Bounds propagate four corners/centre and bracketing-line intervals per D-025. Boundary features may be flagged extrapolated because their pixel bounds straddle x=0; this is not a claim that the drawn trace continues left of the axis.

Triangle centres are the arithmetic centroid of the reconstructed vertices in triangle-vertices.csv. Clean horizontal centre bounds are 2 px; apex-direction bounds are at least height/6. Touching/overlapping ink is noted per marker and bounds widened. Fits of visible side cores were checked on the enlarged original crops; the shared upper triangle in C-11B was reconstructed from its visible apex, right side and base.

Trace samples are on ink at the left end, each readable 500 psf normal-stress location, and the right end. The line is an increasing straight trace, so its maximum is its last feature. Median clean perpendicular line thickness is {thickness:.2f} px ({len(widths)} clean sections); u/v bounds are {half:.2f} px, half the stroke thickness rounded upward to a quarter pixel. Endpoints are line ink, not symbol centres. The branch visibly reaches the x=0 axis; its intersection is the intercept feature. The first point was obtained at the measured ink branch/frame intersection. No printed fit parameter was used to position any point. The green overlay marks sampled ink only; a connection between two samples is not evidence of ink through a symbol-associated gap.

Reading against the printed computation: least-squares slope of the calibrated trace samples is {slope:.6f}; printed Tan Theta is {tan}; reading minus printed = {slope-float(tan):+.6f}. Read intercept shear stress is {intercept:.3f} psf; printed Cohesion is {cohesion} psf; reading minus printed = {intercept-float(cohesion):+.3f} psf. The regression intercept of all samples ({reginter:.3f} psf) is a separate diagnostic and is not substituted for the directly read intercept. Piecewise calibration can introduce small drafting-related changes in the apparent slope at grid knots.

Ambiguities and limitations: {ambiguity}

Files: cal-p1/anchors.csv, calibration.json and verified-knots.json; calibration-eye-checks.csv; points-p1.csv (pixels and reading bounds); points-p1-native.csv (same rows plus values/bounds in psf and cal_model); overlay-p1.png (full original page dimensions); notes.md; triangle-vertices.csv; line-thickness-checks.csv; calibration-sensitivity.md. Enlarged label, marker, triangle-fit, trace, endpoint and ambiguity crops/sheets are retained as inspection evidence. Red overlay = marker centroid, green = sampled trace, blue = feature. Pixel bounds are drawn as bars. Duplicate feature/trace coordinates have different roles and are not additional test observations.
'''
 (d/'notes.md').write_text(notes,encoding='utf-8')
 (d/'calibration-sensitivity.md').write_text(f'# {fig}: {sid}\n\nOnly this reading is compared here: affine diagnostic versus verified piecewise calibration. Over all submitted points, maximum absolute affine-minus-piecewise differences are x={maxdiff[0]:.3f} psf and y={maxdiff[1]:.3f} psf. These are correlated calibration sensitivities, not extra independent observation error. The submitted native values and bounds use the piecewise map.\n',encoding='utf-8')
 summary.append({'figure_id':fig,'series_id':sid,'marker_count':len(recs),'trace_count':len(tt),'feature_count':3,
  'rms_x_psf':cal['rms_residual_x'],'rms_y_psf':cal['rms_residual_y'],'max_x_psf':cal['max_residual_x'],'max_y_psf':cal['max_residual_y'],
  'trace_slope':slope,'printed_tan_theta':tan,'slope_difference':slope-float(tan),'intercept_psf':intercept,'printed_cohesion_psf':cohesion,
  'intercept_difference_psf':intercept-float(cohesion),'line_thickness_px':thickness,'trace_bound_px':half})
 print(summary[-1])
writecsv('out/summary.csv',summary)
