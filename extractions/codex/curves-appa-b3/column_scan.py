import json,numpy as np
from PIL import Image
from pathlib import Path
p=json.loads(Path('out/proposed-pixels.json').read_text());cfg=json.loads(Path('out/config.json').read_text())
for fig,c in cfg.items():
 g=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'))
 print('\n',fig)
 for side in ['left','right']:
  ps=[p[fig][s]['points'][0 if side=='left' else -1] for s in ['upper','mean','lower']];u=round(np.mean([a['u'] for a in ps]))+(12 if side=='left' else -12);lo=round(min(a['v'] for a in ps))-25;hi=round(max(a['v'] for a in ps))+25;ids=np.flatnonzero(g[lo:hi,u]<160);rr=[r+lo for r in np.split(ids,np.where(np.diff(ids)>1)[0]+1) if len(r)];print(side,u,[(float(np.mean(r)),len(r)) for r in rr])
 print('fit end',[(s,p[fig][s]['points'][0]['v'],p[fig][s]['points'][-1]['v']) for s in ['upper','mean','lower']])
