import sys,json,csv
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'tools'); import calibrate_axes as ca
# frame estimates left top,right top,right bottom,left bottom
spec={3:([(558,830),(2520,843),(2510,3927),(549,3916)],list(range(0,15,2)),list(range(7,19))),4:([(610,1103),(2568,1118),(2554,3918),(593,3905)],list(range(0,15,2)),list(range(0,11))),5:([(649,880),(2784,850),(2839,3970),(703,4001)],list(range(0,13,2)),list(range(5,41,5))),6:([(631,835),(2510,787),(2605,3982),(730,4034)],list(range(0,15,2)),list(range(5,30,2))),7:([(489,853),(2738,851),(2752,3938),(507,3938)],list(range(0,17,2)),list(range(0,12)))}
def ridge(g,t,expected,vertical,win=9):
 p=np.arange(round(expected)-win,round(expected)+win+1); a=g[p,round(t)] if not vertical else g[round(t),p]; mask=a<160
 if not mask.any(): return None
 # longest contiguous ink run, favour close to expected
 runs=np.split(np.where(mask)[0],np.where(np.diff(np.where(mask)[0])>1)[0]+1); r=min(runs,key=lambda r:abs(p[r].mean()-expected)-len(r)*.1)
 return float(np.average(p[r],weights=255-a[r]))
def fit(P):
 P=np.array(P); c=np.polyfit(P[:,0],P[:,1],1); r=P[:,1]-np.polyval(c,P[:,0]); keep=abs(r-np.median(r))<max(2,3*np.median(abs(r-np.median(r))))
 c=np.polyfit(P[keep,0],P[keep,1],1); return c,P[keep],float(np.sqrt(np.mean((P[keep,1]-np.polyval(c,P[keep,0]))**2)))
for j,(corners,xs,ys) in spec.items():
 im=Image.open(f'packet/p{j+106:04}.png').convert('L'); g=np.array(im); tl,tr,br,bl=map(np.array,corners)
 frames={}
 for name,a,b,vertical in [('left',tl,bl,True),('right',tr,br,True),('top',tl,tr,False),('bottom',bl,br,False)]:
  ti,pi=(1,0) if vertical else (0,1); P=[]
  for t in np.linspace(a[ti]+40,b[ti]-40,100):
   e=a[pi]+(b[pi]-a[pi])*(t-a[ti])/(b[ti]-a[ti]); p=ridge(g,t,e,vertical,12)
   if p is not None:P.append((t,p))
  frames[name]=fit(P)
 anchors=[]; vl=[];hl=[]; measurement=[]; checks=[]
 for axis,vals in [('x',xs),('y',ys)]:
  for value in vals:
   f=(value-vals[0])/(vals[-1]-vals[0]); isframe=value in (vals[0],vals[-1])
   if axis=='x':
    if isframe: c,P,rms=frames['left' if f==0 else 'right']; vertical=True
    else:
     v=float(np.polyval(frames['bottom'][0],bl[0]+f*(br[0]-bl[0]))); u=bl[0]+f*(br[0]-bl[0]); P=[]
     for t in np.arange(v-29,v-9,1):
      p=ridge(g,t,u,True,14)
      if p is not None:P.append((t,p))
     c,P,rms=fit(P);vertical=True
    line={'x_value':value,'slope_du_dv':float(c[0]),'u_at_v0':float(c[1]),'source':'measured frame with printed label' if isframe else 'measured tick stub','samples':P.tolist()};vl.append(line)
   else:
    if isframe:c,P,rms=frames['bottom' if f==0 else 'top']; vertical=False
    else:
     v=bl[1]+f*(tl[1]-bl[1]); u=np.polyval(frames['left'][0],v);P=[]
     for t in np.arange(u+10,u+30,1):
      p=ridge(g,t,v,False,14)
      if p is not None:P.append((t,p))
     c,P,rms=fit(P);vertical=False
    line={'y_value':value,'slope_dv_du':float(c[0]),'v_at_u0':float(c[1]),'source':'measured frame with printed label' if isframe else 'measured tick stub','samples':P.tolist()};hl.append(line)
   for t,p in P:
    anchors.append({'x_value':value if axis=='x' else '', 'y_value':value if axis=='y' else '', 'u':p if vertical else t,'v':t if vertical else p,'x_source':line['source'] if axis=='x' else '', 'y_source':line['source'] if axis=='y' else ''})
   measurement.append({'axis':axis,'value':value,'slope':float(c[0]),'intercept':float(c[1]),'rms_px':rms,'n':len(P)})
 out=Path(f'out/FB-{j}/cal-p1');out.mkdir(parents=True,exist_ok=True)
 with (out/'anchors.csv').open('w',newline='') as fp:
  w=csv.DictWriter(fp,fieldnames=list(anchors[0]));w.writeheader();w.writerows(anchors)
 coeff={};res={}
 for axis in ['x','y']:
  A=[a for a in anchors if a[axis+'_value']!=''];U=np.array([[a['u'],a['v'],1] for a in A]);V=np.array([a[axis+'_value'] for a in A]);c=np.linalg.lstsq(U,V,rcond=None)[0];r=V-U@c;coeff[axis]=c.tolist();res['rms_residual_'+axis]=float(np.sqrt(np.mean(r*r)));res['max_residual_'+axis]=float(abs(r).max())
 cal={'image':f'packet/p{j+106:04}.png','box':[int(tl[0]-20),int(min(tl[1],tr[1])-20),int(br[0]+20),int(max(bl[1],br[1])+20)],'model':'independently measured tick stubs and labelled frame lines; each line fitted with own tilt','ax':coeff['x'],'ay':coeff['y'],**res,'x_per_px':float(np.linalg.norm(coeff['x'][:2])),'y_per_px':float(np.linalg.norm(coeff['y'][:2])),'n_anchors':len(anchors),'vertical_lines':vl,'horizontal_lines':hl}
 (out/'calibration.json').write_text(json.dumps(cal,indent=2))
 with (out/'tick-fits.csv').open('w',newline='') as fp:
  w=csv.DictWriter(fp,fieldnames=list(measurement[0]));w.writeheader();w.writerows(measurement)
 print(j,res,[(m['axis'],m['value'],round(m['slope'],4)) for m in measurement])
 # all labels and tick stubs for eye checking
 canvas=Image.new('RGB',(1100,max(len(xs),len(ys))*150),'white');d=ImageDraw.Draw(canvas)
 for axis,lines in [('x',vl),('y',hl)]:
  for i,l in enumerate(lines):
   val=l[axis+'_value'];x0=0 if axis=='x' else 550
   if axis=='x':v=bl[1]+(br[1]-bl[1])*(val-xs[0])/(xs[-1]-xs[0]);u=np.polyval([l['slope_du_dv'],l['u_at_v0']],v);box=(int(u-60),int(v-45),int(u+65),int(v+90))
   else:v=bl[1]+(tl[1]-bl[1])*(val-ys[0])/(ys[-1]-ys[0]);u=np.polyval(frames['left'][0],v);v=np.polyval([l['slope_dv_du'],l['v_at_u0']],u);box=(int(u-110),int(v-45),int(u+55),int(v+45))
   cr=im.crop(box).convert('RGB');canvas.paste(cr,(x0+180,i*150));d.text((x0+5,i*150+15),f'{axis}={val} box{box}',fill='blue')
 canvas.save(out/'labels-all.png')
