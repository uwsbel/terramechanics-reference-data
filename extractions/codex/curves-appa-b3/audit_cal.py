import sys,json
sys.path.insert(0,'tools'); import calibrate_axes as ca
from pathlib import Path
cfg=json.loads(Path('out/config.json').read_text())
for fig,c in cfg.items():
 cal,X,Y=ca.piecewise_maps(Path('out')/fig/'cal-p1','packet/'+c['page']+'.png')
 print(fig,'X rejected',[(k['value'],k['reason']) for k in X.rejected],'Y rejected',[(k['value'],k['reason']) for k in Y.rejected])
 print('residual % span RMS/max',cal['rms_residual_x']*100,cal['max_residual_x']*100,100*cal['rms_residual_y']/abs(ca.forward('reciprocal',c['yr'][1])-ca.forward('reciprocal',c['yr'][0])),100*cal['max_residual_y']/abs(ca.forward('reciprocal',c['yr'][1])-ca.forward('reciprocal',c['yr'][0])))
