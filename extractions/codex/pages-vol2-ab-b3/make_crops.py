from PIL import Image
from pathlib import Path
out=Path(__file__).parent
def crop(n,name,box,rot=0,scale=1):
    im=Image.open(f'packet/p{n:04d}.png')
    if rot: im=im.rotate(-rot,expand=True)
    w,h=im.size
    im=im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(box)))
    if scale!=1: im=im.resize((round(im.width*scale),round(im.height*scale)))
    im.save(out/f'p{n:04d}-{name}.png')
for n,box in [(54,(.17,.215,.444,.38)),(61,(.195,.252,.49,.414)),(68,(.505,.524,.811,.692))]:
    crop(n,'table',box,90,1.2)
crop(60,'marks',(.145,.178,.715,.233),scale=1.3)
crop(65,'chemical',(.16,.566,.715,.737),scale=1.25)
crop(67,'marks',(.12,.446,.85,.713),scale=1)
crop(69,'axis',(.709,.452,.74,.63),scale=2)
crop(72,'text',(.125,.394,.86,.88),scale=1)
crop(55,'axis',(.144,.405,.18,.6),scale=1.5)
crop(50,'text',(.135,.24,.86,.405),scale=1)
crop(53,'numbers',(.13,.65,.87,.846),scale=1)
