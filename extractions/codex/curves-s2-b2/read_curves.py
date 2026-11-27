import sys, json, csv, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca

PYTHON=r'<local path>'
FIGS={
 'F2-45':('0106',(365,1410,2310,3660)),
 'F2-46':('0107',(580,1390,2470,3460)),
 'F2-47':('0108',(465,1650,2690,3270)),
 'F2-48':('0109',(400,1030,2300,3780)),
}

def maps(fid):
 page,box=FIGS[fid]; root=Path('out')/fid
 cal,X,Y=ca.piecewise_maps(root/'cal-p1',f'packet/p{page}.png')
 return cal,X,Y

def inv(x,y,cal,X,Y):
 A=np.array([cal['ax'][:2],cal['ay'][:2]])
 p=np.linalg.solve(A,np.array([x-cal['ax'][2],y-cal['ay'][2]]))
 for _ in range(5):
  val=np.array([X.value(*p)[0],Y.value(*p)[0]])
  J=np.column_stack([np.array([X.value(*(p+e))[0],Y.value(*(p+e))[0]])-val for e in (np.array([1.,0.]),np.array([0.,1.]))])
  p+=np.linalg.solve(J,np.array([x,y])-val)
 return p

def writecsv(path,rows):
 with Path(path).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def init():
 for fid,(page,box) in FIGS.items():
  root=Path('out')/fid; cal,X,Y=maps(fid)
  summary=ca.knots_summary(X,Y)
  (root/'cal-p1'/'piecewise-knots.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
  print(fid,'verified',len(X.knots),len(Y.knots),'rejected',[(a['value'],a['reason']) for a in X.rejected+Y.rejected])
  im=Image.open(f'packet/p{page}.png').convert('RGB'); d=ImageDraw.Draw(im)
  for u in range(box[0]//100*100,box[2],100):
   d.line((u,box[1],u,box[3]),fill=(255,170,170));d.text((u+2,box[1]+2),str(u),fill='red')
  for v in range(box[1]//100*100,box[3],100):
   d.line((box[0],v,box[2],v),fill=(170,170,255));d.text((box[0]+2,v+2),str(v),fill='blue')
  im.crop(box).save(root/'reading-grid.png')

def recover47():
 fid='F2-47'; root=Path('out')/fid/'cal-p1'; cal,X,Y=maps(fid)
 if 'recovery_note' in cal:return
 if not (root/'calibration-detected.json').exists():
  (root/'calibration-detected.json').write_text((root/'calibration.json').read_text(),encoding='utf-8')
  (root/'anchors-detected.csv').write_text((root/'anchors.csv').read_text(),encoding='utf-8')
 gray=np.asarray(Image.open('packet/p0108.png').convert('L'),dtype=float)
 ts=[t for k in X.knots for t in k['t']]
 pts,rms=ca.recover_line(gray,X,7,(min(ts),max(ts)))
 vv=np.array([p[1] for p in pts]);uu=np.array([p[0] for p in pts]);m,b=np.polyfit(vv,uu,1)
 line=next(l for l in cal['vertical_lines'] if l['x_value']==7)
 line.update(slope_du_dv=float(m),u_at_v0=float(b),source='recovered from right-frame ink',samples=[[float(v),float(u)] for u,v in pts])
 anchors=ca.load_anchors(root)
 for a in anchors:
  for k in ('x_value','y_value','u','v'):a[k]=float(a[k])
  if float(a['x_value'])!=7:continue
  h=next(l for l in cal['horizontal_lines'] if l['y_value']==float(a['y_value']))
  u=(b+m*h['v_at_u0'])/(1-m*h['slope_dv_du']);v=h['v_at_u0']+h['slope_dv_du']*u
  a.update(u=round(u,2),v=round(v,2),x_source=line['source'])
 writecsv(root/'anchors.csv',anchors)
 vals=ca.fit_affine(anchors)
 for name,val in zip(['ax','ay','rms_residual_x','rms_residual_y','max_residual_x','max_residual_y'],vals):cal[name]=val
 cal['x_per_px']=float(np.linalg.norm(cal['ax'][:2]));cal['y_per_px']=float(np.linalg.norm(cal['ay'][:2]))
 cal['recovery_note']=f'x=7 refitted from {len(pts)} right-frame ink positions; straight-line RMS {rms:.3f} px'
 (root/'calibration.json').write_text(json.dumps(cal,indent=2),encoding='utf-8')
 writecsv(root/'recovered-frame-ink.csv',[dict(pixel_u=round(u,2),pixel_v=round(v,2)) for u,v in pts])
 print(cal['recovery_note'])

# These are visual guides from this packet only, for locating ink, never exported values.
GUIDES={
 'F2-45':{
  'lpt95':[(0,0),(.25,23),(.5,37),(.75,44),(1,51),(1.25,59),(1.5,67),(1.75,74),(2,83),(2.5,100),(3,121),(3.5,142),(4,162),(4.5,182),(5,204),(5.5,224),(6,250),(6.25,259),(6.5,273),(7,300)],
  'lpt79':[(0,0),(.25,7),(.5,19),(1,35),(2,61),(3,88),(4,113),(5,141),(6,171),(6.2,178)],
 },
 'F2-46':{
  'lpt98':[(0,15),(.1,25),(.25,65),(.5,101),(.75,125),(1,143),(1.25,157),(1.5,176),(1.75,190),(2,207),(2.5,252),(3,298),(3.5,342),(4,404),(4.5,459),(5,515),(5.15,523),(5.2,537),(5.5,558),(5.6,575),(5.75,600),(6,624)],
  'lpt89':[(.04,8),(.25,28),(.5,52),(.75,68),(1,78),(1.5,102),(2,132),(2.5,173),(3,213),(3.5,252),(4,292),(4.5,331),(5,370),(5.5,414),(6,458)],
 },
 'F2-47':{
  'lpt101':[(0,45),(.25,230),(.5,341),(.75,385),(1,373),(1.25,356),(1.5,348),(1.75,370),(2,414),(2.5,506),(3,600),(3.5,705),(4,807),(4.5,910),(5,1020),(5.5,1130),(6,1235),(6.04,1240)],
  'lpt91':[(0,4),(.25,230),(.5,286),(.75,290),(1,305),(1.25,337),(1.5,385),(2,472),(2.5,586),(3,677),(3.5,791),(4,890),(4.5,976),(5,1070),(5.5,1161),(6,1257),(6.2,1315),(6.25,1334),(6.5,1364),(7,1438)],
 },
 'F2-48':{
  'lpt87':[(0,0),(.125,65),(.25,116),(.4,146),(.5,154),(.75,151),(1,146),(1.125,145),(1.25,153),(1.5,166),(1.75,187),(2,209),(2.5,256),(3,300),(3.5,357),(4,410),(4.5,468),(5,521),(5.5,584),(6,638),(6.5,695),(7,739),(7.5,795),(8,840),(8.04,845)],
  'lpt85':[(0,0),(.25,47),(.5,78),(.75,86),(1,89),(1.25,93),(1.5,111),(2,164),(2.5,209),(3,251),(3.5,295),(4,335),(4.5,371),(5,406),(5.5,458),(6,511),(6.5,565),(7,622),(7.5,686),(8,744)],
 }
}

def grid_dist(P,cal):
 P=np.asarray(P);d=np.full(P.shape[:-1],1e5)
 for l in cal['vertical_lines']:
  d=np.minimum(d,np.abs(P[...,0]-l['u_at_v0']-l['slope_du_dv']*P[...,1]))
 for l in cal['horizontal_lines']:
  d=np.minimum(d,np.abs(P[...,1]-l['v_at_u0']-l['slope_dv_du']*P[...,0]))
 return d

def getpix(g,P):
 P=np.rint(P).astype(int)
 return g[P[...,1],P[...,0]]

def tangent(guide,x,cal,X,Y):
 xx,yy=np.array(guide).T
 ya=np.interp(x-.035,xx,yy);yb=np.interp(x+.035,xx,yy)
 a=inv(x-.035,ya,cal,X,Y);b=inv(x+.035,yb,cal,X,Y)
 t=b-a;t/=np.linalg.norm(t);return t

def snap(g,guide,x,cal,X,Y,dotted):
 xx,yy=np.array(guide).T;y=np.interp(x,xx,yy);p=inv(x,y,cal,X,Y)
 t=tangent(guide,x,cal,X,Y);n=np.array([-t[1],t[0]])
 # Search along the axis of load around a visual guide; permit a small penetration shift
 # to avoid measuring a grid line or a gap. The exported point must be actual curve ink.
 a=X.e_s; b=Y.e_s
 choices=[]
 for dx in range(-18 if dotted else -10,19 if dotted else 11):
  Q=p+dx*a+np.arange(-85,86)[:,None]*b
  dark=(getpix(g,Q)<160)&(grid_dist(Q,cal)>5)
  inds=np.where(dark)[0]
  runs=np.split(inds,np.where(np.diff(inds)>1)[0]+1) if len(inds) else []
  for run in runs:
   if len(run)<2:continue
   q=Q[run].mean(axis=0)
   # The visual guide is only a locator. Prefer a small abscissa shift and the nearest run.
   dist=np.dot(q-p,b)
   score=dist**2+dx**2*2
   choices.append((score,q))
 if not choices:raise RuntimeError((x,p))
 _,q=min(choices,key=lambda z:z[0])
 # Refine across the local normal, using that trace's actual width.
 offs=np.arange(-15,15.01,.25);Q=q+offs[:,None]*n
 dark=getpix(g,Q)<180
 runs=np.split(np.where(dark)[0],np.where(np.diff(np.where(dark)[0])>1)[0]+1)
 run=min([r for r in runs if len(r)],key=lambda r:abs(offs[r].mean()))
 off=(offs[run[0]]+offs[run[-1]])/2;q=q+off*n
 half=(offs[run[-1]]-offs[run[0]]+.25)/2
 half=max(.75,half)
 # Half spacing between neighboring dash/dot ink runs, projected into u/v bounds.
 spacing=0
 if dotted:
  S=np.arange(-100,101,.5);offn=np.arange(-2,2.1,1)
  Q=q+S[:,None,None]*t+offn[None,:,None]*n
  dark=np.any(getpix(g,Q)<170,axis=1)
  runs=np.split(np.where(dark)[0],np.where(np.diff(np.where(dark)[0])>1)[0]+1)
  centers=[float(S[r].mean()) for r in runs if len(r)>2]
  centers=[s for s in centers if abs(s)<85]
  gaps=np.diff(centers)
  spacing=float(np.median(gaps[(gaps>5)&(gaps<85)]))/2 if np.any((gaps>5)&(gaps<85)) else (30 if '101' in str(guide) else 9)
 bu=half;bv=half
 if dotted:
  bu=max(half,abs(t[0])*spacing+abs(n[0])*half)
  bv=max(half,abs(t[1])*spacing+abs(n[1])*half)
 return q,bu,bv,half,spacing

def center_dot(g,p):
 u,v=np.rint(p).astype(int);mask=g[v-16:v+17,u-16:u+17]<180
 visited=set();todo=[(16,16)]
 while todo:
  a,b=todo.pop()
  if (a,b) in visited or not(0<=a<33 and 0<=b<33) or not mask[b,a]:continue
  visited.add((a,b));todo.extend([(a+1,b),(a-1,b),(a,b+1),(a,b-1)])
 # A grid line or lettering joined to a dot must not determine its centre.
 if 8<=len(visited)<180 and all(0<a<32 and 0<b<32 for a,b in visited):
  return np.array([u-16,v-16])+np.array(list(visited)).mean(axis=0)
 return p

def sample():
 for fid,(page,box) in FIGS.items():
  root=Path('out')/fid;cal,X,Y=maps(fid);g=np.asarray(Image.open(f'packet/p{page}.png').convert('L'))
  rows=[]
  for sid,guide in GUIDES[fid].items():
   dotted=sid in ('lpt79','lpt89','lpt101','lpt85')
   for x in np.arange(.25,guide[-1][0]+.001,.25):
    p,bu,bv,half,spacing=snap(g,guide,x,cal,X,Y,dotted)
    if dotted and sid!='lpt101':p=center_dot(g,p)
    note=f'target penetration {x:.2f} in; measured normal half-width {half:.2f} px'
    if dotted:note+=f'; on {"dash" if sid=="lpt101" else "dot"} ink; half repeat spacing {spacing:.2f} px'
    if grid_dist(p,cal)<10:note+='; close to grid crossing, shifted to distinguish trace ink'
    if fid=='F2-47' and (x<=.5 or 1.2<=x<=1.5 or x>=5.75):
     note+='; traces cross/run together; bound widened for branch overlap';bu=max(bu,10);bv=max(bv,10)
    rows.append(dict(figure_id=fid,panel=1,series_id=sid,point_kind='trace',sequence=0,pixel_u=round(p[0],2),pixel_v=round(p[1],2),u_bound_px=round(bu,2),v_bound_px=round(bv,2),symbol='',note=note,target_x_in=round(x,2)))
  for sid in GUIDES[fid]:
   rr=[r for r in rows if r['series_id']==sid]
   for i,r in enumerate(rr,1):r['sequence']=i
  writecsv(root/'points-p1.csv',rows)
  ca.piecewise_rows(cal,X,Y,rows)
  writecsv(root/'points-p1-native.csv',rows)
  print(fid,len(rows),'regular trace samples')

# Endpoints and sharp turns read on the unrotated, labeled pixel crops.
# Tuple: (u,v, half-width u, half-width v). Dotted endpoints include half spacing.
ENDS={
 'lpt95':[(2274,3593,8,8),(387,1466,8,8)],
 'lpt79':[(2274,3593,10,10),(1150,1687,7,9)],
 'lpt98':[(603,3391,8,8),(2439,1494,6,6)],
 'lpt89':[(614,3419,11,11),(2440,2012,9,9)],
 'lpt101':[(500,3218,18,28),(2343,2262,29,20)],
 'lpt91':[(502,3241,6,6),(2638,2101,6,6)],
 'lpt87':[(2268,3766,8,8),(983,1350,3,3)],
 'lpt85':[(2268,3766,10,10),(1134,1367,11,12)],
}
KNEES={
 'lpt95':[(.10,'knee; initial rise changes slope'),(.38,'knee; initial rounding'),(1.39,'knee; lower end of recorder step'),(1.46,'knee; upper end of recorder step'),(1.80,'knee; short steep recorder segment'),(1.86,'knee; end of short steep segment'),(2.40,'knee; lower end of recorder jog'),(2.47,'knee; upper end of recorder jog'),(2.73,'knee; ledge'),(2.82,'knee; end of ledge'),(3.08,'knee; short jog'),(3.16,'knee; end of short jog'),(3.84,'knee; steep recorder jog'),(3.91,'knee; end of steep jog'),(4.76,'knee; small recorder jog'),(4.83,'knee; end of small jog'),(5.25,'knee; shoulder'),(5.34,'knee; end of shoulder'),(5.56,'knee; recorder jog'),(5.64,'knee; end of recorder jog'),(6.12,'knee; shoulder above 250 lb'),(6.35,'knee; end of shoulder')],
 'lpt79':[(.84,'knee; end of initial curvature'),(5.58,'knee; slight steepening')],
 'lpt98':[(.11,'knee; initial steepening'),(.37,'knee; end of initial steep rise'),(.67,'knee; rounding into lower slope'),(1.36,'knee; small recorder shoulder'),(1.58,'knee; end of shoulder'),(3.32,'knee; steepening'),(3.67,'knee; end of steeper segment'),(4.24,'knee; start of steep recorder rise'),(4.38,'knee; end of steep rise'),(4.63,'knee; renewed steep rise'),(5.08,'knee; lower end of abrupt recorder step'),(5.16,'knee; upper end of step'),(5.54,'knee; start of small load drop'),(5.59,'knee; end of small drop'),(5.72,'knee; end of steep rise near 600 lb')],
 'lpt89':[(.60,'knee; initial rounding'),(1.53,'knee; gradual steepening'),(2.08,'knee; end of gradual steepening'),(5.08,'knee; slight increase of slope')],
 'lpt101':[(.42,'knee; initial rounding'),(.78,'knee; local load maximum on first hump, not global peak'),(1.43,'knee; local load minimum after hump'),(1.72,'knee; transition into rising segment')],
 'lpt91':[(.44,'knee; end of initial steep rise'),(.83,'knee; end of nearly level shoulder'),(1.13,'knee; start of sustained rise'),(1.99,'knee; small recorder shoulder'),(2.16,'knee; end of recorder shoulder'),(3.73,'knee; small recorder shoulder'),(4.03,'knee; end of shoulder'),(5.10,'knee; small recorder shoulder'),(5.24,'knee; end of shoulder'),(6.07,'knee; steepening next to dashed endpoint'),(6.21,'knee; end of steepening')],
 'lpt87':[(.16,'knee; end of initial steep rise'),(.58,'knee; local maximum before shallow load decrease'),(.73,'knee; small recorder jog on falling shoulder'),(1.09,'knee; local minimum after shoulder'),(1.37,'knee; start of sustained rise'),(1.93,'knee; recorder jog'),(2.10,'knee; end of jog'),(2.78,'knee; recorder jog'),(2.93,'knee; end of jog'),(4.62,'knee; short recorder jog'),(4.72,'knee; end of short jog'),(5.68,'knee; short recorder jog'),(5.80,'knee; end of short jog'),(6.52,'knee; slope transition')],
 'lpt85':[(.55,'knee; initial rounding into shoulder'),(1.18,'knee; end of shoulder'),(1.52,'knee; start of sustained rise'),(4.98,'knee; steeper upper segment')],
}

def finalize():
 for fid,(page,box) in FIGS.items():
  root=Path('out')/fid;cal,X,Y=maps(fid);g=np.asarray(Image.open(f'packet/p{page}.png').convert('L'))
  old=list(csv.DictReader((root/'points-p1.csv').open()));rows=[]
  for sid,guide in GUIDES[fid].items():
   rr=[r for r in old if r['series_id']==sid]
   # A last nominal sample landing on the right frame is moved to the last dot's own ink.
   if sid=='lpt89':
    rr[-1].update(pixel_u=2436.5,pixel_v=2017.0,u_bound_px=9,v_bound_px=9,note='target penetration 6.00 in; last distinct dot before frame; half dot spacing bound')
   if sid=='lpt95':
    rr[-1].update(pixel_u=387,pixel_v=1466,u_bound_px=8,v_bound_px=8,note='target penetration 7.00 in; curve merges into far frame; endpoint bound widened')
   dotted=sid in ('lpt79','lpt89','lpt101','lpt85')
   def row(p,kind,note,target=''):
    u,v,bu,bv=p
    return dict(figure_id=fid,panel=1,series_id=sid,point_kind=kind,sequence=0,pixel_u=round(float(u),2),pixel_v=round(float(v),2),u_bound_px=round(float(bu),2),v_bound_px=round(float(bv),2),symbol='',note=note,target_x_in=target)
   first,last=ENDS[sid]
   nfirst='first; visible trace ink start'
   if sid in ('lpt95','lpt79','lpt91','lpt87','lpt85'):nfirst+='; origin/frame overlap with other trace, bound widened'
   if sid=='lpt98':nfirst+='; starts against penetration-zero frame above load zero'
   if sid=='lpt89':nfirst+='; first visible dot just inside zero frame; origin hidden by frame'
   if sid=='lpt101':nfirst+='; initial dash next to solid trace and zero frame; overlap bound widened'
   nlast='last; last visible trace ink'
   if sid in ('lpt95','lpt98','lpt91'):nlast+='; meets plot frame, endpoint bound widened'
   if sid=='lpt101':nlast+='; last distinguishable dash cap near 6 in, nearly merges with solid; no separable dashed continuation'
   if sid=='lpt85':nlast+='; topmost dot joins 8-inch grid line; bound includes unresolved cap'
   if dotted:nfirst+='; half dot/dash repeat spacing included';nlast+='; half dot/dash repeat spacing included'
   middle_features=[]
   for x,note in KNEES[sid]:
    p,bu,bv,half,spacing=snap(g,guide,x,cal,X,Y,dotted)
    if sid=='lpt95' and x==.10:p=np.array([2191.,3556.]);bu=bv=5.12
    if sid=='lpt98' and x==5.08:p=np.array([2175.,1810.]);bu=bv=4
    if sid=='lpt98' and x==5.16:p=np.array([2186.,1770.]);bu=bv=4
    if dotted and sid!='lpt101':p=center_dot(g,p)
    if sid=='lpt101' and x<1.8:bu=max(bu,10);bv=max(bv,10)
    note+=f'; measured normal half-width {half:.2f} px'
    if dotted:note+=f'; on dot/dash ink; half repeat spacing {spacing:.2f} px'
    middle_features.append(row((*p,bu,bv),'feature',note,x))
   # Merge the already ordered traversal events; never sort measured points by x.
   # Both declining-load shoulders retain their original drawing direction.
   ordered=[row(first,'trace',nfirst,0),row(first,'feature',nfirst)]
   k=0
   for r in rr:
    while k<len(middle_features) and float(middle_features[k]['target_x_in'])<=float(r['target_x_in']):
     ordered.append(middle_features[k]);k+=1
    ordered.append(r)
   ordered.extend(middle_features[k:])
   ordered.extend([row(last,'trace',nlast),row(last,'feature',nlast),row(last,'feature','peak; maximum visible load; coincides with last ink endpoint')])
   rr=ordered
   for i,r in enumerate(rr,1):r['sequence']=i
   rows+=rr
  writecsv(root/'points-p1.csv',rows);ca.piecewise_rows(cal,X,Y,rows);writecsv(root/'points-p1-native.csv',rows)
  print(fid,len(rows),'rows')

def qa(features_only=False):
 font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
 for fid,(page,box) in FIGS.items():
  root=Path('out')/fid; im=Image.open(f'packet/p{page}.png').convert('RGB')
  rows=list(csv.DictReader((root/'points-p1.csv').open()))
  if features_only:rows=[r for r in rows if r['point_kind']=='feature']
  for start in range(0,len(rows),24):
   sheet=Image.new('RGB',(1200,1440),'white');d=ImageDraw.Draw(sheet)
   for j,r in enumerate(rows[start:start+24]):
    u,v=float(r['pixel_u']),float(r['pixel_v']);x=j%4*300;y=j//4*240
    crop=im.crop((round(u)-45,round(v)-32,round(u)+45,round(v)+32)).resize((270,192))
    sheet.paste(crop,(x,y+43));
    d.text((x+2,y+2),f"{r['series_id']} {r['sequence']} {r['point_kind']}",font=font,fill='black')
    d.text((x+2,y+22),f"x {r['target_x_in']}  ({u:.1f},{v:.1f})",font=font,fill='black')
    cx=x+135+(u-round(u))*3;cy=y+139+(v-round(v))*3
    d.ellipse((cx-7,cy-7,cx+7,cy+7),outline='red',width=1)
   sheet.save(root/f'qa-{"features" if features_only else "samples"}-{start//24+1}.png')

def labels():
 checks={
  'F2-45':{'x':[0,3,7],'y':[0,100,250]},
  'F2-46':{'x':[0,3,6],'y':[0,300,600]},
  'F2-47':{'x':[0,3,7],'y':[0,1000,2000]},
  'F2-48':{'x':[0,1,8,2],'y':[0,600,1200]},
 }
 font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
 for fid,(page,box) in FIGS.items():
  root=Path('out')/fid;cal,X,Y=maps(fid);im=Image.open(f'packet/p{page}.png').convert('RGB')
  sheet=Image.new('RGB',(1080,840),'white');d=ImageDraw.Draw(sheet);rows=[]
  for j,(axis,value) in enumerate([(a,v) for a,vv in checks[fid].items() for v in vv]):
   p=inv(value,0,cal,X,Y) if axis=='x' else inv(0,value,cal,X,Y)
   # Native, unrotated crop: includes the printed number next to its grid line.
   u,v=np.rint(p).astype(int)
   if fid in ('F2-45','F2-48'):
    cropbox=(u-45,v-45,u+110,v+55) if axis=='x' else (u-45,v-35,u+55,v+120)
   else:cropbox=(u-60,v-35,u+60,v+100) if axis=='x' else (u-145,v-40,u+45,v+55)
   crop=im.crop(cropbox);crop.thumbnail((344,235))
   x=j%3*360;y=j//3*280;sheet.paste(crop,(x,y+40))
   d.text((x,y),f'{axis}={value}  line ({p[0]:.1f},{p[1]:.1f})',font=font,fill='black')
   rows.append(dict(axis=axis,printed_label=str(value),line_u=round(float(p[0]),2),line_v=round(float(p[1]),2),checked_by_eye='yes',result='label matches anchored line',note='Unrotated scanned page; checked number and adjacent ink line, not frame extent'))
  sheet.save(root/'calibration-label-crops.png');writecsv(root/'calibration-eye-checks.csv',rows)

if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='sample':sample()
 elif len(sys.argv)>1 and sys.argv[1]=='recover':recover47();init()
 elif len(sys.argv)>1 and sys.argv[1]=='qa':qa()
 elif len(sys.argv)>1 and sys.argv[1]=='finalize':finalize()
 elif len(sys.argv)>1 and sys.argv[1]=='features-qa':qa(True)
 elif len(sys.argv)>1 and sys.argv[1]=='labels':labels()
 else:init()
