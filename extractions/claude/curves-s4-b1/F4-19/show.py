import sys, json
sys.path.insert(0,'tools'); sys.path.insert(0,'out/F4-19')
import calibrate_axes as C
from PIL import Image, ImageDraw
S = json.load(open('out/F4-19/samples.json'))
maps = {1: C.piecewise_maps('out/F4-19/cal-p1','packet/p0208.png'), 2: C.piecewise_maps('out/F4-19/cal-p2','packet/p0208.png')}
def table(key):
    p = int(key[0]); _, X, Y = maps[p]
    for r in S[key]:
        x = X.value(r['u'], r['v'])[0]; y = Y.value(r['u'], r['v'])[0]
        print(f"{r['kind']} {r['target']:>6g}  u={r['u']:7.1f} v={r['v']:7.1f} ub={r['ub']:4.1f} vb={r['vb']:4.1f}  t={x:7.2f} y={y:8.3f}  {r['note'][:110]}")
def draw(keys, box, zoom, path):
    im = Image.open('packet/p0208.png').convert('RGB').crop(box)
    im = im.resize(((box[2]-box[0])*zoom, (box[3]-box[1])*zoom), Image.NEAREST)
    d = ImageDraw.Draw(im)
    cols = {'run4': (230,0,0), 'run10': (0,160,0), 'run12': (0,0,255)}
    for key in keys:
        c = cols[key.split('_')[1]]
        for r in S[key]:
            x, y = (r['u']-box[0])*zoom, (r['v']-box[1])*zoom
            d.line([(x - r['ub']*zoom, y), (x + r['ub']*zoom, y)], fill=c, width=1)
            d.line([(x, y - r['vb']*zoom), (x, y + r['vb']*zoom)], fill=c, width=1)
            d.ellipse([x-3, y-3, x+3, y+3], fill=c)
    im.save(path)
if __name__ == '__main__':
    if sys.argv[1] == 'table':
        table(sys.argv[2])
    else:
        keys = sys.argv[2].split(','); box = [int(a) for a in sys.argv[3].split(',')]; zoom = int(sys.argv[4]); draw(keys, box, zoom, sys.argv[5])
