from PIL import Image
from pathlib import Path

regions = {
    '116axes': (116, (.19,.475,.25,.555)),
    '116x': (116, (.40,.735,.51,.765)),
    '117dash': (117, (.49,.843,.55,.865)),
    '121legend': (121, (.67,.39,.80,.42)),
    '122legend': (122, (.665,.245,.815,.375)),
    '127cols': (127, (.68,.27,.82,.30)),
    '129angle': (129, (.54,.505,.60,.547)),
    '129report': (129, (.49,.22,.745,.28)),
    '130dash': (130, (.405,.845,.49,.869)),
    '131heading': (131, (.30,.305,.675,.39)),
    '134heading': (134, (.25,.155,.64,.199)),
}
for name, (n, box) in regions.items():
    im = Image.open(f'packet/p{n:04}.png')
    w,h = im.size
    im = im.crop(tuple(int(a*b) for a,b in zip(box,(w,h,w,h))))
    im.resize((im.width*2,im.height*2)).save(f'out/crop-{name}.png')
im = Image.open('packet/p0136.png').rotate(-90, expand=True)
w,h = im.size
im = im.crop((int(w*.684),int(h*.61),int(w*.762),int(h*.683)))
im.resize((im.width*3,im.height*3)).save('out/crop-136legend.png')
