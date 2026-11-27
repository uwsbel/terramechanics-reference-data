"""Column (or row) scans along one drawn curve, for the reader to assign by eye.

    python trace_scan.py <series> <u0> <u1> <step>            column samples
    python trace_scan.py <series> rows <v0> <v1> <step>       row samples (steep parts)

For each sample it lists every dark run within +-W px of the curve's expected position (a
polyline through the reader's own path points below), with the gridline and marker proximity
flags, so a sample on a symbol's outline, on a gridline or in a gap can be rejected.
"""
import json, sys
import numpy as np
from PIL import Image
sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from markers_final import P1

IMG = "../../../packet/p0130.png"
CAL = json.load(open("../cal-p1/calibration.json"))
g = np.asarray(Image.open(IMG).convert("L"))

# rough path of each drawn curve (u, v), from the zoomed crops; only used to centre the search window
PATH = {
 "n4695": [(722,1891),(780,1828),(805,1809),(844,1789),(866,1772),(952,1735),(987,1728),(1067,1705),(1210,1685),(1300,1683),(1420,1678),(1650,1677),(1940,1680),(2060,1685),(2107,1688)],
 "n3815": [(720,2117),(787,2000),(811,1979),(844,1954),(873,1934),(953,1893),(992,1887),(1100,1848),(1127,1843),(1162,1840),(1220,1822),(1300,1808),(1416,1795),(1540,1797),(1676,1798),(1795,1807),(1940,1816),(2060,1826),(2115,1836)],
 "n2934": [(717,2207),(740,2150),(760,2125),(800,2093),(845,2065),(875,2048),(960,2028),(1100,1997),(1243,1982),(1340,1981),(1540,1981),(1780,1983),(1946,1986),(2141,1985)],
 "n1761": [(729,2271),(747,2257),(782,2229),(812,2210),(839,2206),(869,2198),(952,2188),(987,2190),(1078,2180),(1108,2178),(1192,2178),(1220,2173),(1310,2173),(1430,2170),(1543,2163),(1660,2163),(1990,2166),(2141,2172)],
 "n734":  [(717,2253),(745,2251),(787,2250),(813,2240),(844,2242),(882,2237),(958,2236),(998,2230),(1073,2230),(1112,2225),(1187,2225),(1223,2222),(1303,2222),(1420,2221),(1540,2221),(1771,2220),(1943,2218),(2142,2217)],
}

def vline_u(i, v):
    l = CAL["vertical_lines"][i]; return l["u_at_v0"] + l["slope_du_dv"] * v
def hline_v(i, u):
    l = CAL["horizontal_lines"][i]; return l["v_at_u0"] + l["slope_dv_du"] * u

def expected(series, u):
    p = PATH[series]
    for (a, va), (b, vb) in zip(p, p[1:]):
        if a <= u <= b: return va + (vb - va) * (u - a) / (b - a)
    return None
def expected_u(series, v):
    p = PATH[series]
    for (a, va), (b, vb) in zip(p, p[1:]):
        lo, hi = sorted((va, vb))
        if lo <= v <= hi and va != vb: return a + (b - a) * (v - va) / (vb - va)
    return None

def runs(mask, off):
    idx = np.where(mask)[0]; out = []
    if len(idx) == 0: return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1: out.append((int(off + s), int(off + p))); s = i
        p = i
    out.append((int(off + s), int(off + p))); return out

def flags(u, v):
    f = []
    for i in range(len(CAL["vertical_lines"])):
        if abs(u - vline_u(i, v)) < 10: f.append(f"VGRID{CAL['vertical_lines'][i]['x_value']:g}")
    for i in range(len(CAL["horizontal_lines"])):
        if abs(v - hline_v(i, u)) < 14: f.append(f"HGRID{CAL['horizontal_lines'][i]['y_value']:g}@{hline_v(i,u):.0f}")
    for _, s, sym, mu, mv, *_ in P1:
        if abs(u - mu) < 19 and abs(v - mv) < 24: f.append(f"MK:{s}@{mu:.0f},{mv:.0f}")
    return f

def main():
    a = sys.argv[1:]
    s = a[0]; W = 16
    if a[1] == "rows":
        v0, v1, st = map(int, a[2:5])
        for v in range(v0, v1 - 1 if v1 < v0 else v1 + 1, st):
            ue = expected_u(s, v)
            if ue is None: continue
            lo = int(ue - W)
            r = runs(g[v, lo:lo + 2 * W + 1] < 160, lo)
            print(f"row v={v} exp u={ue:.0f}: " + "  ".join(f"[{x}-{y} c{(x+y)/2:.1f} w{y-x+1}]" for x, y in r) + "  " + " ".join(flags(ue, v)))
    else:
        u0, u1, st = map(int, a[1:4])
        for u in range(u0, u1 + 1, st):
            ve = expected(s, u)
            if ve is None: continue
            lo = int(ve - W)
            r = runs(g[lo:lo + 2 * W + 1, u] < 160, lo)
            print(f"col u={u} exp v={ve:.0f}: " + "  ".join(f"[{x}-{y} c{(x+y)/2:.1f} w{y-x+1}]" for x, y in r) + "  " + " ".join(flags(u, ve)))

if __name__ == "__main__":
    main()
