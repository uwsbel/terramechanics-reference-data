import csv,json,sys,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
PY=sys.executable
COLS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
def run(*a):
 subprocess.run([PY,*map(str,a)],check=True)
def dark_runs(a):
 ids=np.flatnonzero(a); out=[]
 if not len(ids): return out
 st=pr=ids[0]
 for z in ids[1:]:
  if z>pr+1: out.append((float((st+pr)/2),int(pr-st+1)));st=z
  pr=z
 out.append((float((st+pr)/2),int(pr-st+1)))
 return out

def hole_refine(im,u,v,sym):
 # Only use an enclosed white interior; no exterior contour or neighboring hole.
 rad=35;u=int(u);v=int(v);a=im[v-rad:v+rad+1,u-rad:u+rad+1]>200
 seen=set(); candidates=[]
 for yy,xx in zip(*np.where(a)):
  if (yy,xx) in seen:continue
  stack=[(yy,xx)];seen.add((yy,xx)); cc=[];border=False
  while stack:
   y,x=stack.pop();cc.append((y,x));border|=y in (0,2*rad) or x in (0,2*rad)
   for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
    ny,nx=y+dy,x+dx
    if 0<=ny<a.shape[0] and 0<=nx<a.shape[1] and a[ny,nx] and (ny,nx) not in seen:
     seen.add((ny,nx));stack.append((ny,nx))
  if border or len(cc)<12:continue
  ys,xs=zip(*cc);cx=(min(xs)+max(xs))/2+u-rad;cy=(min(ys)+max(ys))/2+v-rad
  ratio=len(cc)/((max(xs)-min(xs)+1)*(max(ys)-min(ys)+1))
  shape_ok=ratio<.72 if sym.startswith('triangle') else (ratio>.75 if sym=='square' else .6<ratio<.94)
  if shape_ok and abs(cx-u)<22 and abs(cy-v)<22: candidates.append((len(cc),cx,cy))
 if candidates:
  _,u,v=max(candidates)
 return u,v

def plus_refine(im,u,v):
 rad=27;u=int(u);v=int(v);a=im[v-rad:v+rad+1,u-rad:u+rad+1]<200;seen=set();cs=[]
 for yy,xx in zip(*np.where(a)):
  if (yy,xx) in seen:continue
  stack=[(yy,xx)];seen.add((yy,xx));cc=[];border=False
  while stack:
   y,x=stack.pop();cc.append((y,x));border|=y in (0,2*rad) or x in (0,2*rad)
   for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
    ny,nx=y+dy,x+dx
    if 0<=ny<a.shape[0] and 0<=nx<a.shape[1] and a[ny,nx] and (ny,nx) not in seen:
     seen.add((ny,nx));stack.append((ny,nx))
  if border or len(cc)<30:continue
  ys,xs=zip(*cc);width=max(xs)-min(xs);height=max(ys)-min(ys)
  if width<12 or height<12:continue
  cx=(min(xs)+max(xs))/2+u-rad;cy=(min(ys)+max(ys))/2+v-rad
  if abs(cx-u)<18 and abs(cy-v)<18:cs.append((len(cc),cx,cy))
 if cs:_,u,v=max(cs)
 return u,v

def build(path):
 cfg=json.loads(Path(path).read_text(encoding='utf-8-sig'));fig=cfg['figure'];base=Path('out')/fig;im=np.asarray(Image.open(cfg['image']).convert('L'));summary=[]
 for panel in [1,2]:
  rows=[];cal=json.loads((base/f'cal-p{panel}/calibration.json').read_text());seq={}
  def add(sid,kind,u,v,bu,bv,sym,note):
   seq[sid]=seq.get(sid,0)+1
   rows.append(dict(zip(COLS,[fig,panel,sid,kind,seq[sid],u,v,bu,bv,sym,note])))
  for sid,dat in cfg['series'].items():
   sym=dat['symbol'];markers=dat.get(f'm{panel}',[])
   refined=[]
   for m in markers:
    u,v=m[:2];bound=m[2] if len(m)>2 and isinstance(m[2],(int,float)) else 2;note=m[3] if len(m)>3 else ''
    if sym in ['circle','square','triangle-up','triangle-down'] and not note.startswith('unresolved'):
     orig=(u,v);u,v=hole_refine(im,u,v,sym)
     if (u,v)==orig and bound==2: bound=6;note='Outline interrupted by trace/grid; manual center with wider bound.'
    if sym=='plus' and not note: u,v=plus_refine(im,u,v)
    refined.append((u,v,bound))
    add(sid,'marker',u,v,bound,bound,sym,note)
   guide=dat.get(f't{panel}',[])
   if not guide:continue
   us,vs=np.array(guide).T
   def locate(u,maxshift=11):
    opts=[]
    for du in sorted(range(-maxshift,maxshift+1),key=abs):
     x=int(u+du)
     y=float(np.interp(x,us,vs))
     if x<us[0] or x>us[-1]:continue
     if any(abs(x-(l['u_at_v0']+l['slope_du_dv']*y))<5 for l in cal['vertical_lines']):continue
     if any(abs(x-mu)<(19 if sym.startswith('triangle') or sym=='square' else 16) for mu,mv,b in refined if abs(y-mv)<45):continue
     lo=max(0,int(y-24));hi=min(im.shape[0],int(y+25))
     rs=dark_runs(im[lo:hi,x]<200)
     for c,w in rs:
      vv=lo+c
      if abs(vv-y)>18 or w<7 or w>40:continue
      # Reject horizontal grid ink, except explicit coincident trace cases.
      if any(abs(vv-(l['v_at_u0']+l['slope_dv_du']*x))<5 for l in cal['horizontal_lines']) and not dat.get('grid_overlap'):continue
      opts.append((abs(du)+abs(vv-y)*.4-w*.5,x,vv,w))
    if not opts:return None
    _,x,y,w=min(opts);return x,y,w
   samples=[]; intervals=[]; current=[]
   for u in range(int(us[0]),int(us[-1])+1):
    r=locate(u,0)
    if r:
     if current and (r[0]-current[-1][0]>1 or abs(r[1]-current[-1][1])>15):intervals.append(current);current=[]
     current.append(r)
    elif current:intervals.append(current);current=[]
   if current:intervals.append(current)
   for cc in intervals:
    if len(cc)<3:continue
    samples.extend(cc[1:-1:20]);samples.append(cc[-2])
   for key in ['first','peak','last']:
    if key in dat:
     u,v=dat[key];r=locate(u,4)
     if r:samples.append(r)
   samples=sorted(set(samples))
   for u,v,w in samples:add(sid,'trace',u,v,1,max(.5,w/2),'','Column dark-run center; guide used only to select ink.')
   for key in ['first','peak','last']:
    if key not in dat:continue
    u,v=dat[key];r=(u,v,dat.get('feature_widths',{}).get(key,dat.get('feature_width',10)))
    if r:
     uu,vv,w=r;add(sid,'feature',uu,vv,dat.get('peak_u_bound',2) if key=='peak' else 2,max(.5,w/2),'',key+' point of drawn trace'+('; broad/flat maximum' if key=='peak' and dat.get('peak_u_bound',0)>2 else ''))
    else: print('FEATURE NOT ON ACCEPTED INK',fig,sid,key,u,v)
   gaps=[round((b[0]-a[0])*cal['x_per_px'],2) for a,b in zip(samples,samples[1:]) if (b[0]-a[0])*cal['x_per_px']>5]
   if gaps: print('ink gaps >5',fig,panel,sid,gaps)
  p=base/f'points-p{panel}.csv'
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=COLS);w.writeheader();w.writerows(rows)
  run('tools/calibrate_axes.py','apply',base/f'cal-p{panel}/calibration.json',p,base/f'points-p{panel}-native.csv')
  run('tools/plot_grid.py','overlay',cfg['image'],'--points',p,'--box',*cfg[f'overlay{panel}'],'--out',base/f'overlay-p{panel}.png')
  for sid in cfg['series']:
   rr=[r for r in rows if r['series_id']==sid];ct={k:sum(r['point_kind']==k for r in rr) for k in ['marker','trace','feature']};summary.append([fig,panel,sid,*ct.values(),len(rr)])
 with (base/'counts.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['figure_id','panel','series_id','markers','traces','features','total']);w.writerows(summary)
 print(summary)
if __name__=='__main__':build(sys.argv[1])

