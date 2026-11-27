import json
from pathlib import Path
p=Path('out/read_curves.py');s=p.read_text(encoding='utf-8-sig').replace("w<3 or w>28","w<5 or w>40").replace("abs(du)+abs(vv-y)*.1","abs(du)+abs(vv-y)*.6")
# Explicit feature coordinates were read from ink by eye, so retain them without the automatic marker exclusion.
s=s.replace("u,v=dat[key];r=locate(u,4)\n    if r:samples.append(r)","u,v=dat[key];samples.append((u,v,dat.get('feature_width',10)))")
s=s.replace("u,v=dat[key];r=locate(u,4)\n    if r:\n     uu,vv,w=r;", "u,v=dat[key];r=(u,v,dat.get('feature_width',10))\n    if r:\n     uu,vv,w=r;")
p.write_text(s,encoding='utf-8')
p=Path('out/FC-5B/readings.json');c=json.loads(p.read_text(encoding='utf-8-sig'))
fix={'n4695':([724,1888],[2118,1688]),'n3815':([725,2101],[2119,1835]),'n2934':([723,2193],[2134,1984]),'n1761':([727,2266],[2137,2177]),'n734':([727,2259],[2132,2224])}
for sid,(a,b) in fix.items():
 d=c['series'][sid];d['first']=a;d['last']=b;d['t1'][0]=a;d['t1'][-1]=b
p.write_text(json.dumps(c,indent=1),encoding='utf-8')
