import subprocess,sys,json
from pathlib import Path
from PIL import Image
configs=[('FC-8','p0138.png',[730,1050,2800,3445]),('FC-9A','p0139.png',[630,1390,2710,3775]),('FC-9B','p0140.png',[625,1455,2720,3840]),('FC-9C','p0141.png',[530,1405,2615,3780]),('FC-10A','p0142.png',[580,1370,2695,3770])]
Path('out/config.json').write_text(json.dumps(configs))
for fig,page,box in configs:
 d=Path('out')/fig; d.mkdir(exist_ok=True)
 subprocess.run([sys.executable,'tools/calibrate_axes.py','detect','packet/'+page,'--box',*map(str,box),'--x-values',','.join(map(str,range(0,7001,1000))),'--y-values',','.join(map(str,range(0,8001,1000))),'--out',str(d/'cal-p1'),'--bands','15','--min-frac','0.45','--frame-frac','0.6'],check=True)
 im=Image.open('packet/'+page)
 # top box and axis-label strips preserved large enough to read
 for name,b in [('box',[box[0]-10,box[1]-520,box[2]+10,box[1]+25]),('x-labels',[box[0]-50,box[3]-40,box[2]+130,box[3]+115]),('y-labels',[box[0]-240,box[1]-30,box[0]+35,box[3]+30])]:
  im.crop(b).save(d/(name+'.png'))
