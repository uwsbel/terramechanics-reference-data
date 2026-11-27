from read_batch import *
from collections import Counter
S=json.loads((ROOT/'out/summary.json').read_text());report=[]
table=['| Figure | Average T/M/F | Upper T/M/F | Lower T/M/F | RMS decades / percentage points |','|---|---:|---:|---:|---:|']
for s in S:
 fid=s['figure_id'];d=ROOT/'out'/fid;page=CONFIG[fid][0];g=np.asarray(Image.open(ROOT/'packet'/f'{page}.png').convert('L'))
 required=['cal-p1/calibration.json','cal-p1/anchors.csv','cal-p1/piecewise-knots.json','calibration-eye-checks.csv','points-p1.csv','points-p1-native.csv','overlay-p1.png','notes.md']
 assert all((d/p).is_file() for p in required)
 rows=list(csv.DictReader((d/'points-p1.csv').open()));native=list(csv.DictReader((d/'points-p1-native.csv').open()));assert len(rows)==len(native)
 C,X,Y=ca.piecewise_maps(d/'cal-p1',ROOT/'packet'/f'{page}.png');assert len(X.knots)==12 and len(Y.knots)==11 and not X.rejected and not Y.rejected
 off=[]
 for r in rows:
  assert r['panel']=='1';assert r['figure_id']==fid;assert r['series_id'] in ['average','upper','lower']
  assert float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0
  if r['point_kind'] in ['trace','feature'] and g[round(float(r['pixel_v'])),round(float(r['pixel_u']))]>=150:off.append((r['series_id'],r['point_kind'],r['sequence']))
 assert not off,(fid,off)
 counts=Counter((r['series_id'],r['point_kind']) for r in rows)
 for sid in ['average','upper','lower']:
  tr=[r for r in rows if r['series_id']==sid and r['point_kind']=='trace'];ff=[r for r in rows if r['series_id']==sid and r['point_kind']=='feature']
  assert [(int(r['sequence'])) for r in tr]==list(range(1,len(tr)+1))
  for rr,ffr in [(tr[0],ff[0]),(tr[-1],ff[1])]:assert (rr['pixel_u'],rr['pixel_v'])==(ffr['pixel_u'],ffr['pixel_v'])
  assert {k:counts[sid,k] for k in ['trace','marker','feature']}==s['counts'][sid]
 eye=list(csv.DictReader((d/'calibration-eye-checks.csv').open()));assert len(eye)==23
 flags=[]
 for sid in ['average','upper','lower']:
  tr=[r for r in native if r['series_id']==sid and r['point_kind']=='trace']
  for a,b in zip(tr,tr[1:]):
   if float(b['y_native'])<float(a['y_native'])-2:flags.append(dict(series_id=sid,from_sequence=a['sequence'],to_sequence=b['sequence'],percent_a=a['y_native'],percent_b=b['y_native'],reason='Overlapping near-horizontal ink / dash displacement. Retained in drawing order with stated bounds, not made monotone by sorting.'))
 extra=sum('extrapolated' in r['cal_model'] for r in native)
 qa=dict(figure_id=fid,rows=len(rows),source_ink_centers_checked=sum(r['point_kind'] in ['trace','feature'] for r in rows),off_ink_trace_or_feature_centers=0,x_verified=12,y_verified=11,eye_checked_labels=23,extrapolated_bound_or_center_rows=extra,remaining_order_ambiguities=flags)
 (d/'delivery-check.json').write_text(json.dumps(qa,indent=2));report.append(qa)
 note=(d/'notes.md').read_text(encoding='utf-8')
 note+='\n## Delivery verification\n\nEvery trace and feature center was checked against dark source-image ink; this confirms ink, while the overlay and the stated merge bounds carry curve identity. All 23 labelled knots pass the independent ink checks. Values or bound corners reaching beyond the verified frame are explicitly flagged `extrapolated` in cal_model; '+str(extra)+' rows have that flag, mainly uncertainty intervals touching the 0/100-percent frame. No values were clipped to 0 or 100. Endpoint marks are the last identifiable curve ink at a marker/frame merge, with widened extent bounds; an exact hidden endpoint cannot be claimed.\n'
 if flags:note+='\nSome neighboring readings of the nearly horizontal merged ink have an apparent percent reversal. These remain in requested drawing order and retain widened bounds; see delivery-check.json. They are unresolved readings of an overlap, not a claim that percent finer decreases.\n'
 (d/'notes.md').write_text(note,encoding='utf-8')
 cs=['/'.join(str(s['counts'][sid][k]) for k in ['trace','marker','feature']) for sid in ['average','upper','lower']]
 table.append(f"| [{fid}]({fid}/notes.md) | {' | '.join(cs)} | {s['rms_decades']:.6f} / {s['rms_percent']:.5f} |")
 print(fid,len(rows),'rows; all source ink centers pass; order ambiguities',len(flags))
(ROOT/'out/delivery-check.json').write_text(json.dumps(report,indent=2))
readme='# curves-appa-b2 blind reading\n\nRead only the seven packet pages and their protocol; no other reader or earlier extraction was consulted. T/M/F denotes trace / marker / feature counts. RMS grain residuals are in log10 decades; percent residuals in percentage points. Native points use verified piecewise rulings.\n\n'+'\n'.join(table)+'\n\nEvery figure directory contains `cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, and `notes.md`. Additional files retain crop evidence, calibration diagnostics, marker omissions, calibration sensitivity, helpers and delivery checks. Overlay colors are average red, upper green, lower blue.\n\nAll 12 printed grain labels and 11 percent labels were checked. The labelled fine frame is 0.02 mm; the coarse frame is beyond the interior 9.0 mm ruling and was excluded. Both percent frames carry 0/100 labels.\n\nAmbiguities: FA-2, FA-6, FA-18 and FA-46 have merged near-zero tails and indistinguishable fine symbols; FA-26 approaches the zero frame with close range curves. FA-38 has close range curves and stacked coarse symbols. FA-22 has separated range curves over most of the plot, but coarse symbols and the end of line next to fine symbols remain uncertain. Bounds are widened at merges. Separately unidentified markers are omitted and located in each marker-omissions.csv; endpoint extent limits and remaining local order ambiguities are explicit in notes.md and delivery-check.json.\n'
(ROOT/'out/README.md').write_text(readme,encoding='utf-8')
