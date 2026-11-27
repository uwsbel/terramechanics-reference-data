"""Blind validation packet for the frozen off-ink check (tools/check_trace_ink.py, D-031 v1).

A stratified random sample of trace samples from every batch's ink-checks.csv, none of them an item of the
2026-10-27 re-check (the development set): 120 the check excluded, 150 it passed within 20 px of a plotted
symbol, 80 it passed elsewhere, 50 it sent to review. Each becomes one item, shuffled: a crop with the
sample marked, and one question: is it on its line's own ink? The adjudicators never see the verdict or the
stratum; the key does.

Usage: make_ink_validation.py <packet_dir> <key_csv> [--seed N]
"""
import argparse, csv, json, random, shutil
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[3]
BATCHES = ["curves-pilot-b1", "curves-appc-b1", "curves-appc-b2", "curves-appc-b3", "curves-appc-b5", "curves-appc-b6",
           "curves-appc-b7", "curves-appc-b8", "curves-appc-b9", "curves-appc-b10", "curves-appc-b11", "curves-appa-b1",
           "curves-appa-b2", "curves-appa-b3", "curves-appb-b1"]
QUOTA = {"excluded": 120, "eligible-near": 150, "eligible-far": 80, "review": 50}
NEAR = 20
load = lambda p: list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("packet"); ap.add_argument("key"); ap.add_argument("--seed", type=int, default=20261028)
    a = ap.parse_args()
    out, rng = Path(a.packet), random.Random(a.seed)
    for d in ("crops", "pages", "tools"):
        (out / d).mkdir(parents=True, exist_ok=True)
    # development set: every point of the 2026-10-27 re-check, by reader and submitted series
    dev = set()
    for r in load(REPO / "qa/adjudication-2026-10-27/final-decisions.csv"):
        fig, panel, sid, kind, src, seq = r["object"].split("/")
        dev.add((fig, panel, src.split("-")[0], sid, seq))
    figs = {f["id"]: f for f in load(REPO / "corpus/1968-vol2/figures.csv")}
    strata, info = defaultdict(list), {}
    for b in BATCHES:
        q = REPO / "qa" / b
        ren = {(r["figure_id"], r["submitted"]): r["series_id"] for r in load(q / "series-ids.csv")} if (q / "series-ids.csv").exists() else {}
        meta = json.loads((q / "audit-meta.json").read_text(encoding="utf-8")) if (q / "audit-meta.json").exists() else {}
        ov = {(o["figure_id"], o["panel"]): o["image"] for o in load(q / "overlays.csv")}
        marks, symbol_of = defaultdict(list), defaultdict(lambda: defaultdict(int))
        for reader in ("claude", "codex"):
            for p in (q / "rederived" / reader).glob("*/points-p*-native.csv"):
                for m in load(p):
                    if m["point_kind"] == "marker":
                        marks[(m["figure_id"], m["panel"])].append((float(m["pixel_u"]), float(m["pixel_v"])))
                        symbol_of[(m["figure_id"], ren.get((m["figure_id"], m["series_id"]), m["series_id"]))][m["symbol"]] += 1
        for r in load(q / "ink-checks.csv"):
            sid = ren.get((r["figure_id"], r["series_id"]), r["series_id"])
            if (r["figure_id"], r["panel"], r["reader"], sid, r["sequence"]) in dev:
                continue
            u, v = float(r["pixel_u"]), float(r["pixel_v"])
            if r["verdict"] == "eligible":
                near = any(max(abs(mu - u), abs(mv - v)) <= NEAR for mu, mv in marks[(r["figure_id"], r["panel"])])
                st = "eligible-near" if near else "eligible-far"
            else:
                st = r["verdict"]
            fm = meta.get(r["figure_id"], {})
            label = fm.get("series", {}).get(sid, {}).get("label") or sid
            sy = symbol_of[(r["figure_id"], sid)]
            symbol = fm.get("series", {}).get(sid, {}).get("symbol") or (max(sy, key=sy.get) if sy else "")
            strata[st].append(dict(r, batch=b, series=sid, label=label, legend_symbol=symbol, image=ov[(r["figure_id"], r["panel"])]))
    chosen = []
    for st, n in QUOTA.items():
        pool = strata[st]
        rng.shuffle(pool)
        chosen += [dict(x, stratum=st) for x in pool[:n]]
        print(f"{st}: {len(pool)} available, {min(n, len(pool))} drawn")
    rng.shuffle(chosen)
    items, key, pages = [], [], {}
    for i, r in enumerate(chosen, 1):
        iid = f"{i:03d}"
        if r["image"] not in pages:
            pages[r["image"]] = Image.open(REPO / r["image"]).convert("RGB")
            shutil.copy2(REPO / r["image"], out / "pages" / Path(r["image"]).name)
        u, v = float(r["pixel_u"]), float(r["pixel_v"])
        W, Z = 32, 6
        x0, y0 = int(u) - W, int(v) - W
        c = pages[r["image"]].crop((x0, y0, x0 + 2 * W + 1, y0 + 2 * W + 1)).resize(((2 * W + 1) * Z,) * 2, Image.NEAREST)
        d = ImageDraw.Draw(c)
        X, Y = (u - x0 + 0.5) * Z, (v - y0 + 0.5) * Z
        for (a1, b1, a2, b2) in ((X - 22, Y, X - 7, Y), (X + 7, Y, X + 22, Y), (X, Y - 22, X, Y - 7), (X, Y + 7, X, Y + 22)):
            d.line([a1, b1, a2, b2], fill=(230, 20, 20), width=4)   # an open cross: the sample is at the gap's center
        c.save(out / "crops" / f"item-{iid}.png")
        f = figs.get(r["figure_id"], {})
        items.append({"item": iid, "figure": r["figure_id"], "panel": r["panel"], "series": r["label"],
                      "legend_symbol": r["legend_symbol"], "figure_title": f.get("title_as_printed", ""),
                      "rotation": f.get("rotation", ""), "legend_entries": f.get("legend_entries", ""),
                      "P": f"px ({u:.1f},{v:.1f})", "crop": f"crops/item-{iid}.png", "crop_origin_px": f"{x0},{y0}",
                      "crop_scale": Z, "page": f"pages/{Path(r['image']).name}"})
        key.append({"item": iid, "batch": r["batch"], "figure_id": r["figure_id"], "panel": r["panel"], "reader": r["reader"],
                    "series_id": r["series_id"], "sequence": r["sequence"], "stratum": r["stratum"], "verdict": r["verdict"],
                    "reason": r["reason"]})
    def write(p, rows):
        with open(p, "w", encoding="utf-8", newline="") as h:
            w = csv.DictWriter(h, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
    write(out / "items.csv", items)
    write(out / "answers.csv", [{"item": i["item"], "A": "", "confidence": "", "comment": ""} for i in items])
    Path(a.key).parent.mkdir(parents=True, exist_ok=True)
    write(Path(a.key), key)
    shutil.copy2(REPO / "tools" / "plot_grid.py", out / "tools" / "plot_grid.py")
    print(f"{len(items)} items in {out}")


if __name__ == "__main__":
    main()
