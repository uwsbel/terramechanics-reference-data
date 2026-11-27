from pathlib import Path
import ast
import json
import numpy as np
from PIL import Image, ImageDraw
src=ast.parse(Path('out/read_images.py').read_text())
META=ast.literal_eval(next(n.value for n in src.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='META' for t in n.targets)))
ALL={}
for fig,(page,pts) in META.items():
 g=np.asarray(Image.open(f'packet/{page}.png').convert('L'))
 print(fig)
 for i,(u,v) in enumerate(pts):
  a=g[v-40:v+40,u-40:u+40]>150; seen=set(); comps=[]
  for y,x in zip(*np.where(a)):
   if (y,x) in seen:continue
   stack=[(y,x)]; seen.add((y,x)); comp=[]; boundary=False
   while stack:
    yy,xx=stack.pop();comp.append((yy,xx));boundary |= yy in (0,79) or xx in (0,79)
    for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)):
     y2,x2=yy+dy,xx+dx
     if 0<=y2<80 and 0<=x2<80 and a[y2,x2] and (y2,x2) not in seen:
      seen.add((y2,x2));stack.append((y2,x2))
   if len(comp)>25 and not boundary:
    b=np.array(comp);comps.append({'n':len(comp),'box':[int(b[:,1].min()+u-40),int(b[:,0].min()+v-40),int(b[:,1].max()+u-40),int(b[:,0].max()+v-40)],'centroid':(b.mean(axis=0)[::-1]+[u-40,v-40]).round(2).tolist(),'pixels':b+np.array([v-40,u-40])})
  if fig=='FC-11B' and i==1: c=comps[-1]
  elif fig=='FC-11B' and i==2: c=comps[0]
  elif fig=='FC-11C' and i==3: c=comps[-1]
  elif fig=='FC-11C' and i==4: c=comps[0]
  else: c=min(comps,key=lambda c:sum((a-b)**2 for a,b in zip(c['centroid'],(u,v))))
  p=c['pixels']; ymin,ymax=p[:,0].min(),p[:,0].max();ls=[];rs=[]
  for yy in range(ymin+2,ymax-1):
   xx=p[p[:,0]==yy,1];l,r=int(xx.min()),int(xx.max())
   if r-l<4:continue
   la=l-1
   while g[yy,la-1]<150 and l-la<12:la-=1
   rb=r+1
   while g[yy,rb+1]<150 and rb-r<12:rb+=1
   ls.append((yy,(la+l-1)/2));rs.append((yy,(r+1+rb)/2))
  if len(ls)>=2:
   kl,bl=np.polyfit(*np.array(ls).T,1);kr,br=np.polyfit(*np.array(rs).T,1)
   ay=(br-bl)/(kl-kr);ax=kl*ay+bl
   xc=int(round(c['centroid'][0]));yb=ymax+1; ye=yb
   while g[ye+1,xc]<150 and ye-yb<12:ye+=1
   by=(yb+ye)/2
   vertices=[[ax,ay],[kl*by+bl,by],[kr*by+br,by]]
   ALL.setdefault(fig,[]).append({'sequence':i+1,'vertices':np.round(vertices,2).tolist(),'centroid':np.round(np.mean(vertices,axis=0),2).tolist()})
  for co in comps:co.pop('pixels')
  print(i+1,comps)
# Manual reconstruction after enlarged page inspection: the shared apex/base
# defeats the upper triangle's left-side automatic fit.
ALL['FC-11B'][2]['vertices']=[[1378,2906],[1361,2935],[1394,2935]]
ALL['FC-11B'][2]['centroid']=np.mean(ALL['FC-11B'][2]['vertices'],axis=0).tolist()
Path('out/triangle-fits.json').write_text(json.dumps(ALL,indent=2))
for fig,recs in ALL.items():
 page,_=META[fig];im=Image.open(f'packet/{page}.png').convert('RGB')
 sheet=Image.new('RGB',(900,((len(recs)+2)//3)*310),'white');dr=ImageDraw.Draw(sheet)
 for j,r in enumerate(recs):
  u,v=r['centroid'];box=(round(u)-40,round(v)-40,round(u)+40,round(v)+40)
  crop=im.crop(box).resize((240,240));cd=ImageDraw.Draw(crop)
  vs=[((x-box[0])*3,(y-box[1])*3) for x,y in r['vertices']]
  cd.line(vs+[vs[0]],fill='red',width=1)
  x,y=(u-box[0])*3,(v-box[1])*3;cd.line((x-8,y,x+8,y),fill='blue');cd.line((x,y-8,x,y+8),fill='blue')
  xx=j%3*300;yy=j//3*310;sheet.paste(crop,(xx,yy+40))
  dr.text((xx,yy),f'{j+1}: centroid {u:.2f},{v:.2f}',fill='black')
 sheet.save(Path('out')/fig/'triangle-fit-sheet.png')
