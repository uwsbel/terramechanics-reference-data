"""Trace samples of Fig. 4-20 from the dense centre lines (helpers/dense.csv).

Targets, in drawing order: every crossing of x = 0.1 k in (displacement) and, where the trace is steep
(|dF/dx| > 500 lb/in, i.e. 0.1 in holds more than 50 lb), every crossing of F = 50 m lb. Targets are
located with the affine map on the dense centre line (targeting only).

A sample is placed on the ink:
  solid   the nearest `ok` dense point within 4 px of arc length of the target
  dotted  the middle of the dot (contiguous `ok` stretch) nearest the target, within 22 px
  dashed  the nearest `ok` point at least 3 px inside a dash, within 30 px
Bounds (pixels): hw = half the run width measured across the line at the sample. Solid: hw in u and
v. Dotted and dashed: the bound along the line is widened to half the larger adjacent gap, and the
u and v bounds are those of the rectangle (hw across, gap/2 along) projected on u and v, never less
than hw. Targets that fall where the trace's ink runs into another trace, a grid line or the frame
(status `wide`), or with no ink near, are listed in unresolved.csv for a reading by hand.

usage: sample.py <guides.json> <dense.csv> <calibration.json> <out_auto.csv> <unresolved.csv>
"""
import csv
import json
import math
import sys
from collections import defaultdict

import numpy as np

STEEP = 500.0   # lb per in
MAXD = {"solid": 4, "dotted": 22, "dashed": 30}


WMIN = 6.0     # a narrower run is a sliver (a dash end cut by a grid line, a grid remnant), not a centre


def good(p):
    return p["status"] == "ok" and p["width"] is not None and p["width"] >= WMIN


def stretches(pts):
    """Contiguous good stretches along the dense points: list of (i0, i1) inclusive."""
    out, i = [], 0
    while i < len(pts):
        if good(pts[i]):
            j = i
            while j + 1 < len(pts) and good(pts[j + 1]) and pts[j + 1]["arc"] - pts[j]["arc"] < 1.5:
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return [s for s in out if s[1] - s[0] >= 4]


def main():
    guides = json.load(open(sys.argv[1], encoding="utf-8"))
    dense = list(csv.DictReader(open(sys.argv[2], encoding="utf-8")))
    for r in dense:
        for k in ("arc", "gu", "gv", "cu", "cv", "tu", "tv", "x_aff", "y_aff"):
            r[k] = float(r[k])
        r["width"] = float(r["width"]) if r["width"] else None
    by = defaultdict(list)
    for r in dense:
        by[(r["series_id"], int(r["segment"]))].append(r)
    others = {sid: np.array([[r["cu"], r["cv"]] for r in dense if r["series_id"] == sid and good(r)]) for sid in {r["series_id"] for r in dense}}
    auto, unres = [], []
    for sid, spec in guides.items():
        if sid.startswith("_"):
            continue
        style = spec["style"]
        for k in range(1, len(spec["segments"]) + 1):
            pts = by[(sid, k)]
            A = np.array([p["arc"] for p in pts])
            # targeting on a smoothed centre line (good centres, the guide elsewhere), so the jitter of
            # the centres on a line nearly parallel to a level does not make several crossings
            cal = json.load(open(sys.argv[3], encoding="utf-8"))
            ax, ay = cal["ax"], cal["ay"]
            CU = np.array([p["cu"] if good(p) else p["gu"] for p in pts])
            CV = np.array([p["cv"] if good(p) else p["gv"] for p in pts])
            ker = np.ones(21) / 21
            pad = lambda z: np.concatenate([np.full(10, z[0]), z, np.full(10, z[-1])])
            SU, SV = np.convolve(pad(CU), ker, "valid"), np.convolve(pad(CV), ker, "valid")
            X = ax[0] * SU + ax[1] * SV + ax[2]
            Y = ay[0] * SU + ay[1] * SV + ay[2]
            # smooth the values a little for targeting (merged and gap points use the guide)
            targets = []
            for i in range(len(pts) - 1):
                for name, Z, step in (("x", X, 0.1), ("y", Y, 50.0)):
                    a, b = Z[i] / step, Z[i + 1] / step
                    if math.floor(a) != math.floor(b):
                        m = max(math.floor(a), math.floor(b))
                        f = (m - a) / (b - a)
                        s = A[i] + f * (A[i + 1] - A[i])
                        lo, hi = max(0, i - 8), min(len(pts) - 1, i + 9)
                        dx, dy = X[hi] - X[lo], Y[hi] - Y[lo]
                        steep = abs(dx) < 1e-9 or abs(dy / dx) > STEEP
                        if name == "x" or steep:
                            targets.append((s, name, round(m * step, 3), steep))
            targets.sort()
            kept = []
            for t in targets:   # hysteresis: one crossing of a level within 40 px of arc
                if any(t[1] == q[1] and t[2] == q[2] and abs(t[0] - q[0]) < 40 for q in kept):
                    continue
                kept.append(t)
            targets = kept
            st = stretches(pts)
            used = {}
            for s, name, val, steep in targets:
                label = f"x = {val:g} in" if name == "x" else f"F = {val:g} lb"
                j = int(np.argmin(np.abs(A - s)))
                if style == "solid":
                    cand = [i for i in range(len(pts)) if good(pts[i]) and abs(A[i] - s) <= MAXD[style]]
                    if not cand:
                        unres.append({"series_id": sid, "segment": k, "target": label, "arc": round(s, 1),
                                      "gu": pts[j]["gu"], "gv": pts[j]["gv"], "status_here": pts[j]["status"]})
                        continue
                    i = min(cand, key=lambda i: abs(A[i] - s))
                    gap_along = 0.0
                    shift = A[i] - s
                else:
                    best = None
                    for (i0, i1) in st:
                        if style == "dotted":
                            d = 0 if A[i0] <= s <= A[i1] else min(abs(A[i0] - s), abs(A[i1] - s))
                            ic = (i0 + i1) // 2
                        else:
                            lo_i, hi_i = i0 + 3, i1 - 3
                            if hi_i < lo_i:
                                continue
                            ic = min(range(lo_i, hi_i + 1), key=lambda q: abs(A[q] - s))
                            d = abs(A[ic] - s)
                        if d <= MAXD[style] and (best is None or d < best[0]):
                            best = (d, ic, i0, i1)
                    if best is None:
                        unres.append({"series_id": sid, "segment": k, "target": label, "arc": round(s, 1),
                                      "gu": pts[j]["gu"], "gv": pts[j]["gv"], "status_here": pts[j]["status"]})
                        continue
                    _, i, i0, i1 = best
                    # the white gap on either side: the first run of points with no ink at all, past any
                    # ink that is not a clean centre (a grid line crossing, a sliver); a grid crossing is not a gap
                    gaps = []
                    for direction, start in ((-1, i0 - 1), (1, i1 + 1)):
                        q = start
                        while 0 <= q < len(pts) and pts[q]["status"] != "none":
                            q += direction
                        n0 = 0
                        while 0 <= q < len(pts) and pts[q]["status"] == "none":
                            n0 += 1
                            q += direction
                        if 0 <= q < len(pts) and n0:
                            gaps.append(n0 + 1.0)
                    gap_along = max(gaps) if gaps else 0.0
                    shift = A[i] - s
                p = pts[i]
                if i in used:
                    used[i]["note"] += f"; also the sample for {label}"
                    continue
                hw = (p["width"] or 0) / 2
                tu, tv = p["tu"], p["tv"]
                nu, nv = -tv, tu
                if style == "solid":
                    bu = bv = hw
                else:
                    along = gap_along / 2
                    bu = max(hw, hw * abs(nu) + along * abs(tu))
                    bv = max(hw, hw * abs(nv) + along * abs(tv))
                note = f"sample for {label}"
                if style == "dotted":
                    note += f"; dot centre {abs(shift):.0f} px along the line from the target"
                elif style == "dashed" and abs(shift) > 1.5:
                    note += f"; on the nearest dash, {abs(shift):.0f} px along the line from the target"
                if style != "solid":
                    note += f"; bound widened along the line to half the gap ({gap_along:.0f} px)"
                # another trace close by
                near = []
                for osid, O in others.items():
                    if osid == sid:
                        continue
                    dmin = float(np.min(np.hypot(O[:, 0] - p["cu"], O[:, 1] - p["cv"])))
                    if dmin < 14:
                        near.append(f"{osid} ({dmin:.0f} px between centres)")
                if near:
                    note += "; another trace close by: " + ", ".join(near)
                row = {"series_id": sid, "segment": k, "arc": round(A[i], 1), "pixel_u": round(p["cu"], 1),
                       "pixel_v": round(p["cv"], 1), "u_bound_px": round(bu, 1), "v_bound_px": round(bv, 1),
                       "width_px": p["width"], "target": label, "note": note}
                used[i] = row
                auto.append(row)
    flds = ["series_id", "segment", "arc", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "width_px", "target", "note"]
    with open(sys.argv[4], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=flds, lineterminator="\n")
        w.writeheader()
        w.writerows(auto)
    with open(sys.argv[5], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["series_id", "segment", "target", "arc", "gu", "gv", "status_here"], lineterminator="\n")
        w.writeheader()
        w.writerows(unres)
    from collections import Counter
    print("auto:", dict(Counter(r["series_id"] for r in auto)), "unresolved:", dict(Counter(r["series_id"] for r in unres)))


if __name__ == "__main__":
    main()
