"""Write this blind reading's eye-check records, notes, and consistency audit."""
import argparse,csv,json,sys
from pathlib import Path
from collections import Counter
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import calibrate_axes as ca

DETAIL={
16:('RS',3517,640,'Four horizontal pairs, numbered from the left, and three single circles at the right frame. Pair 1 left is bisected by the left frame. The three right-frame singles are bisected by the frame and overlap respectively upper, mean, and lower. Pair 4 right lies outside the right frame; its horizontal connector crosses the frame. The mean left terminal merges with pair 1 left and the frame. The lower right terminal merges with the lowest right-frame circle. Endpoint traces stop at separately identifiable curve ink; feature intervals include the obscured terminal. The upper and mean extend outside the right frame. No symbol was omitted.'),
17:('PS',3590,730,'One horizontal pair and four singles. The rightmost single is outside the right frame and has a small interior ink speck; it is still an open circle, not another marker. The upper curve and mean meet the right frame; lower extends slightly beyond it. No circle is cut by the frame. Several circles intersect curves or vertical grid lines; their bounds are widened. No symbol was omitted.'),
18:('RSM-a',3438,740,'One horizontal pair and four singles. The two touching circles near (927,2540) and (947,2516) are distinct circles; both get 18 px bounds, and the upper one also touches mean. The pair left overlaps upper and the pair right lies on mean. The lowest left single overlaps lower. The upper right single is on a vertical grid line. No circle is cut by the frame. The upper left terminal is merged with the pair-left circle; its feature interval includes the obscured terminal. All three curves meet the right frame. No symbol was omitted.'),
19:('RC2',3580,814,'Two single open circles; no horizontal pairs. The left circle overlaps mean and the Dr=0 grid line. The mean left terminal merges with that circle, so the first trace position is on the first separately identifiable mean ink; its feature interval includes the obscured terminal. No circle is cut by the frame. All three curves end at approximately the labelled Dr=1 line, well inside the right frame. No symbol was omitted.')}

def write_csv(path,rows):
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--run',action='store_true');a=ap.parse_args()
 if not a.run:return
 summaries=[];sens=[]
 for n,(soil,bottom,left,detail) in DETAIL.items():
  folder=Path(f'out/FC-{n}');calpath=folder/'cal-p1/calibration.json';cal=json.loads(calpath.read_text())
  cal.update(x_quantity='relative density Dr',x_unit='none',y_quantity='direct-shear angle of internal friction phi_DS',y_unit='deg',reader='independent blind page reading',calibration_region_note='box selects labelled Dr=0..1 and phi=30..50 grid lines; unlabelled frame extensions are not anchors')
  calpath.write_text(json.dumps(cal,indent=2),encoding='utf-8')
  checks=[]
  for val,label in [(0,'0'),(.5,'0.5'),(1,'1.0')]:
    line=next(l for l in cal['vertical_lines'] if l['x_value']==val);u=line['u_at_v0']+line['slope_du_dv']*bottom
    checks.append(dict(figure_id=f'FC-{n}',panel=1,axis='x',printed_label=label,value=val,pixel_u=round(u,2),pixel_v=bottom,checked_by_eye='yes',note='Printed Dr label below bottom frame checked against this interior vertical grid line; frame is not the 0 or 1.0 line.'))
  for val in [30,40,50]:
    line=next(l for l in cal['horizontal_lines'] if l['y_value']==val);v=line['v_at_u0']+line['slope_dv_du']*left
    checks.append(dict(figure_id=f'FC-{n}',panel=1,axis='y',printed_label=str(val),value=val,pixel_u=left,pixel_v=round(v,2),checked_by_eye='yes',note='Printed degree label left of frame checked against this horizontal grid line.'))
  write_csv(folder/'calibration-eye-checks.csv',checks)
  native=list(csv.DictReader((folder/'points-p1-native.csv').open()));counts=Counter((r['series_id'],r['point_kind']) for r in native)
  knots=json.loads((folder/'cal-p1/verified-knots.json').read_text());assert len(knots['x'])==11 and len(knots['y'])==5 and not knots['rejected_x'] and not knots['rejected_y']
  im=Image.open(f'packet/p{n+136:04d}.png').convert('L');off=[]
  for r in native:
    if r['point_kind']=='trace' and im.getpixel((round(float(r['pixel_u'])),round(float(r['pixel_v']))))>=160:off.append((r['series_id'],r['sequence']))
  assert not off,(n,off)
  for s in ['data','mean','upper','lower']:
    rs=[r for r in native if r['series_id']==s]
    dx=max(abs(float(r['x_native'])-(cal['ax'][0]*float(r['pixel_u'])+cal['ax'][1]*float(r['pixel_v'])+cal['ax'][2])) for r in rs)
    dy=max(abs(float(r['y_native'])-(cal['ay'][0]*float(r['pixel_u'])+cal['ay'][1]*float(r['pixel_v'])+cal['ay'][2])) for r in rs)
    sens.append(dict(figure_id=f'FC-{n}',series_id=s,max_abs_x_piecewise_minus_affine=round(dx,7),max_abs_y_piecewise_minus_affine_deg=round(dy,5)))
  omitted=(folder/'omitted-samples.txt').read_text().strip()
  text=f'''Independent blind reading of Figure C-{n}, printed page C-{n+22}, packet/p{n+136:04d}.png, panel 1. Only this packet and its protocol were used. Pixel coordinates refer to the original, unrotated 300 dpi page, u right and v down.

Printed soil: "{soil} Soil"; agrees with series.csv. data is every open circle, mean is the continuous solid curve, upper/lower are the dashed curves respectively above/below mean. Horizontal pair connectors are not curve traces. All three curves increase throughout; the right endpoint is also the peak. No separately defensible knee or kink is visible, so each trace has two feature rows (first and last/peak). No identity inference from an earlier data sheet was needed; all symbols have the same data identity. Rules 8 and 9 require no additional disambiguation here.

Calibration uses only the printed interior Dr grid lines 0, 0.1, ... 1.0 and the degree lines 30,35,40,45,50. The numerical anchors are not the outer frame. All 11 x and 5 y lines passed the independent page-ink check; no predicted or rejected line is used. By-eye checks recorded for x labels 0, 0.5, 1.0 and y labels 30, 40, 50; the intervening printed labels were also inspected. Units: x none, y deg. Both vertical frames lie about one grid interval beyond the labelled range (roughly Dr=-0.1 and 1.1, inferred only, not printed values). The top and bottom frames likewise extend beyond the labelled angle lines; they were not assigned calibration values.

Affine diagnostic RMS residuals: x {cal['rms_residual_x']:.8f} Dr, y {cal['rms_residual_y']:.6f} deg. Maximum residuals: x {cal['max_residual_x']:.8f} Dr, y {cal['max_residual_y']:.6f} deg. All are below 0.5% of the calibrated span. Native values and bounds use the verified piecewise grid map with each line's own tilt and location interval, not the affine map or its global residual. Beyond the verified labelled lines, cal_model flags extrapolation. cal-p1/verified-knots.json records the ink tests and line location errors; calibration-sensitivity.csv records the largest piecewise-versus-affine change by series.

{detail}

Markers were read before traces. Clean circle centers have 2 px bounds; grid overlaps and specks 3-5 px; curve overlaps 18 px; frame-bisected circles 20 px; touching circles 18 px. Circle centers were located from the visible annulus, checked on enlarged pixel-grid crops; no filled-in intersection was treated as an extra symbol. Trace samples are measured centers of curve ink with half the local stroke thickness (usually 2.5-6 px). End-cap bounds use half the adjacent stroke, 4.5 px. No line is traced along a horizontal pair connector. Each curve is sampled from its first visible ink, then nominal Dr multiples of 0.05, and finally its last visible ink. Dashed samples in gaps are displaced to nearby visible dash ends, and actual displacement is recorded in each note; samples at grid crossings follow the identifiable diagonal branch, using adjoining curve ink to locate its center. No sample is placed on a circle outline or a dash-gap grid crossing. Where a circle prevents a solid curve reading at its nominal abscissa, the sample is omitted rather than displaced:

{omitted if omitted else 'No solid-curve sample omitted.'}

Terminal locations obscured by circles are explicitly labelled as identifiable-ink limits; the corresponding feature intervals are wider (35 px u, 20 px v) to include the merged terminal, without guessing a hidden pixel center. trace-ink-check.png is a labelled contact sheet of every trace position at 3x enlargement. overlay-p1.png is the full-page unrotated overlay: data red, mean green, upper blue, lower ochre. Counts: data markers {counts['data','marker']}; mean traces/features {counts['mean','trace']}/{counts['mean','feature']}; upper {counts['upper','trace']}/{counts['upper','feature']}; lower {counts['lower','trace']}/{counts['lower','feature']}.
'''
  (folder/'notes.md').write_text(text,encoding='utf-8')
  summaries.append(dict(figure_id=f'FC-{n}',data_markers=counts['data','marker'],mean_traces=counts['mean','trace'],mean_features=counts['mean','feature'],upper_traces=counts['upper','trace'],upper_features=counts['upper','feature'],lower_traces=counts['lower','trace'],lower_features=counts['lower','feature'],rms_residual_x=cal['rms_residual_x'],rms_residual_y_deg=cal['rms_residual_y'],max_residual_x=cal['max_residual_x'],max_residual_y_deg=cal['max_residual_y'],verified_x_lines=11,verified_y_lines=5))
 write_csv(Path('out/reading-summary.csv'),summaries);write_csv(Path('out/calibration-sensitivity.csv'),sens)
 print(json.dumps(summaries,indent=2))

if __name__=='__main__':main()
