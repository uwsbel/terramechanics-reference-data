from trace_read import *
from collections import Counter
COLS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
# Symbol decisions made from the page crops; unresolved stacks are omitted explicitly.
ACCEPT={
 'FA-2':{'average':['4','6','8','10','12','16','20','30','40','50','60','70','80','100','120'],'upper':['6','8','10','20'],'lower':['8','10','12','16','20','30']},
 'FA-6':{'average':['6','8','10','12','16','20','30','40','50','60','70','80','100','120'],'upper':['8','10','12','16','20','30','40','80','100'],'lower':['8','10','12','16','20','30','40']},
 'FA-18':{'average':['4','6','8','10','12','16','20','30','40','50','60','70','80','100','120'],'upper':['8','10','12','16','20','30'],'lower':['8','10','12','16','20','30']},
 'FA-22':{'average':['3/8','3','4','6','8','12','20','30','40','50','60','80','100','200'],'upper':['3','4','6','8','12','20','40','50','60','100','200'],'lower':['4','6','8','12','20','30','40','50','60','70','100','120','200']},
 'FA-26':{'average':['30','40','50','60','70','80','100'],'upper':['30','40','50','60','80'],'lower':['30','40','50','80']},
 'FA-38':{'average':['3','4','6','8','10','12','16','20','30','40','50','60','70','80','100','120','200'],'upper':['8','12','20','30','50','60','70','100','120','200'],'lower':['8','10','12','20','30','40','50','60','70','100','120','200']},
 'FA-46':{'average':['6','8','10','12','16','20','30','40','50','60','70','80','100','120','200'],'upper':['8','12','16','20'],'lower':['8','10','12','16','20','30']}
}
OVERRIDE={('FA-2','average','6'):(740,1573),('FA-2','upper','8'):(1005,1719),('FA-18','average','4'):(591,1443),('FA-22','average','3/8'):(755,1177),('FA-22','upper','3'):(771,1337),('FA-22','upper','6'):(909,1606),('FA-22','average','200'):(2080,3221),('FA-22','upper','200'):(2014,3221),('FA-22','lower','200'):(2134,3221)}
KNEES={'FA-2':[1668,2110],'FA-6':[1740,2150],'FA-18':[1710,2110],'FA-22':[1470,1730],'FA-26':[2410,2780],'FA-38':[1940],'FA-46':[1710,2150]}
TITLE={'FA-2':'Average and Range of Three Samples of Unused RS Soil','FA-6':'Average and Range for Three Samples of Unused PS Soil','FA-18':'Average and Range of Three Samples of Unused RSM Soil','FA-22':'Average and Range of Six Samples of RC2 Soil','FA-26':'Average and Range of Five Samples of SS Soil','FA-38':'Average and Range of Seven Samples of LSM','FA-46':'Average and Range of Sample of Unused RSM-b Soil'}
def merged(fid,v):
 tail={'FA-2':2350,'FA-6':2500,'FA-18':2360,'FA-26':2860,'FA-46':2250}
 if fid in tail and v>tail[fid]:return True
 guides=GUIDES[fid];us=[guide_at(gg,v) for gg in guides.values()];gg=guides['average'];du=(guide_at(gg,v+8)-guide_at(gg,v-8))/16
 return (max(us)-min(us))/np.hypot(du,1)<17
def read_ink(fid,sid,targetv,g,clean,exclude,endpoint=False,targetx=None):
 guide=GUIDES[fid][sid];ismerge=merged(fid,targetv)
 if ismerge:guide=GUIDES[fid]['average']
 v=targetv
 # Correct a locator's normal displacement to the intended grain-size ruling.
 for _ in range(5):
  q=sample(g,guide,v)
  if q is None:break
  p,w,tan=q
  if targetx is None:break
  x=X_GLOBAL.value(*p)[0];err=np.log10(x/targetx)
  if abs(err)<.0004:break
  v+=err/abs(X_GLOBAL.value_q(*p)[1])
  v=np.clip(v,guide[0][1],guide[-1][1])
 basev=v;best=None
 for delta in [0]+[j*k for j in np.arange(.5,55.1,.5) for k in [-1,1]]:
  vv=basev+delta
  if not guide[0][1]<=vv<=guide[-1][1]:continue
  q=sample(g,guide,vv)
  if q is None:continue
  p,w,tan=q;u,pv=p
  if not endpoint and any((u-mu)**2+(pv-mv)**2<rr**2 for mu,mv,rr in exclude):continue
  # Source ink is mandatory; the grid-suppressed image is just a locator aid.
  if not ismerge and np.mean(clean[round(pv)-2:round(pv)+3,round(u)-2:round(u)+3]<150)<.12:continue
  best=(p,w,delta,ismerge);break
 if best is None:
  # At an unresolved merge the actual average ink is the only readable shared ink.
  for delta in range(0,35):
   for dv in (delta,-delta):
    vv=np.clip(targetv+dv,guide[0][1],guide[-1][1]);q=sample(g,guide,vv)
    if q is not None:
     p,w,tan=q;best=(p,max(w,12),dv,True);break
   if best is not None:break
  if best is None:raise RuntimeError((fid,sid,targetv,'no readable ink'))
 p,w,delta,ismerge=best
 note=[]
 if ismerge:
  w=max(w,14);note.append('Curves overlap or merge with percent frame; shared ink, individual position unresolved; widened bound')
 if abs(delta)>.1:note.append(f'Sample moved {delta:+.1f} px along grain direction to nearest readable line ink / dash end, avoiding marker and grid')
 if targetx is not None:note.append(f'Nominal grain-size sample {targetx:.8g} mm')
 return p,max(3,w),'; '.join(note)
def bounds_for(fid,p,w,note):
 bu,bv=w,w
 if 'shared ink' in note:
  bu=max(bu,max(abs(guide_at(gg,p[1])-p[0]) for gg in GUIDES[fid].values())+5)
 return round(float(bu),2),round(float(bv),2)
def read_y(fid,sid,yy,targetv,g,clean,exclude,Y):
 # A five-percent ruling is read by its actual tilted constant-value line, rather than
 # ordering points by page v (a nearly flat sideways trace can double back in v).
 guide=GUIDES[fid][sid];vguess=targetv
 def at_u(v):
  lo,hi=CONFIG[fid][1][0]-60,CONFIG[fid][1][2]+60
  for _ in range(35):
   u=(lo+hi)/2
   if Y.value(u,v)[0]>yy:lo=u
   else:hi=u
  return (lo+hi)/2
 u=at_u(vguess);v0=round(vguess)-55;v1=round(vguess)+56;choices=[]
 # At a percent grid line itself the grid can hide the trace. Read just beside it,
 # preserving the actual pixel position and a bound that covers the requested ruling.
 for du in [0,-6,6,-10,10]:
  uc=u+du;ix=np.where(g[v0:v1,round(uc)]<150)[0]+v0
  for group in np.split(ix,np.where(np.diff(ix)>1)[0]+1):
   if not 5<=len(group)<=45:continue
   v=float(np.mean(group));uu=uc
   if not (guide[0][1]<=v<=guide[-1][1]):continue
   if any((uu-mu)**2+(v-mv)**2<rr**2 for mu,mv,rr in exclude):continue
   if np.mean(clean[round(v)-2:round(v)+3,round(uu)-2:round(uu)+3]<150)<.12:continue
   if g[round(v),round(uu)]>150:continue
   # The guide supplies drawing identity; a crossing grid far from that path is rejected.
   if abs(uu-guide_at(guide,v))>130:continue
   choices.append((abs(v-vguess)+abs(du)*.3,uu,v,max(len(group)/2,abs(du)+1)))
 if choices:
  _,u,v,w=min(choices);p=np.array([u,v]);note='Extra sample on the labelled percent ruling at its curve ink crossing'
  if merged(fid,v):note+='; Curves overlap; shared ink with widened bound'
  return p,max(4,min(w,14)),note+'; ruling obscured by grid: adjacent source ink where necessary'
 return read_ink(fid,sid,targetv,g,clean,exclude)
summary=[]
for fid,(page,box) in CONFIG.items():
 d=ROOT/'out'/fid;source=ROOT/'packet'/f'{page}.png';g=np.array(Image.open(source).convert('L'));clean=np.array(Image.open(d/'grid-suppressed.png'))
 cal,X,Y=ca.piecewise_maps(d/'cal-p1',source);X_GLOBAL=X;rows=[];omitted=[]
 candidates=json.loads((d/'marker-candidates.json').read_text());exclude=[]
 for c in candidates:
  sid,label=c['series_id'],c['label'];u,v=OVERRIDE.get((fid,sid,label),(c['pixel_u'],c['pixel_v']));exclude.append((u,v,17))
  if label not in ACCEPT[fid][sid]:
   omitted.append(dict(series_id=sid,near_sieve_label=label,pixel_u=u,pixel_v=v,reason='No separately identifiable circular symbol center: curve/dash/grid overlap or shared marker stack. Omitted under rule 6.'))
   continue
  note='Circular symbol; curve and/or grid crosses the symbol; bound covers its visible extent'
  if merged(fid,v):note+='; merged range symbols cannot be counted separately; only visible average/shared symbol retained'
  rows.append(dict(figure_id=fid,panel=1,series_id=sid,point_kind='marker',sequence=0,pixel_u=u,pixel_v=v,u_bound_px=14,v_bound_px=14,symbol='circle',note=note+f'; near printed sieve label {label}, read from symbol ink (sieve scale not calibrated)'))
 for sid,guide in GUIDES[fid].items():
  lo=X.value(*guide[-1])[0];hi=X.value(*guide[0])[0]
  samples=[(None,guide[-1][1],'first point')]
  for n in range(100):
   xx=.02*10**(.05*n)
   if lo<xx<hi:samples.append((xx,uv_at_x(guide,X,xx)[1],''))
  samples.append((None,guide[0][1],'last point; maximum percent finer (peak at coarse end)'))
  tr=[]
  for order,(xx,vv,role) in enumerate(samples):
   p,w,note=read_ink(fid,sid,vv,g,clean,exclude,bool(role),xx)
   bu,bv=bounds_for(fid,p,w,note)
   if role: bv=max(bv,20);note+='; endpoint line extent overlaps marker/frame ink; widened extent bound'
   tr.append(dict(figure_id=fid,panel=1,series_id=sid,point_kind='trace',sequence=0,pixel_u=round(float(p[0]),3),pixel_v=round(float(p[1]),3),u_bound_px=bu,v_bound_px=bv,symbol='',note='; '.join(z for z in [role,note] if z),_order=order))
  # Additional 5-percent rulings only in nominal 0.05-decade intervals rising by >10 percent.
  extra=[]
  for index,(a,b) in enumerate(zip(tr,tr[1:])):
   ya=Y.value(a['pixel_u'],a['pixel_v'])[0];yb=Y.value(b['pixel_u'],b['pixel_v'])[0]
   if yb-ya<=10:continue
   for yy in np.arange(np.floor(ya/5)*5+5,yb,5):
    low,high=b['pixel_v'],a['pixel_v']
    for _ in range(30):
     mid=(low+high)/2;u=guide_at(guide,mid)
     if Y.value(u,mid)[0]>yy:low=mid
     else:high=mid
    p,w,note=read_y(fid,sid,yy,(low+high)/2,g,clean,exclude,Y);bu,bv=bounds_for(fid,p,w,note)
    extra.append(dict(figure_id=fid,panel=1,series_id=sid,point_kind='trace',sequence=0,pixel_u=round(float(p[0]),3),pixel_v=round(float(p[1]),3),u_bound_px=bu,v_bound_px=bv,symbol='',note=f'Extra sample at nominal {yy:g} percent finer in interval rising >10 percent; '+note,_order=index+(yy-ya)/(yb-ya)))
  tr=sorted(tr+extra,key=lambda r:r['_order'])
  for r in tr:r.pop('_order')
  rows.extend(tr)
  for r,role in [(tr[0],'first point'),(tr[-1],'last point; maximum percent finer (peak at coarse end)')]:
   z=r.copy();z.update(point_kind='feature',note=role+'; '+r['note']);rows.append(z)
  for vv in KNEES[fid]:
   p,w,note=read_ink(fid,sid,vv,g,clean,exclude)
   bu,bv=bounds_for(fid,p,max(w,12),note)
   rows.append(dict(figure_id=fid,panel=1,series_id=sid,point_kind='feature',sequence=0,pixel_u=round(float(p[0]),3),pixel_v=round(float(p[1]),3),u_bound_px=bu,v_bound_px=bv,symbol='',note='Broad knee / change of curvature, not a sharp kink; location spans transition; '+note))
 # Fix a stable series color order in the overlay.
 rows=sorted(rows,key=lambda r:['average','upper','lower'].index(r['series_id']))
 counts=Counter()
 for r in rows:
  key=(r['series_id'],r['point_kind']);counts[key]+=1;r['sequence']=counts[key]
 with (d/'points-p1.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=COLS);w.writeheader();w.writerows(rows)
 with (d/'marker-omissions.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(omitted[0]));w.writeheader();w.writerows(omitted)
 # Use the protocol's piecewise interpolation and exact bound propagation.
 run(ROOT/'tools/calibrate_axes.py','apply',d/'cal-p1/calibration.json',d/'points-p1.csv',d/'points-p1-affine-diagnostic.csv')
 run(ROOT/'tools/calibrate_axes.py','piecewise',d/'cal-p1',d/'points-p1.csv',d/'points-p1-native.csv','--image',source)
 run(ROOT/'tools/plot_grid.py','overlay',source,'--points',d/'points-p1.csv','--out',d/'overlay-p1.png')
 eye=[]
 for axis,K,values in [('x',X,[.02,.05,.1,.2,.5,1,1.5,2,3,4,5,9]),('y',Y,list(range(0,101,10)))]:
  for val in values:
   kn=next(k for k in K.knots if k['value']==val)
   # Check the grain label at the right-hand labelled edge and percent labels at the coarse end.
   t=float(np.array([box[2] if axis=='x' else box[0],box[1]])@K.e_t)
   p=K.line_s(kn,t)*K.e_s+t*K.e_t
   label=(f'{val:.2f}' if val in [.02,.05] else f'{val:.1f}') if axis=='x' else str(val)
   eye.append(dict(axis=axis,printed_label=label,value=val,pixel_u=round(float(p[0]),2),pixel_v=round(float(p[1]),2),confirmed='yes',frame_status=('labelled fine-end frame' if val==.02 else '9.0 interior line; coarse frame beyond it is unlabelled' if val==9 else 'interior labelled grain ruling') if axis=='x' else 'labelled percent frame' if val in [0,100] else 'interior labelled percent ruling',note='By-eye association of printed label to ruling; detected/refitted line checked against page ink'))
 with (d/'calibration-eye-checks.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(eye[0]));w.writeheader();w.writerows(eye)
 with (d/'points-p1-native.csv').open() as f:native=list(csv.DictReader(f))
 with (d/'points-p1-affine-diagnostic.csv').open() as f:affine=list(csv.DictReader(f))
 sens=[]
 for sid in ['average','upper','lower']:
  rr=[(a,b) for a,b in zip(native,affine) if a['series_id']==sid]
  sens.append(f"- {sid}: largest affine versus piecewise grain difference {max(abs(float(a['x_native'])-float(b['x_native'])) for a,b in rr):.6g} mm; percent difference {max(abs(float(a['y_native'])-float(b['y_native'])) for a,b in rr):.4g} percentage points.")
 note=f"""# {fid}, panel 1

Blind reading from packet/{page}.png only; all pixels refer to the original 3213 by 4558 unrotated page. Printed caption: {TITLE[fid]}.

The solid curve is `average`; `upper` is the dashed range with higher percent finer (leftward on the scanned page at fixed grain size), and `lower` the other dashed range. Grain size increases up and percent finer increases left. Native values are mm and percent, with x_transform=log10. FA-18 prints RSM without the index's '-a' suffix; its supplied id and series ids are retained. FA-46's caption uses singular 'Sample', as printed. No table values, classification strip, or sieve scale ticks are observations.

## Calibration and eye checks

All printed grain labels 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0 and 9.0 and all percent labels 0, 10, ..., 100 were associated with their actual rulings by eye. The 0 and 100 percent frames are labelled. The fine-end grain frame is 0.02; the coarse frame extends past the labelled 9.0 line and is not used as a knot. Unlabelled log subdivisions and dashed sieve rulings were excluded from calibration.

The initial detect result is preserved separately. Some detections followed a minor subdivision or table border; the final labelled major rulings were measured on visible ink with the table excluded and robust straight-line fits. All 12 x and 11 y lines pass the protocol ink check. See cal-p1/anchors.csv and piecewise-knots.json. Affine diagnostic RMS: {cal['rms_residual_x']:.7f} decades and {cal['rms_residual_y']:.6f} percentage points; maxima {cal['max_residual_x']:.7f} decades and {cal['max_residual_y']:.6f} percentage points. Native values and bounds use verified piecewise knots, never the global residual.

## Reading and uncertainty

Markers were examined before sampling traces, using source crops and the marker atlas. Circular symbols often overlap curves, dashed sieve lines and each other. The visible centers are recorded with the symbol-extent bound (14 px) because those overlaps prevent a clean 2 px center claim. Separately unidentifiable range symbols are omitted, with their locations individually listed in marker-omissions.csv. A marker candidate was only a crop locator, not automatically an observation. No triangles were identified; rule 8 does not apply. These are distribution curves, not derived peak envelopes; rule 9 does not supply another source of identity.

Each trace is sampled from the fine end in drawing order, at nominal 0.02 times 10^(0.05*n) mm within its visible extent. Intervals rising more than 10 percent have additional nominal 5-percent samples. Nominal values in notes are sampling requests; x_native and y_native always come from actual ink pixels. In a dash gap or beneath a marker a sample was moved to nearby line ink and the displacement noted; none is a white-gap interpolation or a symbol outline. The first/last features duplicate the trace ink endpoints; broad knees have separate features. The last point also identifies the monotone trace's maximum, so a duplicate peak observation is not added.

Through the coarse shoulders and particularly the fine tails, the curves can run together. Overlaps were read as shared visible ink with a widened bound, not three invented centers. In the near-zero tails of FA-2, FA-6, FA-18 and FA-46 the curve additionally merges into the labelled 0-percent frame; the extent and individual branch positions there are uncertain. FA-26 also approaches that frame. FA-38 has close but often distinguishable curves throughout; the coarse symbols stack. FA-22 has the widest readable range, with separated fine-end circles. Endpoint extent cannot be sharper than the visible merge/marker thickness; flagged bounds reflect that limitation. Normal trace bounds are half the measured line core thickness; wider bounds are expressly flagged. Broad knees are not sharp mathematical breakpoints.

## Calibration sensitivity

"""+'\n'.join(sens)+'\n\nCounts (trace / marker / feature):\n'+ '\n'.join(f"- {sid}: {counts[sid,'trace']} / {counts[sid,'marker']} / {counts[sid,'feature']}" for sid in ['average','upper','lower'])+'\n'
 (d/'notes.md').write_text(note,encoding='utf-8')
 summary.append(dict(figure_id=fid,rms_decades=cal['rms_residual_x'],rms_percent=cal['rms_residual_y'],counts={sid:{kind:counts[sid,kind] for kind in ['trace','marker','feature']} for sid in ['average','upper','lower']},omitted_marker_candidates=len(omitted)))
(ROOT/'out/summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
