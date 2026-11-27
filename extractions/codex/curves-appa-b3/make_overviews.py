from PIL import Image
from pathlib import Path
for p in Path('packet').glob('*.png'):
 im=Image.open(p); im.crop((600,1400,2800,3650)).resize((1100,1125)).save(Path('out')/(p.stem+'-overview.png'))
