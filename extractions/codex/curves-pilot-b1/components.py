from PIL import Image
import numpy as np
from collections import deque
import csv
import sys

# List isolated ink components to check manually read symbol bounding boxes.
g=np.asarray(Image.open('packet/p0117.png').convert('L'))<128
panel=int(sys.argv[1]) if len(sys.argv)>1 else 2
u0,v0,u1,v1=(825,1630,2290,2820) if panel==1 else (770,2990,2310,3395)
b=g[v0:v1,u0:u1].copy()
rows=[]
for y,x in zip(*np.where(b)):
    if not b[y,x]: continue
    q=[(int(y),int(x))]; b[y,x]=False; pts=[]
    while q:
        yy,xx=q.pop(); pts.append((xx+u0,yy+v0))
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
            ny,nx=yy+dy,xx+dx
            if 0<=ny<b.shape[0] and 0<=nx<b.shape[1] and b[ny,nx]:
                b[ny,nx]=False; q.append((ny,nx))
    if len(pts)<20: continue
    p=np.array(pts); lo=p.min(axis=0); hi=p.max(axis=0)
    if max(hi-lo)>70: continue
    rows.append(dict(u=(lo[0]+hi[0])/2,v=(lo[1]+hi[1])/2,left=lo[0],top=lo[1],right=hi[0],bottom=hi[1],ink=len(pts)))
rows.sort(key=lambda r:(r['u'],r['v']))
with open(f'out/p{panel}-components.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
for r in rows: print(r)
