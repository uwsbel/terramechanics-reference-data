import sys, json, numpy as np
from PIL import Image
g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
cal = json.load(open("out/FC-4A/cal-p1/calibration.json"))
ax, ay = np.array(cal["ax"]), np.array(cal["ay"])
A = np.array([ax[:2], ay[:2]]); b = np.array([ax[2], ay[2]])
def px(x, y):
    return np.linalg.solve(A, np.array([x, y]) - b)
def val(u, v):
    return A @ np.array([u, v]) + b
dark = int(sys.argv[1]) if len(sys.argv) > 1 else 160
lines = {"dr95": (px(0,1650), px(5000, 1650+5000*1.327)), "dr0": (px(0,120), px(5000,120+5000*0.933))}
for sid, (p0, p1) in lines.items():
    print("==", sid, "p0", p0.round(1), "p1", p1.round(1))
    for x in range(0, 5001, 250):
        u = px(x, 0)[0]
        # line predicted v at this u
        t = (u - p0[0]) / (p1[0] - p0[0]); vp = p0[1] + t*(p1[1]-p0[1])
        ui = int(round(u))
        col = g[int(vp)-60:int(vp)+60, ui]
        idx = np.where(col < dark)[0]
        runs=[]
        for i in idx:
            if runs and i - runs[-1][-1] <= 1: runs[-1].append(i)
            else: runs.append([i])
        desc = ["%d-%d(c%.1f,w%d)" % (r[0]+int(vp)-60, r[-1]+int(vp)-60, np.mean(r)+int(vp)-60, len(r)) for r in runs]
        print(" x=%4d u=%6.1f vpred=%6.1f  runs: %s" % (x, u, vp, "; ".join(desc)))
