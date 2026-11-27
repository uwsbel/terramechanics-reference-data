"""Draw candidate ids next to candidate blobs on a zoomed crop (for by-eye assignment)."""
import sys, csv
from PIL import Image, ImageDraw, ImageFont
img, cands, out = sys.argv[1], sys.argv[2], sys.argv[3]
u0, v0, u1, v1 = map(int, sys.argv[4:8]); zoom = float(sys.argv[8])
im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1))
im = im.resize((int((u1 - u0) * zoom), int((v1 - v0) * zoom)), Image.LANCZOS)
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("arial.ttf", int(9 * zoom))
except Exception:
    font = ImageFont.load_default()
for r in csv.DictReader(open(cands)):
    uc, vc = float(r["uc"]), float(r["vc"])
    if u0 <= uc <= u1 and v0 <= vc <= v1:
        x, y = (uc - u0) * zoom, (vc - v0) * zoom
        d.text((x + 10 * zoom, y - 14 * zoom), r["cid"], fill=(220, 0, 0), font=font)
        d.rectangle([(float(r["umin"]) - u0) * zoom, (float(r["vmin"]) - v0) * zoom, (float(r["umax"]) - u0) * zoom, (float(r["vmax"]) - v0) * zoom], outline=(0, 160, 255))
im.save(out)
print("wrote", out, im.size)
