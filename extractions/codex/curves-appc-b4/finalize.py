import csv,json,collections
from pathlib import Path
for fig,page in [('FC-7B','p0136.png'),('FC-7C','p0137.png')]:
 root=Path('out')/fig;cal=json.loads((root/'cal-p1/calibration.json').read_text());rows=list(csv.DictReader((root/'points-p1-native.csv').open()));cols=list(rows[0])
 for r in rows:
  u,v,bu,bv=[float(r[k]) for k in ['pixel_u','pixel_v','u_bound_px','v_bound_px']];ax,ay=cal['ax'],cal['ay']
  r['x_native']=f'{ax[0]*u+ax[1]*v+ax[2]:.6f}';r['y_native']=f'{ay[0]*u+ay[1]*v+ay[2]:.6f}'
  r['x_read_bound']=f"{abs(ax[0])*bu+abs(ax[1])*bv+cal['rms_residual_x']:.6f}";r['y_read_bound']=f"{abs(ay[0])*bu+abs(ay[1])*bv+cal['rms_residual_y']:.6f}"
 with (root/'points-p1-native.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows(rows)
 counts=collections.Counter(r['series_id'] for r in rows);state='Dr 1.0, gamma 89 PCF' if fig=='FC-7B' else 'Dr 0.53, gamma 82 PCF'
 notes=f'''# {fig}: independent blind reading

Source: packet/{page}, unrotated 300-dpi image, printed page {'C-22' if fig=='FC-7B' else 'C-23'}. RSM-b; {state}. Only the supplied packet and its protocol were used. Context p0115 and p0135 was inspected for experiment context; no coordinates were read from the failure-envelope figure.

## Axes and independent label checks

Horizontal motion is x in inches (0 to .32); horizontal load is y in psi (0 to 35). The printed motion labels increase UP the scanned page; the load labels increase LEFT. Pixel u increases rightward and v downward. Calibration used tools/calibrate_axes.py detect with --x-direction up --y-direction left, 72 grid intersections, 5 bands, dark=200, min-frac={cal['min_frac']}. The frame box and full fitted line parameters are in cal-p1/calibration.json.

RMS residual: x={cal['rms_residual_x']:.9f} inch ({100*cal['rms_residual_x']/.32:.4f}% of span); y={cal['rms_residual_y']:.9f} psi ({100*cal['rms_residual_y']/35:.4f}% of span). Maximum residual: x={cal['max_residual_x']:.9f} inch; y={cal['max_residual_y']:.9f} psi. These pass the 0.5%-of-span criterion.

By-eye printed labels: x=.04, .16, .32; y=5, 15, 30. Their independently inspected unrotated grid positions and fitted values are in calibration-eye-checks.csv. All six confirm the correct directions. '''
 if fig=='FC-7B':notes+='All gridlines were detected in all five bands. No predicted lines.\n'
 else:notes+='The additional x=.28 check inspects the sole predicted line. Its right-end ink is at v=1584.5 at u=2300, versus the fitted line v=1582.34 (2.16 px). The printed .28 label and visible line confirm it. The initial min-frac=.6 detection predicted both 30 psi and .28 in; lowering to .4 detected 30 psi in all five bands. Final calibration has only .28 in predicted.\n'
 notes+='''
## Symbols, identity, and ordering

The printed normal stresses match the packet series IDs. Symbols, described with the figure upright: highest stress=quarter-circle (open D-shaped/rounded quadrant), 13.8=star, 10.2=triangle-up, 6.6=diamond, 5.1=square, 3.4=circle. No legend-number correction is required. Legend gamma values match the supplied state.

Every output point is point_kind=marker, panel=1. There are no trace, feature, or gridline data rows. The sequence lists visible markers in their loading/motion progression from the baseline toward the top of the page; no interpolated points or hidden extra symbols were created. With symbols only there is no drawn path establishing a separate unloading branch.

Marker counts:

'''
 for sid,n in counts.items():notes+=f'- {sid}: {n}\n'
 notes+=f'\nTotal: {len(rows)} marker rows.\n'
 notes+='''
## Bounds and ambiguities

Clean marker centers have 2-px half-bounds. Gridline interference is noted per point and generally receives 5 px; difficult intersections receive 6-8 px. Touching symbols and symbols obscured by the baseline receive approximately half-symbol-size bounds of 15-18 px. Such bounds express reading uncertainty, not standard deviations. Distinct outlines establish the identities even when their centers have broad bounds. Short isolated horizontal ink and tails were not sampled as curves. Helper component detection was used only to locate candidate ink; merged components were split and their identities checked by eye on the enlarged crops.

'''
 if fig=='FC-7B':notes+='''Crowded groups include quarter-circle/star pairs near (1541,3267)/(1558,3241), triangle/star near (1833,3246)/(1855,3268), diamond/circle/square/triangle near u=1948-2036, v=3219-3266, square/circle/triangle near u=2095-2138, and square/circle near u=2194-2207. At the longest displacement the square and circle near (2041,1750)/(2075,1749) touch across the 5-psi gridline. Each distinct visible outline is separately recorded. The square at (2251,3268) has interior stray ink and meets the baseline; there is insufficient evidence to add another hidden symbol. No series identity remains unassigned among the 107 recorded markers.
'''
 else:notes+='''One separately visible angular marker at (2220,3290), below the square/circle pair at approximately (2220,3273)/(2242,3270), is partly hidden by the baseline and neighbors. Its outline cannot securely distinguish star from diamond. It is included as series_id=unidentified, symbol=unidentified, with 20-px half-bounds, and is excluded from the six assigned-series counts. This explicitly follows protocol rule 7: no series assigned by guess. The uncertainty includes shape/identity, not merely center location. It remains for adjudication from the page.

Other touching groups are quarter-circle/star near (2027,3290)/(2060,3283), square/circle near (2184,3238)/(2204,3238), (2152,3182)/(2166,3182), and (2131,3121)/(2154,3121). The first circle (2292,3283) meets the baseline. Their per-row bounds and notes retain this uncertainty. No invisible initial point was inferred.
'''
 notes+='''
## Files and verification

Required files: cal-p1/anchors.csv, cal-p1/calibration.json, calibration-eye-checks.csv, points-p1.csv, points-p1-native.csv, overlay-p1.png, and notes.md. Supporting enlarged unrotated pixel-grid crops, candidate contact sheets, and overlay crops are retained here. Own helpers are under out/; tools/ was not changed.

The native conversion was run with tools/calibrate_axes.py apply. Its three-decimal rounding would discard some small inch bounds, so a helper retained the SAME affine conversion and bound formula at six decimals: |axis coefficient u|*u_bound + |axis coefficient v|*v_bound + RMS residual. No uncertainty was rounded to zero. Native x units are inch; native y units are psi.

Final overlay was checked against the full plot and enlarged origin crops. Row counts, panel/kind, positive bounds, unique per-series sequences, and equality of raw/native marker identifiers were checked. Coordinates remain in the unrotated scan throughout.
'''
 (root/'notes.md').write_text(notes,encoding='utf-8')
 raw=list(csv.DictReader((root/'points-p1.csv').open()));assert len(raw)==len(rows)
 assert [(r['series_id'],r['sequence'],r['pixel_u'],r['pixel_v']) for r in raw]==[(r['series_id'],r['sequence'],r['pixel_u'],r['pixel_v']) for r in rows]
 assert all(r['panel']=='1' and r['point_kind']=='marker' and float(r['x_read_bound'])>0 and float(r['y_read_bound'])>0 for r in rows)
 assert len(set((r['series_id'],r['sequence']) for r in rows))==len(rows)
 for sid,n in counts.items():assert [int(r['sequence']) for r in rows if r['series_id']==sid]==list(range(1,n+1))
 print(fig, 'validated',len(rows),'markers; native bounds preserved; notes written')
