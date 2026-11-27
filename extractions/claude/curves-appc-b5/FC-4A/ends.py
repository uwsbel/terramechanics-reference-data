import numpy as np, json
from PIL import Image
g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
D = g < 160
F = json.load(open("out/FC-4A/linefit.json"))
cal = json.load(open("out/FC-4A/cal-p1/calibration.json"))
vl = {l["x_value"]: l for l in cal["vertical_lines"]}
def ucal(xv, v):  # u of calibrated vertical line x=xv at row v
    l = vl[xv]; return l["u_at_v0"] + l["slope_du_dv"] * v
for sid in ("dr95", "dr0"):
    a, b = F[sid]["a"], F[sid]["b"]
    P = np.array(F[sid]["pts"]["dash_left"])
    first = P[P[:, 0] <= 956]
    bf, af = np.polyfit(first[:, 0], first[:, 3], 1)
    two = P[P[:, 0] <= 995]
    b2, a2 = np.polyfit(two[:, 0], two[:, 3], 1)
    # intersect with x=0 line
    for name, (aa, bb) in (("solid-fit", (a, b)), ("first-dash", (af, bf)), ("first-two-dashes", (a2, b2)), ("all-left-dashes", tuple(np.polyfit(P[:, 0], P[:, 3], 1)[::-1]))):
        u = 921.0
        for _ in range(20):
            v = aa + bb * u; u = ucal(0.0, v)
        print(sid, name, "intercept u=%.2f v=%.2f  slope %.4f" % (u, v, bb))
    # first dash: leftmost ink column touching frame: list column runs u 918..930
    for u in range(916, 932):
        vc = a + b * u
        idx = np.where(D[int(vc - 20):int(vc + 21), u])[0]
        print("   u=%d dark rows near line: %s" % (u, (idx.min() + int(vc - 20), idx.max() + int(vc - 20), len(idx)) if len(idx) else None))
