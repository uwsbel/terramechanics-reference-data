"""Ring-template centres for the FB-5 markers whose holes are not closed: the overlapping pair at
the left end of the dense line, and the partly printed circle under the right end of the loose line.
A ring of the radii measured on the ten closed markers (inner 11.2, outer 19.2 px, out/FB-5/outer.py)
is matched to the ink in a window that leaves out the drawn line; for the pair both rings are
matched jointly (coordinate descent, 0.25 px steps), the score being the number of window pixels
whose ink agrees with the union of the rings. Also run on two closed markers as a check against their
hole and outer-edge fits. Usage: python template.py <image>"""
import sys
import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = g < 128
R_IN, R_OUT = 11.2, 19.2


def ring(U, V, c):
    r = np.hypot(U - c[0], V - c[1])
    return (r >= R_IN) & (r <= R_OUT)


def score(win, mask, cs):
    u0, v0, u1, v1 = win
    V, U = np.mgrid[v0:v1, u0:u1] + 0.5 - 0.5   # pixel centres at integer coords
    pred = np.zeros_like(mask)
    for c in cs:
        pred |= ring(U, V, c)
    obs = dark[v0:v1, u0:u1]
    return int(((pred == obs) & mask).sum())


def descend(win, mask, cs, span=4.0, step=0.25, rounds=4):
    cs = [list(c) for c in cs]
    for _ in range(rounds):
        for i in range(len(cs)):
            best = None
            for du in np.arange(-span, span + 1e-9, step):
                for dv in np.arange(-span, span + 1e-9, step):
                    trial = [c if j != i else [cs[i][0] + du, cs[i][1] + dv] for j, c in enumerate(cs)]
                    s = score(win, mask, trial)
                    if best is None or s > best[0]:
                        best = (s, trial[i])
            cs[i] = best[1]
        span = max(1.0, span / 2)
    return cs, score(win, mask, cs)


def profile(win, mask, cs, i, axis, d=3.0, step=0.25):
    """Score as circle i is moved along u (axis 0) or v (axis 1): the half-width of the region within
    1 percent of the best score is a measure of how well the centre is pinned."""
    out = []
    for dd in np.arange(-d, d + 1e-9, step):
        trial = [list(c) for c in cs]
        trial[i][axis] += dd
        out.append((dd, score(win, mask, trial)))
    return out


if __name__ == "__main__":
    def report(name, win, mask, cs0):
        cs, s = descend(win, mask, cs0)
        print(f"{name}: score {s} of {int(mask.sum())} px; centres " + "; ".join(f"({c[0]:.2f}, {c[1]:.2f})" for c in cs))
        for i in range(len(cs)):
            for ax in (0, 1):
                pr = profile(win, mask, cs, i, ax)
                best = max(p[1] for p in pr)
                within = [p[0] for p in pr if p[1] >= best - 0.01 * best]
                print(f"   circle {i} axis {'uv'[ax]}: score within 1% over {min(within):+.2f}..{max(within):+.2f} px")
        return cs

    # checks on closed markers (hole fit / outer fit in markers.py, outer.py)
    for name, c, win in (("check dense_mid_up", (1388, 2173), (1362, 2148, 1414, 2198)),
                         ("check loose_top_up", (2353, 2478), (2328, 2453, 2378, 2504))):
        mask = np.ones((win[3] - win[1], win[2] - win[0]), bool)
        report(name, win, mask, [c])
    # the overlapping pair at the left end of the dense line; window below the line's end (v >= 2934)
    win = (1000, 2934, 1072, 2978)
    mask = np.ones((win[3] - win[1], win[2] - win[0]), bool)
    report("dense_left pair", win, mask, [(1027, 2951), (1044, 2951)])
    # the same pair with the window opened up to v = 2925 (line pixels included as disagreement)
    win2 = (1000, 2925, 1072, 2978)
    mask2 = np.ones((win2[3] - win2[1], win2[2] - win2[0]), bool)
    report("dense_left pair (window from v 2925)", win2, mask2, [(1027, 2951), (1044, 2951)])
    # the partly printed circle under the loose line's right end; window below the line (v >= 2560)
    win = (2320, 2565, 2390, 2640)
    mask = np.ones((win[3] - win[1], win[2] - win[0]), bool)
    report("loose_top_low partial", win, mask, [(2351, 2607)])
