from PIL import Image
for j in range(3,8):
 im=Image.open(f'out/FB-{j}/overlay-p1.png');im.thumbnail((1300,1850));im.save(f'out/FB-{j}-overlay-preview.png')
