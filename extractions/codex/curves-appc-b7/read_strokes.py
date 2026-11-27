import sys,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'tools');import calibrate_axes as c
# Stroke seeds read from page, independent of box numbers.
seed={'FC-8':[(765,3310),(2060,2285)],'FC-9A':[(675,3530),(1640,2250)],'FC-9B':[(687,3582),(1780,2405)],'FC-9C':[(590,3510),(1680,2255)],'FC-10A':[(670,3560),(1830,2420)]}
allrec={}
for fig,page,box in json.loads(Path('out/config.json').read_text()):
 d=Path('out')/fig;im=Image.open('packet/'+page).convert('RGB');g=np.asarray(im.convert('L'));cal,X,Y=c.piecewise_maps(d/'cal-p1','packet/'+page)
 (u0,v0),(u1,v1)=seed[fig];m=(v1-v0)/(u1-u0);b=v0-m*u0
 # observe line stroke in many columns, reject crossings with thick vertical/horizontal grid ink
 obs=[]
 for u in range(u0,u1,7):
  pred=m*u+b;lo=int(pred)-20; hi=int(pred)+21
  idx=np.where(g[lo:hi,u]<128)[0];runs=[]
  for a in np.split(idx,np.where(np.diff(idx)>1)[0]+1):
   if len(a)>0:runs.append((len(a),float(np.mean(a))+lo))
  good=[r for r in runs if 7<=r[0]<=19 and abs(r[1]-pred)<12]
  if good:
   n,v=min(good,key=lambda r:abs(r[1]-pred));obs.append((u,v,n))
 ar=np.array(obs);m,b=np.polyfit(ar[:,0],ar[:,1],1);res=ar[:,1]-(m*ar[:,0]+b);keep=abs(res)<3
 m,b=np.polyfit(ar[keep,0],ar[keep,1],1)
 print(fig,'ink fit v=',m,'u +',b,'scatter',np.std(ar[keep,1]-(m*ar[keep,0]+b)))
 # every 500 normal stress through the ink-fit endpoint range
 endrough=json.loads(Path('out/rough-ends.json').read_text())[fig][1];endx=X.value(*endrough)[0]
 records=[]
 for x in np.arange(500,endx,500):
  left=box[0];right=box[2]
  for it in range(45):
   uu=(left+right)/2;vv=m*uu+b
   if X.value(uu,vv)[0]<x:left=uu
   else:right=uu
  u=(left+right)/2;pred=m*u+b;col=int(round(u));lo=int(pred)-20;hi=int(pred)+21
  idx=np.where(g[lo:hi,col]<128)[0];runs=[a for a in np.split(idx,np.where(np.diff(idx)>1)[0]+1) if len(a)]
  near=min(runs,key=lambda a:abs(np.mean(a)+lo-pred)) if runs else []
  v=float(np.mean(near)+lo) if len(near) else pred
  records.append(dict(x_target=float(x),u=round(u,3),v=v,width=len(near),inkfit_v=pred))
 allrec[fig]={'m':m,'b':b,'samples':records}
 canvas=Image.new('RGB',(960,250*((len(records)+3)//4)),'white');dr=ImageDraw.Draw(canvas)
 for i,r in enumerate(records):
  u,v=int(round(r['u'])),int(round(r['v']));cr=im.crop((u-35,v-35,u+35,v+35)).resize((210,210));dd=ImageDraw.Draw(cr)
  for uu in range((u-35+9)//10*10,u+35,10):
   xx=(uu-u+35)*3;dd.line((xx,0,xx,210),fill=(185,220,245));dd.text((xx,0),str(uu),fill='blue')
  for vv in range((v-35+9)//10*10,v+35,10):
   yy=(vv-v+35)*3;dd.line((0,yy,210,yy),fill=(185,220,245));dd.text((0,yy),str(vv),fill='blue')
  dd.ellipse((100,100,110,110),outline='red',width=1)
  xx=i%4*240;yy=i//4*250;canvas.paste(cr,(xx,yy+25));dr.text((xx,yy),f"x={r['x_target']:g}; {r['u']:.1f},{r['v']:.1f}; w={r['width']}",fill='black')
 canvas.save(d/'trace-inspect.png')
Path('out/stroke-readings.json').write_text(json.dumps(allrec,indent=2))
