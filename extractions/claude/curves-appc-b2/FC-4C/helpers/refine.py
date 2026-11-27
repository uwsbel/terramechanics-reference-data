"""Refine approximate marker centers on the page image.

    python refine.py <image> <approx.csv> <out.csv> [--win 20] [--plus-win 13]

approx.csv: panel,series_id,symbol,u,v,note   (u, v: approximate center read from a zoom-3 crop)
out.csv:    same columns plus u_ref, v_ref, method, area, bbox, flag

Hollow symbols (circle, square, triangle-up, triangle-down): the enclosed white hole nearest the
approximate center is found inside a window; its centroid is the refined center. If no enclosed
hole exists (ring broken, hole filled by a crossing line) the row is flagged "nohole" and the
approximate center is kept for reading by eye.
Plus: the vertical and horizontal strokes are the column and row with the most dark pixels in a
small window; their crossing is the center. Flagged "weak" if a stroke is short.
Every refined center is then checked by eye on a montage (montage.py); nothing here is final.
"""
import argparse
import csv

import numpy as np
from PIL import Image


def components(mask):
    """4-connected components of a boolean array; returns label array and count."""
    h, w = mask.shape
    lab = np.zeros((h, w), dtype=int)
    n = 0
    for i in range(h):
        for j in range(w):
            if mask[i, j] and lab[i, j] == 0:
                n += 1
                stack = [(i, j)]
                lab[i, j] = n
                while stack:
                    a, b = stack.pop()
                    for c, d in ((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)):
                        if 0 <= c < h and 0 <= d < w and mask[c, d] and lab[c, d] == 0:
                            lab[c, d] = n
                            stack.append((c, d))
    return lab, n


def refine_hole(g, u, v, win):
    u0, v0 = int(round(u)) - win, int(round(v)) - win
    sub = g[v0:v0 + 2 * win + 1, u0:u0 + 2 * win + 1]
    white = sub >= 128
    lab, n = components(white)
    best = None
    for k in range(1, n + 1):
        ys, xs = np.where(lab == k)
        if ys.min() == 0 or xs.min() == 0 or ys.max() == sub.shape[0] - 1 or xs.max() == sub.shape[1] - 1:
            continue  # touches the window border: not an enclosed hole
        area = len(ys)
        if area < 12 or area > 900:
            continue
        cu, cv = xs.mean() + u0, ys.mean() + v0
        d = float(np.hypot(cu - u, cv - v))
        if best is None or d < best[0]:
            best = (d, cu, cv, area, (xs.min() + u0, ys.min() + v0, xs.max() + u0, ys.max() + v0))
    return best


def refine_plus(g, u, v, win):
    u0, v0 = int(round(u)) - win, int(round(v)) - win
    sub = g[v0:v0 + 2 * win + 1, u0:u0 + 2 * win + 1] < 128
    cols = sub.sum(axis=0)
    rows = sub.sum(axis=1)

    def peak(s):
        m = s.max()
        a = int(np.argmax(s))
        grp = [a]
        i = a - 1
        while i >= 0 and s[i] >= 0.75 * m:
            grp.append(i)
            i -= 1
        i = a + 1
        while i < len(s) and s[i] >= 0.75 * m:
            grp.append(i)
            i += 1
        grp = np.array(grp)
        return (grp * s[grp]).sum() / s[grp].sum(), int(m)

    cu, mc = peak(cols)
    cv, mr = peak(rows)
    return cu + u0, cv + v0, mc, mr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("approx")
    ap.add_argument("out")
    ap.add_argument("--win", type=int, default=20)
    ap.add_argument("--plus-win", type=int, default=13)
    a = ap.parse_args()
    g = np.asarray(Image.open(a.image).convert("L"))
    rows = list(csv.DictReader(open(a.approx, encoding="utf-8-sig", newline="")))
    out = []
    for r in rows:
        u, v = float(r["u"]), float(r["v"])
        sym = r["symbol"]
        rec = dict(r)
        if sym == "plus":
            cu, cv, mc, mr = refine_plus(g, u, v, a.plus_win)
            rec.update(u_ref=round(cu, 1), v_ref=round(cv, 1), method="plus-strokes", area=f"{mc}x{mr}",
                       bbox="", flag="" if min(mc, mr) >= 12 else "weak")
        else:
            b = refine_hole(g, u, v, a.win)
            if b is None:
                rec.update(u_ref=u, v_ref=v, method="approx", area="", bbox="", flag="nohole")
            else:
                d, cu, cv, area, bb = b
                rec.update(u_ref=round(cu, 1), v_ref=round(cv, 1), method="hole-centroid", area=area,
                           bbox=f"{bb[0]}-{bb[2]},{bb[1]}-{bb[3]}", flag="" if d < 8 else f"moved{d:.0f}")
        out.append(rec)
    cols = list(rows[0].keys()) + ["u_ref", "v_ref", "method", "area", "bbox", "flag"]
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    for i, r in enumerate(out):
        print(f"#{i:<3} {r['series_id']:>6} {r['symbol']:<14} {r['u']:>6} {r['v']:>6} -> "
              f"{r['u_ref']:>7} {r['v_ref']:>7}  {r['method']:<14} {str(r['area']):>6} {r['flag']}")


main()
