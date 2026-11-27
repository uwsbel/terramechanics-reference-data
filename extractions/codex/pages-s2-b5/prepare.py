from PIL import Image
from pathlib import Path
rotated={117,118,120,121,122,125,127,133,136,137}
for p in Path('packet').glob('p*.png'):
 im=Image.open(p)
 if int(p.stem[1:]) in rotated: im=im.rotate(-90,expand=True)
 im.save(Path('out')/(p.stem+'-upright.png'))
