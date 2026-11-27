from PIL import Image
import csv
from pathlib import Path
for f in ['p0130','p0132','p0133','p0134']:
 im=Image.open('packet/'+f+'.png').convert('L');print(f,im.size)
 fig={'p0130':'FC-5B','p0132':'FC-6B','p0133':'FC-6C','p0134':'FC-6D'}[f]
 for r in csv.DictReader(open('out/'+fig+'/points-p1.csv')):
  if r['point_kind']=='feature':
   u,v=float(r['pixel_u']),float(r['pixel_v']);gray=im.getpixel((round(u),round(v)))
   if gray>200:print('WHITE feature',fig,r['series_id'],r['note'],u,v,gray)
