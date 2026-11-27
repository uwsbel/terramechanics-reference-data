from PIL import Image,ImageDraw
boxes=[(4,(910,2715,990,2825)),(4,(1930,1290,2008,1380)),(3,(1205,1950,1270,2030)),(7,(450,2970,550,3125)),(7,(460,3420,545,3530))]
can=Image.new('RGB',(2100,700),'white');d=ImageDraw.Draw(can)
for i,(j,b) in enumerate(boxes):
 cr=Image.open(f'packet/p{j+106:04}.png').convert('RGB').crop(b);cr=cr.resize((cr.width*4,cr.height*4));can.paste(cr,(i*420,40));d.text((i*420,0),f'FB-{j} {b}',fill='blue')
can.save('out/overlaps.png')
