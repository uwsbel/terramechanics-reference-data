import json
from pathlib import Path
p=json.loads(Path('out/final-pixels.json').read_text())
a=p['FA-7']['lower']['points'][3];a.update(u=1105,v=2083,bound=3.5)
a=p['FA-27']['upper']['points'][6];a.update(u=1625,v=3413,bound=3.5)
Path('out/final-pixels.json').write_text(json.dumps(p,indent=2))
