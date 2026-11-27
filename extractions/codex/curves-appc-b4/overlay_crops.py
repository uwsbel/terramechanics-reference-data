from PIL import Image
for fig,box in [('FC-7B',(570,1310,2330,3300)),('FC-7C',(590,1330,2370,3340))]:
 im=Image.open(f'out/{fig}/overlay-p1.png');im.crop(box).save(f'out/{fig}/overlay-frame.png');im.crop((1280,3010,2370,3340)).resize((2180,660)).save(f'out/{fig}/overlay-origin.png')
