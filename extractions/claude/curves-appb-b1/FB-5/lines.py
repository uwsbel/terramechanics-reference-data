"""The drawn straight segments of FB-5 measured on the ink.
For each segment (approximate end points from the zoomed crops) the centre of the line's ink is
found on profiles perpendicular to it every 2 px, away from the markers (more than R_OUT + 5 px from
any marker centre); a straight line is fitted to those centres (two passes, outliers beyond 3 MAD
set aside). The ends of each polyline are found by walking along the fitted line until its ink stops
or it meets a marker ring. Usage: python lines.py <image> [out.json]"""
import json
import sys
import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = g < 128
R_OUT = 19.2

MARKERS = {   # final centres (markers.py hole/outer fits averaged; template.py for the cut ones)
    "dense_left_lowL": (1026.75, 2951.0), "dense_left_lowR": (1042.5, 2951.5), "dense_left_top": (1044.2, 2889.0),
    "dense_mid_up": (1388.4, 2173.0), "dense_mid_low": (1390.6, 2235.0), "dense_top_up": (2376.9, 1081.3),
    "dense_top_low": (2375.0, 1148.2), "loose_bot_up": (1124.4, 3472.7), "loose_bot_low": (1136.0, 3506.2),
    "loose_mid_up": (1578.0, 3036.0), "loose_mid_low": (1583.5, 3069.5), "loose_top_up": (2352.9, 2478.4),
    "loose_top_low": (2351.25, 2605.5),
}


def pix(u, v):
    return bool(dark[int(round(v)), int(round(u))])


def profile_centre(p, n, half=12, step=0.5):
    """Centre offset (along n) and width of the dark run nearest p on the profile across the line."""
    offs = np.arange(-half, half + 1e-9, step)
    vals = np.array([pix(p[0] + o * n[0], p[1] + o * n[1]) for o in offs])
    best = None
    i = 0
    while i < len(offs):
        if vals[i]:
            j = i
            while j + 1 < len(offs) and vals[j + 1]:
                j += 1
            c, w = (offs[i] + offs[j]) / 2, offs[j] - offs[i] + step
            if best is None or abs(c) < abs(best[0]):
                best = (c, w)
            i = j + 1
        else:
            i += 1
    return best


def near_marker(p, pad):
    return min(np.hypot(p[0] - m[0], p[1] - m[1]) for m in MARKERS.values()) < R_OUT + pad


def measure(a, b, pad=5, step=2.0):
    a, b = np.array(a, float), np.array(b, float)
    for _ in range(2):
        L = np.hypot(*(b - a))
        d = (b - a) / L
        n = np.array([-d[1], d[0]])
        S, O, W = [], [], []
        for s in np.arange(0, L + 1e-9, step):
            p = a + s * d
            if near_marker(p, pad):
                continue
            r = profile_centre(p, n)
            if r is None or r[1] > 14:
                continue
            S.append(s); O.append(r[0]); W.append(r[1])
        S, O, W = map(np.array, (S, O, W))
        c1, c0 = np.polyfit(S, O, 1)
        res = O - (c0 + c1 * S)
        mad = np.median(np.abs(res - np.median(res))) * 1.4826
        keep = np.abs(res) <= max(1.0, 3 * mad)
        c1, c0 = np.polyfit(S[keep], O[keep], 1)
        res = O[keep] - (c0 + c1 * S[keep])
        a, b = a + c0 * n, b + (c0 + c1 * L) * n   # refined end points of the guide, on the fitted line
    return {"a": a.tolist(), "b": b.tolist(), "rms": float(np.sqrt(np.mean(res ** 2))), "n": int(keep.sum()),
            "n_all": int(len(S)), "width_median": float(np.median(W[keep])), "width_p90": float(np.percentile(W[keep], 90)),
            "s_range": [float(S[keep].min()), float(S[keep].max())], "length": float(np.hypot(*(b - a))),
            "max_abs_res": float(np.abs(res).max())}


def intersect(s1, s2):
    p, r = np.array(s1["a"]), np.array(s1["b"]) - np.array(s1["a"])
    q, t = np.array(s2["a"]), np.array(s2["b"]) - np.array(s2["a"])
    cross = r[0] * t[1] - r[1] * t[0]
    lam = ((q - p)[0] * t[1] - (q - p)[1] * t[0]) / cross
    return (p + lam * r).tolist()


def walk(seg, start, direction, max_len=80):
    """From `start` (a point on the fitted line, on clean ink) walk along the line in `direction`
    (+1 towards b, -1 towards a) in 0.5 px steps: report where the centre stops being dark and where
    the line first meets the outer edge of a marker ring."""
    a, b = np.array(seg["a"]), np.array(seg["b"])
    d = (b - a) / np.hypot(*(b - a)) * direction
    p0 = np.array(start)
    ink_end, ring = None, None
    for k in range(int(max_len / 0.5)):
        p = p0 + k * 0.5 * d
        if ring is None:
            for name, m in MARKERS.items():
                if np.hypot(p[0] - m[0], p[1] - m[1]) <= R_OUT:
                    ring = (p.tolist(), name)
                    break
        # dark at the centre or within 1 px across
        n = np.array([-d[1], d[0]])
        if not any(pix(*(p + o * n)) for o in (-1, 0, 1)):
            ink_end = (p - 0.5 * d).tolist()
            break
    return ink_end, ring


if __name__ == "__main__":
    segs = {
        "dense_1": measure((1040, 2932), (1398, 2190)),
        "dense_2": measure((1398, 2190), (2391, 1099)),
        "loose_1": measure((1143, 3472), (1585, 3052)),
        "loose_2": measure((1585, 3052), (2351, 2543)),
    }
    for k, s in segs.items():
        print(f"{k}: a ({s['a'][0]:.1f}, {s['a'][1]:.1f}) b ({s['b'][0]:.1f}, {s['b'][1]:.1f}) rms {s['rms']:.2f} max {s['max_abs_res']:.2f} "
              f"n {s['n']}/{s['n_all']} width med {s['width_median']:.1f} p90 {s['width_p90']:.1f} s {s['s_range'][0]:.0f}-{s['s_range'][1]:.0f} of {s['length']:.0f}")
    vd = intersect(segs["dense_1"], segs["dense_2"])
    vl = intersect(segs["loose_1"], segs["loose_2"])
    print(f"dense vertex ({vd[0]:.1f}, {vd[1]:.1f}); loose vertex ({vl[0]:.1f}, {vl[1]:.1f})")
    ends = {}
    for name, seg, direction in (("dense_left", segs["dense_1"], -1), ("dense_right", segs["dense_2"], +1),
                                 ("loose_left", segs["loose_1"], -1), ("loose_right", segs["loose_2"], +1)):
        a, b = np.array(seg["a"]), np.array(seg["b"])
        d = (b - a) / np.hypot(*(b - a))
        s_clean = seg["s_range"][0] if direction < 0 else seg["s_range"][1]
        start = a + s_clean * d
        ink_end, ring = walk(seg, start, direction)
        ends[name] = {"clean_from": start.tolist(), "ink_end": ink_end, "ring": ring}
        print(f"{name}: last clean sample ({start[0]:.1f}, {start[1]:.1f}); ink ends at "
              f"{'(%.1f, %.1f)' % tuple(ink_end) if ink_end else 'not within 80 px'}; meets ring "
              f"{'(%.1f, %.1f) of %s' % (ring[0][0], ring[0][1], ring[1]) if ring else 'none'}")
    if len(sys.argv) > 2:
        json.dump({"segments": segs, "vertex_dense": vd, "vertex_loose": vl, "ends": ends, "markers": MARKERS},
                  open(sys.argv[2], "w"), indent=1)
