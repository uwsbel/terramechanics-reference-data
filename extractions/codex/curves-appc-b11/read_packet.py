from pathlib import Path
import sys, json, subprocess
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca
from PIL import Image
tiles={20:[(770,2820,1330,3370),(1250,2350,1810,3070),(1750,2120,2400,2700)],21:[(570,1910,1400,2110),(2290,2160,2480,2290)],22:[(1640,1940,1730,2070),(2300,1500,2390,1630)],23:[(780,1410,2690,3300)]}
for n,boxes in tiles.items():
 d=Path(f'out/FC-{n}'); im=f'packet/p0{136+n}.png'
 cal,X,Y=ca.piecewise_maps(d/'cal-p1',im)
 (d/'cal-p1/verified-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 print(n,'verified',len(X.knots),len(Y.knots),'rejected',[(k['value'],k['reason']) for k in X.rejected+Y.rejected])
 for i,b in enumerate(boxes):
  subprocess.run([sys.executable,'tools/plot_grid.py','crop',im,'--box',*map(str,b),'--out',str(d/f'crop-{i}.png'),'--zoom','1' if n==23 else '3','--step','100' if n==23 else '25'],check=True)
