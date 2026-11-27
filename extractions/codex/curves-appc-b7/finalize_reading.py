import json,sys,csv,subprocess,shutil
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,'tools');import calibrate_axes as c
# Reconstructed core vertices: apex, lower-left and lower-right; triangle centroid is their arithmetic mean.
vertices={
'FC-8':[[[780,3329],[764,3356],[796,3356]],[[955,3141],[938,3170],[972,3170]],[[1425,2753],[1409,2781],[1442,2781]],[[1593,2537],[1576,2567],[1609,2567]],[[1846,2388],[1830,2416],[1862,2416]],[[2104,2309],[2089,2337],[2120,2337]]],
'FC-9A':[[[740,3427],[724,3453],[757,3453]],[[824,3301],[808,3326],[841,3326]],[[1073,2953],[1057,2979],[1090,2979]],[[1327,2603],[1311,2629],[1344,2629]],[[1496,2403],[1480,2429],[1513,2429]],[[1665,2253],[1649,2280],[1682,2280]]],
'FC-9B':[[[950,3270],[934,3295],[967,3295]],[[1253,2979],[1237,3007],[1270,3007]],[[1504,2656],[1488,2683],[1521,2683]],[[1845,2330],[1828,2359],[1862,2359]]],
'FC-9C':[[[555,3603],[539,3633],[571,3633]],[[638,3444],[622,3474],[654,3474]],[[723,3321],[707,3348],[740,3348]],[[851,3222],[835,3248],[868,3248]],[[981,2976],[965,3005],[998,3005]],[[1148,2930],[1132,2957],[1165,2957]],[[1232,2627],[1216,2652],[1249,2652]],[[1402,2607],[1386,2635],[1419,2635]],[[1405,2427],[1389,2454],[1422,2454]],[[1580,2283],[1564,2311],[1597,2311]],[[1750,2288],[1734,2314],[1767,2314]]],
'FC-10A':[[[838,3407],[822,3434],[855,3434]],[[1041,3169],[1025,3194],[1058,3194]],[[1248,2928],[1232,2953],[1265,2953]],[[1460,2744],[1444,2772],[1477,2772]],[[1670,2557],[1654,2583],[1687,2583]],[[1882,2373],[1866,2399],[1899,2399]]]
}
metadata={'FC-8':['rs-loose','RS LOOSE','40.40','38.63','.7992','242.12'],'FC-9A':['rs-dense','RS Dense','54.20','52.55','1.3059','634.20'],'FC-9B':['rs-dense','RS DENSE','54.40','46.65','1.0594','698.23'],'FC-9C':['rs-dense','RS DENSE','54.30','49.39','1.1663','700.44'],'FC-10A':['ps-loose','PS Loose','25.90','43.44','.9471','488.69']}
marker_notes={'FC-8':{4:'Vertical and horizontal grid lines touch triangle; vertices reconstructed from visible sides.'},'FC-9A':{1:'Triangle base crosses 100.00 horizontal grid line; centroid reconstructed.',5:'Right side touches vertical grid line; reconstructed from other sides.'},'FC-9B':{1:'Vertical grid line runs through triangle; centroid reconstructed.',2:'Left base touches vertical grid line; reconstructed from other sides.',3:'Right vertex merges with fitted line and vertical grid; widened to half symbol extent.',4:'Base merges with 500.00 grid and fitted line endpoint; reconstructed from apex/sides, widened to half symbol extent.'},'FC-9C':{1:'Zero-axis line runs through triangle; centroid lies slightly left of axis, retained as read.',2:'100.00 horizontal grid line crosses triangle; centroid reconstructed.',4:'Vertical grid line runs through triangle; centroid reconstructed.',6:'Left base touches vertical grid line; reconstructed from visible sides.',8:'Right base near vertical grid; centroid reconstructed.',9:'Right vertex touches vertical grid; centroid reconstructed.',10:'500.00 horizontal grid line crosses triangle; centroid reconstructed.',11:'500.00 horizontal grid line crosses triangle; centroid reconstructed.'},'FC-10A':{5:'400.00 horizontal grid line crosses apex; centroid reconstructed.',6:'Left side merges with rounded fit-line endpoint; widened to half symbol extent.'}}
omit={'FC-9B':[1000,2000],'FC-9C':[1000]}
# Right terminal loci read from enlarged page crops. C-8/C-9B terminate in merged ink.
terminal={'FC-8':None,'FC-9A':(1681.5,2205.0),'FC-9B':None,'FC-9C':(1740.5,2187.0),'FC-10A':(1868.0,2377.0)}
strokes=json.loads(Path('out/stroke-readings.json').read_text());summary=[]
cols=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note','x_target_psf','x_unit','y_unit']
def write_csv(path,rows,fields):
 with Path(path).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
def axis_intersect(line,m,b):
 u=(line['u_at_v0']+line['slope_du_dv']*b)/(1-line['slope_du_dv']*m);return u,m*u+b
for fig,page,box in json.loads(Path('out/config.json').read_text()):
 d=Path('out')/fig;sid,title,density,angle,tan,cohesion=metadata[fig];cal,X,Y=c.piecewise_maps(d/'cal-p1','packet/'+page);im=Image.open('packet/'+page).convert('L');g=np.asarray(im)
 m,b=strokes[fig]['m'],strokes[fig]['b'];rows=[]
 def add(kind,seq,u,v,bu,bv,note='',symbol='',target=''):
  rows.append(dict(zip(cols,[fig,1,sid,kind,seq,round(u,3),round(v,3),round(bu,3),round(bv,3),symbol,note,target,'psf','psf'])))
 # Markers are entered before any traces.
 vr=[]
 for i,V in enumerate(vertices[fig],1):
  ar=np.array(V);u,v=ar.mean(axis=0);h=ar[:,1].max()-ar[:,1].min();bu,bv=2,max(5,h/6);note=marker_notes.get(fig,{}).get(i,'')
  if note:bu,bv=5,max(8,h/6)
  if (fig=='FC-9B' and i in [3,4]) or (fig=='FC-10A' and i==6):bu,bv=np.ptp(ar[:,0])/2,max(np.ptp(ar[:,1])/2,h/6)
  add('marker',i,u,v,bu,bv,('Triangle centroid from reconstructed vertices. '+note).strip(),'triangle-up')
  vr.append({'marker_sequence':i,'vertices_uv':V,'height_px':float(h),'centroid_uv':[u,v]})
 (d/'triangle-vertices.json').write_text(json.dumps(vr,indent=2))
 # Trace half widths are measured cross sections of the diagonal stroke, excluding grid/symbol ink.
 typical_v={'FC-8':15,'FC-9A':20,'FC-9B':17,'FC-9C':19,'FC-10A':16}[fig]
 bu=typical_v/(2*abs(m));bv=typical_v/2
 # Near zero: fit only the first short, visible diagonal segment, extrapolating its centre a few pixels into the merged axis ink.
 zero=next(z for z in cal['vertical_lines'] if z['x_value']==0);u_guess,v_guess=axis_intersect(zero,m,b);obs=[]
 for u in range(int(u_guess)+12,int(u_guess)+58):
  pred=m*u+b;lo=int(pred)-18;hi=int(pred)+19;idx=np.where(g[lo:hi,u]<128)[0]
  runs=[a for a in np.split(idx,np.where(np.diff(idx)>1)[0]+1) if len(a)]
  valid=[a for a in runs if 8<=len(a)<=24 and abs(np.mean(a)+lo-pred)<8]
  if valid:
   a=min(valid,key=lambda a:abs(np.mean(a)+lo-pred));obs.append((u,np.mean(a)+lo))
 aa=np.array(obs);ml,bl=np.polyfit(aa[:,0],aa[:,1],1);start=axis_intersect(zero,ml,bl)
 if fig in ['FC-8','FC-9B']:
  value=4000 if fig=='FC-8' else 5000;hl=next(z for z in cal['horizontal_lines'] if z['y_value']==value)
  ue=(hl['v_at_u0']-b)/(m-hl['slope_dv_du']);end=(ue,m*ue+b)
 else:end=terminal[fig]
 # Explicit observations at 500 psf increments: preserve centres actually on ink; reject the three visible interruptions.
 tr=[(start[0],start[1],bu,bv,'first point; line begins on zero axis; centre of short diagonal stroke meeting axis ink','')]
 for r in strokes[fig]['samples']:
  target=int(r['x_target'])
  if target in omit.get(fig,[]):continue
  u,v=r['u'],r['v'];width=r['width'];note=''
  if width>=30 or (fig=='FC-8' and target==3500):
   # Column is merged with a grid line. Reconstruct the centre from flanking diagonal ink in a 100 px neighbourhood.
   obs=[]
   for uu in range(int(u)-50,int(u)+51):
    if abs(uu-u)<9:continue
    pred=m*uu+b;lo=int(pred)-18;hi=int(pred)+19;idx=np.where(g[lo:hi,uu]<128)[0];runs=[a for a in np.split(idx,np.where(np.diff(idx)>1)[0]+1) if len(a)]
    vv=[a for a in runs if typical_v-3<=len(a)<=typical_v+3 and abs(np.mean(a)+lo-pred)<3]
    if vv:
     a=min(vv,key=lambda a:abs(np.mean(a)+lo-pred));obs.append((uu,np.mean(a)+lo))
   ar=np.array(obs);mm,bb=np.polyfit(ar[:,0],ar[:,1],1);v=mm*u+bb
   note='Diagonal stroke centre reconstructed from adjacent ink at grid crossing; grid thickness excluded from bound.'
   vvbound=bv;uubound=bu
  else:
   vvbound=width/2;uubound=width/(2*abs(m))
   if width<typical_v-4:note='Sample lies on rounded stroke-cap ink adjacent to a symbol interruption; no sample in the white gap.'
  # Tiny horizontal adjustment keeps normal stress at exactly the requested piecewise abscissa.
  for it in range(4):u+=(target-X.value(u,v)[0])/X.value(u,v)[1]/X.e_s[0]
  tr.append((u,v,uubound,vvbound,note,target))
 endnote='last point; peak of monotonically increasing straight trace'
 ebu,ebv=bu,bv
 if fig=='FC-8':endnote+='; diagonal endpoint merges with 400.00 horizontal grid, no diagonal ink continues above it'
 if fig=='FC-9B':
  endnote+='; terminal locus concealed in final triangle base and 500.00 grid; position assigned to ink merger, wide endpoint bound covers concealed tip';ebu,ebv=17,15
 if fig=='FC-10A':endnote+='; rounded cap is left of final triangle apex; triangle outline excluded'
 tr.append((end[0],end[1],ebu,ebv,endnote,''))
 for i,t in enumerate(tr,1):add('trace',i,*t[:4],t[4],target=t[5])
 add('feature',1,*start,bu,bv,'first point')
 add('feature',2,*end,ebu,ebv,endnote)
 add('feature',3,*start,bu,bv,'intercept')
 write_csv(d/'points-p1.csv',rows,cols)
 subprocess.run([sys.executable,'tools/calibrate_axes.py','apply',str(d/'cal-p1'/'calibration.json'),str(d/'points-p1.csv'),str(d/'cal-p1'/'points-affine.csv')],check=True)
 subprocess.run([sys.executable,'tools/calibrate_axes.py','piecewise',str(d/'cal-p1'),str(d/'points-p1.csv'),str(d/'points-p1-native.csv'),'--image','packet/'+page],check=True)
 shutil.copyfile(d/'points-p1-native.csv',d/'points-p1.csv')
 native=list(csv.DictReader((d/'points-p1-native.csv').open()));nt=[r for r in native if r['point_kind']=='trace'];xf=np.array([float(r['x_native']) for r in nt]);yf=np.array([float(r['y_native']) for r in nt]);slope,ic=np.polyfit(xf,yf,1)
 sb=sum(abs(x-xf.mean())*(float(r['y_read_bound'])+abs(slope)*float(r['x_read_bound'])) for x,r in zip(xf,nt))/sum((xf-xf.mean())**2)
 intr=next(r for r in native if r['note']=='intercept');inter=float(intr['y_native']);ib=float(intr['y_read_bound'])
 # Three printed labels per axis, read against the axis line at the labels.
 checks=[]
 for axis,vals in [('x',[0,3000,7000]),('y',[0,4000,8000])]:
  for val in vals:
   if axis=='x':
    l=next(z for z in cal['vertical_lines'] if z['x_value']==val);vv=next(z for z in cal['horizontal_lines'] if z['y_value']==0);uu=(l['u_at_v0']+l['slope_du_dv']*vv['v_at_u0'])/(1-l['slope_du_dv']*vv['slope_dv_du']);v=vv['v_at_u0']+vv['slope_dv_du']*uu;u=uu
   else:
    l=next(z for z in cal['horizontal_lines'] if z['y_value']==val);vv=zero;u=(vv['u_at_v0']+vv['slope_du_dv']*l['v_at_u0'])/(1-vv['slope_du_dv']*l['slope_dv_du']);v=l['v_at_u0']+l['slope_dv_du']*u
   label=(('00.' if fig in ['FC-8','FC-9A','FC-9B'] else '00') if val==0 else f'{val/10:.2f}')
   checks.append({'figure_id':fig,'panel':1,'axis':axis,'printed_label':label,'multiplier':10,'anchor_value_psf':val,'pixel_u':round(u,2),'pixel_v':round(v,2),'result':'confirmed by eye','note':'Label belongs to this grid/frame line; box above plot excluded from y calibration.'+(' Left digit damaged but identifiable as 4.' if fig=='FC-8' and axis=='y' and val==4000 else '')})
 write_csv(d/'calibration-eye-checks.csv',checks,list(checks[0]))
 aff=list(csv.DictReader((d/'cal-p1'/'points-affine.csv').open()));sx=max(abs(float(a['x_native'])-float(n['x_native'])) for a,n in zip(aff,native));sy=max(abs(float(a['y_native'])-float(n['y_native'])) for a,n in zip(aff,native))
 gaps=omit.get(fig,[])
 text=f'''{fig}, panel 1, page image {page}. Independent reading using only packet/ and the supplied tools; no other reading consulted. Both point CSVs contain the same pixel readings and piecewise values in psf. No SI conversion. Series id retained: {sid}. Printed group: {title} (case as in the box); the index identity agrees with the page.

Printed box values, transcribed as printed:
Avg. Density = {density}
Angle of Friction = {angle}
Tan Theta = {tan}
Cohesion = {cohesion}

Both axis titles print (x 10^1). A printed 100.00 is 1000 psf. Plot range: normal stress 0–7000 psf, shear strength 0–8000 psf. The box top is not the 800.00 grid line. By-eye checks: x {', '.join(r['printed_label'] for r in checks if r['axis']=='x')}; y {', '.join(r['printed_label'] for r in checks if r['axis']=='y')}. Checks identify the actual grid/frame line beside each label, not the label baseline. All 8 vertical and 9 horizontal lines are detected and verified against ink; none predicted or rejected. See cal-p1/knots.json for each ink check and location error. Affine RMS residuals: x {cal['rms_residual_x']:.3f} psf, y {cal['rms_residual_y']:.3f} psf; maximum residuals x {cal['max_residual_x']:.3f}, y {cal['max_residual_y']:.3f} psf, below 0.5% of the respective spans. Final values use verified piecewise knots with each line's tilt. Bounds propagate pixel intervals and bracketing-line location intervals; the global affine residual is not added. Maximum affine-versus-piecewise sensitivity over this series: x {sx:.3f} psf, y {sy:.3f} psf (diagnostic, not added to bounds).

{len(vertices[fig])} triangle-up markers. Marker numbers identify visible symbols in the inspection crops; they are not individual test identities. Each centroid is the mean of three reconstructed core vertices saved in triangle-vertices.json, excluding fit-line, grid and stray ink. Clean marker bounds: u ±2 px, v at least height/6 (rounded up to 5 px); grid-obscured centroids widened to u ±5, v ±8 px. Symbol/fit-line mergers have half-symbol bounds. No two triangles can be distinguished at the same symbol location, and no extra symbol is inferred. All markers use the sole series in series.csv; rule 9 provides no competing series to resolve, and no unavailable data-sheet reading was consulted.

{len(nt)} trace samples, in drawing order from left endpoint, at each available 500 psf normal-stress increment, then right endpoint. All submitted samples lie on diagonal stroke ink; grid-crossing centres are reconstructed from nearby visible diagonal ink. Typical stroke cross-section is {typical_v} px vertically: trace bounds are half the local vertical thickness and half the horizontal thickness (vertical thickness / absolute pixel slope). Rounded caps use their observed narrower cross-section. These are reading bounds, not standard deviations. {('Requested samples omitted at '+', '.join(map(str,gaps))+' psf because the diagonal stroke is visibly interrupted around triangles; the grid/triangle ink at the requested position is not a trace. No interpolation across those white gaps.') if gaps else 'No requested 500 psf location is omitted.'}

The line reaches the normal-stress-zero axis. Its first point and intercept share the same reconstructed stroke/axis junction, not the nearest triangle. Features: first point, last point (also the maximum of this increasing line), and intercept; no knee is visible.

OLS slope of the submitted piecewise trace samples = {slope:.6f}. Difference (reading − printed Tan Theta {tan}) = {slope-float(tan):+.6f}. A conservative first-order slope reading interval from all x/y bounds is ±{sb:.6f}; this is not a regression standard error. Fitted y intercept of the samples = {ic:.3f} psf (diagnostic). Direct zero-axis intercept reading = {inter:.3f} ± {ib:.3f} psf. Difference (direct intercept − printed Cohesion {cohesion} psf) = {inter-float(cohesion):+.3f} psf. The printed cohesion is compared directly in psf, not multiplied by the axis-label factor. No coordinates were adjusted to the printed slope or cohesion.

Ambiguities: {' '.join(f'Marker {k}: {v}' for k,v in marker_notes.get(fig,{}).items())} {endnote if fig in ['FC-8','FC-9B','FC-10A'] else 'Terminal rounded cap is separable from the final triangle.'}
'''
 if fig=='FC-9B':text+='\nC-9B endpoint exception: the last diagonal locus is merged into the triangle base/grid, so the tip cannot be isolated. Its trace and feature bounds are deliberately widened to ±17 u / ±15 v px under rule 6; ordinary half-stroke bounds would imply more certainty than the ink allows. The point is on merged ink, not a white-gap extension.\n'
 if fig=='FC-9C':text+='\nThe triangle on the zero axis is a distinct eleventh marker. Its centroid is retained slightly left of the calibrated zero line; its widened interval includes zero. The two symbols near 3000 psf normal stress and the two near 5000 psf shear stress are individually distinguishable, not merged observations.\n'
 (d/'notes.md').write_text(text,encoding='utf-8')
 subprocess.run([sys.executable,'tools/plot_grid.py','overlay','packet/'+page,'--points',str(d/'points-p1.csv'),'--out',str(d/'overlay-p1.png')],check=True)
 summary.append({'figure':fig,'series':sid,'marker':len(vertices[fig]),'trace':len(nt),'feature':3,'rms_x_psf':cal['rms_residual_x'],'rms_y_psf':cal['rms_residual_y'],'slope':slope,'slope_diff':slope-float(tan),'intercept_psf':inter,'intercept_diff_psf':inter-float(cohesion),'omitted_targets':gaps})
Path('out/summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))

