import argparse,csv,json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser(description='Sample observed line-ink runs, excluding all symbol neighborhoods; creates review contact sheets.')
ap.add_argument('--run',action='store_true');a=ap.parse_args()
if not a.run:raise SystemExit()
data=json.loads(Path('out/reading.json').read_text(encoding='utf-8'))
for fig,c in data.items():
 cal=json.loads(Path('out',fig,'cal-p1/calibration.json').read_text());ax=cal['ax'];ay=cal['ay']
 im=Image.open('packet/'+c['page']+'.png').convert('RGB');g=np.asarray(im.convert('L'))
 allmarkers=[p for s in c['series'].values() for p in s['markers']]
 def native(u,v):return ax[0]*u+ax[1]*v+ax[2],ay[0]*u+ay[1]*v+ay[2]
 rows=[];review=[];exceptions=[]
 for sid,s in c['series'].items():
  for seq,p in enumerate(s['markers'],1):
   note=p[3] if len(p)>3 else '';bd=p[4] if len(p)>4 else 2
   if fig=='FC-1A' and seq==8 and sid=='dr50-57':note+=' Circle close to vertical grid and lower fit; widened for ink interference.';bd=5
   rows.append(dict(figure_id=fig,panel=1,series_id=sid,point_kind='marker',sequence=seq,pixel_u=p[0],pixel_v=p[1],u_bound_px=bd,v_bound_px=bd,symbol=p[2],note=note))
  (u0,v0),(u1,v1)=s['line'];slope=(v1-v0)/(u1-u0);intercept=v0-slope*u0
  def excluded(u,v):
   if any(abs(u-p[0])<26 and abs(v-p[1])<26 for p in allmarkers):return True
   if fig=='FC-1A':
    if any(abs(v-(line['v_at_u0']+line['slope_dv_du']*u))<8 for line in cal['horizontal_lines']):return True
    if any(abs(u-(line['u_at_v0']+line['slope_du_dv']*v))<8 for line in cal['vertical_lines']):return True
   return False
  def runat(u,end=False):
   pred=slope*u+intercept
   lo=max(0,math.floor(pred-45));hi=min(g.shape[0],math.ceil(pred+45))
   col=g[lo:hi,u]<180;edges=np.flatnonzero(np.diff(np.r_[False,col,False].astype('int8')))
   cand=[]
   for l,r in zip(edges[::2],edges[1::2]):
    v=lo+(l+r-1)/2;width=r-l
    if abs(v-pred)>(15 if fig=='FC-1A' else 25 if fig=='FC-4A' else 20):continue
    if not (2<=width<=20) or excluded(u,v):continue
    # A genuine line persists diagonally on neighboring columns. Reject text specks.
    support=0
    for du in [-3,-2,-1,1,2,3]:
     vv=round(v+slope*du)
     if 0<=u+du<g.shape[1] and g[max(0,vv-2):vv+3,u+du].min()<180:support+=1
    if support<4:continue
    cand.append((abs(v-pred),v,float(width)))
   return min(cand) if cand else None
  # Search endpoints only along their respective small neighborhoods, never extending the line model.
  left=[];right=[]
  for u in range(max(0,int(u0)-4),int(u0)+55):
   rr=runat(u)
   if rr:left.append((u,rr))
  for u in range(int(u1)-55,min(g.shape[1],int(u1)+8)):
   rr=runat(u)
   if rr:right.append((u,rr))
  if not left or not right:raise RuntimeError((fig,sid,'endpoint unreadable'))
  # Ignore a frame-only component: choose the line-facing side of the left axis.
  manual_ends={
   ('FC-1A','dr50-57'):[(946,3157,8),(1934,2152,9)],
   ('FC-1A','dr73-88'):[(928,3111,10),(1958,2011.5,11)],
   ('FC-1A','dr100-116'):[(928,3077,11),(1971,1774.5,12)],
   ('FC-2A','dr33-53'):[(951,3241,9),(2338,1658,11)],
   ('FC-2A','dr115-130'):[(950,3299,10),(2377,1824.5,13)],
   ('FC-3A','dr0-15'):[(919,3125,9),(2364,1977,10)],
   ('FC-3A','dr100-130'):[(919,3046,11),(2350,1478,10)],
   ('FC-4A','dr95'):[(923,2993,11),(2380,1053.5,12)],
   ('FC-4A','dr0'):[(923,3444,10),(2377,2088,10)]}
  (lu,lv,lw),(ru,rv,rw)=manual_ends[(fig,sid)];lr=(0,lv,lw);rr=(0,rv,rw)
  targets=[('left end',None,lu,lr)]
  xmax=native(ru,rr[1])[0]
  for x in range(250,int(xmax//250)*250+1,250):
   # Solve exact affine x target along rough line; then measure actual ink.
   ut=(x-ax[2]-ax[1]*intercept)/(ax[0]+ax[1]*slope)
   chosen=None
   for distance in range(0,51):
    trials=[round(ut)] if distance==0 else [round(ut)-distance,round(ut)+distance]
    cs=[]
    for u in trials:
     if not lu<u<ru:continue
     r=runat(u)
     if r:cs.append((r[0],u,r))
    if cs:
     _,u,r=min(cs);chosen=(u,r,distance);break
   if not chosen:
    exceptions.append(f'{sid}: target x={x} unavailable on ink within 50 pixels; omitted.');continue
   u,r,distance=chosen;targets.append(('',x,u,r))
  targets.append(('right end',None,ru,rr))
  for seq,(role,target,u,r) in enumerate(targets,1):
   _,v,width=r;note=role
   # Printed dashed extrapolations and right-hand extensions, read by region.
   dashed=(u<1105 if fig=='FC-1A' else u<1010 if fig=='FC-2A' else u<1130 if fig=='FC-3A' else u<1120 if sid=='dr95' else u<1085)
   if fig=='FC-3A' and ((sid=='dr0-15' and u>2270) or(sid=='dr100-130' and u>2285)):dashed=True
   if fig=='FC-4A' and((sid=='dr95' and u>2150) or(sid=='dr0' and u>2310)):dashed=True
   if dashed:note+='; dashed'
   if target is not None:
    xx,_=native(u,v)
    if abs(xx-target)>4:note+=f'; target x={target} psf falls in a gap/marker/grid interference; nearest visible ink at x={xx:.1f} psf'
   if fig=='FC-1A' and sid=='dr50-57' and role=='left end':note+='; axis intercept obscured by triangle; first visible dashed ink beyond symbol'
   if fig=='FC-4A' and sid=='dr95' and role=='right end':note+='; above plot frame'
   rows.append(dict(figure_id=fig,panel=1,series_id=sid,point_kind='trace',sequence=seq,pixel_u=u,pixel_v=v,u_bound_px=width/2,v_bound_px=width/2,symbol='',note=note.strip('; ')))
   review.append((sid,seq,u,v,target,note))
  # Intercepts: observed intersection when visible, otherwise explicitly bounded hidden location.
  if fig=='FC-1A':sl,il=cal['vertical_lines'][0]['slope_du_dv'],cal['vertical_lines'][0]['u_at_v0']
  else:sl,il=cal['frame_left']
  vi=(slope*il+intercept)/(1-slope*sl);ui=il+sl*vi
  if fig=='FC-1A' and sid=='dr50-57':bd=15;note='intercept; hidden by triangle and axis; location bounded from incoming dashed ink'
  else:
   # Read nearest line run just inside axis, project only its few-pixel axis overlap.
   vi=lv+slope*(ui-lu);bd=lw/2;note='intercept'
  rows.append(dict(figure_id=fig,panel=1,series_id=sid,point_kind='feature',sequence=1,pixel_u=round(ui,2),pixel_v=round(vi,2),u_bound_px=bd,v_bound_px=bd,symbol='',note=note))
  u,v=s['label'];rows.append(dict(figure_id=fig,panel=1,series_id=sid,point_kind='feature',sequence=2,pixel_u=u,pixel_v=v,u_bound_px=3,v_bound_px=3,symbol='',note='label: '+s['angle']))
 out=Path('out',fig)
 with (out/'points-p1.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 # Contact sheets cover every trace sample; pixel crosses are only a review aid.
 for batch in range((len(review)+23)//24):
  chunk=review[batch*24:(batch+1)*24];sheet=Image.new('RGB',(960,((len(chunk)+5)//6)*180),'white');draw=ImageDraw.Draw(sheet)
  for i,(sid,seq,u,v,target,note) in enumerate(chunk):
   x=i%6*160;y=i//6*180;draw.text((x,y),f'{sid} #{seq}\nx={target if target is not None else "end"} ({u},{v})',fill='black')
   crop=im.crop((u-24,round(v)-24,u+24,round(v)+24)).resize((144,144));sheet.paste(crop,(x,y+35))
   draw.line([(x+72,y+35),(x+72,y+179)],fill=(255,0,0));draw.line([(x,y+107),(x+144,y+107)],fill=(0,0,255))
  sheet.save(out/f'trace-check-{batch+1}.png')
 (out/'trace-exceptions.txt').write_text('\n'.join(exceptions))
 print(fig,len(rows),'rows;',len(review),'trace samples;',exceptions)
