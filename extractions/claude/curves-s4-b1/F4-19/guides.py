"""Run the ink follower on segments of each trace and draw the result for checking by eye."""
import sys, json
sys.path.insert(0, 'out/F4-19')
import numpy as np
from PIL import Image, ImageDraw
import trace_tools as T

SEG = json.load(open('out/F4-19/segments.json'))

def run(keys=None):
    ink, bm = T.load_clean()
    out = {}
    for k, a in SEG.items():
        if keys and k not in keys:
            continue
        umin, umax = a.get('umin', -1e9), a.get('umax', 1e9)
        vmin, vmax = a.get('vmin', -1e9), a.get('vmax', 1e9)
        stop = lambda p: not (umin <= p[0] <= umax and vmin <= p[1] <= vmax)
        pts = T.track(ink, a['start'], a['direction'], step=a.get('step', 2.0), half=a.get('half', 9.0),
                      maxgap=a.get('maxgap', 20), stop=stop, width_max=a.get('width_max', 30), maxdist=a.get('maxdist', 4.0))
        out[k] = pts
        print(k, len(pts), 'found', sum(1 for p in pts if p[2]), 'end', tuple(round(x, 1) for x in pts[-1][:2]))
    return out

def draw(out, box, zoom, path):
    im = Image.open('packet/p0208.png').convert('RGB').crop(box)
    im = im.resize(((box[2]-box[0])*zoom, (box[3]-box[1])*zoom), Image.NEAREST)
    d = ImageDraw.Draw(im)
    cols = [(255,0,0),(0,170,0),(0,0,255),(200,0,200),(0,170,170),(230,120,0)]
    for i,(k,pts) in enumerate(out.items()):
        c = cols[i % len(cols)]
        for p in pts:
            x, y = (p[0]-box[0])*zoom, (p[1]-box[1])*zoom
            if p[2]:
                d.ellipse([x-1.5,y-1.5,x+1.5,y+1.5], fill=c)
            else:
                d.ellipse([x-1,y-1,x+1,y+1], outline=(255,150,0))
    im.save(path)

if __name__ == '__main__':
    keys = sys.argv[1].split(',') if len(sys.argv) > 1 and sys.argv[1] != 'all' else None
    out = run(keys)
    old = {}
    try:
        old = json.load(open('out/F4-19/guides.json'))
    except FileNotFoundError:
        pass
    old.update(out)
    json.dump(old, open('out/F4-19/guides.json','w'))
    if len(sys.argv) > 2:
        box = [int(x) for x in sys.argv[2].split(',')]
        zoom = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        draw(out, box, zoom, sys.argv[4] if len(sys.argv) > 4 else 'out/F4-19/crops/guides.png')
