import json
from pathlib import Path
p=Path('out/FC-6D/readings.json');c=json.loads(p.read_text(encoding='utf-8-sig'));d=c['series']['n2934'];d['t1']=[[833,1980.5],[930,1892],[1040,1810],[1140,1730],[1200,1695],[1250,1665],[1300,1635],[1380,1598],[1530,1536],[1690,1477],[1880,1441],[2080,1428],[2212,1423.5]]
fix={'n4695':([826,1733],[2201,862]),'n3814':([826,1828],[2203,1103.5]),'n2934':([833,1980.5],[2212,1423.5]),'n1761':([833,2070],[2206,1731]),'n147':([838,2208],[2205,2165])}
for sid,(a,b) in fix.items():
 d=c['series'][sid];d['first']=a;d['last']=b;d['t1'][0]=a;d['t1'][-1]=b
 if sid in ['n3814','n2934','n1761']:d['peak']=b
c['series']['n147']['feature_width']=13;c['series']['n147']['peak_u_bound']=150
p.write_text(json.dumps(c,indent=1))
