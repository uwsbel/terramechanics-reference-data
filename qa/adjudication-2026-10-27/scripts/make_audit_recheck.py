"""Blind re-check packet for the audit wave 1 points the student reviewers disputed (roadmap 4c).

Points: every wave 1 object whose recorded reviews (qa/audits.csv) are flagged (both say problem), split,
cannot tell by both, or a single review that says problem. Each becomes one item:

  compare-marker  a compare row on a plotted symbol: the kept reading and the other reading of the same
                  symbol, drawn as P (blue circle) and Q (orange square), which is which shuffled per item
  compare-trace   a compare row on a curve sample: the kept trace sample and the other reading's trace at
                  the same x (interpolated between its two neighbouring samples), as P and Q
  check-marker    a symbol row: the kept reading P with its error box; is the printed symbol's center in
                  the box, and is it the named test's symbol
  check-trace     a curve-sample row: the kept sample P with its error box; does the drawn line pass through

The other reading's pixels come from its own re-derived submission (qa/<batch>/rederived/<reader>/), not
from the global map the student packets used to place the orange square (D-027 deferred item).
The adjudicators never see the reviewers' answers or which reading is kept; the key does.

Usage: make_audit_recheck.py <packet_dir> <key_csv> [--seed N]
"""
import argparse, csv, json, random, shutil, sys
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[3]
BLUE, ORANGE = (30, 90, 230), (240, 120, 0)
POINT = ("figure_id", "panel", "series_id", "point_kind", "source", "sequence")


def load(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(p, rows, fields):
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def outcome(verdicts):
    vs = list(verdicts)
    if len(vs) == 1:
        return "single-" + vs[0]
    if all(v == "ok" for v in vs):
        return "confirmed"
    if all(v == "problem" for v in vs):
        return "flagged"
    if all(v == "cannot tell" for v in vs):
        return "both cannot tell"
    return "split"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("packet"); ap.add_argument("key")
    ap.add_argument("--seed", type=int, default=20261027)
    a = ap.parse_args()
    out, rng = Path(a.packet), random.Random(a.seed)
    (out / "crops").mkdir(parents=True, exist_ok=True); (out / "pages").mkdir(exist_ok=True); (out / "tools").mkdir(exist_ok=True)

    # which objects, with their reviews and the key row that asked about them (wave 1 keys only)
    reviews = defaultdict(dict)
    for r in load(REPO / "qa" / "audits.csv"):
        reviews[r["object"]][r["auditor"]] = r["outcome"]
    keyrow = {}
    for f in sorted((REPO / "qa" / "audits" / "keys").glob("key-*-[A-E].csv")):
        for k in load(f):
            if not k["kind"].startswith("control"):
                keyrow.setdefault("/".join(k[c] for c in POINT), k)
    chosen = [(o, outcome(v.values())) for o, v in reviews.items()
              if outcome(v.values()) in ("flagged", "split", "both cannot tell", "single-problem")]
    chosen.sort(key=lambda t: t[0])

    canon, meta, pages, reading, renamed = {}, {}, {}, {}, {}
    def batch_data(b):
        if b in canon:
            return
        canon[b] = {"/".join(p[c] for c in POINT): p for p in load(REPO / "qa" / b / "canonical.csv")}
        # submissions keep the series id as submitted; a canonical-stage rename (series-ids.csv, D-024) maps it
        if (REPO / "qa" / b / "series-ids.csv").exists():
            for r in load(REPO / "qa" / b / "series-ids.csv"):
                renamed[(r["figure_id"], r["submitted"])] = r["series_id"]
        meta[b] = json.loads((REPO / "qa" / b / "audit-meta.json").read_text(encoding="utf-8"))
        for ov in load(REPO / "qa" / b / "overlays.csv"):
            pages[(ov["figure_id"], ov["panel"])] = ov["image"]

    def other_points(b, reader, fid, panel):
        k = (b, reader, fid, panel)
        if k not in reading:
            p = REPO / "qa" / b / "rederived" / reader / fid / f"points-p{panel}-native.csv"
            reading[k] = load(p) if p.exists() else []
        return reading[k]

    images, items, key, skipped = {}, [], [], []
    for obj, oc in chosen:
        k = keyrow.get(obj)
        if not k:
            skipped.append((obj, "no wave 1 key row")); continue
        b, fid, panel, sid, kind_pt = k["batch"], k["figure_id"], k["panel"], k["series_id"], k["point_kind"]
        batch_data(b)
        c = canon[b].get(obj)
        if not c:
            skipped.append((obj, "not in canonical.csv any more")); continue
        fm = meta[b].get(fid, {})
        label = fm.get("series", {}).get(sid, {}).get("label", sid)
        sym = fm.get("series", {}).get(sid, {}).get("symbol", "") or c["symbol"]
        noun = fm.get("series_noun", "curve")
        kept = (float(c["pixel_u"]), float(c["pixel_v"]))
        box = (float(c["u_bound_px"]), float(c["v_bound_px"]))
        other = None
        if k["kind"] == "compare":
            if not c.get("other_y_native"):
                skipped.append((obj, "compare row without the other reading's value")); continue
            reader = "codex" if c["source"].split("-")[0] == "claude" else "claude"
            ox = float(c["other_x_native"] or c["x_native"]); oy = float(c["other_y_native"])
            cand = [r for r in other_points(b, reader, fid, panel)
                    if renamed.get((fid, r["series_id"]), r["series_id"]) == sid and r["point_kind"] == kind_pt]
            if kind_pt == "marker" and cand:
                r = min(cand, key=lambda r: abs(float(r["x_native"]) - ox) / max(abs(ox), 1) + abs(float(r["y_native"]) - oy) / max(abs(oy), 1))
                if abs(float(r["y_native"]) - oy) <= 0.01 * max(abs(oy), 1) + 0.05:
                    other = (float(r["pixel_u"]), float(r["pixel_v"]))
            elif kind_pt == "trace" and cand:
                cand.sort(key=lambda r: float(r["x_native"]))
                x = float(c["x_native"])
                for r0, r1 in zip(cand, cand[1:]):
                    x0, x1 = float(r0["x_native"]), float(r1["x_native"])
                    if x0 <= x <= x1 and x1 > x0:
                        t = (x - x0) / (x1 - x0)
                        yi = float(r0["y_native"]) + t * (float(r1["y_native"]) - float(r0["y_native"]))
                        if abs(yi - oy) <= 0.01 * max(abs(oy), 1) + 0.5:
                            other = (float(r0["pixel_u"]) + t * (float(r1["pixel_u"]) - float(r0["pixel_u"])),
                                     float(r0["pixel_v"]) + t * (float(r1["pixel_v"]) - float(r0["pixel_v"])))
                        break
            if other is None:
                skipped.append((obj, f"other reading ({reader}) not found at its recorded value")); continue

        iid = f"{len(items) + 1:03d}"
        page = pages[(fid, panel)]
        if page not in images:
            images[page] = Image.open(REPO / page).convert("RGB")
            shutil.copy2(REPO / page, out / "pages" / Path(page).name)
        img = images[page]
        pts = [kept] + ([other] if other else [])
        cu = (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2; cv = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
        half = int(max(60, (max(p[0] for p in pts) - min(p[0] for p in pts)) / 2 + 40, (max(p[1] for p in pts) - min(p[1] for p in pts)) / 2 + 40))
        scale = 4 if half <= 75 else 3 if half <= 110 else 2
        x0, y0 = int(cu - half), int(cv - half)
        crop = img.crop((x0, y0, x0 + 2 * half, y0 + 2 * half)).resize((4 * half * scale // 2, 4 * half * scale // 2), Image.NEAREST)
        d = ImageDraw.Draw(crop)
        fmt = lambda p: f"px ({p[0]:.1f},{p[1]:.1f})"
        if other:
            swap = rng.random() < 0.5
            P, Q = (other, kept) if swap else (kept, other)
            for (u, v), col, shape in ((P, BLUE, "circle"), (Q, ORANGE, "square")):
                X, Y, r = (u - x0) * scale, (v - y0) * scale, 4 * scale
                (d.ellipse if shape == "circle" else d.rectangle)([X - r, Y - r, X + r, Y + r], outline=col, width=2)
            ikind = "compare-marker" if kind_pt == "marker" else "compare-trace"
            if ikind == "compare-marker":
                q = (f"P and Q are two readings of the center of the same {sym} symbol of the {label} {noun}. Which mark is at the "
                     "center of the printed symbol? `p`, `q`, `both` (both within the center tolerance), `neither`, `cannot tell`.")
            else:
                q = (f"P and Q are two readings of the drawn line of the {label} {noun} at the same x. Which mark is on the drawn "
                     "line? `p`, `q`, `both`, `neither`, `cannot tell`.")
            items.append({"item": iid, "kind": ikind, "figure": fid, "panel": panel, "series": label, "legend_symbol": sym,
                          "question": q, "P": fmt(P), "Q": fmt(Q), "box_P": "", "crop": f"crops/item-{iid}.png",
                          "crop_origin_px": f"{x0},{y0}", "crop_scale": scale, "page": f"pages/{Path(page).name}"})
            key.append({"item": iid, "object": obj, "batch": b, "review_outcome": oc, "reviews": json.dumps(reviews[obj]),
                        "P": "other" if swap else "kept", "Q": "kept" if swap else "other",
                        "kept_px": fmt(kept), "other_px": fmt(other)})
        else:
            X, Y = (kept[0] - x0) * scale, (kept[1] - y0) * scale
            bu, bv = max(box[0], 1) * scale, max(box[1], 1) * scale
            d.rectangle([X - bu, Y - bv, X + bu, Y + bv], outline=BLUE, width=1)
            d.line([X - 3 * scale, Y, X + 3 * scale, Y], fill=BLUE, width=1); d.line([X, Y - 3 * scale, X, Y + 3 * scale], fill=BLUE, width=1)
            if kind_pt == "marker":
                ikind = "check-marker"
                q = (f"A: is the center of the printed symbol nearest P inside the blue box (half-widths {box[0]:.0f} and {box[1]:.0f} px)? "
                     f"`yes`, `no`, `cannot tell`. B: is that symbol a {sym}, the symbol of the {label} {noun}, on that test's curve? "
                     "`yes`, `no`, `cannot tell`.")
            else:
                ikind = "check-trace"
                q = (f"A: does the drawn line of the {label} {noun} pass through the blue box around P (half-widths {box[0]:.0f} and "
                     f"{box[1]:.0f} px)? `yes`, `no`, `cannot tell`. Leave B empty.")
            items.append({"item": iid, "kind": ikind, "figure": fid, "panel": panel, "series": label, "legend_symbol": sym,
                          "question": q, "P": fmt(kept), "Q": "", "box_P": f"{box[0]:.1f},{box[1]:.1f}", "crop": f"crops/item-{iid}.png",
                          "crop_origin_px": f"{x0},{y0}", "crop_scale": scale, "page": f"pages/{Path(page).name}"})
            key.append({"item": iid, "object": obj, "batch": b, "review_outcome": oc, "reviews": json.dumps(reviews[obj]),
                        "P": "kept", "Q": "", "kept_px": fmt(kept), "other_px": ""})
        crop.save(out / "crops" / f"item-{iid}.png")

    write(out / "items.csv", items, ["item", "kind", "figure", "panel", "series", "legend_symbol", "question", "P", "Q", "box_P",
                                     "crop", "crop_origin_px", "crop_scale", "page"])
    write(out / "answers.csv", [{"item": i["item"]} for i in items], ["item", "A", "B", "confidence", "comment"])
    Path(a.key).parent.mkdir(parents=True, exist_ok=True)
    write(a.key, key, ["item", "object", "batch", "review_outcome", "reviews", "P", "Q", "kept_px", "other_px"])
    # figure notes for the adjudicators: titles, orientation, legend, series and symbols (no readings, no reviews)
    notes = []
    for b in canon:
        for fid, fm in meta[b].items():
            if any(i["figure"] == fid for i in items):
                ser = "; ".join(f"{v.get('label', s)}: {v.get('symbol', '')}" for s, v in fm.get("series", {}).items())
                notes.append(f"## {fid}\n\n{fm.get('title', '')}\n\nRotation {fm.get('rotation', 0)} degrees. "
                             f"Legend: {fm.get('legend_hint', '')}. Tests and symbols: {ser}.\n\n{fm.get('notes_for_reviewers', '') or ''}\n")
    (out / "figures.md").write_text("\n".join(notes), encoding="utf-8", newline="\n")
    shutil.copy2(REPO / "tools" / "plot_grid.py", out / "tools" / "plot_grid.py")
    from collections import Counter
    print(f"{len(items)} items ({dict(Counter(i['kind'] for i in items))}); {len(skipped)} skipped")
    for o, why in skipped:
        print("  skipped", o, "-", why)


if __name__ == "__main__":
    sys.exit(main())
