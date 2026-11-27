"""Anchors for the time lines (constant x) of Figure 5-25, measured where each line is drawn.

For each time line (first located by measure_lines.py), the runs of ink along it are found between the
left frame (panel 1) and the right frame (panel 3, the 0 line of Strut No. 1). A column belongs to a run
when a short dark run (at most 5 px thick, so not a crossing vertical grid line or the trace) lies within
3 px of the line. In each run of 15 px or more, anchors are placed at both ends and about every 16 px
between, in a run of 4 to 14 px one anchor at its middle, each at the centroid of that column's dark run; the anchor list is then refitted. Writes
time_lines.json (fit and anchors per line) and prints a summary.
Short pieces (under 15 px) within 8 px of an interior load line (dots of the dotted load lines) or more than
1.5 px from the line's first fit are left out. Regions excluded: the callout boxes of the inset (u 815 to 1050, v < 2085) and the trace crossings.
"""
import json
import sys
import numpy as np
from PIL import Image

dark = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
lines = json.load(open(sys.argv[2], encoding="utf-8"))
OUT = sys.argv[3]


def column_center(u, vline):
    vi = int(round(vline))
    col = dark[vi - 8:vi + 9, u]
    # dark runs in this column window
    runs, s = [], None
    for i, f in enumerate(list(col) + [False]):
        if f and s is None:
            s = i
        if not f and s is not None:
            runs.append((s, i - 1)); s = None
    best = None
    for a, b in runs:
        c = (a + b) / 2 + vi - 8
        if b - a + 1 <= 5 and abs(c - vline) <= 3:
            if best is None or abs(c - vline) < abs(best - vline):
                best = c
    return best


res = []
for L in lines["horizontal"]:
    if L["value"] == 0:
        # the baseline (bottom frame) is drawn across the figure; keep its band measurements as anchors
        smp = sorted(L["samples"])   # build_cal.py keeps those of each panel, every third (18 px apart)
        res.append({"value": 0.0, "anchors": smp, "v_at_u0": L["v_at_u0"], "slope_dv_du": L["slope_dv_du"]})
        continue
    c0, c1 = L["v_at_u0"], L["slope_dv_du"]
    on = {}
    for u in range(738, 2272):
        vl = c0 + c1 * u
        if u >= 2277.93 - 0.00248 * vl - 4.0:     # the right frame (0 line of panel 3), 6 px thick
            continue
        if 815 <= u <= 1050 and vl < 2085:
            continue
        c = column_center(u, vl)
        if c is not None:
            on[u] = c
    us = sorted(on)
    runs, s, p = [], None, None
    for u in us + [None]:
        if s is None:
            s = p = u; continue
        if u is not None and u == p + 1:
            p = u; continue
        runs.append((s, p)); s = p = u
    anchors = []
    # interior load lines (the frames are not included: a piece reaching a frame is this line meeting it)
    VL = [(V["u_at_v0"], V["slope_du_dv"]) for V in lines["vertical"] if not (V["panel"] == 3 and V["value"] == 0)]
    for a, b in runs:
        if b - a + 1 < 4:
            continue
        uc, vc = (a + b) / 2, c0 + c1 * (a + b) / 2
        if b - a + 1 < 15 and any(abs(uc - (k0 + k1 * vc)) <= 8 for k0, k1 in VL):
            continue            # a short piece at a load line: a dot or dash of that line, not of this one
        if b - a + 1 < 15 and abs(on[int(round(uc))] - vc) > 1.5:
            continue            # a short piece off the line's first fit: stray ink
        if b - a + 1 < 15:      # a short dash: one anchor at its middle column
            u = int(round((a + b) / 2))
            anchors.append([float(u), on[u]])
            continue
        n = max(1, int(round((b - a) / 16)))
        for k in range(n + 1):
            u = int(round(a + (b - a) * k / n))
            anchors.append([float(u), on[u]])
    A = np.array(anchors)
    k1, k0 = np.polyfit(A[:, 0], A[:, 1], 1)
    r = A[:, 1] - (k0 + k1 * A[:, 0])
    res.append({"value": L["value"], "anchors": anchors, "v_at_u0": float(k0), "slope_dv_du": float(k1),
                "rms": float(np.sqrt(np.mean(r ** 2))), "runs": [rr for rr in runs if rr[1] - rr[0] + 1 >= 6]})
    print(f"t={L['value']:.2f}: {len(anchors)} anchors, runs >= 6 px {[rr for rr in runs if rr[1] - rr[0] + 1 >= 6]}, "
          f"v = {k0:.2f} + {k1:+.5f} u (before {c0:.2f} + {c1:+.5f} u), rms {np.sqrt(np.mean(r ** 2)):.2f}, max |r| {np.abs(r).max():.2f}")
json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1)
