"""Guided column measurement of the six FC-23 curves (Claude reader's helper).

Each curve has a guide polyline (helpers/guides.json) written by the reader from the ink pieces
and column runs; the guide only says which run belongs to which curve. In every column the run
nearest the guide is taken; where another curve's guide or a horizontal grid line lies within the
run, the run is a merge of two lines and this curve's centre is taken from the edge on its own side
(edge + half the line's vertical thickness), with a wider bound. A column on a vertical grid line or
the frame is not measured. Output: tracks/<name>_m.json, one record per column.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
CAL = json.loads((OUT / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
VL = [(l["u_at_v0"], l["slope_du_dv"]) for l in CAL["vertical_lines"]]
VL_FRAME = [(768.5, 0.0093), (2639.0, 0.0082)]   # frame lines (not labelled), measured on rows 1400 to 3500
HL = [(l["v_at_u0"], l["slope_dv_du"]) for l in CAL["horizontal_lines"]]
G = json.loads((HERE / "guides.json").read_text())
T_PERP = 8.0      # line thickness across the line, px (column runs of 9 at slope 0.5)
T_GRID = 5.0


def gv(name, u):
    a = np.array(G[name], dtype=float)
    return float(np.interp(u, a[:, 0], a[:, 1], left=np.nan, right=np.nan))


def gslope(name, u):
    a, b = gv(name, u - 8), gv(name, u + 8)
    if np.isnan(a) or np.isnan(b):
        a2 = np.array(G[name], dtype=float)
        i = 0 if u < a2[0, 0] + 8 else -2
        return float((a2[i + 1, 1] - a2[i, 1]) / (a2[i + 1, 0] - a2[i, 0]))
    return (b - a) / 16


def extend(col, a, b):
    h = len(col)
    while a > 0 and col[a - 1]:
        a -= 1
    while b < h - 1 and col[b + 1]:
        b += 1
    return a, b


def measure(dark, name, u_lo, u_hi):
    recs = []
    a_g = np.array(G[name], dtype=float)
    for u in range(u_lo, u_hi + 1):
        uu = min(max(u, a_g[0, 0]), a_g[-1, 0])
        g = float(np.interp(uu, a_g[:, 0], a_g[:, 1]))
        if u < a_g[0, 0] or u > a_g[-1, 0]:
            g = g + gslope(name, uu) * (u - uu)
        s = gslope(name, uu)
        tv = T_PERP * np.sqrt(1 + s * s)
        rec = {"u": u, "g": round(g, 1), "tv": round(tv, 1)}
        if any(abs(u - (a + b * g)) <= 3.5 for a, b in VL) or any(abs(u - (a + b * g)) <= 6.5 for a, b in VL_FRAME):
            rec["status"] = "grid"
            recs.append(rec)
            continue
        col = dark[:, u]
        lo, hi = int(g - 20), int(g + 20)
        runs = []
        i = lo
        while i <= hi:
            if col[i]:
                a, b = extend(col, i, i)
                runs.append((a, b))
                i = b + 1
            else:
                i += 1
        best = None
        for a, b in runs:
            c = 0.5 * (a + b)
            inside = a - 3 <= g <= b + 3
            d = 0 if inside else min(abs(g - a), abs(g - b))
            if d <= 4 and (best is None or d < best[0] or (d == best[0] and abs(c - g) < abs(0.5 * sum(best[1]) - g))):
                best = (d, (a, b))
        if best is None:
            rec["status"] = "gap"
            recs.append(rec)
            continue
        a, b = best[1]
        th = b - a + 1
        rec["run"] = [a, b]
        # other lines near this run
        others = []
        for o in G:
            if o == name:
                continue
            ov = gv(o, u)
            if not np.isnan(ov) and a - 6 <= ov <= b + 6:
                so = gslope(o, u)
                others.append((o, ov, T_PERP * np.sqrt(1 + so * so)))
        for c0, sl in HL:
            hv = c0 + sl * u
            if a - 4 <= hv <= b + 4:
                others.append(("hgrid", hv, T_GRID))
        c = 0.5 * (a + b)
        if not others:
            if th <= tv + 4:
                rec.update(status="ink", v=c, vb=th / 2)
            else:
                rec.update(status="thick", v=c, vb=th / 2)
        elif th <= tv + 3 and all(o[0] != "hgrid" for o in others):
            # a single line's run: this curve's, the other's, or both coincident
            dg = abs(c - g)
            do = min(abs(c - o[1]) for o in others)
            if do - dg > 3:
                rec.update(status="ink", v=c, vb=th / 2, near=[o[0] for o in others])
            elif dg - do > 3:
                rec.update(status="other", near=[o[0] for o in others])
            else:
                rec.update(status="coincident", v=c, vb=th / 2 + 1, near=[o[0] for o in others])
        else:
            ovs = [o[1] for o in others]
            if all(o[0] == "hgrid" for o in others) and th <= tv + 1.5:
                rec.update(status="ink", v=c, vb=th / 2, near=["hgrid"])
            elif g < min(ovs) - 1.5:
                rec.update(status="top-edge", v=a + tv / 2, vb=tv / 2 + 1.5, near=[o[0] for o in others])
            elif g > max(ovs) + 1.5:
                rec.update(status="bottom-edge", v=b - tv / 2, vb=tv / 2 + 1.5, near=[o[0] for o in others])
            else:
                rec.update(status="mid-merge", v=c, vb=th / 2, near=[o[0] for o in others])
        recs.append(rec)
    return recs


if __name__ == "__main__":
    img = sys.argv[1]
    names = sys.argv[2].split(",")
    g = np.asarray(Image.open(img).convert("L"))
    dark = g < 150
    for n in names:
        a = np.array(G[n])
        recs = measure(dark, n, int(a[0, 0]) - 12, int(a[-1, 0]) + 12)
        (OUT / "tracks" / f"{n}_m.json").write_text(json.dumps(recs), encoding="utf-8")
        st = {}
        for r in recs:
            st[r["status"]] = st.get(r["status"], 0) + 1
        inkish = [r for r in recs if r["status"] in ("ink", "top-edge", "bottom-edge", "coincident", "mid-merge", "thick")]
        dev = [r["v"] - r["g"] for r in recs if r["status"] == "ink"]
        print(n, st, "ink u", inkish[0]["u"], inkish[-1]["u"], "guide dev median %.1f max %.1f" % (np.median(np.abs(dev)), np.max(np.abs(dev))))
