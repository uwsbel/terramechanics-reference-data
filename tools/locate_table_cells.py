"""Find where each cell of a transcribed table sits on its scan, for the reviewer audit packets (roadmap 6g, D-050).

Usage:
    python tools/locate_table_cells.py <batch> [--qa-root qa] [--overlay-dir work/table-layout]
    python tools/locate_table_cells.py --probe <image> <rotation> <rows> <columns>   # a page not yet transcribed

A table batch (qa/<batch>/) holds agreed.csv, the cells two blind transcriptions agreed on (tools/diff_tables.py),
and audit-meta.json, written by hand, with one entry per table: `kind` "table", `image` (the page scan), `rotation`
(clockwise degrees that turn the scan upright, as corpus figures.csv), `key` (the column naming a row, such as
run_number) and `columns`, every printed column from left to right as [name, heading as printed], the key first.
The rows are taken in the order both readings list them (extractions/<agent>/<batch>/table.csv, in printed order):
agreed.csv is sorted by diff_tables and need not follow the page, so the two readings must agree on the order, with
no key twice, over the keys of agreed.csv (Codex's review, 2026-11-21).

The scan is turned upright, then straightened by the small angle (within 1.5 degrees) that makes the table's text
rows sharpest (the projection of the ink onto the vertical axis has the largest variance), measured on the table's
own region, the extent of its long vertical lines: on pages with heavy black bars along an edge the whole page would
align the bars. The thirteen drag tables (Figs. 4-6a to 4-16) are 0.05 to 1.2 degrees off, Table 5-T3 0.8, which over
a 3,000 px row is up to 60 px. In that frame the column rules are the long vertical lines (broken prints included),
the frame and the rule under the header the rows inked across most of the table, and the printed rows the bands of
ink in the key column between the header rule and the bottom frame: a stray mark, an annotation or a speck in the
empty part of a short table elsewhere cannot add or join a row there. A band about twice the usual height is split at
its faintest rows; a thin or nearly empty band is dropped. The tool stops, writing nothing, unless it finds exactly
one band per row and one column per entry of `columns`; a matching count is not proof, so the overlay is looked at.
All thirteen drag tables pass the probe with their indexed run counts (2026-11-21).

Writes qa/<batch>/cell-layout.csv, one row per box: figure_id, key, column, role (cell, key: the row's key cell,
header: a column's heading), x0 y0 x1 y1 (the box in the upright, straightened frame, which make_audit_packet.py
rebuilds from rotation and deskew_deg to crop its pictures), u v (the box center on the scan as stored) and bu bv
(half its width and height there, for the viewer), deskew_deg. And <overlay-dir>/<figure>-layout.png, the boxes
drawn on the straightened page, which a person looks at before the layout is used. Nothing here edits data/.
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
INK = 128          # a pixel darker than mid-gray is ink (the scans are bilevel)
EDGE = 80          # lines this close to the page edge are the scan's border, not the table's
FIELDS = ["figure_id", "key", "column", "role", "x0", "y0", "x1", "y1", "u", "v", "bu", "bv", "deskew_deg"]


def upright(img, rotation):
    """The scan turned upright: figures.csv gives clockwise degrees and Pillow turns counter-clockwise."""
    return img.rotate(-rotation, expand=True) if rotation else img.copy()


def straighten(img, angle):
    """The upright page turned by angle degrees counter-clockwise about its center, the same size, white fill."""
    return img.rotate(angle, resample=Image.BILINEAR, center=(img.width / 2, img.height / 2), fillcolor=255) if angle else img


def to_upright(x, y, size, angle):
    """A point of the straightened frame in the upright frame (the inverse of straighten; size = upright size)."""
    if not angle:
        return x, y
    cx, cy, t = size[0] / 2, size[1] / 2, math.radians(angle)
    dx, dy = x - cx, y - cy
    # straighten turns counter-clockwise as seen on screen (y down): a point d goes to (dx cos + dy sin, -dx sin + dy cos)
    return cx + dx * math.cos(t) - dy * math.sin(t), cy + dx * math.sin(t) + dy * math.cos(t)


def to_scan(x, y, scan_size, rotation):
    """A point of the upright frame on the scan as stored (scan_size = the scan's width, height)."""
    w, h = scan_size
    r = rotation % 360
    if r == 0:
        return x, y
    if r == 90:     # upright (x, y) = (h - 1 - v, u)
        return y, h - 1 - x
    if r == 180:
        return w - 1 - x, h - 1 - y
    if r == 270:    # upright (x, y) = (v, w - 1 - u)
        return w - 1 - y, x
    raise ValueError(f"rotation {rotation}: only multiples of 90 are handled")


def deskew_angle(gray, lo=-1.5, hi=1.5, step=0.05):
    """The angle (degrees, counter-clockwise) that makes the text rows sharpest, searched on a half-size copy."""
    small = gray.resize((gray.width // 2, gray.height // 2))
    best = (-1.0, 0.0)
    for k in range(int(round((hi - lo) / step)) + 1):
        a = lo + k * step
        ink = np.asarray(straighten(small, a)) < INK
        prof = ink.sum(axis=1).astype(float)
        best = max(best, (float(np.var(prof)), round(a, 3)))
    return best[1]


def longest_runs(m, where=False):
    """The longest run of True in each row of a boolean array (with where=True, also its start and end)."""
    out, se = np.zeros(m.shape[0], int), np.zeros((m.shape[0], 2), int)
    for i, row in enumerate(m):
        if row.any():
            d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
            s, e = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
            j = int(np.argmax(e - s))
            out[i], se[i] = e[j] - s[j], (s[j], e[j])
    return (out, se) if where else out


def table_region(ink):
    """(x0, y0, x1, y1): the extent of the long vertical lines away from the page edge, the table's own region, or None.
    The skew is measured there: on pages with heavy black bars along an edge (Figs. 4-10 and 4-13), the whole page's
    sharpest angle aligns the bars, not the table (Codex's review, 2026-11-21)."""
    H, W = ink.shape
    vr, se = longest_runs(ink.T, where=True)
    lines = [g for g in groups(np.flatnonzero(vr > 300), gap=12) if g[0] > EDGE and g[1] < W - EDGE]
    if len(lines) < 2:
        return None
    runs = [se[s + int(np.argmax(vr[s:e + 1]))] for s, e in lines]
    return lines[0][0], int(min(r[0] for r in runs)), lines[-1][1], int(max(r[1] for r in runs))


def groups(idx, gap):
    out = []
    for i in idx:
        if out and i - out[-1][1] <= gap:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [tuple(g) for g in out]


def find_layout(ink, n_rows, n_cols):
    """(vertical rules, (top, header, bottom) rules, row bands) of the table in a straightened page, or an error."""
    H, W = ink.shape
    vr = longest_runs(ink.T)
    vlines = [g for g in groups(np.flatnonzero(vr > 300), gap=12) if g[0] > EDGE and g[1] < W - EDGE]
    if len(vlines) != n_cols + 1:
        return None, f"found {len(vlines)} column rules, expected {n_cols + 1}: {vlines}"
    x0, x1 = vlines[0][0], vlines[-1][1]
    frac = ink[:, x0:x1 + 1].mean(axis=1)
    hlines = [g for g in groups(np.flatnonzero(frac > 0.5), gap=2) if g[0] > EDGE and g[1] < H - EDGE]
    if len(hlines) < 3:
        return None, f"found {len(hlines)} horizontal rules across the table, expected the frame and the header rule: {hlines}"
    top, header, bottom = hlines[0], hlines[1], hlines[-1]
    # the printed rows are read from the key column alone (the run numbers): a stray mark, an annotation or a speck in
    # the empty part of a short table elsewhere cannot add or join a row there (Figs. 4-6c and 4-7, Codex's review)
    y_lo, y_hi = header[1] + 1, bottom[0]
    prof = ink[y_lo:y_hi, vlines[0][1] + 6:vlines[1][0] - 6].sum(axis=1)
    bands = [(s + y_lo, e + y_lo) for s, e in groups(np.flatnonzero(prof > 1), gap=3)]
    if not bands:
        return None, "no printed rows in the key column between the header rule and the bottom frame"
    heights = [e - s + 1 for s, e in bands]
    med = float(np.median([h for h in heights if h >= 12] or heights))   # specks do not set the scale
    mass = float(np.median([prof[s - y_lo:e - y_lo + 1].sum() for s, e in bands if e - s + 1 >= 12] or [1]))
    bands = [(s, e) for s, e in bands if e - s + 1 >= 0.4 * med and prof[s - y_lo:e - y_lo + 1].sum() >= 0.15 * mass]
    out = []
    for s, e in bands:
        k = round((e - s + 1) / med) if (e - s + 1) >= 1.6 * med else 1
        if k >= 2:   # rows joined by a stray mark or a descender: cut at the faintest rows near each expected break
            cuts, seg = [], prof[s - y_lo:e - y_lo + 1]
            for j in range(1, k):
                c = round(j * len(seg) / k)
                lo, hi = max(c - int(med / 2), 1), min(c + int(med / 2), len(seg) - 1)
                cuts.append(lo + int(np.argmin(seg[lo:hi])))
            edges = [0] + cuts + [len(seg)]
            out += [(s + edges[j], s + edges[j + 1] - 1) for j in range(k)]
        else:
            out.append((s, e))
    if len(out) != n_rows:
        return None, f"found {len(out)} printed rows, expected {n_rows}: {out}"
    return (vlines, (top, header, bottom), out), ""


def measure(scan, rotation, n_rows, n_cols):
    """(upright page, deskew angle, straightened page, layout or None, error) for one table scan."""
    up = upright(scan, rotation)
    reg = table_region(np.asarray(up) < INK)
    if reg is None:
        return up, 0.0, up, None, "no table frame found (fewer than two long vertical lines)"
    x0, y0, x1, y1 = reg
    m = 40
    angle = deskew_angle(up.crop((max(x0 - m, 0), max(y0 - m, 0), min(x1 + m, up.width), min(y1 + m, up.height))))
    st = straighten(up, angle)
    layout, err = find_layout(np.asarray(st) < INK, n_rows, n_cols)
    return up, angle, st, layout, err


def printed_order(batch, key, agreed_keys):
    """The row keys in printed order, from the two blind readings (each lists its rows as printed): agreed.csv is
    sorted by diff_tables and need not follow the page (Codex's review, 2026-11-21). Both readings must give the same
    order, without duplicates, over the same keys as agreed.csv; otherwise nothing is located."""
    orders = []
    for who in ("claude", "codex"):
        p = ROOT / "extractions" / who / batch / "table.csv"
        if not p.exists():
            sys.exit(f"{batch}: {p.relative_to(ROOT)} missing; the printed row order comes from both readings")
        orders.append([r[key] for r in csv.DictReader(p.open(encoding="utf-8-sig", newline=""))])
    a, b = orders
    if len(set(agreed_keys)) != len(agreed_keys):
        sys.exit(f"{batch}: a row key appears twice in agreed.csv")
    if a != b:
        sys.exit(f"{batch}: the two readings list the rows in different orders; settle the order before locating")
    if len(set(a)) != len(a):
        sys.exit(f"{batch}: a row key appears twice in the readings: {sorted(k for k in set(a) if a.count(k) > 1)}")
    if set(a) != set(agreed_keys):
        sys.exit(f"{batch}: the readings' keys differ from agreed.csv's: {sorted(set(a) ^ set(agreed_keys))}")
    return a


def locate(qa_root, batch, overlay_dir):
    d = qa_root / batch
    meta = json.loads((d / "audit-meta.json").read_text(encoding="utf-8"))
    agreed = list(csv.DictReader((d / "agreed.csv").open(encoding="utf-8-sig", newline="")))
    out = []
    for fid, m in meta.items():
        if m.get("kind") != "table":
            continue
        cols = [c for c, _ in m["columns"]]
        if cols[0] != m["key"]:
            sys.exit(f"{fid}: the first column must be the key, {m['key']}")
        rows = [{m["key"]: k} for k in printed_order(batch, m["key"], [r[m["key"]] for r in agreed])]
        scan = Image.open(ROOT / m["image"]).convert("L")
        up, angle, st, layout, err = measure(scan, int(m.get("rotation", 0)), len(rows), len(cols))
        if not layout:
            sys.exit(f"{fid} (deskew {angle} degrees): {err}; nothing written")
        vlines, (top, header, bottom), bands = layout
        pitch = (bands[-1][0] - bands[0][0]) / max(len(bands) - 1, 1)

        def box(j, y0, y1):
            return vlines[j][1] + 3, y0, vlines[j + 1][0] - 3, y1

        def row_box(i):   # the printed row with a margin, never past halfway to its neighbors
            s, e = bands[i]
            pad = 0.3 * pitch
            up_lim = (bands[i - 1][1] + s) / 2 if i else header[1] + 2
            dn_lim = (e + bands[i + 1][0]) / 2 if i + 1 < len(bands) else bottom[0] - 2
            return round(max(s - pad, up_lim)), round(min(e + pad, dn_lim))

        def record(key, col, role, b):
            x0, y0, x1, y1 = b
            cx, cy = to_upright((x0 + x1) / 2, (y0 + y1) / 2, up.size, angle)
            u, v = to_scan(cx, cy, scan.size, int(m.get("rotation", 0)))
            quarter = int(m.get("rotation", 0)) % 180 == 90   # a quarter turn swaps width and height on the scan
            bu, bv = ((y1 - y0) / 2, (x1 - x0) / 2) if quarter else ((x1 - x0) / 2, (y1 - y0) / 2)
            out.append({"figure_id": fid, "key": key, "column": col, "role": role, "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                        "u": f"{u:.1f}", "v": f"{v:.1f}", "bu": f"{bu:.1f}", "bv": f"{bv:.1f}", "deskew_deg": angle})
        for j, col in enumerate(cols):
            record("", col, "header", box(j, top[1] + 3, header[0] - 3))
        for i, r in enumerate(rows):
            y0, y1 = row_box(i)
            for j, col in enumerate(cols):
                record(r[m["key"]], col, "key" if j == 0 else "cell", box(j, y0, y1))
        if overlay_dir:
            ov = st.convert("RGB")
            dr = ImageDraw.Draw(ov)
            for b in out:
                if b["figure_id"] == fid:
                    color = {"header": (0, 150, 0), "key": (220, 0, 0), "cell": (30, 90, 230)}[b["role"]]
                    dr.rectangle([b["x0"], b["y0"], b["x1"], b["y1"]], outline=color, width=2)
            for i, r in enumerate(rows):   # the key as transcribed, at the left of its band, to check the row order
                dr.text((max(vlines[0][0] - 120, 0), bands[i][0]), r[m["key"]], fill=(220, 0, 0))
            overlay_dir.mkdir(parents=True, exist_ok=True)
            ov.save(overlay_dir / f"{fid}-layout.png")
        print(f"{fid}: deskew {angle} degrees, {len(cols)} columns, {len(bands)} rows, row pitch {pitch:.1f} px")
    if not out:
        sys.exit(f"{batch}: no table in audit-meta.json")
    with (d / "cell-layout.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(f"written: {d / 'cell-layout.csv'} ({len(out)} boxes)" + (f"; overlays in {overlay_dir}" if overlay_dir else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("batch", nargs="?")
    ap.add_argument("--qa-root", default=str(ROOT / "qa"))
    ap.add_argument("--overlay-dir", default=str(ROOT / "work" / "table-layout"))
    ap.add_argument("--probe", nargs=4, metavar=("IMAGE", "ROTATION", "ROWS", "COLUMNS"),
                    help="try a page not yet transcribed (rows from the index) and report; writes nothing")
    a = ap.parse_args()
    if a.probe:
        img, rot, n, k = a.probe
        _, angle, _, layout, err = measure(Image.open(ROOT / img).convert("L"), int(rot), int(n), int(k))
        print(f"{img}: deskew {angle} degrees: " + ("found every row and column" if layout else err))
        return 0 if layout else 1
    if not a.batch:
        ap.error("a batch, or --probe")
    locate(Path(a.qa_root), a.batch, Path(a.overlay_dir) if a.overlay_dir else None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
