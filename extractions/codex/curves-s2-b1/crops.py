from PIL import Image,ImageDraw,ImageFont
regions={
 '29a':(80,(1750,3150,2380,3820)), '29b':(80,(1080,2450,1820,3190)), '29c':(80,(550,1310,1150,2490)),
 '32a':(88,(1500,3130,2010,3710)), '32b':(88,(1030,2550,1670,3210)), '32c':(88,(740,2140,1270,2710)),
 '33a':(89,(1400,2900,2330,3640)), '33b':(89,(800,2200,1600,2940)),
 '34a':(90,(1700,2870,2260,3680)), '34b':(90,(1450,2250,1870,2930)), '34c':(90,(1250,1500,1690,2300))}
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
for name,(n,b) in regions.items():
 im=Image.open(f'packet/p{n:04}.png').crop(b); d=ImageDraw.Draw(im)
 for u in range((b[0]//50+1)*50,b[2],50):
  d.line((u-b[0],0,u-b[0],im.height),fill='#aaddff');d.text((u-b[0]+1,3),str(u),font=font,fill='red')
 for v in range((b[1]//50+1)*50,b[3],50):
  d.line((0,v-b[1],im.width,v-b[1]),fill='#aaddff');d.text((1,v-b[1]+1),str(v),font=font,fill='red')
 im.save(f'out/crop-{name}.png')
