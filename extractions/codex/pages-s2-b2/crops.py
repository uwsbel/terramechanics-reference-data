from PIL import Image
from pathlib import Path
specs = [
(48,'numbers',(440,870,790,970),(1344,1846)),
(48,'total',(190,1320,585,1505),(1344,1846)),
(48,'test',(260,500,475,545),(1344,1846)),
(54,'gamma',(220,1410,800,1500),(1344,1846)),
(58,'sensitivity',(835,425,1110,475),(1344,1886)),
(59,'make',(165,1110,640,1150),(1400,1792)),
(68,'legend',(985,565,1150,1020),(1387,1792)),
(68,'axis',(605,1430,830,1475),(1387,1792)),
(66,'sign',(790,730,866,783),(1792,1376)),
]
for n,name,box,display in specs:
    im=Image.open(f'packet/p{n:04d}.png')
    if n == 66: im=im.rotate(-90,expand=True)
    box=tuple(int(v*im.size[i%2]/display[i%2]) for i,v in enumerate(box))
    crop=im.crop(box)
    crop.resize((crop.width*2,crop.height*2)).save(f'out/p{n:04d}-{name}.png')
