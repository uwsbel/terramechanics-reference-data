import json
from pathlib import Path
p=Path('out/FC-6B/readings.json');c=json.loads(p.read_text());d=c['series']['n4695'];d['t1']=[[712,1761],[790,1580],[900,1440],[1050,1296],[1200,1181],[1360,1090],[1520,1005],[1620,963],[1680,943],[1740,924],[1770,914],[1900,880],[2020,858],[2065,862]]
for d in c['series'].values():d['grid_overlap']=True
p.write_text(json.dumps(c,indent=1))
