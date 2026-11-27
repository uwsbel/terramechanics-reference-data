"""Column runs at each target penetration along the dashed trace (F2-47 helper).

A rough path through the dash centroids (from helpers/components.py, read off the list by eye)
gives the expected row; the column of each target penetration is then computed at that row
(helpers/probe.py u_of) and its dark runs within +-25 px are listed, so the dash run can be told
from the solid trace, the label letters and the grid lines by eye.
"""
import sys
import numpy as np
sys.argv = [sys.argv[0], 'out/F2-47/cal-p1/calibration.json', 'packet/p0108.png', '0', '0']
exec(open('out/F2-47/helpers/probe.py').read().split("u = u_of(x, vg)")[0])
path = [(510,3203),(536,3150),(566,3093),(596,3040),(633.6,2991.8),(681.4,2954.1),(742,2941),(800,2945),
        (862.5,2958.2),(925,2967),(986.7,2965.8),(1047,2947.5),(1100,2925),(1161.7,2897.3),(1218,2870.2),
        (1277,2840),(1331.6,2813.3),(1387.2,2784.6),(1444.5,2754.2),(1499,2724.8),(1558.6,2697.2),
        (1611.3,2665.1),(1667.4,2636.2),(1722,2607),(1780,2576.9),(1836.5,2546.4),(1892.2,2515.9),
        (1948.3,2484.9),(2003,2455),(2059.6,2423),(2114.7,2392.2),(2169.9,2361.2),(2224.2,2330.3),
        (2279.7,2298.8),(2333,2268)]
pu = np.array([p[0] for p in path]); pv = np.array([p[1] for p in path])
for k in range(1, 25):
    x = k * 0.25
    v = 3100.0
    for _ in range(5):
        u = u_of(x, v); v = float(np.interp(u, pu, pv))
    ui = int(round(u))
    col = img[int(v) - 25:int(v) + 26, ui]
    runs = []; i = 0
    while i < len(col):
        if col[i]:
            j = i
            while j < len(col) and col[j]: j += 1
            runs.append(f"{int(v)-25+i}-{int(v)-25+j-1}({j-i})"); i = j
        else: i += 1
    print(f"x={x:5.2f} u={u:7.1f} col {ui} v~{v:6.1f}: " + ' '.join(runs))
