import json
from pathlib import Path
from PIL import Image,ImageDraw
p=json.loads(Path('out/final-pixels.json').read_text());cfg=json.loads(Path('out/config.json').read_text())
source=Path('out/finalize_pixels.py').read_text();exec(source[source.index('# Rebuild sample crops'):])
checks=json.loads(Path('out/file-validation.json').read_text());assert all(not r['white_trace_centres'] for r in checks)
sheet=Image.new('RGB',(1400,3*600),'white');d=ImageDraw.Draw(sheet)
for i,(fig,c) in enumerate(cfg.items()):
 im=Image.open('out/'+fig+'/overlay-p1.png').crop(c['area']);im.thumbnail((450,550));u=i%3*466;v=i//3*600;sheet.paste(im,(u,v+30));d.text((u,v+5),fig,fill='black')
sheet.save('out/final-overlay-check.png')
