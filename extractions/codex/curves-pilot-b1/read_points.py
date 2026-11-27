"""Independent FC-1B reading. Hand-placed markers and guide knots; ink-run trace sampling.
All coordinates refer to packet/p0117.png. No outside readings are inputs.
"""
from pathlib import Path
import csv, json
import numpy as np
from PIL import Image

OUT=Path('out')
SYMBOL={'n294':'circle','n587':'triangle-up','n1172':'triangle-down','n1760':'plus','n2345':'square','n2935':'asterisk','n3520':'x'}
FIELDS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
P1={
'n294':[(853,2791),(975,2739),(1094,2708),(1206,2685),(1329,2676.5),(1443,2670),(1558.5,2673.5),(1675,2678),(1794,2680),(1914,2677),(2028,2675),(2142,2675),(2264,2673)],
'n587':[(914,2625),(1030,2561),(1146.5,2534.5),(1262,2528),(1383,2524),(1495,2526),(1616,2526),(1734,2554),(1853.5,2576),(1973,2600),(2086,2601),(2263,2612)],
'n1172':[(851.5,2637),(965,2521),(1087,2429),(1202,2389),(1323.5,2358.5),(1440.5,2347),(1551.5,2346.5),(1672,2354),(1788,2354),(1909,2357),(1968,2365),(2083,2372),(2264,2386)],
'n1760':[(911,2436),(1028,2333),(1140,2256),(1266.5,2198),(1390,2166),(1498.5,2150),(1612,2168),(1730,2166),(1857,2189),(1970,2193),(2083,2202),(2250,2227)],
'n2345':[(851,2537),(975,2385),(1093,2260),(1263,2122),(1317,2095),(1438,2065),(1550,2039),(1669,2029),(1788,2031),(1911,2027),(2026,2024.5),(2196.5,2046.5),(2259,2061)],
'n2935':[(906,2327.5),(1031,2178.5),(1148,2066.5),(1258,1986),(1383,1925),(1492.5,1893),(1613,1874),(1730,1860.5),(1905,1869),(2015.5,1876.5),(2143,1878.5),(2265,1872.5)],
'n3520':[(906,2243),(1132,1955),(1257,1855.5),(1492.5,1752.5),(1726,1697),(1964,1668),(2081,1672),(2250,1706)]}

P2={
'n294':[(807,3294),(874,3289),(989,3281),(1107,3267),(1222,3242),(1343,3227),(1460.5,3187),(1576,3169),(1687,3149),(1806.5,3121),(1930,3101),(2049.5,3086),(2170.5,3064.5),(2274,3050)],
'n587':[(835,3295),(915,3293),(1027.5,3255.5),(1164.5,3230),(1284.5,3203.5),(1395,3174),(1517.5,3138.5),(1635.5,3122),(1749,3095.5),(1871.5,3071),(1982,3060),(2106.5,3040.5),(2274,3017)],
'n1172':[(808,3296),(874,3309),(991,3303),(1107,3288),(1225,3260),(1345,3246),(1461.5,3220.5),(1578,3196),(1688,3174),(1808.5,3155.5),(1932.5,3134.5),(1989,3121),(2104,3107),(2278,3075)],
'n1760':[(780,3293),(941,3280),(1058,3270),(1164,3260),(1275.5,3243),(1398,3226),(1511,3206),(1633.5,3190),(1750.5,3176),(1863,3162.5),(1982,3156),(2105,3137),(2276,3111)],
'n2345':[(809,3340),(874,3344.5),(992,3339),(1106,3330),(1280.5,3320.5),(1349,3314.5),(1457.5,3297),(1575.5,3290.5),(1687,3286),(1809,3274),(1933,3264),(2044,3258),(2222.5,3225.5),(2277,3221)],
'n2935':[(809,3318),(932,3318),(1044.5,3304.5),(1170,3298.5),(1282,3294),(1390,3285),(1518,3279),(1635,3276),(1753,3273),(1928,3234),(2042.5,3232),(2163.5,3225.5),(2276,3199)],
'n3520':[(809,3368),(932,3355),(1042,3348),(1170,3343),(1278.5,3346.5),(1403,3333),(1507.5,3330),(1628,3328),(1752,3319),(1860,3310),(1987,3299),(2094,3293.5),(2274,3277)]}

# Corrections from individual 4x marker contact sheets (crosshair at initial reading).
P1['n294'][2]=(1094,2706)
P1['n294'][3]=(1209,2687)
P1['n294'][5]=(1443,2672.5)
P1['n294'][8]=(1792.5,2680)
P1['n294'][9]=(1911,2677)
P1['n294'][11]=(2144.5,2675)
P1['n587'][4]=(1383,2528.5)
P1['n587'][5]=(1495,2529)
P1['n587'][6]=(1616,2531)
P1['n587'][7]=(1735.5,2558.5)
P1['n2345'][7]=(1672,2029)
P1['n2345'][8]=(1784,2031)
P1['n2345'][9]=(1905.5,2027)
# No separate down-triangle outline can be established under the circle on the
# lower-panel origin frame. Omit the conjectured duplicate and document the location.
P2['n1172']=P2['n1172'][1:]

# Author-line guides read on the pixel-grid crops, independently of marker centers.
GUIDES={
'n294':[(880,2780),(960,2753),(1020,2730),(1080,2718),(1120,2700),(1200,2688),(1280,2675),(1360,2670),(1450,2670),(1540,2673),(1640,2676),(1730,2681),(1830,2680),(1950,2676),(2070,2675),(2180,2674),(2240,2672)],
'n587':[(936,2607),(1000,2578),(1080,2557),(1190,2537),(1285,2524),(1360,2519),(1440,2520),(1530,2523),(1630,2534),(1730,2548),(1810,2567),(1900,2585),(1990,2602),(2100,2610),(2180,2612),(2240,2611)],
'n1172':[(875,2613),(940,2555),(1000,2503),(1060,2465),(1110,2430),(1170,2405),(1250,2374),(1300,2355),(1360,2346),(1420,2342),(1480,2341),(1530,2341),(1600,2348),(1690,2356),(1790,2359),(1900,2359),(2020,2365),(2150,2375),(2240,2388)],
'n1760':[(925,2425),(980,2370),(1040,2318),(1100,2285),(1170,2245),(1240,2210),(1300,2187),(1380,2168),(1440,2154),(1520,2150),(1580,2151),(1650,2156),(1720,2166),(1810,2180),(1870,2188),(1960,2194),(2040,2198),(2140,2207),(2230,2221)],
'n2345':[(869,2510),(930,2440),(1000,2363),(1050,2310),(1130,2240),(1190,2185),(1250,2140),(1320,2095),(1410,2070),(1500,2045),(1610,2027),(1680,2021),(1760,2022),(1840,2028),(1880,2035),(1930,2044),(1960,2045),(2048,2034),(2110,2040),(2170,2050),(2230,2063)],
'n2935':[(920,2305),(1000,2210),(1080,2124),(1180,2040),(1280,1971),(1360,1935),(1450,1907),(1550,1884),(1660,1866),(1710,1861),(1800,1860),(1880,1867),(1930,1873),(2040,1879),(2110,1880),(2190,1878),(2240,1874)],
'n3520':[(920,2225),(980,2133),(1060,2027),(1120,1970),(1180,1918),(1240,1875),(1320,1820),(1400,1777),(1470,1760),(1530,1742),(1650,1713),(1700,1707),(1760,1695),(1810,1686),(1870,1673),(1920,1668),(2010,1668),(2070,1671),(2120,1680),(2190,1696),(2230,1704)]}

g=np.asarray(Image.open('packet/p0117.png').convert('L'))
cal={p:json.loads((OUT/f'cal-p{p}/calibration.json').read_text()) for p in (1,2)}

def row(p,s,k,u,v,bu,bv,note='',symbol=''):
    return dict(figure_id='FC-1B',panel=p,series_id=s,point_kind=k,sequence=0,pixel_u=round(u,1),pixel_v=round(v,1),u_bound_px=bu,v_bound_px=bv,symbol=symbol,note=note)

def grid_distance(p,u,v):
    return min(abs(u-(l['u_at_v0']+l['slope_du_dv']*v)) for l in cal[p]['vertical_lines'])

def markers(p,coords):
    result=[]
    for s,pts in coords.items():
        for i,(u,v) in enumerate(pts):
            notes=[];bu=bv=3
            if grid_distance(p,u,v)<18:
                bu=bv=12;notes.append('Symbol overlaps vertical grid/frame; center read from exposed sides.')
            if p==2:
                yh=cal[2]['horizontal_lines'][1]
                if abs(v-yh['v_at_u0']-yh['slope_dv_du']*u)<20:
                    bu=bv=max(bu,12);notes.append('Symbol overlaps or touches zero grid line.')
                if s in ('n294','n1172') and u<1410:
                    bu=bv=15;notes.append('Circle and down-triangle touch/overlap; identity from visible arc and triangle sides; center uncertain.')
                if s=='n1760' and i==0:
                    bu=30;bv=8;notes.append('Visible plus just left of plot frame; provisionally retained as n1760 at scanned position (negative calibrated x). Could be displaced origin symbol/reference glyph; horizontal bound reaches frame. Adjacent oval farther left is printed 0 label, not a marker.')
                if s=='n1760' and 2090<u<2120:
                    bu=bv=12;notes.append('Plus touches down-triangle above.')
                if s=='n1172' and 2090<u<2120:
                    bu=bv=12;notes.append('Down-triangle touches plus below.')
                if s=='n2935' and 1910<u<1940:
                    bu=bv=5;notes.append('Asterisk is broken into separate ink pieces.')
                if s=='n2345' and 2200<u<2250:
                    bu=bv=4;notes.append('Right side of square is interrupted; center from remaining corners.')
            else:
                if s=='n1760' and i<2:
                    bu=bv=max(bu,12);notes.append('Plus overlaps rising square-series trace.')
                if s=='n3520' and 1700<u<1760:
                    bu=bv=12;notes.append('x marker overlaps 4000-psf grid line.')
                if s=='n2935' and 1230<u<1280:
                    bu=bv=12;notes.append('Asterisk overlaps 3000-psf grid line.')
                if s=='n2345' and 1800<u<2050:
                    bu=bv=max(bu,6);notes.append('Square near doubled/interrupted drawn trace; marker center is separate from line value.')
            result.append(row(p,s,'marker',u,v,bu,bv,' '.join(notes),SYMBOL[s]))
    return result

def runs(u,v,span=35):
    lo=max(0,int(v-span)); hi=int(v+span+1)
    a=np.where(g[lo:hi,max(0,u-1):u+2].min(axis=1)<128)[0]
    if not len(a):return []
    groups=np.split(a,np.where(np.diff(a)>1)[0]+1)
    return [(lo+(x[0]+x[-1])/2,int(x[-1]-x[0]+1)) for x in groups]

def at_ink(s,u,allow_marker=False):
    a=np.array(GUIDES[s]);v=float(np.interp(u,a[:,0],a[:,1]))
    if grid_distance(1,u,v)<10:return None
    if not allow_marker and any(abs(u-mu)<23 for mu,mv in P1[s]):return None
    if s=='n2345' and 1965<u<2046:return None
    candidates=[(vv,w) for vv,w in runs(u,v) if abs(vv-v)<24 and w<38]
    if not candidates:return None
    vv,w=min(candidates,key=lambda t:abs(t[0]-v))
    # Do not let the 4000-psf horizontal grid pull the high-stress trace downward.
    if s=='n3520' and 1735<u<1880 and vv>v+8:return None
    return vv,w

def trace_point(s,u):
    a=np.array(GUIDES[s]);guess=float(np.interp(u,a[:,0],a[:,1]))
    note='';bu=1
    direct=at_ink(s,u)
    if direct:
        v,w=direct;bv=max(6,w)
    else:
        left=next(((uu,*at_ink(s,uu)) for uu in range(u-1,max(int(a[0,0])-1,u-55),-1) if at_ink(s,uu)),None)
        right=next(((uu,*at_ink(s,uu)) for uu in range(u+1,min(int(a[-1,0])+1,u+56)) if at_ink(s,uu)),None)
        if not left or not right:return None
        v=left[1]+(right[1]-left[1])*(u-left[0])/(right[0]-left[0]);bv=max(15,left[2],right[2])
        note=f'Local bridge across symbol/ink interruption; visible line flanks at u={left[0]} and {right[0]}; not an observed marker.'
    for l in cal[1]['horizontal_lines']:
        if abs(v-l['v_at_u0']-l['slope_dv_du']*u)<10:
            bv=max(bv,14);note+=' Drawn curve meets/merges with horizontal grid line.'
    if s=='n2345' and 1820<u<1970:
        bv=max(bv,24);note+=' Two ink strokes in this region; follow continuation of curved upper stroke into the square/lower segment; bound includes alternative stroke.'
    if s in ('n2345','n1760') and 900<u<1120:
        other='n1760' if s=='n2345' else 'n2345'
        q=np.array(GUIDES[other]); ov=float(np.interp(u,q[:,0],q[:,1]))
        if abs(ov-v)<30:
            bv=max(bv,24);note+=' Rising plus and square curves approach/merge; assignment follows their outgoing branches.'
    return row(1,s,'trace',u,v,bu,bv,note.strip())

rows1=markers(1,P1);rows2=markers(2,P2)
for s in SYMBOL:
    a=np.array(GUIDES[s]);start,end=int(a[0,0]),int(a[-1,0])
    # 20-pixel spacing (~3.4 thousandths); avoid tilted vertical grid columns.
    us=[]
    for u0 in range(start,end+1,20):
        u=u0;v=float(np.interp(u,a[:,0],a[:,1]))
        if grid_distance(1,u,v)<12:
            opts=[q for q in range(u0-12,u0+13) if start<=q<=end and grid_distance(1,q,float(np.interp(q,a[:,0],a[:,1])))>=12]
            if opts:u=min(opts,key=lambda q:abs(q-u0))
        if s=='n2345' and 1965<u<2046:continue
        if u not in us:us.append(u)
    # Add samples at safe edges of excluded grid columns until x gaps <=5.
    selected=set(us)|{start,end}
    def xat(u):
        v=float(np.interp(u,a[:,0],a[:,1]));return float(np.dot(cal[1]['ax'],[u,v,1]))
    previous=start
    for u in range(start+1,end+1):
        if u not in selected:continue
        if xat(u)-xat(previous)>4.95 and not (s=='n2345' and previous<2046 and u>1965):
            options=[q for q in range(previous+1,u) if grid_distance(1,q,float(np.interp(q,a[:,0],a[:,1])))>=10 and trace_point(s,q)]
            if options:selected.add(min(options,key=lambda q:abs(q-(previous+u)/2)))
        previous=u
    for u in range(start,end+1):
        if u not in selected:continue
        r=trace_point(s,u)
        if r is None and u in (start,end):
            ink=at_ink(s,u,allow_marker=True)
            if ink:r=row(1,s,'trace',u,ink[0],1,max(12,ink[1]),'Visible line close to end-symbol rim.')
        if r:rows1.append(r)
    # First/last plotted curve location includes the end marker (line stops at marker rim).
    u,v=P1[s][0];rows1.append(row(1,s,'feature',u,v,18,18,'first point; curve begins at end marker, with a small line-to-symbol gap'))
    u,v=P1[s][-1];rows1.append(row(1,s,'feature',u,v,18,18,'last point; end symbol at/near frame; line ends at symbol rim'))
    # Peak of drawn line, in calibrated y (includes page tilt), not maximum marker ordinate.
    peak=[]
    for u in range(start,end+1):
        p=at_ink(s,u)
        if p:
            v,w=p; y=np.dot(cal[1]['ay'],[u,v,1]);peak.append((y,u,v,w))
    y,u,v,w=max(peak)
    near=[q for q in peak if q[0]>=y-12 and abs(q[1]-u)<160]
    lo,hi=min(q[1] for q in near),max(q[1] for q in near)
    rows1.append(row(1,s,'feature',u,v,max(12,u-lo,hi-u),max(10,w),f'peak of drawn trace; broad/flat summit; within 12 psf of maximum over sampled visible ink u={lo}..{hi}; not peak marker'))

# Specific additional features of the author drawing, not additional observations.
rows1.append(row(1,'n2345','feature',1965,2045,6,24,'end of short lower stroke before the drawing gap; upper and lower strokes coexist upstream'))
rows1.append(row(1,'n2345','feature',2046,2033,8,12,'drawn curve resumes to right of isolated square; no continuous trace visible across u=1966..2045'))
rows1.append(row(1,'n2935','feature',2130,1880,65,12,'shallow post-peak trough / change to slight re-hardening; rounded feature, location uncertain'))
rows1.append(row(1,'n587','feature',2110,2611,55,12,'rounded transition to nearly flat residual tail; no sharp corner'))

def write(p,rows):
    ordered=[]
    for s in SYMBOL:
        source=[r for r in rows if r['series_id']==s]
        # Preserve the manually inspected forward drawing traversal. Do not sort point
        # lists by x: bucket records while walking original-image columns. This is valid
        # only because these particular drawings have no reversal or unloading loop.
        sr=[]
        for u10 in range(int(min(r['pixel_u'] for r in source)*10),int(max(r['pixel_u'] for r in source)*10)+1):
            sr.extend(r for r in source if round(r['pixel_u']*10)==u10)
        for i,r in enumerate(sr,1):r['sequence']=i
        ordered.extend(sr)
    with (OUT/f'points-p{p}.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(ordered)
    return ordered
rows1=write(1,rows1);rows2=write(2,rows2)
for p,rows in ((1,rows1),(2,rows2)):
    for s in SYMBOL:
        sub=[r for r in rows if r['series_id']==s]
        print(p,s,{k:sum(r['point_kind']==k for r in sub) for k in ['marker','trace','feature']})
