import json,numpy as np
from PIL import Image
from pathlib import Path
p=json.loads(Path('out/proposed-pixels.json').read_text());cfg=json.loads(Path('out/config.json').read_text())
for fig,c in cfg.items():
 g=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'));print(fig)
 for s in ['upper','lower']:
  for i,a in enumerate(p[fig][s]['points']):
   if 'gap:' not in a['note']:continue
   u,v=round(a['u']),round(a['v']); lo=v
   while g[lo-1,u]<160:lo-=1
   hi=v
   while g[hi+1,u]<160:hi+=1
   print(s,i+1,(a['u'],a['v']),'rawcore',lo,hi)
