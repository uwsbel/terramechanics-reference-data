"""Blind page reading helpers. Guides are manually read from the packet's pixel crops.
Guide segments select an ink corridor; reported samples are moved to actual stroke ink.
No guide-interpolated point in a dash gap is reported.
"""
import csv,json,sys,math
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca

# (u,v) coordinates on unrotated original pages, in drawing order.
# Vertices only guide selection; they are not observations.
GUIDES={
'F2-42':{
'lpt22':[(844,3351),(852,3270),(862,3198),(874,3100),(884,3040),(894,2960),(902,2885),(915,2800),(925,2733),(938,2650),(948,2577),(960,2500),(970,2422),(983,2340),(1000,2267),(1022,2175),(1045,2110),(1065,2067),(1100,2020),(1137,1992),(1160,2002),(1200,2023),(1240,2041),(1270,2048),(1290,2045),(1310,2010),(1340,1960),(1380,1890),(1420,1825),(1460,1750),(1500,1680),(1540,1615),(1580,1554),(1618,1530)],
'lpt23':[(848,3351),(858,3270),(867,3198),(881,3100),(891,3040),(903,2960),(912,2885),(925,2800),(936,2733),(949,2650),(960,2577),(973,2500),(985,2422),(1000,2340),(1018,2267),(1038,2175),(1060,2110),(1080,2030),(1100,1940),(1120,1850),(1143,1770),(1180,1720),(1210,1685),(1240,1669),(1280,1666),(1320,1666),(1360,1666),(1390,1656),(1420,1640),(1460,1618),(1497,1597)],
'lpt24':[(860,3351),(871,3270),(881,3198),(891,3100),(905,3040),(916,2960),(926,2885),(936,2800),(946,2733),(956,2650),(968,2577),(978,2500),(990,2422),(1003,2340),(1017,2267),(1034,2180),(1050,2110),(1070,2060),(1090,2010),(1114,1960),(1125,1951),(1145,1958),(1180,1972),(1220,1988),(1260,2007),(1300,2023),(1320,2030),(1345,2025),(1370,2010),(1390,1990),(1420,1905),(1460,1815),(1500,1735),(1540,1660),(1580,1597),(1610,1545),(1650,1480),(1690,1407),(1740,1334)],
'lpt25':[(840,3350),(846,3270),(851,3198),(860,3100),(869,3040),(877,2960),(887,2885),(896,2800),(909,2733),(919,2650),(930,2577),(939,2500),(949,2422),(961,2340),(976,2267),(997,2175),(1014,2110),(1037,2040),(1066,1980),(1093,1935),(1125,1890),(1160,1855),(1200,1820),(1240,1797),(1280,1777),(1320,1756),(1360,1735),(1400,1711),(1440,1678),(1480,1637),(1520,1590),(1560,1545),(1600,1495),(1640,1442),(1680,1386),(1715,1334)]
},
'F2-44':{
'lpt24':[(751,3138),(769,3090),(786,3015),(803,2940),(820,2870),(840,2795),(861,2720),(890,2650),(917,2600),(950,2568),(990,2548),(1030,2547),(1070,2555),(1120,2564),(1160,2573),(1190,2580),(1230,2555),(1270,2525),(1310,2497),(1357,2473),(1400,2440),(1440,2406),(1480,2375),(1520,2336),(1560,2298),(1600,2261),(1640,2227),(1672,2207)],
'lpt73':[(749,3135),(764,3070),(780,2990),(797,2910),(811,2830),(824,2750),(839,2670),(854,2610),(875,2578),(893,2567),(920,2568),(950,2578),(990,2594),(1020,2610),(1055,2633),(1080,2617),(1120,2585),(1160,2545),(1200,2490),(1240,2410),(1280,2320),(1320,2230),(1360,2140),(1400,2075),(1440,2035),(1480,1997),(1520,1962),(1560,1927),(1600,1895),(1650,1861)],
'lpt74':[(751,3138),(765,3070),(778,2990),(795,2910),(810,2830),(824,2750),(839,2670),(850,2620),(864,2590),(895,2586),(925,2590),(960,2610),(1000,2640),(1040,2670),(1065,2687),(1090,2685),(1120,2674),(1160,2663),(1200,2640),(1240,2615),(1280,2577),(1320,2520),(1357,2495),(1400,2468),(1440,2444),(1480,2420),(1520,2395),(1560,2365),(1600,2334),(1640,2306),(1680,2272),(1720,2238),(1760,2203),(1800,2160),(1840,2115),(1880,2068),(1920,2023),(1960,1980),(2000,1933),(2040,1888),(2075,1845),(2107,1810)],
'lpt69':[(747,3130),(761,3060),(777,2980),(793,2900),(808,2820),(821,2740),(834,2660),(847,2580),(860,2500),(875,2420),(895,2355),(918,2320),(940,2310),(965,2310),(990,2324),(1020,2355),(1050,2390),(1090,2440),(1130,2491),(1170,2537),(1200,2570),(1219,2576),(1250,2556),(1290,2530),(1330,2500),(1360,2470),(1400,2430),(1440,2388),(1480,2347),(1520,2304),(1560,2260),(1600,2220),(1640,2180),(1680,2140),(1720,2117),(1760,2100),(1800,2085),(1840,2070),(1880,2056),(1920,2043),(1960,2030),(2000,2015),(2040,1997),(2080,1973),(2110,1940),(2140,1893),(2185,1835)],
'lpt64a':[(747,3130),(761,3060),(777,2980),(792,2900),(808,2820),(822,2740),(835,2660),(851,2580),(872,2500),(895,2440),(920,2400),(945,2380),(970,2380),(1010,2385),(1040,2401),(1070,2450),(1100,2505),(1130,2575),(1160,2640),(1190,2683),(1220,2710),(1250,2724),(1290,2732),(1320,2739),(1340,2738),(1370,2725),(1400,2707),(1440,2680),(1480,2645),(1520,2607),(1560,2567),(1600,2525),(1640,2480),(1680,2434),(1720,2382),(1760,2330),(1800,2270),(1840,2211),(1880,2154),(1920,2095),(1960,2039),(2000,1973),(2040,1910),(2077,1840)]
}}
# Correct F2-42 B and D guides below: solid and long dashes are the two LEFT branches.
# Upper read-grid has origin (830,1320). B plateau u~1200,v1666.
# B rise must connect to u~1060,v1800, rather than the C peak below it.
GUIDES['F2-42']['lpt23']=[(848,3351),(855,3270),(862,3198),(875,3100),(886,3040),(898,2960),(907,2885),(919,2800),(929,2733),(941,2650),(951,2577),(961,2500),(972,2422),(983,2340),(998,2267),(1013,2175),(1027,2110),(1043,2030),(1061,1940),(1082,1850),(1106,1770),(1146,1720),(1180,1685),(1210,1669),(1240,1666),(1280,1666),(1320,1666),(1360,1666),(1390,1656),(1420,1640),(1460,1618),(1497,1597)]
# Coordinates of D in the upper crop reach the frame at u~1617, not the C frame end.
GUIDES['F2-42']['lpt25']=[(840,3350),(842,3300),(845,3200),(851,3100),(856,3000),(860,2900),(869,2800),(879,2700),(890,2600),(904,2500),(917,2400),(932,2300),(949,2200),(970,2110),(1000,2030),(1019,2000),(1045,1950),(1070,1900),(1100,1860),(1140,1820),(1180,1790),(1226,1750),(1270,1728),(1310,1700),(1365,1666),(1400,1630),(1428,1597),(1470,1550),(1515,1490),(1550,1440),(1580,1390),(1618,1334)]
GUIDES['F2-42']['lpt23']=[(848,3351),(850,3300),(859,3200),(864,3100),(867,3000),(874,2900),(885,2800),(895,2700),(903,2600),(920,2500),(937,2400),(945,2300),(959,2200),(974,2110),(993,2030),(1003,1995),(1015,1950),(1028,1900),(1047,1840),(1064,1800),(1087,1750),(1134,1700),(1170,1675),(1200,1666),(1250,1666),(1310,1666),(1350,1666),(1390,1656),(1420,1640),(1460,1618),(1497,1597)]
GUIDES['F2-42']['lpt22']=[(844,3351),(853,3300),(865,3200),(871,3100),(875,3000),(882,2900),(891,2800),(904,2700),(915,2600),(930,2500),(946,2400),(959,2300),(981,2200),(1006,2110),(1042,2050),(1080,2025),(1118,2000),(1137,1992),(1160,2002),(1200,2023),(1240,2041),(1270,2048),(1290,2045),(1310,2010),(1340,1960),(1380,1890),(1420,1825),(1460,1750),(1500,1680),(1540,1615),(1580,1554),(1618,1530)]
GUIDES['F2-42']['lpt24']=[(860,3351),(862,3300),(870,3200),(878,3100),(887,3000),(895,2900),(905,2800),(915,2700),(927,2600),(940,2500),(953,2400),(971,2300),(995,2200),(1019,2110),(1048,2050),(1077,2000),(1102,1960),(1125,1951),(1145,1958),(1180,1972),(1220,1988),(1260,2007),(1300,2023),(1320,2030),(1345,2025),(1370,2010),(1390,1990),(1420,1905),(1460,1815),(1500,1735),(1540,1660),(1580,1597),(1610,1545),(1650,1480),(1690,1407),(1740,1334)]
GUIDES['F2-42']['lpt22']=GUIDES['F2-42']['lpt22'][:24]+[(1346,1950),(1383,1900),(1415,1850),(1446,1800),(1476,1750),(1507,1700),(1537,1650),(1568,1597),(1596,1554),(1618,1530)]
GUIDES['F2-42']['lpt25']=GUIDES['F2-42']['lpt25'][:13]+[(993,2030),(1003,1995),(1015,1950),(1025,1930),(1040,1910),(1055,1890),(1080,1855),(1105,1828),(1135,1800),(1175,1775),(1226,1750),(1270,1728),(1310,1700),(1365,1666),(1400,1630),(1428,1597),(1470,1550),(1515,1490),(1550,1440),(1580,1390),(1618,1334)]
GUIDES['F2-44']['lpt24']=GUIDES['F2-44']['lpt24'][:22]+[(1357,2480),(1400,2450),(1450,2410),(1500,2385),(1550,2338),(1600,2295),(1650,2246),(1672,2210)]
GUIDES['F2-44']['lpt73']=GUIDES['F2-44']['lpt73'][:22]+[(1360,2175),(1400,2115),(1440,2075),(1480,2031),(1520,1996),(1560,1958),(1600,1915),(1650,1861)]
GUIDES['F2-44']['lpt64a']=[p for p in GUIDES['F2-44']['lpt64a'] if p[0]<1400]+[(1406,2700),(1506,2600),(1592,2500),(1673,2400),(1745,2300),(1818,2200),(1888,2100),(1964,2000),(2034,1900),(2077,1840)]
GUIDES['F2-44']['lpt74']=[p for p in GUIDES['F2-44']['lpt74'] if p[0]<1600]+[(1600,2340),(1660,2300),(1720,2250),(1774,2200),(1800,2173),(1850,2126),(1900,2078),(1950,2028),(1990,1990),(2025,1953),(2060,1917),(2107,1867)]
GUIDES['F2-42']['lpt25'][2]=(855,3200)
GUIDES['F2-42']['lpt24']=[p for p in GUIDES['F2-42']['lpt24'] if p[0]<1320]+[(1320,2025),(1345,2018),(1360,2000),(1375,1977),(1395,1930),(1420,1880),(1450,1824),(1480,1765),(1510,1707),(1540,1652),(1580,1590),(1610,1545),(1650,1480),(1690,1407),(1740,1334)]
GUIDES['F2-44']['lpt74']=[p for p in GUIDES['F2-44']['lpt74'] if p[0]<1160]+[(1160,2633),(1200,2607),(1219,2580),(1250,2556),(1290,2530),(1330,2500),(1357,2488)]+[p for p in GUIDES['F2-44']['lpt74'] if p[0]>1357]
GUIDES['F2-44']['lpt24']=[p for p in GUIDES['F2-44']['lpt24'] if p[0]<1190]+[(1190,2580),(1230,2565),(1270,2539),(1310,2510),(1357,2480)]+[p for p in GUIDES['F2-44']['lpt24'] if p[0]>1357]
GUIDES['F2-44']['lpt24']=[(762,3144),(780,3060),(797,2980),(816,2900),(846,2800),(881,2700),(906,2640),(930,2590),(970,2555),(1030,2547),(1070,2555),(1120,2564),(1160,2573),(1190,2580),(1230,2565),(1270,2539),(1310,2510),(1357,2480),(1400,2450),(1450,2410),(1500,2385),(1550,2338),(1600,2295),(1650,2246),(1672,2210)]
GUIDES['F2-42']['lpt25'][3]=(856,3100)
GUIDES['F2-42']['lpt25'][4]=(858,3000)
GUIDES['F2-44']['lpt24']=[p for p in GUIDES['F2-44']['lpt24'] if p[0]<1357]+[(1357,2490),(1400,2460),(1430,2438),(1450,2422),(1480,2400),(1510,2375),(1550,2340),(1585,2302),(1620,2270),(1650,2240),(1672,2210)]
GUIDES['F2-44']['lpt24']=[p for p in GUIDES['F2-44']['lpt24'] if p[0]<930]+[(930,2607),(955,2580),(980,2563),(1000,2549),(1017,2541),(1035,2545),(1070,2555)]+[p for p in GUIDES['F2-44']['lpt24'] if p[0]>1070]

STYLES={'F2-42':{'lpt22':'dotted','lpt23':'solid','lpt24':'short-dashed','lpt25':'long-dashed'},'F2-44':{'lpt24':'dashed','lpt73':'dashed','lpt74':'dotted','lpt69':'solid','lpt64a':'solid'}}

FEATURES={
'F2-42':{
'lpt22':[(1137,1992,'peak; first local maximum'),(1270,2048,'knee; minimum after first maximum'),(1310,2010,'knee; steeper recovery')],
'lpt23':[(1087,1750,'knee; rise begins flattening'),(1210,1666,'peak; first local maximum; nearly flat shelf'),(1355,1667,'knee; shallow minimum at shelf end, not resolved beyond stroke width')],
'lpt24':[(1125,1951,'peak; first local maximum'),(1320,2025,'knee; minimum after first maximum'),(1375,1977,'knee; recovery steepens')],
'lpt25':[(1140,1820,'knee; initial rise flattens'),(1365,1666,'knee; rise steepens')]
},
'F2-44':{
'lpt24':[(1017,2541,'peak; first local maximum; adjacent dash ends bound the uninked apex'),(1190,2580,'knee; minimum after first maximum')],
'lpt73':[(893,2567,'peak; first local maximum'),(1055,2633,'knee; minimum after first maximum'),(1360,2175,'knee; steep recovery becomes shallower')],
'lpt74':[(895,2586,'peak; first local maximum'),(1065,2687,'knee; minimum after first maximum'),(1219,2580,'knee; recovery joins nearly coincident rising traces')],
'lpt69':[(950,2310,'peak; first local maximum'),(1219,2576,'knee; minimum after first maximum'),(1710,2120,'knee; recovery becomes shallower'),(2090,1965,'knee; final upturn')],
'lpt64a':[(955,2380,'peak; first local maximum'),(1320,2739,'knee; minimum after first maximum')]
}}

def writecsv(p,rows):
 with Path(p).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def runs(x):
 z=np.where(x)[0]
 return np.split(z,np.where(np.diff(z)>1)[0]+1) if len(z) else []

def read(fig,page):
 folder=Path('out')/fig
 cal,X,Y=ca.piecewise_maps(folder/'cal-p1','packet/'+page+'.png')
 g=np.array(Image.open('packet/'+page+'.png').convert('L'))
 # Do not allow a grid or frame stroke to stand in for dashed/dotted curve ink.
 curveg=g.copy()
 vmin,vmax=(1325,3355) if fig=='F2-42' else (1690,3260)
 umin,umax=(833,1768) if fig=='F2-42' else (730,2295)
 for ln in cal['vertical_lines']:
  for vv in range(vmin,vmax+1):
   uu=round(ln['u_at_v0']+ln['slope_du_dv']*vv)
   half=5 if ln['x_value'] in (0,3 if fig=='F2-42' else 5) else 3
   curveg[vv,uu-half:uu+half+1]=255
 for ln in cal['horizontal_lines']:
  for uu in range(umin,umax+1):
   if fig=='F2-42' and ln['y_value']==400 and uu>1200:continue
   if fig=='F2-44' and ln['y_value']==2000 and 1040<uu<1970:continue
   vv=round(ln['v_at_u0']+ln['slope_dv_du']*uu)
   half=5 if ln['y_value']==0 else 2
   curveg[vv-half:vv+half+1,uu]=255
 allrows=[];audit=[]
 for sid,verts in GUIDES[fig].items():
  verts=np.array(verts,float)
  d=np.r_[0,np.cumsum(np.linalg.norm(np.diff(verts,axis=0),axis=1))]
  ts=np.arange(0,d[-1]+.1,.5)
  if ts[-1]<d[-1]:ts=np.r_[ts,d[-1]]
  path=np.column_stack([np.interp(ts,d,verts[:,i]) for i in (0,1)])
  tangent=np.gradient(path,axis=0);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
  normal=np.column_stack([-tangent[:,1],tangent[:,0]])
  # Read transverse dark runs near the manually selected trace corridor.
  cand=[];width=[]
  for q,n in zip(path,normal):
   off=np.arange(-8,8.01,.5)
   pos=q+off[:,None]*n
   dark=curveg[np.rint(pos[:,1]).astype(int),np.rint(pos[:,0]).astype(int)]<150
   rr=[r for r in runs(dark) if len(r)>=2]
   if not rr:cand.append([np.nan,np.nan]);width.append(np.nan);continue
   rr=min(rr,key=lambda r:abs(np.mean(off[r])))
   mid=np.mean(off[rr]);cand.append(q+n*mid);width.append((len(rr)*.5)/2)
  cand=np.array(cand);width=np.array(width)
  natural_valid=np.isfinite(width)
  valid=natural_valid & (width>=2.5)
  # A grid crossing may clip a transverse run into a false narrow fragment.
  # Move the sample along its trace to clear that grid, and disclose the move.
  for ln in cal['vertical_lines']:
   valid &= abs(path[:,0]-(ln['u_at_v0']+ln['slope_du_dv']*path[:,1]))>8
  for ln in cal['horizontal_lines']:
   if ln['y_value']==400 and fig=='F2-42':covered=path[:,0]>1200
   elif ln['y_value']==2000 and fig=='F2-44':covered=(path[:,0]>1040)&(path[:,0]<1970)
   else:covered=np.zeros(len(path),bool)
   valid &= (abs(path[:,1]-(ln['v_at_u0']+ln['slope_dv_du']*path[:,0]))>8)|covered
  # Calculate sampling targets from the verified piecewise grids, retaining path order.
  xv=np.array([X.value(*q)[0] for q in path]);yv=np.array([Y.value(*q)[0] for q in path])
  targets=[(0,'trace','first trace ink'),(len(path)-1,'trace','last trace ink')]
  for x in np.arange(.25,math.floor(max(xv)*4)/4+.001,.25):
   # The last short dash meets the x=3 grid; the endpoint is also the
   # nearest readable stroke sample for the 3-inch target.
   if fig=='F2-44' and sid=='lpt24' and x==3:continue
   ii=np.where((xv[:-1]-x)*(xv[1:]-x)<=0)[0]
   for j in ii:targets.append((int(j),'trace',f'penetration target {x:g} in'))
  # 100-lb spacing on initial rising branch, until the first local peak.
  firstpeak=FEATURES[fig][sid][0][:2] if FEATURES[fig][sid] and FEATURES[fig][sid][0][2].startswith('peak') else None
  stop=int(np.argmin(np.sum((path-np.array(firstpeak))**2,axis=1))) if firstpeak else int(np.argmax(yv[:max(2,len(path)//2)]))
  if fig=='F2-42' and sid in ('lpt23','lpt25'):stop=np.argmin(abs(yv-1000))
  for y in np.arange(math.ceil(yv[0]/100)*100,max(yv[:stop+1])+1,100):
   ii=np.where((yv[:stop]-y)*(yv[1:stop+1]-y)<=0)[0]
   if len(ii):targets.append((int(ii[0]),'trace',f'initial rise target {y:g} lb'))
  features=[(*verts[0],'first; visible ink start'),*FEATURES[fig][sid],(*verts[-1],'last; visible ink end')]
  for u,v,note in features:
   targets.append((int(np.argmin(np.sum((path-[u,v])**2,axis=1))),'feature',note))
  targets.sort(key=lambda t:(t[0],0 if t[1]=='trace' else 1))
  rows=[];read_order=[];lasttrace=-100
  for idx,kind,note in targets:
   endpoint=idx in (0,len(path)-1)
   near=np.where((natural_valid if endpoint else valid) & (abs(ts-ts[idx])<80))[0]
   if not len(near):raise ValueError((fig,sid,idx,path[idx].tolist(),'no own ink'))
   j=near[np.argmin(abs(ts[near]-ts[idx]))]
   if kind=='trace' and abs(ts[j]-lasttrace)<4:continue
   if kind=='trace':lasttrace=ts[j]
   p=cand[j].copy();n=normal[j];t=tangent[j]
   # Measure the full local stroke on the original image, not the clipped mask.
   off=np.arange(-20,20.01,.25);pos=p+off[:,None]*n
   rr=runs(g[np.rint(pos[:,1]).astype(int),np.rint(pos[:,0]).astype(int)]<150)
   rr=min(rr,key=lambda z:abs(np.mean(off[z])))
   half=len(rr)*.25/2
   p+=n*np.mean(off[rr])
   # Half the nearest complete dash/dot gap along this manually identified corridor.
   # Gaps are searched locally rather than mistaken for continuous observations.
   a=max(0,j-140);b=min(len(path),j+141)
   gaps=runs(~natural_valid[a:b])
   gap=max([len(z)*.5/2 for z in gaps if min(abs((z+a)-j))<80] or [0]) if STYLES[fig][sid]!='solid' else 0
   bu=max(.75,half)+abs(t[0])*gap;bv=max(.75,half)+abs(t[1])*gap
   # Endpoints are identifiable only along the ink; preserve the hand-read endpoint.
   isfirst=('first;' in note or note=='first trace ink')
   islast=('last;' in note or note=='last trace ink')
   if isfirst or islast:
    end=verts[0] if isfirst else verts[-1]
    p=end.copy()
    # A hand endpoint can be subpixel displaced from binary scan ink.
    uu,vv=map(lambda z:int(round(z)),p)
    if g[vv,uu]>=150:
     coords=np.argwhere(g[vv-4:vv+5,uu-4:uu+5]<150)
     if len(coords):
      c=coords[np.argmin(np.sum((coords-[4,4])**2,axis=1))];p=np.array([uu+c[1]-4,vv+c[0]-4],float)
    if isfirst:note+='; merged/partly unresolved start, bound covers neighboring initial strokes'
   elif abs(ts[j]-ts[idx])>2:
    note+=f'; moved {abs(ts[j]-ts[idx]):.1f} px along trace to ink clear of dash gap/grid'
   if gap>1:note+=f'; {STYLES[fig][sid]} ink; half local gap {gap:.1f} px along stroke'
   if fig=='F2-42':
    if p[1]>2110:bu=max(bu,10);bv=max(bv,12);note+='; congested initial rise, traces overlap or run together'
    if sid=='lpt22' and p[0]>1570:bu=max(bu,9);bv=max(bv,12);note+='; dotted A approaches/merges short-dashed C'
    if sid in ('lpt22','lpt24') and 1270<p[0]<1335 and p[1]<2070:bu=max(bu,9);bv=max(bv,10);note+='; A/C crossing vicinity'
    if sid in ('lpt23','lpt25') and 1315<p[0]<1390 and p[1]<1700:bu=max(bu,10);bv=max(bv,10);note+='; B/D crossing vicinity'
   else:
    if p[0]<870:bu=max(bu,13);bv=max(bv,18);note+='; congested initial rise, individual starts not resolved'
    if sid in ('lpt24','lpt74','lpt69') and 1180<p[0]<1380 and 2460<p[1]<2620:
     bu=max(bu,15);bv=max(bv,16);note+='; 24/74/69 nearly coincident rising strokes; individual centers unresolved'
    if sid in ('lpt24','lpt73','lpt74') and 890<p[0]<990 and 2555<p[1]<2640:
     bu=max(bu,12);bv=max(bv,12);note+='; crossing/near approach of 24,73,74; identity from branch continuity'
    # Explicitly mark crossing neighborhoods, below and above the first peaks.
    if (1120<p[0]<1235 and 2490<p[1]<2690) or (1300<p[0]<1390 and 2440<p[1]<2535) or (1870<p[0]<1990 and 1990<p[1]<2125):
     bu=max(bu,10);bv=max(bv,12);note+='; crossing or near-coincident trace neighborhood; identity by continuity/style'
   r=dict(figure_id=fig,panel=1,series_id=sid,point_kind=kind,sequence=len(rows)+1,pixel_u=round(p[0],2),pixel_v=round(p[1],2),u_bound_px=round(bu,2),v_bound_px=round(bv,2),symbol='',note=note)
   rows.append(r)
   read_order.append((0 if isfirst else d[-1] if islast else ts[j],0 if kind=='trace' else 1))
   audit.append(dict(series_id=sid,sequence=r['sequence'],guide_u=round(path[idx,0],2),guide_v=round(path[idx,1],2),move_px=round(float(np.linalg.norm(p-path[idx])),2),normal_halfwidth_px=round(half,2),half_gap_px=round(gap,2)))
  # Snapping to a dash can move past a neighboring target. Restore order by
  # distance along the manually followed stroke, never by penetration/x.
  ix=sorted(range(len(rows)),key=lambda k:read_order[k])
  rows=[rows[k] for k in ix]
  aa=audit[-len(rows):]
  aa=[aa[k] for k in ix]
  for k,(r,a) in enumerate(zip(rows,aa),1):r['sequence']=k;a['sequence']=k
  audit[-len(rows):]=aa
  allrows+=rows
 writecsv(folder/'points-p1.csv',allrows)
 writecsv(folder/'sampling-audit.csv',audit)
 native=[r.copy() for r in allrows]
 ca.piecewise_rows(cal,X,Y,native)
 writecsv(folder/'points-p1-native.csv',native)
 (folder/'cal-p1'/'verified-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 # Native-vs-affine diagnostic requested by D-025.
 sensitivity=[]
 for sid in GUIDES[fig]:
  rr=[r for r in native if r['series_id']==sid]
  dx=[abs(r['x_native']-np.dot(cal['ax'],[r['pixel_u'],r['pixel_v'],1])) for r in rr]
  dy=[abs(r['y_native']-np.dot(cal['ay'],[r['pixel_u'],r['pixel_v'],1])) for r in rr]
  sensitivity.append(dict(series_id=sid,max_x_difference_in=round(max(dx),6),max_y_difference_lb=round(max(dy),4)))
 writecsv(folder/'calibration-sensitivity.csv',sensitivity)
 print(fig,dict(Counter((r['series_id'],r['point_kind']) for r in allrows)))

if __name__=='__main__':
 read('F2-42','p0102');read('F2-44','p0104')
