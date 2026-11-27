from read_batch import *
TABLE={'FA-2':(860,2270,1485,3670),'FA-6':(1050,2260,1685,3650),'FA-18':(880,2100,1520,3610),'FA-22':(770,2220,1370,3760),'FA-26':(690,2540,1210,3780),'FA-38':(1340,1250,1940,2740),'FA-46':(915,2370,1520,3710)}
def robust_line(pts):
 t,p=np.array(pts).T
 best=None
 for i in range(len(t)):
  for j in range(i+1,len(t)):
   if abs(t[j]-t[i])<300:continue
   s=(p[j]-p[i])/(t[j]-t[i]);b=p[i]-s*t[i]
   keep=abs(p-(s*t+b))<2
   score=keep.sum()
   if best is None or score>best[0]:best=(score,keep)
 keep=best[1]
 s,b=np.polyfit(t[keep],p[keep],1)
 return s,b,[(float(a),float(c)) for a,c in zip(t[keep],p[keep])]
for fid,(page,box) in CONFIG.items():
 d=ROOT/'out'/fid/'cal-p1';orig=json.loads((d/'detection-original.json').read_text());g=np.array(Image.open(ROOT/'packet'/f'{page}.png').convert('L'))
 H={l['x_value']:(l['slope_dv_du'],l['v_at_u0']) for l in orig['horizontal_lines']}
 V={l['y_value']:(l['slope_du_dv'],l['u_at_v0']) for l in orig['vertical_lines']}
 # Fix the grain-axis prediction to definite labelled lines 1, 5 and 0.02.
 h1=np.array(H[1]);h5=np.array(H[5]);h02=np.array(H[.02]);new=[];lines=[]
 tab=TABLE[fid]
 for axis,vals in [('x',[.02,.05,.1,.2,.5,1,1.5,2,3,4,5,9]),('y',range(0,101,10))]:
  for val in vals:
   if axis=='x':
    a,b=(h1,h02) if val<1 else (h1,h5)
    va,vb=(1,.02) if val<1 else (1,5)
    seed=a+(b-a)*(np.log10(val)-np.log10(va))/(np.log10(vb)-np.log10(va))
    ts=np.arange(box[0]+45,box[2]-40,31)
   else:
    # Only the 0 and 100 percent *labelled* frames set the initial prediction.
    seed=np.array(V[0])+(np.array(V[100])-np.array(V[0]))*val/100
    # Their detected slopes can be corrupted where curves meet the frame; use reliable 10/30 slopes.
    slope=np.mean([V[10][0],V[30][0]])
    ref=box[1]+90; seed=np.array([slope,seed[1]+seed[0]*ref-slope*ref])
    ts=np.arange(box[1]+35,box[3]-40,37)
   pts=[]
   for t in ts:
    pred=seed[0]*t+seed[1]
    u,v=(t,pred) if axis=='x' else (pred,t)
    if tab[0]-15<u<tab[2]+15 and tab[1]-15<v<tab[3]+15:continue
    # Long-stretch profile isolates grid ink from a crossing curve. Wider labels are never anchors.
    ps=np.arange(round(pred)-18,round(pred)+19)
    along=np.arange(t-12,t+13)
    if axis=='x': profile=(g[ps[:,None],along[None,:].astype(int)]<150).mean(axis=1)
    else: profile=(g[along[:,None].astype(int),ps[None,:]]<150).mean(axis=0)
    ix=np.where(profile>.75)[0]
    runs=[]
    for group in np.split(ix,np.where(np.diff(ix)>1)[0]+1):
     if len(group)>=3:runs.append((len(group),float(np.mean(ps[group])),group))
    if not runs:continue
    # The labelled major grid is thicker than the intervening minor lines.
    width,center,group=max(runs,key=lambda r:(r[0],-abs(r[1]-pred)))
    if width>14:continue
    pts.append((t,center))
   s,b,good=robust_line(pts)
   lines.append((axis,val,s,b))
   for t,p in good:
    u,v=(t,p) if axis=='x' else(p,t)
    new.append(dict(x_value=val if axis=='x' else '',y_value=val if axis=='y' else '',u=round(u,3),v=round(v,3),x_source='measured labelled major grid ink; label checked' if axis=='x' else '',y_source='measured labelled percent grid ink; label checked' if axis=='y' else ''))
 xl={val:(s,b) for axis,val,s,b in lines if axis=='x'};yl={val:(s,b) for axis,val,s,b in lines if axis=='y'}
 aa=[]
 for x,(sx,bx) in xl.items():
  for y,(sy,by) in yl.items():
   u,v=ca.intersect((x,sx,bx,'',[]),(y,sy,by,'',[]));aa.append(dict(x_value=x,y_value=y,u=u,v=v))
 ax,ay,rx,ry,mx,my=ca.fit_affine(aa,'log10','linear')
 cal=orig.copy();cal.update(ax=ax,ay=ay,x_per_px=float(np.hypot(*ax[:2])),y_per_px=float(np.hypot(*ay[:2])),rms_residual_x=rx,rms_residual_y=ry,max_residual_x=mx,max_residual_y=my,n_anchors=len(new),refinement='Label-supported major lines refitted with table excluded; measured lines and checks are piecewise-knots.json; detection-original.json preserves initial diagnostic')
 cal['horizontal_lines']=[dict(x_value=val,slope_dv_du=s,v_at_u0=b,source='measured labelled ink',samples=[[r['u'],r['v']] for r in new if r['x_value']==val]) for val,(s,b) in xl.items()]
 cal['vertical_lines']=[dict(y_value=val,slope_du_dv=s,u_at_v0=b,source='measured labelled ink',samples=[[r['v'],r['u']] for r in new if r['y_value']==val]) for val,(s,b) in yl.items()]
 (d/'calibration.json').write_text(json.dumps(cal,indent=2))
 with (d/'anchors.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(new[0]));w.writeheader();w.writerows(new)
 C,X,Y=ca.piecewise_maps(d,ROOT/'packet'/f'{page}.png');(d/'piecewise-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 print(fid,'rms',round(rx,5),round(ry,4),'max',round(mx,5),round(my,4),'X',[(k['value'],k.get('reason')) for k in X.rejected],'Y',[(k['value'],k.get('reason')) for k in Y.rejected])
 print('x labels at right',[(val,round(s*box[2]+b,1)) for val,(s,b) in xl.items()]); print('y labels at coarse end',[(val,round(s*box[1]+b,1)) for val,(s,b) in yl.items()])
