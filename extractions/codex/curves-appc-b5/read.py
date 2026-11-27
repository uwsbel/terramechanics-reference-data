import argparse,csv,json,sys,importlib.util
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ap=argparse.ArgumentParser(description='Independent tick calibration and packet marker/trace inspection.')
ap.add_argument('command',choices=['ticks','atlas'])
a=ap.parse_args()
spec=importlib.util.spec_from_file_location('calibrate', 'tools/calibrate_axes.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
configs={
'FC-2A':dict(page='p0120',box=[945,1465,2435,3395],xt=[(949,3348),(1249,3355),(1525,3361),(1814,3366),(2114,3370),(2408,3375)],yt=[(949,3348),(952,3067),(955,2765),(959,2480),(963,2188),(966,1881),(969,1605)]),
'FC-3A':dict(page='p0123',box=[910,1450,2385,3215],xt=[(919,3198),(1210,3199),(1498,3200),(1790,3202),(2083,3203),(2370,3205)],yt=[(919,3198),(918,2903),(917,2612),(916,2314),(915,2030),(915,1733),(914,1454)]),
'FC-4A':dict(page='p0126',box=[915,1155,2385,3490],xt=[(922,3480),(1213,3482),(1510,3484),(1795,3485),(2087,3487),(2374,3489)],yt=[(922,3480),(922,3187),(922,2898),(921,2607),(921,2315),(921,2024),(920,1730),(920,1441),(920,1164)])}
if a.command=='ticks':
    for fig,c in configs.items():
        g=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'))
        anchors=[]; xt=[];yt=[]
        # Independently measure the frame tilt from clean, short stretches.
        leftsamples=[];bottomsamples=[]
        for u,v in c['yt'][1:-1]:
            vv=v+60
            prof=(g[vv-8:vv+9,u-15:u+16]<180).sum(axis=0)
            ids=np.flatnonzero(prof>=prof.max()*.8)
            leftsamples.append((vv,u-15+float(np.mean(ids))))
        for u,v in c['xt'][1:-1]:
            uu=u+50
            prof=(g[v-18:v+19,uu-8:uu+9]<180).sum(axis=1)
            ids=np.flatnonzero(prof>=prof.max()*.8)
            bottomsamples.append((uu,v-18+float(np.mean(ids))))
        sl,il=np.polyfit(*np.array(leftsamples).T,1)
        sb,ib=np.polyfit(*np.array(bottomsamples).T,1)
        corneru=(il+sl*ib)/(1-sl*sb);cornerv=ib+sb*corneru
        # Measure tick positions from ink extending outside the axis, excluding digits.
        for i,(u,v) in enumerate(c['xt']):
            if i==0: uu=corneru;v=cornerv
            elif i==len(c['xt'])-1:
                prof=(g[v-100:v-50,u-20:u+21]<180).sum(axis=0)
                ids=np.flatnonzero(prof>=prof.max()*.8)
                uu=u-20+float(np.mean(ids));v=ib+sb*uu
            else:
                vals=(g[v+8:v+21,u-15:u+16]<180).sum(axis=0)
                ids=np.flatnonzero(vals>=max(3,vals.max()*.6))
                uu=u-15+float(np.mean(ids))
                v=ib+sb*uu
            xt.append((uu,v));anchors.append(dict(x_value=i*1000,y_value=0,u=uu,v=v,x_source='measured axis tick',y_source='bottom axis'))
        for i,(u,v) in enumerate(c['yt']):
            if i==0: vv=cornerv;u=corneru
            elif fig=='FC-4A' and i==8:
                # Top frame itself; no separate outward tick.
                continue
            else:
                vals=(g[v-30:v+31,u-24:u-8]<180).sum(axis=1)
                ids=np.flatnonzero(vals>=max(3,vals.max()*.6))
                vv=v-30+float(np.mean(ids));u=il+sl*vv
            yt.append((u,vv));anchors.append(dict(x_value=0,y_value=i*1000,u=u,v=vv,x_source='left axis',y_source='measured axis tick'))
        ax,ay,rx,ry,mx,my=mod.fit_affine(anchors)
        out=Path('out')/fig/'cal-p1';out.mkdir(parents=True,exist_ok=True)
        with (out/'anchors.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(anchors[0]));w.writeheader();w.writerows(anchors)
        cal=dict(image='packet/'+c['page']+'.png',box=c['box'],model='affine least squares on measured axis tick intersections; no interior grid exists',ax=ax,ay=ay,x_per_px=float(np.hypot(*ax[:2])),y_per_px=float(np.hypot(*ay[:2])),rms_residual_x=rx,rms_residual_y=ry,max_residual_x=mx,max_residual_y=my,n_anchors=len(anchors),vertical_lines=[],horizontal_lines=[],axis_ticks_x=xt,axis_ticks_y=yt,frame_left=[sl,il],frame_bottom=[sb,ib],source='independent measurement of packet ink; rejected grid detect trial; no predicted interior lines used')
        (out/'calibration.json').write_text(json.dumps(cal,indent=2))
        print(fig,'xt',xt,'yt',yt,'RMS',rx,ry)
elif a.command=='atlas':
    data=json.loads(Path('out/reading.json').read_text(encoding='utf-8'))
    for fig,c in data.items():
        im=Image.open('packet/'+c['page']+'.png').convert('RGB')
        pts=[(sid,p) for sid,s in c['series'].items() for p in s['markers']]
        width=800;height=((len(pts)+3)//4)*235
        atlas=Image.new('RGB',(width,height),'white');d=ImageDraw.Draw(atlas)
        for i,(sid,p) in enumerate(pts):
            u,v=p[:2]; x=(i%4)*200;y=(i//4)*235
            atlas.paste(im.crop((u-30,v-30,u+30,v+30)).resize((180,180)),(x,y+45))
            d.text((x,y),f'{i+1} {sid}\n({u},{v})',fill='black')
            d.line([(x+90,y+45),(x+90,y+225)],fill='red');d.line([(x,y+135),(x+180,y+135)],fill='blue')
        atlas.save(Path('out')/fig/'marker-atlas.png')
