"""Sample a straight plotted line of a density chart on its ink (pixel space).

Inputs: the page, the calibration directory (only its vertical grid lines are used, to place the
samples at Dr = 0.1 ... 0.9 where the line crosses them), and a coarse line v = a + b (u - uref).

1. Grid mask: pixels in horizontal runs >= 45 px or vertical runs >= 30 px (the grid; a plotted
   line at slope 0.3 makes runs of about 23 px), dilated by 1 px.
2. Local centre c(u): least-squares line through the grid-free ink within +-4 px of the coarse
   line, over columns u +- 20 (widened to 40, 60 when there is too little ink); evaluated at u.
3. State of every column along the line, from the rows of the line's core (c(u) +- h, h = half
   the measured vertical thickness minus 1): 'occ' when every core row is in the grid mask,
   else 'ink' when a visible core row is dark, else 'white'.
4. Dashes: maximal runs not interrupted by a white run of 3 px or more; each dash end is the
   outermost 'ink' column, and the end is 'hidden' when an 'occ' run touches it on the gap side.
Prints JSON: thickness, dashes, and for each grid line x = k/10 the crossing (u*, v*) and the
state of the columns on either side of the grid line.
Usage: trace.py <image> <cal_dir> uref a b ua ub [name]"""
import sys
import json
import numpy as np
from PIL import Image

img, cal_dir = sys.argv[1], sys.argv[2]
uref, a0, b0, ua, ub = map(float, sys.argv[3:8])
G = np.asarray(Image.open(img).convert("L")) < 128
H, W = G.shape
cal = json.loads(open(cal_dir + "/calibration.json", encoding="utf-8").read())

# grid mask on a window around the line
vlo = int(min(a0 + b0 * (ua - uref), a0 + b0 * (ub - uref))) - 80
vhi = int(max(a0 + b0 * (ua - uref), a0 + b0 * (ub - uref))) + 80
ulo, uhi = int(ua) - 60, int(ub) + 60
sub = G[vlo:vhi, ulo:uhi]


def long_runs(mask, L):
    out = np.zeros_like(mask)
    for i in range(mask.shape[0]):
        d = np.diff(np.concatenate([[0], mask[i].astype(int), [0]]))
        for s, e in zip(np.where(d == 1)[0], np.where(d == -1)[0]):
            if e - s >= L:
                out[i, s:e] = True
    return out


gr = long_runs(sub, 45) | long_runs(sub.T, 30).T
gm = gr.copy()
gm[1:, :] |= gr[:-1, :]; gm[:-1, :] |= gr[1:, :]; gm[:, 1:] |= gr[:, :-1]; gm[:, :-1] |= gr[:, 1:]
GM = np.zeros_like(G); GM[vlo:vhi, ulo:uhi] = gm
ink = G & ~GM
vv, uu = np.nonzero(ink[vlo:vhi, ulo:uhi]); vv = vv + vlo; uu = uu + ulo
near = np.abs(vv - (a0 + b0 * (uu - uref))) <= 4
vv, uu = vv[near], uu[near]


def centre(u):
    for w in (40, 60, 80):
        s = np.abs(uu - u) <= w
        if s.sum() >= 60 and np.ptp(uu[s]) >= w:
            b, a = np.polyfit(uu[s] - u, vv[s], 1)
            return float(a), float(b), w
    return float(a0 + b0 * (u - uref)), b0, None


# vertical thickness: ink runs through the centre in columns whose core is clear of the grid
th = []
for u in range(int(ua) + 5, int(ub) - 5, 3):
    c, _, _ = centre(u)
    ci = int(round(c))
    if not G[ci, u] or GM[ci - 6:ci + 7, u].any():
        continue
    lo = ci
    while G[lo - 1, u]:
        lo -= 1
    hi = ci
    while G[hi + 1, u]:
        hi += 1
    if hi - lo + 1 <= 14:
        th.append(hi - lo + 1)
thick = float(np.median(th)) if th else 7.0
h = max(1, int(thick / 2) - 1)

cols = np.arange(int(ua), int(ub) + 1)
cs = np.array([centre(u)[0] for u in cols])
state = []
for u, c in zip(cols, cs):
    rows = range(int(round(c)) - h, int(round(c)) + h + 1)
    vis = [r for r in rows if not GM[r, u]]
    if not vis:
        state.append("occ")
    elif any(G[r, u] for r in vis):
        state.append("ink")
    else:
        state.append("white")
state = np.array(state)
# dashes
gaps = []
i = 0
while i < len(cols):
    if state[i] == "white":
        j = i
        while j + 1 < len(cols) and state[j + 1] == "white":
            j += 1
        if j - i + 1 >= 3:
            gaps.append((i, j))
        i = j + 1
    else:
        i += 1
dashes = []
starts = [0] + [g[1] + 1 for g in gaps]
ends = [g[0] - 1 for g in gaps] + [len(cols) - 1]
for s, e in zip(starts, ends):
    if s > e:
        continue
    inks = [k for k in range(s, e + 1) if state[k] == "ink"]
    if not inks:
        continue
    s_ink, e_ink = inks[0], inks[-1]
    hid_s = s_ink > s or (s_ink > 0 and state[s_ink - 1] == "occ")
    hid_e = e_ink < e or (e_ink < len(cols) - 1 and state[e_ink + 1] == "occ")
    dashes.append({"u_start": int(cols[s_ink]), "v_start": round(float(cs[s_ink]), 1), "start_hidden": bool(hid_s),
                   "u_end": int(cols[e_ink]), "v_end": round(float(cs[e_ink]), 1), "end_hidden": bool(hid_e),
                   "occ_before_start": int(cols[s_ink] - cols[s]) if s_ink > s else 0,
                   "occ_after_end": int(cols[e] - cols[e_ink]) if e_ink < e else 0})
out = {"thickness_v_px": thick, "n_thick": len(th), "dashes": dashes, "gridline_crossings": []}
for ln in cal["vertical_lines"]:
    xv = ln["x_value"]
    u = float(ln["u_at_v0"] + ln["slope_du_dv"] * centre(ua)[0])
    for _ in range(5):
        c, b, w = centre(u)
        u = float(ln["u_at_v0"] + ln["slope_du_dv"] * c)
    c, b, w = centre(u)
    k = int(round(u)) - int(ua)
    left = "".join(s[0] for s in state[max(0, k - 14):k]) if 0 <= k < len(cols) else ""
    right = "".join(s[0] for s in state[k:k + 15]) if 0 <= k < len(cols) else ""
    out["gridline_crossings"].append({"x": xv, "u": round(u, 1), "v": round(c, 1), "local_slope": round(b, 4),
                                      "fit_halfwidth": w, "states_left": left, "states_right": right})
print(json.dumps(out, indent=1))
