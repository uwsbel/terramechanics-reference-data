from PIL import Image,ImageDraw,ImageFont
import csv,math
im=Image.open('packet/p0117.png').convert('RGB')
font=ImageFont.truetype('arial.ttf',18)
for p in (1,2):
    rows=list(csv.DictReader(open(f'out/points-p{p}.csv')))
    for sid in dict.fromkeys(r['series_id'] for r in rows):
        pts=[r for r in rows if r['series_id']==sid and r['point_kind']=='marker']
        sheet=Image.new('RGB',(1000,math.ceil(len(pts)/4)*230),'white');d=ImageDraw.Draw(sheet)
        for i,r in enumerate(pts):
            u,v=round(float(r['pixel_u'])),round(float(r['pixel_v']))
            crop=im.crop((u-30,v-25,u+30,v+25)).resize((240,200),Image.Resampling.NEAREST)
            cd=ImageDraw.Draw(crop)
            cd.line((120,0,120,199),fill=(255,140,140));cd.line((0,100,239,100),fill=(150,150,255))
            for k in range(0,241,20):cd.line((k,95,k,105),fill=(0,170,0))
            for k in range(0,201,20):cd.line((115,k,125,k),fill=(0,170,0))
            x,y=(i%4)*250,(i//4)*230
            d.text((x,y),f'{i+1}: ({u}, {v})',font=font,fill='black');sheet.paste(crop,(x,y+25))
        sheet.save(f'out/markers-p{p}-{sid}.png')
