"""Check every trace sample of a curve batch against CURVE-READING.md rule 7 (D-031): a trace sample is on
its drawn line's own ink, never on a plotted symbol or in the white gap between a dash and a symbol.

Usage:
    python tools/check_trace_ink.py <batch> [<batch> ...]

Writes qa/<batch>/ink-checks.csv, one row per trace sample of both readings (rederived points), with a
verdict:
  eligible   the line's own ink (page ink minus symbol ink minus grid lines) is within 2 px
  excluded   the sample is inside a plotted symbol's footprint, or the line's own ink is more than 2 px away
  review     the verdict changes with how far the symbol's ink is taken to reach (2, 3 or 4 px beyond its
             fitted outline), or it rests on a symbol only one reader recorded where the other reader
             recorded symbols in that panel
Shadow mode: nothing else reads this file yet (D-031 validation first). Passing the check confers no
agreement or verification; it only says the sample is not shown to be off its line.

Method (Codex's ownership design, D-031, as frozen on 2026-10-28 after development on the 2026-10-27
adjudicated set; parameters below are not to be tuned to the validation sample):
1. Page ink is the dark level of the bilevel page; grid lines and frame are straight horizontal or vertical
   runs of at least 400 px, removed (dilated 1 px) before anything else.
2. Every marker of either reading (merged within 4 px) gets a symbol template fitted to the ink: shape from
   the reading, outer size 14 to 36 px, stroke 3 to 8 px, center offset up to 3 px; the score is the ink
   coverage of the template's stroke minus 0.7 x the ink in a closed shape's interior minus 0.5 x the ink
   in a ring 2 to 4 px outside it (a too-small template leaves the symbol's arms there). A first pass over
   the panel gives each shape's median size among clean fits (score >= 0.75, at least 3); the second pass
   keeps each fit within 6 px of it. Stroke symbols (x, plus, six-armed asterisk) occupy their disk.
3. A symbol's ink is all ink connected to its fitted stroke within `grow` px of its footprint (arm tips,
   corner flares, line ink fused onto the outline). The verdict is taken at grow 3 and checked at 2 and 4.
"""
import argparse
import csv
import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
H = 26                      # half window of a symbol template, px
SIZES = range(14, 37)       # symbol outer size, px
STROKES = (3, 4, 5, 6, 7, 8)
OFF = range(-3, 4)
GRID_RUN = 400              # a straight run of ink this long is a grid line or the frame
PRIOR_SCORE, PRIOR_N, PRIOR_HALF = 0.75, 3, 6
GROWS = (2, 3, 4)           # how far a symbol's connected ink reaches beyond its outline; verdict at 3
LINE_PX = 2.0               # rule 7 / round 2 convention 1: on the line's ink or within 2 px of it
MERGE_PX = 4                # two readings' markers of different tests this close are one symbol
MERGE_SAME_PX = 10          # of the same test: the readings' centers differ by up to a triangle's height/6 and more

NEAR_PX = 40                # markers considered around a sample
CROSS_PX, CROSS_SPREAD = 10, 135   # a curve crossing a grid line has own ink on two sides at least this far apart (deg)
PARAMS = dict(method="D-031 v1 2026-10-28", H=H, sizes=[SIZES.start, SIZES.stop - 1], strokes=list(STROKES), off=[OFF.start, OFF.stop - 1],
              grid_run=GRID_RUN, prior=[PRIOR_SCORE, PRIOR_N, PRIOR_HALF], grows=list(GROWS), line_px=LINE_PX,
              merge_px=[MERGE_PX, MERGE_SAME_PX], cross=[CROSS_PX, CROSS_SPREAD], weights={"core": 0.7, "ring": 0.5, "ring_px": [2, 4]})
SHAPE = {"circle": "circle", "circle-dot": "circle", "dotted circle": "circle", "quarter-circle": "circle",
         "filled circle": "filled circle", "square": "square", "square with x": "square", "diamond": "diamond",
         "triangle-up": "triangle-up", "dotted triangle": "triangle-up", "triangle-down": "triangle-down",
         "x": "x", "plus": "plus", "asterisk": "asterisk", "star": "asterisk"}


def load(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def dilate(m, n=1):
    for _ in range(n):
        o = m.copy()
        o[1:, :] |= m[:-1, :]; o[:-1, :] |= m[1:, :]; o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]
        o[1:, 1:] |= m[:-1, :-1]; o[:-1, :-1] |= m[1:, 1:]; o[1:, :-1] |= m[:-1, 1:]; o[:-1, 1:] |= m[1:, :-1]
        m = o
    return m


def runs_mask(a, L):
    out = np.zeros_like(a)
    for i, row in enumerate(a):
        d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
        for a0, a1 in zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]):
            if a1 - a0 >= L:
                out[i, a0:a1] = True
    return out


def seg_dist(X, Y, a, b):
    (ax, ay), (bx, by) = a, b
    vx, vy = bx - ax, by - ay
    t = np.clip(((X - ax) * vx + (Y - ay) * vy) / (vx * vx + vy * vy), 0, 1)
    return np.hypot(X - (ax + t * vx), Y - (ay + t * vy))


def poly_inside(X, Y, pts):
    inside = np.zeros_like(X, dtype=bool)
    for i in range(len(pts)):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
        inside ^= ((y1 > Y) != (y2 > Y)) & (X < (x2 - x1) * (Y - y1) / (y2 - y1 + 1e-12) + x1)
    return inside


@lru_cache(maxsize=None)
def template(shape, s, t):
    """(stroke, footprint, interior core) masks, (2H+1)^2, centered, for a symbol of outer size s, stroke t."""
    Y, X = np.mgrid[-H:H + 1, -H:H + 1].astype(float)
    r = s / 2.0
    if shape in ("circle", "filled circle"):
        d = np.hypot(X, Y)
        band = ((d <= r) & (d >= r - t)) if shape == "circle" else d <= r
        core = (d <= r - t - 1.5) if shape == "circle" else np.zeros_like(band)
        return band, d <= r + 1, core
    if shape in ("square", "diamond"):
        d = np.maximum(abs(X), abs(Y)) if shape == "square" else (abs(X) + abs(Y)) / 1.414
        return (d <= r) & (d >= r - t), d <= r + 1, d <= r - t - 1.5
    if shape in ("triangle-up", "triangle-down"):
        h, sg = s * 0.95, (1 if shape == "triangle-up" else -1)
        pts = [(0, -sg * h / 2), (-r, sg * h / 2), (r, sg * h / 2)]
        ins = poly_inside(X, Y, pts)
        dist = np.minimum.reduce([seg_dist(X, Y, pts[i], pts[(i + 1) % 3]) for i in range(3)])
        return (ins & (dist <= t)) | (dist <= 0.5), ins | (dist <= 1), ins & (dist > t + 1.5)
    segs = {"x": [((-r * .707, -r * .707), (r * .707, r * .707)), ((-r * .707, r * .707), (r * .707, -r * .707))],
            "plus": [((-r, 0), (r, 0)), ((0, -r), (0, r))],
            "asterisk": [((0, -r), (0, r)), ((-r * .866, -r * .5), (r * .866, r * .5)), ((-r * .866, r * .5), (r * .866, -r * .5))]}[shape]
    d = np.minimum.reduce([seg_dist(X, Y, a, b) for a, b in segs])
    return d <= t / 2, np.hypot(X, Y) <= r + 1, np.zeros(X.shape, bool)


@lru_cache(maxsize=None)
def ring_of(shape, s, t):
    _, foot, _ = template(shape, s, t)
    return dilate(foot, 4) & ~dilate(foot, 1)


class Panel:
    """One panel of one figure: the page's ink without grid lines, the markers of both readings, their fits."""

    def __init__(self, ink, markers, grid):
        self.ink, self.markers, self._fits, self.grid = ink, markers, {}, grid
        # a symbol only one reader recorded is uncertain only if the other reader recorded symbols here at all
        # (the pilot's Claude reading of FC-1B's upper panel has traces and no markers)
        self.marker_readers = {r for m in markers for r in m["readers"]}
        self.prior = {}
        by = {}
        for m in markers:
            sc, (sz, *_r) = self._fit(m, None)
            if sc >= PRIOR_SCORE:
                by.setdefault(m["shape"], []).append(sz)
        self.prior = {k: int(np.median(v)) for k, v in by.items() if len(v) >= PRIOR_N}

    def _fit(self, m, sizes):
        U, V, best = int(round(m["u"])), int(round(m["v"])), (-9.0, None)
        for du in OFF:
            for dv in OFF:
                win = self.ink[V + dv - H:V + dv + H + 1, U + du - H:U + du + H + 1]
                if win.shape != (2 * H + 1, 2 * H + 1):
                    continue
                for s in (sizes or SIZES):
                    for t in STROKES:
                        band, foot, core = template(m["shape"], s, t)
                        sc = win[band].mean() - (0.7 * win[core].mean() if core.any() else 0) - 0.5 * win[ring_of(m["shape"], s, t)].mean()
                        if sc > best[0]:
                            best = (sc, (s, t, du, dv))
        return best

    def fit(self, m):
        k = id(m)
        if k not in self._fits:
            pr = self.prior.get(m["shape"])
            self._fits[k] = self._fit(m, range(max(SIZES.start, pr - PRIOR_HALF), pr + PRIOR_HALF + 1) if pr else None)
        return self._fits[k]

    def classify(self, u, v, R=NEAR_PX):
        near = [m for m in self.markers if abs(m["u"] - u) < R and abs(m["v"] - v) < R]
        U0, V0 = int(round(u)), int(round(v))
        win = self.ink[V0 - R:V0 + R + 1, U0 - R:U0 + R + 1]
        if win.shape != (2 * R + 1, 2 * R + 1):
            return "review", "too close to the page edge", "", 99.0
        placed = []
        for m in near:
            sc, (s, t, du, dv) = self.fit(m)
            band, foot, _ = template(m["shape"], s, t)
            cu, cv = int(round(m["u"])) + du - U0 + R, int(round(m["v"])) + dv - V0 + R
            B, F = np.zeros_like(win), np.zeros_like(win)
            for src, dst in ((band, B), (foot, F)):
                ys, xs = np.nonzero(src)
                ys, xs = cv + ys - H, cu + xs - H
                ok = (ys >= 0) & (ys <= 2 * R) & (xs >= 0) & (xs <= 2 * R)
                dst[ys[ok], xs[ok]] = True
            placed.append((m, s, t, sc, B, F))
        verdicts = []
        cy, cx = R + int(round(v - V0)), R + int(round(u - U0))
        for grow in GROWS:
            sym, inside, on_stroke = np.zeros_like(win), None, False
            for m, s, t, sc, B, F in placed:
                # the symbol's ink grows from its stroke over connected ink, but not into a closed symbol's
                # interior: a line drawn through an open symbol keeps its own ink there (Codex's design, D-031)
                interior = F & ~dilate(B, 1)
                region, g = dilate(F, grow) & ~interior & win, B & win
                for _ in range(grow + 8):
                    n = dilate(g, 1) & region
                    if (n == g).all():
                        break
                    g = n
                sym |= g
                if F[cy, cx] and inside is None:
                    inside, on_stroke = m, bool(dilate(B, 1)[cy, cx])
            ys, xs = np.nonzero(win & ~sym)
            if inside is not None:
                near_line = len(xs) and float(np.hypot(xs - (R + (u - U0)), ys - (R + (v - V0))).min()) <= LINE_PX
                if on_stroke:
                    verdicts.append(("excluded", inside, f"on the stroke of {inside['label']}", 0.0))
                elif near_line:
                    verdicts.append(("review", inside, f"inside {inside['label']}, on line ink through its interior", 0.0))
                else:
                    verdicts.append(("excluded", inside, f"inside {inside['label']}, white interior", 0.0))
                continue
            dx, dy = xs - (R + (u - U0)), ys - (R + (v - V0))
            dist = np.hypot(dx, dy)
            d = float(dist.min()) if len(xs) else 99.0
            if d > LINE_PX:
                # removing the grid cuts a hole in a curve where it crosses a grid line: a sample on grid ink with
                # the curve's own ink on two opposite sides (3 to 10 px out) is on a curve crossing the line;
                # on grid ink without that, the curve may run along the grid line: review, never exclude
                gy, gx = np.nonzero(self.grid[V0 - R:V0 + R + 1, U0 - R:U0 + R + 1])
                dg = float(np.hypot(gx - (R + (u - U0)), gy - (R + (v - V0))).min()) if len(gx) else 99.0
                if dg <= LINE_PX:
                    sel = (dist >= 3) & (dist <= CROSS_PX)
                    ang = np.sort(np.degrees(np.arctan2(dy[sel], dx[sel])) % 360) if sel.any() else np.array([])
                    gap = np.max(np.diff(np.concatenate((ang, ang[:1] + 360)))) if len(ang) > 1 else 360.0
                    if len(ang) > 1 and 360.0 - gap >= CROSS_SPREAD:
                        verdicts.append(("eligible", None, f"on a grid line the curve crosses (own ink {d:.1f} px)", d)); continue
                    verdicts.append(("review", None, f"on a grid line, own line ink {d:.1f} px away", d)); continue
            verdicts.append(("excluded" if d > LINE_PX else "eligible", None, f"own line ink {d:.1f} px away", d))
        kind, m, why, d = verdicts[GROWS.index(3)]
        if kind == "review":
            return "review", why, (m["label"] if m else ""), d
        if len({x[0] for x in verdicts}) > 1:
            return "review", "; ".join(f"grow {g}: {x[0]} ({x[2]})" for g, x in zip(GROWS, verdicts)), "", d
        if kind == "excluded" and m is not None and len(m["readers"]) == 1 and self.marker_readers - set(m["readers"]):
            return "review", f"{why}, a symbol only {m['readers'][0]} recorded", m["label"], d
        return kind, why, (m["label"] if m else ""), d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batches", nargs="+")
    a = ap.parse_args()
    phash = hashlib.sha256(json.dumps(PARAMS, sort_keys=True).encode()).hexdigest()[:12]
    for batch in a.batches:
        q = ROOT / "qa" / batch
        rows, pages = [], {}
        renamed = {(r["figure_id"], r["submitted"]): r["series_id"] for r in load(q / "series-ids.csv")} if (q / "series-ids.csv").exists() else {}
        for ov in load(q / "overlays.csv"):
            fid, panel = ov["figure_id"], ov["panel"]
            pts = {}
            for reader in ("claude", "codex"):
                p = q / "rederived" / reader / fid / f"points-p{panel}-native.csv"
                pts[reader] = load(p) if p.exists() else []
            if not any(r["point_kind"] == "trace" for L in pts.values() for r in L):
                continue
            if ov["image"] not in pages:
                raw = np.asarray(Image.open(ROOT / ov["image"]).convert("L")) < 128
                grid = runs_mask(raw, GRID_RUN) | runs_mask(raw.T, GRID_RUN).T
                g1 = dilate(grid, 1)
                pages[ov["image"]] = (raw & ~g1, raw & g1, hashlib.sha256((ROOT / ov["image"]).read_bytes()).hexdigest()[:12])
            ink, grid, ihash = pages[ov["image"]]
            markers = []
            for reader, L in pts.items():
                for r in L:
                    if r["point_kind"] != "marker":
                        continue
                    u, v = float(r["pixel_u"]), float(r["pixel_v"])
                    sid = renamed.get((fid, r["series_id"]), r["series_id"])
                    hit = next((m for m in markers if max(abs(m["u"] - u), abs(m["v"] - v)) <= (MERGE_SAME_PX if m["series"] == sid else MERGE_PX)), None)
                    if hit:
                        if reader not in hit["readers"]:
                            hit["readers"].append(reader)
                        continue
                    shape = SHAPE.get(r["symbol"], "circle")
                    markers.append({"u": u, "v": v, "shape": shape, "readers": [reader], "series": sid,
                                    "label": f"{r['symbol'] or 'symbol'} of {r['series_id']} at ({u:.0f},{v:.0f})"})
            P = Panel(ink, markers, grid)
            for reader, L in pts.items():
                for r in L:
                    if r["point_kind"] != "trace":
                        continue
                    verdict, why, sym, d = P.classify(float(r["pixel_u"]), float(r["pixel_v"]))
                    rows.append({"figure_id": fid, "panel": panel, "reader": reader, "series_id": r["series_id"],
                                 "point_kind": "trace", "sequence": r["sequence"], "pixel_u": r["pixel_u"],
                                 "pixel_v": r["pixel_v"], "verdict": verdict, "line_ink_px": f"{d:.1f}",
                                 "symbol": sym, "reason": why, "image_sha": ihash, "params": phash})
        fields = ["figure_id", "panel", "reader", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
                  "verdict", "line_ink_px", "symbol", "reason", "image_sha", "params"]
        with open(q / "ink-checks.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)
        from collections import Counter
        c = Counter(r["verdict"] for r in rows)
        print(f"{batch}: {len(rows)} trace samples: " + ", ".join(f"{k} {c[k]}" for k in ("eligible", "excluded", "review")) + f" (params {phash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
