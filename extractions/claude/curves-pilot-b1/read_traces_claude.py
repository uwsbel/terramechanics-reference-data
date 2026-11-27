"""Claude's blind reading of the drawn curves of FC-1B upper panel: column scan + tracked assignment.

Columns at x = 5, 10, ..., 245 thousandths (skipping the x gridlines at multiples of 50). In each
column the dark runs are listed; legend text (upper left, v < 1480 and u < 1470) and bare
horizontal gridlines (thin runs at a known gridline v) are removed. Series are assigned starting
from the rightmost column, where the seven curves are separated and in the known order
(3520 top ... 294 bottom), and walking left: each series takes the run nearest its predicted
position (last position plus the last step), within a window. A run thick enough to hold two
curves may be shared (both series get it with a bound of half its thickness). A series with no
run in the window gets no point at that x (gap noted).
"""
import csv, json, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, r"<repository>\tools")
from plot_grid import load_gray, runs

HERE = Path(__file__).parent
cal = json.loads((HERE / "cal-fc1b-p1" / "calibration.json").read_text())
img = load_gray(r"<repository>\corpus\1968-vol2\images\p0117.png")
ORDER = ["n3520", "n2935", "n2345", "n1760", "n1172", "n587", "n294"]
SYMBOL = {"n3520": "x", "n2935": "asterisk", "n2345": "square", "n1760": "plus", "n1172": "triangle-down",
          "n587": "triangle-up", "n294": "circle"}
V0, V1 = 1130, 2880
WINDOW = 75

vl = sorted(cal["vertical_lines"], key=lambda l: l["x_value"])
hl = cal["horizontal_lines"]


def u_of(x, v):
    xs = [l["x_value"] for l in vl]
    i = max(0, min(len(vl) - 2, int(np.searchsorted(xs, x) - 1)))
    a, b = vl[i], vl[i + 1]
    ua = a["u_at_v0"] + a["slope_du_dv"] * v
    ub = b["u_at_v0"] + b["slope_du_dv"] * v
    return ua + (x - a["x_value"]) / (b["x_value"] - a["x_value"]) * (ub - ua)


def column_runs(u):
    col = img[V0:V1, u - 1:u + 2].min(axis=1) < 200
    gv = [l["v_at_u0"] + l["slope_dv_du"] * u for l in hl]
    out = []
    for c, w in runs(np.where(col)[0]):
        v = c + V0
        if w <= 4:
            continue
        if u < 1470 and v < 1480:
            continue                                     # legend text
        on_grid = any(abs(v - g) <= 6 for g in gv)
        if w <= 9 and on_grid:
            continue                                     # a bare horizontal grid line
        out.append({"v": v, "w": w, "grid": on_grid})
    return out


xs = [x for x in range(5, 250, 5) if x % 50 != 0]
cols = {x: (int(round(u_of(x, 2000))), None) for x in xs}
for x in xs:
    u = cols[x][0]
    cols[x] = (u, column_runs(u))

rows, notes = [], []
# start at the rightmost column: expect seven runs in order
xr = xs[-1]
u, rr = cols[xr]
if len(rr) != 7:
    raise SystemExit(f"rightmost column x={xr} u={u} has {len(rr)} runs, expected 7: {rr}")
pos = {sid: [r["v"]] for sid, r in zip(ORDER, rr)}      # actual positions only
gap = {sid: 0 for sid in ORDER}                          # columns since the last actual position
for sid, r in zip(ORDER, rr):
    rows.append((xr, u, sid, r))
for x in reversed(xs[:-1]):
    u, rr = cols[x]
    taken = {}
    for sid in ORDER:
        hist = pos[sid]
        # Predict from the last actual step, damped and clamped; after a gap, hold the last
        # actual position and widen the window instead of extrapolating further.
        step = (hist[-1] - hist[-2]) if len(hist) >= 2 else 0.0
        step = max(-60.0, min(60.0, 0.7 * step))
        pred = hist[-1] + (step if gap[sid] == 0 else 0.0)
        window = WINDOW * (1 + 0.5 * gap[sid])
        cands = sorted(rr, key=lambda r: abs(r["v"] - pred))
        pick = None
        for r in cands:
            if abs(r["v"] - pred) > window:
                break
            if id(r) in taken and r["w"] < 20:
                continue                                 # already used by a neighbour and too thin to hold two curves
            pick = r
            break
        if pick is None:
            notes.append(f"x={x}: no run for {sid} near v={pred:.0f}; runs {[(r['v'], r['w']) for r in rr]}")
            gap[sid] += 1
            continue
        taken[id(pick)] = taken.get(id(pick), 0) + 1
        pos[sid].append(pick["v"])
        gap[sid] = 0
        rows.append((x, u, sid, pick))

shared = {}
for x, u, sid, r in rows:
    shared.setdefault((x, id(r)), []).append(sid)
out = []
for x, u, sid, r in sorted(rows, key=lambda t: (ORDER.index(t[2]), t[0])):
    others = [s for s in shared[(x, id(r))] if s != sid]
    note = []
    if others:
        note.append("run shared with " + ",".join(others))
    if r["grid"]:
        note.append("on horizontal gridline")
    if r["w"] >= 18 and not others:
        note.append("thick run (marker or gridline merge)")
    out.append({"figure_id": "FC-1B", "panel": 1, "series_id": sid, "point_kind": "trace", "sequence": x,
                "pixel_u": u, "pixel_v": round(r["v"], 1), "u_bound_px": 1, "v_bound_px": round(r["w"] / 2, 1),
                "symbol": SYMBOL[sid], "note": "; ".join(note)})
with (HERE / "claude-fc1b-p1-traces.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)
print(f"{len(out)} trace points over {len(xs)} columns; {len(notes)} gaps")
for n in notes:
    print("  " + n)
