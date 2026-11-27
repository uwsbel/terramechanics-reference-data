import json,csv
from pathlib import Path
p=Path('out/FC-1C');d=json.loads((p/'reading.json').read_text())
revised={
'n3520':[(633,3287),(714,3325),(828,3320),(934,3322),(1040,3306),(1158,3303),(1276,3290),(1393,3277),(1507,3265),(1629,3262),(1750,3247),(1873,3237),(1983,3229),(2096,3218)],
'n2935':[(654,3292),(741,3294),(846,3289),(998,3298),(1100,3287),(1219,3265),(1332,3251),(1458,3229),(1575,3212),(1699,3215),(1825,3195),(1900,3173),(2070,3162)],
'n2345':[(691,3314),(797,3317),(870,3292),(1041,3297),(1151,3280),(1276,3269),(1450,3245),(1574,3237),(1708,3215),(1819,3201),(1921,3189),(2088,3175)],
'n1760':[(628,3367),(741,3345),(921,3343),(984,3331),(1106,3318),(1220,3305),(1337,3281),(1452,3273),(1518,3255),(1574,3261),(1708,3233),(1820,3228),(1921,3216),(2120,3178)],
'n1172':[(628,3322),(740,3314),(866,3313),(980,3289),(1219,3238),(1339,3220),(1453,3199),(1576,3178),(1699,3169),(1820,3147),(1920,3134),(2094,3110)],
'n587':[(628,3294),(691,3290),(803,3268),(921,3247),(1040,3223),(1159,3197),(1277,3166),(1453,3117),(1513,3101),(1628,3074),(1740,3048),(1860,3027),(1978,3009)],
'n294':[(740,3274),(860,3246),(977,3231),(1096,3196),(1219,3166),(1339,3128),(1459,3093),(1569,3066),(1689,3045)]}
for s,pts in revised.items():
    d['p2'][s]['markers']=[[*pt,6,'closely spaced symbol cluster; center checked in 10-pixel-grid crop'] if pt[0]<1225 and s not in ['n587','n294'] else list(pt) for pt in pts]
d['p2']['n3520']['markers'][8]=[1507,3265,8,'x overlaps plus and vertical grid; center uncertain']
d['p2']['n1760']['markers'][8]=[1518,3255,8,'plus and x near 150 grid; center/identity uncertain']
(p/'reading.json').write_text(json.dumps(d,indent=2))
checks=[]
for panel,axis,ref,eyes in [(1,'x',2000,[(0,623),(100,1214),(250,2088)]),(1,'y',700,[(6000,1109),(4000,1693),(0,2847)]),(2,'x',3500,[(0,631),(100,1222),(250,2094)]),(2,'y',700,[(100,2992),(0,3276),(-100,3563)])]:
    cal=json.loads((p/f'cal-p{panel}/calibration.json').read_text())
    for val,eye in eyes:
        ls=cal['vertical_lines' if axis=='x' else 'horizontal_lines'];key='x_value' if axis=='x' else 'y_value'
        l=next(l for l in ls if l[key]==val)
        fit=l['u_at_v0']+l['slope_du_dv']*ref if axis=='x' else l['v_at_u0']+l['slope_dv_du']*ref
        checks.append(['FC-1C',panel,axis,val,f'{fit:.2f} at '+('v=' if axis=='x' else 'u=')+str(ref),eye])
with (p/'calibration-eye-checks.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['figure','panel','axis','printed_label','fitted_pixel','eye_pixel']);w.writerows(checks)
(p/'notes.md').write_text('''# FC-1C independent reading

Only packet/p0118.png, packet tables and the packet protocol were used. Coordinates refer to the unrotated 3263 x 4508 image. Markers were read before traces in zoom-3 and zoom-4 labeled grid crops. The lower-panel centers were checked again in three smaller crops with a 10-pixel grid. There are no lower-panel connecting curves.

Both panels use the six labeled vertical lines x=0,50,100,150,200,250, excluding the unlabeled legend frame beyond 250 from calibration. Upper y=0..6000 psf; lower y=-100..100 thousandths. Eye checks at the reference coordinates are in calibration-eye-checks.csv. All inspected fitted/eye positions agree within about 2 px. The predicted 5000 line is visible at v~1399 near the left/right sides of the interrupted annotation; it was explicitly checked. Upper RMS residuals: x=0.4089 thousandths, y=7.9098 psf; lower x=0.3696 thousandths, y=0.2226 thousandths. All are below 0.5% of span.

Legend identities: x=3520; asterisk=2935; square=2345; plus=1760; triangle-down=1172; triangle-up=587; circle=294. No legend misprint identified.

Upper n3520/n2935 share or approach the rising stroke near x~50. The distinct lower branch first visibly separates near (968,1852); no additional unresolvable n2935 observations are invented along the shared earlier stroke. n2345 has a shallow first maximum, a dip, and a second slightly higher maximum; these are kept as separate features. Its square centers and the author curve's maxima differ. The n587 triangle near (1039,2467) has doubled/dark ink. n587's broad plateau and n294's broad maximum do not identify a unique peak abscissa; peak feature bounds are widened. Several terminal symbols sit beside the x=250 grid or just beyond it; they are retained without clipping.

Lower-panel early symbols touch the zero line and one another. Bounds are widened in the cluster; no claim of a 2-px center is made there. The x/plus cluster at (1507..1518,3255..3265) is particularly uncertain in center and identity. Near x=200, square/down-triangle/plus have vertical-grid ink; the asterisk lies immediately to the right. At the right end the plus (2120,3178) is beyond x=250. Every identified symbol is included. No unattested lower-panel origin marker was manufactured; the frame cluster has wide bounds.

Trace sampling uses actual dark-run centers in columns spaced nominally 18 px (~3.1 thousandths), displaced up to 6 px to avoid vertical grid lines, hollow marker edges and dash gaps. Hand-read paths only choose the appropriate ink run, never generate an ordinate. The uncertainty is half the observed run thickness. The sample files trace-gaps-p1-*.json record columns where no separate author-line ink was readable; these are genuine symbol/dash/grid interruptions, not interpolated observations. A sample gap can exceed 5 thousandths when the drawn curve itself is interrupted by a symbol or grid. Features and marker centers provide additional readings at those locations. The overlays were checked against the page after the lower-panel revision.
''',encoding='utf-8')
