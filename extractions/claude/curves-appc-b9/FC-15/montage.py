import sys
from PIL import Image, ImageDraw
paths = sys.argv[2:]
ims = [Image.open(p) for p in paths]
w = max(i.width for i in ims); h = max(i.height for i in ims)
cols = 4
rows = (len(ims) + cols - 1) // cols
M = Image.new("RGB", (cols * w, rows * h), "white")
d = ImageDraw.Draw(M)
for k, im in enumerate(ims):
    x, y = (k % cols) * w, (k // cols) * h
    M.paste(im, (x, y))
    d.text((x + 5, y + 5), paths[k].split("/")[-1], fill=(0, 0, 255))
M.save(sys.argv[1])
