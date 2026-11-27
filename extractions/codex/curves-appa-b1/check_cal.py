import sys,json
from pathlib import Path
sys.path.insert(0,'tools')
import calibrate_axes as ca
cfg=json.loads(Path('out/config.json').read_text())
for f,c in cfg.items():
 cal,X,Y=ca.piecewise_maps(Path('out')/f/'cal-p1','packet/'+c['page']+'.png')
 s=ca.knots_summary(X,Y);(Path('out')/f/'cal-p1'/'knots-verified.json').write_text(json.dumps(s,indent=2))
 print(f,'rms',cal['rms_residual_x'],cal['rms_residual_y'],'verified',[k['value'] for k in X.knots],[k['value'] for k in Y.knots],'rejected',s['rejected_x'],s['rejected_y'])
