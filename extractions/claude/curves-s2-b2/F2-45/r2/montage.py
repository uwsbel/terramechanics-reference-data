"""Tile several plot_grid crops into one image. Usage: montage.py out.png ncols name:u0,v0,u1,v1:zoom ..."""
import sys, subprocess
from PIL import Image, ImageDraw
out, ncol = sys.argv[1], int(sys.argv[2])
ims = []
for spec in sys.argv[3:]:
    name, box, z = spec.split(':')
    b = box.split(',')
    p = f'out/F2-45/r2/_m_{name}.png'
    subprocess.run([sys.executable, 'tools/plot_grid.py', 'crop', 'packet/p0106.png', '--box', *b, '--zoom', z,
                    '--step', '10', '--out', p], check=True, capture_output=True)
    im = Image.open(p).convert('RGB')
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 60, 16], fill=(255, 255, 0)); d.text((3, 3), name, fill=(0, 0, 0))
    ims.append(im)
W = max(i.size[0] for i in ims); H = max(i.size[1] for i in ims)
nrow = (len(ims) + ncol - 1) // ncol
M = Image.new('RGB', (ncol * (W + 6), nrow * (H + 6)), (80, 80, 80))
for k, im in enumerate(ims):
    M.paste(im, ((k % ncol) * (W + 6), (k // ncol) * (H + 6)))
M.save(out); print('wrote', out, M.size)
