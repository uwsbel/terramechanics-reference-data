from pathlib import Path
import csv,json,subprocess,sys
fixes={
'FC-5B':{'n4695':{'last':([2105,1688],[2105,1690],3)},'n734':{'last':([2127,2224],[2137,2218.5],14)}},
'FC-6B':{'n4695':{'last':([2065,862],[2067,856],9)},'n734':{'last':([2078,2001],[2063,1995.5],10)}},
'FC-6C':{'n4695':{'last':([2063,1223],[2061,1225],17)},'n1961':{'first':([718,2145],[714,2157],1)},'n714':{'first':([725,2227],[729,2228],9)}},
'FC-6D':{'n2934':{'peak':([2212,1423.5],[2208,1423.5],12),'last':([2212,1423.5],[2208,1423.5],12)},'n147':{'peak':([2175,2166],[2175,2159.5],12)}}}
for fig,series in fixes.items():
 base=Path('out')/fig;p=base/'points-p1.csv';rows=list(csv.DictReader(p.open()));cols=list(rows[0])
 for sid,roles in series.items():
  for role,(old,new,width) in roles.items():
   for r in rows:
    if r['series_id']==sid and r['point_kind'] in ['trace','feature'] and [float(r['pixel_u']),float(r['pixel_v'])]==old:
     r['pixel_u'],r['pixel_v']=new;r['v_bound_px']=width/2
   # Features sharing an ordinate have independent roles but use same revised point.
   cfgp=base/'readings.json';cfg=json.loads(cfgp.read_text(encoding='utf-8-sig'));d=cfg['series'][sid];d[role]=new
   if role in ['first','last']:d['t1'][0 if role=='first' else -1]=new
   d.setdefault('feature_widths',{})[role]=width;cfgp.write_text(json.dumps(cfg,indent=1))
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
 cfg=json.loads((base/'readings.json').read_text());subprocess.run([sys.executable,'tools/calibrate_axes.py','apply',str(base/'cal-p1/calibration.json'),str(p),str(base/'points-p1-native.csv')],check=True)
 subprocess.run([sys.executable,'tools/plot_grid.py','overlay',cfg['image'],'--points',str(p),'--box',*map(str,cfg['overlay1']),'--out',str(base/'overlay-p1.png')],check=True)
 with (base/'notes.md').open('a') as f:
  f.write('\nFinal ink audit corrected explicit feature endpoints onto their measured dark runs (and corresponding trace samples); coordinates in the delivered CSVs supersede approximate paths in reading aids. Narrow end-cap ink has its measured half-thickness bound.\n')
p=Path('out/read_curves.py');s=p.read_text().replace("dat.get('feature_width',10)","dat.get('feature_widths',{}).get(key,dat.get('feature_width',10))");p.write_text(s)
