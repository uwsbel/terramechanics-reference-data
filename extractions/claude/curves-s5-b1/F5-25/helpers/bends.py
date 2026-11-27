"""Bends of a panel's center line on the page: the turning angle between the chord directions 25 px of
arc before and after each point (from the center line resampled every 1 px of arc length); local maxima
above 15 degrees are listed, with the time and load there."""
import json
import sys
import numpy as np
from trace_tools import Panel
n = int(sys.argv[1])
P = Panel(n)
cl = [p for p in json.load(open(f"centerline-p{n}.json"))["points"] if p["kind"] in ("row", "col", "row-amb", "col-amb")]
cl.sort(key=lambda p: p["x"])
U = np.array([p["u"] for p in cl]); V = np.array([p["v"] for p in cl])
# light smoothing
k = 5
Us = np.convolve(U, np.ones(k) / k, mode="valid"); Vs = np.convolve(V, np.ones(k) / k, mode="valid")
s = np.concatenate([[0], np.cumsum(np.hypot(np.diff(Us), np.diff(Vs)))])
S = np.arange(0, s[-1], 1.0)
u = np.interp(S, s, Us); v = np.interp(S, s, Vs)
D = 25
ang = np.zeros(len(S))
for i in range(D, len(S) - D):
    a = np.array([u[i] - u[i - D], v[i] - v[i - D]]); b = np.array([u[i + D] - u[i], v[i + D] - v[i]])
    c = np.clip(a @ b / np.hypot(*a) / np.hypot(*b), -1, 1)
    ang[i] = np.degrees(np.arccos(c)) * np.sign(a[0] * b[1] - a[1] * b[0])
for i in range(D, len(S) - D):
    w = np.abs(ang[max(0, i - 20):i + 21])
    if abs(ang[i]) >= 15 and abs(ang[i]) == w.max():
        x, y = P.xy(u[i], v[i])
        print(f"bend {ang[i]:+6.1f} deg at u={u[i]:.1f} v={v[i]:.1f}  t={x:.4f} y={y:.2f}")
