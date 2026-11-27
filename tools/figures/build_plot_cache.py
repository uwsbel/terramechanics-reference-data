"""Build the site's plot and overlay cache from data/experiments and the batch overlay recipes.

    python tools/figures/build_plot_cache.py [--only <experiment_id> ...]

Writes, under work/site-cache/ (ignored by git, copied into site/img/ by tools/build_site.py):
    plots/<experiment_id>.png          the experiment's family (all series read from the same figure) in SI,
                                       this experiment in color and the others in grey (legend labels from
                                       data/experiments/index.csv: normal stress in kPa for direct shear,
                                       otherwise the printed label)
    plots/<figure_id>-family.png       all experiments read from the same figure, together
    overlays/<figure>-p<n>.png         both readings on the page image, from qa/<batch>/overlays.csv
                                       (columns: figure_id, panel, image, box, points_a, points_b, name)

Run from a conda env with matplotlib, Pillow and NumPy (pychrono10 on this machine); the site
builder itself needs none of them.
"""
import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLOTS = ROOT / "work" / "site-cache" / "plots"
# The record whose page is the reader-facing card (plan v3 pilot, tools/build_site.py PILOT_RECORD) has a title of its
# own. Every record plot is drawn readable (plot_observations.py --readable: short tick labels with an SI prefix, no
# baked caption, since the page carries one), for every record since 2026-11-21 (Dan's look at a density plot).
PILOT = "b68-lpt-024"
KINDS = {"ds": "direct shear tests", "lpt": "load-penetration tests", "dens": "density measurements",
         "sonic": "sonic modulus tests", "gs": "grain size analyses", "gs;dens": "grain size and density analyses",
         "drag": "footpad drag tests", "dpt": "dynamic penetrometer tests", "imp": "footpad impact tests",
         "mdrop": "drops of the 1/6-scale Lunar Module model", "tx": "triaxial tests"}
OVERLAYS = ROOT / "work" / "site-cache" / "overlays"


def label_of(row, exp):
    m = re.search(r"(\d+(?:\.\d+)?)\s*psf", row.get("loading", ""))
    if row.get("test_type") == "ds" and m:
        return f"{float(m.group(1)) * 47.880258980336 / 1000:.1f} kPa"
    return row.get("test_label_printed") or exp


def title_of(row, figs):
    """The plot's title, in words; a record read from several figures names them all (the model drops: Figs. 5-24 and
    5-25). Figure ids as printed: 'F2-42' -> 'Fig. 2-42', 'FA-19' -> 'Fig. A-19'."""
    soil = row.get("soil_family") or "soil"
    dr = f", Dr {row['dr_printed']}" if row.get("dr_printed") else ""
    kind = KINDS.get(row.get("test_type"), row.get("test_type", "tests"))
    names = [f[1:] for f in figs]
    return f"{soil}{dr}: {kind} printed in Fig{'s' if len(figs) > 1 else ''}. {' and '.join(names)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    PLOTS.mkdir(parents=True, exist_ok=True)
    OVERLAYS.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    plot = str(ROOT / "tools" / "figures" / "plot_observations.py")
    exps = sorted(p.parent.name for p in (ROOT / "data" / "experiments").glob("*/observations.csv"))
    # --only limits which plots are WRITTEN; a family is always drawn from all its records (filtering first would
    # redraw a record's plot, and its figure's family plot, without the other tests of the figure)
    with (ROOT / "data" / "experiments" / "index.csv").open(encoding="utf-8-sig", newline="") as f:
        index = {r["experiment_id"]: r for r in csv.DictReader(f)}
    families, figs_of = {}, {}
    for e in exps:
        meta = json.loads((ROOT / "data" / "experiments" / e / "series.json").read_text(encoding="utf-8"))
        families.setdefault(meta.get("figure_id", "unknown"), []).append(e)
        figs_of[e] = meta.get("figures") or [meta.get("figure_id", "unknown")]
    for fig, members in families.items():
        if a.only and not set(members) & set(a.only):
            continue
        labels = [label_of(index.get(e, {}), e) for e in members]
        for e in members:
            if a.only and e not in a.only:
                continue
            row = index.get(e, {})
            title = (f"{row.get('test_label_printed') or e} (red) and the other tests printed in Fig. {fig[1:]} (gray)"
                     if e == PILOT else title_of(row, figs_of[e]))
            subprocess.run([py, plot, *members, "--highlight", e, "--labels", ",".join(labels), "--out", str(PLOTS / f"{e}.png"),
                            "--title", title, "--readable"], check=True)
        if not a.only:
            subprocess.run([py, plot, *members, "--out", str(PLOTS / f"{fig}-family.png"),
                            "--title", f"All series read from {fig}"], check=True)
    rotation = {}   # figure id -> degrees clockwise that make a figure printed sideways read upright (as render_pages.py)
    for src in ("1968", "1968-vol2"):
        with (ROOT / "corpus" / src / "figures.csv").open(encoding="utf-8-sig", newline="") as f:
            rotation.update({r["id"]: int(r.get("rotation") or 0) for r in csv.DictReader(f)})
    n = 0
    for recipe in (ROOT / "qa").glob("*/overlays.csv"):
        with recipe.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                pts = [str(ROOT / r["points_a"])] + ([str(ROOT / r["points_b"])] if r.get("points_b") else [])
                out = OVERLAYS / f"{r['name']}.png"
                cmd = [py, str(ROOT / "tools" / "plot_grid.py"), "overlay", str(ROOT / r["image"]), "--points", *pts,
                       "--box", *r["box"].split(), "--out", str(out)]
                subprocess.run(cmd, check=True, capture_output=True)
                # The points are drawn in the unrotated page frame they were read in; only the finished
                # picture is turned, so the overlay can never drift from the readings.
                if rotation.get(r["figure_id"]):
                    from PIL import Image
                    with Image.open(out) as im:
                        im.rotate(-rotation[r["figure_id"]], expand=True).save(out)   # Pillow turns counter-clockwise
                n += 1
    print(f"plots for {len(exps)} experiments and {len(families)} families; {n} overlays")
    return 0


if __name__ == "__main__":
    sys.exit(main())
