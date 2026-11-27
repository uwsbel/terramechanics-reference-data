"""Fitted pixel of a printed gridline value from a calibration.json (inverse of the affine map).

usage: fitted_pixel.py <calibration.json> y <value> <u>   -> v where the map gives y=value at column u
       fitted_pixel.py <calibration.json> x <value> <v>   -> u where the map gives x=value at row v
       fitted_pixel.py <calibration.json> pt <u> <v>       -> x, y at a pixel
"""
import json
import sys

cal = json.load(open(sys.argv[1], encoding="utf-8"))
ax, ay = cal["ax"], cal["ay"]
kind = sys.argv[2]
a, b = float(sys.argv[3]), float(sys.argv[4])
if kind == "y":
    print(f"{(a - ay[0] * b - ay[2]) / ay[1]:.1f}")
elif kind == "x":
    print(f"{(a - ax[1] * b - ax[2]) / ax[0]:.1f}")
else:
    print(f"{ax[0]*a+ax[1]*b+ax[2]:.2f} {ay[0]*a+ay[1]*b+ay[2]:.2f}")
