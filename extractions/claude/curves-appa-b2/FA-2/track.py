"""Strand tracking aid for FA-2: follows one drawn curve column by column (shallow stretches) or
row by row (steep stretches) from the reader's rough seed points, and reports where the stroke's
ink lies, with a flag for every column or row. A reading aid: the reader checks every result on
overlays of the page and decides what is kept.

A stroke's centre is taken from its ink edges: the middle of a clean run (white on both sides, not
on a printed grid line); where the run merges with a grid line or with another strand, from its one
clean edge and the stroke's thickness; nothing where neither edge is clean.

Grid lines are predicted from reference stretches free of curves: horizontal lines from columns
u 1995..2015 (v 1380..1900) and u 735..760 (v 1650..3720), vertical lines from rows v 1150..1300,
each converted to its grain size or percent through the reader's calibration (cal-p1) and mapped
back at the column or row where it is needed.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fa2_tools as T  # noqa: E402

DARK = T.GRAY < 128
THICK = 10.0   # stroke thickness across the line, px (measured on clean stretches: 9.5 to 11)


def ref_runs(axis_cols, lo, hi, vertical):
    """runs dark in at least half of the reference columns (or rows)."""
    if vertical:   # horizontal grid lines: look down columns
        block = DARK[lo:hi + 1, axis_cols[0]:axis_cols[1] + 1]
        frac = block.mean(axis=1)
    else:
        block = DARK[axis_cols[0]:axis_cols[1] + 1, lo:hi + 1]
        frac = block.mean(axis=0)
    on = frac >= 0.5
    d = np.diff(np.concatenate(([0], on.astype(np.int8), [0])))
    s, e = np.where(d == 1)[0], np.where(d == -1)[0]
    return [(lo + a, lo + b - 1) for a, b in zip(s, e)]


def build_grid():
    rows = []
    for (c0, c1), (v0, v1) in (((1995, 2015), (1380, 1900)), ((735, 760), (1650, 3720))):
        uc = 0.5 * (c0 + c1)
        for a, b in ref_runs((c0, c1), v0, v1, True):
            rows.append((T.X.value(uc, a - 0.5)[0], T.X.value(uc, b + 0.5)[0]))
    cols = []
    vr = 1225.0
    for a, b in ref_runs((1150, 1300), 660, 2190, False):
        cols.append((T.Y.value(a - 0.5, vr)[0], T.Y.value(b + 0.5, vr)[0]))
    return rows, cols


GRID_ROWS, GRID_COLS = build_grid()


_UREF = (600.0, 1400.0, 2200.0)
_VREF = (1100.0, 2400.0, 3700.0)
_ROWS_AT = [[(min(T.v_of_grain(g0, u), T.v_of_grain(g1, u)), max(T.v_of_grain(g0, u), T.v_of_grain(g1, u)))
             for g0, g1 in GRID_ROWS] for u in _UREF]
_COLS_AT = [[(min(T.u_of_pct(p0, v), T.u_of_pct(p1, v)), max(T.u_of_pct(p0, v), T.u_of_pct(p1, v)))
             for p0, p1 in GRID_COLS] for v in _VREF]


def _lerp(tab, refs, x):
    out = []
    for i in range(len(tab[0])):
        a = [np.interp(x, refs, [tab[k][i][0] for k in range(len(refs))])]
        b = [np.interp(x, refs, [tab[k][i][1] for k in range(len(refs))])]
        out.append((float(a[0]), float(b[0])))
    return out


def grid_rows_at(u):
    """the horizontal grid lines' v extents at column u (each a straight line between three references)."""
    return _lerp(_ROWS_AT, _UREF, u)


def grid_cols_at(v):
    return _lerp(_COLS_AT, _VREF, v)


def runs_1d(line, off):
    d = np.diff(np.concatenate(([0], line.astype(np.int8), [0])))
    s, e = np.where(d == 1)[0], np.where(d == -1)[0]
    return [(int(off + a), int(off + b - 1)) for a, b in zip(s, e)]


def on_grid(x, grid):
    return any(g0 - 1.5 <= x <= g1 + 1.5 for g0, g1 in grid)


def interp_seeds(seeds, t, along):
    """seed polyline position across the stroke at coordinate `t` along the scan direction."""
    S = sorted(seeds, key=lambda p: p[0] if along == "u" else p[1])
    ts = [p[0] if along == "u" else p[1] for p in S]
    xs = [p[1] if along == "u" else p[0] for p in S]
    return float(np.interp(t, ts, xs)), float(np.interp(t + 1, ts, xs) - np.interp(t - 1, ts, xs)) / 2


def track(seeds, t0, t1, mode, tol=7.0, win=16):
    """mode 'col': scan columns u = t0..t1, stroke centre in v. mode 'row': rows v = t0..t1, centre in u."""
    res = []
    for t in range(int(t0), int(t1) + 1):
        pred, slope = interp_seeds(seeds, t, "u" if mode == "col" else "v")
        h = THICK * np.sqrt(1 + slope ** 2)          # extent of the stroke along the scan line
        if mode == "col":
            line = DARK[:, t]
            grid = grid_rows_at(t)
        else:
            line = DARK[t, :]
            grid = grid_cols_at(t)
        lo, hi = int(pred - 40), int(pred + 40)
        seg = line[lo:hi + 1]
        if seg[int(40 - 25):int(40 + 26)].mean() >= 0.85:
            res.append((t, None, "cross-grid", None))
            continue
        cands = []
        for a, b in runs_1d(seg, lo):
            if b < pred - win or a > pred + win:
                continue
            ln = b - a + 1
            top_ok = not line[a - 1] and not on_grid(a, grid)
            bot_ok = not line[b + 1] and not on_grid(b, grid)
            if h - 3 <= ln <= h + 4 and top_ok and bot_ok:
                cands.append((0.5 * (a + b), "clean", (a, b)))
            elif ln > h + 4:
                if top_ok:
                    cands.append((a + (h - 1) / 2, "edge-low", (a, b)))
                if bot_ok:
                    cands.append((b - (h - 1) / 2, "edge-high", (a, b)))
                if not top_ok and not bot_ok:
                    cands.append((0.5 * (a + b), "merged", (a, b)))
            else:
                flag = "partial" if top_ok and bot_ok else "partial-grid"
                cands.append((0.5 * (a + b), flag, (a, b)))
        cands = [c for c in cands if abs(c[0] - pred) <= tol]
        if not cands:
            res.append((t, None, "no-ink", None))
            continue
        c = min(cands, key=lambda c: abs(c[0] - pred))
        res.append((t, round(float(c[0]), 1), c[1], [int(c[2][0]), int(c[2][1])]))
    return res


if __name__ == "__main__" and sys.argv[1] != "overlay":
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = {}
    for name, spec in cfg.items():
        r = track(spec["seeds"], spec["t0"], spec["t1"], spec["mode"], spec.get("tol", 7.0))
        out[name] = r
        good = [x for x in r if x[2] in ("clean", "edge-low", "edge-high")]
        print(f"{name}: {len(r)} lines, {len(good)} read; flags " +
              ", ".join(f"{f}={sum(1 for x in r if x[2] == f)}" for f in sorted(set(x[2] for x in r))))
    Path(sys.argv[2]).write_text(json.dumps(out), encoding="utf-8")


COLORS = {"lower": (230, 0, 0), "average": (0, 160, 0), "upper": (0, 0, 230)}


def overlay(trk, box, out, zoom=3, extra=None):
    from PIL import Image, ImageDraw
    u0, v0, u1, v1 = box
    im = Image.open(T.IMG).convert("RGB").crop(box).resize(((u1 - u0) * zoom, (v1 - v0) * zoom), Image.NEAREST)
    # grey the page so marks stand out
    a = np.asarray(im).copy()
    a[a[:, :, 0] < 128] = (110, 110, 110)
    a[a[:, :, 0] >= 128] = (255, 255, 255)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    for uu in range((u0 // 25 + 1) * 25, u1, 25):
        d.line([((uu - u0) * zoom, 0), ((uu - u0) * zoom, im.height)], fill=(255, 200, 200))
        if uu % 100 == 0:
            d.text(((uu - u0) * zoom + 2, 2), str(uu), fill=(200, 0, 0))
    for vv in range((v0 // 25 + 1) * 25, v1, 25):
        d.line([(0, (vv - v0) * zoom), (im.width, (vv - v0) * zoom)], fill=(200, 200, 255))
        if vv % 100 == 0:
            d.text((2, (vv - v0) * zoom + 2), str(vv), fill=(0, 0, 200))
    for name, rows in trk.items():
        base = name.split(":")[0]
        col = COLORS.get(base, (200, 0, 200))
        mode = "row" if name.endswith(":row") else "col"
        for t, c, flag, run in rows:
            if c is None:
                continue
            u, v = (t, c) if mode == "col" else (c, t)
            x, y = (u - u0) * zoom, (v - v0) * zoom
            if flag == "clean":
                d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=col)
            elif flag.startswith("edge"):
                d.rectangle([x - 2, y - 2, x + 2, y + 2], outline=col)
            else:
                d.line([x - 2, y - 2, x + 2, y + 2], fill=col)
    for (u, v, col) in (extra or []):
        x, y = (u - u0) * zoom, (v - v0) * zoom
        d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=col, width=2)
    im.save(out)
    print(f"wrote {out}")


if __name__ == "__main__" and sys.argv[1] == "overlay":
    trk = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    box = [int(x) for x in sys.argv[3:7]]
    overlay(trk, box, sys.argv[7], int(sys.argv[8]) if len(sys.argv) > 8 else 3)
