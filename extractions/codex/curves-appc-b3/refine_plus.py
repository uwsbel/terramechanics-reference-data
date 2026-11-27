from pathlib import Path
p=Path('out/read_curves.py');s=p.read_text();insert='''def plus_refine(im,u,v):
 rad=27;u=int(u);v=int(v);a=im[v-rad:v+rad+1,u-rad:u+rad+1]<200;seen=set();cs=[]
 for yy,xx in zip(*np.where(a)):
  if (yy,xx) in seen:continue
  stack=[(yy,xx)];seen.add((yy,xx));cc=[];border=False
  while stack:
   y,x=stack.pop();cc.append((y,x));border|=y in (0,2*rad) or x in (0,2*rad)
   for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
    ny,nx=y+dy,x+dx
    if 0<=ny<a.shape[0] and 0<=nx<a.shape[1] and a[ny,nx] and (ny,nx) not in seen:
     seen.add((ny,nx));stack.append((ny,nx))
  if border or len(cc)<30:continue
  ys,xs=zip(*cc);width=max(xs)-min(xs);height=max(ys)-min(ys)
  if width<12 or height<12:continue
  cx=(min(xs)+max(xs))/2+u-rad;cy=(min(ys)+max(ys))/2+v-rad
  if abs(cx-u)<18 and abs(cy-v)<18:cs.append((len(cc),cx,cy))
 if cs:_,u,v=max(cs)
 return u,v

'''
s=s.replace('def build(path):',insert+'def build(path):')
s=s.replace("refined.append((u,v,bound))", "if sym=='plus' and not note: u,v=plus_refine(im,u,v)\n    refined.append((u,v,bound))")
p.write_text(s)
import json
p=Path('out/FC-5B/readings.json');c=json.loads(p.read_text());d=c['series']['n4695'];d['last']=[2105,1688];d['t1'][-1]=d['last'];d=c['series']['n3815'];d['last']=[2110,1835];d['t1'][-1]=d['last'];d=c['series']['n734'];d['last']=[2127,2224];d['t1'][-1]=d['last'];p.write_text(json.dumps(c,indent=1))
