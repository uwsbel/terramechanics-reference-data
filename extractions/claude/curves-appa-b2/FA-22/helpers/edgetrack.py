"""Fine tracking of one curve on the page ink, row by row (the curves run from lower right to upper
left at |du/dv| < 2.5 below v = 1450): every `step` rows, the run of ink nearest the predicted centre is
taken in each of the rows v-6..v+6; its left and right edges are fitted separately with straight lines
(robustly: an edge touched by a crossing grid line is an outlier), and the centre at v is the mean of
the two edge lines. Rows crossed by a horizontal grid line (a run much wider than the stroke) are skipped.
A dash gap is a stretch with no run near the prediction; a symbol a stretch with runs much wider than
the stroke. The prediction is the last two good centres extrapolated. Output: a list of track points
(v, u, kind, width). A measuring aid; every sample taken from it is checked by eye."""
import json, sys
import numpy as np
import fa22lib as L

INK = L.page() < 128

def runs(row, a, b):
    a, b = max(a, 0), min(b, len(row))
    seg = row[a:b]; out = []; i = 0
    while i < len(seg):
        if seg[i]:
            j = i
            while j + 1 < len(seg) and seg[j + 1]:
                j += 1
            out.append((a + i, a + j)); i = j + 1
        else:
            i += 1
    return out

def robust_line(r, x):
    r, x = np.asarray(r, float), np.asarray(x, float)
    keep = np.ones(len(r), bool)
    for _ in range(4):
        if keep.sum() < 3:
            return None
        k, c = np.polyfit(r[keep], x[keep], 1)
        res = x - (c + k * r)
        new = np.abs(res) <= max(1.2, 2.0 * np.median(np.abs(res[keep])))
        if (new == keep).all():
            break
        keep = new
    return k, c, int(keep.sum())

def measure_at(v, upred, slope, thick=9.0, half=6, tol=6.0):
    """centre of the stroke at row v (float) near upred; returns (u, width, nrows, kind)."""
    w_exp = thick * np.sqrt(1 + slope ** 2)
    rows, L_, R_ = [], [], []
    wide = 0
    for r in range(int(round(v)) - half, int(round(v)) + half + 1):
        uc = upred + slope * (r - v)
        rr = runs(INK[r], int(uc - w_exp - 25), int(uc + w_exp + 25))
        cand = [x for x in rr if x[1] >= uc - w_exp / 2 - tol and x[0] <= uc + w_exp / 2 + tol]
        if not cand:
            continue
        x = min(cand, key=lambda x: abs((x[0] + x[1]) / 2 - uc))
        wid = x[1] - x[0] + 1
        if wid > 2.2 * w_exp + 8:
            wide += 1
            continue                      # a horizontal grid line, or a symbol
        rows.append(r - v); L_.append(x[0]); R_.append(x[1])
    if len(rows) < 4:
        return None, None, len(rows), ("wide" if wide >= 4 else "gap")
    fl, fr = robust_line(rows, L_), robust_line(rows, R_)
    if fl is None or fr is None:
        return None, None, len(rows), "fit"
    u = 0.5 * (fl[1] + fr[1]); width = fr[1] - fl[1] + 1
    kind = "ok" if 0.55 * w_exp <= width <= 1.6 * w_exp + 3 else ("thin" if width < 0.55 * w_exp else "thick")
    return u, width, len(rows), kind

def track(seed, v_end, step=4, slope0=0.5, thick=9.0):
    """from seed (u, v) along decreasing v (towards the coarse end) when v_end < v, else increasing."""
    u, v = seed
    d = -1 if v_end < v else 1
    pts = [(v, u)]
    good = [(v, u)]
    out = []
    slope = slope0
    vv = v
    while (vv - v_end) * d < 0:
        vv += d * step
        if len(good) >= 2:
            (va, ua), (vb, ub) = good[-2], good[-1]
            if abs(vb - va) > 0:
                slope = 0.5 * slope + 0.5 * (ub - ua) / (vb - va) if abs(vb - va) < 3 * step else (ub - ua) / (vb - va)
        upred = good[-1][1] + slope * (vv - good[-1][0])
        uc, wd, n, kind = measure_at(vv, upred, slope, thick)
        if uc is not None and abs(uc - upred) <= 6 and kind == "ok":
            good.append((vv, uc))
        out.append({"v": vv, "u": uc, "upred": upred, "w": wd, "n": n, "kind": kind if uc is not None else kind, "slope": slope})
    return out

if __name__ == "__main__":
    name, su, sv, vend = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    s0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
    tr = track((su, sv), vend, slope0=s0)
    (L.OUT / "helpers" / f"track-{name}.json").write_text(json.dumps(tr, indent=0), encoding="utf-8")
    for p in tr:
        if p["kind"] != "ok" or int(p["v"]) % 20 == 0:
            print(f"v {p['v']:.0f} u {p['u'] if p['u'] is None else round(p['u'],1)} pred {p['upred']:.1f} w {p['w'] if p['w'] is None else round(p['w'],1)} n {p['n']} {p['kind']} s {p['slope']:.2f}")
