"""Provisional trace samples: for each curve and each sampling grain size, the centre of the curve's
ink where it crosses the line of that grain size, measured on the de-gridded ink near the waypoint
polyline (row runs over +-10 rows, a straight-line fit across rows, evaluated on the sampling line).
Every sample is then checked by eye on overlays and corrected by hand where needed."""
import sys, json, math
import numpy as np
from PIL import Image
import fa22lib as L
from waypoints import CURVES, u_at

D = np.asarray(Image.open(L.OUT / "helpers" / "degrid.png"))
REST = D == 0          # ink not on long straight grid runs
INK = D < 255          # all ink

def row_runs(row_mask, u0, u1):
    seg = row_mask[u0:u1]
    out, i = [], 0
    while i < len(seg):
        if seg[i]:
            j = i
            while j + 1 < len(seg) and seg[j + 1]:
                j += 1
            out.append((u0 + i, u0 + j))
            i = j + 1
        else:
            i += 1
    return out

def measure(curve, vs, half_rows=10, win=22):
    up = u_at(curve, vs)
    if up is None:
        return None
    # local slope du/dv of the waypoint polyline
    a, b = u_at(curve, vs - 15) or up, u_at(curve, vs + 15) or up
    slope = (b - a) / 30.0
    rows, cents, widths = [], [], []
    for r in range(int(round(vs)) - half_rows, int(round(vs)) + half_rows + 1):
        uc = up + slope * (r - vs)
        rr = row_runs(REST[r], int(uc - win), int(uc + win))
        rr = [x for x in rr if x[1] - x[0] + 1 >= 3]
        if not rr:
            continue
        best = min(rr, key=lambda x: abs((x[0] + x[1]) / 2 - uc))
        rows.append(r); cents.append((best[0] + best[1]) / 2); widths.append(best[1] - best[0] + 1)
    if len(rows) < 4:
        return {"u": up, "v": vs, "n": len(rows), "flag": "few rows", "near": False}
    R, Cc = np.array(rows, float), np.array(cents, float)
    k, c = np.polyfit(R - vs, Cc, 1)
    res = Cc - (c + k * (R - vs))
    keep = np.abs(res) <= max(2.0, 2.5 * np.median(np.abs(res)))
    if keep.sum() >= 4:
        k, c = np.polyfit(R[keep] - vs, Cc[keep], 1)
    near = any(abs(r - vs) <= 2 for r in rows)
    return {"u": float(c), "v": float(vs), "n": len(rows), "slope": float(k), "w_med": float(np.median(widths)),
            "rms": float(np.sqrt(np.mean(res[keep] ** 2))) if keep.sum() else None, "near": near,
            "flag": "" if near else "no ink within 2 rows (gap?)"}

if __name__ == "__main__":
    out = {}
    for name, cur in CURVES.items():
        vmin, vmax = min(p[1] for p in cur), max(p[1] for p in cur)
        res = []
        for e in np.arange(-1.15, 1.0001, 0.05):
            x = 10 ** round(e, 2)
            up = u_at(cur, L.v_of_x(x, 1500))
            if up is None:
                continue
            vs = L.v_of_x(x, up)
            if not (vmin <= vs <= vmax):
                continue
            m = measure(cur, vs)
            if m is None:
                continue
            m["e"] = round(float(e), 2); m["x"] = x
            res.append(m)
            print(f"{name:8s} log {e:+.2f} x {x:7.4f} v {vs:7.1f} u {m['u']:7.1f} n {m['n']:2d} w {m.get('w_med', 0):4.1f} "
                  f"slope {m.get('slope', 0):+.2f} rms {m.get('rms') or 0:.2f} {m['flag']}")
        out[name] = res
    (L.OUT / "helpers" / "tracer-out.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
