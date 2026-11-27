from read_batch import *
for fid,(page,box) in CONFIG.items():
 d=ROOT/'out'/fid;g=np.array(Image.open(ROOT/'packet'/f'{page}.png').convert('L'));cal=json.loads((d/'cal-p1/calibration.json').read_text());
 sx=np.median([l['slope_dv_du'] for l in cal['horizontal_lines']]);sy=np.median([l['slope_du_dv'] for l in cal['vertical_lines']]);u0,v0,u1,v1=box
 U,V=np.meshgrid(np.arange(u0-20,u1+20),np.arange(v0-100,v1));UC=(u0+u1)/2;VC=(v0+v1)/2
 UU=np.rint(U+sy*(V-VC)).astype(int);VV=np.rint(V+sx*(U-UC)).astype(int)
 b=g[VV,UU]<150
 # Repeated long grid lines are found by coverage; this image is only a locator aid.
 cc=np.mean(b,axis=0)>.42
 for i in [-1,0,1]:b[:,np.roll(cc,i)]=False
 rr=np.mean(b,axis=1)>.27
 for i in [-1,0,1]:b[np.roll(rr,i),:]=False
 TABLE={'FA-2':(860,2270,1485,3670),'FA-6':(1050,2260,1685,3650),'FA-18':(880,2100,1520,3610),'FA-22':(770,2220,1370,3760),'FA-26':(690,2540,1210,3780),'FA-38':(1340,1250,1940,2740),'FA-46':(915,2370,1520,3710)}
 tab=TABLE[fid];b[(UU>tab[0]-8)&(UU<tab[2]+8)&(VV>tab[1]-8)&(VV<tab[3]+8)]=False
 out=np.full(g.shape,255,dtype=np.uint8);out[VV,UU]=np.where(b,0,255)
 Image.fromarray(out).save(d/'grid-suppressed.png')
 Image.fromarray(out).crop((u0-20,v0-100,u1+20,v1)).save(d/'curve-locator.png')
