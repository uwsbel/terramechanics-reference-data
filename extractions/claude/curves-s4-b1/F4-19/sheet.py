"""Contact sheet: one zoomed crop per sample, the sample drawn with its bounds, for checking by eye."""
import sys, json
from PIL import Image, ImageDraw, ImageFont
S = json.load(open('out/F4-19/samples.json'))
img = Image.open('packet/p0208.png').convert('RGB')
def sheet(items, path, half=24, zoom=5, cols=6):
    W = 2*half*zoom
    rows = (len(items)+cols-1)//cols
    out = Image.new('RGB', (cols*W, rows*(W+16)), 'white')
    d = ImageDraw.Draw(out)
    for k,(label, r) in enumerate(items):
        u, v = r['u'], r['v']
        box = (int(u)-half, int(v)-half, int(u)+half, int(v)+half)
        c = img.crop(box).resize((W, W), Image.NEAREST)
        dc = ImageDraw.Draw(c)
        x, y = (u-box[0])*zoom, (v-box[1])*zoom
        col = (255,0,0)
        dc.line([(x-r['ub']*zoom, y), (x+r['ub']*zoom, y)], fill=col, width=2)
        dc.line([(x, y-r['vb']*zoom), (x, y+r['vb']*zoom)], fill=col, width=2)
        dc.ellipse([x-4,y-4,x+4,y+4], outline=(0,200,0), width=2)
        X, Y = (k%cols)*W, (k//cols)*(W+16)
        out.paste(c, (X, Y+16))
        d.text((X+2, Y+1), label, fill=(0,0,0))
    out.save(path)
if __name__ == '__main__':
    sel = sys.argv[1]   # e.g. 1_run4 or list "1_run4:t:7,1_run10:f:50"
    items = []
    if ':' in sel:
        for s in sel.split(','):
            key, kind, tgt = s.split(':')
            for r in S[key]:
                if r['kind']==kind and abs(r['target']-float(tgt))<1e-6:
                    items.append((f"{key} {kind}{tgt}", r))
    else:
        for key in sel.split('+'):
            for r in S[key]:
                items.append((f"{key} {r['kind']}{r['target']:g}", r))
    sheet(items, sys.argv[2], cols=int(sys.argv[3]) if len(sys.argv)>3 else 6)
    print(len(items))
