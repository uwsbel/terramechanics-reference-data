import json,csv,sys
from pathlib import Path
p=Path('out')/sys.argv[1];d=json.loads((p/'reading.json').read_text());meta=json.loads((p/'metadata.json').read_text());checks=[]
for panel,axis,ref,eyes in meta['eye_checks']:
    cal=json.loads((p/f'cal-p{panel}/calibration.json').read_text())
    for val,eye in eyes:
        ls=cal['vertical_lines' if axis=='x' else 'horizontal_lines'];key='x_value' if axis=='x' else 'y_value'
        l=next(l for l in ls if l[key]==val)
        fit=l['u_at_v0']+l['slope_du_dv']*ref if axis=='x' else l['v_at_u0']+l['slope_dv_du']*ref
        checks.append([sys.argv[1],panel,axis,val,round(fit,3),eye])
with (p/'calibration-eye-checks.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['figure','panel','axis','printed_label','fitted_pixel','eye_pixel']);w.writerows(checks)
notes=meta['notes']+'\n\nEye-check reference coordinates: '+str(meta['eye_checks'])+'\n\n'
for panel in [1,2]:
    cal=json.loads((p/f'cal-p{panel}/calibration.json').read_text());notes+=f"Panel {panel} calibration RMS: x={cal['rms_residual_x']:.6f}, y={cal['rms_residual_y']:.6f}; maximum residual x={cal['max_residual_x']:.6f}, y={cal['max_residual_y']:.6f}. Units are those printed on the respective axes.\n\n"
notes+='''Markers were read before traces in labeled zoom-3/4 crops; local symbol templates from this same page were then used only inside the hand-read neighborhoods to check placement. Cropped overlays were inspected. Bounds are 2 px for a clean by-eye center, 4 px where the center check has some stroke/shape uncertainty, and larger where ink is shared or a grid line passes through the marker. No markers from the legend are counted. The lower panel has no connecting author curves.

Upper traces are actual dark-run centers at nominal 12-pixel column intervals, with nearby columns selected to avoid vertical grids and dash gaps. Hand paths only identify the relevant ink run; ordinates are not interpolated from markers. Several measured markers depart significantly from the author fit and are therefore retained separately from the fitted trace. Clean trace vertical bounds are half the observed ink thickness. If the author line shares marker ink, a 16-pixel vertical bound records that its ordinate is not separately resolved from the symbol; if the author line shares horizontal-grid ink, the vertical bound is at least 8 pixels. These cases are explicitly noted per row and do not claim a clean line center. Unreadable target columns are listed in trace-gaps-p1-*.json; neighboring samples retain displacement gaps under five thousandths, as audited in out/trace-coverage.csv. Features record the first, maximum and last visible curve positions; broad maxima have wider bounds. Any short initial reversal is described above and preserved in drawing order.
'''
(p/'notes.md').write_text(notes,encoding='utf-8')
