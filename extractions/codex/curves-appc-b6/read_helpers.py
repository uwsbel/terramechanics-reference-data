import argparse, csv, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'out'
PAGES={'FC-5A':'p0129.png','FC-6A':'p0131.png','FC-7A':'p0135.png'}
FIELDS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']

# Centers read from enlarged, pixel-labelled crops, before line sampling.
MARKERS={
'FC-5A': {
'dr2-13':('circle',[(1038,2779,2,2,''),(1328,2740,3,3,'horizontal grid crosses upper part of circle'),(1676,2562,2,2,''),(1931,2400,2,2,''),(2185,2250,2,2,'')]),
'dr30':('square',[(1027,2893,5,5,'line overlaps square'),(1210,2780,4,4,'line crosses square'),(1350,2709,3,3,'line crosses square'),(1549,2556,3,3,'line crosses square'),(2011,2248,3,3,'line crosses square')]),
'dr48':('triangle-down',[(1025,2864,8,6,'overlaps upright triangle and fit'),(1208,2747,7,7,'triangle base obscured by horizontal grid and fit; centroid reconstructed'),(1343,2602,5,7,'overlaps upright triangle; on 41.5-degree line rather than own 36.9-degree fit; series by shape'),(1548,2487,4,6,'fit crosses triangle'),(1905,2242,3,6,'fit crosses triangle')]),
'':('obscured angular outline',[(912,2960,14,14,'unassigned: near-origin symbol cannot be distinguished confidently between triangle-down and square; heavily overlapped by converging fits; no density guessed')]),
'dr77':('triangle-up',[(910,2929,4,6,'near-origin stack'),(1024,2840,6,6,'overlaps downward triangle'),(1201,2710,4,6,'fit overlaps edge'),(1340,2580,5,7,'overlaps downward triangle'),(1544,2395,3,6,'fit crosses triangle')])},
'FC-6A': {
'dr5-40':('triangle-up',[(973,2979,5,7,'fit crosses triangle'),(1444,2551,8,7,'overlaps circle and fit; triangle centroid reconstructed'),(1763,2208,5,7,'on middle fit; series by triangle shape'),(2027,1919,7,7,'overlaps circle and construction line; on middle fit; series by triangle shape'),(2260,1654,3,7,'')]),
'':('triangle-down',[(1787,2148,10,8,'unassigned: clearly downward triangular outline; no corresponding shape in legend; overlaps square and upper fit; cannot establish density from packet')]),
'dr19-28':('circle',[(1146,2882,2,2,''),(1442,2527,6,6,'overlaps triangle and line'),(2043,1889,5,5,'line crosses circle'),(2289,1740,2,2,'')]),
'dr103-107':('square',[(1147,2774,2,2,'on or beside upper fit; series by square shape'),(1441,2592,2,2,''),(1786,2128,9,9,'overlaps downward triangle and grid; on upper fit rather than own lower fit; series by square shape'),(2036,2097,3,3,'overlaps dashed construction'),(2288,1802,2,2,'')])},
'FC-7A': {
'dr53':('dotted circle',[(877,2856,3,3,'fit crosses dotted circle'),(985,2763,4,4,'overlaps vertical grid and fit'),(1075,2665,3,3,'fit crosses dotted circle'),(1297,2416,4,4,'overlaps vertical grid and fit'),(1522,2197,3,3,'fit crosses dotted circle'),(2300,1415,3,3,'fit crosses upper-left edge')]),
'dr100':('dotted triangle',[(877,2710,3,6,'upright dotted triangle'),(990,2612,5,6,'upright dotted triangle; overlaps vertical grid and fit'),(1079,2518,4,7,'upright dotted triangle; overlaps horizontal grid and fit'),(1297,2220,6,6,'upright dotted triangle; overlaps grid intersection and fit'),(1524,1890,4,6,'upright dotted triangle; fit beside right edge'),(2341,1055,3,6,'upright dotted triangle')])}}

def rows_markers(fig):
    rows=[]
    for sid,(sym,pts) in MARKERS[fig].items():
        for i,(u,v,bu,bv,note) in enumerate(pts,1):
            if 'SYMBOL=triangle-down;' in note:
                sym1='triangle-down'; note=note.replace('SYMBOL=triangle-down; ','')
            else: sym1=sym
            rows.append(dict(zip(FIELDS,[fig,1,sid,'marker',i,u,v,bu,bv,sym1,note])))
    return rows

def atlas(fig, rows, name, radius=30, zoom=5):
    im=Image.open(ROOT/'packet'/PAGES[fig]).convert('RGB')
    cell=2*radius*zoom; cols=4; height=cell+40
    sheet=Image.new('RGB',(cols*cell,math.ceil(len(rows)/cols)*height),'white');d=ImageDraw.Draw(sheet)
    for i,r in enumerate(rows):
        u,v=float(r['pixel_u']),float(r['pixel_v']); x=i%cols*cell; y=i//cols*height
        left,top=round(u)-radius,round(v)-radius
        patch=im.crop((left,top,left+2*radius,top+2*radius)).resize((cell,cell),Image.Resampling.NEAREST)
        dd=ImageDraw.Draw(patch); cx=(u-left)*zoom;cy=(v-top)*zoom
        dd.line((cx-12,cy,cx-5,cy),fill='red',width=2);dd.line((cx+5,cy,cx+12,cy),fill='red',width=2)
        dd.line((cx,cy-12,cx,cy-5),fill='red',width=2);dd.line((cx,cy+5,cx,cy+12),fill='red',width=2)
        sheet.paste(patch,(x,y+40));d.text((x+2,y+2),f"{r['series_id']} {r['point_kind']} {r['sequence']}",fill='black');d.text((x+2,y+18),f"({u:.1f}, {v:.1f})",fill='black')
    sheet.save(OUT/fig/name)

# Guide equations locate each author line; final samples are measured on raster ink,
# never values calculated from the printed angle. Endpoints are separately read.
GUIDES={
 'FC-5A':{'dr2-13':(-.574,3506,820,2282,[(2067,2274,'29°')]),
          'dr30':(-.661,3574.7,820,2154,[(1832,2320,'32.8°')]),
          'dr48':(-.747,3638.7,820,1968,[(1815,2235,'36.9°')]),
          'dr77':(-.889,3762.7,820,1682,[(1593,2292,'41.5°')])},
 'FC-6A':{'dr5-40':(-.996,3940.4,935,2345,[]),
          'dr19-28':(-1.01,3996,934,2254,[]),
          'dr103-107':(-.923,3884.5,994,2262,[])},
 'FC-7A':{'dr53':(-1.043,3784,668,2310,[(1718,2043,'45°')]),
          'dr100':(-1.253,3850.5,666,2310,[(1715,1764,'50.5°')])}}

EYES={
 'FC-5A':[('x',0,821,3030),('x',2000,1407,3028),('x',5000,2288,3026),('y',1000,818,2736),('y',3000,814,2147),('y',5000,811,1555)],
 'FC-6A':[('x',1000,1228,3006),('x',3000,1812,3000),('x',5000,2401,2995),('y',1000,931,2712),('y',4000,921,1829),('y',6000,915,1245)],
 'FC-7A':[('x',0,668,3163),('x',15,1606,3156),('x',30,2545,3150),('y',0,668,3163),('y',20,652,1910),('y',35,641,972)]}

def write_eye_checks(fig):
    cal=json.loads((OUT/fig/'cal-p1/calibration.json').read_text())
    im=Image.open(ROOT/'packet'/PAGES[fig]).convert('RGB')
    sheet=Image.new('RGB',(960,6*260),'white');d=ImageDraw.Draw(sheet);checks=[]
    for i,(axis,val,u,v) in enumerate(EYES[fig]):
        aa=cal['ax' if axis=='x' else 'ay']; pred=aa[0]*u+aa[1]*v+aa[2]
        error=(pred-val)/cal[axis+'_per_px']
        checks.append(dict(figure_id=fig,panel=1,axis=axis,printed_label=str(val),pixel_u_eye=u,pixel_v_eye=v,
                           fitted_value=round(pred,5),value_difference=round(pred-val,5),position_difference_px=round(error,3),
                           eye_bound_px=4,result='pass' if abs(error)<=4+cal['rms_residual_'+axis]/cal[axis+'_per_px'] else 'review',note='printed label and its grid/frame crossing read by eye; compare position difference to eye bound plus calibration RMS; original page coordinates'))
        box=(u-90,v-25,u+90,v+120) if axis=='x' else (u-230,v-45,u+30,v+45)
        patch=im.crop(box).resize((4*(box[2]-box[0]),4*(box[3]-box[1])),Image.Resampling.NEAREST)
        # Axis label strips are reduced only vertically to fit the evidence sheet.
        patch.thumbnail((720,220));sheet.paste(patch,(0,i*260+35))
        d.text((5,i*260+5),f'{axis}: printed {val}; eye tick ({u},{v}); map {pred:.4f}; error {error:.2f} px',fill='black')
    sheet.save(OUT/fig/'cal-p1/eye-label-checks.png')
    with (OUT/fig/'calibration-eye-checks.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)

def run_at(g,u,pred,search=9):
    ui=round(u);lo=round(pred)-search;hi=round(pred)+search
    ids=np.where(g[lo:hi+1,ui]<150)[0]+lo
    runs=[r for r in np.split(ids,np.where(np.diff(ids)>1)[0]+1) if len(r)>=3]
    if not runs:return None
    r=min(runs,key=lambda r:abs((r[0]+r[-1])/2-pred))
    center=float((r[0]+r[-1])/2)
    if abs(center-pred)>7:return None
    return center,len(r)

def blocked(fig,u,v,cal):
    # Avoid reading marker rims or ambiguous merges as author-line samples.
    for sid,(sym,pts) in MARKERS[fig].items():
        for mu,mv,bu,bv,n in pts:
            rad=24 if 'triangle' in sym or 'angular' in sym else 21
            if abs(u-mu)<rad and abs(v-mv)<rad:return True
    for l in cal['vertical_lines']:
        if abs(u-(l['u_at_v0']+l['slope_du_dv']*v))<5:return True
    for l in cal['horizontal_lines']:
        if abs(v-(l['v_at_u0']+l['slope_dv_du']*u))<5:return True
    return False

def traces(fig):
    cal=json.loads((OUT/fig/'cal-p1/calibration.json').read_text());aa=cal['ax']
    g=np.asarray(Image.open(ROOT/'packet'/PAGES[fig]).convert('L'));rows=[];audit=[]
    step=2 if fig=='FC-7A' else 250
    for sid,(m,b,ul,ur,labels) in GUIDES[fig].items():
        end_x=aa[0]*ur+aa[1]*(m*ur+b)+aa[2]
        targets=[None]+list(np.arange(step,end_x,step))+[None]
        for seq,target in enumerate(targets,1):
            endpoint=seq in (1,len(targets));note=''
            if endpoint:
                u=ul if seq==1 else ur
                rr=run_at(g,u,m*u+b,12)
                if not rr:
                    # A visible first/last dash can be a few pixels from the guide endpoint.
                    options=[]
                    for delta in range(-12,13):
                        rr=run_at(g,u+delta,m*(u+delta)+b,12)
                        if rr:options.append((abs(delta),u+delta,rr))
                    _,u,rr=min(options)
                v,width=rr;note='left end' if seq==1 else 'right end; peak of drawn fit'
                if fig=='FC-6A' and sid=='dr103-107' and seq==1:
                    note='left end of separately identifiable dashed ink; earlier join obscured by triangle and frame, not resolved as a trace endpoint'
            else:
                ut=(target-aa[1]*b-aa[2])/(aa[0]+aa[1]*m)
                candidates=[]
                # Snap only along this line to actual, unobscured ink; retain the nominal target in notes.
                for delta in range(-55,56):
                    u0=ut+delta
                    if not ul<u0<ur:continue
                    rr=run_at(g,u0,m*u0+b)
                    if not rr:continue
                    v0,width=rr
                    if blocked(fig,u0,v0,cal):continue
                    candidates.append((abs(delta),u0,v0,width))
                if not candidates:
                    audit.append({'series_id':sid,'target':float(target),'note':'omitted: no unobscured author-line ink within 55 pixels of nominal sample'})
                    continue
                _,u,v,width=min(candidates)
                actual=aa[0]*u+aa[1]*v+aa[2]
                if abs(actual-target)>cal['x_per_px']*1.1:
                    note=f'target {target:g}; shifted to adjacent author-line ink to avoid gap, marker, or grid merge'
                # Keep x exactly at the nominal target where no shift was necessary.
                elif abs(u-ut)<.01:
                    u=(target-aa[1]*v-aa[2])/aa[0]
            if (fig=='FC-5A' and sid=='dr2-13' and u>2195) or (fig=='FC-6A' and sid!='dr5-40' and u<1210) or (fig=='FC-7A' and u<(875 if sid=='dr53' else 850)):
                note=('dashed; '+note).rstrip('; ')
            normal_half=round(width/(2*math.sqrt(1+m*m)),2)
            # Endpoint merges use the independently observed typical line width, not the width of the frame.
            if endpoint:normal_half=4.5 if fig=='FC-5A' else (5 if fig=='FC-6A' else 3.5)
            if fig=='FC-5A' and u<950:note=(note+'; converging fits merge near origin').strip('; ')
            rows.append(dict(zip(FIELDS,[fig,1,sid,'trace',seq,round(u,2),round(v,2),normal_half,normal_half,'',note])))
        # The x=0 feature is a geometric intercept even if a dash gap or the frame hides it.
        u0=(-aa[1]*b-aa[2])/(aa[0]+aa[1]*m);v0=m*u0+b
        note='intercept'
        feature_bound=7 if fig in ('FC-5A','FC-6A') else 4
        rows.append(dict(zip(FIELDS,[fig,1,sid,'feature',1,round(u0,2),round(v0,2),feature_bound,feature_bound,'',note])))
        for j,(u,v,label) in enumerate(labels,2):
            rows.append(dict(zip(FIELDS,[fig,1,sid,'feature',j,u,v,3,3,'','label: '+label])))
    (OUT/fig/'sample-exceptions.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    return rows

def write_points(fig):
    rows=rows_markers(fig)+traces(fig)
    with (OUT/fig/'points-p1.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    rr=[r for r in rows if r['point_kind']=='trace']
    # Several smaller sheets preserve full zoom during inspection.
    for i in range(0,len(rr),24):atlas(fig,rr[i:i+24],f'trace-checks-{i//24+1}.png',radius=22,zoom=5)
    atlas(fig,rows_markers(fig),'marker-checks.png')

def notes(fig):
    from collections import Counter
    cal=json.loads((OUT/fig/'cal-p1/calibration.json').read_text())
    rr=list(csv.DictReader((OUT/fig/'points-p1.csv').open(encoding='utf-8')))
    counts=Counter((r['series_id'] or 'unassigned',r['point_kind']) for r in rr)
    common=f'''# {fig}: independent reading, panel 1

Source: packet/{PAGES[fig]}, original unrotated 300-dpi image, pixel coordinates u right / v down. Only this packet was consulted. The context page p0115.png identifies Appendix C as direct shear data from Notre Dame, with the C-5A exception.

## Calibration

All interior calibration lines are actual detected printed grid lines; none are predicted. The affine map and detected-line samples are in cal-p1/calibration.json, with 42 anchors on C-5A/C-6A and 56 on C-7A. The frame box is {cal['box']}.

RMS residual x / y: {cal['rms_residual_x']:.6f} / {cal['rms_residual_y']:.6f} native units. Maximum residual x / y: {cal['max_residual_x']:.6f} / {cal['max_residual_y']:.6f}. These are below 0.5% of the axis spans. Three printed labels per axis were checked independently against the tick/grid intersections read by eye, recorded in calibration-eye-checks.csv and shown in cal-p1/eye-label-checks.png. Position differences are compared to the 4-pixel eye bound plus the calibration RMS. C-5A's upper frame is unlabelled; its value 6000 follows the printed 1000-psf spacing, and it is not one of the three printed-label checks.

## Reading conventions

Markers were read first, from the labelled zoomed crops. Clear circle/square centers have 2-pixel bounds; overlaps are widened. Triangles use reconstructed centroids, with v bounds at least one sixth of their reconstructed height. No hidden data-sheet readings were available or used. Blank series_id means identity unresolved; it does not create a new density series.

Trace guide equations in read_helpers.py only locate the ink. Samples themselves use the center of a visible ink run, checked in trace-checks-*.png. A guide is never used to fill a dash gap. Sampling proceeds from the left ink end at nominal 250-psf intervals (2 psi on C-7A), ending at the last ink; labels and marker rims are avoided. Where the nominal abscissa falls in a dash/erasure gap, marker, or grid merge, the sample is moved to the nearest clean part of the same line, with the nominal target in its note. Thus x_native can differ from the nominal target. Bounds are half the measured stroke thickness perpendicular to the line, expressed as a conservative equal u/v radius. Endpoint bounds use the typical full stroke, rather than the thin cap or thick frame. C-5A's converging fits have fused ink near the origin, noted on affected trace rows.

The intercept features use the drawn straight line's meeting with the calibrated x=0 axis; short obscured joins or gaps are reconstructed locally, with widened feature bounds. They are geometric features, not additional test markers. First, maximum, and last line roles are carried by the endpoint trace rows; a straight rising fit has no knee. Angle-label features are at the printed text's center, not points on the fit. The native-unit CSV is generated with tools/calibrate_axes.py apply, including calibration RMS in its read bounds.

## Counts

| Series | Marker | Trace | Feature |
|---|---:|---:|---:|
'''
    for sid in MARKERS[fig]:
        ss=sid or 'unassigned'
        common+=f"| {ss} | {counts[ss,'marker']} | {counts[ss,'trace']} | {counts[ss,'feature']} |\n"
    extra={
    'FC-5A':'''\n## Legend, line labels, and ambiguities

The legend prints SS Soil; circles: gamma 95.2 to 97.6 Lb./Ft.^3, Dr .02 to .13; squares: 100, Dr .30; downward triangles: 103, Dr .48; upward triangles: 107, Dr .77. The three latter entries cite **Bendix Report No. MM-65-2**, differing from MM-66-2 in figures-rows.csv. Series IDs are retained.

The lowest fit is dr2-13, labelled **29°**; the next is dr30, **32.8°**; the next is dr48, **36.9°**; the steepest is dr77, **41.5°**. All start in the fused origin ink. The 29° line has a dashed right extension to the right frame; dashed samples are marked. Erasures at circles and vertical grid lines are not separate observations.

The downward triangle at approximately (1343,2602) overlaps an upward triangle and lies on the 41.5° fit. It remains dr48 by shape. Near (1208,2747), the downward triangle's base and fit merge with the horizontal grid; its centroid was reconstructed from the sides. At (912,2960), the surviving angular outline cannot confidently distinguish a downward triangle from a square; one wide-bound unassigned marker records it. A further square or downward triangle could be wholly hidden in that stack; no second center is supported by the surviving ink, so none is invented. The upper triangle near (910,2929) is separately visible.
''',
    'FC-6A':'''\n## Legend, line assignment, and ambiguities

The legend prints LSM Soil; upward triangles: gamma 66.8 to 75.2 Lb./Ft.^3, Dr .05 to .40; circles: 71.1 to 73, Dr .19 to .28; squares: 91 to 93.3, Dr 1.03 to 1.07. IDs are retained as given. The upper author fit is assigned to dr5-40, the middle to dr19-28, and the lower to dr103-107 from the high-load shape order and the drawn line continuations. Several individual symbols depart substantially from that order.

**No friction-angle labels are printed on this page.** There are therefore no angle-label feature rows for C-6A. This is an evidence-based exception to the requested one label per series; no angle was calculated or supplied. The numbers **3820** and **3680** label the vertical and horizontal dashed construction through the high-load group, not angles or another failure envelope. Grid/frame and these construction lines are excluded from series traces.

The square at (1786,2128) is on the upper fit; the square near (1147,2774) is also beside it. Both remain dr103-107 by shape. Upright triangles near (1763,2208) and (2027,1919) sit on the middle fit and remain dr5-40 by shape. The circle at (1442,2527) overlaps the upright triangle at (1444,2551); both centers are recorded separately with wide bounds.

The distinct downward triangle at (1787,2148), immediately below the square, has no corresponding legend shape. It is recorded with blank series_id and wide bounds, rather than guessing between density groups. There is no confidently identifiable circle in that same stack. The printed zero at approximately (894,3056), outside the lower-left frame, is an axis label, not a plotted circle.

Circle and square fits have dashed low-load extensions. The circle extension continues below the horizontal frame and is sampled where it reaches the extrapolated x=0 axis. The square's earlier low-load join is obscured by the triangle/frame: its first trace row is at the first separately identifiable dashed ink near (994,2968), explicitly not a claim to a resolved original left endpoint. Its intercept lies in the obscured/gapped join and is a geometric feature. The circle and square fits nearly coalesce at low load; their samples around 1000-1500 psf consequently share or adjoin ink. The upper fit has visible erasure gaps but is not designated dashed solely because it is interrupted.
''',
    'FC-7A':'''\n## Legend, line labels, and ambiguities

The legend prints RSM-b Soil; dotted circles: gamma 82 Lb/ft^3, Dr 0.53; dotted upright triangles: gamma 89 Lb/ft^3, Dr 1.0. IDs dr53 and dr100 are retained. The axes print **Normal Load - PSI** and **Shear Load - PSI**; the caption's Normal Shear Stress wording does not change the axis quantities.

The lower dotted-circle fit carries **45°**, not 46° (confirmed in angle-detail.png). The steeper dotted-triangle fit carries **50.5°**. Both have dashed extensions reaching the shear-load axis. The 50.5° line ends at the top frame; the last triangle is a separate marker below and to the right of that ink endpoint. The 45° fit also continues beyond the upper-left side of its last circle, ending near (2309,1377), not at that circle's center.

Central dots are visible in both symbol groups and are preserved in the symbol descriptions. Triangle points are centroids, not their dots or bounding-box midpoints. Some symbols overlap grid lines and fits, particularly the circle/triangle pair near normal load 10 psi; their bounds are widened. No additional unidentified marker was found.
'''}[fig]
    (OUT/fig/'notes.md').write_text(common+extra,encoding='utf-8')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['markers','scan','write','ends','verify']);a=ap.parse_args()
    if a.action=='verify':
        from collections import Counter
        summary={}
        for fig in PAGES:
            required=['points-p1.csv','points-p1-native.csv','calibration-eye-checks.csv','overlay-p1.png','notes.md','cal-p1/calibration.json','cal-p1/anchors.csv']
            assert all((OUT/fig/p).is_file() for p in required)
            rr=list(csv.DictReader((OUT/fig/'points-p1.csv').open(encoding='utf-8')))
            native=list(csv.DictReader((OUT/fig/'points-p1-native.csv').open(encoding='utf-8')))
            assert len(rr)==len(native)
            cal=json.loads((OUT/fig/'cal-p1/calibration.json').read_text())
            assert not any(l['source']=='predicted' for l in cal['vertical_lines']+cal['horizontal_lines'])
            eyes=list(csv.DictReader((OUT/fig/'calibration-eye-checks.csv').open(encoding='utf-8')))
            assert len(eyes)==6 and all(r['result']=='pass' for r in eyes)
            g=np.asarray(Image.open(ROOT/'packet'/PAGES[fig]).convert('L'))
            ink=[]
            for r in rr:
                if r['point_kind']=='trace':
                    u,v=round(float(r['pixel_u'])),round(float(r['pixel_v']))
                    if g[v,u]>=150:ink.append((r['series_id'],r['sequence'],u,v,int(g[v,u])))
            assert not ink,ink
            for sid in GUIDES[fig]:
                tr=[r for r in rr if r['series_id']==sid and r['point_kind']=='trace']
                assert all(float(q['pixel_u'])>float(p['pixel_u']) for p,q in zip(tr,tr[1:]))
                assert [int(r['sequence']) for r in tr]==list(range(1,len(tr)+1))
            c=Counter((r['series_id'] or 'unassigned',r['point_kind']) for r in rr)
            counts={sid or 'unassigned':{k:c[sid or 'unassigned',k] for k in ['marker','trace','feature']} for sid in MARKERS[fig]}
            summary[fig]={'counts':counts,'rms_residual_x':cal['rms_residual_x'],'rms_residual_y':cal['rms_residual_y'],
                          'eye_checks':6,'max_eye_position_difference_px':max(abs(float(r['position_difference_px'])) for r in eyes),
                          'all_trace_centers_on_dark_ink':True,'required_files_present':True}
        (OUT/'batch-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
        print(json.dumps(summary,indent=2));return
    if a.action=='ends':
        for fig in PAGES:
            g=np.asarray(Image.open(ROOT/'packet'/PAGES[fig]).convert('L'))
            print(fig)
            for sid,(m,b,ul,ur,_) in GUIDES[fig].items():
                print(sid,[(u,run_at(g,u,m*u+b,12)) for u in range(ur-5,ur+12)])
        return
    if a.action=='scan':
        for fig in PAGES:
            g=np.asarray(Image.open(ROOT/'packet'/PAGES[fig]).convert('L'))
            print(fig)
            for u in ([1100,1400,1700,2000,2300] if fig=='FC-7A' else [1000,1300,1600,1900,2200]):
                ids=np.where(g[1400:3030,u]<140)[0]+1400
                runs=np.split(ids,np.where(np.diff(ids)>1)[0]+1)
                print(u,[(int(r[0]),int(r[-1])) for r in runs if len(r)>3])
        return
    for fig in PAGES:
        if a.action=='write':
            write_eye_checks(fig);write_points(fig);notes(fig)
        else:atlas(fig,rows_markers(fig),'marker-checks.png')

if __name__=='__main__':main()
