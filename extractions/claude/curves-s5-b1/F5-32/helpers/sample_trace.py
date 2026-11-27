"""Trace samples of one panel of Figure 5-32 from its centre line, in drawing order (time order).

Polyline: the first point (where the trace's ink meets the bottom frame), then the column centre line of a
stretch where the trace runs nearly along the page's rows (panel 3's initial rise: columns are cut instead
of rows), then the row centre line (centerline-p<n>.csv), then the last point. Values for choosing the
sampling places come from the piecewise map of the reader's calibration (tools/calibrate_axes.py, imported,
with the ink check); the values written to the native file are computed again by the tool's `piecewise`.

Samples: the first point, one every 0.002 s up to 0.02 s and every 0.005 s after, and on steep parts (where
the load changes by more than 5 lb between two such samples) also one at every multiple of 5 lb crossed, and
the last point. A sample is placed on the centre line; one that falls where the drawn line has no ink (a
break) is moved to the nearest row with ink, and says so. Bound: half the trace's thickness across the line,
measured at the sample (the row or column cut times the cosine of the line's angle to the cut), plus 1 px
where the trace runs over a grid line (merged or trimmed rows).

usage: sample_trace.py <tools_dir> <page.png> <cal_dir> <grid_measured.json> <centerline.csv> <panel>
                       <series_id> <first_u> <first_v> <last_u> <last_v> <out.csv> [col_u_from col_u_to]
"""
import csv
import json
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca  # noqa: E402


def runs(idx):
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append((s, p))
            s = i
        p = i
    out.append((s, p))
    return out


def main():
    (tools, page, cal_dir, gm, clf, pn, sid, fu, fv, lu, lv, out) = sys.argv[1:13]
    pn, fu, fv, lu, lv = int(pn), float(fu), float(fv), float(lu), float(lv)
    col_range = (int(sys.argv[13]), int(sys.argv[14])) if len(sys.argv) > 14 else None
    g = np.asarray(Image.open(page).convert("L")) < 128
    cal, X, Y = ca.piecewise_maps(cal_dir, page)
    G = json.load(open(gm, encoding="utf-8"))
    lines = G["load_lines"][str(pn)]
    frame = G["frame_t0"]

    pts = [{"u": fu, "v": fv, "w": None, "cut": "end", "flag": "first"}]
    if col_range:
        # column centre line: the trace's run in each column above the bottom frame; columns on a grid line skipped
        v_prev = fv
        for u in range(col_range[0], col_range[1] - 1, -1):
            if any(abs(u - (l["u_at_v0"] + l["slope_du_dv"] * 3460)) <= 4.5 for l in lines):
                continue
            vf_top = frame["v_at_u0"] + frame["slope_dv_du"] * u - 3   # the frame's upper edge
            col = g[3380:int(vf_top) + 8, u]
            rr = [(3380 + a, 3380 + b) for a, b in runs(np.where(col)[0])]
            rr = [r for r in rr if r[0] < vf_top - 1]
            if not rr:
                continue
            # the run nearest the previous column's centre (the trace moves less than a few px per column)
            a, b = min(rr, key=lambda r: abs((r[0] + min(r[1], vf_top - 1)) / 2 - v_prev))
            if abs((a + min(b, vf_top - 1)) / 2 - v_prev) > 6:
                continue
            flag = ""
            if b >= vf_top - 0.5:   # merged with the frame: the trace's own part ends at the frame's edge
                b = min(b, int(vf_top) - 1)
                flag = "frame"
            pts.append({"u": float(u), "v": (a + b) / 2, "w": b - a + 1, "cut": "col", "flag": flag})
            v_prev = (a + b) / 2
    with open(clf, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    v_join = pts[-1]["v"] if col_range else None
    for r in rows:
        if r["u_center"] == "":
            continue
        v = float(r["v"])
        if v_join is not None and v >= v_join:
            continue
        w = float(r["run_width"])
        flag = r["flag"] if w >= 3 else "gap"
        pts.append({"u": float(r["u_center"]), "v": v, "w": w, "cut": "row", "flag": flag})
    pts.append({"u": lu, "v": lv, "w": None, "cut": "end", "flag": "last"})
    for p in pts:
        p["x"] = X.value(p["u"], p["v"])[0]
        p["y"] = Y.value(p["u"], p["v"])[0]
    # perpendicular thickness at each point from the local direction
    U = np.array([p["u"] for p in pts]); V = np.array([p["v"] for p in pts])
    for i, p in enumerate(pts):
        lo, hi = max(0, i - 4), min(len(pts) - 1, i + 4)
        d = np.array([U[hi] - U[lo], V[hi] - V[lo]]); d = d / (np.hypot(*d) or 1)
        p["dir"] = d
        if p["w"] is None or p["flag"] == "gap":
            p["wp"] = None
        elif p["cut"] == "row":
            p["wp"] = p["w"] * abs(d[1])
        else:
            p["wp"] = p["w"] * abs(d[0])
    clean = [p["wp"] for p in pts if p["wp"] is not None and p["flag"] == ""]
    w_med = float(np.median(clean))

    def local_w(i):
        near = [pts[j]["wp"] for j in range(max(0, i - 15), min(len(pts), i + 16))
                if pts[j]["wp"] is not None and pts[j]["flag"] == ""]
        return float(np.median(near)) if near else w_med

    def interp(i, f):
        a, b = pts[i], pts[i + 1]
        return a["u"] + f * (b["u"] - a["u"]), a["v"] + f * (b["v"] - a["v"])

    def has_ink(u, v, r=2):
        ui, vi = int(round(u)), int(round(v))
        return bool(g[vi - r:vi + r + 1, ui - r:ui + r + 1].any())

    # the trace's own ink: the page's ink with the load lines (2.5 px either side of their fitted centre) and
    # the bottom frame (3.5 px) removed, as a mechanical ink check would see it
    H, W = g.shape
    vv = np.arange(H)[:, None]; uu = np.arange(W)[None, :]
    own = g.copy()
    for ls in G["load_lines"].values():
        for l in ls:
            own &= ~(np.abs(uu - (l["u_at_v0"] + l["slope_du_dv"] * vv)) <= 2.5)
    own &= ~(np.abs(vv - (frame["v_at_u0"] + frame["slope_dv_du"] * uu)) <= 3.5)

    def has_own_ink(u, v, r=2):
        ui, vi = int(round(u)), int(round(v))
        return bool(own[vi - r:vi + r + 1, ui - r:ui + r + 1].any())

    def make(i, f, kind_note):
        u, v = interp(i, f)
        j = i if f < 0.5 else i + 1
        note = kind_note
        if not has_own_ink(u, v) and pts[j]["flag"] != "gap":
            # on a grid line crossing: moved along the centre line to the nearest place with the trace's own ink
            for d in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 8, -8, 10, -10):
                k = j + d
                if 0 < k < len(pts) - 1 and pts[k]["flag"] != "gap" and has_own_ink(pts[k]["u"], pts[k]["v"]):
                    note += (f"; moved {np.hypot(pts[k]['u'] - u, pts[k]['v'] - v):.0f} px along the trace off the "
                             f"grid line it crosses here, to the trace's own ink")
                    u, v, j = pts[k]["u"], pts[k]["v"], k
                    i, f = k, 0.0
                    break
            else:
                note += "; the trace runs over a grid line here: no ink of its own once the line is removed"
        if pts[j]["flag"] == "gap" or pts[i]["flag"] == "gap" and pts[i + 1]["flag"] == "gap":
            # inside a break of the drawn line: move to the nearest point with ink
            k = min((k for k in range(len(pts)) if pts[k]["flag"] not in ("gap",) and pts[k]["cut"] != "end"),
                    key=lambda k: abs(k - j))
            u, v, j = pts[k]["u"], pts[k]["v"], k
            note += "; moved off a break in the drawn line to the nearest ink"
        w = local_w(j)
        b = w / 2 + (1.0 if pts[j]["flag"] in ("merged", "trimmed", "frame") else 0.0)
        if pts[j]["flag"] in ("merged", "trimmed"):
            note += "; trace over a load grid line here (bound widened 1 px)"
        if pts[j]["flag"] == "frame":
            note += "; trace merging into the bottom frame (bound widened 1 px)"
        if not has_ink(u, v):
            note += "; NO INK within 2 px"
        elif not has_own_ink(u, v) and "no ink of its own" not in note:
            note += "; no ink of its own within 2 px once the grid lines and frame are removed"
        return {"u": u, "v": v, "b": b, "note": note, "x": X.value(u, v)[0], "y": Y.value(u, v)[0], "idx": i + f}

    samples = []
    # first point
    samples.append({"u": fu, "v": fv, "b": None, "note": "first ink of the trace", "x": pts[0]["x"], "y": pts[0]["y"], "idx": 0.0})
    xs = np.array([p["x"] for p in pts]); ys = np.array([p["y"] for p in pts])
    t_end = xs[-1]
    targets = [round(0.002 * k, 3) for k in range(1, 11)] + [round(0.02 + 0.005 * k, 3) for k in range(1, 40)]
    targets = [t for t in targets if xs[0] < t < t_end]
    tsamp = []
    for t in targets:
        for i in range(len(pts) - 1):
            if (xs[i] - t) * (xs[i + 1] - t) <= 0 and xs[i] != xs[i + 1]:
                f = (t - xs[i]) / (xs[i + 1] - xs[i])
                tsamp.append(make(i, f, f"t = {t:g} s"))
                break
    # steep parts: 5 lb levels between consecutive time samples (and the end points)
    seq = [samples[0]] + tsamp + [{"idx": len(pts) - 1.0, "y": ys[-1]}]
    lsamp = []
    for a, b in zip(seq, seq[1:]):
        if abs(b["y"] - a["y"]) <= 5:
            # also look for an excursion inside the interval larger than 5 lb (a V between two samples)
            i0, i1 = int(np.floor(a["idx"])), int(np.ceil(b["idx"]))
            seg = ys[i0:i1 + 1]
            if len(seg) == 0 or (seg.max() - seg.min()) <= 5:
                continue
        i0, i1 = int(np.floor(a["idx"])), int(np.ceil(b["idx"]))
        for i in range(i0, min(i1, len(pts) - 1)):
            y0, y1 = ys[i], ys[i + 1]
            if y0 == y1:
                continue
            lo, hi = sorted((y0, y1))
            for L in range(int(np.ceil(lo / 5.0)) * 5, int(np.floor(hi / 5.0)) * 5 + 1, 5):
                if L == y0 and i > i0:
                    continue
                f = (L - y0) / (y1 - y0)
                if not (0 <= f <= 1):
                    continue
                if i + f <= a["idx"] or i + f >= b["idx"]:
                    continue
                lsamp.append(make(i, f, f"{L:+d} lb level on a steep part"))
    allp = samples + sorted(tsamp + lsamp, key=lambda s: s["idx"])
    # drop level samples within 3 px of a time sample (the same place twice)
    keep = []
    for s in allp:
        if keep and np.hypot(s["u"] - keep[-1]["u"], s["v"] - keep[-1]["v"]) < 3:
            continue
        keep.append(s)
    keep.append({"u": lu, "v": lv, "b": None, "note": "last ink of the trace", "x": xs[-1], "y": ys[-1], "idx": len(pts) - 1.0})
    w0 = local_w(1)
    w1 = local_w(len(pts) - 2)
    keep[0]["b"] = keep[0]["b"] or w0 / 2
    keep[-1]["b"] = keep[-1]["b"] or w1 / 2
    with open(out, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px",
                     "v_bound_px", "symbol", "note", "x_est", "y_est"])
        for k, s in enumerate(keep, 1):
            wr.writerow(["F5-32", pn, sid, "trace", k, round(s["u"], 1), round(s["v"], 1), round(s["b"], 1),
                         round(s["b"], 1), "", s["note"], round(s["x"], 5), round(s["y"], 2)])
    print(f"panel {pn}: {len(keep)} trace samples ({len(tsamp)} at times, {len(lsamp)} at 5 lb levels before dedup); "
          f"median trace thickness {w_med:.1f} px; t from {xs[0]:.4f} to {xs[-1]:.4f} s; y from {ys.min():.1f} to {ys.max():.1f}")
    # polyline values for the feature search
    with open(out.replace(".csv", "-polyline.csv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["i", "u", "v", "x", "y", "wp", "flag"])
        for i, p in enumerate(pts):
            wr.writerow([i, round(p["u"], 1), round(p["v"], 1), round(p["x"], 5), round(p["y"], 2),
                         "" if p["wp"] is None else round(p["wp"], 2), p["flag"]])


if __name__ == "__main__":
    main()
