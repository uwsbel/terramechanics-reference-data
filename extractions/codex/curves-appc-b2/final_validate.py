from pathlib import Path
import csv,json,hashlib,math
import numpy as np
from PIL import Image
root=Path.cwd();out=root/'out';fids=['FC-3B','FC-3C','FC-4B','FC-4C'];base=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note'];extra=['x_native','y_native','x_read_bound','y_read_bound'];report={};counts=[];cals=[];manifest=[]
for fid in fids:
 od=out/fid;spec=json.loads((od/'reading-spec.json').read_text());im=np.array(Image.open(spec['image']).convert('L'));checks=list(csv.DictReader((od/'calibration-eye-checks.csv').open()));audit=json.loads((od/'marker-center-audit.json').read_text());manual=sum(a['method']=='manual-unisolated' for a in audit)
 r={'panels':{},'manual_unisolated_centers':manual,'warnings':[]}
 for panel in [1,2]:
  cal=json.loads((od/f'cal-p{panel}/calibration.json').read_text());
  assert not any(l['source']=='predicted' for l in cal['horizontal_lines']+cal['vertical_lines'])
  for axis in ['x','y']:assert len({q['printed_label'] for q in checks if q['panel']==str(panel) and q['axis']==axis})>=3
  cals.append([fid,panel,cal['rms_residual_x'],cal['rms_residual_y'],cal['max_residual_x'],cal['max_residual_y']])
  with (od/f'points-p{panel}.csv').open() as f:rd=csv.DictReader(f);assert rd.fieldnames==base;rows=list(rd)
  with (od/f'points-p{panel}-native.csv').open() as f:rd=csv.DictReader(f);assert rd.fieldnames==base+extra;native=list(rd)
  assert len(rows)==len(native)
  for a,b in zip(rows,native):
   assert all(a[k]==b[k] for k in base);assert a['figure_id']==fid and int(a['panel'])==panel
   assert a['series_id'] in spec['panels'][str(panel)];assert a['point_kind'] in ['marker','trace','feature'];u,v=float(a['pixel_u']),float(a['pixel_v']);bu,bv=float(a['u_bound_px']),float(a['v_bound_px']);assert bu>=0 and bv>=0 and 0<=u<im.shape[1] and 0<=v<im.shape[0]
   assert all(math.isfinite(float(b[k])) for k in extra)
   if a['point_kind']=='marker':assert a['symbol']==spec['panels'][str(panel)][a['series_id']]['symbol']
   if a['point_kind']=='trace':assert im[round(v),round(u)]<180
  for sid in spec['panels'][str(panel)]:
   kinds={}
   for kind in ['marker','trace','feature']:
    rr=[q for q in rows if q['series_id']==sid and q['point_kind']==kind];assert [int(q['sequence']) for q in rr]==list(range(1,len(rr)+1));kinds[kind]=len(rr)
    if kind=='trace':assert all(float(rr[i]['pixel_u'])>float(rr[i-1]['pixel_u']) for i in range(1,len(rr)))
   if panel==1:
    ff=[q['note'] for q in rows if q['series_id']==sid and q['point_kind']=='feature'];assert all(any(q.startswith(k+':') for q in ff) for k in ['first','peak','last'])
   counts.append([fid,panel,sid,kinds['marker'],kinds['trace'],kinds['feature'],sum(kinds.values())])
  r['panels'][panel]={'row_count':len(rows),'trace_ink_checked':True,'schema_and_sequences_checked':True}
 if fid=='FC-4B':r['warnings'].append('Upper maximum y calibration residual 35.687 psf = .714% of span; uneven printed grid, documented in notes.')
 r['warnings'].append('Trace sampling gaps above 5 thousandths are retained at visible interruptions or symbol/grid/shared-ink exclusions; details in trace-sampling-audit.json.')
 report[fid]=r
 for rel in ['cal-p1/anchors.csv','cal-p1/calibration.json','cal-p2/anchors.csv','cal-p2/calibration.json','calibration-eye-checks.csv','points-p1.csv','points-p1-native.csv','points-p2.csv','points-p2-native.csv','overlay-p1.png','overlay-p2.png','notes.md']:assert (od/rel).is_file()
 for p in sorted(od.rglob('*')):
  if p.is_file():manifest.append([str(p.relative_to(root)).replace('\\','/'),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
for name,cols,data in [('counts-summary.csv',['figure_id','panel','series_id','markers','traces','features','total'],counts),('calibration-summary.csv',['figure_id','panel','rms_x','rms_y','max_x','max_y'],cals),('files-manifest.csv',['path','bytes','sha256'],manifest)]:
 with (out/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(data)
(out/'validation.json').write_text(json.dumps(report,indent=2))
lines=['# Independent reading: curves-appc-b2','', 'Evidence was restricted to the supplied packet. All four figures have complete required artifact sets; unreadable/shared observations and calibration limitations are documented individually. No other reading was consulted.','', '## Counts','', 'M = marker, T = actual drawn-ink trace sample, F = feature. Lower panels contain no connecting curves.','', '| Figure | Panel | Series | M | T | F | Total |','|---|---:|---|---:|---:|---:|---:|']
lines += ['| '+' | '.join(map(str,r))+' |' for r in counts]
lines += ['', '## Calibration residuals','', 'x units: thousandths of an inch. Panel 1 y: psf. Panel 2 y: thousandths of an inch.','', '| Figure | Panel | RMS x | RMS y | Max x | Max y |','|---|---:|---:|---:|---:|---:|']
lines += ['| '+f'{fid} | {p} | {rx:.3f} | {ry:.3f} | {mx:.3f} | {my:.3f}'+' |' for fid,p,rx,ry,mx,my in cals]
lines += ['', 'FC-4B upper maximum y residual exceeds .5% of the axis span (.714%); the printed top grid interval is uneven. RMS is .412%. The notes state the limitation of retaining the required affine fit. No final calibration line is predicted. Each panel has at least three eye checks on each axis.','', '## Principal ambiguities','', '- FC-3B: circle plateau shares 3000-psf grid ink; lower x=0 circle not separable; possible missing upper terminal triangle-down and triangle-up near 150 thousandths.','- FC-3C: heading hides most of 6000-psf frame; possible missing upper square near 130 thousandths; crowded lower circle/triangle/plus pairs.','- FC-4B: uneven y grid; several upper markers depart from drawn curves; tiny lower circles and partially shared clusters, including one circle beyond right frame; no identifiable lower plus at x=0/200.','- FC-4C: n2934 is triangle-up and n741 triangle-down; unlabeled outer top frame above 8000; early and late shared curve ink; lower frame/zero clusters, possible hidden triangle-ups, and a small circle beyond left frame.','', 'Trace sampling is nominally about 2.06 thousandths. Gaps exceeding 5 are explicitly retained at symbol interruptions, excluded grid contacts or inseparable ink. No interpolated y values are emitted. The audit JSON lists gaps/columns so this exception to uniform coverage is reviewable.','', '## Files','']
for fid in fids:
 lines += [f'### {fid}','', f'[Notes]({fid}/notes.md) · [upper overlay]({fid}/overlay-p1.png) · [lower overlay]({fid}/overlay-p2.png)','']
 for p in sorted((out/fid).rglob('*')):
  if p.is_file():rel=p.relative_to(out).as_posix();lines.append(f'- [{rel}]({rel})')
 lines.append('')
lines += ['Batch summaries: counts-summary.csv, calibration-summary.csv, files-manifest.csv, validation.json. Helper scripts are under out/. Required raw point schemas exactly follow section 3 of CURVE-READING.md; native tables add its four converted-value/bound columns.','']
(out/'SUMMARY.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'validation':'passed','panels':{fid:[report[fid]['panels'][p]['row_count'] for p in [1,2]] for fid in fids},'trace_counts':{fid:json.loads((out/fid/'counts.json').read_text())['1'] for fid in fids}},indent=1))
