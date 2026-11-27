import sys,csv,json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'tools');import calibrate_axes as ca
from guides import CURVES
COLS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']

def runs(a):
 ix=np.flatnonzero(a)
 return [g for g in np.split(ix,np.where(np.diff(ix)>1)[0]+1) if len(g)]
def gu(P,v):return float(np.interp(v,P[::-1,1],P[::-1,0]))
def savecsv(path,rows):
 with open(path,'w',newline='',encoding='utf-8') as fp:
  w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def maskgrid(c,g):
 mask=np.zeros(g.shape,dtype=bool);vv=np.arange(g.shape[0]);uu=np.arange(g.shape[1])
 for l in c['vertical_lines']:
  us=l['u_at_v0']+l['slope_du_dv']*vv
  for d in range(-7,8):mask[vv,np.clip(np.rint(us).astype(int)+d,0,g.shape[1]-1)]=True
 for l in c['horizontal_lines']:
  vs=l['v_at_u0']+l['slope_dv_du']*uu
  for d in range(-7,8):mask[np.clip(np.rint(vs).astype(int)+d,0,g.shape[0]-1),uu]=True
 return mask

def overlap(f,s,x):
 if f=='F2-32':
  if s in ['lpt52','lpt53'] and 2.9<x<7.2:return 'solid and dotted traces close/run together; branch uncertainty'
  if s in ['lpt52','fit'] and 6.4<x<7.3:return 'dotted trace meets/crosses fit'
  if s in ['lpt93','fit'] and (.15<x<.8 or 5.9<x<6.8):return 'dashed trace crosses fit'
 if f=='F2-33':
  if s in ['lpt74','fit'] and .3<x<.65:return 'thin trace crosses fit'
  if s in ['lpt75','fit'] and 2.65<x<3.3:return 'thick recorded trace and fit cross/run together'
  if s in ['lpt74','lpt75'] and 2.15<x<2.4:return 'recorded traces cross'
  if s in ['lpt74','bce'] and .08<x<.3:return 'thin trace crosses bearing-capacity line'
  if s in ['lpt75','bce'] and 2.05<x<2.25:return 'thick trace crosses bearing-capacity line'
 if f=='F2-34':
  if s in ['lpt88','fit'] and 3.8<x<5.5:return 'thin record and fit close/cross; branch uncertainty'
  if s in ['lpt87','fit'] and (.05<x<.4 or 2.15<x<2.5):return 'surface-start trace crosses fit'
  if s in ['lpt87','lpt88'] and 2.15<x<2.6:return 'recorded traces cross/run together'
 return ''

for f,fc in CURVES.items():
 d=Path('out')/f;page=Path(f'packet/p{fc["page"]:04}.png');g=np.array(Image.open(page).convert('L'))
 c,X,Y=ca.piecewise_maps(d/'cal-p1',page);mask=maskgrid(c,g);rows=[]
 (d/'cal-p1/verified-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 c['x_unit']='inch';c['y_unit']='lb';c['y_axis_label_printed']='Load - Lbs. x 100' if f=='F2-34' else 'Load (Lb.)' if f in ['F2-32','F2-33'] else 'Load (Lbs.)'
 (d/'cal-p1/calibration.json').write_text(json.dumps(c,indent=2))
 for s,sc in fc['curves'].items():
  P=np.array(sc['p'],float)
  # Locate recorder ink in each unrotated page row. Grid ink is excluded from the search.
  dense=[]
  for v in range(int(P[-1,1]),int(P[0,1])+1):
   pred=gu(P,v);lo=max(0,int(pred-38));hi=min(g.shape[1],int(pred+39))
   rr=[a+lo for a in runs((g[v,lo:hi]<180)&~mask[v,lo:hi]) if len(a)>=2]
   if not rr:continue
   if sc.get('straight'):r=min(rr,key=lambda a:abs(a.mean()-pred))
   elif f=='F2-32' and s in ['lpt53','lpt52'] and v<3070:
    near=[a for a in rr if abs(a.mean()-pred)<27]
    if near:r=(max if s=='lpt53' else min)(near,key=lambda a:a.mean())
    else:r=min(rr,key=lambda a:abs(a.mean()-pred))
   else:r=min(rr,key=lambda a:abs(a.mean()-pred))
   if abs(r.mean()-pred)>32:continue
   dense.append((v,float(r.mean())))
  D=np.array(dense)
  def center(v,endpoint=False):
   pred=gu(P,v)
   if not endpoint and min(abs(v-P[0,1]),abs(v-P[-1,1]))<8:
    e=P[0] if abs(v-P[0,1])<abs(v-P[-1,1]) else P[-1]
    return float(e[0]),float(e[1])
   if endpoint:
    # Cap center on terminal ink, retaining its observed location rather than extending the guide.
    return pred,float(v)
   z=D[np.abs(D[:,0]-v)<12]
   if len(z)>=5:
    coef=np.polyfit(z[:,0]-v,z[:,1],1);pred=float(coef[1])
   elif len(z):pred=float(z[np.argmin(abs(z[:,0]-v)),1])
   else:return pred,float(v)
   # Use actual ink at the requested penetration row, or the nearest dash/dot if that row is a gap.
   candidates=[]
   for dv in [0,-1,1,-2,2,-3,3,-4,4,-5,5,-6,6,-8,8,-10,10]:
    vv=int(round(v+dv));pp=pred+(gu(P,v+dv)-gu(P,v));lo=int(pp-12);hi=int(pp+13)
    if vv<0 or vv>=g.shape[0]:continue
    rr=runs(g[vv,lo:hi]<180)
    for a in rr:
     if len(a)>0:
      u=float(a.mean()+lo)
      if mask[vv,int(round(u))] and dv==0 and not(sc.get('dashed') or sc.get('dotted')):
       return pred,float(v)
      if len(a)>=2 and abs(u-pp)<10 and not mask[vv,int(round(u))]:candidates.append((abs(dv)*1.2+abs(u-pp),u,float(vv)))
    if candidates and dv==0:break
   if candidates:
    _,u,vv=min(candidates);return u,vv
   return pred,float(v)
  def width(u,v):
   # Normal transects of nearby ink give local stroke thickness, avoiding the grid.
   slope=(gu(P,v+8)-gu(P,v-8))/16
   normal=np.array([1.,-slope]);normal/=np.linalg.norm(normal)
   ws=[]
   for dv in [-9,-6,-3,0,3,6,9]:
    vv=v+dv;uu=u+gu(P,vv)-gu(P,v)
    ds=np.arange(-15,15.01,.5);ps=np.array([uu,vv])+ds[:,None]*normal
    ui=np.rint(ps[:,0]).astype(int);vi=np.rint(ps[:,1]).astype(int)
    valid=(ui>=0)&(ui<g.shape[1])&(vi>=0)&(vi<g.shape[0]);ui=ui[valid];vi=vi[valid];dd=ds[valid]
    ink=(g[vi,ui]<180)&~mask[vi,ui]
    rr=runs(ink)
    if rr:
     r=min(rr,key=lambda a:abs(dd[a].mean()))
     if abs(dd[r].mean())<4:ws.append((dd[r[-1]]-dd[r[0]]+.5)/2)
   return max(1.,round(float(np.median(ws)) if ws else 3.,2))
  specs=[]
  if sc.get('straight'):
   # The endpoints and every labelled penetration crossing, no equation-derived coordinates.
   specs=[(P[0,1],'trace','ink start',True),(P[-1,1],'trace','ink end',True)]
   xmin,xmax=sorted([X.value(*P[0])[0],X.value(*P[-1])[0]])
   for kn in X.knots:
    x=kn['value']
    if xmin<x<xmax:
     vlo,vhi=P[-1,1],P[0,1]
     for _ in range(30):
      vm=(vlo+vhi)/2;xx=X.value(gu(P,vm),vm)[0]
      if xx>x:vlo=vm
      else:vhi=vm
     specs.append(((vlo+vhi)/2,'trace',f'labelled penetration {x:g} in',False))
   if sc.get('intercept'):specs.append((P[0,1],'feature','intercept; terminal ink merges with load axis',True))
  else:
   specs=[(P[0,1],'feature','first',True),(P[-1,1],'feature','peak; maximum load of whole trace',True),(P[-1,1],'feature','last',True)]
   xmin,xmax=sorted([X.value(*P[0])[0],X.value(*P[-1])[0]])
   start=math.ceil((xmin-0.02)*4)/4
   for x in np.arange(start,xmax+.001,.25):
    if x<-.02:continue
    vlo,vhi=P[-1,1],P[0,1]
    for _ in range(30):
     vm=(vlo+vhi)/2;xx=X.value(gu(P,vm),vm)[0]
     if xx>x:vlo=vm
     else:vhi=vm
    specs.append(((vlo+vhi)/2,'trace',f'target penetration {x:g} in',False))
   for v in sc.get('feature_vs',[]):specs.append((v,'feature','knee; local turn or recorder step',False))
  specs.sort(key=lambda a:-a[0])
  for seq,(v,kind,note,endpoint) in enumerate(specs,1):
   u,vv=center(v,endpoint);b=width(u,vv);x=X.value(u,vv)[0]
   ov=overlap(f,s,x)
   if ov:b=max(b,7 if f=='F2-32' else 9);note+='; '+ov
   if f=='F2-32' and s=='lpt52' and endpoint and vv<2300:
    b=max(b,12);note+='; terminal dotted ink merges with fit and grid; endpoint uncertain'
   if f=='F2-32' and s=='lpt93' and endpoint and vv>3680:
    note+='; cap extends slightly beyond zero-penetration line'
   # Recenter faint-edge/gap candidates on ink within 3 px, without changing branch.
   ui,vi=round(u),round(vv)
   yy,xx=np.mgrid[vi-3:vi+4,ui-3:ui+4];sub=g[vi-3:vi+4,ui-3:ui+4];dd=np.hypot(xx-u,yy-vv)
   if np.any(sub<180) and np.min(dd[sub<180])>2:
    score=np.where(sub<180,dd,99);a,z=np.unravel_index(score.argmin(),score.shape);u=float(xx[a,z]);vv=float(yy[a,z]);note+='; snapped faint edge to nearby ink'
   if not endpoint and abs(vv-v)>.6:note+=f'; moved {vv-v:+.1f} px in v to nearby own ink (dash/dot or scan gap)'
   if any(abs(vv-(l['v_at_u0']+l['slope_dv_du']*u))<8 for l in c['horizontal_lines']):
    b=max(b,5);note+='; grid crossing, thickness from adjacent clean stroke'
   rows.append(dict(zip(COLS,[f,1,s,kind,seq,round(u,2),round(vv,2),b,b,'',note])))
  if sc.get('straight'):
   u,v=sc['label'];rows.append(dict(zip(COLS,[f,1,s,'feature',len(specs)+1,u,v,5,5,'','label: '+sc['text']])))
 savecsv(d/'points-p1.csv',rows)
 native=[r.copy() for r in rows];ca.piecewise_rows(c,X,Y,native)
 for r in native:r['x_unit']='inch';r['y_unit']='lb'
 savecsv(d/'points-p1-native.csv',native)
 # Save per-series affine versus local-grid sensitivity.
 sens=[]
 for s in fc['curves']:
  rs=[r for r in native if r['series_id']==s and not r['note'].startswith('label:')]
  sens.append({'series_id':s,'max_abs_x_affine_minus_piecewise_in':max(abs(np.dot(c['ax'],[r['pixel_u'],r['pixel_v'],1])-r['x_native']) for r in rs),'max_abs_y_affine_minus_piecewise_lb':max(abs(np.dot(c['ay'],[r['pixel_u'],r['pixel_v'],1])-r['y_native']) for r in rs)})
 savecsv(d/'calibration-sensitivity.csv',sens)
 print(f, {s:{k:sum(r['series_id']==s and r['point_kind']==k for r in rows) for k in ['trace','feature','marker']} for s in fc['curves']})
