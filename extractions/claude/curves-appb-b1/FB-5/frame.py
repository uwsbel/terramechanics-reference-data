"""Locate the four frame lines of FB-5 (p0111.png) by the centre of their ink, column by column (or
row by row), and fit each as a straight line. Corner guesses come from zoomed crops.
Usage: python frame.py <image>   (prints the fits; importable: fit_line)"""
import sys
import numpy as np
from PIL import Image


def runs(profile, offset):
    idx = np.where(profile)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append(((s + p) / 2 + offset, p - s + 1))
            s = i
        p = i
    out.append(((s + p) / 2 + offset, p - s + 1))
    return out


def fit_line(dark, a, b, horizontal, step=5, half=20, maxw=18, skip=()):
    """Line from page point a to page point b (guesses). For a horizontal line, sample columns u and
    find the dark run nearest the guessed v; for a vertical line, rows v and the run nearest u.
    Returns slope, intercept (v = c + k u, or u = c + k v), rms, n kept, n sampled, median width, samples."""
    (ua, va), (ub, vb) = a, b
    pts = []
    if horizontal:
        for u in range(int(ua), int(ub), step):
            if any(lo <= u <= hi for lo, hi in skip):
                continue
            vg = va + (vb - va) * (u - ua) / (ub - ua)
            lo = int(round(vg)) - half
            rr = [r for r in runs(dark[lo:lo + 2 * half, u], lo) if r[1] <= maxw]
            if rr:
                c, w = min(rr, key=lambda r: abs(r[0] - vg))
                pts.append((u, c, w))
    else:
        for v in range(int(va), int(vb), step):
            if any(lo <= v <= hi for lo, hi in skip):
                continue
            ug = ua + (ub - ua) * (v - va) / (vb - va)
            lo = int(round(ug)) - half
            rr = [r for r in runs(dark[v, lo:lo + 2 * half], lo) if r[1] <= maxw]
            if rr:
                c, w = min(rr, key=lambda r: abs(r[0] - ug))
                pts.append((v, c, w))
    P = np.array(pts, dtype=float)
    k, c = np.polyfit(P[:, 0], P[:, 1], 1)
    for _ in range(3):
        res = P[:, 1] - (c + k * P[:, 0])
        keep = np.abs(res) < max(1.5, 3 * np.median(np.abs(res)) * 1.4826)
        k, c = np.polyfit(P[keep, 0], P[keep, 1], 1)
    res = P[keep, 1] - (c + k * P[keep, 0])
    return dict(slope=float(k), intercept=float(c), rms=float(np.sqrt(np.mean(res ** 2))), n_kept=int(keep.sum()),
                n=len(P), width=float(np.median(P[:, 2])), samples=P[keep].tolist())


if __name__ == "__main__":
    g = np.asarray(Image.open(sys.argv[1]).convert("L"))
    dark = g < 128
    TL, TR, BR, BL = (652, 880), (2783, 852), (2834, 3966), (700, 3995)
    res = {
        "bottom": fit_line(dark, (BL[0] + 40, BL[1]), (BR[0] - 40, BR[1]), True),
        "top": fit_line(dark, (TL[0] + 40, TL[1]), (TR[0] - 40, TR[1]), True),
        "left": fit_line(dark, (TL[0], TL[1] + 40), (BL[0], BL[1] - 40), False),
        "right": fit_line(dark, (TR[0], TR[1] + 40), (BR[0], BR[1] - 40), False),
    }
    for k, r in res.items():
        print(f"{k:7s} slope {r['slope']:+.5f} intercept {r['intercept']:.2f} rms {r['rms']:.2f} kept {r['n_kept']}/{r['n']} width {r['width']}")
