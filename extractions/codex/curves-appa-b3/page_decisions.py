import json
from pathlib import Path
p=json.loads(Path('out/final-pixels.json').read_text())
changes={
 'FA-3':{'upper':{6:(1650,2948,3.5),10:(2270,3078,4)}},
 'FA-7':{'lower':{4:(1082,2077,3.5),8:(1717,2311,3.5)}},
 'FA-23':{'upper':{7:(1654,2111,3.5)},'lower':{3:(1140,2731,3.5)}},
 'FA-27':{'upper':{6:(1459,3364,3.5),7:(1620,3411,3.5)},'lower':{8:(1762,3528,3.5)}},
 'FA-47':{'lower':{9:(2018,2874,3.5)}}}
for fig,ss in changes.items():
 for sid,points in ss.items():
  for n,(u,v,b) in points.items():
   p[fig][sid]['points'][n-1].update(u=u,v=v,bound=b,note=f'target Dr={(n-1)/10:.1f}; gap: nearest dash end checked by eye; grid ink excluded')
Path('out/final-pixels.json').write_text(json.dumps(p,indent=2))
