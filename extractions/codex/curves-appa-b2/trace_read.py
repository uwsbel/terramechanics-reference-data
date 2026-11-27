from read_batch import *
GUIDES=json.loads((ROOT/'out/guides.json').read_text())
SIEVE=[('3/8',9.5),('3',6.3),('4',4.76),('6',3.36),('8',2.38),('10',2),('12',1.68),('16',1.19),('20',.84),('30',.595),('40',.42),('50',.297),('60',.25),('70',.21),('80',.177),('100',.149),('120',.125),('200',.074)]
def guide_at(guide,v):
 pts=np.array(guide); return float(np.interp(v,pts[:,1],pts[:,0]))
def uv_at_x(guide,X,value):
 lo,hi=guide[0][1],guide[-1][1]
 for _ in range(32):
  mid=(lo+hi)/2;u=guide_at(guide,mid)
  if X.value(u,mid)[0]>value:lo=mid
  else:hi=mid
 v=(lo+hi)/2;return guide_at(guide,v),v
def atlas(fid):
 page,box=CONFIG[fid];d=ROOT/'out'/fid;im=Image.open(ROOT/'packet'/f'{page}.png').convert('RGB');_,X,Y=ca.piecewise_maps(d/'cal-p1',ROOT/'packet'/f'{page}.png')
 rows=[]
 for label,x in SIEVE:
  guide=GUIDES[fid]['average'];u,v=uv_at_x(guide,X,x)
  if X.value(*[guide_at(guide,guide[0][1]),guide[0][1]])[0]<x*.92:continue
  if X.value(*[guide_at(guide,guide[-1][1]),guide[-1][1]])[0]>x*1.1:continue
  strips=[]
  for sid in ['upper','average','lower']:
   gg=GUIDES[fid][sid];u,v=uv_at_x(gg,X,x)
   # Pure page crops: approximate abscissa only locates the crop, never records a point.
   p=im.crop((round(u)-48,round(v)-30,round(u)+48,round(v)+30)).resize((288,180))
   dr=ImageDraw.Draw(p);dr.text((3,3),f'{sid} ~({u:.0f},{v:.0f})',fill=(255,0,0));strips.append(p)
  row=Image.new('RGB',(924,180),'white');ImageDraw.Draw(row).text((3,60),label,fill='black')
  for j,p in enumerate(strips):row.paste(p,(60+j*288,0))
  rows.append(row)
 allim=Image.new('RGB',(924,180*len(rows)),'white')
 for j,p in enumerate(rows):allim.paste(p,(0,j*180))
 allim.save(d/'marker-atlas.png')
 # Split so each figure can be visually examined without downscaling symbols.
 for j in range(0,len(rows),5):allim.crop((0,j*180,924,min(len(rows),j+5)*180)).save(d/f'marker-atlas-{j//5}.png')
def sample(g,guide,v):
 u=guide_at(guide,v);du=(guide_at(guide,v+8)-guide_at(guide,v-8))/16
 tangent=np.array([du,1.]);tangent/=np.linalg.norm(tangent);normal=np.array([tangent[1],-tangent[0]])
 # Short tangent profiles keep a crossing grid line from becoming a curve run.
 ns=np.arange(-20,20.01,.5);ts=np.arange(-4,4.01,1)
 U=u+ns[:,None]*normal[0]+ts[None,:]*tangent[0];V=v+ns[:,None]*normal[1]+ts[None,:]*tangent[1]
 prof=(g[np.rint(V).astype(int),np.rint(U).astype(int)]<150).mean(axis=1)
 ix=np.where(prof>=.66)[0];groups=np.split(ix,np.where(np.diff(ix)>1)[0]+1)
 runs=[]
 for r in groups:
  if not len(r):continue
  width=(len(r)-1)*.5+1
  if width<4:continue
  center=float(np.mean(ns[r]));runs.append((abs(center),center,width))
 if not runs:return None
 _,off,width=min(runs)
 p=np.array([u,v])+off*normal
 # Center must be actual source ink, not a grid-free interpolation.
 if g[round(p[1]),round(p[0])]>150:return None
 return p,width/2,tangent
def marker_candidates(fid):
 page,box=CONFIG[fid];d=ROOT/'out'/fid;im=Image.open(ROOT/'packet'/f'{page}.png').convert('RGB');g=np.array(im.convert('L'));_,X,Y=ca.piecewise_maps(d/'cal-p1',ROOT/'packet'/f'{page}.png');pts=[]
 theta=np.radians([a for a in range(0,360,10) if a%90 not in (0,10,80)])
 for label,x in SIEVE:
  for sid in ['upper','average','lower']:
   guide=GUIDES[fid][sid]
   if X.value(*guide[0])[0]<x*.92 or X.value(*guide[-1])[0]>x*1.12:continue
   u,v=uv_at_x(guide,X,x);vv,uu=np.meshgrid(np.arange(round(v)-18,round(v)+19),np.arange(round(u)-45,round(u)+46),indexing='ij')
   best=None
   for rad in [9,10,11,12,13,14]:
    score=np.zeros(uu.shape)
    for angle in theta:
     dark=np.zeros(uu.shape)
     for dr in [-1,0,1]:dark+=(g[np.rint(vv+(rad+dr)*np.sin(angle)).astype(int),np.rint(uu+(rad+dr)*np.cos(angle)).astype(int)]<150)
     score+=dark/3
    score/=len(theta)
    score-=.0006*(uu-u)**2+.0009*(vv-v)**2
    idx=np.unravel_index(np.argmax(score),score.shape);sc=score[idx]
    if best is None or sc>best[0]:best=(float(sc),int(uu[idx]),int(vv[idx]),rad)
   sc,mu,mv,r=best
   pts.append(dict(label=label,series_id=sid,pixel_u=mu,pixel_v=mv,radius=r,score=round(sc,3)))
 with (d/'marker-candidates.json').open('w') as f:json.dump(pts,f,indent=2)
 # Show all candidates for a visual check of symbol identity and centers.
 montage=Image.new('RGB',(900,len(SIEVE)*145),'white');draw=ImageDraw.Draw(montage)
 j=0
 for label,x in SIEVE:
  group=[p for p in pts if p['label']==label]
  if not group:continue
  for k,p in enumerate(group):
   u,v=p['pixel_u'],p['pixel_v'];crop=im.crop((u-40,v-22,u+40,v+22)).resize((240,132));dr=ImageDraw.Draw(crop);dr.line((120-10,66,120+10,66),fill='red');dr.line((120,56,120,76),fill='red');dr.text((1,1),f"{p['series_id']} ({u},{v}) {p['score']}",fill='red');montage.paste(crop,(100+k*260,j*145))
  draw.text((1,j*145+60),label,fill='black');j+=1
 montage=montage.crop((0,0,900,j*145));montage.save(d/'marker-candidates.png')
 for i in range(0,j,5):montage.crop((0,i*145,900,min(j,i+5)*145)).save(d/f'marker-candidates-{i//5}.png')
if __name__=='__main__':
 if sys.argv[1]=='atlas':
  for fid in CONFIG:atlas(fid)
 if sys.argv[1]=='guides':
  for fid in CONFIG:
   im=Image.open(ROOT/'packet'/f'{CONFIG[fid][0]}.png').convert('RGB');dr=ImageDraw.Draw(im)
   for sid,col in [('average','red'),('upper','green'),('lower','blue')]:dr.line([tuple(p) for p in GUIDES[fid][sid]],fill=col,width=3)
   b=CONFIG[fid][1];im.crop((b[0]-20,b[1]-100,b[2]+20,b[3])).save(ROOT/'out'/fid/'guides-overlay.png')
 if sys.argv[1]=='markers':
  for fid in CONFIG:marker_candidates(fid)
