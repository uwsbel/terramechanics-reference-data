from PIL import Image
im=Image.open('out/p0119-upright.png')
for j,b in enumerate([(290,2630,2710,2895),(290,3160,2710,3460)]):
 im.crop(b).resize(((b[2]-b[0]),(b[3]-b[1]))).save(f'out/p0119-marks{j}.png')
