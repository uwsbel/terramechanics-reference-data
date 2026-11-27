from pathlib import Path
import sys,subprocess,json,csv
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import calibrate_axes as ca
CONFIG={
 'FA-2':('p0007',(685,1125,2190,3740)),
 'FA-6':('p0014',(780,1160,2280,3770)),
 'FA-18':('p0039',(575,1130,2120,3770)),
 'FA-22':('p0047',(745,1170,2250,3780)),
 'FA-26':('p0054',(565,1210,2055,3820)),
 'FA-38':('p0077',(685,1160,2190,3770)),
 'FA-46':('p0095',(715,1150,2225,3770)),
}
def run(*args):
 subprocess.run([sys.executable,*map(str,args)],check=True,cwd=ROOT)
if __name__=='__main__':
 for fid,(page,box) in CONFIG.items():
  dest=ROOT/'out'/fid; dest.mkdir(exist_ok=True)
  if sys.argv[1]=='cal':
   run(ROOT/'tools/calibrate_axes.py','detect',ROOT/'packet'/f'{page}.png','--box',*box,'--x-values','0.02,0.05,0.1,0.2,0.5,1,1.5,2,3,4,5,9','--y-values','0,10,20,30,40,50,60,70,80,90,100','--x-direction','up','--y-direction','left','--x-transform','log10','--bands',15,'--min-frac',.6,'--snap',8,'--out',dest/'cal-p1')
  if sys.argv[1]=='crops':
   im=Image.open(ROOT/'packet'/f'{page}.png')
   u0,v0,u1,v1=box
   im.crop((u0-110,v0-120,u1+150,v0+700)).save(dest/'labels-top.png')
   im.crop((u1-50,v0-80,u1+180,v1+80)).save(dest/'labels-grain.png')
   for i,(a,b) in enumerate([(v0-100,v0+650),(v0+600,v0+1250),(v0+1200,v0+1950),(v0+1900,v1+30)]):
    run(ROOT/'tools/plot_grid.py','crop',ROOT/'packet'/f'{page}.png','--box',u0-20,a,u1+20,b,'--out',dest/f'crop-{i}.png','--zoom',1,'--step',25)
