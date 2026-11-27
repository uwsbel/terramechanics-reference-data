import json,sys,csv,numpy as np
from pathlib import Path
from PIL import Image
sys.path.insert(0,'tools');import calibrate_axes as ca
cfg=json.loads(Path('out/config.json').read_text())
ca.INK_HALF_WIDTH_PX=14
for fig,c in cfg.items():
 d=Path('out')/fig/'cal-p1'; cal=json.loads((d/'calibration-initial.json').read_text())
 gray=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'),dtype=float)
 out=[]
 for orientation,key,skey,ikey in [('v','vertical_lines','slope_du_dv','u_at_v0'),('h','horizontal_lines','slope_dv_du','v_at_u0')]:
  for l in cal[key]:
   ca.INK_HALF_WIDTH_PX=14 if orientation=='h' and l['y_value']==c['yr'][1] else 6
   slope,inter=l[skey],l[ikey]; positions=np.linspace(c['box'][1]+20,c['box'][3]-20,101) if orientation=='v' else np.linspace(c['box'][0]+20,c['box'][2]-20,101)
   pts=[]
   # ink window wide enough to contain white on both sides of the thick bottom frame
   for t in positions:
    p=np.array([inter+slope*t,t]) if orientation=='v' else np.array([t,inter+slope*t])
    es=np.array([1.,0.]) if orientation=='v' else np.array([0.,1.]); et=np.array([0.,1.]) if orientation=='v' else np.array([1.,0.])
    off=ca.ink_offset(gray,p,es,et)
    if off is not None: pts.append((t,inter+slope*t+off))
   T,S=np.array(pts).T
   for rep in range(3):
    sl,iv=np.polyfit(T,S,1);res=S-(sl*T+iv);keep=np.abs(res)<=max(1.5,3*1.4826*np.median(np.abs(res-np.median(res))));T,S=T[keep],S[keep]
   l[skey],l[ikey]=float(sl),float(iv);l['samples']=list(map(list,zip(T.tolist(),S.tolist())));l['source']='detected; refined on page ink; 6 px half-window (14 px for thick bottom frame)'
   out.append(dict(axis=orientation,value=l.get('x_value',l.get('y_value')),n=len(T),rms_px=float(np.sqrt(np.mean((S-(sl*T+iv))**2)))))
 vl=[(l['x_value'],l['slope_du_dv'],l['u_at_v0'],l['source'],l['samples']) for l in cal['vertical_lines']]; hl=[(l['y_value'],l['slope_dv_du'],l['v_at_u0'],l['source'],l['samples']) for l in cal['horizontal_lines']]
 anchors=[]
 for h in hl:
  for v in vl:
   u,vv=ca.intersect(h,v);anchors.append(dict(x_value=v[0],y_value=h[0],u=round(u,3),v=round(vv,3),x_source=v[3],y_source=h[3]))
 ax,ay,rx,ry,mx,my=ca.fit_affine(anchors,'linear','reciprocal');cal.update(ax=ax,ay=ay,rms_residual_x=rx,rms_residual_y=ry,max_residual_x=mx,max_residual_y=my,x_per_px=float(np.hypot(*ax[:2])),y_per_px=float(np.hypot(*ay[:2])))
 cal['ink_check_half_window_px']=14
 with (d/'anchors.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(anchors[0]));w.writeheader();w.writerows(anchors)
 (d/'calibration.json').write_text(json.dumps(cal,indent=2));(d/'refinement.json').write_text(json.dumps(out,indent=2))
 from reading_lib import load_maps
 cal,X,Y=load_maps(fig,c);(d/'verified-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 print(fig,'reject',[(k['value'],k['reason']) for k in X.rejected+Y.rejected],'RMS/max px',rx/cal['x_per_px'],mx/cal['x_per_px'],ry/cal['y_per_px'],my/cal['y_per_px'])

