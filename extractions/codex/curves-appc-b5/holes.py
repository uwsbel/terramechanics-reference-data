import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser(description='Locate enclosed white regions for visual inspection of hollow symbols; no series assignment.')
ap.add_argument('--run',action='store_true');a=ap.parse_args()
if a.run:
 data=json.loads(Path('out/reading.json').read_text())
 for fig,c in data.items():
  im=Image.open('packet/'+c['page']+'.png').convert('RGB');g=np.asarray(im.convert('L'))>200
  parent=[];stat=[];prev=[]
  def root(i):
   while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
   return i
  for v,row in enumerate(g):
   ids=np.flatnonzero(np.diff(np.r_[False,row,False].astype('int8')));runs=[];j=0
   for l,r in zip(ids[::2],ids[1::2]):
    while j<len(prev) and prev[j][1]<=l:j+=1
    hits=[];k=j
    while k<len(prev) and prev[k][0]<r:
     hits.append(root(prev[k][2]));k+=1
    if not hits:
     q=len(parent);parent.append(q);stat.append([l,v,r,v+1,r-l,(l+r-1)*(r-l)/2,v*(r-l)])
    else:
     q=hits[0]
     for z in set(hits[1:]):
      z=root(z);q=root(q)
      if q!=z:
       parent[z]=q;s=stat[q];t=stat[z]
       stat[q]=[min(s[0],t[0]),min(s[1],t[1]),max(s[2],t[2]),max(s[3],t[3]),s[4]+t[4],s[5]+t[5],s[6]+t[6]]
     s=stat[q];stat[q]=[min(l,s[0]),min(v,s[1]),max(r,s[2]),max(v+1,s[3]),s[4]+r-l,s[5]+(l+r-1)*(r-l)/2,s[6]+v*(r-l)]
    runs.append((l,r,q))
   prev=runs
  holes=[]
  for i,s in enumerate(stat):
   if root(i)==i and 7<=s[2]-s[0]<=35 and 7<=s[3]-s[1]<=35 and s[4]>40 and s[0]>880 and s[2]<2450 and 1450<s[1]<3300:
    holes.append([round(s[5]/s[4],1),round(s[6]/s[4],1),s[:5]])
  Path('out',fig,'holes.json').write_text(json.dumps(holes,indent=1,default=lambda x:float(x)))
  d=ImageDraw.Draw(im)
  for n,(u,v,s) in enumerate(holes):d.rectangle((u-20,v-20,u+20,v+20),outline='red',width=2);d.text((u+20,v),str(n),fill='red')
  im.crop((880,1450,2450,3300)).save(Path('out',fig,'holes.png'))
  print(fig,holes)
