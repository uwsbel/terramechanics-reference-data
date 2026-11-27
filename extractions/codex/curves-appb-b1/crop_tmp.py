from PIL import Image,ImageDraw
im=Image.open('packet/p0112.png').convert('RGB'); cr=im.crop((620,1050,735,1400)).resize((460,1400)); cr.save('out/ticks6.png')
