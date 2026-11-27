"""Draw the tracked column centres of the curves over a zoomed crop (FC-18 blind reading helper).

    python show_tracks.py <image> <out.png> u0 v0 u1 v1 zoom track1.csv [track2.csv ...]

ok columns are drawn as small dots in a colour per track; flagged columns as grey dots.
"""
import csv
import sys

from PIL import Image, ImageDraw

COLS = [(220, 0, 0), (0, 150, 0), (0, 0, 230)]


def main():
    img, out = sys.argv[1], sys.argv[2]
    u0, v0, u1, v1, z = (int(x) for x in sys.argv[3:8])
    im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1))
    im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for u in range((u0 // 25) * 25, u1 + 1, 25):
        x = (u - u0) * z
        d.line([(x, 0), (x, im.height)], fill=(180, 180, 255), width=1)
        if u % 100 == 0:
            d.text((x + 2, 2), str(u), fill=(0, 0, 200))
    for v in range((v0 // 25) * 25, v1 + 1, 25):
        y = (v - v0) * z
        d.line([(0, y), (im.width, y)], fill=(180, 230, 180), width=1)
        if v % 100 == 0:
            d.text((2, y + 2), str(v), fill=(0, 120, 0))
    for i, path in enumerate(sys.argv[8:]):
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if not r["centre"]:
                    continue
                u, c = float(r["u"]), float(r["centre"])
                if not (u0 <= u < u1 and v0 <= c < v1):
                    continue
                x, y = (u - u0 + 0.5) * z, (c - v0 + 0.5) * z
                col = COLS[i % 3] if r["flag"] == "ok" else (150, 150, 150)
                d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=col)
    im.save(out)
    print(f"wrote {out}: {im.width}x{im.height}")


if __name__ == "__main__":
    main()
