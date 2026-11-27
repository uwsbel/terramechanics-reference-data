"""Dark runs along a row or a column of the page image (binary scan), for reading trace centers.

usage:
  runs.py row <v> <u0> <u1>         dark runs along row v between u0 and u1
  runs.py col <u> <v0> <v1>         dark runs along column u between v0 and v1
  runs.py rows <v0> <v1> <u0> <u1> [step]   one line of runs per row
  runs.py inv <x> <y>               pixel (u, v) of a value pair from the affine map of cal-p1
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parents[1] / "packet" / "p0102.png").convert("L")) < 128

def runs(arr, off):
    out, s = [], None
    for i, d in enumerate(arr):
        if d and s is None: s = i
        if not d and s is not None: out.append((s + off, i - 1 + off)); s = None
    if s is not None: out.append((s + off, len(arr) - 1 + off))
    return out

def fmt(rs): return "  ".join(f"{a}-{b}({(a+b)/2:.1f},w{b-a+1})" for a, b in rs)
c = sys.argv[1]
if c == "row":
    v, u0, u1 = map(int, sys.argv[2:5]); print(v, fmt(runs(g[v, u0:u1 + 1], u0)))
elif c == "col":
    u, v0, v1 = map(int, sys.argv[2:5]); print(u, fmt(runs(g[v0:v1 + 1, u], v0)))
elif c == "rows":
    v0, v1, u0, u1 = map(int, sys.argv[2:6]); st = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    for v in range(v0, v1 + 1, st): print(v, fmt(runs(g[v, u0:u1 + 1], u0)))
elif c == "cols":
    u0, u1, v0, v1 = map(int, sys.argv[2:6]); st = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    for u in range(u0, u1 + 1, st): print(u, fmt(runs(g[v0:v1 + 1, u], v0)))
elif c == "inv":
    cal = json.loads((HERE / "cal-p1" / "calibration.json").read_text())
    ax, ay = np.array(cal["ax"]), np.array(cal["ay"])
    x, y = float(sys.argv[2]), float(sys.argv[3])
    A = np.array([ax[:2], ay[:2]]); b = np.array([x - ax[2], y - ay[2]])
    u, v = np.linalg.solve(A, b); print(f"x={x} y={y} -> u={u:.1f} v={v:.1f}")
