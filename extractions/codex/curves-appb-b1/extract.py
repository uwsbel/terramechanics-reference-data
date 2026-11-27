import json,csv,sys,math
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from readings import DATA
for key,uv in json.loads(Path('out/center-refinements.json').read_text()).items():
 j,sid,k=key.split('/');m=DATA[int(j)][sid]['markers'][int(k)];DATA[int(j)][sid]['markers'][int(k)]=tuple(uv)+m[2:]
DATA[7]['dr104']['markers'][3]=(809.5,2136)
DATA[7]['dr104']['markers'][6]=(1187,2169)
DATA[7]['dr104']['markers'][8]=(2101.5,1646)
DATA[7]['dr77']['markers'][6]=(1170.5,2318.5)
from tick_maps import load_maps,verify
sys.path.insert(0,'tools');import calibrate_axes as ca
COLS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note','trace_segment']
def writecsv(p,rows,cols=None):
 with Path(p).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols or list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def near_marker(p,markers,r=22):return any(np.linalg.norm(np.array(p)-np.array(m[:2]))<r for m in markers)
def read_normal(g,p,n,window=8):
 ds=np.arange(-window,window+.01,.25);uu=p[0]+n[0]*ds;vv=p[1]+n[1]*ds
 a=g[np.round(vv).astype(int),np.round(uu).astype(int)];ink=a<150
 if not ink.any():return None
 runs=np.split(np.where(ink)[0],np.where(np.diff(np.where(ink)[0])>1)[0]+1)
 r=min(runs,key=lambda z:abs(ds[z].mean()));w=255-a[r];offset=np.average(ds[r],weights=w);return p+n*offset,(ds[r[-1]]-ds[r[0]]+1)/2,float(a[r].min())
def fit_segment(g,a,b,markers):
 a=np.array(a,float);b=np.array(b,float);t=(b-a)/np.linalg.norm(b-a);n=np.array([-t[1],t[0]]);P=[]
 for f in np.linspace(.025,.975,180):
  p=a+f*(b-a)
  if near_marker(p,markers,27):continue
  z=read_normal(g,p,n,10)
  if z is not None:P.append(z[0])
 P=np.array(P);center=P.mean(axis=0)
 for _ in range(3):
  _,_,V=np.linalg.svd(P-center);tn=V[0];nn=np.array([-tn[1],tn[0]]);err=(P-center)@nn;keep=abs(err-np.median(err))<max(2.5,3*np.median(abs(err-np.median(err))));P=P[keep];center=P.mean(axis=0)
 if tn@t<0:tn=-tn
 return center,tn,float(np.sqrt(np.mean(((P-center)@nn)**2))),len(P)
def project(p,L):c,t,*_=L;return c+np.dot(np.array(p)-c,t)*t
def cross(L,M):
 c,t,*_=L;d,s,*_=M;z=np.linalg.solve(np.column_stack([t,-s]),d-c);return c+z[0]*t
summ=[]
for j,series in DATA.items():
 d=Path(f'out/FB-{j}');cal,x,y=load_maps(d/'cal-p1');g=np.array(Image.open(cal['image']).convert('L'),dtype=float);verify(x,g);verify(y,g)
 rows=[];omits=[];fits=[];allmarkers=[m for S in series.values() for m in S['markers']]
 def add(sid,kind,p,b,symbol='',note='',seg=''):
  seq=1+sum(r['series_id']==sid and r['point_kind']==kind for r in rows);rows.append(dict(zip(COLS,[f'FB-{j}',1,sid,kind,seq,round(float(p[0]),3),round(float(p[1]),3),round(float(b),2),round(float(b),2),symbol,note,seg])))
 # markers all read before any traces
 for sid,S in series.items():
  for m in S['markers']:add(sid,'marker',m[:2],m[2] if len(m)>2 else 2,S.get('symbol','circle'),m[3] if len(m)>3 else '')
 for sid,S in series.items():
  vertices=S['vertices'];label=S['label'];fnotes=[]
  if not vertices:add(sid,'feature',label[:2],2,'',f'label: {label[2]}; printed legend symbol is a square with x');continue
  L=[fit_segment(g,a,b,allmarkers) for a,b in zip(vertices,vertices[1:])]
  V=[project(vertices[0],L[0])]+[cross(a,b) for a,b in zip(L,L[1:])]+[project(vertices[-1],L[-1])]
  V_est=[p.copy() for p in V]
  # At an overprinted endpoint keep the first/last unambiguous separate line stroke.
  for ind,direction,line in [(0,1,L[0]),(-1,-1,L[-1])]:
   p=V[ind].copy();t=line[1]*direction;steps=0
   while near_marker(p,allmarkers,22) and steps<150:p=p+t*.5;steps+=1
   if steps:fnotes.append(f'{"left" if ind==0 else "right"} trace end: first separable stroke is {steps*.5:.1f} px inward of estimated symbol junction; hidden endpoint not guessed')
   V[ind]=p
  # move free endpoints to actual terminal core within a short search when terminal not symbol-obscured
  for ind,sgn,line in [(0,-1,L[0]),(-1,1,L[-1])]:
   p=V[ind];t=line[1]*sgn;n=np.array([-t[1],t[0]])
   # only extend if no nearby marker. Black symbol outline is never an endpoint target.
   if not (j==7 and ind==0) and not near_marker(p,allmarkers,42):
    ps=[]
    for z in np.arange(-8,13,.5):
     q=p+z*t
     if near_marker(q,allmarkers,22):continue
     r=read_normal(g,q,n,5)
     if r is not None:ps.append((z,r[0]))
    if ps:
     # terminal stroke at maximum outward continuous position; cap at observed terminal
     z,q=max(ps,key=lambda z:z[0]);V[ind]=q
  for k,(ln,a,b) in enumerate(zip(L,V,V[1:])):
   fits.append({'series_id':sid,'segment':k+1,'start_u':float(a[0]),'start_v':float(a[1]),'end_u':float(b[0]),'end_v':float(b[1]),'orthogonal_rms_px':ln[2],'ink_samples':ln[3]})
  # feature first / vertices / last, all with label independently
  for k,p in enumerate(V):
   role='first point' if k==0 else ('last point; peak' if k==len(V)-1 else 'vertex')
   if j==7 and k==0:role+='; first separable diagonal ink; continuation to axis is obscured and omitted'
   hidden=near_marker(p,allmarkers,22);note=role+('; intersection obscured by symbol; reconstructed from adjacent straight ink' if hidden else '')
   if k==0 or k==len(V)-1:note+='; '+('; '.join(fnotes) if fnotes else 'visible line end')
   fb=22 if hidden else 4
   if k==0 and any(n.startswith('left trace end') for n in fnotes):p=V_est[0];fb=22;note+='; hidden endpoint extent, distinct trace starts farther along visible ink'
   if k==len(V)-1 and any(n.startswith('right trace end') for n in fnotes):p=V_est[-1];fb=22;note+='; hidden endpoint extent, distinct trace ends before symbol'
   if j==7 and k==0:
    p=np.array([504.,3080.]) if sid=='dr99p5' else np.array([506.,3690.]);fb=70;note='first point; origin obscured by left frame/symbol ink; wide extent only; trace starts on first separable diagonal stroke'
   add(sid,'feature',p,fb,'',note)
  add(sid,'feature',label[:2],2,'',f'label: {label[2]}')
  # full drawing-order candidates, then actual ink at each required integer x
  candidates=[]
  for k,(a,b) in enumerate(zip(V,V[1:])):
   xa=x.value(*a)[0];xb=x.value(*b)[0];ts=[(0,'first point' if k==0 else 'vertex')]
   for val in range(math.ceil(min(xa,xb)),math.floor(max(xa,xb))+1):
    if abs(val-xa)<.00001 or abs(val-xb)<.00001:continue
    lo,hi=0.,1.
    for _ in range(40):
     mid=(lo+hi)/2;xx=x.value(*(a+mid*(b-a)))[0]
     if (xx<val)==(xa<xb):lo=mid
     else:hi=mid
    ts.append(((lo+hi)/2,f'x={val} psi'))
   ts.append((1,'last point' if k==len(V)-2 else 'vertex'))
   for t,role in sorted(ts):
    if k>0 and t==0:continue
    candidates.append((a+t*(b-a),role,k))
  segment=1;prev=None
  for p,role,k in candidates:
   if near_marker(p,allmarkers,22) or (j==7 and near_marker(p,series['dr104']['markers'],29)):
    omits.append({'series_id':sid,'requested':role,'pixel_u':round(float(p[0]),3),'pixel_v':round(float(p[1]),3),'reason':'symbol overlap/white interior; no trace sample placed on circle/square outline'});segment+=1;prev=None;continue
   t=L[k][1];n=np.array([-t[1],t[0]]);r=read_normal(g,p,n,5)
   if r is None:
    omits.append({'series_id':sid,'requested':role,'pixel_u':float(p[0]),'pixel_v':float(p[1]),'reason':'no separate line ink'});segment+=1;prev=None;continue
   pp,half,_=r
   if prev is not None:
    # a pair of stored samples may not support interpolation across a symbol interruption
    for f in np.linspace(.05,.95,50):
     if near_marker(prev+f*(pp-prev),allmarkers,22):segment+=1;break
   # use half measured normal stroke thickness; square pixel bounds enclose this disk
   bound=max(3.5,round(half*2)/2)
   add(sid,'trace',pp,bound,'',role,segment);prev=pp
  S['fit_notes']=fnotes
 writecsv(d/'points-p1.csv',rows,COLS)
 # Native piecewise values and worst-corner intervals; no affine residual added.
 native=[];sens=[]
 for r in rows:
  u,v,bu,bv=[float(r[k]) for k in ['pixel_u','pixel_v','u_bound_px','v_bound_px']];xx,bx,ex=x.interval(u,v,bu,bv);yy,by,ey=y.interval(u,v,bu,bv)
  affine_x=np.dot(cal['ax'],[u,v,1]);affine_y=np.dot(cal['ay'],[u,v,1]);native.append({**r,'x_native':f'{xx:.8f}','y_native':f'{yy:.8f}','x_read_bound':f'{bx:.8f}','y_read_bound':f'{by:.8f}','cal_model':'piecewise'+('; extrapolated x' if ex else '')+('; extrapolated y' if ey else ''),'x_unit':'psi','y_unit':'kips/in.^2'})
  sens.append({'series_id':r['series_id'],'point_kind':r['point_kind'],'sequence':r['sequence'],'affine_minus_piecewise_x':float(affine_x-xx),'affine_minus_piecewise_y':float(affine_y-yy)})
 writecsv(d/'points-p1-native.csv',native);writecsv(d/'cal-p1'/'line-fits.csv',fits);writecsv(d/'trace-omissions.csv',omits,['series_id','requested','pixel_u','pixel_v','reason']);writecsv(d/'cal-p1'/'calibration-sensitivity.csv',sens)
 checks=[]
 chx=[0,6,14] if j in [3,4,6] else ([0,6,12] if j==5 else [0,8,16]);chy={3:[7,13,18],4:[0,5,10],5:[5,20,40],6:[5,17,29],7:[0,6,11]}[j]
 for axis,vals,key in [('x',chx,'vertical_lines'),('y',chy,'horizontal_lines')]:
  for val in vals:
   l=next(l for l in cal[key] if l[axis+'_value']==val);P=np.array(l['samples']);t=float(np.median(P[:,0]));p=float(np.median(P[:,1]));u,v=(p,t) if axis=='x' else (t,p)
   if 'frame' in l['source']:
    # check at labelled corner on that frame rather than its middle
    if axis=='x':
     h=cal['horizontal_lines'][0];u=(l['u_at_v0']+l['slope_du_dv']*h['v_at_u0'])/(1-l['slope_du_dv']*h['slope_dv_du']);v=h['v_at_u0']+h['slope_dv_du']*u
    else:
     vl=cal['vertical_lines'][0];u=(vl['u_at_v0']+vl['slope_du_dv']*l['v_at_u0'])/(1-vl['slope_du_dv']*l['slope_dv_du']);v=l['v_at_u0']+l['slope_dv_du']*u
   checks.append({'figure_id':f'FB-{j}','panel':1,'axis':axis,'printed_label':str(val),'value_used':val,'pixel_u':round(u,2),'pixel_v':round(v,2),'checked_by_eye':'yes','result':'label visibly aligned to this tick/frame; direction and sequence confirmed','evidence':'cal-p1/labels-all.png'})
 writecsv(d/'calibration-eye-checks.csv',checks)
 # full-resolution overlay, all symbol centers numbered by kind sequence
 im=Image.open(cal['image']).convert('RGB');draw=ImageDraw.Draw(im);colors=['#df153c','#165fdb','#009650']
 try:font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
 except:font=None
 for i,(sid,S) in enumerate(series.items()):
  col=colors[i]
  for r in rows:
   if r['series_id']!=sid:continue
   u,v=float(r['pixel_u']),float(r['pixel_v']);kind=r['point_kind'];seq=r['sequence']
   if kind=='marker':draw.ellipse((u-24,v-24,u+24,v+24),outline=col,width=3);draw.line((u-5,v,u+5,v),fill=col,width=2);draw.line((u,v-5,u,v+5),fill=col,width=2);draw.text((u+27,v-13),f'M{seq}',fill=col,font=font)
   elif kind=='trace':draw.line((u-8,v,u+8,v),fill=col,width=3);draw.line((u,v-8,u,v+8),fill=col,width=3)
   else:draw.polygon([(u,v-13),(u+13,v),(u,v+13),(u-13,v)],outline='#e07900',width=3)
 draw.rectangle((700,100,2900,270),fill='white',outline='gray',width=2)
 draw.text((720,110),f'FB-{j}: independent reading | M = marker; cross = trace; orange diamond = feature',fill='black',font=font)
 for i,sid in enumerate(series):draw.text((730,150+35*i),sid,fill=colors[i],font=font)
 im.save(d/'overlay-p1.png')
 counts={sid:dict(Counter(r['point_kind'] for r in rows if r['series_id']==sid)) for sid in series};summ.append({'figure_id':f'FB-{j}','counts':counts,'rms_x':cal['rms_residual_x'],'rms_y':cal['rms_residual_y'],'max_x':cal['max_residual_x'],'max_y':cal['max_residual_y'],'omitted_trace_samples':len(omits)})
 # write notes
 notes=[f'# FB-{j}: independent blind reading','',f'Only packet/p{j+106:04}.png, packet tables, and packet/CURVE-READING.md were used. Coordinates refer to the original unrotated 300 dpi image. No other reading was consulted.','', '## Calibration','',f'All {len(x.knots)} x and {len(y.knots)} y knots are measured printed ticks or labelled frame lines. Tick stubs were sampled at 1 px intervals, each fitted independently with its own tilt. Opposite frame lines were also fitted independently. No interior knot was predicted from frame spacing. The native conversion is piecewise between these independently tilted lines; the affine map is diagnostic only.',f'Affine residual RMS: x={cal["rms_residual_x"]:.6f} psi, y={cal["rms_residual_y"]:.6f} kips/in.^2; maxima x={cal["max_residual_x"]:.6f}, y={cal["max_residual_y"]:.6f}. Every short tick is ink-checked at five positions along its actual stub; full frame lines use the protocol ink check. verified-knots.json records these checks and position errors. Bounds propagate the pixel rectangle and the bracketing line position intervals; global affine residual is not added.','Short tick strokes give limited leverage on their extended direction. Their independently fitted slopes are retained literally, rather than forcing parallel lines. calibration-sensitivity.csv reports affine minus piecewise values so the effect is visible. No inferred interior grid is treated as printed ink.',f'By-eye checks: x labels {chx}; y labels {chy}. All printed tick labels were also inspected in labels-all.png. See calibration-eye-checks.csv for the six requested checks.','', '## Series, symbols, and drawn lines','']
 for sid,S in series.items():
  notes += [f'- {sid}: printed "{S["label"][2]}"; {S.get("symbol","circle")}; '+('polyline through '+str(len(S['vertices'])-2)+' internal vertices.' if S['vertices'] else 'symbols only; no polyline was drawn for this group.')]
  for n in S.get('fit_notes',[]):notes.append('  - '+n)
 notes+=['','Markers were recorded before trace extraction. Clean marker centers have 2 px bounds; overlaps, missing arcs, or axis crossings have wider bounds stated per row. Legend symbols are not counted as measurement markers. Trace bounds are half the measured ink thickness (at least 3.5 px for the rasterized line core), without using symbol rims to extend a stroke. Features locate each first/last point, every bend, and the printed group label center. Hidden bends are features with wider bounds, not trace samples in white symbol interiors.','',f'Requested samples blocked by symbols or missing line ink are listed in trace-omissions.csv ({len(omits)} omissions). Rule 7 takes precedence over placing a trace sample on a symbol or in a white gap. trace_segment changes across a symbol obstruction; interpolation must not cross that break.','', '## Ambiguities','']
 if j==3:notes+=['The y tick between 7 and 9 prints as "3" (not 8). Its measured spacing is approximately one unit from both neighbours, confirming 8; it is used as 8, never as 3.','Dense knee around (1237,1988) is a thick, unresolved circle cluster. One marker is retained with a 20 px bound; additional coincident circles cannot be counted reliably. The two top circles and the two overlapping loose circles near (1090,3775) are distinguishable.']
 if j==4:notes+=['The low dense triplet and loose bend triplet have merged rims; individual residual arcs support the separate markers. The dense rightmost cluster has one main hole and tiny upper/lower crescents: two overlapping circles are recorded with 12 px bounds. The two widely scattered loose observations near each of x˜5 and x˜10 are assigned to the loose line, which passes between each pair; neither pair lies on the dense line.']
 if j==5:notes+=['At the dense left end two side-by-side circles share ink at (1026,2951) and (1040,2951). The loose rightmost lower circle has only a left/lower arc; its center is reconstructed with an 11 px bound. The loose density label is damaged near its leading zero: the readable text and printed index give Dr = 0.26; ID dr26 is retained.']
 if j==6:notes+=['The frame is visibly skewed. Each tick stroke and each of the four frame sides has its own fitted tilt; no single page rotation or rectangular-frame assumption is imposed. The broken dense left circle and the loose circle overlapping the bottom frame have widened bounds. The overlapping loose circles at the right end are distinguishable from the two white interior lobes.']
 if j==7:notes+=['The isolated square-with-x immediately before "Dr = 1.04" at approximately (1805,1315) is the printed legend symbol, not a measurement. All other square-with-x marks, including ones touching the upper and lower polylines, belong to dr104 by the printed legend identity. The upper line carries Dr = 0.995 and open circles; the lower line carries Dr = 0.77 and filled circles.','At the left frame there are two open circles near v=3019 and 3067, a square near v=3091, a square near v=3364, two overlapping filled circles near v=3474 and 3495, and one filled circle near v=3848. The two filled lobes are separately identifiable but their centers have 10 px bounds. The line origins merge with the axis/symbol ink and their hidden continuation cannot be separated; the trace starts at the first identifiable diagonal stroke.','The printed 7 on the y axis is thin/broken but the 6–8 spacing confirms it. The ticks at y=1, 2 and 3 were measured on their clear right tips beyond the overlapping oblique line/square symbols.']
 notes+=['','## Files','', 'points-p1.csv; points-p1-native.csv; overlay-p1.png; calibration-eye-checks.csv; trace-omissions.csv; cal-p1/calibration.json; cal-p1/anchors.csv; cal-p1/tick-fits.csv; cal-p1/verified-knots.json; cal-p1/line-fits.csv; cal-p1/labels-all.png; cal-p1/calibration-sensitivity.csv. Helpers and enlarged coordinate crops are retained under out/.','', 'Counts: '+json.dumps(counts)]
 (d/'notes.md').write_text('\n'.join(notes)+'\n',encoding='utf-8')
Path('out/summary.json').write_text(json.dumps(summ,indent=2));print(json.dumps(summ,indent=2))




