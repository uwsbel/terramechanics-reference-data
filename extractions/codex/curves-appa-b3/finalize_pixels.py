import json,numpy as np
from pathlib import Path
from PIL import Image,ImageDraw
p=json.loads(Path('out/proposed-pixels.json').read_text());cfg=json.loads(Path('out/config.json').read_text())
# Explicit decisions from the magnified page crops. Pixel coordinates only.
changes={
'FA-3':{'upper':{6:(1652,2950,4.5)},'lower':{7:(1806,3053.5,4),11:(2435,3169,4)}},
'FA-7':{'upper':{8:(1703,2178,4)},'lower':{8:(1700,2300,3.5)}},
'FA-19':{},
'FA-23':{'upper':{1:(836,1377,4),3:(1100,1623,3),7:(1660,2115,3.5)},'lower':{3:(1133,2730,3),4:(1259,2816,4),10:(2097,3438,4)}},
'FA-27':{'mean':{1:(685,3159,4.5),11:(2224,3627,4.5)},'upper':{5:(1315,3320,3.5),6:(1444,3358,3.5),7:(1608,3415,3.5),11:(2224,3577,4)},'lower':{1:(685,3171,4.5),5:(1289,3365,3),11:(2224,3686,5)}},
'FA-39':{'upper':{8:(1855,2652,3.5)}},
'FA-47':{'upper':{3:(1178,2466,3.5),11:(2277,2963,3.5)},'mean':{11:(2284,2975,5)},'lower':{11:(2284,2975,5)}}}
for fig,c in cfg.items():
 g=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'))
 for sid in ['mean','upper','lower']:
  for i,a in enumerate(p[fig][sid]['points']):
   if 'gap:' in a['note']:
    u,v=round(a['u']),round(a['v']);lo=hi=v
    while g[lo-1,u]<160:lo-=1
    while g[hi+1,u]<160:hi+=1
    if hi-lo<14:a['v']=(lo+hi)/2;a['bound']=(hi-lo+1)/2
   if i+1 in changes.get(fig,{}).get(sid,{}):
    u,v,b=changes[fig][sid][i+1];a.update(u=u,v=v,bound=b)
    if i not in [0,10]:a['note']=f'target Dr={i/10:.1f}; gap: nearest dash end checked by eye'
    else:a['note']+='; endpoint checked by eye'
   if fig=='FA-47' and i==10:a['note']+='; right end approaches common ink cluster; shared printed label 89.4'
Path('out/final-pixels.json').write_text(json.dumps(p,indent=2))
# Rebuild sample crops after all decisions.
for fig,c in cfg.items():
 im=Image.open('packet/'+c['page']+'.png').convert('RGB');sheet=Image.new('RGB',(11*240,3*230),'white');draw=ImageDraw.Draw(sheet)
 for j,sid in enumerate(['mean','upper','lower']):
  for i,a in enumerate(p[fig][sid]['points']):
   u,v=round(a['u']),round(a['v']);box=(u-39,v-31,u+39,v+31);tile=im.crop(box).resize((234,186),Image.Resampling.NEAREST);td=ImageDraw.Draw(tile)
   for ku in range((box[0]//25+1)*25,box[2],25):td.line(((ku-box[0])*3,0,(ku-box[0])*3,186),fill=(245,160,160))
   for kv in range((box[1]//25+1)*25,box[3],25):td.line((0,(kv-box[1])*3,234,(kv-box[1])*3),fill=(170,170,245))
   px=(a['u']-box[0])*3;py=(a['v']-box[1])*3;td.ellipse((px-4,py-4,px+4,py+4),outline='red',width=1)
   sheet.paste(tile,(i*240,j*230+40));draw.text((i*240+3,j*230+2),f'{fig} {sid} {i+1} Dr {i/10:.1f}',fill='black');draw.text((i*240+3,j*230+16),f"{a['u']:.1f}, {a['v']:.1f} b={a['bound']:.1f}"+(' shifted' if 'gap:' in a['note'] else ''),fill='black')
 sheet.save('out/'+fig+'/sample-checks-final.png')
