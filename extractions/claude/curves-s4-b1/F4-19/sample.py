"""Sample the traces of Figure 4-19 on their ink (Claude, batch curves-s4-b1) and write points-p<n>.csv.

For each trace: a dense guide (series_def.py) in drawing order; time targets (every 1 ms to 10 ms, every 2 ms
to 30 ms, every 5 ms after) and, on panel 1 where the force changes faster than 50 lb per ms, force targets
every 50 lb. Each target is the guide's crossing of the line of constant value (piecewise map of the
reader's calibration). On an auto stretch the point is moved to the ink center: the ink is read across the
guide at 7 positions within 6 px along it, a straight line is fitted to the run centers and intersected with
the line of constant value. A point that falls in a gap between dots or dashes (or in a drop-out of the
solid line) is moved along the guide to the nearest ink, and its time or force is then what the pixel says.
Bounds: half the measured line width across the line; on a dotted or long-dash trace also half the local gap
along the line (TASK.md); manual stretches carry the bounds of series_def.py.
"""
import csv
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
sys.path.insert(0, str(HERE))
import numpy as np
import calibrate_axes as C
import trace_tools as T
from series_def import SERIES, FEATURES

IMG = str(HERE.parent.parent / "packet" / "p0208.png")
G = json.loads((HERE / "guides.json").read_text())
INK, BM = T.load_clean()
DARK = T.load_gray() < T.DARK
MAPS = {1: C.piecewise_maps(str(HERE / "cal-p1"), IMG), 2: C.piecewise_maps(str(HERE / "cal-p2"), IMG)}

TGRID = [float(t) for t in range(0, 11)] + [float(t) for t in range(12, 31, 2)] + [float(t) for t in range(35, 151, 5)]
FGRID = [float(f) for f in range(0, 601, 50)]


def piece_points(pc):
    if "pts" in pc:
        return [tuple(p) for p in pc["pts"]]
    pts = [(p[0], p[1]) for p in G[pc["seg"]] if p[2]]
    if pc.get("reverse"):
        pts = pts[::-1]
    if "u" in pc:
        pts = [p for p in pts if pc["u"][0] <= p[0] <= pc["u"][1]]
    if "v" in pc:
        pts = [p for p in pts if pc["v"][0] <= p[1] <= pc["v"][1]]
    return pts


def dense_guide(pieces):
    """Resample the concatenated pieces every 1 px of arc. Returns arrays P (n,2), piece index per point."""
    pts, idx = [], []
    for k, pc in enumerate(pieces):
        pp = piece_points(pc)
        pts += pp
        idx += [k] * len(pp)
    P = np.array(pts, float)
    seg = np.hypot(*np.diff(P, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    out, oidx = [], []
    for a in np.arange(0, s[-1], 1.0):
        i = min(np.searchsorted(s, a, side="right") - 1, len(P) - 2)
        f = (a - s[i]) / seg[i] if seg[i] > 0 else 0.0
        out.append(P[i] + f * (P[i + 1] - P[i]))
        # a stretch between two pieces belongs to the manual piece if either end is manual (a crossing)
        ki, kj = idx[i], idx[i + 1]
        is_man = lambda k: "pts" in pieces[k] and len(pieces[k]["pts"]) > 1
        man = [k for k in (ki, kj) if is_man(k)]
        if man:
            oidx.append(man[0])
        elif "pts" in pieces[ki] and not is_man(ki):     # anchor point: the stretch belongs to the next auto piece
            oidx.append(kj)
        else:
            oidx.append(ki)
    out.append(P[-1]); oidx.append(idx[-1])
    return np.array(out), np.array(oidx)


def tangent(P, i, h=4):
    a, b = P[max(0, i - h)], P[min(len(P) - 1, i + h)]
    d = b - a
    n = np.hypot(*d)
    return d / n if n > 0 else np.array([1.0, 0.0])


def ink_at(p, r=2):
    u, v = int(round(p[0])), int(round(p[1]))
    return bool(DARK[v - r:v + r + 1, u - r:u + r + 1].any())


def in_band(q):
    return bool(BM[int(round(q[1])), int(round(q[0]))])


STYLE = {"style": "solid"}


def width_at(p, d, half=12.0):
    """Line width across the guide near p: median, over positions within 10 px along it (2 px on a dotted line,
    where it is the dot's size) that are not on a grid line, of the dark run (original image) through the line
    center; on a dotted line the largest such run."""
    n = np.array([-d[1], d[0]])
    ws = []
    kr = 2 if STYLE["style"] == "dotted" else 10
    for k in np.arange(-kr, kr + 0.01, 1.0):
        q = p + k * d
        if in_band(q):
            continue
        r = T.nearest_run(T.profile_runs(DARK, q, n, half), 0.0, 3.0)
        if (r is not None and r[0] > -half + 0.25 and r[1] < half - 0.25
                and not in_band(q + r[0] * n) and not in_band(q + r[1] * n)):
            ws.append(r[1] - r[0] + 0.5)
    if not ws:
        return None
    return float(max(ws)) if STYLE["style"] == "dotted" else float(np.median(ws))


def run_center(q, n, W, half=14.0, maxdist=4.0):
    """Center (offset along n) and width of the trace's ink across the line at q, on the original image. A run
    end inside a grid band is not the trace's edge: the center is then taken from the other end and the line
    width W. Returns (offset, measured width or None) or None."""
    r = T.nearest_run(T.profile_runs(DARK, q, n, half), 0.0, maxdist)
    if r is None or r[0] <= -half + 0.25 or r[1] >= half - 0.25:
        return None
    lo_b, hi_b = in_band(q + r[0] * n), in_band(q + r[1] * n)
    if not lo_b and not hi_b:
        return 0.5 * (r[0] + r[1]), r[1] - r[0] + 0.5
    if lo_b and not hi_b and r[1] - r[0] + 0.5 >= 0.6 * W:
        return r[1] + 0.25 - 0.5 * W, None
    if hi_b and not lo_b and r[1] - r[0] + 0.5 >= 0.6 * W:
        return r[0] - 0.25 + 0.5 * W, None
    return None


def snap(p, d, K, target, W):
    """Ink center near p (guide point, tangent d) on the line K = target. Returns (point, width) or None."""
    n = np.array([-d[1], d[0]])
    cs = []
    for k in np.arange(-8, 8.01, 1.0):
        if in_band(p + k * d):
            continue
        rc = run_center(p + k * d, n, W)
        if rc is not None:
            cs.append((k, rc[0], rc[1] if rc[1] is not None else np.nan))
    if len(cs) < 2:
        return None
    ks, cc, ww = (np.array(x, float) for x in zip(*cs))
    keep = ~((ww > 1.6 * W) | (ww < 0.6 * W))   # merged with another trace, or split by a hole in the ink
    if keep.sum() >= 2:
        ks, cc, ww = ks[keep], cc[keep], ww[keep]
    if len(ks) >= 4 and np.ptp(ks) >= 6:
        inl = np.ones(len(ks), bool)
        for _ in range(5):          # robust line: holes in the ink or a touching dot pull single centers off
            b, a = np.polyfit(ks[inl], cc[inl], 1)
            res = np.abs(cc - (a + b * ks))
            new = res <= max(1.5, 2.5 * np.median(res[inl]))
            if new.sum() < 3 or (new == inl).all():
                break
            inl = new
        b, a = np.polyfit(ks[inl], cc[inl], 1)
        ww = ww[inl]
    elif len(ks) >= 2 and np.ptp(ks) >= 6:
        b, a = np.polyfit(ks, cc, 1)
    else:     # centers found over a short stretch only (a dash end at a grid line): keep the guide's direction
        b, a = 0.0, float(np.mean(cc))
    line = lambda k: p + k * d + (a + b * k) * n
    kk = np.arange(-8, 8.01, 1.0)
    vals = np.array([K.value(*line(k))[0] for k in kk])
    sgn = np.sign(vals - target)
    j = np.where(np.diff(sgn) != 0)[0]
    if len(j) == 0:
        k0 = 0.0
    else:
        j = j[np.argmin(np.abs(kk[j]))]
        k0 = kk[j] + (target - vals[j]) / (vals[j + 1] - vals[j]) * (kk[j + 1] - kk[j])
    q = line(k0)
    w = width_at(q, d)
    if w is None:
        w = float(np.nanmedian(ww)) if np.isfinite(ww).any() else W
    return q, w


def snap_free(p, d, W):
    """Ink center across the guide at p (no constant-value constraint)."""
    n = np.array([-d[1], d[0]])
    rc = run_center(p, n, W)
    if rc is None:
        return None
    q = p + rc[0] * n
    w = width_at(q, d)
    return q, (w if w is not None else (rc[1] if rc[1] is not None else W))


def on_stroke(q, d, W):
    """Is q on the body of the stroke: the dark run across the line through q (original image) contains q
    and is at least half the line width (not the corner of a dot or the cap of a dash)?"""
    n = np.array([-d[1], d[0]])
    rr = T.nearest_run(T.profile_runs(DARK, q, n, 10.0), 0.0, 0.5)
    return rr is not None and (rr[1] - rr[0] + 0.5) >= 0.5 * W


def ink_profile(P, step=1):
    """Is there trace ink across the guide at each guide point (cleaned image, run within 3 px)?"""
    on = np.zeros(len(P), bool)
    for i in range(0, len(P), step):
        d = tangent(P, i)
        n = np.array([-d[1], d[0]])
        on[i] = T.nearest_run(T.profile_runs(INK, P[i], n, 6.0), 0.0, 3.0) is not None
    return on


def local_gap(on, i):
    """Mean length (px) of the white stretches next to the ink piece at or nearest guide point i."""
    n = len(on)
    if not on[i]:
        l = i
        while l > 0 and not on[l]:
            l -= 1
        r = i
        while r < n - 1 and not on[r]:
            r += 1
        return float(r - l - 1)
    l = i
    while l > 0 and on[l]:
        l -= 1
    r = i
    while r < n - 1 and on[r]:
        r += 1
    gaps = []
    a = l
    while a > 0 and not on[a]:
        a -= 1
    if l > 0:
        gaps.append(l - a)
    b = r
    while b < n - 1 and not on[b]:
        b += 1
    if r < n - 1:
        gaps.append(b - r)
    gaps = [g for g in gaps if g < 60]
    return float(np.mean(gaps)) if gaps else 0.0


def crossings(vals, target):
    out = []
    for i in range(len(vals) - 1):
        a, b = vals[i] - target, vals[i + 1] - target
        if a == 0 or a * b < 0:
            out.append(i + (0 if a == 0 else a / (a - b)))
    return out


def run(panel, sid):
    spec = SERIES[(panel, sid)]
    pieces = spec["pieces"]
    style = spec["style"]
    STYLE["style"] = style
    cal, X, Y = MAPS[panel]
    P, pidx = dense_guide(pieces)
    xs = np.array([X.value(*p)[0] for p in P])
    ys = np.array([Y.value(*p)[0] for p in P])
    on = ink_profile(P)
    samples = []
    # time targets
    for t in TGRID:
        last_arc = -1e9
        for c in crossings(xs, t):
            i = int(round(c))
            d = tangent(P, i)
            if abs(d[0]) < 0.18:      # near-vertical stretch: time is not a usable sampling coordinate there
                continue
            if c - last_arc < 15:
                continue
            last_arc = c
            samples.append(("t", t, c))
    # force targets on the steep parts (panel 1)
    if panel == 1:
        for f in FGRID:
            for c in crossings(ys, f):
                i = int(round(c))
                lo, hi = max(0, i - 15), min(len(P) - 1, i + 15)
                dx = xs[hi] - xs[lo]
                dy = ys[hi] - ys[lo]
                rate = abs(dy / dx) if dx != 0 else float("inf")
                xt = xs[i]
                dt_grid = 1.0 if xt <= 10 else (2.0 if xt <= 30 else 5.0)
                if rate * dt_grid > 50.0:
                    samples.append(("f", f, c))
    rows = []
    for kind, target, c in samples:
        i = int(round(c))
        i0 = int(math.floor(c)); f = c - i0
        g = P[i0] + f * (P[min(i0 + 1, len(P) - 1)] - P[i0])
        d = tangent(P, i)
        pc = pieces[pidx[i]]
        K = X if kind == "t" else Y
        note = []
        moved = False
        if "pts" in pc:      # manual stretch
            q = g.copy()
            width = None
            ub, vb = pc["ub"], pc["vb"]
            note.append(pc["note"])
            gaps = pc.get("gaps", [])
            in_gap = lambda pt: any(a0 <= pt[0] <= a1 for a0, a1 in gaps)
            r_ok = 0
            if in_gap(q) or not ink_at(q, r_ok):
                # move along the guide to the nearest ink of this trace (not into a declared gap)
                for k in range(1, 40):
                    for sgn in (1, -1):
                        j = i + sgn * k
                        if 0 <= j < len(P) and not in_gap(P[j]) and ink_at(P[j], r_ok):
                            q = P[j].copy(); moved = True; break
                    if moved:
                        break
                if not moved:
                    continue
                note.append("no ink of this trace at the target on the guide (gap): moved along the guide to the nearest ink")
            if style == "dotted":
                # the dot's center along the line: middle of the dark run along the guide through q
                j0 = int(np.argmin(np.hypot(*(P - q).T)))
                a_ = b_ = j0
                while a_ > 0 and ink_at(P[a_ - 1], 0) and not in_gap(P[a_ - 1]) and j0 - a_ < 14:
                    a_ -= 1
                while b_ < len(P) - 1 and ink_at(P[b_ + 1], 0) and not in_gap(P[b_ + 1]) and b_ - j0 < 14:
                    b_ += 1
                if b_ - a_ < 20:
                    qm = P[(a_ + b_) // 2].copy()
                    if np.hypot(*(qm - q)) > 1.0:
                        q = qm
                        if not moved:
                            note.append("on a dot: taken at the dot's center along the guide")
                        moved = True
        else:
            res = snap(g, d, K, target, spec['nominal']) if style != "dotted" else None
            if res is not None and not on_stroke(res[0], d, spec["nominal"]):
                res = None
            if style == "dotted" and on[i]:
                # on a dot: take that dot's center along the line (the middle of its ink along the guide)
                a_ = b_ = i
                while a_ > 0 and on[a_ - 1]:
                    a_ -= 1
                while b_ < len(P) - 1 and on[b_ + 1]:
                    b_ += 1
                m = (a_ + b_) // 2 if b_ - a_ < 30 else i
                r = snap_free(P[m], tangent(P, m), spec['nominal'])
                if r is not None and on_stroke(r[0], tangent(P, m), spec["nominal"]):
                    res = r
                    if abs(m - i) > 1:
                        moved = True
                        note.append("on a dot: taken at the dot's center")
            if res is None:
                # gap: move along the guide to the nearest ink and take the ink center there
                res2 = None
                for k in range(1, 40):
                    for sgn in (1, -1):
                        j = i + sgn * k
                        if 0 <= j < len(P) and on[j]:
                            a = b = j
                            while a > 0 and on[a - 1]:
                                a -= 1
                            while b < len(P) - 1 and on[b + 1]:
                                b += 1
                            m = (a + b) // 2 if b - a < 30 else (min(b, j + 4) if sgn > 0 else max(a, j - 4))
                            r = snap_free(P[m], tangent(P, m), spec['nominal'])
                            if r is not None and on_stroke(r[0], tangent(P, m), spec["nominal"]):
                                res2 = r; break
                    if res2 is not None:
                        break
                if res2 is None:
                    continue
                q, width = res2
                moved = True
                note.append("target fell in a gap of the line: moved along the guide to the nearest ink")
            else:
                q, width = res
            hw = max(width / 2.0, 1.0)
            ub = vb = hw
            if style in ("dotted", "long-dash"):
                gap = local_gap(on, i)
                ub = max(ub, abs(d[0]) * gap / 2.0)
                vb = max(vb, abs(d[1]) * gap / 2.0)
                note.append(f"{style} trace: bound includes half the local gap along the line ({gap:.0f} px)")
            if width > 1.6 * spec["nominal"]:
                note.append(f"ink {width:.0f} px wide here (merged with another trace or a grid line); bound is half that width")
            note.insert(0, f"line width {width:.1f} px")
        xv, yv = X.value(*q)[0], Y.value(*q)[0]
        tag = (f"sampled at t = {target:g} ms" if kind == "t" else f"sampled at {target:g} lb (steep part)")
        if moved:
            tag += f"; taken at t = {xv:.2f} ms, y = {yv:.3g}"
        rows.append({"arc": c, "kind": kind, "target": target, "u": round(float(q[0]), 1), "v": round(float(q[1]), 1),
                     "ub": round(float(ub), 1), "vb": round(float(vb), 1), "note": "; ".join([tag] + note)})
    # de-duplicate points that ended up at the same pixel (moved to the same ink)
    rows.sort(key=lambda r: r["arc"])
    out = []
    for r in rows:
        if out and abs(out[-1]["u"] - r["u"]) < 1.5 and abs(out[-1]["v"] - r["v"]) < 1.5:
            out[-1]["note"] += f"; also the target {r['target']:g} ({r['kind']}) landed here"
            continue
        out.append(r)
    return out, P, xs, ys, pidx, on


def centerline(panel, sid, P, pidx, on, step=2):
    """Dense ink centerline along the guide: snapped ink centers on auto stretches (on the body of the stroke
    only; on a dotted trace only on dots), the guide itself on manual stretches. Returns list of
    (arc index, u, v, manual)."""
    spec = SERIES[(panel, sid)]
    STYLE["style"] = spec["style"]
    out = []
    for i in range(0, len(P), step):
        pc = spec["pieces"][pidx[i]]
        if "pts" in pc and len(pc["pts"]) > 1:
            if ink_at(P[i], 0) and not any(a0 <= P[i][0] <= a1 for a0, a1 in pc.get("gaps", [])):
                out.append((i, float(P[i][0]), float(P[i][1]), True))
            continue
        if not on[i]:
            continue
        d = tangent(P, i)
        r = snap_free(P[i], d, spec["nominal"])
        if r is not None and on_stroke(r[0], d, spec["nominal"]):
            out.append((i, float(r[0][0]), float(r[0][1]), False))
    return out


def extremes(panel, sid, P, pidx, on, prom):
    """Local extremes of y along the trace (prominence `prom` in y units), from the dense centerline."""
    cal, X, Y = MAPS[panel]
    cl = centerline(panel, sid, P, pidx, on)
    U = np.array([c[1] for c in cl]); V = np.array([c[2] for c in cl])
    y = np.array([Y.value(u, v)[0] for u, v in zip(U, V)])
    # smooth over about 9 px of arc
    k = 4
    ys = np.array([np.median(y[max(0, j - k):j + k + 1]) for j in range(len(y))])
    found = []
    j = 0
    n = len(ys)
    # simple alternating extreme search with prominence
    trend = 0
    ext_j = 0
    for j in range(1, n):
        if trend >= 0:
            if ys[j] > ys[ext_j]:
                ext_j = j
            elif ys[ext_j] - ys[j] >= prom:
                if trend == 1 or (trend == 0):
                    found.append(("max", ext_j))
                trend = -1; ext_j = j
        if trend < 0:
            if ys[j] < ys[ext_j]:
                ext_j = j
            elif ys[j] - ys[ext_j] >= prom:
                found.append(("min", ext_j))
                trend = 1; ext_j = j
    out = []
    for kind, j in found:
        # flat extreme: the stretch within one pixel of v of the extreme
        vj = V[j]
        a_ = j
        while a_ > 0 and abs(V[a_ - 1] - vj) <= 1.0:
            a_ -= 1
        b_ = j
        while b_ < n - 1 and abs(V[b_ + 1] - vj) <= 1.0:
            b_ += 1
        m = (a_ + b_) // 2
        half_len = 0.5 * abs(U[b_] - U[a_])
        out.append({"kind": kind, "u": U[m], "v": V[m], "y": y[m], "half_len": half_len, "arc": cl[m][0], "manual": cl[m][3]})
    return out, cl


if __name__ == "__main__":
    res = {}
    for key in SERIES:
        rows, P, xs, ys, pidx, on = run(*key)
        res[f"{key[0]}_{key[1]}"] = rows
        ex, cl = extremes(key[0], key[1], P, pidx, on, 3.0 if key[0] == 1 else 0.02)
        res[f"{key[0]}_{key[1]}_extremes"] = ex
        res[f"{key[0]}_{key[1]}_ends"] = {"first": cl[0], "last": cl[-1]}
        print("   extremes:", [(e["kind"], round(e["u"], 1), round(e["v"], 1), round(e["y"], 3), round(e["half_len"], 1), e["manual"]) for e in ex])
        print("   ends:", cl[0], cl[-1])
        print(key, len(rows), "samples; guide", len(P), "px; t range", round(xs.min(), 2), round(xs.max(), 2))
    (HERE / "samples.json").write_text(json.dumps(res, indent=0))
