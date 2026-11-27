"""Bounding-box centers of the clean template instances used by refine_markers.py, so the
NCC alignment can be corrected for any offset between my eye-read template center and the
symbol's true geometric center. Run from the FC-4B workspace root."""
import numpy as np
from PIL import Image

im = np.array(Image.open('packet/p0127.png').convert('L'))
dark = im < 128
for name, (u, v, h) in {
    'triangle-up': (1502, 3097, 19), 'square': (1503, 3247, 19), 'triangle-down': (924, 3296, 19),
    'plus': (1442, 3331, 19), 'circle': (1782, 1651, 17),
}.items():
    w = dark[v - h:v + h + 1, u - h:u + h + 1]
    ys, xs = np.nonzero(w)
    cu = u - h + (xs.min() + xs.max()) / 2
    cv = v - h + (ys.min() + ys.max()) / 2
    print(f"{name:14s} eye=({u},{v}) bbox u {u-h+xs.min()}..{u-h+xs.max()} v {v-h+ys.min()}..{v-h+ys.max()} "
          f"center=({cu:.1f},{cv:.1f}) offset=({cu-u:+.1f},{cv-v:+.1f}) size={xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}")
