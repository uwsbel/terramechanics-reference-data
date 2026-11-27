from pathlib import Path
import sys,json
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'tools')
import calibrate_axes as ca
# Candidate centroid positions selected from the page crops, before the traces.
spec={
'FC-12':('p0148.png',[(630,3668),(808,3505),(1100,3164),(1265,3039),(1435,2919),(1694,2650),(1865,2515),(1950,2410)]),
'FC-13':('p0147.png',[(755,3681),(1215,3415),(1396,3318),(1561,3239),(1821,3077),(1992,2949),(2077,2936)]),
'FC-14':('p0150.png',[(670,3683),(845,3624),(1148,3269),(1318,3193),(1487,2908),(1751,2655),(1933,2587),(2012,2516)]),
'FC-15':('p0151.png',[(740,3598),(908,3484),(1205,3307),(1373,2936),(1539,2821),(1800,2804),(1967,2416),(2055,2521)])}
for f,(pg,pts) in spec.items():
 g=np.array(Image.open('packet/'+pg).convert('L'));im=Image.open('packet/'+pg).convert('RGB')
 fitted=[];sheet=Image.new('RGB',(4*300,2*300),'white');dr=ImageDraw.Draw(sheet)
 for i,(u,v) in enumerate(pts):
  # Fit a triangle outline template. Score the three drawn sides independently;
  # this avoids weighting an intersecting fitted line as part of the symbol.
  best=None
  for ax in np.arange(u-3,u+3.1,1):
   for ay in np.arange(v-22,v-11,1):
    for h in np.arange(21,31,1):
     w=1.17*h
     scores=[]
     for side in (-1,1):
      t=np.linspace(.12,.9,20);xx=ax+side*w/2*t;yy=ay+h*t
      vv=[]
      for off in (-1,0,1):vv.append((255-g[np.round(yy).astype(int),np.round(xx+off).astype(int)])/255)
      scores.append(np.mean(vv))
     xx=np.linspace(ax-w*.35,ax+w*.35,20);yy=np.full(20,ay+h)
     scores.append(np.mean([(255-g[np.round(yy+off).astype(int),np.round(xx).astype(int)])/255 for off in (-1,0,1)]))
     # Also require a hollow interior, except where another drawn line crosses it.
     xx=np.linspace(ax-w*.15,ax+w*.15,8);yy=np.full(8,ay+h*.67)
     white=np.mean(g[np.round(yy).astype(int),np.round(xx).astype(int)]/255)
     score=sum(scores)+.2*white
     if best is None or score>best[0]:best=(score,ax,ay,h,w)
  _,ax,ay,h,w=best;cx=ax;cy=ay+2*h/3
  fitted.append({'sequence':i+1,'centroid':[round(cx,2),round(cy,2)],'vertices':[[ax,ay],[ax-w/2,ay+h],[ax+w/2,ay+h]],'height':h})
  box=(u-50,v-40,u+50,v+40);cr=im.crop(box).resize((300,240),Image.Resampling.NEAREST);dd=ImageDraw.Draw(cr)
  vv=[((xx-box[0])*3,(yy-box[1])*3) for xx,yy in fitted[-1]['vertices']]
  dd.line(vv+[vv[0]],fill=(0,150,0),width=1);cc=((cx-box[0])*3,(cy-box[1])*3);dd.ellipse((cc[0]-3,cc[1]-3,cc[0]+3,cc[1]+3),outline='red')
  sheet.paste(cr,(i%4*300,i//4*300+40));dr.text((i%4*300,i//4*300),f'{f} #{i+1} {cx:.1f},{cy:.1f}\nheight {h}',fill='black')
 (Path('out')/f/'marker-vertices.json').write_text(json.dumps(fitted,indent=1,default=lambda o:float(o)),encoding='utf-8')
 sheet.save(Path('out')/f/'marker-centroids-inspection.png')
 print(f,[(p['centroid'],p['height']) for p in fitted])
