import csv,json,math
from pathlib import Path
from collections import Counter

result={}
expected={'F2-45':{'lpt95':28,'lpt79':24},'F2-46':{'lpt98':24,'lpt89':24},'F2-47':{'lpt101':24,'lpt91':28},'F2-48':{'lpt87':32,'lpt85':32}}
for fid,series in expected.items():
 root=Path('out')/fid
 for f in ['cal-p1/calibration.json','cal-p1/anchors.csv','cal-p1/piecewise-knots.json','calibration-eye-checks.csv','points-p1.csv','points-p1-native.csv','overlay-p1.png','notes.md']:assert (root/f).is_file(),(fid,f)
 pixels=list(csv.DictReader((root/'points-p1.csv').open()))
 native=list(csv.DictReader((root/'points-p1-native.csv').open()))
 assert len(pixels)==len(native)
 for r,n in zip(pixels,native):
  assert r.items()<=n.items()
  assert r['panel']=='1' and r['figure_id']==fid and r['series_id'] in series
  assert r['point_kind'] in ['trace','feature'] and r['symbol']==''
  for k in ['pixel_u','pixel_v','u_bound_px','v_bound_px']:assert math.isfinite(float(r[k]))
  assert float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0
  for k in ['x_native','y_native','x_read_bound','y_read_bound']:assert math.isfinite(float(n[k]))
  assert n['cal_model'].startswith('piecewise')
 for sid,nquarter in series.items():
  rr=[r for r in pixels if r['series_id']==sid]
  assert [int(r['sequence']) for r in rr]==list(range(1,len(rr)+1))
  trace=[r for r in rr if r['point_kind']=='trace']
  nominal=[float(r['target_x_in']) for r in trace if r['target_x_in'] and float(r['target_x_in'])>0]
  assert nominal==[i/4 for i in range(1,nquarter+1)],(fid,sid,nominal)
  features=[r for r in rr if r['point_kind']=='feature']
  for role in ('first;','peak;','last;'):assert any(r['note'].startswith(role) for r in features),(fid,sid,role)
 checks=list(csv.DictReader((root/'calibration-eye-checks.csv').open()))
 for axis in ('x','y'):assert sum(r['axis']==axis and r['checked_by_eye']=='yes' for r in checks)>=3
 knots=json.loads((root/'cal-p1/piecewise-knots.json').read_text())
 assert not knots['rejected_x'] and not knots['rejected_y']
 audit=list(csv.DictReader((root/'ink-distance-audit.csv').open()))
 assert max(float(r['nearest_dark_px']) for r in audit)<=2
 result[fid]={'rows':len(pixels),'counts':{sid:{kind:sum(r['series_id']==sid and r['point_kind']==kind for r in pixels) for kind in ['trace','feature','marker']} for sid in series},'verified_x_knots':len(knots['x']),'verified_y_knots':len(knots['y']),'label_checks':len(checks),'all_points_dark_ink_within_2px':True,'note':'Raw ink distance is not D031; line identity and gaps were visually reviewed.'}
Path('out/validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
