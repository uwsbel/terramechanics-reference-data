"""Label and tick check for FC-3A against the fitted calibration (helper). Writes calibration-eye-checks.csv."""
import sys, json, csv, numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 160
cal = json.load(open(sys.argv[2])); ax, ay = cal["ax"], cal["ay"]
X = lambda u, v: ax[0] * u + ax[1] * v + ax[2]
Y = lambda u, v: ay[0] * u + ay[1] * v + ay[2]
def runs(a, off):
    idx = np.where(a)[0]; out = []
    if len(idx) == 0: return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1: out.append(((s + p) / 2 + off, p - s + 1)); s = i
        p = i
    out.append(((s + p) / 2 + off, p - s + 1)); return out
def bbox(u0, v0, u1, v1):
    ys, xs = np.nonzero(g[v0:v1, u0:u1]); return u0 + xs.min(), v0 + ys.min(), u0 + xs.max(), v0 + ys.max()
def vaxis(u):   # bottom axis center at column u
    c = np.where(g[3185:3225, int(round(u))])[0] + 3185
    c = c[(c > 3195) & (c < 3216)]; return (c.min() + c.max()) / 2
def uaxis(v):   # left axis center at row v
    r = np.where(g[int(round(v)), 905:930])[0] + 905; return (r.min() + r.max()) / 2
rows = []
# x ticks below the axis (rows 3215..3228), labels below (3240..3300)
xt = {1000: 1212.5, 2000: 1501.5, 3000: 1794.5, 4000: 2089.5, 5000: 2374.5}
for val, u in xt.items():
    r = [x for x, w in runs(g[3222, int(u) - 15:int(u) + 16], int(u) - 15)]
    ut = r[0]
    va = vaxis(ut)
    lb = bbox(int(ut) - 70, 3240, int(ut) + 75, 3310)
    rows.append(("x", val, "tick below axis", ut, va, (lb[0] + lb[2]) / 2, (lb[1] + lb[3]) / 2))
# x = 0: left axis meets bottom axis; printed '0' sits below-left of the corner
lb = bbox(860, 3240, 905, 3310); va = vaxis(930)
rows.append(("x", 0, "left axis line (no tick); label '0' under the corner", uaxis(3190), va, (lb[0] + lb[2]) / 2, (lb[1] + lb[3]) / 2))
yt = {1000: 2905.5, 2000: 2614.5, 3000: 2317.5, 4000: 2033.5, 5000: 1737.0, 6000: 1457.5}
for val, v in yt.items():
    r = [x for x, w in runs(g[int(v) - 15:int(v) + 16, 900], int(v) - 15)]
    vt = r[0]; ua = uaxis(vt + 12)
    lb = bbox(760, int(vt) - 25, 892, int(vt) + 26)
    rows.append(("y", val, "tick left of axis" + (" (joins top frame line)" if val == 6000 else ""), ua, vt, (lb[0] + lb[2]) / 2, (lb[1] + lb[3]) / 2))
rows.append(("y", 0, "bottom axis line (no tick); shares the '0' under the corner", uaxis(3190), vaxis(930), None, None))
span = {"x": 5000.0, "y": 6000.0}
with open(sys.argv[3], "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["axis", "printed_label", "mark", "mark_u", "mark_v", "label_center_u", "label_center_v",
                "fitted_value_at_mark", "residual_value", "residual_pct_of_span", "residual_px", "by_eye", "note"])
    for axn, val, mark, u, v, lu, lv in rows:
        fv = X(u, v) if axn == "x" else Y(u, v)
        res = fv - val
        px = res / (cal["x_per_px"] if axn == "x" else cal["y_per_px"])
        pct = 100 * abs(res) / span[axn]
        ok = "pass" if pct <= 0.5 else "FAIL (>0.5% of span)"
        note = ""
        if axn == "y" and 0 < val < 6000:
            note = "calibration (frame-interpolated, 'predicted') places %g at v=%.1f; printed tick is %.1f px %s" % (
                val, v + px, abs(px), "above" if px > 0 else "below")
        w.writerow([axn, val, mark, "%.1f" % u, "%.1f" % v, "" if lu is None else "%.1f" % lu, "" if lv is None else "%.1f" % lv,
                    "%.1f" % fv, "%+.1f" % res, "%.2f" % pct, "%+.1f" % px, ok, note])
        print(axn, val, "mark (%.1f, %.1f) label (%s, %s) fitted %.1f res %+.1f (%.2f%%, %+.1f px) %s" % (u, v, lu, lv, fv, res, pct, px, ok))
