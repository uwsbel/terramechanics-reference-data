"""Trace samples of one panel from its dense center line (centerline.py): at the sampling times
(every 0.002 s to 0.02 s, every 0.005 s after) and, where consecutive time samples differ by more than
5 lb, at every multiple of 5 lb between them. Each sample is interpolated between the two nearest
center-line points around it (in time, or in load on a steep stretch), preferring clean chords (not
touching a grid line, not longer than 14 px). The local line width is measured from the chords and
the line's direction (w = chord x |sin| for a chord along constant time, chord x |cos| along constant
load); the bound is half of it. Prints the samples and local extrema; writes samples-p<n>.json."""
import json
import sys
import numpy as np
from trace_tools import Panel, DARK

n = int(sys.argv[1])
cl = json.load(open(f"centerline-p{n}.json"))["points"]
t_first, t_last = float(sys.argv[2]), float(sys.argv[3])
P = Panel(n)
for p in cl:
    p["clean"] = p["kind"] in ("row", "col") and p["chord"] <= 14
clean = sorted([p for p in cl if p["clean"]], key=lambda p: p["x"])
alls = sorted(cl, key=lambda p: p["x"])


def direction(i, pts):
    a, b = pts[max(0, i - 3)], pts[min(len(pts) - 1, i + 3)]
    du, dv = b["u"] - a["u"], b["v"] - a["v"]
    h = np.hypot(du, dv) or 1.0
    return du / h, dv / h


def width(p, i, pts):
    du, dv = direction(i, pts)
    # constant-time lines run nearly along u, constant-load lines nearly along v
    if p["kind"].startswith("row"):
        return p["chord"] * abs(dv)
    return p["chord"] * abs(du)


W = []
for i, p in enumerate(clean):
    W.append(width(p, i, clean))
W = np.array(W)


def local_w(x):
    idx = np.argsort([abs(p["x"] - x) for p in clean])[:9]
    return float(np.median(W[idx]))


def interp_t(t):
    for pool, tol, flag in ((clean, 0.0004, ""), (alls, 0.0006, "amb")):
        lo = [p for p in pool if p["x"] <= t and t - p["x"] <= tol]
        hi = [p for p in pool if p["x"] >= t and p["x"] - t <= tol]
        if lo and hi:
            a, b = max(lo, key=lambda p: p["x"]), min(hi, key=lambda p: p["x"])
            f = 0 if b["x"] == a["x"] else (t - a["x"]) / (b["x"] - a["x"])
            return a["u"] + f * (b["u"] - a["u"]), a["v"] + f * (b["v"] - a["v"]), flag
    return None


def interp_y(y, t1, t2):
    # clean chords first; at a grid line (no clean chord along it) across the gap, up to 0.0012 s wide
    for pool, gap, flag in ((clean, 0.0006, ""), (clean, 0.0012, "across a grid line")):
        seg = [p for p in pool if t1 - 0.0003 <= p["x"] <= t2 + 0.0003]
        for a, b in zip(seg, seg[1:]):
            if (a["y"] - y) * (b["y"] - y) <= 0 and a["y"] != b["y"]:
                if b["x"] - a["x"] > gap:
                    break
                f = (y - a["y"]) / (b["y"] - a["y"])
                return a["u"] + f * (b["u"] - a["u"]), a["v"] + f * (b["v"] - a["v"]), flag
    return None


TIMES = [round(0.002 * k, 3) for k in range(1, 11)] + [round(0.02 + 0.005 * k, 3) for k in range(1, 17)]
TIMES = [t for t in TIMES if t_first < t <= t_last + 1e-9]
out = []
for t in TIMES:
    r = interp_t(t)
    if r is None:
        print(f"t={t}: no center line"); continue
    u, v, flag = r
    x, y = P.xy(u, v)
    out.append({"by": "time", "target": t, "u": u, "v": v, "x": x, "y": y, "w": local_w(x), "flag": flag})
# steep stretches: every multiple of 5 lb between consecutive time samples more than 5 lb apart
extra = []
for a, b in zip(out, out[1:]):
    if abs(b["y"] - a["y"]) > 5:
        lo, hi = sorted((a["y"], b["y"]))
        for y in np.arange(np.ceil(lo / 5) * 5, hi, 5):
            if abs(y - a["y"]) < 0.5 or abs(y - b["y"]) < 0.5:
                continue
            r = interp_y(float(y), a["x"], b["x"])
            if r is None:
                print(f"y={y} between t={a['target']} and {b['target']}: not found"); continue
            u, v, flag = r
            x, yy = P.xy(u, v)
            extra.append({"by": "load", "target": float(y), "u": u, "v": v, "x": x, "y": yy, "w": local_w(x), "flag": flag})
allS = sorted(out + extra, key=lambda s: s["x"])
for s in allS:
    vi, ui = int(round(s["v"])), int(round(s["u"]))
    s["ink"] = bool(DARK[vi - 2:vi + 3, ui - 2:ui + 3].any())
    print(f"{s['by']:5s} {s['target']:7.3f}  u={s['u']:8.2f} v={s['v']:8.2f}  x={s['x']:.5f} y={s['y']:8.2f}  w={s['w']:.1f} {s['flag']} {'' if s['ink'] else 'NO INK'}")
# local extrema of the clean center line (smoothed over 7 points)
ys = np.array([p["y"] for p in clean]); xs = np.array([p["x"] for p in clean])
k = 7
ysm = np.convolve(ys, np.ones(k) / k, mode="same")
for i in range(k, len(ys) - k):
    w = ysm[(xs >= xs[i] - 0.004) & (xs <= xs[i] + 0.004)]
    if ysm[i] == w.max() or ysm[i] == w.min():
        kind = "max" if ysm[i] == w.max() else "min"
        # report only clear extrema: 0.3 lb or more above (below) the line on both sides within 0.01 s
        L = ysm[(xs >= xs[i] - 0.010) & (xs <= xs[i] - 0.001)]
        R = ysm[(xs <= xs[i] + 0.010) & (xs >= xs[i] + 0.001)]
        if len(L) and len(R):
            dl = ysm[i] - (L.min() if kind == "max" else L.max())
            dr = ysm[i] - (R.min() if kind == "max" else R.max())
            if (kind == "max" and dl > 0.3 and dr > 0.3) or (kind == "min" and dl < -0.3 and dr < -0.3):
                print(f"extremum {kind}: x={xs[i]:.5f} y={ysm[i]:.2f} u={clean[i]['u']:.1f} v={clean[i]['v']:.1f}")
json.dump({"panel": n, "samples": allS}, open(f"samples-p{n}.json", "w"), indent=1)
