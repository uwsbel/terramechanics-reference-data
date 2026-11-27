"""Claude reader helper (FA-18): print the classified ink (C curve, g grid, . white) along the iso-grain-size
line of each sample of the low band and along lines shifted by a few pixels, u from U0 to U1; the 0 percent
frame line of cal-p1 is marked with | at its centre (column of the string)."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import geom, scanline as sl  # noqa: E402

U0, U1 = int(sys.argv[1]), int(sys.argv[2])
ks = [int(x) for x in sys.argv[3].split(",")]
offs = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else [-6, -3, 0, 3, 6]
f0 = [l for l in geom.cal["vertical_lines"] if l["y_value"] == 0][0]
for k in ks:
    g = 0.02 * 10 ** (0.05 * k)
    c, kk = geom.iso_g(g)
    print(f"k={k} g={g:.4f}  (u0={U0})")
    for d in offs:
        s = ""
        for u in range(U0, U1):
            v = c + kk * u + d
            s += sl.cls(u, v)
        vmid = c + kk * 2060 + d
        fu = f0["u_at_v0"] + f0["slope_du_dv"] * vmid
        i = int(round(fu)) - U0
        s = s[:i] + "|" + s[i + 1:]
        print(f"  v~{vmid:7.1f} {s}")
