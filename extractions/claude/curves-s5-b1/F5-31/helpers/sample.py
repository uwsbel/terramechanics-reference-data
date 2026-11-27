"""Trace samples and features of Figure 5-31 from rows.csv (reader helper).

Trace samples: every 0.002 s to 0.02 s and every 0.005 s after; on the steep part also every 0.2 in
where that spacing is finer than the time spacing (slope above 0.2/0.005 = 40 in/s after 0.02 s, above
0.2/0.002 = 100 in/s before). A sample sits on a row where the line's own ink is clear of every grid line
(`clean` in rows.csv); a target that falls where the line is merged with a grid line is moved to the
nearest clean row and the note says so. The center is the local straight-line fit of the clean run
centers over +-6 rows (always inside the run at that row; checked). Bound: half the line's thickness
across it, measured there (median run width over +-6 clean rows times cos of the line's angle to the row).
"""
import csv, sys
from pathlib import Path
import numpy as np
ws = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ws / "tools"))
import calibrate_axes as ca

cal, X, Y = ca.piecewise_maps(str(ws / "out" / "F5-31" / "cal-p1"))
allrows = list(csv.DictReader(open(ws / "out" / "F5-31" / "helpers" / "rows.csv")))
clean = [r for r in allrows if r["clean"] == "1"]
V = np.array([int(r["v"]) for r in clean]); C = np.array([float(r["center"]) for r in clean])
L = np.array([int(r["left"]) for r in clean]); R = np.array([int(r["right"]) for r in clean])
Wd = np.array([float(r["width"]) for r in clean])
T = np.array([X.value(u, v)[0] for u, v in zip(C, V)]); D = np.array([Y.value(u, v)[0] for u, v in zip(C, V)])
order = np.argsort(T)
assert np.all(np.diff(V[order]) < 0)   # drawing order: time increasing, v decreasing


def local(i, half=6):
    """Fitted center u at clean row i, the slope du/dv, the half thickness across the line."""
    m = np.abs(V - V[i]) <= half
    k, c = np.polyfit(V[m], C[m], 1)
    u = k * V[i] + c
    assert L[i] - 0.5 <= u <= R[i] + 0.5, (V[i], u, L[i], R[i])
    thick = float(np.median(Wd[m])) / np.sqrt(1 + k * k)
    return float(u), float(k), round(thick / 2, 1)


def nearest_clean(t_target=None, d_target=None):
    """Clean row nearest to where the center line reaches the target time (or depth)."""
    key, tgt = (T, t_target) if t_target is not None else (D, d_target)
    j = np.argsort(key)
    v_exact = float(np.interp(tgt, key[j], V[j]))       # row of the target on the clean center line
    i = int(np.argmin(np.abs(V - v_exact) + 1e-3 * (V < v_exact)))
    return i, v_exact


def why_at(v_exact):
    """The grid lines the line's ink is merged with at that row, from the geometry: the line's center there
    (interpolated along the clean rows) against each grid line's fitted position. A depth line merges when
    its center is within its half width (4.5 px) plus the line's half run (6.5 px); a time line when the row
    is within its half width (4.5 px, the bottom frame 6) plus the line's half thickness (4 px)."""
    j = np.argsort(V)
    u_c = float(np.interp(v_exact, V[j], C[j]))
    parts = []
    for l in cal["vertical_lines"]:
        if abs(u_c - (l["u_at_v0"] + l["slope_du_dv"] * v_exact)) <= 4.5 + 6.5:
            parts.append(f"merged with the depth line {l['y_value']:g}")
    for l in cal["horizontal_lines"]:
        half = 6.0 if l["x_value"] == 0.0 else 4.5
        if abs(v_exact - (l["v_at_u0"] + l["slope_dv_du"] * u_c)) <= half + 4:
            parts.append(f"crossing the time line {l['x_value']:g}")
    return "; ".join(parts) or "no grid line within reach"


samples = []   # (t, u, v, bu, bv, note)
# time targets
for t in [round(0.002 * k, 3) for k in range(1, 11)] + [round(0.02 + 0.005 * k, 3) for k in range(1, 16)]:
    i, v_exact = nearest_clean(t_target=t)
    u, k, b = local(i)
    note = f"t target {t:.3f} s"
    if abs(V[i] - v_exact) > 1.0:
        note += (f"; moved {abs(V[i] - v_exact):.0f} px along the line to the nearest row where its ink is clear "
                 f"of the grid ({why_at(v_exact)})")
    samples.append((float(T[i]), u, float(V[i]), b, b, note))
# depth targets on the steep part
for d in [round(0.2 * k, 1) for k in range(1, 22)]:
    if d > D.max():
        break
    i, v_exact = nearest_clean(d_target=d)
    m = np.abs(T - T[i]) <= 0.0015
    slope = np.polyfit(T[m], D[m], 1)[0]
    limit = 0.2 / 0.002 if T[i] <= 0.02 else 0.2 / 0.005
    if slope <= limit:
        continue
    u, k, b = local(i)
    note = f"depth target {d:.1f} in (steep part, local slope {slope:.0f} in/s)"
    if abs(V[i] - v_exact) > 1.0:
        note += (f"; moved {abs(V[i] - v_exact):.0f} px along the line to the nearest row where its ink is clear "
                 f"of the grid ({why_at(v_exact)})")
    samples.append((float(T[i]), u, float(V[i]), b, b, note))

# ends of the line's own ink (first and last clean rows) as the first and last trace samples
i0 = int(np.argmax(V)); i1 = int(np.argmin(V))
u0, k0, b0 = local(i0); u1, k1, b1 = local(i1)
samples.append((float(T[i0]), u0, float(V[i0]), b0, b0,
                "start of the line's own ink: below this row it merges with the depth 0 line and the bottom frame (t = 0)"))
samples.append((float(T[i1]), u1, float(V[i1]), b1, b1,
                "end of the line's own ink: above this row it runs into the top frame (t = 0.1)"))
samples.sort(key=lambda s: s[0])
# merge samples that fall on the same row (a time and a depth target)
ded = []
for s in samples:
    if ded and abs(ded[-1][2] - s[2]) < 0.5:
        ded[-1] = ded[-1][:5] + (ded[-1][5] + "; also " + s[5],)
        continue
    ded.append(s)
samples = ded


def frame_meet(i_rows, frame_value):
    """Where the center line, fitted over the given clean rows, meets the center of a frame line."""
    k, c = np.polyfit(V[i_rows], C[i_rows], 1)
    h = next(l for l in cal["horizontal_lines"] if l["x_value"] == frame_value)
    # v = v0 + s u ; u = k v + c  ->  v = v0 + s (k v + c)
    v = (h["v_at_u0"] + h["slope_dv_du"] * c) / (1 - h["slope_dv_du"] * k)
    return float(k * v + c), float(v)


bottom = np.where(V >= V.max() - 30)[0]
top = np.where(V <= V.min() + 40)[0]
uf, vf = frame_meet(bottom, 0.0)
ul, vl = frame_meet(top, 0.1)
features = []
features.append((0.0, uf, vf, b0, round(max(b0, abs(V[i0] - vf)), 1),
                 f"first: the line runs into the corner of the bottom frame (t = 0) and the depth 0 line; its own ink is "
                 f"distinct down to v {V[i0]}, the center line extended {abs(V[i0] - vf):.0f} px from there to the frame's "
                 f"center line; v bound widened to reach the last row of the line's own ink"))
KNEES = [((0.016, 0.027), (0.033, 0.040), "the slope drops from about 65 to 54 in/s, a kink just before the time line 0.03"),
         ((0.048, 0.055), (0.063, 0.069), "the slope drops from about 49 to 29 in/s over 0.056 to 0.062 s"),
         ((0.082, 0.086), (0.094, 0.099), "the line rounds over from about 20 in/s to the flat top over 0.086 to 0.093 s")]
for (b_, a_, what) in KNEES:
    fits = []
    for t0, t1 in (b_, a_):
        m = (T >= t0) & (T <= t1)
        fits.append(np.polyfit(V[m], C[m], 1))
    (ka, ca_), (kb, cb) = fits
    vx = (cb - ca_) / (ka - kb); ux = ka * vx + ca_
    i = int(np.argmin(np.hypot(C - ux, V - vx)))
    u, k, b = local(i)
    turn = np.degrees(np.arctan(ka) - np.arctan(kb))
    features.append((float(T[i]), u, float(V[i]), b, b,
                     f"knee: {what}; the point of the line nearest the meeting of straight fits to the stretches "
                     f"t {b_[0]}-{b_[1]} and {a_[0]}-{a_[1]} s (turn {turn:.0f} degrees on the page)"))
# peak: the flat top; deepest center rows
top_rows = np.where(T >= 0.095)[0]
dmax = D[top_rows].max()
flat = top_rows[D[top_rows] >= dmax - 0.004]
i = int(flat[np.argmin(np.abs(V[flat] - np.median(V[flat])))])
u, k, b = local(i)
features.append((float(T[i]), u, float(V[i]), b, b,
                 f"peak: the deepest part of the line is a flat top, level within 0.004 in (one pixel) from t "
                 f"{T[flat].min():.4f} s to the frame at 0.1 s; the line does not turn down before the frame, so this "
                 f"maximum is the end of the record and its time is not an observation (placed at the middle of the flat top)"))
features.append((0.1, ul, vl, b1, round(max(b1, abs(V[i1] - vl)), 1),
                 f"last: the line runs into the top frame (t = 0.1); its own ink is distinct up to v {V[i1]}, the center "
                 f"line extended {abs(V[i1] - vl):.0f} px from there to the frame's center line; v bound widened to reach "
                 f"the last row of the line's own ink"))

out = ws / "out" / "F5-31" / "points-p1.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px",
                "v_bound_px", "symbol", "note"])
    for n, (t, u, v, bu, bv, note) in enumerate(samples, 1):
        w.writerow(["F5-31", 1, "pen", "trace", n, round(u, 1), round(v, 1), bu, bv, "line", note])
    for n, (t, u, v, bu, bv, note) in enumerate(features, 1):
        w.writerow(["F5-31", 1, "pen", "feature", n, round(u, 1), round(v, 1), bu, bv, "line", note])
print(f"wrote {out}: {len(samples)} trace samples, {len(features)} features")
