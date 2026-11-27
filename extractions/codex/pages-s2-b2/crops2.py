from PIL import Image
specs=[
(48,'sievefirst',(194,748,325,860),(1344,1846)),
(51,'symbols',(130,462,355,520),(1344,1886)),
(51,'footnote',(142,1390,1120,1460),(1344,1886)),
(53,'gradation',(510,1065,1020,1110),(1344,1886)),
(55,'equation',(495,470,885,555),(1344,1846)),
(59,'when',(160,300,670,350),(1400,1792)),
(63,'adapted',(630,1150,1130,1200),(1387,1792)),
]
for n,name,box,display in specs:
    im=Image.open(f'packet/p{n:04d}.png')
    box=tuple(int(v*im.size[i%2]/display[i%2]) for i,v in enumerate(box))
    im.crop(box).save(f'out/p{n:04d}-{name}.png')
