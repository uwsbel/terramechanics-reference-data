from pathlib import Path
import json
p=Path('out/read_curves.py');s=p.read_text().replace('w<5 or w>40','w<7 or w>40').replace('abs(du)+abs(vv-y)*.6','abs(du)+abs(vv-y)*.4-w*.5')
s=s.replace("samples=[]\n   for u in np.arange(us[0],us[-1]+1,20):\n    r=locate(u)\n    if r and (not samples or r[0]>samples[-1][0]):samples.append(r)","""samples=[]; intervals=[]; current=[]
   for u in range(int(us[0]),int(us[-1])+1):
    r=locate(u,0)
    if r:
     if current and (r[0]-current[-1][0]>1 or abs(r[1]-current[-1][1])>15):intervals.append(current);current=[]
     current.append(r)
    elif current:intervals.append(current);current=[]
   if current:intervals.append(current)
   for cc in intervals:
    if len(cc)<3:continue
    samples.extend(cc[1:-1:20]);samples.append(cc[-2])""")
p.write_text(s)
p=Path('out/FC-6B/readings.json');c=json.loads(p.read_text(encoding='utf-8-sig'));fix={'n4695':([712,1761],[2065,862]),'n3815':([719,1714],[2068,1000]),'n2934':([732,1826],[2067,1242]),'n1761':([726,1920],[2069,1625]),'n734':([728,1981],[2078,2001])}
for sid,(a,b) in fix.items():
 d=c['series'][sid];d['first']=a;d['last']=b;d['t1'][0]=a;d['t1'][-1]=b
c['series']['n1761']['peak']=[2069,1625];c['series']['n2934']['peak']=[2067,1242]
p.write_text(json.dumps(c,indent=1))
