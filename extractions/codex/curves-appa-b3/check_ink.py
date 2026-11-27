import json,numpy as np
from PIL import Image
from pathlib import Path
p=json.loads(Path('out/proposed-pixels.json').read_text());cfg=json.loads(Path('out/config.json').read_text())
for fig,c in cfg.items():
 g=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L')); bad=[]
 for s in ['mean','upper','lower']:
  for i,a in enumerate(p[fig][s]['points']):
   u,v=round(a['u']),round(a['v'])
   if g[v,u]>160:bad.append((s,i+1,a['u'],a['v'],int(g[v,u])))
 print(fig,'white centers',bad)
