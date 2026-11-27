import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image
ap=argparse.ArgumentParser(description='Measure isolated printed angle glyph bounding boxes for label-center verification.')
ap.add_argument('--run',action='store_true');a=ap.parse_args()
if a.run:
 data=json.loads(Path('out/reading.json').read_text(encoding='utf-8'))
 for fig,c in data.items():
  im=Image.open('packet/'+c['page']+'.png').convert('L')
  for sid,s in c['series'].items():
   u,v=s['label'];l=u-65;t=v-65;ink=np.asarray(im.crop((l,t,u+65,v+65)))<180
   seen=np.zeros(ink.shape,bool);stats=[]
   for yy,xx in zip(*np.where(ink)):
    if seen[yy,xx]:continue
    stack=[(yy,xx)];seen[yy,xx]=True;pixels=[]
    while stack:
     y,x=stack.pop();pixels.append((x,y))
     for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
      yn=y+dy;xn=x+dx
      if 0<=yn<130 and 0<=xn<130 and ink[yn,xn] and not seen[yn,xn]:seen[yn,xn]=True;stack.append((yn,xn))
    xs,ys=np.array(pixels).T
    if len(pixels)>8 and min(xs)>0 and max(xs)<129 and min(ys)>0 and max(ys)<129:stats.append([int(l+min(xs)),int(t+min(ys)),int(l+max(xs)),int(t+max(ys)),len(pixels)])
   print(fig,sid,stats)
