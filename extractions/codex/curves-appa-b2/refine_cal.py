from read_batch import *
for fid,(page,box) in CONFIG.items():
 d=ROOT/'out'/fid/'cal-p1'; cal=json.loads((d/'calibration.json').read_text())
 if not (d/'detection-original.json').exists():
  (d/'detection-original.json').write_text(json.dumps(cal,indent=2))
 g=np.asarray(Image.open(ROOT/'packet'/f'{page}.png').convert('L'))
 # First report the independent detector's ink checks, without reading other extractions.
 C,X,Y=ca.piecewise_maps(d,ROOT/'packet'/f'{page}.png')
 print(fid,'X verified',[k['value'] for k in X.knots],'rejected',[(k['value'],k['reason']) for k in X.rejected], 'Y verified',[k['value'] for k in Y.knots],'rejected',[(k['value'],k['reason']) for k in Y.rejected])
 (d/'initial-ink-check.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 # Recover printed lines from our own strongest label-supported neighbours.
 # The 0.2 mm detector on FA-6/18 was on a minor line. Exclude it from prediction.
 X.knots=[k for k in X.knots if not(fid in ('FA-6','FA-18') and k['value']==.2)]
 new=[]; rec=[]
 for axis,K,vals in [('x',X,[.02,.05,.1,.2,.5,1,1.5,2,3,4,5,9]),('y',Y,list(range(0,101,10)))]:
  ts=[t for k in K.knots for t in k['t']]
  for val in vals:
   pts,rms=ca.recover_line(g,K,val,(min(ts),max(ts)),search_px=20,step=45)
   if len(pts)<3: raise RuntimeError((fid,axis,val,'missing'))
   for u,v in pts:
    new.append(dict(x_value=val if axis=='x' else '',y_value=val if axis=='y' else '',u=round(u,3),v=round(v,3),x_source='recovered from labelled grid ink' if axis=='x' else '',y_source='recovered from labelled grid ink' if axis=='y' else ''))
   rec.append(dict(axis=axis,value=val,n=len(pts),rms_px=round(rms,3)))
 # Refit affine diagnostics using intersections, keeping independent measured knots for piecewise.
 def line(pts,axis):
  if axis=='x': return np.polyfit([p['u'] for p in pts],[p['v'] for p in pts],1)
  return np.polyfit([p['v'] for p in pts],[p['u'] for p in pts],1)
 xl={val:line([p for p in new if p['x_value']==val],'x') for val in [.02,.05,.1,.2,.5,1,1.5,2,3,4,5,9]}
 yl={val:line([p for p in new if p['y_value']==val],'y') for val in range(0,101,10)}
 anchors=[]
 for xv,(xs,xi) in xl.items():
  for yv,(ys,yi) in yl.items():
   u,v=ca.intersect((xv,xs,xi,'',[]),(yv,ys,yi,'',[]))
   anchors.append(dict(x_value=xv,y_value=yv,u=u,v=v))
 ax,ay,rx,ry,mx,my=ca.fit_affine(anchors,'log10','linear')
 cal.update(ax=ax,ay=ay,x_per_px=float(np.hypot(*ax[:2])),y_per_px=float(np.hypot(*ay[:2])),rms_residual_x=rx,rms_residual_y=ry,max_residual_x=mx,max_residual_y=my,n_anchors=len(new),refinement='Measured labelled lines; original detector preserved in detection-original.json; per-line fits and ink checks in piecewise-knots.json')
 (d/'calibration.json').write_text(json.dumps(cal,indent=2))
 with (d/'anchors.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(new[0])); w.writeheader();w.writerows(new)
 with (d/'recovery.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rec[0]));w.writeheader();w.writerows(rec)
 C,X,Y=ca.piecewise_maps(d,ROOT/'packet'/f'{page}.png')
 (d/'piecewise-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 print('REFINED',fid,'rms',rx,ry,'max',mx,my,'X rejected',[(k['value'],k['reason']) for k in X.rejected],'Y rejected',[(k['value'],k['reason']) for k in Y.rejected])
