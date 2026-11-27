"""Refine marker centers by matched filtering with synthetic symbol templates.

Each template is defined on a (2R+1)^2 grid about the symbol's plotted center: +1 on the symbol
ink, -1 on its hollow interior (for a plus, on the white quadrants around the crossing), -0.3 on
a thin halo just outside. Triangle centers are the centroid of the outer outline (for an
equilateral outline this is also the center of the inscribed and circumscribed circles; the
bounding-box center lies H/6, about 5 px, toward the apex). The best integer offset within
+-search px of the approximate center is refined with a parabola in u and in v.

python match.py <image> <in.csv> <out.csv> [--search 8]
  in.csv columns: key, symbol, u, v   (approximate centers read by eye)
  out.csv adds: u_fit, v_fit, score, score_ratio (best score / template ink count), at_search_edge
The result is only a proposal: every center is checked by eye on a contact sheet (check.py).
"""
import argparse
import csv

import numpy as np
from PIL import Image


def poly_mask(R, verts):
    """Pixels whose centers fall inside the convex polygon (verts as (du, dv) about the center)."""
    yy, xx = np.mgrid[-R:R + 1, -R:R + 1].astype(float)
    n = len(verts)
    signs = []
    for i in range(n):
        x1, y1 = verts[i]
        x2, y2 = verts[(i + 1) % n]
        signs.append((x2 - x1) * (yy - y1) - (y2 - y1) * (xx - x1))
    s = np.stack(signs)
    return (s >= 0).all(0) | (s <= 0).all(0)


def template(sym, R=24):
    yy, xx = np.mgrid[-R:R + 1, -R:R + 1].astype(float)
    w = np.zeros(xx.shape)
    if sym == "square":
        a, t = 15.0, 5.0
        outer = (abs(xx) <= a) & (abs(yy) <= a)
        inner = (abs(xx) <= a - t) & (abs(yy) <= a - t)
        halo = (abs(xx) <= a + 3) & (abs(yy) <= a + 3) & ~outer
    elif sym == "circle":
        rx, ry, t = 12.0, 12.5, 5.5
        r = np.sqrt((xx / rx) ** 2 + (yy / ry) ** 2)
        outer = r <= 1.0
        inner = np.sqrt((xx / (rx - t)) ** 2 + (yy / (ry - t)) ** 2) <= 1.0
        halo = (r <= 1.0 + 3.0 / rx) & ~outer
    elif sym in ("triangle-up", "triangle-down"):
        b, H, t = 16.0, 30.0, 5.5          # outer half-base, outer height, stroke
        base, apex = H / 3.0, -2.0 * H / 3.0   # centroid at the origin; v grows downward
        verts = [(-b, base), (b, base), (0.0, apex)]
        side = np.hypot(b, H)
        r_in = (2 * b * H / 2) / ((2 * b + 2 * side) / 2)   # area / semiperimeter
        inc_v = base - r_in
        k = max(0.0, (r_in - t) / r_in)
        iverts = [(x * k, inc_v + (y - inc_v) * k) for x, y in verts]
        kk = (r_in + 3) / r_in
        hverts = [(x * kk, inc_v + (y - inc_v) * kk) for x, y in verts]
        if sym == "triangle-down":
            verts = [(x, -y) for x, y in verts]
            iverts = [(x, -y) for x, y in iverts]
            hverts = [(x, -y) for x, y in hverts]
        outer = poly_mask(R, verts)
        inner = poly_mask(R, iverts)
        halo = poly_mask(R, hverts) & ~outer
    elif sym == "plus":
        L, t = 13.5, 3.0
        outer = ((abs(xx) <= L) & (abs(yy) <= t)) | ((abs(yy) <= L) & (abs(xx) <= t))
        inner = (abs(xx) > t + 1) & (abs(yy) > t + 1) & (abs(xx) <= L - 3) & (abs(yy) <= L - 3)
        halo = np.zeros(xx.shape, bool)
    else:
        raise ValueError(sym)
    w[outer] = 1.0
    w[inner] = -1.0
    w[halo] = -0.3
    nink = int((w == 1.0).sum())
    return w, nink


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--search", type=int, default=8)
    ap.add_argument("--dark", type=int, default=128)
    a = ap.parse_args()
    g = (np.asarray(Image.open(a.image).convert("L")) < a.dark).astype(float)
    R, S = 24, a.search
    rows = list(csv.DictReader(open(a.inp, encoding="utf-8")))
    out = []
    for r in rows:
        w, nink = template(r["symbol"], R)
        u0, v0 = int(round(float(r["u"]))), int(round(float(r["v"])))
        sc = np.full((2 * S + 1, 2 * S + 1), -1e9)
        for dv in range(-S, S + 1):
            for du in range(-S, S + 1):
                uc, vc = u0 + du, v0 + dv
                patch = g[vc - R:vc + R + 1, uc - R:uc + R + 1]
                sc[dv + S, du + S] = (patch * w).sum()
        iv, iu = np.unravel_index(np.argmax(sc), sc.shape)

        def para(m1, c, p1):
            d = m1 - 2 * c + p1
            return 0.0 if d >= 0 else 0.5 * (m1 - p1) / d

        fu = para(sc[iv, iu - 1], sc[iv, iu], sc[iv, iu + 1]) if 0 < iu < 2 * S else 0.0
        fv = para(sc[iv - 1, iu], sc[iv, iu], sc[iv + 1, iu]) if 0 < iv < 2 * S else 0.0
        edge = iu in (0, 2 * S) or iv in (0, 2 * S)
        r2 = dict(r)
        r2.update(u_fit=round(u0 + iu - S + fu, 1), v_fit=round(v0 + iv - S + fv, 1),
                  score=round(float(sc[iv, iu]), 1), score_ratio=round(float(sc[iv, iu]) / nink, 2),
                  at_search_edge=int(edge))
        out.append(r2)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n")
        wr.writeheader()
        wr.writerows(out)
    for r in out:
        print(r["key"], r["symbol"], r["u"], r["v"], "->", r["u_fit"], r["v_fit"], r["score_ratio"],
              "EDGE" if r["at_search_edge"] else "")


if __name__ == "__main__":
    main()
