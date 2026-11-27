"""Build points-p1.csv for a density chart from a reader's sample plan (JSON).

Plan: {"figure_id", "cal_dir", "bound_px", "label_bound_px", "lines": {series_id: {"uref", "a", "b",
"centres": csv from clean_centres.py, "symbol"}}, "samples": {series_id: [[where, note], ...]},
"features": {series_id: [[u, v, note, bound], ...]}}
`where` is "x=<value>" (the line's crossing with the calibration's vertical grid line of that
value) or a pixel column u. The line's centre at u is its straight-line fit plus the median
residual of its clean centres within 50 px (100 px, then the nearest 5 when too few), so the
sample sits on the ink's centre. Features "first point" / "last point" copy the first and last
trace samples. Usage: build_points.py <plan.json> <out.csv>"""
import sys
import json
import csv
import numpy as np

plan = json.load(open(sys.argv[1], encoding="utf-8"))
cal = json.load(open(plan["cal_dir"] + "/calibration.json", encoding="utf-8"))
vl = {round(l["x_value"], 6): l for l in cal["vertical_lines"]}
fid = plan["figure_id"]
B = plan["bound_px"]
rows = []


def centre_fn(L):
    R = np.loadtxt(L["centres"], delimiter=",", skiprows=1)
    def f(u):
        base = L["a"] + L["b"] * (u - L["uref"])
        for w in (50, 100):
            s = np.abs(R[:, 0] - u) <= w
            if s.sum() >= 5:
                return base + float(np.median(R[s, 3]))
        idx = np.argsort(np.abs(R[:, 0] - u))[:5]
        return base + float(np.median(R[idx, 3]))
    return f


for sid, L in plan["lines"].items():
    f = centre_fn(L)
    trace = []
    for k, (where, note) in enumerate(plan["samples"][sid], 1):
        if isinstance(where, str) and where.startswith("x="):
            ln = vl[round(float(where[2:]), 6)]
            u = ln["u_at_v0"] + ln["slope_du_dv"] * f(ln["u_at_v0"])
            for _ in range(10):
                u = ln["u_at_v0"] + ln["slope_du_dv"] * f(u)
        else:
            u = float(where)
        v = f(u)
        trace.append((u, v))
        rows.append({"figure_id": fid, "panel": 1, "series_id": sid, "point_kind": "trace", "sequence": k,
                     "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": B, "v_bound_px": B,
                     "symbol": L["symbol"], "note": note})
    feats = [(trace[0][0], trace[0][1], "first point", B), (trace[-1][0], trace[-1][1], "last point", B)]
    feats += [tuple(x) for x in plan["features"].get(sid, [])]
    for k, (u, v, note, b) in enumerate(feats, 1):
        rows.append({"figure_id": fid, "panel": 1, "series_id": sid, "point_kind": "feature", "sequence": k,
                     "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": b, "v_bound_px": b,
                     "symbol": "label" if note.startswith("label") else L["symbol"], "note": note})
with open(sys.argv[2], "w", encoding="utf-8", newline="") as fo:
    w = csv.DictWriter(fo, fieldnames=["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u",
                                       "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(f"wrote {sys.argv[2]}: {len(rows)} points")
