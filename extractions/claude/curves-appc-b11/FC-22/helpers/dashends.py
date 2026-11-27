"""Refine the dash ends of each curve on the ink: around each approximate end (from the zoomed crops),
walk along the curve's local centerline and report the outermost column with curve ink within +-5 px of
the centerline (columns on a vertical grid line and rows on a horizontal one reported, not skipped)."""
import sys, json
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"), dtype=float)
cal = json.load(open(sys.argv[2]))
vl = [(l["x_value"], l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
hl = [(l["y_value"], l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
cl = json.load(open(sys.argv[3]))
dashes = {
 "upper": [(860, 943), (965, 1073), (1106, 1243), (1283, 1410), (1447, 1614), (1658, 1767), (1825, 1975), (2007, 2149), (2178, 2299), (2336, 2403)],
 "lower": [(851, 1001), (1043, 1186), (1217, 1401), (1447, 1613), (1653, 1748), (1798, 1928), (1985, 2137), (2180, 2308), (2352, 2402)],
 "mean": [(853, 2413)],
}
def on_v(u, v): return any(abs(u - (i0 + s * v)) <= 5 for _, i0, s in vl)
def on_h(u, v): return any(abs(v - (i0 + s * u)) <= 5 for _, i0, s in hl)
for name, ds in dashes.items():
    rows = [r for r in cl[name] if (r[3] - r[2]) < 14 and not r[4] and not r[5]]
    U = np.array([r[0] for r in rows], float); V = np.array([r[1] for r in rows], float)
    for (a, b) in ds:
        for end, sgn in ((a, -1), (b, +1)):
            m = (np.abs(U - (end - sgn * 25)) <= 25)
            if m.sum() < 8:
                print(name, end, "few columns"); continue
            p = np.polyfit(U[m], V[m], 1)
            last = None
            for u in range(end - sgn * 20, end + sgn * 15, sgn):
                vc = np.polyval(p, u)
                col = g[int(vc) - 5:int(vc) + 6, u]
                if (col < 140).sum() >= 2:
                    last = u
                elif last is not None and abs(u - last) > 2:
                    break
            vc = np.polyval(p, last)
            print(f"{name:5s} approx {end:5d} {'start' if sgn < 0 else 'end  '} outermost ink u={last} v={vc:.1f} on_vline={on_v(last, vc)} on_hline={on_h(last, vc)} slope={p[0]:.3f}")
