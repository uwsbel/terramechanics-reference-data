from PIL import Image
for n in [119,123,124,126,129,132,134,135,138]:
 im=Image.open(f'out/p{n:04}-upright.png')
 w,h=im.size
 top=950 if h>4400 else 660
 bot=h-380
 mid=(top+bot)//2
 im.crop((280,top,w-450,mid+60)).save(f'out/p{n:04}-review-a.png')
 im.crop((280,mid-60,w-450,bot)).save(f'out/p{n:04}-review-b.png')
im=Image.open('out/p0120-upright.png'); im.crop((780,810,2310,1730)).save('out/p0120-table.png')
