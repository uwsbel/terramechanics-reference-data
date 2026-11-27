"""For trial lines (angle deg, rho) list the runs of ink within +-tol px along the line, with the
end points in pixels and in psf (calibration cal-p1). Reader's aid only."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[2]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
cal = json.loads((HERE.parent / "cal-p1" / "calibration.json").read_text())
ax, ay = cal["ay"], cal["ay"]
ax = cal["ax"]
def val(u, v):
    return ax[0]*u + ax[1]*v + ax[2], ay[0]*u + ay[1]*v + ay[2]
dark = g < 160
tol = float(sys.argv[1])
for spec in sys.argv[2:]:
    a, rho = map(float, spec.split(","))
    r = np.radians(a)
    n = np.array([np.sin(r), np.cos(r)])       # normal (u, v)
    d = np.array([np.cos(r), -np.sin(r)])      # direction, u increasing
    base = rho * n
    ts = np.arange(-2600, 2600, 1.0)
    on = []
    for t in ts:
        p = base + t * d
        if not (900 < p[0] < 2420 and 1220 < p[1] < 3080):
            on.append(False); continue
        ok = False
        for s in np.arange(-tol, tol + 0.1, 1.0):
            q = p + s * n
            ui, vi = int(round(q[0])), int(round(q[1]))
            if dark[vi, ui]:
                ok = True; break
        on.append(ok)
    on = np.array(on)
    # runs with gaps <= 2 merged
    runs = []
    i = 0
    while i < len(ts):
        if on[i]:
            j = i
            while j + 1 < len(ts) and (on[j+1] or (j + 3 < len(ts) and on[j+2]) or (j + 3 < len(ts) and on[j+3])):
                j += 1
            runs.append((ts[i], ts[j])); i = j + 1
        else:
            i += 1
    print(f"line angle {a} rho {rho}")
    for t0, t1 in runs:
        if t1 - t0 < 8:
            continue
        p0 = base + t0 * d; p1 = base + t1 * d
        x0, y0 = val(*p0); x1, y1 = val(*p1)
        print(f"   run len {t1-t0:5.0f}  ({p0[0]:6.0f},{p0[1]:6.0f}) -> ({p1[0]:6.0f},{p1[1]:6.0f})   psf ({x0:6.0f},{y0:6.0f}) -> ({x1:6.0f},{y1:6.0f})")
