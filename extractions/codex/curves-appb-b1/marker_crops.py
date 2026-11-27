import json
from PIL import Image,ImageDraw
from pathlib import Path
clusters={3:[(865,3050),(1238,1990),(1940,912),(1100,3790),(1385,3240),(2445,2240)],4:[(775,3215),(950,2770),(950,2545),(1285,1860),(1295,2310),(1975,1340),(1950,1950)],5:[(1030,2915),(1390,2200),(2380,1115),(1130,3480),(1580,3050),(2350,2535)],6:[(1030,3345),(1325,2420),(1965,1160),(1000,3975),(1340,3425),(1960,2665)],7:[(502,3850),(500,3485),(502,3370),(500,3070),(775,2655),(795,2335),(820,2125),(1445,1840),(1435,2145),(1415,2305),(1310,1990),(1800,1300),(1815,1510),(1810,1835),(1930,1810),(1940,1675),(1770,1690),(2090,1640)]}
for j,cs in clusters.items():
 im=Image.open(f'packet/p{j+106:04}.png').convert('RGB');w=480;h=620;canvas=Image.new('RGB',(w*3,h*((len(cs)+2)//3)),'white');d=ImageDraw.Draw(canvas)
 for i,(u,v) in enumerate(cs):
  box=(u-65,v-85,u+65,v+95);cr=im.crop(box).resize((390,540));dd=ImageDraw.Draw(cr)
  for x in range((box[0]//25+1)*25,box[2],25):
   xx=(x-box[0])*3;dd.line((xx,0,xx,540),fill=(190,210,240));dd.text((xx,0),str(x),fill='red')
  for y in range((box[1]//25+1)*25,box[3],25):
   yy=(y-box[1])*3;dd.line((0,yy,390,yy),fill=(190,210,240));dd.text((0,yy),str(y),fill='red')
  x0=i%3*w;y0=i//3*h;canvas.paste(cr,(x0,y0+30));d.text((x0,y0),f'{j} cluster {i+1} {box}',fill='blue')
 canvas.save(f'out/FB-{j}-markers.png')
Path('out/clusters.json').write_text(json.dumps(clusters))
