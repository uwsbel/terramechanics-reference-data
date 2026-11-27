import csv,json,math
from pathlib import Path
root=Path('out');figs=['FC-1C','FC-1D','FC-2B','FC-2C']
cols=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
assertions=[];coverage=[];counts=[];cals=[]
for fig in figs:
    p=root/fig
    eye=list(csv.DictReader((p/'calibration-eye-checks.csv').open()))
    assert all(sum(int(r['panel'])==panel and r['axis']==axis for r in eye)>=3 for panel in [1,2] for axis in ['x','y'])
    for panel in [1,2]:
        cal=json.loads((p/f'cal-p{panel}/calibration.json').read_text());cals.append([fig,panel,cal['rms_residual_x'],cal['rms_residual_y'],cal['max_residual_x'],cal['max_residual_y']])
        with (p/f'points-p{panel}.csv').open() as f:
            rd=csv.DictReader(f);assert rd.fieldnames==cols;rows=list(rd)
        with (p/f'points-p{panel}-native.csv').open() as f:
            rd=csv.DictReader(f);assert rd.fieldnames==cols+['x_native','y_native','x_read_bound','y_read_bound'];native=list(rd)
        assert len(rows)==len(native)>0
        series=list(dict.fromkeys(r['series_id'] for r in rows))
        for sid in series:
            sub=[r for r in rows if r['series_id']==sid]
            ns=[r for r in native if r['series_id']==sid]
            cc={kind:sum(r['point_kind']==kind for r in sub) for kind in ['marker','trace','feature']}
            counts.append([fig,panel,sid,cc['marker'],cc['trace'],cc['feature'],len(sub)])
            for kind in ['marker','trace','feature']:
                rr=[r for r in sub if r['point_kind']==kind]
                assert [int(r['sequence']) for r in rr]==list(range(1,len(rr)+1))
            if panel==1:
                tt=[r for r in ns if r['point_kind']=='trace']
                gaps=[abs(float(b['x_native'])-float(a['x_native'])) for a,b in zip(tt,tt[1:])]
                assert all(g<=5 for g in gaps),(fig,sid,'trace gap exceeds five thousandths')
                ff=[r for r in ns if r['point_kind']=='feature']
                first=next(r for r in ff if 'first' in r['note'])
                last=next(r for r in ff if 'last' in r['note'])
                assert abs(float(first['x_native'])-float(tt[0]['x_native']))<=5
                assert abs(float(last['x_native'])-float(tt[-1]['x_native']))<=5
                # Combined readings show marker interruptions and distinct off-fit observations.
                coverage.append([fig,sid,len(tt),round(max(gaps,default=0),3),sum(g>5 for g in gaps),'See gap JSON and notes: line is interrupted by symbols/dashes/grid; no ordinate interpolation'])
                assert cc['feature']>=3 and cc['trace']>0
            else:assert cc['trace']==0 and cc['feature']==0
        for r,n in zip(rows,native):
            assert r['figure_id']==fig and int(r['panel'])==panel
            assert r=={k:n[k] for k in cols}
            for k in ['pixel_u','pixel_v','u_bound_px','v_bound_px']:
                assert math.isfinite(float(r[k]))
            assert float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0
            assert float(n['x_read_bound'])>0 and float(n['y_read_bound'])>0
            assert r['point_kind'] in ['marker','trace','feature']
        assert (p/f'overlay-p{panel}.png').exists()
    assertions.append(f'{fig}: schemas, native conversions, sequences, bounds, 12 eye checks, features, overlays, and trace gaps <=5 thousandths verified.')
def write(path,columns,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(columns);w.writerows(rows)
write(root/'counts.csv',['figure_id','panel','series_id','markers','traces','features','total'],counts)
write(root/'calibration-summary.csv',['figure_id','panel','rms_x','rms_y','max_x','max_y'],cals)
write(root/'trace-coverage.csv',['figure_id','series_id','trace_count','maximum_x_gap_native','gaps_over_5','note'],coverage)
(root/'validation.txt').write_text('\n'.join(assertions)+'\nNo other reader outputs were accessed.\n',encoding='utf-8')
manifest=[[str(p).replace('\\','/'),p.stat().st_size] for p in sorted(root.rglob('*')) if p.is_file() and p.name!='manifest.csv']
write(root/'manifest.csv',['path','bytes'],manifest)
print('\n'.join(assertions));print('Trace coverage:',coverage)
print('Counts:',counts);print('Calibration:',cals)
