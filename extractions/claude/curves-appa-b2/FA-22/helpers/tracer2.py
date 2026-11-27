"""Second pass of the provisional tracer: waypoints refined from the first pass (samples whose fit
was good), a narrower search window, row runs of at least 5 px only. Output tracer2-out.json.
Every sample is still checked by eye before it is used."""
import json
import numpy as np
import fa22lib as L
import tracer as T
from waypoints import CURVES, u_at

first = json.loads((L.OUT / "helpers" / "tracer-out.json").read_text(encoding="utf-8"))
def measure(curve, vs, half_rows=9, win=13):
    up = u_at(curve, vs)
    a, b = u_at(curve, vs - 12) or up, u_at(curve, vs + 12) or up
    slope = (b - a) / 24.0
    rows, cents, widths = [], [], []
    for r in range(int(round(vs)) - half_rows, int(round(vs)) + half_rows + 1):
        uc = up + slope * (r - vs)
        rr = [x for x in T.row_runs(T.REST[r], int(uc - win), int(uc + win)) if x[1] - x[0] + 1 >= 5]
        if not rr:
            continue
        best = min(rr, key=lambda x: abs((x[0] + x[1]) / 2 - uc))
        rows.append(r); cents.append((best[0] + best[1]) / 2); widths.append(best[1] - best[0] + 1)
    if len(rows) < 4:
        return {"u": up, "v": vs, "n": len(rows), "flag": "few rows", "near": False}
    R, Cc = np.array(rows, float), np.array(cents, float)
    k, c = np.polyfit(R - vs, Cc, 1)
    res = Cc - (c + k * (R - vs))
    keep = np.abs(res) <= max(1.5, 2.5 * np.median(np.abs(res)))
    if keep.sum() >= 4:
        k, c = np.polyfit(R[keep] - vs, Cc[keep], 1)
        res = Cc[keep] - (c + k * (R[keep] - vs))
    near = any(abs(r - vs) <= 2 for r in rows)
    return {"u": float(c), "v": float(vs), "n": len(rows), "slope": float(k), "w_med": float(np.median(widths)),
            "rms": float(np.sqrt(np.mean(res ** 2))), "near": near, "flag": "" if near else "no rest ink within 2 rows"}

out = {}
for name, cur in CURVES.items():
    good = [(m["u"], m["v"]) for m in first[name] if (m.get("rms") or 9) < 2.0 and m["n"] >= 10]
    way = sorted(set(cur) | set(good), key=lambda p: p[1])
    # drop first-pass points that disagree with the hand waypoints by more than 6 px (contaminated)
    way = [p for p in way if p in cur or abs(p[0] - u_at(cur, p[1])) <= 6]
    res = []
    for m0 in first[name]:
        m = measure(way, m0["v"])
        m["e"], m["x"] = m0["e"], m0["x"]
        res.append(m)
        print(f"{name:8s} {m['e']:+.2f} v {m['v']:7.1f} u {m['u']:7.1f} (pass1 {m0['u']:7.1f}) n {m['n']:2d} w {m.get('w_med', 0):4.1f} rms {m.get('rms', 0):.2f} {m['flag']}")
    out[name] = res
(L.OUT / "helpers" / "tracer2-out.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
