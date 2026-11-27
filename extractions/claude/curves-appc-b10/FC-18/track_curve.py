"""Follow one drawn curve column by column on the page image (FC-18 blind reading helper).

    python track_curve.py <image> <calibration.json> <name> u_start v_start u_end <out.csv>

From (u_start, v_start) it steps one pixel column at a time to u_end. In each column it looks for dark
runs (gray < 140) within 12 px of the predicted line centre (a straight line fitted to the last 40
accepted columns) and keeps the run nearest the prediction. Each column gets a flag:
    ok      a run of normal size within 6 px of the prediction (used for prediction and sampling)
    vgrid   within 8 px of a vertical grid line of the calibration (the run is the grid line)
    merged  the run is longer than 1.6 times the median of the ok runs so far (a horizontal grid line,
            a circle, or the frame joins the curve here)
    hgrid   the predicted centre is within 10 px of a horizontal grid line (the run may include it)
    speck   a run shorter than 4 px (a speck or the tail of a dash), not used
    gap     no dark run within 6 px of the prediction (a gap between dashes)
Writes u, top, bottom, centre, length, flag. Nothing is fitted across a flagged stretch here; the
sampler reads only ok columns.
"""
import csv
import json
import sys

import numpy as np
from PIL import Image


def runs(col, lo):
    idx = np.where(col)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append((s + lo, p + lo))
            s = i
        p = i
    out.append((s + lo, p + lo))
    return out


def main():
    img, cal_path, name = sys.argv[1:4]
    u_s, v_s, u_e = float(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6])
    out = sys.argv[7]
    slope0 = float(sys.argv[8]) if len(sys.argv) > 8 else -0.45   # dv/du before any column is accepted
    g = np.asarray(Image.open(img).convert("L"))
    cal = json.loads(open(cal_path, encoding="utf-8").read())
    vlines = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
    hlines = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
    acc = []          # accepted (u, centre)
    lens = []
    rows = []
    vp = v_s
    for u in range(int(round(u_s)), u_e + 1):
        recent = acc[-40:]   # the last 40 accepted columns, however far back (a dash gap is bridged by extrapolation)
        if len(recent) >= 6:
            A = np.array(recent)
            k, b = np.polyfit(A[:, 0], A[:, 1], 1)
            vp = k * u + b
        elif acc:
            vp = acc[-1][1] + slope0 * (u - acc[-1][0])
        else:
            vp = v_s + slope0 * (u - u_s)
        lo, hi = int(vp - 12), int(vp + 12)
        rr = runs(g[lo:hi + 1, u] < 140, lo)
        near_grid = any(abs(u - (a + s * vp)) <= 8 for a, s in vlines)
        near_h = any(abs(vp - (a + s * u)) <= 10 for a, s in hlines)
        if not rr:
            rows.append((u, "", "", "", 0, "vgrid" if near_grid else "gap"))
            continue
        top, bot = min(rr, key=lambda r: abs((r[0] + r[1]) / 2 - vp))
        c = (top + bot) / 2
        ln = bot - top + 1
        med = np.median(lens) if len(lens) >= 5 else 10
        if near_grid:
            flag = "vgrid"
        elif near_h:
            flag = "hgrid"
        elif ln < 4:
            flag = "speck"
        elif abs(c - vp) > 6:
            flag = "gap"
        elif ln > 1.6 * med:
            flag = "merged"
        else:
            flag = "ok"
            acc.append((u, c))
            lens.append(ln)
        rows.append((u, top, bot, round(c, 2), ln, flag))
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["u", "top", "bottom", "centre", "length", "flag"])
        w.writerows(rows)
    fl = [r[5] for r in rows]
    print(f"{name}: {len(rows)} columns, ok {fl.count('ok')}, vgrid {fl.count('vgrid')}, merged {fl.count('merged')}, "
          f"gap {fl.count('gap')}; median ok run {np.median(lens):.1f} px")
    # stretches of non-ok columns
    s = None
    for r in rows + [(None, 0, 0, 0, 0, "ok")]:
        if r[5] != "ok" and s is None:
            s = r
        elif r[5] == "ok" and s is not None:
            prev = rows[rows.index(s):] if r[0] is None else rows[rows.index(s):rows.index(r)]
            flags = sorted(set(x[5] for x in prev))
            print(f"   u {s[0]}..{prev[-1][0]} ({len(prev)} cols): {','.join(flags)}")
            s = None


if __name__ == "__main__":
    main()
