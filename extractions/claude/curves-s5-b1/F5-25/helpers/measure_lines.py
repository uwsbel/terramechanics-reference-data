"""Measure the drawn grid lines of Figure 5-25 (p0330.png) on the page ink.

Vertical lines (constant load) are measured in bands along v; horizontal lines (constant time)
in short windows along u, only where they are drawn. Each measurement is the darkness-weighted
center of a narrow dark core near the predicted position; a window with a second dark run (the
trace crossing) or a core wider than the line is skipped. Each line is fitted as a straight line
with outliers beyond max(1.5 px, 3 MAD) set aside. Prints the fits and writes lines.json.
"""
import json
import sys
import numpy as np
from PIL import Image

IMG = sys.argv[1]
OUT = sys.argv[2]
dark = np.asarray(Image.open(IMG).convert("L")) < 128


def core_center(prof, lo_idx, min_frac, max_width):
    """prof: dark fraction per pixel across the line in a window. Returns center offset index or None."""
    if prof.max() < min_frac:
        return None
    runs, inrun = [], False
    thr = max(min_frac * 0.5, 0.5 * prof.max())
    for i, f in enumerate(prof):
        if f >= thr and not inrun:
            s, inrun = i, True
        elif f < thr and inrun:
            runs.append((s, i - 1)); inrun = False
    if inrun:
        runs.append((s, len(prof) - 1))
    # any other ink run of comparable strength in the window: a crossing curve; skip
    if len(runs) != 1:
        return None
    s, e = runs[0]
    if e - s + 1 > max_width:
        return None
    w = prof[s:e + 1]
    return float(np.sum((np.arange(s, e + 1)) * w) / np.sum(w)) + lo_idx


def fit(ts, ps):
    T, P = np.array(ts, float), np.array(ps, float)
    keep = np.ones(len(T), bool)
    for _ in range(5):
        c1, c0 = np.polyfit(T[keep], P[keep], 1) if keep.sum() >= 2 and np.ptp(T[keep]) > 0 else (0.0, float(np.mean(P[keep])))
        res = P - (c0 + c1 * T)
        mad = 1.4826 * np.median(np.abs(res[keep] - np.median(res[keep])))
        new = np.abs(res) <= max(1.5, 3 * mad)
        if (new == keep).all():
            break
        keep = new
    rms = float(np.sqrt(np.mean(res[keep] ** 2)))
    return float(c0), float(c1), keep, rms


def vline(u_guess, v0, v1, band, half=9, min_frac=0.1, max_width=10, slope=0.0, vref=2700):
    ts, ps = [], []
    for v in range(v0, v1 - band + 1, band // 2):
        uc = u_guess + slope * (v + band / 2 - vref)
        lo = int(round(uc)) - half
        win = dark[v:v + band, lo:lo + 2 * half + 1]
        prof = win.mean(axis=0)
        c = core_center(prof, lo, min_frac, max_width)
        if c is not None:
            # the center of the ink rows actually present (dotted lines): v center of dark rows in the core
            ts.append(v + band / 2); ps.append(c)
    return ts, ps


def hline(v_guess, ranges, win_w=12, half=9, min_frac=0.5, max_width=10, slope=0.0, uref=1500):
    ts, ps = [], []
    for (a, b) in ranges:
        for u in range(a, b - win_w + 1, win_w // 2):
            vc = v_guess + slope * (u + win_w / 2 - uref)
            lo = int(round(vc)) - half
            win = dark[lo:lo + 2 * half + 1, u:u + win_w]
            prof = win.mean(axis=1)
            c = core_center(prof, lo, min_frac, max_width)
            if c is not None:
                ts.append(u + win_w / 2); ps.append(c)
    return ts, ps


if __name__ == "__main__":
    spec = json.loads(open(sys.argv[3], encoding="utf-8").read())
    out = {"vertical": [], "horizontal": []}
    for L in spec["vertical"]:
        ts, ps = vline(L["u"], L["v0"], L["v1"], L.get("band", 40), min_frac=L.get("min_frac", 0.1),
                       max_width=L.get("max_width", 10), slope=spec.get("vslope", 0.0))
        c0, c1, keep, rms = fit(ts, ps)
        out["vertical"].append({**L, "u_at_v0": c0, "slope_du_dv": c1, "n": int(keep.sum()), "n_all": len(ts),
                                "rms": rms, "samples": [[p, t] for t, p, k in zip(ts, ps, keep) if k],
                                "set_aside": [[p, t] for t, p, k in zip(ts, ps, keep) if not k]})
        print(f"V {L['panel']} {L['value']:>6g}: u = {c0:8.2f} + {c1:+.5f} v   n={keep.sum()}/{len(ts)} rms={rms:.2f}  u@2700={c0 + c1 * 2700:.1f}  v range {min(ts) if ts else 0:.0f}-{max(ts) if ts else 0:.0f}")
    for L in spec["horizontal"]:
        ts, ps = hline(L["v"], L["ranges"], min_frac=L.get("min_frac", 0.5), max_width=L.get("max_width", 10),
                       slope=spec.get("hslope", 0.0))
        c0, c1, keep, rms = fit(ts, ps)
        out["horizontal"].append({**L, "v_at_u0": c0, "slope_dv_du": c1, "n": int(keep.sum()), "n_all": len(ts),
                                  "rms": rms, "samples": [[t, p] for t, p, k in zip(ts, ps, keep) if k],
                                  "set_aside": [[t, p] for t, p, k in zip(ts, ps, keep) if not k]})
        us = [t for t, k in zip(ts, keep) if k]
        print(f"H {L['value']:>6g}: v = {c0:8.2f} + {c1:+.5f} u   n={keep.sum()}/{len(ts)} rms={rms:.2f}  v@800={c0 + c1 * 800:.1f} v@2240={c0 + c1 * 2240:.1f}  u in {min(us) if us else 0:.0f}..{max(us) if us else 0:.0f}")
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
