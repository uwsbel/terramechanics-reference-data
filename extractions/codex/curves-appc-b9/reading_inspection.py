from pathlib import Path
import sys,json,subprocess
from PIL import Image,ImageDraw
sys.path.insert(0,'tools')
import calibrate_axes as ca
spec={
'FC-12':('p0148.png',[(630,3668),(808,3505),(1100,3164),(1265,3039),(1435,2919),(1694,2650),(1865,2515),(1950,2410)]),
'FC-13':('p0147.png',[(755,3681),(1215,3415),(1396,3318),(1561,3239),(1821,3077),(1992,2949),(2077,2936)]),
'FC-14':('p0150.png',[(670,3683),(845,3624),(1148,3269),(1318,3193),(1487,2908),(1751,2655),(1933,2587),(2012,2516)]),
'FC-15':('p0151.png',[(740,3598),(908,3484),(1205,3307),(1373,2936),(1539,2821),(1800,2804),(1967,2416),(2055,2521)])}
for f,(page,markers) in spec.items():
 d=Path('out')/f
 cal,X,Y=ca.piecewise_maps(d/'cal-p1','packet/'+page)
 summary=ca.knots_summary(X,Y)
 (d/'cal-p1'/'knots-verified.json').write_text(json.dumps(summary,indent=1),encoding='utf-8')
 print(f,'verified',len(X.knots),len(Y.knots),'rejected',[(a['value'],a['reason']) for a in X.rejected+Y.rejected])
 sheets=Image.new('RGB',(4*300,2*320),'white');draw=ImageDraw.Draw(sheets)
 for i,(u,v) in enumerate(markers):
  box=[u-50,v-45,u+50,v+45]
  dest=d/f'marker-{i+1:02}.png'
  subprocess.run([sys.executable,'tools/plot_grid.py','crop','packet/'+page,'--box',*map(str,box),'--out',str(dest),'--zoom','3','--step','25'],check=True,stdout=subprocess.DEVNULL)
  sheets.paste(Image.open(dest),(i%4*300,i//4*320+35))
  draw.text((i%4*300,i//4*320),f'{f} #{i+1} center near {u},{v}',fill='black')
 sheets.save(d/'markers-inspection.png')
 im=Image.open('packet/'+page)
 # Header and label evidence, no transformations of coordinate system.
 boxes=[(1200,1000,2050,1380),(400,3650,2790,3880),(360,1330,710,3780)]
 for j,b in enumerate(boxes):
  im.crop(b).save(d/f'labels-{j}.png')
