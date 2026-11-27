"""For every panel of the curve batches: lines verified in one reading but missing or rejected in the other
(and lines rejected in both). Try to measure each on the page from the lacking reading's own lines
(calibrate_axes.recover_line), and print candidate knots.csv rows with the measurement quality."""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import numpy as np
from PIL import Image
import calibrate_axes as ca

batches = sys.argv[1:]
out = csv.writer(sys.stdout, lineterminator="\n")
for b in batches:
    q = Path("qa") / b
    for ov in csv.DictReader(open(q / "overlays.csv", encoding="utf-8-sig")):
        fid, p = ov["figure_id"], ov["panel"]
        gray = np.asarray(Image.open(ov["image"]).convert("L"), dtype=float)
        maps = {}
        for lab in ("claude", "codex"):
            d = q / "rederived" / lab / fid / f"cal-p{p}"
            cal, X, Y = ca.piecewise_maps(d, ov["image"])
            maps[lab] = {"x": X, "y": Y}
        for axis in ("x", "y"):
            ver = {lab: {kn["value"] for kn in maps[lab][axis].knots} for lab in maps}
            rej = {lab: {kn["value"] for kn in maps[lab][axis].rejected} for lab in maps}
            union = ver["claude"] | ver["codex"] | rej["claude"] | rej["codex"]
            for lab in maps:
                K = maps[lab][axis]
                for val in sorted(union - ver[lab]):
                    ts = [t for kn in K.knots for t in kn["t"]]
                    pts, rms = ca.recover_line(gray, K, val, (min(ts), max(ts)))
                    span = 0.0
                    if len(pts) >= 2:
                        tt = [np.array(pt) @ K.e_t for pt in pts]
                        span = (max(tt) - min(tt)) / (max(ts) - min(ts))
                    why = "rejected" if val in rej[lab] else "missing"
                    other = "verified in the other reading" if val in ver["codex" if lab == "claude" else "claude"] else "not verified in either"
                    print(f"{b} {fid} p{p} {lab} {axis}={val:g} ({why}; {other}): {len(pts)} points, span {span:.0%}, rms {rms:.2f}",
                          file=sys.stderr)
                    for u, v in pts:
                        out.writerow([b, fid, p, lab, val if axis == "x" else "", val if axis == "y" else "", round(u, 2), round(v, 2),
                                      f"{why}; {len(pts)} points over {span:.0%} of the line, straight-line rms {rms:.2f} px"])
