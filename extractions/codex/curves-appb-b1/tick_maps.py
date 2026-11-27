import json,csv,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,'tools');import calibrate_axes as ca

def load_maps(d):
 cal=json.loads((d/'calibration.json').read_text());anc=ca.load_anchors(d);x=ca.AxisKnots(anc,'x_value','x_source',cal['ax'][:2]);y=ca.AxisKnots(anc,'y_value','y_source',cal['ay'][:2]);return cal,x,y

def verify(K,g):
 for kn in K.knots:
  if np.ptp(kn['t'])>200:
   ok,err,reason,check=K.check_line(g,kn)
  else:
   ts=np.linspace(min(kn['t'])+2,max(kn['t'])-2,5);offs=[]
   for t in ts:
    p=K.line_s(kn,t)*K.e_s+t*K.e_t;off=ca.ink_offset(g,p,K.e_s,K.e_t)
    if off is not None:offs.append(float(off))
   med=float(np.median(np.abs(offs))) if offs else 99;ok=len(offs)>=2 and med<=2;err=max(.5,float(np.max(np.abs(offs))) if offs else 99);reason='' if ok else 'stub ink check failed';check={'method':'measured short tick: five positions inside stub','found':len(offs),'median_px':med,'offsets_px':offs}
  kn['err']=max(kn['err'],err);kn['check']=check;kn['verified']=ok
  if not ok:raise ValueError((kn['value'],reason))
 return K
if __name__=='__main__':
 for j in range(3,8):
  d=Path(f'out/FB-{j}/cal-p1');cal=json.loads((d/'calibration.json').read_text());g=np.array(Image.open(cal['image']).convert('L'),dtype=float)
  if j==7:
   for val,ur,vr in [(1,(530,537),(3654,3668)),(2,(523,533),(3370,3386)),(3,(522,536),(3094,3108))]:
    l=next(l for l in cal['horizontal_lines'] if l['y_value']==val);P=[]
    for u in range(*ur):
     vv=np.arange(*vr);w=np.clip(180-g[vv,u],0,None)
     if w.sum():P.append((u,float(np.average(vv,weights=w))))
    c=np.polyfit(np.array(P)[:,0],np.array(P)[:,1],1);l['samples']=[list(p) for p in P];l['slope_dv_du']=float(c[0]);l['v_at_u0']=float(c[1]);l['source']='measured tick tip clear of overlapping symbol/line'
  anc=[]
  for axis,key in [('x','vertical_lines'),('y','horizontal_lines')]:
   for l in cal[key]:
    for t,p in l['samples']:anc.append({'x_value':l['x_value'] if axis=='x' else '','y_value':l['y_value'] if axis=='y' else '','u':p if axis=='x' else t,'v':t if axis=='x' else p,'x_source':l['source'] if axis=='x' else '', 'y_source':l['source'] if axis=='y' else ''})
  for axis in ['x','y']:
   A=[a for a in anc if a[axis+'_value']!=''];U=np.array([[a['u'],a['v'],1] for a in A]);V=np.array([a[axis+'_value'] for a in A]);c=np.linalg.lstsq(U,V,rcond=None)[0];r=V-U@c;cal['a'+axis]=c.tolist();cal['rms_residual_'+axis]=float(np.sqrt(np.mean(r*r)));cal['max_residual_'+axis]=float(abs(r).max());cal[axis+'_per_px']=float(np.linalg.norm(c[:2]))
  cal['model']='measured tick stubs and labelled frame lines: each fitted independently with its own tilt; affine diagnostic; native map piecewise between these lines';cal['n_anchors']=len(anc)
  with (d/'anchors.csv').open('w',newline='') as fp:w=csv.DictWriter(fp,fieldnames=list(anc[0]));w.writeheader();w.writerows(anc)
  (d/'calibration.json').write_text(json.dumps(cal,indent=2));_,x,y=load_maps(d);verify(x,g);verify(y,g)
  (d/'verified-knots.json').write_text(json.dumps({'x':x.knots,'y':y.knots,'rejected_x':[],'rejected_y':[]},indent=2)); print(j,len(x.knots),len(y.knots),cal['rms_residual_x'],cal['rms_residual_y'])

