import sys
sys.argv = sys.argv[:1]
from geom import u_for_y
import subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
CEN = [(2130,2130),(2120,2120),(2000,1965),(1960,1945),(1900,1910),(1800,1863),(1700,1833),(1600,1800),(1500,1777),(1400,1767),(1300,1745),(1200,1730),(1100,1720),(1000,1710),(900,1690),(800,1660),(740,1560)]
def vc(u):
    pts = sorted(CEN)
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        if u0 <= u <= u1:
            return v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return pts[0][1] if u < pts[0][0] else pts[-1][1]
for y in range(5, 100, 5):
    u = 2000.0
    for _ in range(5):
        u = u_for_y(y, vc(u))
    print(f"y={y} u={u:.1f} vband~{vc(u):.0f}")
