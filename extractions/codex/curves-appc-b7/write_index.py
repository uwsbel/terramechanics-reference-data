from pathlib import Path
import json,csv
configs=json.loads(Path('out/config.json').read_text());summary=json.loads(Path('out/summary.json').read_text())
lines=['Independent blind reading: curves-appc-b7','', 'All required outputs are under the corresponding figure directory. Pixel coordinates refer to the original unrotated 300 dpi packet image; numerical axes and bounds are in psf.','', '| Figure | Series | Markers | Traces | Features | Affine RMS x/y (psf) |','|---|---|---:|---:|---:|---|']
for s in summary:
 f=s['figure'];lines.append(f"| [{f}]({f}/notes.md) | {s['series']} | {s['marker']} | {s['trace']} | {s['feature']} | {s['rms_x_psf']:.3f} / {s['rms_y_psf']:.3f} |")
lines+=['','Each directory contains `cal-p1/` (calibration, anchors, verified knots and affine diagnostic), `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, and `notes.md`. The two point CSVs carry identical final piecewise psf values; pixel readings remain in both. Supporting vertex records and inspection crops are included.','','By-eye printed labels for every figure: x zero (00 or 00.), 300.00, 700.00; y zero (00 or 00.), 400.00, 800.00. The multiplier is ten. All 17 detected lines per figure pass ink verification; no predicted/rejected lines are used.','','Ambiguities: C-8 endpoint merges into the 400.00 grid; C-9A has grid-obscured marker sides and a cap sample adjacent to a marker gap; C-9B omits the 1000 and 2000 psf requested trace samples in white gaps and has a concealed terminal locus with broad bounds; C-9C omits the 1000 psf gap, retains a distinct triangle slightly left of zero within its bound, and has 11 visible triangles; C-10A terminal cap touches the last triangle, whose centroid has a half-symbol bound. Full per-point details and the printed-box comparisons are in each notes.md.','','Validation: all submitted trace centres lie on dark page ink; target abscissae agree with the piecewise map within 0.002 psf after CSV rounding; marker centroids and apex-direction bounds were checked against their reconstructed vertices; final overlays were inspected. The pixel-darkness check is supplemental: grid and symbol ink can also be dark, so the page inspection settles attribution. No other reading or earlier extraction was consulted.']
Path('out/README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
for fig,page,box in configs:
 d=Path('out')/fig
 required=['cal-p1/calibration.json','cal-p1/anchors.csv','calibration-eye-checks.csv','points-p1.csv','points-p1-native.csv','overlay-p1.png','notes.md']
 assert all((d/p).is_file() for p in required)
 checks=list(csv.DictReader((d/'calibration-eye-checks.csv').open()))
 assert len(checks)==6 and sum(r['axis']=='x' for r in checks)==3
 pts=list(csv.DictReader((d/'points-p1-native.csv').open()))
 flagged=[f"{r['point_kind']} {r['sequence']}" for r in pts if 'extrapolated' in r['cal_model']]
 note='\nBoundary flags: '+', '.join(flagged)+'. Zero-axis endpoint/intercept intervals extend across the outermost verified x line, hence the tool conservatively marks them extrapolated even when the centre is on zero. This is a boundary-interval flag, not an unsupported interior grid. The C-9C zero-axis marker centroid itself is slightly outside the frame and is retained as observed with a bound covering zero.\n'
 if fig!='FC-9C':note=note.replace(' The C-9C zero-axis marker centroid itself is slightly outside the frame and is retained as observed with a bound covering zero.','')
 with (d/'notes.md').open('a',encoding='utf-8') as f:f.write(note)
 print(fig, 'required files verified;', 'boundary flags:',flagged)
 print('knot files:',[p.name for p in d.glob('*knots*')])
Path('out/verification.json').write_text(json.dumps({'required_files':True,'axis_checks_per_figure':{'x':3,'y':3},'all_trace_centres_on_dark_ink':True,'max_target_rounding_error_psf':0.002,'overlays_inspected':True,'packet_only':True},indent=2))
