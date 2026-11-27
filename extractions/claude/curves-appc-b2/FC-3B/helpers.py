"""Helper for the blind reading of FC-3B (Claude). Not part of tools/.
  python helpers.py fitted <calibration.json> x|y <value> <other_pixel>
  python helpers.py holes <image> u0 v0 u1 v1 [--ink]   list enclosed white regions (marker interiors)
                                                      or, with --ink, small isolated ink blobs (plus signs)
"""
import sys, json
import numpy as np
from PIL import Image

def load_cal(p):
    with open(p) as f:
        return json.load(f)

def fitted_pixel(cal, axis, value, other):
    ax, ay = cal["ax"], cal["ay"]
    # x = ax0 u + ax1 v + ax2 ; y = ay0 u + ay1 v + ay2
    if axis == "x":   # solve u given x=value and v=other
        return (value - ax[1] * other - ax[2]) / ax[0]
    else:             # solve v given y=value and u=other
        return (value - ay[0] * other - ay[2]) / ay[1]

def label_components(mask):
    """Row-run union-find labeling of True pixels in a 2-D bool array. Returns list of
    components as dicts: area, bbox (u0,v0,u1,v1), centroid (u,v), touches_border."""
    H, W = mask.shape
    parent = []
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    runs = []  # (row, c0, c1, label)
    prev = []
    for r in range(H):
        row = mask[r]
        d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
        starts = np.where(d == 1)[0]; ends = np.where(d == -1)[0]
        cur = []
        for c0, c1 in zip(starts, ends):
            lab = len(parent); parent.append(lab)
            for (pc0, pc1, plab) in prev:
                if pc0 < c1 and c0 < pc1:
                    union(plab, lab)
            cur.append((c0, c1, lab))
            runs.append((r, c0, c1, lab))
        prev = cur
    comps = {}
    for (r, c0, c1, lab) in runs:
        root = find(lab)
        c = comps.setdefault(root, {"area": 0, "u0": 1e9, "v0": 1e9, "u1": -1, "v1": -1, "su": 0.0, "sv": 0.0})
        n = c1 - c0
        c["area"] += n
        c["u0"] = min(c["u0"], c0); c["u1"] = max(c["u1"], c1 - 1)
        c["v0"] = min(c["v0"], r); c["v1"] = max(c["v1"], r)
        c["su"] += n * (c0 + c1 - 1) / 2.0
        c["sv"] += n * r
    out = []
    for c in comps.values():
        out.append({"area": c["area"], "u0": c["u0"], "v0": c["v0"], "u1": c["u1"], "v1": c["v1"],
                    "cu": c["su"] / c["area"], "cv": c["sv"] / c["area"],
                    "border": c["u0"] == 0 or c["v0"] == 0 or c["u1"] == W - 1 or c["v1"] == H - 1})
    return out

def holes(img, box, ink=False, amin=40, amax=2500, smax=60):
    u0, v0, u1, v1 = box
    g = np.array(Image.open(img).convert("L"))[v0:v1, u0:u1]
    mask = (g < 128) if ink else (g >= 128)
    comps = label_components(mask)
    res = []
    for c in comps:
        w = c["u1"] - c["u0"] + 1; h = c["v1"] - c["v0"] + 1
        if c["border"] or c["area"] < amin or c["area"] > amax or w > smax or h > smax:
            continue
        res.append({**c, "u0": c["u0"] + u0, "u1": c["u1"] + u0, "v0": c["v0"] + v0, "v1": c["v1"] + v0,
                    "cu": c["cu"] + u0, "cv": c["cv"] + v0, "w": w, "h": h})
    res.sort(key=lambda c: (c["cu"], c["cv"]))
    return res

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fitted":
        cal = load_cal(sys.argv[2]); print(f"{fitted_pixel(cal, sys.argv[3], float(sys.argv[4]), float(sys.argv[5])):.1f}")
    elif cmd == "holes":
        img = sys.argv[2]; box = [int(x) for x in sys.argv[3:7]]
        ink = "--ink" in sys.argv
        for c in holes(img, box, ink=ink):
            print(f"cu={c['cu']:7.1f} cv={c['cv']:7.1f} area={c['area']:5d} w={c['w']:3d} h={c['h']:3d} bbox=({c['u0']},{c['v0']},{c['u1']},{c['v1']})")
