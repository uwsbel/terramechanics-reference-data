"""Rotated, enlarged crop of the page for reading sideways text only (no coordinates are read from it).
usage: rotcrop.py image u0 v0 u1 v1 zoom angle out.png   (angle: degrees counterclockwise, PIL convention)"""
import sys
from PIL import Image
img, u0, v0, u1, v1, z, ang, out = sys.argv[1:9]
im = Image.open(img).convert("L").crop((int(u0), int(v0), int(u1), int(v1)))
im = im.resize((im.width * int(z), im.height * int(z)), Image.LANCZOS)
im = im.rotate(float(ang), expand=True, fillcolor=255)
im.save(out)
print("wrote", out, im.size)
