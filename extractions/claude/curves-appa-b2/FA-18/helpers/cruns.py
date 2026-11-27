"""Claude reader helper (FA-18): along page rows (mode r: fixed v, u range) or along iso-percent lines
(mode p: fixed percent, v range), the runs of curve ink, where runs separated only by grid ink (g) are
joined and marked with * (the curve may continue under the grid line), and runs bordering grid ink on
a side are marked with < or > (that edge may be hidden)."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import geom, scanline as sl  # noqa: E402


def runs(seq):
    """seq: list of (t, cls). Returns [(t0, t1, joined, hid_lo, hid_hi)] of C runs joined across g."""
    out = []
    i, n = 0, len(seq)
    while i < n:
        if seq[i][1] != "C":
            i += 1; continue
        j = i
        joined = False
        while True:
            while j + 1 < n and seq[j + 1][1] == "C":
                j += 1
            k = j + 1
            while k < n and seq[k][1] == "g":
                k += 1
            if k < n and k > j + 1 and seq[k][1] == "C" and (k - j - 1) <= 10:
                j = k; joined = True
                continue
            break
        lo = i > 0 and seq[i - 1][1] == "g"
        hi = j + 1 < n and seq[j + 1][1] == "g"
        out.append((seq[i][0], seq[j][0], joined, lo, hi))
        i = j + 1
    return out


def fmt(r):
    a, b, jn, lo, hi = r
    return f"{'<' if lo else ''}{a:.0f}-{b:.0f}{'>' if hi else ''}{'*' if jn else ''}"


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "r":
        u0, u1 = int(sys.argv[2]), int(sys.argv[3])
        v0, v1, st = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
        for v in range(v0, v1, st):
            seq = [(u, sl.cls(u, v)) for u in range(u0, u1)]
            print(v, " ".join(fmt(r) for r in runs(seq) if r[1] - r[0] >= 2))
    else:
        v0, v1 = int(sys.argv[2]), int(sys.argv[3])
        for p in [float(x) for x in sys.argv[4].split(",")]:
            c, k = geom.iso_p(p)
            seq = [(v, sl.cls(c + k * v, v)) for v in range(v0, v1)]
            print(f"p={p:5.1f} u~{c + k * (v0 + v1) / 2:7.1f}:", " ".join(fmt(r) for r in runs(seq) if r[1] - r[0] >= 2))
