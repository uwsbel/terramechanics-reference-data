from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,csv
from pathlib import Path
for fig,p in [('FC-7B','p0136'),('FC-7C','p0137')]:
 cal=json.loads(Path(f'out/{fig}/cal-p1/calibration.json').read_text()); g=np.array(Image.open(f'packet/{p}.png').convert('L')); m=g<150
 u0,v0,u1,v1=cal['box']; m[:v0]=False;m[v1:]=False;m[:,:u0]=False;m[:,u1:]=False
 for l in cal['vertical_lines']:
  for v in range(v0,v1):
   u=round(l['u_at_v0']+l['slope_du_dv']*v);m[v,u-5:u+6]=False
 for l in cal['horizontal_lines']:
  for u in range(u0,u1):
   v=round(l['v_at_u0']+l['slope_dv_du']*u);m[v-5:v+6,u]=False
 cs=[]
 for v,u in zip(*np.where(m)):
  if not m[v,u]:continue
  stack=[(v,u)];m[v,u]=False;pts=[]
  while stack:
   y,x=stack.pop();pts.append((x,y))
   for yy in range(y-1,y+2):
    for xx in range(x-1,x+2):
     if m[yy,xx]:m[yy,xx]=False;stack.append((yy,xx))
  if len(pts)>=15:
   a=np.array(pts);cs.append([int(a[:,0].min()),int(a[:,1].min()),int(a[:,0].max()),int(a[:,1].max()),len(pts)])
 # merge nearby fragments of markers cut by grids
 changed=True
 while changed:
  changed=False
  for i in range(len(cs)):
   for j in range(i+1,len(cs)):
    a,b=cs[i],cs[j];dx=max(0,a[0]-b[2],b[0]-a[2]);dy=max(0,a[1]-b[3],b[1]-a[3])
    if dx<=12 and dy<=12 and max(a[2],b[2])-min(a[0],b[0])<55 and max(a[3],b[3])-min(a[1],b[1])<55:
     cs[i]=[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]),a[4]+b[4]];cs.pop(j);changed=True;break
   if changed:break
 cs=[c for c in cs if c[4]>=65 and c[2]-c[0]>=12 and c[3]-c[1]>=12];cs.sort(key=lambda c:(-c[1],c[0]))
 with open(f'out/{fig}/candidates.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['id','u','v','u0','v0','u1','v1','ink']);w.writerows([[i,(c[0]+c[2])/2,(c[1]+c[3])/2,*c] for i,c in enumerate(cs,1)])
 im=Image.open(f'packet/{p}.png').convert('RGB');d=ImageDraw.Draw(im);font=ImageFont.truetype('arial.ttf',22)
 for i,c in enumerate(cs,1):
  d.rectangle(c[:4],outline='red',width=1);d.text((c[2]+4,c[1]-7),str(i),fill='blue',font=font)
 im.crop((u0,v0,u1,v1)).save(f'out/{fig}/candidates.png')
 print(fig,len(cs))
