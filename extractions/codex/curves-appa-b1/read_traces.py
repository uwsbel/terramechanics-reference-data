import json,sys,csv,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'tools')
import calibrate_axes as ca
cfg=json.loads(Path('out/config.json').read_text())
guides={
'FA-4':[[835,2147],[1100,2010],[1400,1870],[1600,1770],[1760,1715],[2000,1630],[2388,1495]],
'FA-8':[[863,2064],[1100,2020],[1300,1957],[1500,1890],[1800,1800],[2100,1710],[2400,1633]],
'FA-20':[[812,2507],[1100,2350],[1400,2180],[1600,2080],[1800,2000],[2048,1892],[2100,1870],[2357,1765]],
'FA-24':[[785,2145],[1000,2078],[1200,1994],[1400,1882],[1700,1722],[2000,1555],[2200,1440],[2333,1385]],
'FA-28':[[771,3225],[1000,3145],[1200,3040],[1300,2960],[1400,2845],[1500,2720],[1600,2615],[1700,2530],[1800,2470],[2000,2380],[2200,2320],[2309,2294]],
'FA-48':[[796,2541],[1000,2430],[1200,2305],[1400,2160],[1600,2012],[1700,1937],[1800,1870],[2000,1740],[2100,1672],[2200,1625],[2340,1565]]}
Path('out/guides.json').write_text(json.dumps(guides,indent=2))

def runs(a):
 ix=np.flatnonzero(a)
 if not len(ix):return []
 return [(z[0],z[-1]) for z in np.split(ix,np.where(np.diff(ix)>1)[0]+1)]

def measure(g,u,expected):
 # Neighbour columns isolate the curve from thin grid lines and frame. Guides were read by eye.
 obs=[]
 for uu in range(round(u)-20,round(u)+21):
  lo=round(expected)-45; hi=round(expected)+46
  rr=[(lo+(a+b)/2,b-a+1) for a,b in runs(g[lo:hi,uu]<160) if 3<=b-a+1<=25]
  if rr:
   vv,w=min(rr,key=lambda z:abs(z[0]-expected));
   if abs(vv-expected)<32:obs.append([uu,vv,w])
 if len(obs)<5:raise ValueError((u,expected,obs))
 ar=np.array(obs); co=np.polyfit(ar[:,0]-u,ar[:,1],1);pred=co[1]
 # Robust local line fit removes horizontal grid runs and small broken edges.
 for _ in range(3):
  res=ar[:,1]-np.polyval(co,ar[:,0]-u);keep=np.abs(res)<max(2.5,3*np.median(abs(res-np.median(res))))
  co=np.polyfit(ar[keep,0]-u,ar[keep,1],1)
 pred=co[1];typ=float(np.median(ar[keep,2]))
 lo=round(pred)-25;hi=round(pred)+26
 rr=[(lo+(a+b)/2,b-a+1) for a,b in runs(g[lo:hi,round(u)]<160)]
 center,w=min(rr,key=lambda z:abs(z[0]-pred))
 note=''
 if w<=typ+3 and abs(center-pred)<4:
  v=center;thick=w
 else:
  v=pred;thick=typ;note='Curve/grid or frame intersection; centre and line thickness read from adjoining curve ink.'
 if g[round(v),round(u)]>=160:
  # Return surviving ink only, flag scan defect for explicit review.
  candidates=[(lo+(a+b)/2,b-a+1) for a,b in runs(g[lo:hi,round(u)]<160) if abs(lo+(a+b)/2-pred)<12]
  if not candidates:raise ValueError(('no ink',u,pred))
  v,thick=min(candidates,key=lambda z:abs(z[0]-pred));note+=' Scan defect: sample on surviving curve ink.'
 return round(v,2), max(1.5,round(thick/2,2)),note

cols=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
for f,guide in guides.items():
 c=cfg[f];root=Path('out')/f;im=Image.open('packet/'+c['page']+'.png').convert('RGB');g=np.array(im.convert('L'))
 cal,X,Y=ca.piecewise_maps(root/'cal-p1','packet/'+c['page']+'.png');rows=[]
 for i,target in enumerate(np.arange(0,1.001,.05)):
  v=np.interp(guide[0][0]+target*(guide[-1][0]-guide[0][0]),np.array(guide)[:,0],np.array(guide)[:,1]);u=0
  for _ in range(4):
   l,r=600.,2500.
   for j in range(35):
    m=(l+r)/2
    if X.value(m,v)[0]<target:l=m
    else:r=m
   u=(l+r)/2;expected=np.interp(u,np.array(guide)[:,0],np.array(guide)[:,1]);v,b,note=measure(g,u,expected)
  if f=='FA-28' and i==0:
   u=771.;v=3225.;b=2.;note='First visible curve ink is detached from the left frame; no sample invented at Dr=0.'
  if i in (0,20) and not(f=='FA-28' and i==0):note+=' Endpoint merges with frame; curve centre followed into the junction.'
  rows.append(dict(zip(cols,[f,1,'curve','trace',i+1,round(u,2),v,b,b,'',note.strip()])))
 with (root/'points-p1.csv').open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=cols);w.writeheader();w.writerows(rows)
 # Contact sheet: every sample, raw page ink with a hollow cross and page coordinates.
 sheet=Image.new('RGB',(4*260,6*205),'white');d=ImageDraw.Draw(sheet)
 for j,r in enumerate(rows):
  u,v=float(r['pixel_u']),float(r['pixel_v']);b=(round(u)-40,round(v)-26,round(u)+40,round(v)+26)
  tile=im.crop(b).resize((240,156),Image.Resampling.NEAREST);td=ImageDraw.Draw(tile);x=(u-b[0])*3;y=(v-b[1])*3
  for p,q in [((x-21,y),(x-7,y)),((x+7,y),(x+21,y)),((x,y-21),(x,y-7)),((x,y+7),(x,y+21))]:td.line([p,q],fill='red',width=1)
  xx=(j%4)*260;yy=(j//4)*205;sheet.paste(tile,(xx+5,yy+30));d.text((xx+5,yy+3),f"{j+1}: Dr {j*.05:.2f}  ({u:.1f},{v:.1f})",fill='black')
 sheet.save(root/'samples-check.png')
 print(f,[(r['sequence'],r['pixel_u'],r['pixel_v'],r['v_bound_px']) for r in rows])
