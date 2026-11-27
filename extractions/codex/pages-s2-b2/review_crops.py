from PIL import Image
for n in [49,51,53,54,55,58,59,60,62,63,70]:
    im=Image.open(f'packet/p{n:04d}.png')
    w,h=im.size
    top=.22 if n in [49,51,53,54,55,58,70] else .15
    im=im.crop((int(w*.075),int(h*top),int(w*.90),int(h*.89)))
    im.thumbnail((1800,2200))
    im.save(f'out/p{n:04d}-review.png')
