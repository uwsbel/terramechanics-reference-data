import csv,json
from pathlib import Path
FIELDS=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note']
symbols=['quarter-circle','star','triangle-up','diamond','square','circle']
idsB=['n27p1psi','n13p8psi','n10p2psi','n6p6psi','n5p1psi','n3p4psi'];idsC=['n26p5psi',*idsB[1:]]
# Lists transcribed by symbol from enlarged unrotated crops, in motion progression.
# Integers reference the helper's image components; tuples are separately read centers.
B=[
[1,2,(1541,3267,15,'Quarter-circle below touching star; baseline obscures lower outline.'),(1350,3264,8,'Quarter-circle on 20-psi gridline near baseline.'),7,9,12,17,22,28,34,40,46,52,58,64,70,76,86,87,93,95],
[(1855,3268,16,'Star touches triangle and baseline.'),8,(1558,3241,16,'Star touches quarter-circle below.'),14,18,25,(1349,3039,6,'Star crossed by 20-psi and .04-in gridlines.'),36,45,47,54,60,68,75,(1586,2058,8,'Star crossed by 15-psi and .20-in gridlines; center bounded from exposed outline.'),84,91,94,96],
[(2138,3262,16,'Triangle touches circle/square cluster and baseline.'),(1948,3266,17,'Triangle below touching diamond in origin cluster.'),(1833,3246,16,'Triangle touches star below and 10-psi gridline.'),16,24,29,35,(1564,2793,6,'Triangle on .08-in gridline; nearby short horizontal ink is not a curve.'),48,53,61,69,71,81,82,92],
[(2021,3253,18,'Diamond touches circle in origin cluster.'),(1948,3244,17,'Diamond touches circle above and triangle below.'),15,19,26,30,37,42,49,55,59,66,74,78,85,90],
[(2251,3268,16,'Square lower edge touches baseline; interior stray ink cannot establish another symbol.'),(2194,3265,16,'Square overlaps circle and baseline.'),(2095,3259,16,'Square overlaps circle.'),(1999,3231,16,'Square touches neighboring circles in origin cluster.'),20,23,33,39,43,50,56,62,65,72,77,(2023,1903,5,'Square near adjacent circle; distinct rectangular outline.'),(2041,1750,16,'Square touches circle on 5-psi gridline.')],
[(2207,3264,16,'Circle overlaps square and baseline.'),(2112,3259,16,'Circle overlaps square and triangle.'),(2036,3254,17,'Circle touches diamond.'),(1975,3219,16,'Circle touches diamond and square in origin cluster.'),(1948,3160,3,'Circle close to square; exposed circular outline.'),(1949.5,3098.5,3,'Short stray ink near circle; center read on circular outline.'),(1949.5,3038.5,5,'Circle crossed by .04-in gridline.'),(1973.5,2915,3,'Short tail is scan ink; circular outline supplies center.'),(1977.5,2792,5,'Circle crossed by .08-in gridline.'),51,(2018,2546,5,'Circle crossed by .12-in gridline; short nearby ink ignored.'),63,67,73,79,(2057,1903,6,'Circle next to square; edge joins 5-psi gridline.'),(2075,1749,16,'Circle touches square and 5-psi gridline.')]
]
C=[
[(2027,3290,17,'Quarter-circle touches star and baseline; lower curved outline partly obscured.'),2,6,11,16,21,27,(1133,2836.5,6,'Quarter-circle crossed by 25-psi and .08-in gridlines; exposed outline supplies center.'),39,45,51,57,63,69,75,81],
[(2060,3283,18,'Star touches quarter-circle and baseline.'),8,13,17,22,28,34,40,(1615,2577,8,'Star at intersection of 15-psi and .12-in gridlines; exposed outline used.'),52,59,64,70,76,82,87,88],
[4,7,12,18,23,29,35,41,48,53,58,65,(1847,2085,8,'Triangle crossed by 10-psi and .20-in gridlines; center bounded from exposed outline.'),78,(1878,1777,3,'Triangle center on outline; short horizontal tail ignored.')],
[5,10,14,19,24,31,37,42,49,55,61,67,72,79,84],
[(2220,3273,18,'Square touches circle and unidentified angular marker below.'),(2184,3238,16,'Square overlaps circle.'),(2152,3182,16,'Square overlaps circle.'),(2131,3121,16,'Square overlaps circle.'),25,(2059,2940,3,'Square center from rectangular outline; short tail ignored.'),(2040,2819,5,'Square crossed by .08-in gridline.'),(2027,2695,4,'Square center from rectangular outline; nearby horizontal ink ignored.'),47,54,60,66,73,(2078,1930,6,'Square right edge merges with 5-psi gridline.'),85],
[(2292,3283,17,'Circle bottom obscured by baseline.'),(2242,3270,17,'Circle touches square and unidentified angular marker.'),(2204,3238,16,'Circle overlaps square.'),(2166,3182,16,'Circle overlaps square.'),(2154,3121,16,'Circle overlaps square.'),26,32,38,(2102.5,2686.5,5,'Circle crossed by 5-psi gridline; nearby horizontal ink ignored.'),50,56,62,68,74,(2143.5,1926.5,3,'Circle center from round outline; short tail ignored.'),86]
]
for fig,data,sids in [('FC-7B',B,idsB),('FC-7C',C,idsC)]:
 cal=json.load(open(f'out/{fig}/cal-p1/calibration.json'));can={int(r['id']):r for r in csv.DictReader(open(f'out/{fig}/candidates.csv'))};rows=[]
 for sid,sym,entries in zip(sids,symbols,data):
  for seq,e in enumerate(entries,1):
   if isinstance(e,int):
    r=can[e];u,v=float(r['u']),float(r['v']);b=2;notes=[]
   else:u,v,b,note=e;notes=[note]
   for l in cal['vertical_lines']:
    if abs(u-l['u_at_v0']-l['slope_du_dv']*v)<20:
     notes.append(f"{l['y_value']:g}-psi gridline intersects/abuts symbol.");b=max(b,5)
   for l in cal['horizontal_lines']:
    if abs(v-l['v_at_u0']-l['slope_dv_du']*u)<21:
     notes.append(f"{l['x_value']:g}-in gridline intersects/abuts symbol.");b=max(b,5)
   if v>3240:b=max(b,15);notes.append('Crowded near origin; bound is approximately half the symbol width.')
   rows.append(dict(zip(FIELDS,[fig,1,sid,'marker',seq,u,v,b,b,sym,' '.join(notes)])))
 if fig=='FC-7C':rows.append(dict(zip(FIELDS,[fig,1,'unidentified','marker',1,2220,3290,20,20,'unidentified','Separate angular outline below square/circle pair is partly covered by baseline and neighbors. Star versus diamond cannot be identified securely; no test assigned (protocol rule 7).'])))
 with open(f'out/{fig}/points-p1.csv','w',newline='') as f:w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerows(rows)
 print(fig,len(rows),{s:sum(r['series_id']==s for r in rows) for s in sids},'unidentified',sum(r['series_id']=='unidentified' for r in rows))
 # Independent by-eye label observations at the unrotated frame. Values are only axis checks, never data rows.
 checks=([('x',.32,2310,1317),('x',.16,2313,2299),('x',.04,2315,3035),('y',30,850,3287),('y',15,1585,3285),('y',5,2073,3284)] if fig=='FC-7B' else [('x',.32,2322,1336),('x',.28,2300,1584.5),('x',.16,2338,2323),('x',.04,2350,3058),('y',30,883,3320),('y',15,1618,3310),('y',5,2108,3302)])
 with open(f'out/{fig}/calibration-eye-checks.csv','w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['figure_id','panel','axis','printed_label_read_by_eye','pixel_u','pixel_v','fitted_value','fitted_grid_position','line_source','check','note'])
  for axis,value,u,v in checks:
   a=cal['ax' if axis=='x' else 'ay'];fit=a[0]*u+a[1]*v+a[2];lines=cal['horizontal_lines' if axis=='x' else 'vertical_lines'];l=next(t for t in lines if t[axis+'_value']==value);pos=(l['v_at_u0']+l['slope_dv_du']*u if axis=='x' else l['u_at_v0']+l['slope_du_dv']*v)
   w.writerow([fig,1,axis,value,u,v,f'{fit:.6f}',f'{pos:.2f}',l['source'],'confirmed','Printed motion labels increase upward; printed load labels increase leftward.'+(' Predicted .28-in line inspected at right end: observed v=1584.5; fitted v=1582.34 (about 2.2 px difference).' if l['source']=='predicted' else '')])
