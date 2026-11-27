"""Draw candidate marks on a zoomed crop of the page, to check them by eye (FC-18 blind reading helper).

    python check_marks.py <image> <out.png> u0 v0 u1 v1 zoom <spec> [<spec> ...]

spec: c:u:v:r   a circle of radius r (px) centred at (u, v), drawn in red with a red centre dot
      p:u:v     a point, a small blue cross
Pixel grid lines every 10 px (light) and labels every 50 px, in page pixels.
"""
import sys

from PIL import Image, ImageDraw


def main():
    img, out = sys.argv[1], sys.argv[2]
    u0, v0, u1, v1, z = (int(x) for x in sys.argv[3:8])
    im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1))
    im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for u in range((u0 // 10) * 10, u1 + 1, 10):
        x = (u - u0) * z
        d.line([(x, 0), (x, im.height)], fill=(200, 200, 255) if u % 50 else (120, 120, 255), width=1)
        if u % 50 == 0:
            d.text((x + 2, 2), str(u), fill=(0, 0, 200))
    for v in range((v0 // 10) * 10, v1 + 1, 10):
        y = (v - v0) * z
        d.line([(0, y), (im.width, y)], fill=(200, 255, 200) if v % 50 else (60, 180, 60), width=1)
        if v % 50 == 0:
            d.text((2, y + 2), str(v), fill=(0, 120, 0))
    for spec in sys.argv[8:]:
        k, *vals = spec.split(":")
        vals = [float(x) for x in vals]
        X = lambda u: (u - u0 + 0.5) * z
        Y = lambda v: (v - v0 + 0.5) * z
        if k == "c":
            u, v, r = vals
            d.ellipse([X(u - r), Y(v - r), X(u + r), Y(v + r)], outline=(255, 0, 0), width=2)
            d.ellipse([X(u) - 3, Y(v) - 3, X(u) + 3, Y(v) + 3], fill=(255, 0, 0))
        elif k == "p":
            u, v = vals
            d.line([(X(u) - 6, Y(v)), (X(u) + 6, Y(v))], fill=(0, 120, 255), width=2)
            d.line([(X(u), Y(v) - 6), (X(u), Y(v) + 6)], fill=(0, 120, 255), width=2)
    im.save(out)
    print(f"wrote {out}: {im.width}x{im.height}")


if __name__ == "__main__":
    main()
