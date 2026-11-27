"""Inverse of a calibration: value (x, y) -> pixel (u, v), and pixel -> value.
usage: calpix.py <calibration.json> topix x y [x y ...] | toval u v [u v ...]"""
import json, sys
import numpy as np
cal = json.load(open(sys.argv[1], encoding="utf-8"))
ax, ay = np.array(cal["ax"]), np.array(cal["ay"])
M = np.array([[ax[0], ax[1]], [ay[0], ay[1]]]); c = np.array([ax[2], ay[2]])
mode = sys.argv[2]; nums = [float(s) for s in sys.argv[3:]]
for i in range(0, len(nums), 2):
    a, b = nums[i], nums[i + 1]
    if mode == "topix":
        u, v = np.linalg.solve(M, np.array([a, b]) - c)
        print(f"x={a:g} y={b:g} -> u={u:.1f} v={v:.1f}")
    else:
        x, y = M @ np.array([a, b]) + c
        print(f"u={a:g} v={b:g} -> x={x:.2f} y={y:.2f}")
