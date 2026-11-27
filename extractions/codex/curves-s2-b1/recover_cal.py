import sys,csv,json
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,'tools'); import calibrate_axes as ca
for f,p,axis,val in [('F2-32',88,'x',2),('F2-34',90,'y',1000)]:
 d=Path('out')/f/'cal-p1'; im=f'packet/p{p:04}.png'; cal,X,Y=ca.piecewise_maps(d,im); K=X if axis=='x' else Y
 ts=[t for kn in K.knots for t in kn['t']]
 pts,rms=ca.recover_line(np.asarray(Image.open(im).convert('L')),K,val,(min(ts),max(ts)),search_px=20,step=40)
 rows=ca.load_anchors(d)
 (d/'anchors-before-recovery.csv').write_bytes((d/'anchors.csv').read_bytes())
 for r in rows:
  if float(r[axis+'_value'])==val:r[axis+'_value']='';r[axis+'_source']=''
 for u,v in pts: rows.append({'x_value':val if axis=='x' else '', 'y_value':val if axis=='y' else '', 'u':round(u,3),'v':round(v,3),'x_source':'recovered ink' if axis=='x' else '', 'y_source':'recovered ink' if axis=='y' else ''})
 with (d/'anchors.csv').open('w',newline='') as fp:
  w=csv.DictWriter(fp,fieldnames=['x_value','y_value','u','v','x_source','y_source']);w.writeheader();w.writerows(rows)
 (d/'recovery.json').write_text(json.dumps({'axis':axis,'value':val,'rms_px':rms,'points':pts},indent=2))
 print(f,axis,val,len(pts),rms)
