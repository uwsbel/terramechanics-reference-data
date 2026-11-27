from pathlib import Path
import sys,json,csv
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'tools')
import calibrate_axes as ca
spec={'FC-12':('p0148.png',(584,3688),(1946,2423)), 'FC-13':('p0147.png',(712,3702),(2064,2943)), 'FC-14':('p0150.png',(637,3738),(2015,2476)), 'FC-15':('p0151.png',(688,3668),(2064,2457))}
for f,(pg,start,end) in spec.items():
 d=Path('out')/f
 cal,X,Y=ca.piecewise_maps(d/'cal-p1','packet/'+pg)
 im=Image.open('packet/'+pg).convert('RGB');g=np.asarray(im.convert('L'))
 slope=(end[1]-start[1])/(end[0]-start[0]);inter=start[1]-slope*start[0]
 rows=[]
 for target in range(500,4501,500):
  u=(target-cal['ax'][2]-cal['ax'][1]*3000)/cal['ax'][0]
  for j in range(5):
   v=inter+slope*u
   u+=(target-X.value(u,v)[0])/cal['x_per_px']
  pred=inter+slope*u
  # Read the dark diagonal in a narrow column at this sampling location.
  lo=int(pred)-15;hi=int(pred)+16
  dark=255-g[lo:hi,int(round(u))-1:int(round(u))+2].mean(axis=1)
  ii=np.where(dark>100)[0]
  if len(ii):
   # Connected run nearest predicted diagonal; no interpolation across white.
   runs=np.split(ii,np.where(np.diff(ii)>1)[0]+1)
   run=min(runs,key=lambda r:abs(np.mean(r)+lo-pred))
   v=float(lo+np.average(run,weights=dark[run]));width=len(run)
  else:v=pred;width=0
  # A fixed-stress sample can be on a vertical grid line. Locate the diagonal
  # on both sides, discarding long vertical runs, then evaluate its local center.
  local=[];widths=[]
  for uu in range(int(u)-24,int(u)+25):
   pp=inter+slope*uu;ll=int(pp)-17;hh=int(pp)+18
   ink=255-g[ll:hh,uu].astype(float)
   ids=np.where(ink>100)[0]
   if not len(ids):continue
   runs=np.split(ids,np.where(np.diff(ids)>1)[0]+1)
   rr=min(runs,key=lambda r:abs(np.mean(r)+ll-pp))
   if not 7<=len(rr)<=20:continue
   vv=ll+np.average(rr,weights=ink[rr])
   if abs(vv-pp)>9:continue
   local.append((uu,vv));widths.append(len(rr))
  arr=np.array(local);m,b=np.polyfit(arr[:,0],arr[:,1],1)
  resid=arr[:,1]-(m*arr[:,0]+b);keep=np.abs(resid)<2.5
  if keep.sum()>5:m,b=np.polyfit(arr[keep,0],arr[keep,1],1)
  v=m*u+b
  rows.append(dict(target_psf=target,pixel_u=round(u,3),pixel_v=round(v,3),vertical_ink_width=round(float(np.median(widths)),2),predicted_v=round(pred,2)))
 sheet=Image.new('RGB',(3*300,3*260),'white');dr=ImageDraw.Draw(sheet)
 for i,r in enumerate(rows):
  u,v=r['pixel_u'],r['pixel_v'];box=(int(u)-50,int(v)-35,int(u)+50,int(v)+35)
  cr=im.crop(box).resize((300,210),Image.Resampling.NEAREST);dd=ImageDraw.Draw(cr)
  for uu in range((box[0]//25+1)*25,box[2],25):dd.line(((uu-box[0])*3,0,(uu-box[0])*3,210),fill=(255,160,160));dd.text(((uu-box[0])*3,0),str(uu),fill='red')
  for vv in range((box[1]//25+1)*25,box[3],25):dd.line((0,(vv-box[1])*3,300,(vv-box[1])*3),fill=(160,160,255));dd.text((0,(vv-box[1])*3),str(vv),fill='blue')
  dd.ellipse((145,100,155,110),outline='green',width=1)
  sheet.paste(cr,(i%3*300,i//3*260+45));dr.text((i%3*300,i//3*260),f"{r['target_psf']} psf: {u:.2f},{v:.2f}\nwidth {r['vertical_ink_width']} px",fill='black')
 sheet.save(d/'trace-inspection.png')
 with (d/'trace-candidates.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 print(f,rows)
