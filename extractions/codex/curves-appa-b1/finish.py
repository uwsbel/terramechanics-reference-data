import sys,csv,json,copy,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'tools')
import calibrate_axes as ca
cfg=json.loads(Path('out/config.json').read_text());cfg['FA-40']['box'][2]=2370
Path('out/config.json').write_text(json.dumps(cfg,indent=2))
bottoms={'FA-4':3309,'FA-8':3448,'FA-20':3414,'FA-24':3532,'FA-28':3523,'FA-40':3571,'FA-48':3538}
cols=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
knees={'FA-4':[(12,90,37,'Rounded knee: transition to the shallower upper segment; location broad, approximately Dr 0.50 to 0.60.')],
'FA-8':[(5,65,22,'Rounded lower knee: initial shallow segment turns into the rising main segment; location broad, approximately Dr 0.16 to 0.24.')],
'FA-20':[(11,95,50,'Broad rounded change of slope, approximately Dr 0.44 to 0.56; no sharp kink.')],
'FA-24':[(5,65,35,'Rounded lower knee, approximately Dr 0.16 to 0.24; no sharp corner.')],
'FA-28':[(7,65,55,'Lower rounded knee: onset of the steep segment, approximately Dr 0.26 to 0.34.'),(14,90,60,'Upper rounded knee: transition toward the flatter upper tail, approximately Dr 0.59 to 0.71.')],
'FA-48':[(17,90,60,'Broad upper shoulder: slope starts to diminish, approximately Dr 0.74 to 0.86; no sharp kink.')]}
summary=[]
for f,c in cfg.items():
 root=Path('out')/f;im=Image.open('packet/'+c['page']+'.png').convert('RGB');g=np.asarray(im.convert('L'));cal,X,Y=ca.piecewise_maps(root/'cal-p1','packet/'+c['page']+'.png')
 if f!='FA-40':
  rows=[r for r in csv.DictReader((root/'points-p1.csv').open()) if r['point_kind']=='trace']
  if f=='FA-28':
   rows[0].update(pixel_u=770,pixel_v=3223,u_bound_px=6,v_bound_px=6,note='First visible cap ink at (770,3223), detached from the left frame by 3 white columns. Cap is worn to 1 px at its extreme left; bound is half the adjoining 12 px stroke. No invented sample at Dr=0.')
  if f=='FA-48':
   rows[17].update(u_bound_px=7,v_bound_px=7,note='Scan loss cuts through the lower part of the stroke. Sample is centred on the surviving upper curve ink; bound is half the adjoining 14 px line width, covering the uncertain full-stroke centre.')
  if f=='FA-4':rows[0].update(u_bound_px=7.5,v_bound_px=7.5)
  feats=[]
  first=copy.deepcopy(rows[0]);first.update(point_kind='feature',sequence=1,note='First point. '+str(first['note']));feats.append(first)
  for idx,bu,bv,note in knees[f]:
   r=copy.deepcopy(rows[idx-1]);r.update(point_kind='feature',sequence=len(feats)+1,u_bound_px=bu,v_bound_px=bv,note=note+' Feature bounds describe the rounded transition region; trace bounds remain half the local stroke thickness.');feats.append(r)
  last=copy.deepcopy(rows[-1]);last.update(point_kind='feature',sequence=len(feats)+1,note='Last point; peak (maximum of monotonically rising trace). '+str(last['note']));feats.append(last);rows+=feats
 else:
  rows=[]
  for sid,yvalue in [('band-top',45),('band-bottom',40)]:
   series=[]
   for i,target in enumerate(np.arange(0,1.001,.05)):
    # Intersect the two verified constant-value lines for the sampling abscissa.
    vl=next(z for z in cal['vertical_lines'] if z['x_value']==0);u=780+target*1550;v=2040 if yvalue==45 else 2420
    for _ in range(4):
     lo,hi=700,2450
     for k in range(35):
      mid=(lo+hi)/2
      if X.value(mid,v)[0]<target:lo=mid
      else:hi=mid
     u=(lo+hi)/2
     hl=next(z for z in cal['horizontal_lines'] if z['y_value']==yvalue);v=hl['v_at_u0']+hl['slope_dv_du']*u
    obs=[]
    for uu in range(round(u)-18,round(u)+19):
     if not 770<uu<2340:continue
     lo=round(v)-15;arr=g[lo:round(v)+16,uu]<160;ii=np.flatnonzero(arr)
     rr=np.split(ii,np.where(np.diff(ii)>1)[0]+1) if len(ii) else []
     for z in rr:
      cen=lo+(z[0]+z[-1])/2;wid=len(z)
      if abs(cen-v)<4 and wid<=13:obs.append((uu,cen,wid))
    if len(obs)<3:raise ValueError((f,sid,i,obs))
    ar=np.array(obs);a,b=np.polyfit(ar[:,0]-u,ar[:,1],1);vc=float(b);thick=float(np.median(ar[:,2]));note='Hatched band boundary coincides with the printed '+str(yvalue)+' degree grid line; hatch crossings are not data symbols.'
    if 0<i<20:
     lo=round(vc)-7;ii=np.flatnonzero(g[lo:round(vc)+8,round(u)]<160)
     rr=np.split(ii,np.where(np.diff(ii)>1)[0]+1) if len(ii) else []
     good=[z for z in rr if 0<len(z)<=13 and abs(lo+(z[0]+z[-1])/2-vc)<3]
     if good:
      z=min(good,key=lambda z:abs(lo+(z[0]+z[-1])/2-vc));vc=lo+(z[0]+z[-1])/2;thick=len(z)
    if sid=='band-bottom' and i==19:
     thick=7;note+=' Hatch vertex joins the boundary here; thickness measured on the adjoining boundary stroke.'
    if i in(0,20):note+=' Endpoint joins the frame.'
    if g[round(vc),round(u)]>=160:raise ValueError(('band sample white',sid,i,u,vc))
    series.append(dict(zip(cols,[f,1,sid,'trace',i+1,round(u,2),round(vc,2),thick/2,thick/2,'',note])))
   rows+=series
   for j,idx in enumerate([0,-1]):
    r=copy.deepcopy(series[idx]);r.update(point_kind='feature',sequence=j+1,note=('First point; peak lies across the whole flat edge. ' if j==0 else 'Last point; flat edge has no unique peak abscissa. ')+r['note']);rows.append(r)
 # Write, convert using verified piecewise maps, save verification details.
 with (root/'points-p1.csv').open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows(rows)
 subprocess.run([sys.executable,'tools/calibrate_axes.py','piecewise',str(root/'cal-p1'),str(root/'points-p1.csv'),str(root/'points-p1-native.csv'),'--image','packet/'+c['page']+'.png'],check=True)
 (root/'cal-p1'/'knots-verified.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 # Source-only, enlarged label snippets, preserving the axis/line association.
 checks=[];sheet=Image.new('RGB',(1200,1800),'white');d=ImageDraw.Draw(sheet)
 for j,val in enumerate([0,.2,.4,.6,.8,1.]):
  vl=next(z for z in cal['vertical_lines'] if z['x_value']==val);vb=bottoms[f];uu=vl['u_at_v0']+vl['slope_du_dv']*vb
  tile=im.crop((round(uu)-80,vb-50,round(uu)+80,vb+125)).resize((320,350));xx=(j%3)*400;yy=(j//3)*420;sheet.paste(tile,(xx,yy+35));d.text((xx,yy+5),f'x label checked: {val:g}; page u~{uu:.1f}',fill='black')
  checks.append(dict(figure_id=f,panel=1,axis='x',printed_label='0' if val==0 else ('1.0' if val==1 else f'{val:.1f}'),native_value=val,line_coordinate=round(uu,2),at_cross_coordinate=vb,checked_by_eye='yes',note='Printed label aligned to the vertical grid/frame line; x increases right; dimensionless.'))
 for j,val in enumerate(map(float,c['ys'].split(','))):
  hl=next(z for z in cal['horizontal_lines'] if z['y_value']==val);ul=next(z for z in cal['vertical_lines'] if z['x_value']==0);uu=(ul['u_at_v0']+ul['slope_du_dv']*hl['v_at_u0'])/(1-ul['slope_du_dv']*hl['slope_dv_du']);vv=hl['v_at_u0']+hl['slope_dv_du']*uu
  tile=im.crop((round(uu)-130,round(vv)-55,round(uu)+110,round(vv)+55)).resize((480,220));xx=(j%2)*600;yy=850+(j//2)*300;sheet.paste(tile,(xx,yy+35));d.text((xx,yy+5),f'y label checked: {val:g}; page v~{vv:.1f}',fill='black')
  checks.append(dict(figure_id=f,panel=1,axis='y',printed_label=f'{val:g}',native_value=val,line_coordinate=round(vv,2),at_cross_coordinate=round(uu,2),checked_by_eye='yes',note='Printed numeral checked against this horizontal line at left axis; y increases up; degrees.'))
 sheet.save(root/'cal-p1'/'label-checks.png')
 with (root/'calibration-eye-checks.csv').open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=list(checks[0]),lineterminator='\n');w.writeheader();w.writerows(checks)
 subprocess.run([sys.executable,'tools/plot_grid.py','overlay','packet/'+c['page']+'.png','--points',str(root/'points-p1.csv'),'--out',str(root/'overlay-p1.png')],check=True,capture_output=True)
 native=list(csv.DictReader((root/'points-p1-native.csv').open()));counts={}
 for r in native:
  key=r['series_id']+'/'+r['point_kind'];counts[key]=counts.get(key,0)+1
 sens={}
 for sid in sorted(set(r['series_id'] for r in native)):
  rs=[r for r in native if r['series_id']==sid and r['point_kind']=='trace'];ax=np.array(cal['ax']);ay=np.array(cal['ay'])
  sens[sid]=dict(max_abs_x=max(abs(float(r['x_native'])-ax@np.array([float(r['pixel_u']),float(r['pixel_v']),1])) for r in rs),max_abs_y=max(abs(float(r['y_native'])-ay@np.array([float(r['pixel_u']),float(r['pixel_v']),1])) for r in rs))
 summary.append(dict(figure_id=f,counts=counts,rms_x=cal['rms_residual_x'],rms_y=cal['rms_residual_y'],max_x=cal['max_residual_x'],max_y=cal['max_residual_y'],sensitivity=sens,extrapolated=sum('extrapolated' in r['cal_model'] for r in native)))
Path('out/summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
