"""Trace samples of FC-16 at every 0.05 of Dr, from the measured ink centre lines (measured.json).
A sample whose Dr falls in a gap between dashes, or where the line is hidden under a circle and the
frame, moves to the nearest dash end / nearest clear ink (rule 7). v of a sample is a straight fit to
the measured ink centres of the same dash within +-10 px (widened to 15, 25 px when a grid line removes
columns). Bound: half the line thickness across the line."""
import json, sys, csv
import numpy as np
sys.path.insert(0, "tools")
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps("out/FC-16/cal-p1", "packet/p0152.png")
M = json.load(open("out/FC-16/measured.json"))
def u_for(dr, v):
    lo, hi = 560.0, 2700.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if X.value(mid, v)[0] < dr: lo = mid
        else: hi = mid
    return (lo + hi) / 2
def fit_at(P, u, halfs=(10, 15, 25, 40)):
    for h in halfs:
        w = np.abs(P[:, 0] - u) <= h
        if w.sum() >= 6 and P[w, 0].min() <= u + 3 and True:
            k, b = np.polyfit(P[w, 0], P[w, 1], 1)
            th = float(np.median(P[w, 2]))
            return k * u + b, k, th, h
    raise ValueError(u)
# reader's extents: start / end of each curve's visible ink, hidden stretches (line under circle + frame)
ENDS = {"upper": (653, 2530), "mean": (660, 2545), "lower": (653, 2479)}
HIDDEN = {"upper": [(2480, 2516, "under the ring of the single circle at the right frame (top) and the frame")],
          "mean": [(2483, 2515, "under the ring of the single circle at the right frame (middle) and the frame")],
          "lower": []}
# dash extents (visible ink, reader's) override the first/last measured columns where a grid line or ring hides the end
EXT = {("upper", 0): (653, 724), ("lower", 10): (2358, 2479), ("upper", 13): (2441, 2530), ("mean", 7): (2380, 2545)}
STYLE = {"upper": "dashed", "mean": "solid", "lower": "dashed"}
rows = []
targets = [round(-0.05 + 0.05 * i, 2) for i in range(0, 24)]
for name in ("upper", "mean", "lower"):
    dashes = []
    for i, d in enumerate(M[name]):
        P = np.array(d["pts"])
        a, b = EXT.get((name, i), (d["u0"], d["u1"]))
        dashes.append((a, b, P))
    if name == "mean":   # one continuous line, measured in overlapping windows: merge
        P = np.vstack([d[2] for d in dashes]); _, idx = np.unique(P[:, 0], return_index=True); P = P[idx]
        dashes = [(ENDS["mean"][0], ENDS["mean"][1], P)]
    allP = np.vstack([d[2] for d in dashes])
    seq = 0
    def add(u, note, dash):
        global seq
        v, k, th, h = fit_at(dash[2], u)
        half = round(th * np.cos(np.arctan(k)) / 2 * 2) / 2   # to 0.5 px
        rows.append(dict(series_id=name, point_kind="trace", pixel_u=round(u, 1), pixel_v=round(v, 1),
                         u_bound_px=half, v_bound_px=half, symbol=STYLE[name], note=note))
    # left end
    u0, u1 = ENDS[name]
    start_note = {"upper": "left end: ink emerges from under the left frame (Dr about -0.1); the line may start under the frame",
                  "mean": "left end: first ink clear of the frame-cut circle of pair 1 (left) at the left frame; the line runs into that ring",
                  "lower": "left end: ink emerges from under the left frame (Dr about -0.1); the line may start under the frame"}[name]
    add(u0, start_note, dashes[0])
    for dr in targets:
        u = u_for(dr, fit_at(allP, min(max(u_for(dr, 2000), u0), u1), (40, 80, 200))[0])
        u = u_for(dr, fit_at(allP, min(max(u, u0), u1), (40, 80, 200))[0])
        if u <= u0 + 2 or u >= u1 - 2: continue
        hid = [h for h in HIDDEN[name] if h[0] <= u <= h[1]]
        inside = [d for d in dashes if d[0] <= u <= d[1]]
        if inside and not hid:
            add(round(u, 1), f"Dr {dr:.2f}", inside[0]); continue
        # nearest visible ink: a dash end, or the edge of the hidden stretch
        cands = []
        for d in dashes:
            for e in (d[0], d[1]):
                cands.append((abs(e - u), e, d))
        if hid:
            a, b, why = hid[0]
            cands = [(abs(e - u), e, d) for d in dashes for e in (a - 1, b + 1) if d[0] <= e <= d[1]]
            dist, e, d = min(cands, key=lambda c: c[0])
            add(e, f"Dr {dr:.2f} moved {e - u:+.0f} px to the nearest clear ink: the line is {why}", d)
        else:
            dist, e, d = min(cands, key=lambda c: c[0])
            GAPNOTE = {("upper", 0.5): " (the gap holds the left circle of pair 2)", ("lower", 0.0): " (the gap holds the right circle of pair 1)",
                       ("lower", 0.1): " (the gap holds the Dr 0.1 grid line)", ("lower", 0.8): " (the gap holds the crossings of the 45 deg and Dr 0.8 grid lines)",
                       ("lower", 1.0): " (the gap holds the Dr 1.0 grid line)", ("lower", 0.9): "", ("upper", 1.05): ""}
            add(e, f"Dr {dr:.2f} falls in a gap between dashes{GAPNOTE.get((name, dr), '')}; moved {e - u:+.0f} px to the nearest dash end", d)
    end_note = {"upper": "right end: last ink of the last dash, beyond the right frame (the dash passes through the top single circle)",
                "mean": "right end: last ink, beyond the right frame (the line passes through the middle single circle)",
                "lower": "right end: last ink clear of the ring of the bottom single circle at the right frame, which the dash runs into 2 to 3 px further right; no ink of the curve beyond the circle"}[name]
    add(u1, end_note, dashes[-1])
# drop exact duplicates (a moved sample landing on an end)
seen = set(); out = []
for r in rows:
    key = (r["series_id"], r["pixel_u"])
    if key in seen:
        print("duplicate dropped:", r); continue
    seen.add(key); out.append(r)
json.dump(out, open("out/FC-16/traces.json", "w"), indent=0)
for r in out: print(r["series_id"], r["pixel_u"], r["pixel_v"], r["u_bound_px"], r["note"])
