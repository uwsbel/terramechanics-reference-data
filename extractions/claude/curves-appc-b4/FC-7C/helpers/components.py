"""Candidate symbol finder (reader's aid only, every candidate is checked by eye).

Masks the fitted grid lines (from calibration.json), labels the remaining dark pixels into
connected components (8-connectivity), merges components whose boxes lie within `gap` px of each
other, and prints bbox, bbox center, ink centroid and filled-area centroid per merged blob.
Usage: python components.py <image> <calibration.json> u0 v0 u1 v1 [--gap 4] [--minpix 40]
"""
import sys, json
from collections import deque
import numpy as np
from PIL import Image


def main():
    img, calp = sys.argv[1], sys.argv[2]
    u0, v0, u1, v1 = map(int, sys.argv[3:7])
    gap = 4
    minpix = 40
    halfw = 4
    args = sys.argv[7:]
    if '--gap' in args:
        gap = int(args[args.index('--gap') + 1])
    if '--minpix' in args:
        minpix = int(args[args.index('--minpix') + 1])
    if '--halfw' in args:
        halfw = float(args[args.index('--halfw') + 1])
    g = np.array(Image.open(img).convert('L'))
    dark = g[v0:v1, u0:u1] < 160
    cal = json.load(open(calp))
    H, W = dark.shape
    vv, uu = np.mgrid[v0:v1, u0:u1]
    mask = np.zeros_like(dark)
    for L in cal['vertical_lines']:
        uc = L['u_at_v0'] + L['slope_du_dv'] * vv
        hw = halfw + (2 if L['y_value'] in (0.0, 35.0) else 0)
        mask |= np.abs(uu - uc) <= hw
    for L in cal['horizontal_lines']:
        vc = L['v_at_u0'] + L['slope_dv_du'] * uu
        hw = halfw + (2 if L['x_value'] in (0.0, 0.32) else 0)
        mask |= np.abs(vv - vc) <= hw
    d = dark & ~mask
    lab = -np.ones((H, W), dtype=int)
    comps = []
    for (r, c) in zip(*np.nonzero(d)):
        if lab[r, c] >= 0:
            continue
        k = len(comps)
        q = deque([(r, c)])
        lab[r, c] = k
        pix = []
        while q:
            y, x = q.popleft()
            pix.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < H and 0 <= xx < W and d[yy, xx] and lab[yy, xx] < 0:
                        lab[yy, xx] = k
                        q.append((yy, xx))
        comps.append(np.array(pix))
    # merge by bbox proximity
    boxes = [[p[:, 1].min(), p[:, 0].min(), p[:, 1].max(), p[:, 0].max()] for p in comps]
    parent = list(range(len(comps)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if a[0] - gap <= b[2] and b[0] - gap <= a[2] and a[1] - gap <= b[3] and b[1] - gap <= a[3]:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(len(comps)):
        groups.setdefault(find(i), []).append(comps[i])
    out = []
    for gid, ps in groups.items():
        p = np.vstack(ps)
        if len(p) < minpix:
            continue
        bu0, bv0, bu1, bv1 = p[:, 1].min(), p[:, 0].min(), p[:, 1].max(), p[:, 0].max()
        # filled centroid: fill rows between first and last ink per row inside bbox (rough)
        sub = np.zeros((bv1 - bv0 + 1, bu1 - bu0 + 1), bool)
        sub[p[:, 0] - bv0, p[:, 1] - bu0] = True
        fill = np.zeros_like(sub)
        for r in range(sub.shape[0]):
            xs = np.nonzero(sub[r])[0]
            if len(xs):
                fill[r, xs.min():xs.max() + 1] = True
        fy, fx = np.nonzero(fill)
        out.append((bu0 + u0, bv0 + v0, bu1 + u0, bv1 + v0, len(p),
                    (bu0 + bu1) / 2 + u0, (bv0 + bv1) / 2 + v0,
                    p[:, 1].mean() + u0, p[:, 0].mean() + v0,
                    fx.mean() + bu0 + u0, fy.mean() + bv0 + v0))
    out.sort(key=lambda t: (t[1], t[0]))
    print('u0,v0,u1,v1,npix,bbox_cu,bbox_cv,ink_cu,ink_cv,fill_cu,fill_cv,w,h')
    for t in out:
        print('%d,%d,%d,%d,%d,%.1f,%.1f,%.1f,%.1f,%.1f,%.1f,%d,%d' % (t + (t[2] - t[0] + 1, t[3] - t[1] + 1)))


if __name__ == '__main__':
    main()
