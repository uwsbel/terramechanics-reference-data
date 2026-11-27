"""The two drawn polylines of FB-6, measured on the ink.

For each group: every row v between the rough ends, the dark run nearest the rough polyline (within
12 px) gives the line's centre u at that row; rows within 23 px of a plotted circle's centre (the
ring's outer radius is about 20.6 px) are set aside, since there the ring and the line cannot be told
apart. Two straight lines are fitted (u = a + b v), the break row chosen by least squares; the vertex
is their intersection. Ends: the outermost rows where the line's own ink is found (a free end), or
where the line meets a circle's ring (the end is then taken on the fitted centre line at the ring's
outer radius from the circle's centre). Trace samples at every 1 psi between ends and vertex are
placed on the fitted segment where the piecewise map gives that x, then moved onto the ink: u is the
centre of the dark run in that row. Prints everything; writes nothing."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

W = Path(sys.argv[1])
sys.path.insert(0, str(W / "tools"))
import calibrate_axes as ca  # noqa: E402

img = W / "packet" / "p0112.png"
g = np.asarray(Image.open(img).convert("L"))
dark = g < 128
cal, X, Y = ca.piecewise_maps(str(W / "out" / "FB-6" / "cal-p1"), str(img))

M = json.loads((W / "out" / "FB-6" / "helpers" / "markers.json").read_text(encoding="utf-8"))
centres = [(m["u"], m["v"]) for m in M]
R_OUT = 20.6

ROUGH = {
    "dr82": [(999, 3448), (1322, 2411), (1977, 1117)],
    "dr02": [(994, 3979), (1344, 3425), (1943, 2698)],
}


def runs(row):
    idx = np.where(row)[0]
    return np.split(idx, np.where(np.diff(idx) != 1)[0] + 1) if len(idx) else []


def rough_u(poly, v):
    for (u0, v0), (u1, v1) in zip(poly, poly[1:]):
        if min(v0, v1) <= v <= max(v0, v1):
            return u0 + (u1 - u0) * (v - v0) / (v1 - v0)
    return None


def ink_at_row(v, u_pred, half=12, maxw=16):
    lo = int(round(u_pred - half))
    rs = [r for r in runs(dark[int(v), lo:lo + 2 * half + 1]) if len(r) <= maxw]
    if not rs:
        return None
    r = min(rs, key=lambda r: abs(lo + (r[0] + r[-1]) / 2 - u_pred))
    return lo + (r[0] + r[-1]) / 2, len(r)


def near_marker(u, v, rad=23.0):
    return min(math.hypot(u - a, v - b) for a, b in centres) < rad


def xy(u, v):
    return X.value(u, v)[0], Y.value(u, v)[0]


out = {}
for sid, poly in ROUGH.items():
    v_top, v_bot = min(p[1] for p in poly), max(p[1] for p in poly)
    S = []
    for v in range(int(v_top) - 12, int(v_bot) + 13):
        up = rough_u(poly, min(max(v, v_top), v_bot))
        if up is None:
            continue
        # extend the rough line beyond its ends to see where the ink stops
        if v < v_top:
            (u0, v0), (u1, v1) = poly[-1], poly[-2]
            up = u0 + (u1 - u0) * (v - v0) / (v1 - v0)
        if v > v_bot:
            (u0, v0), (u1, v1) = poly[0], poly[1]
            up = u0 + (u1 - u0) * (v - v0) / (v1 - v0)
        r = ink_at_row(v, up)
        if r is None:
            continue
        S.append((v, r[0], r[1], near_marker(r[0], v)))
    S = np.array(S, dtype=float)
    free = S[S[:, 3] == 0]
    # breakpoint search on the free rows
    best = None
    for vb in range(int(poly[1][1]) - 60, int(poly[1][1]) + 61):
        lo_, hi_ = free[free[:, 0] >= vb], free[free[:, 0] < vb]      # lower segment: larger v
        if len(lo_) < 20 or len(hi_) < 20:
            continue
        p1, p2 = np.polyfit(lo_[:, 0], lo_[:, 1], 1), np.polyfit(hi_[:, 0], hi_[:, 1], 1)
        sse = np.sum((lo_[:, 1] - np.polyval(p1, lo_[:, 0])) ** 2) + np.sum((hi_[:, 1] - np.polyval(p2, hi_[:, 0])) ** 2)
        if best is None or sse < best[0]:
            best = (sse, vb, p1, p2)
    _, vb, p1, p2 = best
    # robust refit (drop rows more than 2 px off, e.g. specks touching the line)
    segs = []
    for p, sel in ((p1, free[:, 0] >= vb), (p2, free[:, 0] < vb)):
        pts = free[sel]
        for _ in range(3):
            res = pts[:, 1] - np.polyval(p, pts[:, 0])
            keep = np.abs(res) <= 2.0
            p = np.polyfit(pts[keep, 0], pts[keep, 1], 1)
        res = pts[keep, 1] - np.polyval(p, pts[keep, 0])
        slope = p[0]
        thick = float(np.median(pts[keep, 2])) / math.sqrt(1 + slope ** 2)
        segs.append({"p": p, "rms": float(np.sqrt(np.mean(res ** 2))), "max": float(np.abs(res).max()),
                     "n": int(keep.sum()), "of": len(pts), "w_row": float(np.median(pts[keep, 2])), "thick": thick,
                     "v_range": [float(pts[:, 0].min()), float(pts[:, 0].max())]})
    (b1, a1), (b2, a2) = segs[0]["p"], segs[1]["p"]
    vv = (a2 - a1) / (b1 - b2)
    uv = a1 + b1 * vv
    print(f"== {sid}: break row {vb}; vertex ({uv:.1f}, {vv:.1f}) -> x {xy(uv, vv)[0]:.3f}, y {xy(uv, vv)[1]:.3f}; ink at vertex row: {ink_at_row(round(vv), uv)}")
    for nm, s in zip(("lower", "upper"), segs):
        print(f"   {nm}: u = {s['p'][1]:.2f} {s['p'][0]:+.5f} v; rows {s['n']}/{s['of']} rms {s['rms']:.2f} max {s['max']:.2f}; "
              f"row width {s['w_row']:.1f} -> thickness {s['thick']:.1f} px; v {s['v_range']}")
    # ends: outermost rows with line ink (contiguous from the fitted line)
    allrows = {int(r[0]): r for r in S}
    v_end_lo = max(v for v in allrows if abs(allrows[v][1] - np.polyval(segs[0]["p"], v)) <= 3)
    v_end_hi = min(v for v in allrows if abs(allrows[v][1] - np.polyval(segs[1]["p"], v)) <= 3)
    print(f"   lowest line-ink row {v_end_lo} (u {allrows[v_end_lo][1]:.1f}, near marker {bool(allrows[v_end_lo][3])}); "
          f"highest line-ink row {v_end_hi} (u {allrows[v_end_hi][1]:.1f}, near marker {bool(allrows[v_end_hi][3])})")
    # gaps along the line: rows between the ends with no ink at the fitted line
    gaps = []
    for v in range(v_end_hi, v_end_lo + 1):
        p = segs[0]["p"] if v >= vv else segs[1]["p"]
        r = ink_at_row(v, np.polyval(p, v), half=5)
        if r is None:
            gaps.append(v)
    if gaps:
        gr = np.split(np.array(gaps), np.where(np.diff(gaps) != 1)[0] + 1)
        print("   rows with no ink on the line:", [(int(x[0]), int(x[-1])) for x in gr])
    out[sid] = {"segs": [{"a": float(s["p"][1]), "b": float(s["p"][0]), "thick": s["thick"]} for s in segs],
                "vertex": [float(uv), float(vv)], "v_end_lo": v_end_lo, "v_end_hi": v_end_hi}

(W / "out" / "FB-6" / "helpers" / "lines.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
