import json
from pathlib import Path
p=Path('out/FC-6C/readings.json');c=json.loads(p.read_text(encoding='utf-8-sig'));fix={'n4695':([710,1805],[2063,1223],[2030,1223]),'n3815':([711,1995],[2077,1519],[2077,1519]),'n2934':([718,2070],[2078,1558],[1850,1537]),'n1961':([718,2145],[2090,2019],[1680,2001]),'n714':([725,2227],[2089,2194],[850,2194])}
for sid,(a,b,peak) in fix.items():
 d=c['series'][sid];d['first']=a;d['last']=b;d['peak']=peak;d['t1'][0]=a;d['t1'][-1]=b
p.write_text(json.dumps(c,indent=1))
p=Path('out/read_curves.py');s=p.read_text();s=s.replace("u,v=hole_refine(im,u,v,sym)\n    if sym=='plus'", "orig=(u,v);u,v=hole_refine(im,u,v,sym)\n     if (u,v)==orig and bound==2: bound=6;note='Outline interrupted by trace/grid; manual center with wider bound.'\n    if sym=='plus'")
p.write_text(s)
