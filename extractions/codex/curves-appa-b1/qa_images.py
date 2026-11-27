import csv,json
from pathlib import Path
from PIL import Image,ImageDraw
cfg=json.loads(Path('out/config.json').read_text())
for f,c in cfg.items():
 root=Path('out')/f;im=Image.open('packet/'+c['page']+'.png').convert('RGB');rows=list(csv.DictReader((root/'points-p1.csv').open()))
 for sid in sorted({r['series_id'] for r in rows}):
  rs=[r for r in rows if r['series_id']==sid and r['point_kind']=='trace'];sheet=Image.new('RGB',(1080,1230),'white');d=ImageDraw.Draw(sheet)
  for j,r in enumerate(rs):
   u,v=float(r['pixel_u']),float(r['pixel_v']);b=(round(u)-40,round(v)-26,round(u)+40,round(v)+26);tile=im.crop(b).resize((240,156),Image.Resampling.NEAREST);td=ImageDraw.Draw(tile);x=(u-b[0])*3;y=(v-b[1])*3
   for p,q in [((x-21,y),(x-7,y)),((x+7,y),(x+21,y)),((x,y-21),(x,y-7)),((x,y+7),(x,y+21))]:td.line([p,q],fill='red',width=1)
   xx=(j%4)*270;yy=(j//4)*205;sheet.paste(tile,(xx+5,yy+30));d.text((xx+5,yy+3),f"{j+1}: ({u:.1f},{v:.1f}) b={r['v_bound_px']}",fill='black')
  sheet.save(root/('samples-check.png' if sid=='curve' else f'samples-check-{sid}.png'))
 ov=Image.open(root/'overlay-p1.png');b=c['plot'];ov=ov.crop((b[0]-170,b[1]-20,b[2]+25,b[3]+120));ov.thumbnail((1000,1400));ov.save(root/'overlay-detail.png')
