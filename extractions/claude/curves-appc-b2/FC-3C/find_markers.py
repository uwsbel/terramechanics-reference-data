"""Helper for the FC-3C blind reading: symbol templates cut from clean markers on this page,
coverage-score matching (fraction of the template's ink lying on page ink), used to
(a) list candidate markers of each symbol in a panel box and (b) refine an eye-read center.
The score is immune to extra ink (the drawn curve passing through a marker) because it only
asks whether the template's own strokes are covered. Every result is checked by eye on
contact sheets (`sheet`) and on the overlay; the helper does not replace the eye check.

  python find_markers.py search <image> --box u0 v0 u1 v1 [--min-score 0.85]
  python find_markers.py refine <image> <guesses.csv> <out.csv> [--radius 10]
  python find_markers.py sheet  <image> <points.csv> <outprefix> [--zoom 4] [--half 35]
"""
import sys, csv, argparse, numpy as np
from PIL import Image, ImageDraw

# clean instances on p0125.png: (symbol, u, v) near the marker; the connected component there
# is the template and its bbox center is the template origin.
CLEAN = {"circle": (1957, 1590), "plus": (2092, 1405), "square": (1668, 2141),
         "triangle-up": (1815, 3098), "triangle-down": (1814, 3179)}


def load(path):
    return np.array(Image.open(path).convert("L")) < 128


def component(im, u, v, r=20):
    H, W = im.shape
    v0, v1, u0, u1 = max(v - r, 0), min(v + r, H), max(u - r, 0), min(u + r, W)
    ys, xs = np.nonzero(im[v0:v1, u0:u1])
    k = np.argmin((ys + v0 - v) ** 2 + (xs + u0 - u) ** 2)
    sv, su = ys[k] + v0, xs[k] + u0
    seen = np.zeros_like(im)
    stack = [(sv, su)]
    seen[sv, su] = True
    pts = []
    while stack:
        y, x = stack.pop()
        pts.append((y, x))
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < H and 0 <= xx < W and im[yy, xx] and not seen[yy, xx]:
                seen[yy, xx] = True
                stack.append((yy, xx))
        if len(pts) > 3000:
            raise RuntimeError("component too large: not an isolated marker")
    return np.array(pts)


def templates(im):
    T = {}
    for sym, (u, v) in CLEAN.items():
        p = component(im, u, v)
        vmin, umin = p.min(0)
        vmax, umax = p.max(0)
        cu, cv = (umin + umax) / 2.0, (vmin + vmax) / 2.0
        T[sym] = (p[:, 1] - cu, p[:, 0] - cv, (umax - umin + 1, vmax - vmin + 1))
    return T


def dilate(im):
    d = im.copy()
    d[1:, :] |= im[:-1, :]
    d[:-1, :] |= im[1:, :]
    d[:, 1:] |= im[:, :-1]
    d[:, :-1] |= im[:, 1:]
    return d


def score_map(imd, T, box):
    """coverage score for the template origin at every integer (u, v) in box. Offsets are
    half-integers when the bbox size is even; they are rounded (0.5 px bias at most)."""
    du, dv, _ = T
    du = np.round(du).astype(int)
    dv = np.round(dv).astype(int)
    u0, v0, u1, v1 = box
    acc = np.zeros((v1 - v0, u1 - u0), dtype=np.float32)
    H, W = imd.shape
    for a, b in zip(du, dv):
        vs0, vs1 = v0 + b, v1 + b
        us0, us1 = u0 + a, u1 + a
        if vs0 < 0 or us0 < 0 or vs1 > H or us1 > W:
            sub = np.zeros_like(acc)
            vv0, vv1 = max(vs0, 0), min(vs1, H)
            uu0, uu1 = max(us0, 0), min(us1, W)
            sub[vv0 - vs0:vv1 - vs0, uu0 - us0:uu1 - us0] = imd[vv0:vv1, uu0:uu1]
        else:
            sub = imd[vs0:vs1, us0:us1]
        acc += sub
    return acc / len(du)


def peaks(S, box, min_score, sep=12):
    u0, v0, _, _ = box
    cand = []
    Sc = S.copy()
    while True:
        k = np.argmax(Sc)
        v, u = np.unravel_index(k, Sc.shape)
        s = Sc[v, u]
        if s < min_score:
            break
        vv0, vv1 = max(v - sep, 0), min(v + sep + 1, Sc.shape[0])
        uu0, uu1 = max(u - sep, 0), min(u + sep + 1, Sc.shape[1])
        sub = Sc[vv0:vv1, uu0:uu1]
        m = sub >= s - 0.02
        ys, xs = np.nonzero(m)
        cu, cv = xs.mean() + uu0 + u0, ys.mean() + vv0 + v0
        cand.append((cu, cv, float(s), int(m.sum())))
        Sc[vv0:vv1, uu0:uu1] = 0
    return cand


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("search")
    a.add_argument("image")
    a.add_argument("--box", nargs=4, type=int, required=True)
    a.add_argument("--min-score", type=float, default=0.85)
    a.add_argument("--symbols", default=",".join(CLEAN))
    b = sp.add_parser("refine")
    b.add_argument("image")
    b.add_argument("guesses")
    b.add_argument("out")
    b.add_argument("--radius", type=int, default=10)
    c = sp.add_parser("sheet")
    c.add_argument("image")
    c.add_argument("points")
    c.add_argument("outprefix")
    c.add_argument("--zoom", type=int, default=4)
    c.add_argument("--half", type=int, default=35)
    c.add_argument("--per-row", type=int, default=4)
    c.add_argument("--rows", type=int, default=3)
    c.add_argument("--kind", default="marker")
    args = ap.parse_args()
    im = load(args.image)
    if args.cmd == "sheet":
        rows = list(csv.DictReader(open(args.points, newline="", encoding="utf-8")))
        rows = [r for r in rows if r.get("point_kind", "marker") == args.kind]
        page = Image.open(args.image).convert("RGB")
        z, h = args.zoom, args.half
        per = args.per_row * args.rows
        n = 0
        for s in range(0, len(rows), per):
            chunk = rows[s:s + per]
            W = args.per_row * (2 * h * z + 8)
            H = args.rows * (2 * h * z + 8 + 14)
            sheet = Image.new("RGB", (W, H), "white")
            d = ImageDraw.Draw(sheet)
            for i, r in enumerate(chunk):
                u, v = float(r["pixel_u"]), float(r["pixel_v"])
                cu, cv = int(round(u)), int(round(v))
                crop = page.crop((cu - h, cv - h, cu + h, cv + h)).resize((2 * h * z, 2 * h * z), Image.NEAREST)
                dc = ImageDraw.Draw(crop)
                x = (u - (cu - h)) * z
                y = (v - (cv - h)) * z
                dc.line([(x - 40, y), (x + 40, y)], fill=(255, 0, 0), width=1)
                dc.line([(x, y - 40), (x, y + 40)], fill=(255, 0, 0), width=1)
                bu = float(r.get("u_bound_px") or 2)
                bv = float(r.get("v_bound_px") or 2)
                dc.rectangle([x - bu * z, y - bv * z, x + bu * z, y + bv * z], outline=(0, 160, 0))
                ox = (i % args.per_row) * (2 * h * z + 8)
                oy = (i // args.per_row) * (2 * h * z + 8 + 14)
                sheet.paste(crop, (ox, oy + 14))
                label = "%s #%s %s (%.1f,%.1f) %s" % (r.get("series_id", ""), r.get("sequence", ""),
                                                      r.get("symbol", ""), u, v, (r.get("note") or "")[:40])
                d.text((ox + 2, oy), label, fill=(0, 0, 200))
            out = "%s%02d.png" % (args.outprefix, n)
            sheet.save(out)
            print("wrote", out, len(chunk))
            n += 1
        return
    T = templates(im)
    imd = dilate(im)
    for sym, (du, dv, sz) in T.items():
        print("template %s: %d px, bbox %dx%d" % (sym, len(du), sz[0], sz[1]), file=sys.stderr)
    if args.cmd == "search":
        for sym in args.symbols.split(","):
            S = score_map(imd, T[sym], args.box)
            for cu, cv, s, npl in peaks(S, args.box, args.min_score):
                print("%s,%.1f,%.1f,%.3f,%d" % (sym, cu, cv, s, npl))
    elif args.cmd == "refine":
        rows = list(csv.DictReader(open(args.guesses, newline="", encoding="utf-8")))
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            fields = list(rows[0].keys()) + ["ref_u", "ref_v", "score", "plateau", "shift"]
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in rows:
                u, v = float(r["pixel_u"]), float(r["pixel_v"])
                rad = args.radius
                box = (int(u) - rad, int(v) - rad, int(u) + rad + 1, int(v) + rad + 1)
                S = score_map(imd, T[r["symbol"]], box)
                k = np.argmax(S)
                pv, pu = np.unravel_index(k, S.shape)
                s = S[pv, pu]
                m = S >= s - 0.02
                ys, xs = np.nonzero(m)
                cu, cv = xs.mean() + box[0], ys.mean() + box[1]
                sh = float(np.hypot(cu - u, cv - v))
                r.update(ref_u="%.1f" % cu, ref_v="%.1f" % cv, score="%.3f" % s, plateau=int(m.sum()), shift="%.1f" % sh)
                w.writerow(r)
                print("%s %s guess (%.0f,%.0f) -> (%.1f,%.1f) score %.3f plateau %d shift %.1f" %
                      (r["series_id"], r["symbol"], u, v, cu, cv, s, int(m.sum()), sh))


if __name__ == "__main__":
    main()
