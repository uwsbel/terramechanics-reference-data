import sys,subprocess,json
from pathlib import Path
sys.path.insert(0,'tools')
from PIL import Image
P=sys.executable
cfg={
 'FA-4':dict(page='p0009',box=[820,1370,2400,2940],ys='30,35,40,45,50',plot=[810,1360,2410,3350]),
 'FA-8':dict(page='p0016',box=[850,1510,2420,3075],ys='30,35,40,45,50',plot=[840,1510,2430,3470]),
 'FA-20':dict(page='p0041',box=[800,1480,2370,3050],ys='30,35,40,45,50',plot=[795,1470,2380,3440]),
 'FA-24':dict(page='p0049',box=[775,1590,2345,3165],ys='30,35,40,45,50',plot=[770,1210,2350,3550]),
 'FA-28':dict(page='p0056',box=[750,1590,2325,3540],ys='25,30,35,40,45,50',plot=[740,1200,2335,3540]),
 'FA-40':dict(page='p0079',box=[765,1620,2370,3205],ys='30,35,40,45,50',plot=[760,1250,2360,3600]),
 'FA-48':dict(page='p0097',box=[770,1605,2360,3170],ys='30,35,40,45,50',plot=[765,1230,2370,3560]),
}
Path('out/config.json').write_text(json.dumps(cfg,indent=2))
for fid,c in cfg.items():
 out=Path('out')/fid;out.mkdir(exist_ok=True)
 args=[P,'tools/calibrate_axes.py','detect','packet/'+c['page']+'.png','--box',*map(str,c['box']),'--x-values','0,0.2,0.4,0.6,0.8,1.0','--y-values',c['ys'],'--out',str(out/'cal-p1'),'--bands','12','--min-frac','0.55','--frame-frac','0.66']
 r=subprocess.run(args,capture_output=True,text=True);(out/'cal-p1-detect.log').write_text(r.stdout+r.stderr); print(fid,r.stdout,r.stderr)
 im=Image.open('packet/'+c['page']+'.png');b=c['plot'];im.crop((b[0]-180,b[1]-30,b[2]+20,b[3]+130)).save(out/'plot-labels.png')
