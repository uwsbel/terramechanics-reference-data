"""Assemble points-p1.csv and points-p2.csv (pixels, bounds, notes) from samples.json and the features.

Trace rows: the samples of sample.py plus a trace sample where the ink starts and where it ends (rule 7).
Feature rows: first, last, every local maximum of the trace (peak) and the local minimum after it (knee,
minimum); extremes on auto stretches come from the dense ink centerline (sample.py), the others are read by
eye (series_def.FEATURES and the list below). Sequence: drawing order (arc position along the guide).
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np
import sample as S
from series_def import SERIES, FEATURES

D = json.loads((HERE / "samples.json").read_text())

STYLE = {"run4": "solid line", "run10": "dotted line", "run12": "long-dash line"}


CALS = {p: json.loads((HERE / f"cal-p{p}" / "calibration.json").read_text()) for p in (1, 2)}


def alt_times(panel, u, v):
    """Time of pixel (u, v) interpolated between the drawn vertical lines 100, line 11, 12, 13 and the right
    frame, read (A) as 100, 110, 120, 130, 140 (uniform grid; labels 120, 130, 140 taken as misprints, no 110
    printed) and (B) as printed, 100, 120, 130, 140, then 150 for the unlabeled frame."""
    L = CALS[panel]["vertical_lines"]
    us = [l["u_at_v0"] + l["slope_du_dv"] * v for l in L if l["x_value"] >= 100]
    A = [100, 110, 120, 130, 140]
    B = [100, 120, 130, 140, 150]
    for k in range(len(us) - 1):
        if us[k] <= u <= us[k + 1] or (k == len(us) - 2 and u > us[k + 1]):
            f = (u - us[k]) / (us[k + 1] - us[k])
            return A[k] + f * (A[k + 1] - A[k]), B[k] + f * (B[k + 1] - B[k])
    return None


# extremes: which detected extreme becomes which feature, with what bounds and note. (panel, series) ->
# list of (role, source, values...). source "auto:<i>" = the i-th detected extreme; "pix" = given pixel.
EXTRA = {
    (1, "run4"): [
        ("knee", "auto:1", "knee, minimum after the first peak"),
        ("peak", "auto:2", "peak: second force maximum (broad top)"),
        ("knee", "auto:3", "knee, minimum after the second peak: lowest of three touching traces (runs 10 and 12 lie on it), flat bottom"),
    ],
    (1, "run10"): [
        ("knee", "auto:1", "knee, minimum after the first peak"),
        ("peak", "auto:2", "peak: second force maximum (broad top)"),
        ("knee", "auto:3", "knee, minimum after the second peak: dots between the dash of run 12 and run 4, all touching; flat bottom, the trace then stays near 30 lb"),
    ],
    (1, "run12"): [
        ("knee", "auto:1", "knee, minimum after the first peak (close to 0 lb)"),
        ("peak", "auto:2", "peak: second force maximum"),
        ("knee", "auto:3", "knee, minimum after the second peak, end of a dash before a dash gap"),
        ("peak", "auto:4", "peak: small third maximum, a dash lying on the dots of run 10 with run 4 below (touching); flat top; identity of the ink in this band read from the dot and dash patterns, see notes.md"),
        ("knee", "pix:2240,1919.3,80,6", "knee, minimum after the third peak: the flat final dash (2160 to 2321 px), dots of run 10 on top"),
    ],
    (2, "run4"): [
        ("peak", "pix:1830,2256.3,35,6", "peak: maximum displacement (broad, 1800 to 1860 px)"),
        ("knee", "pix:2030,2264.8,35,6", "knee, minimum after the peak: slight rebound of the displacement (2000 to 2060 px)"),
        ("last", "pix:2319,2259.8,4,6", "last: ink ends under the vertical grid line labeled 140 (uniform-grid value 130 ms)"),
    ],
    (2, "run10"): [
        ("peak", "plateau", "peak: maximum displacement on the plateau (dots between about 1450 and 1700 px); x not an observation"),
        ("last", "pix:1692,2781.5,5,5", "last: last dot (the dotted trace stops at about 78 ms; the other two runs continue to the grid line labeled 140)"),
    ],
    (2, "run12"): [
        ("first", "pix:856.9,3134.1,6,6", "first: this run's own ink starts here, a kink where the long-dash trace leaves the bundle of runs 4 and 10; its first 9 ms are not drawn separately"),
        ("peak", "plateau", "peak: maximum displacement on the plateau; x not an observation"),
        ("last", "pix:2337,2961.8,4,6", "last: dash ends 11 px right of the grid line labeled 140"),
    ],
}


def nearest_arc(P, u, v):
    return int(np.argmin(np.hypot(P[:, 0] - u, P[:, 1] - v)))


def main():
    out = {1: [], 2: []}
    for key, spec in SERIES.items():
        panel, sid = key
        tag = f"{panel}_{sid}"
        P, pidx = S.dense_guide(spec["pieces"])
        cal, X, Y = S.MAPS[panel]
        rows = []
        for r in D[tag]:
            rows.append(dict(kind="trace", arc=r["arc"], u=r["u"], v=r["v"], ub=r["ub"], vb=r["vb"], note=r["note"]))
        feats = []
        for role, u, v, ub, vb, note in FEATURES[key]:
            feats.append((role, u, v, ub, vb, note))
        ex = D.get(tag + "_extremes", [])
        for role, src, note in EXTRA.get(key, []):
            if src.startswith("auto:"):
                e = ex[int(src.split(":")[1])]
                hw = 6.0 if spec["style"] != "dotted" else 5.0
                feats.append((role, e["u"], e["v"], max(e["half_len"], hw), hw, note + (" (manual stretch)" if e["manual"] else "")))
            elif src.startswith("pix:"):
                u, v, ub, vb = (float(x) for x in src.split(":")[1].split(","))
                feats.append((role, u, v, ub, vb, note))
            elif src == "plateau":
                cl = S.centerline(panel, sid, P, pidx, S.ink_profile(P))
                V = np.array([c[2] for c in cl]); U = np.array([c[1] for c in cl])
                k = 4
                Vs = np.array([np.median(V[max(0, j - k):j + k + 1]) for j in range(len(V))])
                j = int(np.argmin(Vs))
                flat = np.where(np.abs(Vs - Vs[j]) <= 2.0)[0]
                ub = 0.5 * (U[flat].max() - U[flat].min())
                feats.append((role, float(U[j]), float(Vs[j]), max(ub, 5.0), 5.0, note))
        # first and last trace samples at the ink ends (rule 7)
        roles = {f[0]: f for f in feats}
        for role in ("first", "last"):
            if role in roles:
                f = roles[role]
                rows.append(dict(kind="trace", arc=nearest_arc(P, f[1], f[2]) + (-0.5 if role == "first" else 0.5),
                                 u=f[1], v=f[2], ub=f[3], vb=f[4], note=f"{role} trace sample: where the line's ink {'starts' if role == 'first' else 'ends'}; " + f[5].split(': ', 1)[-1]))
        for role, u, v, ub, vb, note in feats:
            rows.append(dict(kind="feature", arc=nearest_arc(P, u, v) + (-0.6 if role == "first" else (0.6 if role == "last" else 0.1)),
                             u=round(u, 1), v=round(v, 1), ub=round(ub, 1), vb=round(vb, 1), note=f"{role}: " + note if not note.startswith(role) else note))
        rows.sort(key=lambda r: r["arc"])
        # a time sample that landed within 2 px of the ink-end trace sample duplicates it
        keep = []
        for r in rows:
            dup = (r["kind"] == "trace" and any(q["kind"] == "trace" and abs(q["u"] - r["u"]) < 2 and abs(q["v"] - r["v"]) < 2
                                                 for q in keep))
            if not dup:
                keep.append(r)
        rows = keep
        for k, r in enumerate(rows, 1):
            t = X.value(r["u"], r["v"])[0]
            note = r["note"]
            if t > 100.0:
                ab = alt_times(panel, r["u"], r["v"])
                note += (f"; beyond the 100 ms line (the lines beyond it are not anchored: the labels skip 110): x is the 90 to 100 ms interval "
                         f"extrapolated, {t:.1f} ms; between the drawn lines read as 110, 120, 130, 140 it is {ab[0]:.1f} ms; "
                         f"read as printed (120, 130, 140, frame 150) it is {ab[1]:.1f} ms; see notes.md")
            out[panel].append({"figure_id": "F4-19", "panel": panel, "series_id": sid, "point_kind": r["kind"], "sequence": k,
                               "pixel_u": round(float(r["u"]), 1), "pixel_v": round(float(r["v"]), 1),
                               "u_bound_px": round(float(r["ub"]), 1), "v_bound_px": round(float(r["vb"]), 1),
                               "symbol": STYLE[sid], "note": note.replace("\n", " ")})
    cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
    for panel in (1, 2):
        with (HERE / f"points-p{panel}.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
            w.writeheader()
            w.writerows(out[panel])
        from collections import Counter
        c = Counter((r["series_id"], r["point_kind"]) for r in out[panel])
        print(panel, dict(c))


if __name__ == "__main__":
    main()
