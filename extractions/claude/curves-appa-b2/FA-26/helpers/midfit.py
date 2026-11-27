"""Local fits of each curve's centre v(u) from mid_obs.csv; crossings of grain-size rows; values at columns."""
import csv, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import calib
base = Path(__file__).resolve().parents[1]
obs = {}
for r in csv.DictReader((base / "helpers" / "mid_obs.csv").open(encoding="utf-8")):
    obs.setdefault(r["curve"], []).append((float(r["u"]), float(r["v"]), r["kind"]))
def vfit(curve, u, half=25):
    P = np.array([(a, b) for a, b, _ in obs[curve]])
    for hh in (half, 2 * half, 3 * half):
        m = np.abs(P[:, 0] - u) <= hh
        if m.sum() >= 4 and np.ptp(P[m, 0]) > 8:
            c = np.polyfit(P[m, 0], P[m, 1], 1)
            res = P[m, 1] - np.polyval(c, P[m, 0])
            return float(np.polyval(c, u)), float(c[0]), int(m.sum()), float(np.sqrt(np.mean(res ** 2))), hh
    return None
if __name__ == "__main__":
    for curve in ("lower", "average", "upper"):
        print(curve)
        for k in (-0.45, -0.40, -0.35, -0.30, -0.25):
            x = 10 ** k
            # find u where v_curve(u) = v of grain line at u
            us = np.arange(660, 1870, 1.0)
            best = None
            for u in us:
                f = vfit(curve, u)
                if f is None: continue
                d = f[0] - calib.v_at(u, x)
                if best is not None and np.sign(d) != np.sign(best[1]):
                    print(f"  {x:.4f} mm crosses near u {u:.0f} (v {f[0]:.1f}, slope {f[1]:.2f}, n {f[2]}, rms {f[3]:.2f})  pct {calib.val(u, f[0])[1]:.1f}")
                best = (u, d)
