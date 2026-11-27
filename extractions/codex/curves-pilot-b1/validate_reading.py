import csv,json
from pathlib import Path
import numpy as np

out=Path('out');summary=[];checks={};expected=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
for p in (1,2):
    with (out/f'points-p{p}.csv').open() as f:
        rd=csv.DictReader(f);assert rd.fieldnames==expected;raw=list(rd)
    native=list(csv.DictReader((out/f'points-p{p}-native.csv').open()))
    assert len(raw)==len(native)
    cal=json.loads((out/f'cal-p{p}/calibration.json').read_text())
    gaps=[]
    for sid in dict.fromkeys(r['series_id'] for r in native):
        sr=[r for r in native if r['series_id']==sid]
        assert [int(r['sequence']) for r in sr]==list(range(1,len(sr)+1))
        counts={k:sum(r['point_kind']==k for r in sr) for k in ('marker','trace','feature')}
        summary.append(dict(panel=p,series_id=sid,**counts,total=len(sr)))
        ts=[r for r in sr if r['point_kind']=='trace']
        for a,b in zip(ts,ts[1:]):
            dx=float(b['x_native'])-float(a['x_native'])
            assert dx>0
            if dx>5:gaps.append(dict(series=sid,u_from=float(a['pixel_u']),u_to=float(b['pixel_u']),dx_native=round(dx,3)))
        for r in sr:
            assert r['figure_id']=='FC-1B' and int(r['panel'])==p
            assert float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0
            uv=np.array([float(r['pixel_u']),float(r['pixel_v']),1])
            for axis in ('x','y'):
                assert abs(float(r[f'{axis}_native'])-np.dot(cal[f'a{axis}'],uv))<=0.00051
            if r['point_kind']=='marker':assert r['symbol'] in ('x','asterisk','square','plus','triangle-down','triangle-up','circle')
        if p==1:
            fs=[r['note'] for r in sr if r['point_kind']=='feature']
            for kind in ('first point','peak of drawn trace','last point'):assert any(n.startswith(kind) for n in fs)
    checks[str(p)]=dict(points=len(raw),calibration_rms_x=cal['rms_residual_x'],calibration_rms_y=cal['rms_residual_y'],calibration_max_x=cal['max_residual_x'],calibration_max_y=cal['max_residual_y'],trace_gaps_above_5=gaps)
    assert cal['rms_residual_x']<1.25
    assert cal['rms_residual_y']<(30 if p==1 else 1)
    if p==1:assert all(q['series']=='n2345' and q['u_from']>=1940 and q['u_to']<=2050 for q in gaps)
with (out/'counts.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=summary[0]);w.writeheader();w.writerows(summary)
(out/'validation.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
print('All schema, sequence, native conversion, bounds, calibration and spacing checks passed (documented n2345 drawing gap excepted).')

# By-eye grid intersections checked against fitted native coordinate values.
observed={1:[('x',0,800,2854),('x',100,1390,2843),('x',250,2270,2828),('y',6000,766,1127),('y',5000,800,1420),('y',4000,778,1709),('y',3000,783,1992),('y',0,800,2854)],
          2:[('x',0,812,3566),('x',100,1402,3556),('x',250,2285,3541),('y',100,800,2995),('y',0,806,3278),('y',-100,812,3566)]}
rows=[]
for p,pts in observed.items():
    c=json.loads((out/f'cal-p{p}/calibration.json').read_text())
    for axis,val,u,v in pts:
        fit=float(np.dot(c['a'+axis],[u,v,1]))
        rows.append(dict(panel=p,axis=axis,label_read=val,eye_u=u,eye_v=v,fitted_value=round(fit,3),difference=round(fit-val,3)))
with (out/'calibration-eye-checks.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('By-eye label checks:',rows)
