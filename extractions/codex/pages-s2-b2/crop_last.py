from PIL import Image
im=Image.open('packet/p0051.png'); w,h=im.size
im.crop((int(w*.10),int(h*.49),int(w*.78),int(h*.52))).save('out/p0051-the-values.png')
