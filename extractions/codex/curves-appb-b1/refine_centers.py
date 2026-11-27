import json
from pathlib import Path
from readings import DATA
from PIL import Image
import numpy as np
R={}
for j,ss in DATA.items():
 a=np.array(Image.open(f'packet/p{j+106:04}.png').convert('L'))
 for sid,S in ss.items():
  if S.get('symbol','circle')!='circle':continue
  for k,m in enumerate(S['markers']):
   if (m[2] if len(m)>2 else 2)>4:continue
   u,v=map(int,m[:2]);B=a[v-25:v+26,u-25:u+26]>200;seed=(25,25)
   if not B[seed]:continue
   seen={seed};stack=[seed]
   while stack:
    y,x=stack.pop()
    for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
     q=(y+dy,x+dx)
     if 0<=q[0]<51 and 0<=q[1]<51 and B[q] and q not in seen:seen.add(q);stack.append(q)
   P=np.array(list(seen))
   if len(P)<200 or P.min()==0 or P.max()==50:continue
   bb=(P.max(axis=0)+P.min(axis=0))[::-1]/2+[u-25,v-25];R[f'{j}/{sid}/{k}']=bb.tolist()
Path('out/center-refinements.json').write_text(json.dumps(R,indent=2))
# square/filled candidates: isolated ink bounding boxes within 45x45 neighbourhood (exclude long axis/line)
for sid in ['dr104','dr77']:
 for i,m in enumerate(DATA[7][sid]['markers']):
  u,v=map(int,m[:2]);G=a[v-23:v+24,u-23:u+24]<160;yy,xx=np.where(G)
  if min(xx)==0 or max(xx)==46 or min(yy)==0 or max(yy)==46:continue
  print(sid,i+1,m[:2],[(xx.min()+xx.max())/2+u-23,(yy.min()+yy.max())/2+v-23])
