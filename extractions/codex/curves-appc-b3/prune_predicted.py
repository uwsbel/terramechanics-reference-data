import json,csv,sys
from pathlib import Path
sys.path.insert(0,'tools')
from calibrate_axes import fit_affine
base=Path(sys.argv[1]);c=json.loads((base/'calibration.json').read_text());rows=list(csv.DictReader((base/'anchors.csv').open()));rows=[r for r in rows if r['x_source']!='predicted' and r['y_source']!='predicted']
for r in rows:
 for k in ['x_value','y_value','u','v']:r[k]=float(r[k])
ax,ay,rx,ry,mx,my=fit_affine(rows)
import numpy as np
c.update(ax=ax,ay=ay,rms_residual_x=rx,rms_residual_y=ry,max_residual_x=mx,max_residual_y=my,x_per_px=float(np.hypot(ax[0],ax[1])),y_per_px=float(np.hypot(ay[0],ay[1])),n_anchors=len(rows),reader_note='Synthetic predicted grid intersections excluded from fit: no printed horizontal grid lines at those levels. Retained predicted line positions describe the nominal scale only.')
with (base/'anchors.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
(base/'calibration.json').write_text(json.dumps(c,indent=1));print(base,rx,ry)
