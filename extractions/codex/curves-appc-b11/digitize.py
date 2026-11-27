"""Independent pixel reading: eye-defined curve corridors refined to visible ink.
No values are inferred for dash gaps. Sampling locations move to actual ink.
"""
from pathlib import Path
import sys,json,csv,math
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca
import numpy as np
from PIL import Image,ImageDraw
paths={
20:{'mean':[(798,3260),(960,3212),(1110,3152),(1270,3050),(1418,2915),(1570,2740),(1730,2600),(1890,2495),(2030,2420),(2190,2360),(2323,2324)],'upper':[(798,3178),(966,3100),(1120,3005),(1280,2850),(1425,2720),(1550,2610),(1730,2450),(1890,2350),(2040,2260),(2190,2195),(2335,2170)],'lower':[(805,3385),(976,3320),(1120,3260),(1260,3190),(1425,3070),(1570,2890),(1730,2730),(1890,2605),(2030,2530),(2190,2455),(2340,2395)]},
22:{'mean':[(858,2544),(1168,2360),(1475,2163),(1690,2017),(1950,1840),(2340,1584),(2410,1548)],'upper':[(859,2456),(1168,2265),(1475,2070),(1800,1850),(2110,1650),(2410,1463)],'lower':[(857,2649),(1170,2460),(1475,2265),(1800,2050),(2110,1840),(2410,1650)]},
23:{'rc2':[(926,2257),(1090,2207),(1248,2140),(1400,2070),(1565,1977),(1720,1885),(1880,1790),(2030,1698),(2180,1614),(2340,1530),(2508,1460)],'ps':[(927,2243),(1090,2210),(1248,2170),(1400,2130),(1565,2080),(1720,2025),(1880,1980),(2030,1930),(2180,1885),(2340,1830),(2508,1780),(2645,1748)],'rs':[(790,2544),(950,2460),(1100,2380),(1250,2305),(1410,2230),(1565,2160),(1720,2080),(1880,2020),(2030,1960),(2180,1900),(2340,1830),(2500,1770),(2642,1700)],'rsm-b':[(938,2604),(1100,2517),(1250,2430),(1410,2330),(1570,2230),(1720,2125),(1880,2008),(2030,1902),(2180,1800),(2340,1690),(2504,1605)],'rsm-a':[(938,2714),(1100,2620),(1260,2540),(1410,2450),(1560,2380),(1720,2300),(1880,2220),(2030,2150),(2180,2080),(2340,2010),(2645,1920)],'ss':[(946,3293),(1095,3240),(1255,3172),(1410,3080),(1565,2945),(1725,2760),(1885,2624),(2040,2530),(2195,2455),(2340,2410),(2515,2350)]}}
markers={20:[(826,3230,2,'single'),(826,3281,18,'pair 1 left; circle overlaps solid curve'),(1008,3281,2,'pair 1 right'),(1263,2966,9,'single; circle overlaps vertical grid line'),(1529,2672,2,'single'),(1994,2319,2,'single'),(2342,2320,18,'single; circle overlaps solid curve and vertical grid line')],21:[(669,2037,17,'pair 1 left; circle overlaps hatching'),(1361,2023,18,'pair 1 right; circle overlaps another circle, hatching and vertical grid line'),(1361,2042,18,'single; circle overlaps pair 1 right, hatching and vertical grid line; two rings visible'),(1033,1983,17,'pair 2 left; circle overlaps hatching'),(1177,1983,17,'pair 2 right; circle overlaps hatching'),(2339,2202,17,'pair 3 left; circle overlaps hatching'),(2426,2199,17,'pair 3 right; circle overlaps hatching; close to right frame but not cut'),(2339,2245,17,'single; circle overlaps hatching')],22:[(1690,2017,18,'single; circle overlaps solid curve and horizontal grid line'),(2340,1584,18,'single; circle overlaps solid curve')]}
labels={'rc2':(1637,1895,'RC2'),'ps':(1665,2004,'PS'),'rs':(1363,2209,'RS'),'rsm-b':(1214,2415,'RSM-b'),'rsm-a':(1787,2241,'RSM-a'),'ss':(1793,2655,'SS')}
cols='figure_id panel series_id point_kind sequence pixel_u pixel_v u_bound_px v_bound_px symbol note'.split()
def writecsv(p,rows):
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows(rows)
def row(n,s,k,seq,u,v,b,note='',symbol=''):
 return dict(zip(cols,[f'FC-{n}',1,s,k,seq,round(u,2),round(v,2),b,b,symbol,note]))
for n in [20,21,22,23]:
 d=Path(f'out/FC-{n}'); im=f'packet/p0{136+n}.png'; gray=np.asarray(Image.open(im).convert('L')); cal,X,Y=ca.piecewise_maps(d/'cal-p1',im)
 rows=[row(n,'data','marker',i+1,u,v,b,note,'circle') for i,(u,v,b,note) in enumerate(markers.get(n,[]))]
 if n==21:
  # The band boundaries are the printed 45 and 40 degree horizontal grid lines.
  for s,value in [('band-top',45),('band-bottom',40)]:
   hl=next(l for l in cal['horizontal_lines'] if l['y_value']==value)
   left=590 if value==45 else 599;right=2454 if value==45 else 2460
   slope=hl['slope_dv_du'];inter=hl['v_at_u0']; pts=[(left,inter+slope*left)]
   for x in np.arange(-.05,1.1,.05):
    # Solve x knot interpolation iteratively at the band's y.
    u=left+(x+.1)*1560
    for _ in range(5):u+=(x-X.value(u,inter+slope*u)[0])/cal['ax'][0]
    if left+3<u<right-3:pts.append((u,inter+slope*u))
   pts.append((right,inter+slope*right))
   for i,(u,v) in enumerate(pts):rows.append(row(n,s,'trace',i+1,u,v,2.5,'band boundary coincides with grid line'))
   rows.extend([row(n,s,'feature',1,*pts[0],2.5,'first point'),row(n,s,'feature',2,*pts[-1],2.5,'last point; peak')])
 else:
  for s,path in paths[n].items():
   pp=np.array(path); us=np.arange(pp[0,0],pp[-1,0]+1); vs=np.interp(us,pp[:,0],pp[:,1]); grad=np.gradient(vs)
   track=[]
   for u,v,m in zip(us,vs,grad):
    # Scan perpendicular to the expected tangent, averaging across 5 pixels of line.
    # Grid coincidences and marker outlines are left for the visual review.
    if any(abs(u-(l['u_at_v0']+l['slope_du_dv']*v))<7 for l in cal['vertical_lines']):continue
    if any(abs(v-(l['v_at_u0']+l['slope_dv_du']*u))<7 for l in cal['horizontal_lines']):continue
    if any((u-a)**2+(v-b)**2<23**2 for a,b,r,_ in markers.get(n,[])):continue
    offsets=np.arange(-32,33); scores=[]
    for off in offsets:
     vv=v+off
     vals=[gray[round(vv+m*t),round(u+t)] for t in range(-2,3)]
     scores.append(np.mean(vals))
    mask=np.array(scores)<100; idx=np.flatnonzero(mask)
    if len(idx)==0:continue
    runs=np.split(idx,np.where(np.diff(idx)>1)[0]+1)
    runs=[r for r in runs if 2<=len(r)<=16 and not any(abs(v+np.mean(offsets[r])-(l['v_at_u0']+l['slope_dv_du']*u))<8 for l in cal['horizontal_lines'])]
    if n==23 and s=='ps':runs=[r for r in runs if not (1620<u<1680 and 1980<v+np.mean(offsets[r])<2037)]
    if n==23 and s=='rsm-b':runs=[r for r in runs if not (1130<u<1210 and 2360<v+np.mean(offsets[r])<2462)]
    if not runs:continue
    r=min(runs,key=lambda r:abs(np.mean(offsets[r])))
    center=v+np.mean(offsets[r]);track.append((float(u),float(center),max(2,len(r)/2)))
   track=np.array(track); targets=[]
   # Endpoints are explicit eye readings, refined within their small end neighbourhood.
   ends={20:{'mean':[(798,3262),(2322,2326)],'upper':[(801,3177),(2336,2167)],'lower':[(805,3385),(2343,2393)]},22:{'mean':[(854,2546),(2414,1546)],'upper':[(858,2455),(2410,1465)],'lower':[(855,2648),(2413,1647)]},23:{'rc2':[(926,2259),(2513,1460)],'ps':[(926,2247),(2643,1748)],'rs':[(792,2544),(2646,1706)],'rsm-b':[(938,2605),(2509,1608)],'rsm-a':[(938,2717),(2646,1920)],'ss':[(945,3296),(2515,2347)]}}
   if n==22:ends[n]={'mean':[(854,2546),(2411,1548)],'upper':[(858,2455),(2404,1466)],'lower':[(855,2648),(2408,1647)]}
   if n==20:ends[n]['mean'][-1]=(2322,2318)
   if n==23:ends[n]['ss'][0]=(946,3292)
   for u,v in ends[n][s]:
    # A small final pixel check keeps manually located endpoints on actual ink.
    near=[(math.hypot(uu-u,vv-v),uu,vv) for uu in range(u-6,u+7) for vv in range(v-6,v+7) if gray[vv,uu]<100]
    if near and gray[v,u]>=100:_,u,v=min(near)
    targets.append(np.array([u,v,3.0]))
   start,end=targets
   a=X.value(*start[:2])[0];b=X.value(*end[:2])[0];samples=[(start,None)]
   for x in np.arange(math.floor(a/.05)*.05+.05,b-.0001,.05):
    xv=np.array([X.value(u,v)[0] for u,v,_ in track]);idx=np.argmin(abs(xv-x));p=track[idx]
    # At a grid crossing of a solid curve the adjoining ink establishes its center.
    # Keep the requested abscissa; the pixel itself is on the crossing's visible ink.
    if s in ['mean','rc2','ss']:
     u=p[0]
     for _ in range(4):
      v=np.interp(u,track[:,0],track[:,1]);u+=(x-X.value(u,v)[0])/cal['ax'][0]
     v=np.interp(u,track[:,0],track[:,1]);p=np.array([u,v,p[2]])
    samples.append((p,float(x)))
   samples.append((end,None))
   for i,(p,x) in enumerate(samples):
    u,v,width=p;note='first ink point' if i==0 else ('last ink point' if i==len(samples)-1 else f'target Dr={x:.2f}')
    if x is not None and abs(X.value(u,v)[0]-x)>.004:note+='; moved to nearest visible dash end or ink beside grid/symbol interruption'
    rows.append(row(n,s,'trace',i+1,u,v,round(width,1),note))
   rows.extend([row(n,s,'feature',1,*start[:2],round(start[2],1),'first point'),row(n,s,'feature',2,*end[:2],round(end[2],1),'last point; peak')])
   if n==23:
    u,v,label=labels[s];rows.append(row(n,s,'feature',3,u,v,3,f'label: {label}'))
 writecsv(d/'points-p1.csv',rows)
 ca.piecewise_rows(cal,X,Y,rows)
 with (d/'points-p1-native.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 # Full-page, unrotated overlay; no interpolation across the dashed curves.
 img=Image.open(im).convert('RGB');draw=ImageDraw.Draw(img)
 palette=['#e32636','#164cff','#008050','#ba00ba','#d27000','#00a0aa']
 series=list(dict.fromkeys(r['series_id'] for r in rows))
 for r in rows:
  color=palette[series.index(r['series_id'])%len(palette)];u=float(r['pixel_u']);v=float(r['pixel_v']);b=float(r['u_bound_px'])
  if r['point_kind']=='marker':draw.ellipse((u-b,v-b,u+b,v+b),outline=color,width=2);draw.line((u-6,v,u+6,v),fill=color,width=2);draw.line((u,v-6,u,v+6),fill=color,width=2)
  else:draw.ellipse((u-5,v-5,u+5,v+5),outline=color,width=2)
 draw.rectangle((30,100,550,160+40*len(series)),fill='white')
 for i,s in enumerate(series):draw.text((50,130+i*40),f'{s}: '+palette[i%6],fill=palette[i%6])
 img.save(d/'overlay-p1.png')
 print(n,[(s,k,sum(r['series_id']==s and r['point_kind']==k for r in rows)) for s in series for k in ['marker','trace','feature'] if any(r['series_id']==s and r['point_kind']==k for r in rows)])
