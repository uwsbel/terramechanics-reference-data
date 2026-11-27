"""Template matching for plotted symbols (helper written by the reader; not part of tools/).

Synthesizes ideal binary templates for each symbol, correlates them with the thresholded page
image inside a box, and lists local maxima above a threshold. The output is a candidate list that
the reader checks by eye; nothing here enters the points file without that check.
Usage: python find_markers.py <image> u0 v0 u1 v1 <symbol> [--thr T] [--out csv]
"""
import sys, numpy as np
from PIL import Image, ImageDraw

def template(sym):
    S = 41; c = S // 2
    im = Image.new("L", (S, S), 0); d = ImageDraw.Draw(im)
    inner = Image.new("L", (S, S), 0); di = ImageDraw.Draw(inner)
    w = 5
    if sym == "asterisk":
        r = 12
        for k in range(3):
            a = np.pi / 2 + k * np.pi / 3
            d.line([(c - r * np.cos(a), c - r * np.sin(a)), (c + r * np.cos(a), c + r * np.sin(a))], fill=255, width=w)
    elif sym == "x":
        r = 10
        d.line([(c - r, c - r), (c + r, c + r)], fill=255, width=w)
        d.line([(c - r, c + r), (c + r, c - r)], fill=255, width=w)
    elif sym == "square":
        h = 11
        d.rectangle([c - h, c - h, c + h, c + h], outline=255, width=w)
        di.rectangle([c - h + w + 1, c - h + w + 1, c + h - w - 1, c + h - w - 1], fill=255)
    elif sym == "triangle-up":
        h = 13
        pts = [(c, c - h), (c - h, c + h * 0.6), (c + h, c + h * 0.6)]
        d.polygon(pts, outline=255); d.line(pts + [pts[0]], fill=255, width=w)
        di.polygon([(c, c - h + 8), (c - h + 7, c + h * 0.6 - 4), (c + h - 7, c + h * 0.6 - 4)], fill=255)
    elif sym == "circle":
        r = 13
        d.ellipse([c - r, c - r, c + r, c + r], outline=255, width=w)
        di.ellipse([c - r + w + 1, c - r + w + 1, c + r - w - 1, c + r - w - 1], fill=255)
    elif sym == "dot":
        r = 9
        d.ellipse([c - r, c - r, c + r, c + r], fill=255)
    else:
        raise SystemExit("unknown symbol")
    ink = np.array(im) > 127
    hole = np.array(inner) > 127
    t = ink.astype(float) - 1.5 * hole.astype(float)
    return t, ink.sum()

def main():
    a = sys.argv
    img = np.array(Image.open(a[1]).convert("L")) < 128
    u0, v0, u1, v1 = map(int, a[2:6]); sym = a[6]
    thr = 0.55; out = None
    if "--thr" in a: thr = float(a[a.index("--thr") + 1])
    if "--out" in a: out = a[a.index("--out") + 1]
    sub = img[v0:v1, u0:u1].astype(float)
    t, n_ink = template(sym)
    S = t.shape[0]; c = S // 2
    H, W = sub.shape
    F = np.fft.rfft2(sub, s=(H + S, W + S))
    T = np.fft.rfft2(t[::-1, ::-1], s=(H + S, W + S))
    corr = np.fft.irfft2(F * T, s=(H + S, W + S))[c:c + H, c:c + W] / n_ink
    # local maxima with suppression radius
    R = 10
    cands = []
    ys, xs = np.where(corr >= thr)
    order = np.argsort(-corr[ys, xs])
    taken = []
    for k in order:
        y, x = ys[k], xs[k]
        if any((y - ty) ** 2 + (x - tx) ** 2 <= R * R for ty, tx in taken):
            continue
        taken.append((y, x))
        cands.append((u0 + x, v0 + y, corr[y, x]))
    cands.sort()
    lines = [f"{u},{v},{s:.3f}" for u, v, s in cands]
    print(f"{sym}: {len(cands)} candidates (thr {thr})")
    print("\n".join(lines))
    if out:
        with open(out, "w") as f:
            f.write("pixel_u,pixel_v,score\n" + "\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
