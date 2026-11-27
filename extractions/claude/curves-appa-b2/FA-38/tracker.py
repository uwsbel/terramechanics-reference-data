"""Reader helper: follow strokes row by row from seed positions (rowink.json), reporting per row each track's
run (centre, edges) or its absence. usage: tracker.py v_start v_end step 'name:u:slope,...' [tol]"""
import sys, json
import numpy as np
R = json.load(open("rowink.json"))
v0, v1, st = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
tracks = []
for spec in sys.argv[4].split(","):
    n, u, s = spec.split(":"); tracks.append({"n": n, "u": float(u), "s": float(s), "v": v0, "hist": []})
tol = float(sys.argv[5]) if len(sys.argv) > 5 else 5
for v in range(v0, v1 + st, st):
    r = R[str(v)]
    line = f"v {v} {'G' if r['grid_row'] else ' '} |"
    used = set()
    for t in tracks:
        pred = t["u"] + t["s"] * (v - t["v"])
        best = None
        for i, (p, q) in enumerate(r["runs"]):
            if p - tol <= pred <= q + tol:
                ctr = (p + q) / 2
                d = abs(ctr - pred) if q - p + 1 <= 16 else 0
                if best is None or d < best[0]: best = (d, i, p, q)
        if best is None or r["grid_row"]:
            line += f" {t['n']}:{'-' if best is None else 'g'}({pred:6.1f})       |"
            continue
        _, i, p, q = best
        w = q - p + 1
        ctr = (p + q) / 2
        tag = "" if w <= 16 else "W"
        line += f" {t['n']}:{ctr:6.1f}[{p}-{q}]{tag:1s} |"
        if w <= 16 and abs(ctr - pred) <= tol:
            t["hist"].append((v, ctr))
            h = [x for x in t["hist"] if abs(x[0] - v) <= 40]
            if len(h) >= 8:
                A = np.array(h); t["s"] = float(np.polyfit(A[:, 0], A[:, 1], 1)[0])
            t["u"], t["v"] = ctr, v
    print(line)
