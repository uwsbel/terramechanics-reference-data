from pathlib import Path
import csv,json,zipfile,subprocess,sys
root=Path.cwd().resolve();out=(root/'out').resolve();assert out.is_relative_to(root)
# Retain the reproducible reader and verifier; remove our temporary procedural scripts.
for p in out.glob('*.py'):
 if p.name not in ['read_helpers.py','final_validate.py','package_reading.py']:
  assert p.resolve().is_relative_to(out);p.unlink()
for fid in ['FC-3B','FC-3C','FC-4B','FC-4C']:
 od=out/fid
 for p in od.glob('*.py'):
  assert p.resolve().is_relative_to(out);p.unlink()
 rows=list(csv.DictReader((od/'points-p1-native.csv').open()));gaps=[]
 for sid in json.loads((od/'counts.json').read_text())['1']:
  rr=[r for r in rows if r['series_id']==sid and r['point_kind']=='trace']
  for a,b in zip(rr,rr[1:]):
   dx=float(b['x_native'])-float(a['x_native'])
   if dx>5:
    lo,hi=float(a['pixel_u']),float(b['pixel_u']);mm=[r for r in rows if r['point_kind']=='marker' and lo-20<=float(r['pixel_u'])<=hi+20 and abs(float(r['pixel_v'])-(float(a['pixel_v'])+float(b['pixel_v']))/2)<100]
    gaps.append([fid,1,sid,a['sequence'],b['sequence'],a['pixel_u'],b['pixel_u'],a['x_native'],b['x_native'],round(dx,3),'; '.join(r['series_id']+' marker '+r['sequence'] for r in mm),'Gap retained at interruption/symbol/grid/shared ink; no interpolation. See overlay and notes.'])
 with (od/'trace-gaps-over-5.csv').open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(['figure_id','panel','series_id','from_sequence','to_sequence','from_pixel_u','to_pixel_u','from_x_native','to_x_native','gap_native','nearby_markers','note']);w.writerows(gaps)
 p=od/'notes.md';t=p.read_text(encoding='utf-8-sig').replace('with at least 3-px bounds.','with 5-px bounds when the outer outline is connected to other ink.');t+='\nFinal reproducibility: use the final reading-spec.json with out/read_helpers.py to regenerate tables and overlays. Temporary procedural editing scripts were removed; final specs and image crops are retained. Clean disconnected triangle outlines use the outer ink bounding box; connected outlines use the white-interior method with 5-px bounds.\n';p.write_text(t,encoding='utf-8')
result=subprocess.run([sys.executable,str(out/'final_validate.py')],capture_output=True,text=True);assert result.returncode==0,result.stderr
p=out/'SUMMARY.md';t=p.read_text();t+='\nCommon final helper files: read_helpers.py, final_validate.py, package_reading.py. The deliverable archive curves-appc-b2-reading.zip contains the four figure folders, helpers and batch summary/audit files.\n';p.write_text(t,encoding='utf-8')
archive=out/'curves-appc-b2-reading.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.rglob('*')):
  if p.is_file() and p!=archive and '__pycache__' not in p.parts:z.write(p,p.relative_to(out).as_posix())
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'archive':str(archive),'archive_bytes':archive.stat().st_size,'series_totals':{fid:{panel:{sid:sum(v.values()) for sid,v in dd.items()} for panel,dd in json.loads((out/fid/'counts.json').read_text()).items()} for fid in ['FC-3B','FC-3C','FC-4B','FC-4C']},'validation':'passed; limitations retained in notes/validation.json'},indent=1))
