import json,subprocess,sys
from pathlib import Path
p=json.loads(Path('out/proposed-pixels.json').read_text());cfg=json.loads(Path('out/config.json').read_text())
items=[('FA-23','upper',3),('FA-23','lower',3),('FA-39','upper',8),('FA-39','lower',8),('FA-47','upper',3),('FA-27','upper',5),('FA-27','upper',7),('FA-27','lower',5)]
for fig,s,n in items:
 a=p[fig][s]['points'][n-1];u,v=round(a['u']),round(a['v']);b=[u-60,v-45,u+60,v+45];subprocess.run([sys.executable,'tools/plot_grid.py','crop','packet/'+cfg[fig]['page']+'.png','--box',*map(str,b),'--out',f'out/{fig}/check-{s}-{n}.png','--zoom','4','--step','10'],capture_output=True)
