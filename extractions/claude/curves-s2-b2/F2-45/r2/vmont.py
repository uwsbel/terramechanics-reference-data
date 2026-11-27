"""Verification montage: diag crops (with the points file) centered on given page points, tiled 2 per row.
Usage: vmont.py out.png half zoom u,v u,v ..."""
import sys, subprocess
from PIL import Image
out, half, z = sys.argv[1], int(sys.argv[2]), sys.argv[3]
ims = []
for k, c in enumerate(sys.argv[4:]):
    u, v = map(int, c.split(','))
    p = f'out/F2-45/r2/_v{k}.png'
    subprocess.run([sys.executable, 'out/F2-45/r2/diag.py', str(u - half), str(v - half), str(u + half), str(v + half), z, p,
                    'out/F2-45/points-p1.csv'], check=True, capture_output=True)
    ims.append(Image.open(p))
W, H = ims[0].size
M = Image.new('RGB', (2 * W + 6, ((len(ims) + 1) // 2) * (H + 6)), (60, 60, 60))
for k, im in enumerate(ims):
    M.paste(im, ((k % 2) * (W + 6), (k // 2) * (H + 6)))
M.save(out); print('wrote', out, M.size)
