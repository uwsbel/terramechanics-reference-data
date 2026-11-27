"""Builds out/FC-4A/points-p1.csv for Figure C-4A (blind reading, Claude).
Markers: bounding-box centers of each symbol's outline ink (component bboxes, checked on zoomed
crops). Traces: column-wise center of the drawn line's ink at the column nearest each 250 psf
sampling abscissa where the line ink is clean (full width, not merged with a symbol, label or the
frame); left end and intercept: the straight centerline of the left dashes extended to the
calibrated sigma = 0 line; right end: tip of the ink."""
import csv, json
import numpy as np
from PIL import Image

g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
D = g < 160
F = json.load(open("out/FC-4A/linefit.json"))
cal = json.load(open("out/FC-4A/cal-p1/calibration.json"))
ax, ay = cal["ax"], cal["ay"]
X = lambda u, v: ax[0] * u + ax[1] * v + ax[2]

TYP = {"dr95": 15, "dr0": 12}
HALF = 4.5   # half the perpendicular line thickness (measured 9.0 px dr95, 8.8 px dr0)
EXCL = {"dr95": [(2283, 2303)],                    # line crosses the top frame line
        "dr0": [(1126, 1168), (2015, 2053), (2272, 2310)]}   # line merges with circle outlines

def run_at(sid, u):
    a, b = F[sid]["a"], F[sid]["b"]
    vc = a + b * u
    lo = int(vc - 16)
    idx = np.where(D[lo:int(vc + 17), u])[0]
    runs = []
    for i in idx:
        if runs and i - runs[-1][-1] <= 3: runs[-1].append(i)   # bridge 1-2 px white specks inside the ink
        else: runs.append([i])
    if not runs: return None
    r = min(runs, key=lambda r: abs(np.mean(r) + lo - vc))
    return r[0] + lo, r[-1] + lo, (r[0] + r[-1]) / 2 + lo, len(r), vc

def clean(sid, u):
    if any(a <= u <= b for a, b in EXCL[sid]): return None
    r = run_at(sid, u)
    if r is None: return None
    v0, v1, c, w, vc = r
    if not (TYP[sid] - 2 <= w <= TYP[sid] + 3): return None
    if abs(c - vc) > 3.5: return None
    # neighbours must be ink too (not a dash cap)
    for du in (-3, 3):
        rr = run_at(sid, u + du)
        if rr is None or rr[3] < TYP[sid] - 3: return None
    return c

def u_for_x(sid, x):
    a, b = F[sid]["a"], F[sid]["b"]
    # solve ax0 u + ax1 (a + b u) + ax2 = x
    return (x - ax[2] - ax[1] * a) / (ax[0] + ax[1] * b)

# dashed parts (u ranges of the drawn dashes), from the ink map along each line
DASHED = {"dr95": [(918, 1112), (2180, 2390)], "dr0": [(918, 1086), (2306, 2390)]}
is_dashed = lambda sid, u: any(a <= u <= b for a, b in DASHED[sid])

rows = []
def add(sid, kind, seq, u, v, bu, bv, sym, note):
    rows.append({"figure_id": "FC-4A", "panel": 1, "series_id": sid, "point_kind": kind, "sequence": seq,
                 "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": bu, "v_bound_px": bv,
                 "symbol": sym, "note": note})

# ---- markers (sigma increasing) ----
MK = {"dr95": [(1136.5, 2766.0, 2, 2, "left tick mark at u 1120-1122 beside the square is not part of it; square sits below the start of the solid line"),
               (1421.5, 2200.5, 2, 2, "square left of the line; line has a gap beside it (u 1462-1491)"),
               (1770.5, 1871.0, 2, 2, "square on the line (center about 5 px below the line centerline), drawn in a gap of the line (u 1750-1792); top edge broken"),
               (2031.5, 1382.5, 2, 2, "square clearly above the line; bottom edge mostly unprinted, sides and corners clear"),
               (2280.5, 1353.5, 2, 2, "square clearly below the dashed upper extension of the line")],
      "dr0": [(1147.5, 3257.5, 3, 4, "circle touching the solid line from below: its top arc is hidden under the line ink; center from the left and right arcs (u 1132-1163), the bottom arc (v 3273) and the height of the other circles (33 to 35 px); bound widened"),
              (1438.0, 2915.0, 2, 2, "circle above the line; line has a gap beside it (u 1460-1470)"),
              (1780.0, 2685.0, 2, 2, "circle just below the line, beside a gap of the line (u 1750-1773)"),
              (2034.0, 2401.0, 2, 2, "circle on the line, in a line gap (u 2024-2054); a stray horizontal stroke runs right from the line at v 2389-2395, u 2054-2112"),
              (2290.0, 2159.5, 2, 2, "circle at the end of the solid part; dashed extension starts right of it")]}
for sid, sym in (("dr95", "square"), ("dr0", "circle")):
    for k, (u, v, bu, bv, note) in enumerate(MK[sid], 1):
        add(sid, "marker", k, u, v, bu, bv, sym, note)

# ---- traces ----
ENDS = {"dr95": {"left": (922.5, 3000.3, HALF, 8.0), "right": (2378.5, 1049.0, HALF, HALF)},
        "dr0": {"left": (922.8, 3451.0, HALF, 6.0), "right": (2377.6, 2091.5, HALF, HALF)}}
LEFT_NOTE = {"dr95": "left end; dashed; the first dash meets the shear-stress axis: point is the straight centerline of the left dashes at the calibrated sigma=0 line; ink at the junction spans v 2984-3001 (center 2992.5), bound widened to 8 px to cover it",
             "dr0": "left end; dashed; the first dash meets the shear-stress axis: point is the straight centerline of the left dashes at the calibrated sigma=0 line; ink at the junction (u 927) is centered about 2.8 px above that line, bound widened to 6 px"}
RIGHT_NOTE = {"dr95": "right end; dashed; tip of the last dash, above the top frame (beyond tau = 8000) at sigma about 5000; serves as the 5000 psf sample",
              "dr0": "right end; dashed; last dash runs into the right frame line (sigma = 5000) and nothing is drawn beyond it; point is the dash centerline at the frame center; serves as the 5000 psf sample"}
report = []
for sid in ("dr95", "dr0"):
    seq = 1
    u, v, bu, bv = ENDS[sid]["left"]
    add(sid, "trace", seq, u, v, bu, bv, "", LEFT_NOTE[sid])
    for x in range(250, 5000, 250):
        ut = u_for_x(sid, x)
        found = None
        for k in range(0, 40):
            for s in ((0,) if k == 0 else (1, -1)):
                uu = int(round(ut)) + s * k
                c = clean(sid, uu)
                if c is not None:
                    found = (uu, c); break
            if found: break
        uu, c = found
        shift = uu - ut
        notes = []
        if is_dashed(sid, uu): notes.append("dashed")
        if abs(shift) > 2.5:
            ui = int(round(ut))
            r0 = run_at(sid, ui)
            if any(a <= ut <= b for a, b in EXCL[sid]):
                why = "a plotted symbol outline (where the line merges with or breaks around the symbol)"
            elif r0 is None or abs(r0[2] - r0[4]) > 6:
                why = "a dash gap" if is_dashed(sid, ut) else "a gap in the line"
            else:
                why = "the rounded end of an ink segment (dash or line piece)"
            notes.append(f"sampling column {ut:.0f} for sigma {x} falls on {why}; sampled at the nearest full-width ink column")
        seq += 1
        add(sid, "trace", seq, uu, c, HALF, HALF, "", "; ".join(notes))
        report.append((sid, x, round(ut, 1), uu, c))
    u, v, bu, bv = ENDS[sid]["right"]
    seq += 1
    add(sid, "trace", seq, u, v, bu, bv, "", RIGHT_NOTE[sid])

# ---- features ----
LAB = {"dr95": (1587.5, 2037.5, "53°"), "dr0": (1802.5, 2571.0, "43°")}
for sid in ("dr95", "dr0"):
    u, v, bu, bv = ENDS[sid]["left"]
    add(sid, "feature", 1, u, v, bu, bv, "", "intercept" )
    lu, lv, txt = LAB[sid]
    add(sid, "feature", 2, lu, lv, 6, 6, "", f"label: {txt}")

with open("out/FC-4A/points-p1.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader(); w.writerows(rows)
for r in report: print(r)
print(len(rows), "rows")
