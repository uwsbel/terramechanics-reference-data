import json,numpy as np
from pathlib import Path
from PIL import Image
p=json.loads(Path('out/final-pixels.json').read_text());cfg=json.loads(Path('out/config.json').read_text())
for fig,c in cfg.items():
 g=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'));dark=g<160
 h=np.pad(np.cumsum(dark.astype(np.int16),axis=1),((0,0),(1,0)));v=np.pad(np.cumsum(dark.astype(np.int16),axis=0),((1,0),(0,0)));hm=np.zeros_like(dark);vm=np.zeros_like(dark);hm[:,30:-30]=(h[:,61:]-h[:,:-61])>43;vm[30:-30,:]=(v[61:,:]-v[:-61,:])>43;clean=dark&~hm&~vm
 for sid in ['mean','upper','lower']:
  for i,a in enumerate(p[fig][sid]['points']):
   if 'checked by eye' not in a['note'] or i in (0,10):continue
   u,v=round(a['u']),round(a['v']);ids=np.argwhere(clean[v-14:v+15,u-14:u+15]);ids=ids+np.array([v-14,u-14]);z=ids[np.argmin(np.sum((ids-np.array([v,u]))**2,axis=1))];nv,nu=map(int,z)
   lo=hi=nv
   while dark[lo-1,nu]:lo-=1
   while dark[hi+1,nu]:hi+=1
   if hi-lo<=12:nv=(hi+lo)/2;b=(hi-lo+1)/2
   else:
    lo=hi=nv
    while clean[lo-1,nu]:lo-=1
    while clean[hi+1,nu]:hi+=1
    nv=(hi+lo)/2;b=3.5
   a.update(u=nu,v=nv,bound=max(2,b));print(fig,sid,i+1,nu,nv)
Path('out/final-pixels.json').write_text(json.dumps(p,indent=2))
