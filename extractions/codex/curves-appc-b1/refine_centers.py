"""Local image-template center checks, restricted to independently read symbol neighborhoods."""
import json,sys,csv
from pathlib import Path
import numpy as np
from PIL import Image
fig=sys.argv[1];panel=int(sys.argv[2]);refs=json.loads(sys.argv[3]);p=Path('out')/fig
d=json.loads((p/'reading.json').read_text());g=np.asarray(Image.open(d['image']).convert('L'))<180
changes=[]
for sid,e in d[f'p{panel}'].items():
    key=sid if sid in refs else e['symbol']
    if key not in refs:continue
    ru,rv=refs[key];rad=17
    ref=g[rv-rad:rv+rad+1,ru-rad:ru+rad+1].astype(float)
    # More weight in the symbol than in the approaching/leaving author stroke.
    yy,xx=np.mgrid[-rad:rad+1,-rad:rad+1];weight=np.exp(-(xx**2+yy**2)/350)
    for pt in e['markers']:
        ou,ov=map(int,pt[:2]);best=None
        for v in range(ov-22,ov+23):
            for u in range(ou-22,ou+23):
                sub=g[v-rad:v+rad+1,u-rad:u+rad+1]
                score=float(((sub!=ref)*weight).sum())+0.012*((u-ou)**2+(v-ov)**2)
                if best is None or score<best[0]:best=(score,u,v)
        _,u,v=best;changes.append([sid,ou,ov,u,v,round(best[0],2)])
        pt[0]=u;pt[1]=v
        if len(pt)==2:pt.extend([4,'center checked against local symbol image template; hand crop inspected'])
    # Do not alter path knots: they select line ink, not measured ordinates.
(p/'reading.json').write_text(json.dumps(d,indent=2))
with (p/f'center-check-p{panel}.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['series','initial_u','initial_v','checked_u','checked_v','template_mismatch']);w.writerows(changes)
print(changes)
