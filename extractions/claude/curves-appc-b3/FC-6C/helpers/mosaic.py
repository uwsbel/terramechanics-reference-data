"""Make a mosaic of zoomed crops around approximate centers, each with a title, using the
project's plot_grid.py crop (unmodified) for the labeled pixel grid.
usage: mosaic.py <image> <out.png> <half> <zoom> <ncols> label:u:v [label:u:v ...]"""
import subprocess, sys, os, tempfile
from PIL import Image, ImageDraw, ImageFont
img, out, half, zoom, ncols = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
items = [s.split(":") for s in sys.argv[6:]]
here = os.path.dirname(os.path.abspath(__file__))
tool = os.path.join(here, "..", "..", "..", "tools", "plot_grid.py")
tmp = tempfile.mkdtemp()
tiles = []
for k, (lab, u, v) in enumerate(items):
    u, v = int(float(u)), int(float(v))
    p = os.path.join(tmp, f"t{k}.png")
    subprocess.run([sys.executable, "-I", tool, "crop", img, "--box", str(u - half), str(v - half), str(u + half), str(v + half),
                    "--out", p, "--zoom", str(zoom), "--step", "5"], check=True, capture_output=True)
    t = Image.open(p).convert("RGB")
    T = Image.new("RGB", (t.width, t.height + 22), (255, 255, 200))
    T.paste(t, (0, 22))
    d = ImageDraw.Draw(T)
    try:
        f = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        f = ImageFont.load_default()
    d.text((4, 2), f"{lab}  (center {u},{v})", fill=(0, 0, 0), font=f)
    tiles.append(T)
w, h = tiles[0].width, tiles[0].height
nrows = (len(tiles) + ncols - 1) // ncols
M = Image.new("RGB", (ncols * (w + 6), nrows * (h + 6)), (100, 100, 100))
for k, t in enumerate(tiles):
    M.paste(t, ((k % ncols) * (w + 6), (k // ncols) * (h + 6)))
M.save(out)
print(out, M.size)
