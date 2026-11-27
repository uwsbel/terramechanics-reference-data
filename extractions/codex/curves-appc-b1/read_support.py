"""Reader's pixel observations and ink-supported trace extraction; no outside readings."""
import csv,json,sys,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
COLS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
def runs(a):
    ii=np.where(a)[0]
    if len(ii)==0:return []
    chunks=np.split(ii,np.where(np.diff(ii)>1)[0]+1)
    return [(float((c[0]+c[-1])/2),int(len(c))) for c in chunks]
def execute(fig):
    dest=ROOT/'out'/fig
    data=json.loads((dest/'reading.json').read_text())
    gray=np.asarray(Image.open(ROOT/data['image']).convert('L'))
    summary={}
    for panel in [1,2]:
        cal=json.loads((dest/f'cal-p{panel}'/'calibration.json').read_text())
        rows=[]
        def add(sid,kind,u,v,bu,bv,symbol,note):
            seq=1+sum(r['series_id']==sid and r['point_kind']==kind for r in rows)
            rows.append(dict(zip(COLS,[fig,panel,sid,kind,seq,round(u,2),round(v,2),bu,bv,symbol,note])))
        for sid,entry in data[f'p{panel}'].items():
            symbol=entry['symbol']
            for pt in entry['markers']:
                u,v=pt[:2];bu=bv=2;note=''
                if len(pt)>2:bu=bv=pt[2];note=pt[3]
                # Mark proximity to each independently fitted grid line.
                near=[]
                for l in cal['vertical_lines']:
                    if abs(u-(l['u_at_v0']+l['slope_du_dv']*v))<11:near.append('vertical grid')
                for l in cal['horizontal_lines']:
                    if abs(v-(l['v_at_u0']+l['slope_dv_du']*u))<11:near.append('horizontal grid')
                if near:bu=max(bu,5);bv=max(bv,5);note=('; '.join(filter(None,[note,'symbol intersects '+', '.join(near)])))
                add(sid,'marker',u,v,bu,bv,symbol,note)
            if 'path' not in entry:continue
            for prefix in entry.get('prefix',[]):
                add(sid,'trace',prefix[0],prefix[1],prefix[2],prefix[3],'','by-eye initial bend; drawing order preserved')
            path=np.array(entry['path'],float)
            # x order follows drawing order; all these inspected curves are monotone in x.
            trace=[];miss=[]
            for target in np.arange(path[0,0],path[-1,0]+.1,12):
                candidates=[]
                for u in sorted(range(int(target)-6,int(target)+7),key=lambda u:abs(u-target)):
                    if u<path[0,0] or u>path[-1,0]:continue
                    expected=float(np.interp(u,path[:,0],path[:,1]))
                    if any(abs(u-(l['u_at_v0']+l['slope_du_dv']*expected))<6 for l in cal['vertical_lines']):continue
                    search=entry.get('search',40)
                    lo=max(0,int(expected)-search-20);hi=min(gray.shape[0],int(expected)+search+21)
                    for v,w in runs(gray[lo:hi,u]<200):
                        v+=lo
                        if v-w/2<=lo or v+w/2>=hi-1:continue
                        if abs(v-expected)>search:continue
                        if w>32:continue
                        shared_grid=any(abs(v-(l['v_at_u0']+l['slope_dv_du']*u))<5 for l in cal['horizontal_lines'])
                        if shared_grid and abs(v-expected)>8:continue
                        shared_symbol=any(abs(u-p[0])<16 and abs(v-p[1])<22 for p in entry['markers'])
                        candidates.append((abs(u-target)*.7+abs(v-expected),u,v,w,shared_grid,shared_symbol))
                if candidates:
                    _,u,v,w,shared_grid,shared_symbol=min(candidates)
                    if trace and u<=trace[-1][0]:continue
                    trace.append((u,v,w))
                    note='visible author-line ink; column displaced from vertical grid'
                    vb=max(1,w/2)
                    if shared_grid:note+='; curve/horizontal-grid shared ink; ordinate uncertain';vb=max(vb,8)
                    if shared_symbol:note+='; curve/marker shared ink; ordinate uncertain';vb=max(vb,16)
                    add(sid,'trace',u,v,1,vb,'',note)
                else:miss.append(float(target))
            for f in entry['features']:
                u,v,label=f[:3];b=f[3] if len(f)>3 else 3
                add(sid,'feature',u,v,b,b,'',label)
            (dest/f'trace-gaps-p{panel}-{sid}.json').write_text(json.dumps(miss))
        with (dest/f'points-p{panel}.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,COLS,lineterminator='\n');w.writeheader();w.writerows(rows)
        subprocess.run([sys.executable,str(ROOT/'tools/calibrate_axes.py'),'apply',str(dest/f'cal-p{panel}/calibration.json'),str(dest/f'points-p{panel}.csv'),str(dest/f'points-p{panel}-native.csv')],check=True)
        subprocess.run([sys.executable,str(ROOT/'tools/plot_grid.py'),'overlay',str(ROOT/data['image']),'--points',str(dest/f'points-p{panel}.csv'),'--out',str(dest/f'overlay-p{panel}.png')],check=True)
        summary[f'p{panel}']={s:{k:sum(r['series_id']==s and r['point_kind']==k for r in rows) for k in ['marker','trace','feature']} for s in data[f'p{panel}']}
    (dest/'counts.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':execute(sys.argv[1])
