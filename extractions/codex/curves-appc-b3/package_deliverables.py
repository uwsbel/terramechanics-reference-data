import csv,json,zipfile
from pathlib import Path
figs=['FC-5B','FC-6B','FC-6C','FC-6D'];lines=['# Blind reading: curves-appc-b3','', 'Evidence confined to the supplied packet. No other reading used.','', '## Counts','', 'M = markers; T = trace samples; F = features. Lower panels contain markers only.','', '| Figure | Series | P1 M | P1 T | P1 F | P1 total | P2 M |','|---|---|---:|---:|---:|---:|---:|']
for fig in figs:
 rr=list(csv.DictReader((Path('out')/fig/'counts.csv').open()));upper=[r for r in rr if r['panel']=='1'];lower={r['series_id']:r for r in rr if r['panel']=='2'}
 for r in upper:lines.append(f"| {fig} | {r['series_id']} | {r['markers']} | {r['traces']} | {r['features']} | {r['total']} | {lower[r['series_id']]['markers']} |")
lines+=['','## Calibration residuals','', 'RMS x is in thousandths inch. RMS upper y is psf; lower y is thousandths inch.','', '| Figure | Panel | RMS x | RMS y |','|---|---:|---:|---:|']
for r in csv.DictReader(open('out/summary.csv')):lines.append(f"| {r['figure_id']} | {r['panel']} | {float(r['rms_x_native']):.3f} | {float(r['rms_y_native']):.3f} |")
lines+=['','## Review limitations','', '- FC-5B: touching lower triangles; grid/frame markers; wider first displacement bay; heading gamma 97.3 differs from legend 97.6.','- FC-6B: lower square series not identifiable and omitted; x calibration RMS exceeds 0.5% in both panels despite correct grid detection and revised thresholds. Printed -100 lower label is displaced from nominal scale.','- FC-6C: upper plus/down-triangle traces share horizontal grid ink; lower circles touch zero; only two lower y numerals visible, so central zero line is checked as inferred/unlabelled. Legend confirms 1961 and 714.','- FC-6D: plus/down-triangle stacks; three rebound symbols beyond x=250, with their interpretation flagged; potential upper n147 marker at x~50 and lower plus/circle rebound markers cannot be separately found. Legend confirms 3814 and 147.','- Trace sampling nominally every 20 px (~3.4 thousandths) within visible ink, with explicit first/last ink endpoints. Gaps around marker outlines/dashes are preserved and can exceed 5 thousandths under protocol rule 7. No interpolation through these gaps. Shared grid/curve ink and initial n147 frame overlap carry wider bounds.','- Pixel audit confirms all delivered trace/feature coordinates lie on dark image pixels; this checks ink presence, not independently the curve identity. Overlay review is also recorded in per-figure notes.','', '## Files','']
required=['cal-p1/anchors.csv','cal-p1/calibration.json','cal-p2/anchors.csv','cal-p2/calibration.json','calibration-eye-checks.csv','points-p1.csv','points-p1-native.csv','points-p2.csv','points-p2-native.csv','overlay-p1.png','overlay-p2.png','notes.md','counts.csv']
for fig in figs:
 lines.append('In `out/'+fig+'/`:')
 lines.extend('- `'+name+'`' for name in required);lines.append('')
lines+=['Reading aids (readings.json, enlarged labeled crops, helper scripts) remain under out/. The ZIP contains the required deliverables and this summary, rather than temporary reading aids.']
Path('out/READING-SUMMARY.md').write_text('\n'.join(lines))
with zipfile.ZipFile('out/curves-appc-b3.zip','w',zipfile.ZIP_DEFLATED) as z:
 for fig in figs:
  for name in required:
   p=Path('out')/fig/name;z.write(p,arcname=fig+'/'+name)
 for name in ['READING-SUMMARY.md','summary.csv']:
  z.write('out/'+name,arcname=name)
print('Bundle created; required files:',len(figs)*len(required),'point records:',sum(int(r['total_points']) for r in csv.DictReader(open('out/summary.csv'))))
