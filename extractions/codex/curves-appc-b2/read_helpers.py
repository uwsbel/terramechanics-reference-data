import csv,json,sys,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
COLS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
def components(a):
 seen=np.zeros(a.shape,bool); out=[]
 for y,x in zip(*np.where(a)):
  if seen[y,x]:continue
  stack=[(y,x)]; seen[y,x]=True; pts=[]
  while stack:
   yy,xx=stack.pop();pts.append((xx,yy))
   for dy in [-1,0,1]:
    for dx in [-1,0,1]:
     ny,nx=yy+dy,xx+dx
     if 0<=ny<a.shape[0] and 0<=nx<a.shape[1] and a[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;stack.append((ny,nx))
  if len(pts)>7:out.append(np.array(pts))
 return out
def refine(g,u,v,b,symbol):
 if b>3:return u,v,b,'manual-wide'
 # Prefer the outer ink box when the complete symbol is disconnected from other ink.
 if symbol!='plus':
  u0,v0=round(u)-32,round(v)-32;isolated=[]
  for c in components(g[v0:v0+65,u0:u0+65]<160):
   lo=c.min(0);hi=c.max(0);w,h=hi-lo+1;mid=(lo+hi)/2+[u0,v0]
   if 7<=w<=39 and 7<=h<=39 and np.linalg.norm(mid-[u,v])<12:
    isolated.append((np.linalg.norm(mid-[u,v]),mid))
  if isolated:
   mid=min(isolated,key=lambda z:z[0])[1]
   return *mid,b,'ink-bounding-box'
 # Closed white interiors isolate a hollow marker even when its outline joins curve ink.
 u0,v0=round(u)-27,round(v)-27
 if symbol!='plus':
  candidates=[]
  for c in components(g[v0:v0+55,u0:u0+55]>=160):
   lo=c.min(0);hi=c.max(0);w,h=hi-lo+1
   if np.any(lo==0) or np.any(hi==54):continue
   mid=(lo+hi)/2+[u0,v0]
   if 4<=w<=37 and 4<=h<=37 and np.linalg.norm(mid-[u,v])<13:
    if symbol=='triangle-up':mid[1]-=1.5
    if symbol=='triangle-down':mid[1]+=1.5
    candidates.append((np.linalg.norm(mid-[u,v]),mid))
  if candidates:
   mid=min(candidates,key=lambda z:z[0])[1]
   return *mid,max(b,5 if symbol.startswith('triangle') else 2),'hollow-interior'
 else:
  # Two orthogonal bars distinguish a plus from a diagonal author-drawn stroke.
  candidates=[]
  for yy in range(round(v)-10,round(v)+11):
   for xx in range(round(u)-10,round(u)+11):
    hf=(g[yy-1:yy+2,xx-8:xx+9]<160).max(axis=0).mean()
    vf=(g[yy-8:yy+9,xx-1:xx+2]<160).max(axis=1).mean()
    if min(hf,vf)>=.65:
     score=min(hf,vf)+.3*(hf+vf)-.001*((xx-u)**2+(yy-v)**2)
     candidates.append((score,xx,yy))
  if candidates:
   score,xx,yy=max(candidates)
   return xx,yy,b,'orthogonal-bars'
 u0,v0=round(u)-32,round(v)-32;candidates=[]
 for c in components(g[v0:v0+65,u0:u0+65]<160):
  lo=c.min(0);hi=c.max(0);w,h=hi-lo+1;mid=(lo+hi)/2+[u0,v0]
  if 7<=w<=39 and 7<=h<=39 and np.linalg.norm(mid-[u,v])<12:
   candidates.append((np.linalg.norm(mid-[u,v]),mid))
 if candidates:
  mid=min(candidates,key=lambda z:z[0])[1]
  return *mid,b,'ink-bounding-box'
 return u,v,max(b,6),'manual-unisolated'
def runs(a):
 ids=np.where(a)[0];out=[]
 if len(ids):
  groups=np.split(ids,np.where(np.diff(ids)>1)[0]+1)
  out=[((q[0]+q[-1])/2,len(q)) for q in groups]
 return out
def build(specfile):
 s=json.loads(Path(specfile).read_text(encoding='utf-8-sig'));fid=s['figure'];od=ROOT/'out'/fid;od.mkdir(exist_ok=True)
 g=np.array(Image.open(ROOT/s['image']).convert('L'));summary={};diagnostics={};marker_audit=[]
 for panel in [1,2]:
  cal=json.loads((od/f'cal-p{panel}/calibration.json').read_text());rows=[];mark=[];geometry=[]
  for msid,md in s['panels'][str(panel)].items():
   for mp in md['markers']:
    mu,mv=mp[:2];mb=mp[2] if len(mp)>2 else 2
    mu,mv,mb,_=refine(g,mu,mv,mb,md['symbol'])
    hw={'plus':16,'circle':19,'square':17,'triangle-up':20,'triangle-down':20}[md['symbol']]
    hh={'plus':16,'circle':19,'square':17,'triangle-up':19,'triangle-down':19}[md['symbol']]
    geometry.append((mu,mv,hw+(3 if mb>=8 else 0),hh+(3 if mb>=8 else 0)))
  for sid,d in s['panels'][str(panel)].items():
   for i,p in enumerate(d['markers'],1):
    u,v=p[:2];b=p[2] if len(p)>2 else 2;note=p[3] if len(p)>3 else ''
    nu,nv,b,method=refine(g,u,v,b,d['symbol'])
    marker_audit.append({'panel':panel,'series':sid,'sequence':i,'seed':[u,v],'center':[nu,nv],'method':method,'bound':b})
    if method=='hollow-interior' and d['symbol'].startswith('triangle'):note+=' Triangle outer outline joins other ink; interior-based center has 5 px bound.'
    if method=='manual-unisolated':note+=' Symbol joins other ink or has a broken outline; by-eye center retained with widened bound.'
    rows.append(dict(zip(COLS,[fid,panel,sid,'marker',i,nu,nv,b,b,d['symbol'],note])))
    mark.append((sid,nu,nv,b))
   if 'guide' in d:
    guide=np.array(d['guide'],float);trace=[];miss=[]
    for target in range(int(guide[0,0]),int(guide[-1,0])+1,12):
     cand=[]
     for du in [0,3,-3,6,-6]:
      u=target+du
      if u<guide[0,0] or u>guide[-1,0] or (trace and u<=trace[-1]['pixel_u']):continue
      vguess=np.interp(u,guide[:,0],guide[:,1])
      if any(lo<=u<=hi for lo,hi in d.get('trace_exclude_ranges',[])):continue
      if any(abs(u-(l['u_at_v0']+l['slope_du_dv']*vguess))<6 for l in cal['vertical_lines']):continue
      radius=28
      v0=int(vguess)-radius; seg=g[v0:v0+2*radius+1,u]<180
      for center,w in runs(seg):
       v=v0+center
       if w<3 or w>40 or abs(v-vguess)>radius-3:continue
       if any(abs(u-mu)<=hw and abs(v-mv)<=hh+w/2 for mu,mv,hw,hh in geometry):continue
       neargrid=any(abs(v-(l['v_at_u0']+l['slope_dv_du']*u))<5 for l in cal['horizontal_lines'])
       if neargrid and (not d.get('shared_grid',False) or not any(abs(vguess-(l['v_at_u0']+l['slope_dv_du']*u))<=10 for l in cal['horizontal_lines'])):continue
       shared=any(lo<=u<=hi for lo,hi,_,_ in d.get('ambiguous_ranges',[]))
       if not shared:
        wrong_branch=False
        for osid,other_spec in s['panels'][str(panel)].items():
         if osid==sid or 'guide' not in other_spec:continue
         og=np.array(other_spec['guide'],float)
         if not og[0,0]<=u<=og[-1,0]:continue
         ov=np.interp(u,og[:,0],og[:,1])
         if abs(ov-vguess)>10 and abs(v-vguess)>8 and abs(v-ov)+3<abs(v-vguess):wrong_branch=True
        if wrong_branch:continue
       score=abs(v-vguess)+abs(du)*.5+max(0,6-w)
       cand.append((score,u,v,w,neargrid))
     if not cand:miss.append(target);continue
     _,u,v,w,neargrid=min(cand)
     note='Drawn ink sample; column selected near regular 12 px sampling grid.'
     if neargrid:note+=' Curve shares or approaches horizontal grid ink; widened bound.'
     vb=max(w/2,7 if neargrid else 0)
     for lo,hi,bb,nn in d.get('ambiguous_ranges',[]):
      if lo<=u<=hi:vb=max(vb,bb);note+=' '+nn
     row=dict(zip(COLS,[fid,panel,sid,'trace',len(trace)+1,u,v,1,vb,'',note]));trace.append(row)
    rows+=trace;diagnostics[f'{panel}/{sid}']={'missed_target_columns':miss,'largest_sample_spacing_native':round(max([((trace[i]['pixel_u']-trace[i-1]['pixel_u'])*cal['x_per_px']) for i in range(1,len(trace))] or [0]),3)}
    for i,p in enumerate(d.get('features',[]),1):
     if len(p)==4:u,v,b,name=p;bu=b;bv=b
     else:u,v,bu,bv,name=p
     rows.append(dict(zip(COLS,[fid,panel,sid,'feature',i,u,v,bu,bv,'',name])))
  path=od/f'points-p{panel}.csv'
  with path.open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,COLS,lineterminator='\n');w.writeheader();w.writerows(rows)
  subprocess.run([sys.executable,str(ROOT/'tools/calibrate_axes.py'),'apply',str(od/f'cal-p{panel}/calibration.json'),str(path),str(od/f'points-p{panel}-native.csv')],check=True)
  subprocess.run([sys.executable,str(ROOT/'tools/plot_grid.py'),'overlay',str(ROOT/s['image']),'--points',str(path),'--out',str(od/f'overlay-p{panel}.png'),'--box',*[str(v) for v in s['overlay_boxes'][str(panel)]]],check=True)
  summary[str(panel)]={sid:{k:sum(r['series_id']==sid and r['point_kind']==k for r in rows) for k in ['marker','trace','feature']} for sid in s['panels'][str(panel)]}
 checks=[]
 for p,axis,val,other,eye in s['eye_checks']:
  cal=json.loads((od/f'cal-p{p}/calibration.json').read_text());a=cal['ax'] if axis=='x' else cal['ay']
  fitted=(val-a[1]*other-a[2])/a[0] if axis=='x' else (val-a[0]*other-a[2])/a[1]
  checks.append({'figure':fid,'panel':p,'axis':axis,'printed_label':val,'fitted_pixel':round(fitted,2),'eye_pixel':eye})
 with (od/'calibration-eye-checks.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,checks[0].keys(),lineterminator='\n');w.writeheader();w.writerows(checks)
 (od/'counts.json').write_text(json.dumps(summary,indent=2));(od/'trace-sampling-audit.json').write_text(json.dumps(diagnostics,indent=2))
 (od/'marker-center-audit.json').write_text(json.dumps(marker_audit,indent=2));print(json.dumps(summary));print(json.dumps(diagnostics))
if __name__=='__main__':build(sys.argv[1])



