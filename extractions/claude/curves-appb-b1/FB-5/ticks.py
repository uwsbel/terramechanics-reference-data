"""Find tick marks along the four frame lines of FB-5: dark runs in thin strips parallel to each frame
line, on both sides of it, at several distances from its centre line. A tick shows as a short run
(a few px) found at successive distances at the same position along the line.
Usage: python ticks.py <image>"""
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
from frame import fit_line, runs  # noqa: E402

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = g < 128
TL, TR, BR, BL = (652, 880), (2783, 852), (2834, 3966), (700, 3995)
F = {
    "bottom": fit_line(dark, (BL[0] + 40, BL[1]), (BR[0] - 40, BR[1]), True),
    "top": fit_line(dark, (TL[0] + 40, TL[1]), (TR[0] - 40, TR[1]), True),
    "left": fit_line(dark, (TL[0], TL[1] + 40), (BL[0], BL[1] - 40), False),
    "right": fit_line(dark, (TR[0], TR[1] + 40), (BR[0], BR[1] - 40), False),
}


def scan(name, dists, t_lo, t_hi):
    f = F[name]
    horizontal = name in ("bottom", "top")
    print(f"== {name}")
    for d in dists:
        prof = []
        for t in range(t_lo, t_hi):
            c = f["intercept"] + f["slope"] * t + d
            ci = int(round(c))
            prof.append(dark[ci, t] if horizontal else dark[t, ci])
        rr = runs(np.array(prof), t_lo)
        rr = [r for r in rr if r[1] <= 25]
        print(f"  d={d:+4d}: " + ", ".join(f"{c:.1f}({w})" for c, w in rr))


scan("bottom", [-10, -14, -18, -22, -26, 10, 14, 18], 720, 2820)
scan("top", [-14, -10, 10, 14, 18, 22], 670, 2770)
scan("left", [-14, -10, 8, 12, 16, 20, 24], 900, 3975)
scan("right", [-14, -10, -8, 8, 10, 14], 870, 3950)
