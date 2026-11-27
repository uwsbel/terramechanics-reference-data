import sys,json,csv
from pathlib import Path
sys.path.insert(0,'tools'); import calibrate_axes as ca
from PIL import Image
import numpy as np
for f,p in [('F2-29',80),('F2-32',88),('F2-33',89),('F2-34',90)]:
 d=Path('out')/f/'cal-p1'; im=f'packet/p{p:04}.png'
 cal,X,Y=ca.piecewise_maps(d,im)
 print(f, 'verified', [k['value'] for k in X.knots],[k['value'] for k in Y.knots], 'rejected',[(k['value'],k['reason']) for k in X.rejected+Y.rejected])
 (d/'initial-ink-verification.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
