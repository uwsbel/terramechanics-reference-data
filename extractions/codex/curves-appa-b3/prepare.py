import subprocess,sys,json
from pathlib import Path
from PIL import Image
cfg={
'FA-3':dict(page='p0008',box=[885,1850,2450,3380],yr=[25,65],area=[660,2750,2750,3410]),
'FA-7':dict(page='p0015',box=[618,1960,2190,3515],yr=[25,65],area=[400,1720,2470,2550]),
'FA-19':dict(page='p0040',box=[735,810,2350,3750],yr=[55,115],area=[530,1020,2540,2410]),
'FA-23':dict(page='p0048',box=[825,1460,2270,3740],yr=[55,100],area=[620,1290,2500,3590]),
'FA-27':dict(page='p0055',box=[650,775,2240,3720],yr=[55,115],area=[420,3110,2570,3780]),
'FA-39':dict(page='p0078',box=[855,1060,2285,3700],yr=[55,115],area=[600,1860,2510,3120]),
'FA-47':dict(page='p0096',box=[850,1040,2330,3700],yr=[55,115],area=[710,2250,2570,3050])}
Path('out/config.json').write_text(json.dumps(cfg,indent=2))
for fig,c in cfg.items():
 d=Path('out')/fig; d.mkdir(exist_ok=True)
 im=Image.open('packet/'+c['page']+'.png'); im.crop(c['area']).save(d/'trace-area.png')
 cmd=[sys.executable,'tools/calibrate_axes.py','detect','packet/'+c['page']+'.png','--box',*map(str,c['box']),'--x-values',','.join(str(x/10) for x in range(11)),'--y-values',','.join(map(str,range(c['yr'][0],c['yr'][1]+1,5))),'--y-transform','reciprocal','--y-direction','down','--out',str(d/'cal-p1'),'--bands','15','--snap','12','--min-frac','0.5']
 p=subprocess.run(cmd,capture_output=True,text=True); (d/'cal-p1-detect.log').write_text(p.stdout+p.stderr); print(fig,p.returncode,p.stdout)
