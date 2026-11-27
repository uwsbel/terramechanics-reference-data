"""Reader's helper: trace samples of one curve from its tracker record (track.py).

    python sample.py <cal_dir> <image> <tr.json> <series_id> <step> [--first-u U] [--last-u U] [--min-dash 15]

Ink stretches: columns where the tracker found this curve's ink (clean, or merged with a grid line
or a symbol and read from the free edge); a vertical grid line crossing (vgrid) belongs to the
stretch when ink is found within 8 px on both sides; gaps of 3 columns or more break a stretch;
stretches shorter than --min-dash px are specks and are dropped.

Samples: the left end (first ink column), the curve at every `step` of x (piecewise map of the
calibration, with the page image), the right end (last ink column). A sample's centre is a straight
line fitted to the clean columns within 6 px on the same stretch (vgrid columns are bridged from
the clean columns either side); a sample whose x falls in a gap moves to the nearer stretch end.
Prints one CSV row per sample: pixel_u, pixel_v, u_bound_px, v_bound_px, note.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import calibrate_axes as ca  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("cal_dir")
ap.add_argument("image")
ap.add_argument("tr")
ap.add_argument("series")
ap.add_argument("step", type=float)
ap.add_argument("--min-dash", type=int, default=15)
ap.add_argument("--first-u", type=int)
ap.add_argument("--last-u", type=int)
a = ap.parse_args()

cal, X, Y = ca.piecewise_maps(a.cal_dir, a.image)
d = json.load(open(a.tr, encoding="utf-8"))
t_typ = d["t_typ"]
R = {r["u"]: r for r in d["records"]}
us = sorted(R)


def has_ink(r):
    return r["kind"] in ("clean", "thick") or (r["kind"] == "hgrid" and r.get("edge") != "hidden") \
        or (r["kind"] == "hgrid" and r.get("edge") == "hidden")


ink = {u: has_ink(R[u]) for u in us}
for u in us:
    if R[u]["kind"] == "vgrid":
        left = any(ink.get(u - k) and R[u - k]["kind"] != "vgrid" for k in range(1, 9) if u - k in R)
        right = any(ink.get(u + k) and R[u + k]["kind"] != "vgrid" for k in range(1, 9) if u + k in R)
        # a vgrid run can be up to 11 columns wide: look past it
        if not left:
            left = any(ink.get(u - k) and R[u - k]["kind"] != "vgrid" for k in range(1, 14) if u - k in R)
        if not right:
            right = any(ink.get(u + k) and R[u + k]["kind"] != "vgrid" for k in range(1, 14) if u + k in R)
        ink[u] = left and right
stretches, cur, gap = [], None, 0
for u in us:
    if ink[u]:
        if cur is None:
            cur = [u, u]
        cur[1] = u
        gap = 0
    else:
        gap += 1
        if cur is not None and gap >= 3:
            stretches.append(cur)
            cur = None
if cur:
    stretches.append(cur)
stretches = [s for s in stretches if s[1] - s[0] + 1 >= a.min_dash]
if a.first_u is not None:
    stretches = [[max(s[0], a.first_u), s[1]] for s in stretches if s[1] >= a.first_u]
if a.last_u is not None:
    stretches = [[s[0], min(s[1], a.last_u)] for s in stretches if s[0] <= a.last_u]
# trim vgrid / non-clean columns off the ends: an end is where the curve's own ink ends
def own_ink(r):
    return r["kind"] == "clean" or (r["kind"] in ("hgrid", "thick") and r.get("edge") in ("top", "bottom"))


for s in stretches:
    while not own_ink(R[s[0]]) and s[0] < s[1]:
        s[0] += 1
    while not own_ink(R[s[1]]) and s[1] > s[0]:
        s[1] -= 1


def stretch_of(u):
    for s in stretches:
        if s[0] <= u <= s[1]:
            return s
    return None


def center(u, s):
    """(v, v_bound, how) of the curve at column u within stretch s."""
    clean = [(k, R[k]["v"], R[k]["t"]) for k in range(max(s[0], u - 6), min(s[1], u + 6) + 1)
             if R[k]["kind"] == "clean" and R[k]["t"] >= 0.6 * t_typ]
    how = "clean"
    if R[u]["kind"] != "clean" or len(clean) < 4:
        # bridge: clean columns and free-edge readings within 14 px either side (35 px if too few)
        for w in (14, 35):
            clean = [(k, R[k]["v"], R[k].get("t", t_typ) if R[k]["kind"] == "clean" else t_typ)
                     for k in range(max(s[0], u - w), min(s[1], u + w) + 1)
                     if (R[k]["kind"] == "clean" and R[k]["t"] >= 0.6 * t_typ)
                     or (R[k]["kind"] in ("hgrid", "thick") and R[k].get("edge") in ("top", "bottom"))]
            if len(clean) >= 6:
                break
        how = R[u]["kind"] + (("-" + R[u]["edge"]) if "edge" in R[u] else "")
    if len(clean) >= 3:
        kk = np.array([c[0] for c in clean], float)
        vv = np.array([c[1] for c in clean], float)
        p = np.polyfit(kk, vv, 1)
        v = float(np.polyval(p, u))
        t = float(np.median([c[2] for c in clean]))
    else:
        v, t = R[u].get("v"), t_typ
        how += " (few clean columns)"
    if how.startswith("hgrid") or how.startswith("thick"):
        # also compare with the free-edge reading of that column
        ve = R[u].get("v")
        if ve is not None and abs(ve - v) > 1.5:
            how += f" (edge reading {ve:.1f})"
    return v, t / 2, how


def xval(u, v):
    return X.value(u, v)[0]


# column -> x along the curve, for the columns with a usable centre
samples = []
s0, s1 = stretches[0][0], stretches[-1][1]
v0, b0, h0 = center(s0, stretches[0])
samples.append((s0, v0, 1.5, b0, "left end of the drawn line (first ink column)"))
x_first = xval(s0, v0)
v1, b1, h1 = center(s1, stretches[-1])
x_last = xval(s1, v1)
targets = [round(k * a.step, 4) for k in range(int(np.ceil(x_first / a.step - 1e-9)), int(np.floor(x_last / a.step + 1e-9)) + 1)]
targets = [t for t in targets if t > x_first + 1e-4 and t < x_last - 1e-4]
for tx in targets:
    # find the column where the curve's x equals tx: scan all columns, using a smooth v estimate
    best = None
    for u in range(s0, s1 + 1):
        s = stretch_of(u)
        if s is None:
            # in a gap: interpolate between the stretch ends only to locate the x (not a reading)
            prev = max((st for st in stretches if st[1] < u), key=lambda st: st[1])
            nxt = min((st for st in stretches if st[0] > u), key=lambda st: st[0])
            va, _, _ = center(prev[1], prev)
            vb, _, _ = center(nxt[0], nxt)
            v = va + (vb - va) * (u - prev[1]) / (nxt[0] - prev[1])
        else:
            v = R[u]["v"] if R[u]["kind"] == "clean" else None
            if v is None:
                v, _, _ = center(u, s)
        xv = xval(u, v)
        if best is None or abs(xv - tx) < abs(best[1] - tx):
            best = (u, xv)
    u = best[0]
    s = stretch_of(u)
    if s is None:
        prev = max((st for st in stretches if st[1] < u), key=lambda st: st[1])
        nxt = min((st for st in stretches if st[0] > u), key=lambda st: st[0])
        ue = prev[1] if (u - prev[1]) <= (nxt[0] - u) else nxt[0]
        se = prev if ue == prev[1] else nxt
        v, b, how = center(ue, se)
        samples.append((ue, v, 2.0, b, f"x={tx:g} falls in a gap of the line (u {prev[1] + 1}..{nxt[0] - 1}); moved to the nearer dash end, on the ink"))
    else:
        v, b, how = center(u, s)
        note = f"x={tx:g}"
        bu = 1.0
        if how != "clean":
            note += f"; {how}: centre bridged from the curve's own ink on either side (clean columns, and free-edge readings where a grid line merges)"
            b += 1.0 if not how.startswith("vgrid") else 0.0
        samples.append((u, v, bu, b, note))
samples.append((s1, v1, 1.5, b1, "right end of the drawn line (last ink column)"))
for st in stretches:
    for end, nb in ((st[0], st[0] - 1), (st[1], st[1] + 1)):
        if nb in R and R[nb]["kind"] == "vgrid":
            print(f"# stretch end {end} meets a vertical line at {nb}", file=sys.stderr)
        if not own_ink(R[end]) or R[end]["kind"] != "clean":
            print(f"# stretch end {end} is {R[end]['kind']} {R[end].get('edge', '')}", file=sys.stderr)
print(f"# {a.series}: stretches {stretches}; x_first {x_first:.4f}, x_last {x_last:.4f}", file=sys.stderr)
for u, v, bu, bv, note in samples:
    print(f"{u},{v:.1f},{bu:.1f},{bv:.1f},{note}")
