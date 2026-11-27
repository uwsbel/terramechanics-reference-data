"""Locate the straight plotted lines of a density chart on the page (pixel space only, no calibration).
1. Grid removal: pixels in horizontal runs >= HRUN or vertical runs >= VRUN are grid (dilated by 1 px).
2. Hough search over v = a + b (u - uref): counts grid-free ink within +-2.5 px of each candidate.
3. Each of the n strongest, well-separated peaks is refined by least squares on the grid-free ink
   within +-5 px (two passes, the second within +-4 px of the first fit).
4. Coverage along each fitted line on the ORIGINAL page: for every column u in [ua, ub], whether
   there is ink within +-1 px of the line's centre; white runs are listed (dash gaps, or the white
   between a line's end and the frame).
Usage: lines_fit.py <image> u0 v0 u1 v1 uref a_lo a_hi b_lo b_hi nlines [ua ub]"""
import sys
import json
import numpy as np
from PIL import Image

img = sys.argv[1]
u0, v0, u1, v1 = map(int, sys.argv[2:6])
uref = float(sys.argv[6])
a_lo, a_hi, b_lo, b_hi = map(float, sys.argv[7:11])
nl = int(sys.argv[11])
ua, ub = (float(sys.argv[12]), float(sys.argv[13])) if len(sys.argv) > 13 else (u0, u1)
HRUN, VRUN = 45, 30
G = np.asarray(Image.open(img).convert("L")) < 128
g = G[v0:v1, u0:u1]


def long_runs(mask, L):
    out = np.zeros_like(mask)
    for i in range(mask.shape[0]):
        d = np.diff(np.concatenate([[0], mask[i].astype(int), [0]]))
        for s, e in zip(np.where(d == 1)[0], np.where(d == -1)[0]):
            if e - s >= L:
                out[i, s:e] = True
    return out


grid = long_runs(g, HRUN) | long_runs(g.T, VRUN).T
gm = grid.copy()
gm[1:, :] |= grid[:-1, :]; gm[:-1, :] |= grid[1:, :]; gm[:, 1:] |= grid[:, :-1]; gm[:, :-1] |= grid[:, 1:]
ink = g & ~gm
vv, uu = np.nonzero(ink)
vv = vv + v0; uu = uu + u0
du = uu - uref

As = np.arange(a_lo, a_hi + 0.01, 0.5)
Bs = np.arange(b_lo, b_hi + 1e-6, 0.0005)
acc = np.zeros((len(Bs), len(As)))
for j, b in enumerate(Bs):
    r = vv - b * du                      # intercept of each pixel for this slope
    h, _ = np.histogram(r, bins=np.append(As - 0.25, As[-1] + 0.25))
    # +-2.5 px window: sum 11 bins of 0.5 px
    acc[j] = np.convolve(h, np.ones(11), mode="same")
peaks = []
A2 = acc.copy()
for _ in range(nl):
    j, i = np.unravel_index(np.argmax(A2), A2.shape)
    peaks.append((As[i], Bs[j], A2[j, i]))
    # suppress lines within 6 px anywhere over the u-range
    for jj, b in enumerate(Bs):
        for ii, a in enumerate(As):
            d1 = abs((a - As[i]) + (b - Bs[j]) * (ua - uref))
            d2 = abs((a - As[i]) + (b - Bs[j]) * (ub - uref))
            if min(d1, d2) < 6 and max(d1, d2) < 25:
                A2[jj, ii] = 0
res = []
for a, b, score in sorted(peaks, key=lambda p: p[0]):
    for win in (5, 4):
        sel = np.abs(vv - (a + b * du)) <= win
        b, a = np.polyfit(du[sel], vv[sel], 1)
    sel = np.abs(vv - (a + b * du)) <= 4
    rms = float(np.sqrt(np.mean((vv[sel] - (a + b * du[sel])) ** 2)))
    # coverage on the original page
    cols = np.arange(int(np.ceil(ua)), int(np.floor(ub)) + 1)
    cov = []
    for u in cols:
        c = a + b * (u - uref)
        lo, hi = int(np.floor(c - 1)), int(np.ceil(c + 1))
        cov.append(G[lo:hi + 1, u].any())
    cov = np.array(cov)
    d = np.diff(np.concatenate([[1], cov.astype(int), [1]]))
    gaps = [(int(cols[s]), int(cols[e - 1])) for s, e in zip(np.where(d == -1)[0], np.where(d == 1)[0])]
    res.append({"a_at_uref": round(float(a), 2), "slope": round(float(b), 5), "score": int(score),
                "n_pix": int(sel.sum()), "rms_px": round(rms, 2),
                "v_at_ua": round(float(a + b * (ua - uref)), 1), "v_at_ub": round(float(a + b * (ub - uref)), 1),
                "white_runs": [g_ for g_ in gaps if g_[1] - g_[0] >= 2]})
for r in res:
    print(json.dumps(r))
