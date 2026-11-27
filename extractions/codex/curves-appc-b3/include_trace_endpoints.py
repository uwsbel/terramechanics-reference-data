import csv,json,subprocess,sys
from pathlib import Path
for fig in ['FC-5B','FC-6B','FC-6C','FC-6D']:
 base=Path('out')/fig;p=base/'points-p1.csv';rows=list(csv.DictReader(p.open()));cols=list(rows[0]);cfg=json.loads((base/'readings.json').read_text());out=[]
 if fig=='FC-5B':
  for r in rows:
   if r['series_id']=='n734' and r['point_kind']=='feature' and r['note'].startswith('last'):
    r.update(pixel_u=2133,pixel_v=2217,v_bound_px=5.5)
  d=cfg['series']['n734'];d['last']=[2133,2217];d['t1'][-1]=d['last']
  # Prior end-cap trace coordinate is removed if it intrudes into final triangle outline.
  rows=[r for r in rows if not(r['series_id']=='n734' and r['point_kind']=='trace' and float(r['pixel_u'])==2137)]
 for sid in cfg['series']:
  rr=[r for r in rows if r['series_id']==sid];markers=[r for r in rr if r['point_kind']=='marker'];traces=[r for r in rr if r['point_kind']=='trace'];features=[r for r in rr if r['point_kind']=='feature']
  for r in features:
   if not(r['note'].startswith('first') or r['note'].startswith('last')):continue
   t=r.copy();t['point_kind']='trace';t['u_bound_px']=1;t['note']='Drawn-line ink endpoint; independently checked on endpoint crop and pixel ink audit.'
   # Explicit endpoint replaces an automatic sample at the same column.
   traces=[z for z in traces if float(z['pixel_u'])!=float(t['pixel_u'])];traces.append(t)
  extra=[]
  if fig=='FC-6C' and sid=='n1961':extra=[(795,2088.5,7),(815,2075,6.5)]
  if fig=='FC-6D' and sid=='n147':extra=[(855,2207.5,7),(895,2205,9.5)]
  for u,v,b in extra:
   t=features[0].copy();t.update(point_kind='trace',pixel_u=u,pixel_v=v,u_bound_px=1,v_bound_px=b,symbol='',note='Additional column-run reading to sample visible early stroke; n147 early ink merges with frame.' if sid=='n147' else 'Additional column-run reading on visible early stroke.');traces.append(t)
  traces.sort(key=lambda r:float(r['pixel_u']))
  for i,r in enumerate(markers+traces+features,1):r['sequence']=i;out.append(r)
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(out)
 (base/'readings.json').write_text(json.dumps(cfg,indent=1))
 subprocess.run([sys.executable,'tools/calibrate_axes.py','apply',str(base/'cal-p1/calibration.json'),str(p),str(base/'points-p1-native.csv')],check=True)
 subprocess.run([sys.executable,'tools/plot_grid.py','overlay',cfg['image'],'--points',str(p),'--box',*map(str,cfg['overlay1']),'--out',str(base/'overlay-p1.png')],check=True)
 with (base/'notes.md').open('a') as f:f.write('\nFirst/last feature coordinates are also retained as explicit endpoint trace samples, on the separately checked ink. Sampling order in delivered files is marker records, trace drawing order, feature roles.\n')
