"""Stack PNG crops vertically (or horizontally with -h) into one image, separated by a gray bar."""
import sys
from PIL import Image
args = sys.argv[1:]
horiz = False
if args[0] == "-h":
    horiz = True; args = args[1:]
out, ins = args[0], args[1:]
ims = [Image.open(p).convert("RGB") for p in ins]
if horiz:
    W = sum(i.width for i in ims) + 6 * (len(ims) - 1); H = max(i.height for i in ims)
else:
    W = max(i.width for i in ims); H = sum(i.height for i in ims) + 6 * (len(ims) - 1)
canvas = Image.new("RGB", (W, H), (128, 128, 128))
p = 0
for i in ims:
    canvas.paste(i, (p, 0) if horiz else (0, p))
    p += (i.width if horiz else i.height) + 6
canvas.save(out)
print(out, W, H)
