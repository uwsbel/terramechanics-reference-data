import json,sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca
import plot_grid as pg
TR={
 'FC-10B':('p0143',[(574,3715),(1834,2525)]),
 'FC-10C':('p0144',[(486,3706),(1753,2511)]),
 'FC-11A':('p0145',[(707,3679),(2052,2719)]),
 'FC-11B':('p0146',[(654,3485),(2036,2448)]),
 'FC-11C':('p0149',[(635,3602),(2015,2534)])}
ALL={}
for fig,(page,ends) in TR.items():
 im=Image.open(f'packet/{page}.png').convert('RGB');g=np.asarray(im.convert('L'),dtype=float)
 cal,X,Y=ca.piecewise_maps(Path('out')/fig/'cal-p1',f'packet/{page}.png')
 m=(ends[1][1]-ends[0][1])/(ends[1][0]-ends[0][0]);b=ends[0][1]-m*ends[0][0]
 # Find ink near the independent visual line estimate at columns away from frames.
 xy=[]
 for u in range(ends[0][0]+30,ends[1][0]-20,10):
  v0=int(round(m*u+b)); vv=np.arange(v0-18,v0+19)
  # thickness-weighted centre of the local run nearest the visual estimate
  dark=g[vv,u]<150;idx=np.flatnonzero(dark)
  runs=np.split(idx,np.flatnonzero(np.diff(idx)>1)+1)
  runs=[r for r in runs if len(r)>=3 and len(r)<=17]
  if runs:
   r=min(runs,key=lambda r:abs(vv[r].mean()-v0));xy.append((u,vv[r].mean()))
 p=np.array(xy);coef=np.polyfit(p[:,0],p[:,1],1);res=p[:,1]-np.polyval(coef,p[:,0]);keep=np.abs(res)<4
 m,b=np.polyfit(p[keep,0],p[keep,1],1)
 # x inversion at the ink line. The line position is refined locally later.
 def inv(x):
  lo,hi=ends[0][0]-10,ends[1][0]+10
  for _ in range(45):
   mid=(lo+hi)/2;vv=m*mid+b
   if X.value(mid,vv)[0]<x:lo=mid
   else:hi=mid
  return (lo+hi)/2
 records=[]
 for target in [0]+list(range(500,5000,500)):
  u=inv(target);v=m*u+b
  if u>ends[1][0]+5:continue
  e_s=np.array([-m,1.])/np.hypot(m,1);e_t=np.array([1.,m])/np.hypot(m,1)
  off=ca.ink_offset(g,np.array([u,v]),e_s,e_t)
  if off is not None and abs(off)<=5:
   u,v=np.array([u,v])+off*e_s
  records.append({'target':target,'u':float(u),'v':float(v),'ink_offset':off})
 # The right endpoint is a manual visual check, not the fitted value.
 records.append({'target':'right-end','u':ends[1][0],'v':ends[1][1]})
 ALL[fig]={'page':page,'ink_fit':[float(m),float(b)],'samples':records}
 sheet=Image.new('RGB',(1000,((len(records)+3)//4)*290),'white');dr=ImageDraw.Draw(sheet)
 for i,r in enumerate(records):
  u,v=r['u'],r['v'];box=[round(u)-40,round(v)-40,round(u)+40,round(v)+40]
  dest=Path('out')/fig/f'trace-crop-{i+1}.png'
  pg.cmd_crop(SimpleNamespace(image=f'packet/{page}.png',box=box,out=str(dest),zoom=3,step=25))
  crop=Image.open(dest);cd=ImageDraw.Draw(crop);xx=(u-box[0])*3;yy=(v-box[1])*3
  cd.ellipse((xx-3,yy-3,xx+3,yy+3),outline='green',width=1)
  x=i%4*250;y=i//4*290;sheet.paste(crop,(x,y+35));dr.text((x,y),f'{r["target"]}: {u:.2f},{v:.2f}',fill='black')
 sheet.save(Path('out')/fig/'trace-sheet.png')
 print(fig,'pixel ink fit',m,b)
Path('out/trace-candidates.json').write_text(json.dumps(ALL,indent=2))
