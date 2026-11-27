"""Fine tracking of a curve with grid-aware edges (supersedes edgetrack.py). In each row near the
prediction the stroke is the segment of ink nearest the predicted centre, where pixels of vertical grid
lines count as ink of unknown ownership: an edge of the segment that falls on a grid line is not used.
Rows where a horizontal grid line covers the stroke are skipped. Left and right edges are fitted
separately over rows v-7..v+7 (robust straight lines); the centre at v is the mean of the two edge lines
(one edge plus half the median stroke width when the other has too few rows). Output as edgetrack.py."""
import json, sys
import numpy as np
import fa22lib as L

INK = L.page() < 128
VL = np.load(L.OUT / "helpers" / "vline.npy")
HL = np.load(L.OUT / "helpers" / "hline.npy")
REAL = INK & ~VL & ~HL

def robust_line(r, x):
    r, x = np.asarray(r, float), np.asarray(x, float)
    if len(r) < 3:
        return None
    keep = np.ones(len(r), bool)
    for _ in range(5):
        if keep.sum() < 3:
            return None
        k, c = np.polyfit(r[keep], x[keep], 1)
        res = x - (c + k * r)
        new = np.abs(res) <= max(1.2, 2.5 * np.median(np.abs(res[keep])))
        if (new == keep).all():
            break
        keep = new
    return k, c, int(keep.sum())

def segments(r, a, b):
    """segments of (ink or vline) pixels in row r between a and b: (start, end, nreal, left_ok, right_ok)"""
    row_any = (INK[r] & ~HL[r]) | VL[r]
    out, i = [], a
    while i < b:
        if row_any[i]:
            j = i
            while j + 1 < b and row_any[j + 1]:
                j += 1
            nreal = int(REAL[r, i:j + 1].sum())
            out.append((i, j, nreal, bool(REAL[r, i]) and not VL[r, i - 1], bool(REAL[r, j]) and not VL[r, j + 1]))
            i = j + 1
        else:
            i += 1
    return out

def measure_at(v, upred, slope, thick=9.0, half=7, tol=7.0):
    w_exp = thick * np.sqrt(1 + slope ** 2)
    Lr, Lx, Rr, Rx, widths = [], [], [], [], []
    nrows = 0
    for r in range(int(round(v)) - half, int(round(v)) + half + 1):
        uc = upred + slope * (r - v)
        a, b = int(uc - w_exp - 30), int(uc + w_exp + 30)
        if HL[r, int(uc - w_exp / 2):int(uc + w_exp / 2) + 1].mean() > 0.5:
            continue
        segs = [s for s in segments(r, a, b) if s[2] >= 2 and s[1] >= uc - w_exp / 2 - tol and s[0] <= uc + w_exp / 2 + tol]
        if not segs:
            continue
        s = min(segs, key=lambda s: abs((s[0] + s[1]) / 2 - uc))
        if s[1] - s[0] + 1 > 2.5 * w_exp + 10:
            continue
        nrows += 1
        if s[3]: Lr.append(r - v); Lx.append(s[0])
        if s[4]: Rr.append(r - v); Rx.append(s[1])
        if s[3] and s[4]: widths.append(s[1] - s[0] + 1)
    fl, fr = robust_line(Lr, Lx), robust_line(Rr, Rx)
    if fl and fr:
        u, width, how = 0.5 * (fl[1] + fr[1]), fr[1] - fl[1] + 1, "both"
    elif fl and widths:
        u, width, how = fl[1] + np.median(widths) / 2 - 0.5, np.median(widths), "left"
    elif fr and widths:
        u, width, how = fr[1] - np.median(widths) / 2 + 0.5, np.median(widths), "right"
    else:
        return None, None, nrows, ("gap" if nrows < 3 else "edges")
    kind = "ok" if 0.55 * w_exp <= width <= 1.7 * w_exp + 3 else ("thin" if width < 0.55 * w_exp else "thick")
    return float(u), float(width), nrows, kind + ("" if how == "both" else "/" + how)

def track(seed, v_end, step=4, slope0=0.5, thick=9.0, maxdev=5.0):
    u, v = seed
    d = -1 if v_end < v else 1
    good = [(v, u)]
    out = []
    slope = slope0
    vv = v
    while (vv - v_end) * d < 0:
        vv += d * step
        if len(good) >= 3:
            (va, ua) = good[-3]; (vb, ub) = good[-1]
            if 0 < abs(vb - va) <= 6 * step:
                slope = (ub - ua) / (vb - va)
        upred = good[-1][1] + slope * (vv - good[-1][0])
        uc, wd, n, kind = measure_at(vv, upred, slope, thick)
        if uc is not None and abs(uc - upred) <= maxdev and kind.startswith("ok"):
            good.append((vv, uc))
        out.append({"v": vv, "u": uc, "upred": upred, "w": wd, "n": n, "kind": kind, "slope": slope,
                    "used": bool(good[-1][0] == vv)})
    return out

if __name__ == "__main__":
    name, su, sv, vend = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    s0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
    tr = track((su, sv), vend, slope0=s0)
    (L.OUT / "helpers" / f"track-{name}.json").write_text(json.dumps(tr, indent=0), encoding="utf-8")
    for p in tr:
        if not p["used"] or int(p["v"]) % 40 == 0:
            print(f"v {p['v']:.0f} u {p['u'] if p['u'] is None else round(p['u'],1)} pred {p['upred']:.1f} w {p['w'] if p['w'] is None else round(p['w'],1)} n {p['n']} {p['kind']} s {p['slope']:.2f} {'used' if p['used'] else ''}")
