"""Dense ink track of one drawn curve: for every column u in a range, the dark run (center v,
thickness) nearest a guide polyline, skipping columns where a plotted symbol (any series) or a
vertical grid line sits, and flagging runs that touch a horizontal grid line. Output is a
per-column CSV the reader then samples from; nothing here decides a reading on its own.

python track.py <image> --guide "u,v;u,v;..." --u0 U --u1 U --out track.csv
       [--win 14] [--markers markers.csv] [--vgrid 955,1245,...] [--hgrid 925,1215,...]
"""
import argparse
import csv

import numpy as np
from PIL import Image


def runs(mask, off):
    idx = np.where(mask)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append(((s + p) / 2 + off, p - s + 1, s + off, p + off))
            s = i
        p = i
    out.append(((s + p) / 2 + off, p - s + 1, s + off, p + off))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--guide", default="")
    ap.add_argument("--u0", type=int, required=True)
    ap.add_argument("--u1", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--win", type=float, default=14)
    ap.add_argument("--markers", default="")
    ap.add_argument("--panel", default="1")
    ap.add_argument("--vgrid", default="")
    ap.add_argument("--hgrid", default="")
    ap.add_argument("--dark", type=int, default=128)
    ap.add_argument("--cal", default="", help="calibration.json: grid lines with their tilt (overrides --vgrid/--hgrid)")
    ap.add_argument("--vgrid-excl", type=float, default=8)
    ap.add_argument("--min-thick", type=int, default=1, help="ignore thinner runs (stray dashes are 1 to 4 px)")
    ap.add_argument("--guide-file", default="", help="CSV with columns u,v: a dense guide (overrides --guide)")
    a = ap.parse_args()
    g = np.asarray(Image.open(a.image).convert("L")) < a.dark
    if a.guide_file:
        gu = np.array([[float(r["u"]), float(r["v"])] for r in csv.DictReader(open(a.guide_file, encoding="utf-8"))])
    else:
        gu = np.array([[float(t) for t in p.split(",")] for p in a.guide.split(";")])
    order = np.argsort(gu[:, 0])
    gu = gu[order]
    boxes = []
    if a.markers:
        for r in csv.DictReader(open(a.markers, encoding="utf-8")):
            if r["panel"] != a.panel:
                continue
            h = 13 if r["symbol"] in ("circle",) else 16
            boxes.append((float(r["pixel_u"]), float(r["pixel_v"]), h))
    vgrid = [(float(x), 0.0) for x in a.vgrid.split(",") if x]
    hgrid = [(float(x), 0.0) for x in a.hgrid.split(",") if x]
    if a.cal:
        import json
        cal = json.load(open(a.cal, encoding="utf-8"))
        vgrid = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
        hgrid = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
        # frame lines not in the calibration (left frame of the upper panel)
        vgrid.append((638.0, 0.0))
    rows = []
    for u in range(a.u0, a.u1 + 1):
        vg = float(np.interp(u, gu[:, 0], gu[:, 1]))
        lo, hi = int(vg - a.win - 25), int(vg + a.win + 25)
        col = g[lo:hi, u - 1:u + 2].any(1)
        cand = [r for r in runs(col, lo) if abs(r[0] - vg) <= a.win + r[1] / 2 and r[1] >= a.min_thick]
        flag = []
        if any(abs(u - (x0 + sl * vg)) <= a.vgrid_excl for x0, sl in vgrid):
            flag.append("vgrid")
        # drop runs that lie inside a symbol box
        keep = []
        for c in cand:
            inside = any(abs(u - bu) <= bh + 1 and c[2] <= bv + bh + 1 and c[3] >= bv - bh - 1 for bu, bv, bh in boxes)
            if not inside:
                keep.append(c)
            else:
                flag.append("symbol")
        if keep:
            c = min(keep, key=lambda c: abs(c[0] - vg))
            if any(c[2] - 4 <= (h0 + sl * u) <= c[3] + 4 for h0, sl in hgrid):
                flag.append("hgrid")
            rows.append(dict(u=u, v=c[0], thick=c[1], top=c[2], bot=c[3], guide=round(vg, 1), flags="|".join(sorted(set(flag)))))
        else:
            rows.append(dict(u=u, v="", thick="", top="", bot="", guide=round(vg, 1), flags="|".join(sorted(set(flag + ["none"])))))
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {a.out}: {len(rows)} columns, {sum(1 for r in rows if r['v'] != '')} with ink")


if __name__ == "__main__":
    main()
