import subprocess,sys,json
from pathlib import Path
cfg=json.loads(Path('out/config.json').read_text())
regions={
'FA-4':[[810,1900,1360,2190],[1340,1660,1890,1960],[1870,1470,2410,1730]],
'FA-8':[[840,1950,1380,2090],[1360,1770,1900,1980],[1880,1600,2420,1810]],
'FA-20':[[790,2230,1330,2530],[1310,1970,1850,2260],[1830,1730,2370,2030]],
'FA-24':[[765,1960,1300,2180],[1280,1660,1830,1990],[1810,1350,2350,1720]],
'FA-28':[[740,2970,1280,3260],[1260,2510,1810,3060],[1790,2260,2335,2550]],
'FA-48':[[770,2240,1310,2570],[1290,1860,1830,2280],[1810,1530,2365,1900]],
}
for f,rs in regions.items():
 for i,b in enumerate(rs):
  subprocess.run([sys.executable,'tools/plot_grid.py','crop','packet/'+cfg[f]['page']+'.png','--box',*map(str,b),'--out',f'out/{f}/trace-grid-{i+1}.png','--zoom','3','--step','25'],check=True,capture_output=True)
