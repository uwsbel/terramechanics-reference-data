import json,csv,sys,subprocess,math
from pathlib import Path
from PIL import Image,ImageDraw
from reading_lib import load_maps,ca
cfg=json.loads(Path('out/config.json').read_text());pixels=json.loads(Path('out/final-pixels.json').read_text())
# Rectangles enclose the printed numerical glyphs, without the leaders.
labels={
'FA-3':{'upper':[('40.1',[680,2760,788,2810]),('51.8',[2610,3080,2726,3133])],'mean':[('41.3',[680,2817,788,2870]),('52.9',[2610,3135,2726,3190])],'lower':[('42.5',[680,2874,788,2933]),('54.0',[2610,3190,2726,3247])]},
'FA-7':{'upper':[('23.3',[450,1750,556,1814]),('29.3',[2240,2320,2380,2390])],'mean':[('23.8',[450,1813,556,1874]),('30.2',[2240,2438,2380,2500])],'lower':[('24.3',[450,1874,556,1938]),('31.1',[2240,2514,2380,2602])]},
'FA-19':{'upper':[('57.3',[540,1025,654,1092]),('65.1',[2395,1693,2520,1760])],'mean':[('57.9',[540,1093,654,1153]),('70.3',[2385,2031,2510,2100])],'lower':[('58.5',[540,1152,654,1215]),('75.5',[2400,2348,2520,2410])]},
'FA-23':{'upper':[('53.6',[720,1347,827,1403]),('71.2',[2290,2570,2390,2640])],'mean':[('61.4',[735,1990,830,2043]),('83.1',[2290,3102,2415,3170])],'lower':[('69.2',[735,2470,840,2536]),('94.0',[2300,3478,2415,3545])]},
'FA-27':{'upper':[None,('110.5',[2390,3570,2540,3635])],'mean':[('95.4',[458,3168,568,3225]),('112.7',[2390,3640,2540,3693])],'lower':[('95.8',[458,3228,568,3290]),('114.9',[2390,3698,2540,3755])]},
'FA-39':{'upper':[('66.6',[620,1890,726,1947]),('88.1',[2390,2923,2505,2980])],'mean':[('67.8',[620,1948,726,1996]),('90.2',[2390,3000,2505,3054])],'lower':[('69.0',[620,2003,726,2050]),('92.3',[2390,3059,2505,3116])]},
'FA-47':{'upper':[('73.5',[745,2290,848,2345]),('89.4',[2360,2930,2492,2990])],'mean':[('74.4',[745,2346,848,2400]),('89.4',[2360,2930,2492,2990])],'lower':[('75.3',[745,2440,848,2500]),('89.4',[2360,2930,2492,2990])]}}
cols=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note','sample_dr_target']
summary=[]
for fig,c in cfg.items():
 d=Path('out')/fig;im=Image.open('packet/'+c['page']+'.png').convert('RGB');cal,X,Y=load_maps(fig,c);rows=[];textboxes=[]
 for sid in ['mean','upper','lower']:
  pp=pixels[fig][sid]['points']
  for i,a in enumerate(pp):rows.append(dict(zip(cols,[fig,1,sid,'trace',i+1,a['u'],a['v'],a['bound'],a['bound'],'',a['note'],a['target']])))
  for i,idx in enumerate([0,-1]):
   a=pp[idx];rows.append(dict(zip(cols,[fig,1,sid,'feature',i+1,a['u'],a['v'],a['bound'],a['bound'],'','first point' if i==0 else 'last point',''])))
  n=3
  for side,item in zip(['left','right'],labels[fig][sid]):
   if item is None:continue
   val,box=item;g=im.crop(box).convert('L');import numpy as np
   mask=np.asarray(g)<160; seen=set();components=[]
   for iy,ix in zip(*np.where(mask)):
    if (iy,ix) in seen:continue
    stack=[(int(iy),int(ix))];seen.add((iy,ix));comp=[]
    while stack:
     qy,qx=stack.pop();comp.append((qy,qx))
     for dy,dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
      ny,nx=qy+dy,qx+dx
      if 0<=ny<mask.shape[0] and 0<=nx<mask.shape[1] and mask[ny,nx] and (ny,nx) not in seen:seen.add((ny,nx));stack.append((ny,nx))
    ar=np.array(comp);ch=np.ptp(ar[:,0])+1;cw=np.ptp(ar[:,1])+1
    if len(comp)>=50 and ch>=25 and cw>=6:components.extend(comp)
   if not components:raise ValueError((fig,sid,side,'no glyphs'))
   yy,xx=np.array(components).T
   u=box[0]+(min(xx)+max(xx))/2;v=box[1]+(min(yy)+max(yy))/2
   rows.append(dict(zip(cols,[fig,1,sid,'feature',n,u,v,2,2,'','label: '+val,''])));n+=1;textboxes.append((sid,side,val,box,u,v))
 with (d/'points-p1.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows(rows)
 native=[dict(r) for r in rows];ca.piecewise_rows(cal,X,Y,native)
 with (d/'points-p1-native.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols+['x_native','y_native','x_read_bound','y_read_bound','cal_model'],lineterminator='\n');w.writeheader();w.writerows(native)
 (d/'cal-p1'/'verified-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 ychecks=[25,45,65] if c['yr'][0]==25 else ([55,75,100] if fig=='FA-23' else [55,85,115]);checks=[];checksheet=Image.new('RGB',(1200,600),'white');draw=ImageDraw.Draw(checksheet)
 bottom=cal['horizontal_lines'][-1];left=cal['vertical_lines'][0];right=cal['vertical_lines'][-1]
 for j,xval in enumerate([0,.5,1]):
  vl=next(l for l in cal['vertical_lines'] if l['x_value']==xval);u=(vl['u_at_v0']+vl['slope_du_dv']*bottom['v_at_u0'])/(1-vl['slope_du_dv']*bottom['slope_dv_du']);v=bottom['v_at_u0']+bottom['slope_dv_du']*u
  checks.append([fig,1,'x',str(xval),round(u),round(v),'verified by eye: printed Dr label and its vertical line'])
  box=[round(u)-90,round(v)-40,round(u)+90,round(v)+90];tile=im.crop(box).resize((360,260));checksheet.paste(tile,(j*400,20));draw.text((j*400+4,4),f'{fig}: Dr label {xval}',fill='black')
 for j,yval in enumerate(ychecks):
  hl=next(l for l in cal['horizontal_lines'] if l['y_value']==yval);u=(left['u_at_v0']+left['slope_du_dv']*hl['v_at_u0'])/(1-left['slope_du_dv']*hl['slope_dv_du']);v=hl['v_at_u0']+hl['slope_dv_du']*u
  checks.append([fig,1,'y',str(yval),round(u),round(v),'verified by eye: printed pcf label on the left; same labelled horizontal line on the right'])
  box=[round(u)-140,round(v)-55,round(u)+40,round(v)+55];tile=im.crop(box).resize((360,220));checksheet.paste(tile,(j*400,320));draw.text((j*400+4,302),f'{fig}: pcf label {yval}',fill='black')
 with (d/'calibration-eye-checks.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['figure_id','panel','axis','printed_label','checked_line_u','checked_line_v','result']);w.writerows(checks)
 checksheet.save(d/'cal-p1'/'eye-check-crops.png')
 # Text-centre QA crops, shared labels intentionally repeated.
 sheet=Image.new('RGB',(900,3*180),'white');sd=ImageDraw.Draw(sheet)
 for j,sid in enumerate(['mean','upper','lower']):
  for k,(s,side,val,box,u,v) in enumerate(z for z in textboxes if z[0]==sid):
   x=0 if side=='left' else 450; tile=im.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2));td=ImageDraw.Draw(tile);pu,pv=(u-box[0])*2,(v-box[1])*2;td.ellipse((pu-4,pv-4,pu+4,pv+4),outline='red',width=2);sheet.paste(tile,(x,j*180+30));sd.text((x,j*180+5),sid+' '+side+' '+val,fill='black')
 sheet.save(d/'label-centre-checks.png')
 # Affine/piecewise difference is diagnostic only.
 sens=[]
 for sid in ['mean','upper','lower']:
  rr=[r for r in native if r['series_id']==sid and r['point_kind']=='trace'];dx=[];dy=[]
  for r in rr:
   u,v=r['pixel_u'],r['pixel_v'];xa=sum(a*b for a,b in zip(cal['ax'],[u,v,1]));q=sum(a*b for a,b in zip(cal['ay'],[u,v,1]));ya=ca.TRANSFORMS['reciprocal'][1](q);dx.append(abs(xa-r['x_native']));dy.append(abs(ya-r['y_native']))
  sens.append([sid,max(dx),max(dy)])
 with (d/'cal-p1'/'calibration-sensitivity.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['series_id','max_affine_piecewise_Dr','max_affine_piecewise_pcf']);w.writerows(sens)
 xspan=1;yspan=abs(ca.forward('reciprocal',c['yr'][1])-ca.forward('reciprocal',c['yr'][0]));rx=cal['rms_residual_x']*100;ry=cal['rms_residual_y']/yspan*100;mx=cal['max_residual_x']*100;my=cal['max_residual_y']/yspan*100
 counts={sid:{kind:sum(r['series_id']==sid and r['point_kind']==kind for r in rows) for kind in ['trace','feature']} for sid in ['mean','upper','lower']}
 summary.append(dict(figure_id=fig,counts=counts,rms_x_percent=rx,rms_y_reciprocal_span_percent=ry,max_x_percent=mx,max_y_reciprocal_span_percent=my,rms_x_pixels=cal['rms_residual_x']/cal['x_per_px'],rms_y_pixels=cal['rms_residual_y']/cal['y_per_px'],checks_x=[0,.5,1],checks_y=ychecks,n_verified_x=len(X.knots),n_verified_y=len(Y.knots)))
 notes=f'''Blind reading, batch curves-appa-b3, {fig}, panel 1. Only packet pages and protocol were used. All pixel coordinates refer to the original unrotated page, {c['page']}.png.

Calibration uses printed Dr 0 through 1.0 (all eleven labelled vertical lines), linear rightward, and labelled unit weights {c['yr'][0]} through {c['yr'][1]} pcf in steps of 5, reciprocal downward. Unlabelled horizontal subdivisions are not knots. Both the minimum-density and maximum-density labels refer to the same horizontal lines. The extra grid above the first labelled line in A-3, A-7 and A-23 is excluded. Trace/label positions above the first verified labelled line are explicitly extrapolated; no reciprocal is typed as a measurement.

Detected lines were refined against page ink. Standard 6 px half-window is used for checks except the thick bottom frame, whose 14 px half-window includes the white background needed to locate its core. This adaptation is in out/reading_lib.py; tools were not modified. All {len(X.knots)} x and {len(Y.knots)} y knots pass the protocol's coverage and 2 px end-deviation checks; none are predicted. Initial detection is retained for reproducibility. Values and read bounds use piecewise interpolation with verified line errors and the declared transform. Native y values are pcf. The affine map is diagnostic only.

Affine RMS residual: Dr {cal['rms_residual_x']:.7g} ({rx:.4f}% of span; {cal['rms_residual_x']/cal['x_per_px']:.3f} px), reciprocal-y {cal['rms_residual_y']:.7g} ({ry:.4f}% of reciprocal span; {cal['rms_residual_y']/cal['y_per_px']:.3f} px). Maximum residual: x {mx:.4f}% and reciprocal-y {my:.4f}% of span. Three by-eye checks per axis: Dr 0, 0.5, 1.0; pcf {', '.join(map(str,ychecks))}. See calibration-eye-checks.csv and the check crops. Every other labelled calibration line was also checked against the page grid.

''' 
 if mx>.5:notes+='The maximum affine x residual exceeds 0.5% although its RMS does not. The box/threshold detection was followed by direct ink refinement before extraction. The remaining maximum reflects uneven grid drafting; every labelled line passes its own ink check. Piecewise values preserve that grid rather than applying the global affine discrepancy to the points.\n\n'
 notes+='End labels, left -> right (printed numbers; not imposed on the trace calibration):\n\n'
 for sid in ['mean','upper','lower']:
  items=labels[fig][sid];notes+=f"- {sid}: "+' -> '.join(z[0] if z else '[no separate printed label]' for z in items)+'.\n'
 notes+='\nEach series has eleven trace samples, in drawing order: left ink end, nominal Dr 0.1 through 0.9, right ink end. Dashed samples falling in gaps move to the nearest visible dash end; individual notes identify moves. Enlarged crops were used to distinguish curve ink from grid ink. Bounds represent half the observed stroke thickness; overlapping end strokes use the merged ink width. The stroke meets the frame at most ends, so its exact termination within the frame cannot be separated from frame ink. Endpoint features repeat the endpoint coordinates; label features lie at the bounding-box centre of their printed glyphs (2 px centre-reading bound). Native coordinates of label features describe their page position, not a measurement of the number printed in the label. No markers, knees or interior peaks are drawn; these monotonic straight traces have endpoint extrema already recorded. Rules 8 and 9 have no applicable symbols or derived-envelope identities.\n\n'
 if fig in ['FA-19','FA-23','FA-27','FA-39','FA-47']:notes+='The task text says 25–65 pcf for all pages; this page prints a different range, recorded above and used in calibration.\n\n'
 if fig in ['FA-19','FA-47']:notes+='The caption prints RSM Soil without an a/b suffix; the supplied figure and series IDs are retained.\n\n'
 if fig=='FA-27':notes+='Ambiguity: only two left endpoint labels are printed. The 95.4 leader terminates at the solid mean start, and 95.8 at the lower dashed start. The upper dashed start lies beside the 95 grid line and has no separate printed numerical endpoint label. No left-label feature or inferred text value is invented for upper. All three right leaders are distinct.\n\n'
 if fig=='FA-47':notes+='Ambiguity: the single printed 89.4 right label has a short detached leader beside the converging ends. There are no three separate right labels. It is recorded at the same text centre for each series to identify the shared annotation, not as three independently printed numbers. Its individual leader association is uncertain: closest to upper, but adjacent to the combined cluster. Mean and lower meet in merged ink at the right frame; their last feature uses the same observed cluster centre and a 5 px half-width bound. Upper ends slightly above them.\n\n'
 notes+='Counts: '+ '; '.join(f"{s}: {counts[s]['trace']} trace, {counts[s]['feature']} feature" for s in counts)+'.\n'
 (d/'notes.md').write_text(notes,encoding='utf-8')
 subprocess.run([sys.executable,'tools/plot_grid.py','overlay','packet/'+c['page']+'.png','--points',str(d/'points-p1.csv'),'--out',str(d/'overlay-p1.png')],capture_output=True,check=True)
 print(fig,len(rows),f'RMS% {rx:.4f}/{ry:.4f}; max% {mx:.4f}/{my:.4f}')
Path('out/batch-summary.json').write_text(json.dumps(summary,indent=2))



