"""Second helper for Figure 2-29. Classifies the dark runs along a row (page row of constant v, or a
tilted row of constant penetration from the calibration) as `grid` (a narrow run at a calibrated
vertical line), `trace` (ink away from the grid) or `merged` (a run that overlaps a vertical grid
line and is wider than it: the trace runs on or beside the line, its centre is uncertain).
The legend box and the frame rows are masked. Prints the runs so the reader can decide."""
import json, sys
import numpy as np
from PIL import Image

cal = json.load(open("out/F2-29/cal-p1/calibration.json"))
g = np.asarray(Image.open("packet/p0080.png").convert("L"))
dark = g < 160
H, W = g.shape
ax, ay = cal["ax"], cal["ay"]
# legend box (printed text block, u 700..1065, v 2950..3680): not the trace
dark[2950:3680, 700:1066] = False
VL = cal["vertical_lines"]
HL = cal["horizontal_lines"]

def u_grid(v):
    return [l["u_at_v0"] + l["slope_du_dv"] * v for l in VL]

def v_grid(u):
    return [l["v_at_u0"] + l["slope_dv_du"] * u for l in HL]

def v_of_p(p, u):
    return (p - ax[0] * u - ax[2]) / ax[1]

def pen(u, v):
    return ax[0] * u + ax[1] * v + ax[2]

def load(u, v):
    return ay[0] * u + ay[1] * v + ay[2]

def runs(d):
    out, start = [], None
    for i, x in enumerate(d):
        if x and start is None: start = i
        if not x and start is not None: out.append((start, i - 1)); start = None
    if start is not None: out.append((start, len(d) - 1))
    return out

def row_runs(vs, us):
    """vs: v per u (int array). Combine v-1..v+1. Returns classified runs."""
    d = dark[vs, us] | dark[vs - 1, us] | dark[vs + 1, us]
    rr = [(us[a], us[b]) for a, b in runs(d)]
    merged = []
    for a, b in rr:
        if merged and a - merged[-1][1] <= 2: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    out = []
    vmid = int(np.median(vs))
    gl = u_grid(vmid)
    for a, b in merged:
        w = b - a + 1
        near = [x for x in gl if a - 4 <= x <= b + 4]
        if near and w <= 12:
            kind = "grid"
        elif near:
            kind = "merged"
        else:
            kind = "trace"
        if w >= 2:
            out.append((kind, a, b, (a + b) / 2, w))
    return out

def col_run(u, v):
    a = v
    while a - 1 >= 0 and dark[a - 1, u]: a -= 1
    b = v
    while b + 1 < H and dark[b + 1, u]: b += 1
    return a, b

def tilted(p, du=1):
    us = np.arange(480, 2345, du)
    vs = np.round(v_of_p(p, us)).astype(int)
    return row_runs(vs, us)

def flat(v):
    us = np.arange(480, 2345)
    vs = np.full_like(us, v)
    return row_runs(vs, us)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "p":
        ps = [float(x) for x in sys.argv[2].split(",")]
        for p in ps:
            if abs(p - round(p)) < 1e-6:
                for dv in (-13, +13):
                    us = np.arange(480, 2345)
                    vs = np.round(v_of_p(p, us)).astype(int) + dv
                    rr = row_runs(vs, us)
                    print(f"p={p:5.2f} (row {dv:+d} px): " + " | ".join(f"{k} u {a}-{b} (c {c:.1f}, w {w})" for k, a, b, c, w in rr if k != "grid"))
            else:
                rr = tilted(p)
                print(f"p={p:5.2f}: " + " | ".join(f"{k} u {a}-{b} (c {c:.1f}, w {w})" for k, a, b, c, w in rr if k != "grid"))
    elif mode == "poly":
        v0, v1, step = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        for v in range(v0, v1, step):
            vg = v_grid(1400)
            if any(abs(v - x) <= 12 for x in vg):
                continue
            rr = [r for r in flat(v) if r[0] != "grid"]
            print(f"v={v}: " + " | ".join(f"{k} u {a}-{b} (c {c:.1f}, w {w})" for k, a, b, c, w in rr))

def polyline(v0=1330, v1=3790, step=2):
    """Trace centre u per page row v (rows on the horizontal grid lines skipped). Picks the run
    nearest the previous row's centre."""
    pts, prev = [], None
    for v in range(v1, v0, -step):      # drawing order: penetration 0 up
        vg = v_grid(1400)
        if any(abs(v - x) <= 11 for x in vg):
            continue
        rr = [r for r in flat(v) if r[0] != "grid" and r[1] > 520]
        if not rr:
            continue
        if prev is None:
            r = max(rr, key=lambda r: r[3])   # start at the right (load 0)
        else:
            r = min(rr, key=lambda r: abs(r[3] - prev))
            if abs(r[3] - prev) > 60:
                continue
        prev = r[3]
        pts.append((v, r[3], r[4], r[0]))
    return pts

if __name__ == "__main__" and sys.argv[1] == "ext":
    pts = polyline()
    us = np.array([p[1] for p in pts]); vs = np.array([p[0] for p in pts])
    # local extremes of u along v with a prominence of >= 6 px over a window of +-20 rows
    win = 10
    for i in range(win, len(pts) - win):
        seg = us[i - win:i + win + 1]
        if us[i] == seg.min() and seg.max() - us[i] >= 6 and us[i] < us[i-1] and us[i] <= us[i+1]:
            print(f"local MIN u (load max) at v={vs[i]} u={us[i]:.1f} pen={pen(us[i], vs[i]):.2f} load={load(us[i], vs[i]):.0f}")
        if us[i] == seg.max() and us[i] - seg.min() >= 6 and us[i] > us[i-1] and us[i] >= us[i+1]:
            print(f"local MAX u (load min) at v={vs[i]} u={us[i]:.1f} pen={pen(us[i], vs[i]):.2f} load={load(us[i], vs[i]):.0f}")
    print(f"{len(pts)} rows; first {pts[0]}, last {pts[-1]}")
