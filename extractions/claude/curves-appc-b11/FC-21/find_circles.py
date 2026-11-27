# Ring-template search for open circles (outer half-span ~18.5 px, inner ~11.5 px) over a box.
import sys
import numpy as np
from PIL import Image
img = sys.argv[1]; u0, v0, u1, v1 = map(int, sys.argv[2:6])
g = (np.asarray(Image.open(img).convert("L"))[v0:v1, u0:u1] < 128).astype(float)
R = 20
yy, xx = np.mgrid[-R:R + 1, -R:R + 1]
r = np.hypot(xx, yy)
ring = ((r >= 12.5) & (r <= 17.5)).astype(float); ring /= ring.sum()
hole = (r <= 9.5).astype(float); hole /= hole.sum()
def conv(a, k):
    H, W = a.shape; kh, kw = k.shape
    F = np.fft.rfft2(a, s=(H + kh, W + kw)); K = np.fft.rfft2(k, s=(H + kh, W + kw))
    c = np.fft.irfft2(F * K, s=(H + kh, W + kw))
    return c[R:R + H, R:R + W]
ringv = conv(g, ring); holev = conv(g, hole)
score = ringv - holev
# local maxima above threshold
thr = float(sys.argv[6]) if len(sys.argv) > 6 else 0.55
cand = []
S = score.copy()
while True:
    i = np.unravel_index(np.argmax(S), S.shape)
    if S[i] < thr: break
    cand.append((i[1] + u0, i[0] + v0, S[i], ringv[i], holev[i]))
    S[max(0, i[0]-15):i[0]+16, max(0, i[1]-15):i[1]+16] = -1
for c in cand:
    print(f"u={c[0]} v={c[1]} score={c[2]:.2f} ring={c[3]:.2f} hole={c[4]:.2f}")
