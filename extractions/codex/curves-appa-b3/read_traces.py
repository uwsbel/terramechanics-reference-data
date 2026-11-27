import sys,json,csv,numpy as np
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from reading_lib import load_maps
cfg=json.loads(Path('out/config.json').read_text());seeds=json.loads(Path('out/trace-seeds.json').read_text())
def groups(vals):
 a=np.asarray(vals);ids=np.flatnonzero(a);return [g for g in np.split(ids,np.where(np.diff(ids)>1)[0]+1) if len(g)]
result={}
for fig,c in cfg.items():
 im=Image.open('packet/'+c['page']+'.png').convert('RGB');g=np.asarray(im.convert('L'));dark=g<160
 # Long horizontal/vertical ink is grid, not support for a curve in a dash gap.
 h=np.pad(np.cumsum(dark.astype(np.int16),axis=1),((0,0),(1,0)));v=np.pad(np.cumsum(dark.astype(np.int16),axis=0),((1,0),(0,0)))
 hm=np.zeros_like(dark);vm=np.zeros_like(dark);hm[:,30:-30]=(h[:,61:]-h[:,:-61])>43;vm[30:-30,:]=(v[61:,:]-v[:-61,:])>43
 clean=dark&~hm&~vm
 cal,X,Y=load_maps(fig,c);result[fig]={};tiles=[]
 for sid in ['mean','upper','lower']:
  (u0,v0),(u1,v1)=seeds[fig][sid];m=(v1-v0)/(u1-u0);b=v0-m*u0
  def extract(m,b):
   pts=[]
   for u in range(u0+12,u1-12):
    pred=m*u+b;lo=int(round(pred))-7;col=clean[lo:lo+15,u];runs=groups(col)
    if not runs:continue
    rr=min(runs,key=lambda r:abs(lo+np.mean(r)-pred));vc=lo+float(np.mean(rr))
    if len(rr)>=2 and abs(vc-pred)<5:pts.append((u,vc))
   return np.array(pts)
  for rep in range(3):
   p=extract(m,b);res=p[:,1]-(m*p[:,0]+b);p=p[np.abs(res)<5];m,b=np.polyfit(p[:,0],p[:,1],1)
  # Fill only small grid interruptions, retaining long white dash gaps.
  vals=np.zeros(u1-u0+1,dtype=bool);centers={}
  for u in range(u0,u1+1):
   pred=m*u+b;lo=int(round(pred))-6;runs=groups(clean[lo:lo+13,u])
   if runs:
    rr=min(runs,key=lambda r:abs(lo+np.mean(r)-pred));vc=lo+float(np.mean(rr))
    if len(rr)>=2 and abs(vc-pred)<=4:vals[u-u0]=True;centers[u]=vc
  for rr in groups(~vals):
   if rr[0]>0 and rr[-1]<len(vals)-1 and len(rr)<=13:vals[rr]=True
  support=groups(vals)
  dashspans=[(u0+int(rr[0]),u0+int(rr[-1])) for rr in support if len(rr)>=12]
  pts=[]
  for i in range(11):
   target=i/10
   # Solve intersection with this reading's vertical line, keeping its own tilt.
   l=cal['vertical_lines'][i];u=(l['u_at_v0']+l['slope_du_dv']*b)/(1-l['slope_du_dv']*m)
   note=''
   if i in (0,10):
    u=max(u0,u) if i==0 else min(u1,u)
    note='first point; stroke meets plot frame' if i==0 else 'last point; stroke meets plot frame'
   elif sid!='mean':
    left=[z for z in centers if u-12<=z<=u];right=[z for z in centers if u<=z<=u+12]
    spanning=[(a,z) for a,z in dashspans if a<=u<=z] if left and right else []
    if not spanning:
     ends=[z for a,zv in dashspans for z in centers if a<=z<=zv and (z<=a+3 or z>=zv-3)];nu=min(ends,key=lambda z:abs(z-u));note=f'target Dr={target:.1f}; gap: moved {nu-u:+.2f} px to nearest dash end';u=nu
   pred=m*u+b
   # Vertical core centre, with nearby curve-only centers settling grid crossings.
   near=np.array([(a,z) for a,z in centers.items() if abs(a-u)<=7])
   if len(near)>=3:
    mv,bv=np.polyfit(near[:,0],near[:,1],1);vv=mv*u+bv
   else:vv=pred
   if 'gap:' in note: vv=centers[int(u)]
   # Local thickness away from a grid crossing; conservative rectangular half-width.
   widths=[]
   for t in range(round(u)-8,round(u)+9):
    if t not in centers:continue
    cv=centers[t];lo=round(cv)-10;runs=groups(dark[lo:lo+21,t]);rr=min(runs,key=lambda r:abs(lo+np.mean(r)-cv))
    if len(rr)<15:widths.append(len(rr))
   bound=round(float(np.median(widths))/2,2) if widths else 3.5
   bound=max(2.0,min(5.0,bound))
   pts.append(dict(u=round(float(u),2),v=round(float(vv),2),bound=bound,note=note,target=target))
  result[fig][sid]={'slope':float(m),'intercept':float(b),'dash_spans':dashspans,'points':pts}
 # 33 magnified, numbered samples, in three rows (each row a series).
 sheet=Image.new('RGB',(11*240,3*230),'white');draw=ImageDraw.Draw(sheet)
 for j,sid in enumerate(['mean','upper','lower']):
  for i,p in enumerate(result[fig][sid]['points']):
   u,v=round(p['u']),round(p['v']);box=(u-39,v-31,u+39,v+31);tile=im.crop(box).resize((234,186),Image.Resampling.NEAREST);td=ImageDraw.Draw(tile)
   for ku in range((box[0]//25+1)*25,box[2],25):td.line(((ku-box[0])*3,0,(ku-box[0])*3,186),fill=(245,160,160))
   for kv in range((box[1]//25+1)*25,box[3],25):td.line((0,(kv-box[1])*3,234,(kv-box[1])*3),fill=(170,170,245))
   px=(p['u']-box[0])*3;py=(p['v']-box[1])*3;td.ellipse((px-5,py-5,px+5,py+5),outline='red',width=2)
   sheet.paste(tile,(i*240,j*230+40));draw.text((i*240+3,j*230+2),f'{fig} {sid} {i+1} Dr {i/10:.1f}',fill='black');draw.text((i*240+3,j*230+16),f"{p['u']:.1f}, {p['v']:.1f}"+(' shifted' if 'gap:' in p['note'] else ''),fill='black')
 sheet.save('out/'+fig+'/sample-checks.png')
 print(fig,[(s,len(result[fig][s]['dash_spans']),sum('gap:' in p['note'] for p in result[fig][s]['points'])) for s in result[fig]])
Path('out/proposed-pixels.json').write_text(json.dumps(result,indent=2))

