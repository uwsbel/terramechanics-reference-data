"""Reader's helpers for Figure 4-19 (Claude, batch curves-s4-b1): grid removal, ink following, and
sampling of a drawn trace on its ink. Pixel coordinates are those of packet/p0208.png (u right, v down).

clean(): the dark pixels of the page (gray < DARK) with every measured grid line and frame removed
(the lines of out/F4-19/cal-p*/calibration.json, anchored or not); a band pixel is kept only where ink
lies on both sides of the band, so a trace crossing a grid line keeps its ink there.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

DARK = 160
HERE = Path(__file__).resolve().parent
IMG = HERE.parent.parent / "packet" / "p0208.png"


def load_gray():
    return np.asarray(Image.open(IMG).convert("L"), dtype=float)


def grid_lines():
    """All measured lines: (kind, intercept, slope, panel, label) with kind 'v' (u = a + b v) or 'h' (v = a + b u)."""
    out = []
    for p in ("cal-p1", "cal-p2"):
        cal = json.loads((HERE / p / "calibration.json").read_text(encoding="utf-8"))
        box = cal["box"]
        for L in cal["vertical_lines"]:
            out.append(("v", L["u_at_v0"], L["slope_du_dv"], p, L["label_printed"], box))
        for L in cal["horizontal_lines"]:
            out.append(("h", L["v_at_u0"], L["slope_dv_du"], p, L["label_printed"], box))
    return out


def clean(gray):
    dark = gray < DARK
    H, W = dark.shape
    keep = dark.copy()
    bandmask = np.zeros_like(dark)
    for kind, a, b, p, lab, box in grid_lines():
        u0, v0, u1, v1 = box
        ts = np.arange(v0, v1) if kind == "v" else np.arange(u0, u1)
        # thickness: median dark run through the line center at 60 positions
        widths = []
        for t in ts[:: max(1, len(ts) // 60)]:
            c = a + b * t
            ci = int(round(c))
            if kind == "v":
                prof = dark[t, ci - 12: ci + 13]
            else:
                prof = dark[ci - 12: ci + 13, t]
            if not prof[12]:
                continue
            lo = 12
            while lo > 0 and prof[lo - 1]:
                lo -= 1
            hi = 12
            while hi < len(prof) - 1 and prof[hi + 1]:
                hi += 1
            if lo > 0 and hi < len(prof) - 1:
                widths.append(hi - lo + 1)
        w = int(np.median(widths)) if widths else 5
        hw = w / 2.0 + 1.0
        for t in ts:
            c = a + b * t
            lo, hi = int(np.floor(c - hw)), int(np.ceil(c + hw))
            # ink on both sides of the band, 2 px beyond it
            if kind == "v":
                both = dark[t, lo - 2] and dark[t, hi + 2]
                if not both:
                    keep[t, lo:hi + 1] = False
                bandmask[t, lo:hi + 1] = True
            else:
                both = dark[lo - 2, t] and dark[hi + 2, t]
                if not both:
                    keep[lo:hi + 1, t] = False
                bandmask[lo:hi + 1, t] = True
    return keep, bandmask


if __name__ == "__main__":
    g = load_gray()
    k, bm = clean(g)
    np.save(HERE / "clean.npy", k)
    np.save(HERE / "bandmask.npy", bm)
    im = np.where(k, 0, 255).astype(np.uint8)
    rgb = np.stack([im, im, im], -1)
    rgb[bm & ~k] = (255, 200, 200)
    Image.fromarray(rgb).save(HERE / "crops" / "clean.png")
    print("saved clean.npy, bandmask.npy, crops/clean.png")


# ---------------------------------------------------------------------------------------------
# Ink following along a guide, and sampling on the ink

def load_clean():
    return np.load(HERE / "clean.npy"), np.load(HERE / "bandmask.npy")


def profile_runs(ink, p, n, half):
    """Dark runs along the line p + s n, s in [-half, half] (step 0.5 px, nearest pixel).
    Returns list of (s_start, s_end)."""
    s = np.arange(-half, half + 0.01, 0.5)
    U = np.rint(p[0] + s * n[0]).astype(int)
    V = np.rint(p[1] + s * n[1]).astype(int)
    d = ink[V, U]
    runs = []
    i = 0
    while i < len(d):
        if d[i]:
            j = i
            while j < len(d) and d[j]:
                j += 1
            runs.append((float(s[i]), float(s[j - 1])))
            i = j
        else:
            i += 1
    return runs


def nearest_run(runs, c=0.0, maxdist=4.0):
    best = None
    for a, b in runs:
        dist = 0.0 if a <= c <= b else min(abs(a - c), abs(b - c))
        if dist <= maxdist and (best is None or dist < best[0]):
            best = (dist, a, b)
    return None if best is None else (best[1], best[2])


def track(ink, start, direction, step=2.0, half=9.0, maxgap=40.0, nsteps=2000, stop=None, width_max=30.0, maxdist=4.0):
    """Follow a line from `start` in `direction`. At each step the profile along the normal is read at the
    predicted point; the run nearest the prediction (within 4 px) gives the new center. Gaps (no run) are
    bridged straight up to `maxgap` px. Returns list of (u, v, found, width)."""
    p = np.array(start, float)
    d = np.array(direction, float)
    d /= np.hypot(*d)
    pts = [(p[0], p[1], True, 0.0)]
    gap = 0.0
    hist = [p.copy()]
    for _ in range(nsteps):
        q = p + step * d
        n = np.array([-d[1], d[0]])
        r = nearest_run(profile_runs(ink, q, n, half), 0.0, maxdist)
        if r is not None and (r[1] - r[0]) <= width_max:
            c = 0.5 * (r[0] + r[1])
            q = q + c * n
            gap = 0.0
            pts.append((q[0], q[1], True, r[1] - r[0]))
            hist.append(q.copy())
            if len(hist) > 6:
                dd = hist[-1] - hist[-6]
                if np.hypot(*dd) > 0:
                    d = 0.6 * d + 0.4 * dd / np.hypot(*dd)
                    d /= np.hypot(*d)
        else:
            gap += step
            pts.append((q[0], q[1], False, 0.0))
            if gap > maxgap:
                break
        p = q
        if stop is not None and stop(p):
            break
    return pts
