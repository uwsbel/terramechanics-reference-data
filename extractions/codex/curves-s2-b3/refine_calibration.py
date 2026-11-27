import sys,json,csv
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca

def refine(fig,page):
 d=Path('out')/fig/'cal-p1'
 cal=json.loads((d/'calibration.json').read_text())
 if (d/'calibration-detect.json').exists():cal=json.loads((d/'calibration-detect.json').read_text())
 if not (d/'calibration-detect.json').exists():
  (d/'calibration-detect.json').write_text(json.dumps(cal,indent=2))
 g=np.asarray(Image.open('packet/'+page+'.png').convert('L'),float)
 for orient,key,sk,ik in [('v','vertical_lines','slope_du_dv','u_at_v0'),('h','horizontal_lines','slope_dv_du','v_at_u0')]:
  for ln in cal[key]:
   val=ln['x_value' if orient=='v' else 'y_value']
   k,b=ln[sk],ln[ik]
   if fig=='F2-44' and orient=='h' and val==2000:k,b=-.005,1708
   if fig=='F2-42' and orient=='h' and val==400:k,b=.001,2731
   if fig=='F2-44' and orient=='v' and val==3:k,b=.0082,1646
   if fig=='F2-42' and orient=='h' and val==0:k,b=0,3353.5
   if orient=='v':ts=np.arange(1510,3310,50) if fig=='F2-42' else np.arange(1760,3230,50)
   else:ts=np.arange(870,1750,30) if fig=='F2-42' else np.arange(770,2260,35)
   if fig=='F2-42' and orient=='v' and val in (2,3):ts=ts[(ts<2520)|(ts>2910)]
   if fig=='F2-42' and orient=='h' and val==400:ts=ts[ts<1195]
   if fig=='F2-44' and orient=='h' and val==2000:ts=ts[(ts<1040)|(ts>1970)]
   es,et=(np.array([1.,0]),np.array([0.,1])) if orient=='v' else (np.array([0.,1]),np.array([1.,0]))
   pts=[]
   for t in ts:
    p=(b+k*t)*es+t*et
    off=ca.ink_offset(g,p,es,et)
    if off is not None:pts.append([t,b+k*t+off])
   pts=np.array(pts)
   for _ in range(4):
    kk,bb=np.polyfit(pts[:,0],pts[:,1],1)
    res=pts[:,1]-(bb+kk*pts[:,0]); mad=np.median(abs(res-np.median(res)))*1.4826
    pts=pts[abs(res)<max(1.3,3*mad)]
   ln[sk],ln[ik]=float(kk),float(bb)
   ln['source']='detected; refit on visible grid ink; legend and crossing outliers excluded'
   ln['samples']=pts.tolist()
 anchors=[]
 for h in cal['horizontal_lines']:
  for v in cal['vertical_lines']:
   hm,hb=h['slope_dv_du'],h['v_at_u0'];vm,vb=v['slope_du_dv'],v['u_at_v0']
   u=(vb+vm*hb)/(1-vm*hm);vv=hb+hm*u
   anchors.append(dict(x_value=v['x_value'],y_value=h['y_value'],u=u,v=vv,x_source=v['source'],y_source=h['source']))
 ax,ay,rx,ry,mx,my=ca.fit_affine(anchors)
 cal.update(ax=ax,ay=ay,x_per_px=float(np.hypot(*ax[:2])),y_per_px=float(np.hypot(*ay[:2])),rms_residual_x=rx,rms_residual_y=ry,max_residual_x=mx,max_residual_y=my,n_anchors=len(anchors),refinement='Refit visible ink, keeping detected line identities; see samples. Unlabelled frame and 627 tick not knots.')
 (d/'calibration.json').write_text(json.dumps(cal,indent=2))
 # The 400-lb grid exists only to the left of the inset, so do not claim
 # covered intersections as ink anchors. Keep the affine diagnostic above.
 if fig=='F2-42':
  for a in anchors:
   if a['y_value']==400 and a['x_value']>1:a['y_value']='';a['y_source']=''
  h=next(h for h in cal['horizontal_lines'] if h['y_value']==400)
  anchors += [dict(x_value='',y_value=400,u=t,v=s,x_source='',y_source=h['source']) for t,s in h['samples']]
 with (d/'anchors.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=anchors[0]);w.writeheader();w.writerows(anchors)
 _,X,Y=ca.piecewise_maps(d,'packet/'+page+'.png')
 summary=ca.knots_summary(X,Y)
 (d/'verified-knots.json').write_text(json.dumps(summary,indent=2))
 print(fig,'rms',rx,ry,'max',mx,my,'knots',[k['value'] for k in X.knots],[k['value'] for k in Y.knots],'rejected',[(k['value'],k['reason']) for k in X.rejected+Y.rejected])

refine('F2-42','p0102');refine('F2-44','p0104')
