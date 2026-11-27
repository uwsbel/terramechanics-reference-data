"""Plot the recovered observations of an experiment, or of a family of experiments, in SI.

    python tools/figures/plot_observations.py <experiment_id> [<experiment_id> ...] --out <png>
        [--title "..."] [--dpi 150] [--highlight <experiment_id>] [--labels "a,b,..."] [--readable]

With --highlight, that experiment is drawn in color and the others in light grey (a record page
showing one test against its family). --labels gives legend labels in the order of the
experiments (default: the experiment ids).

One PNG with one subplot per panel (panel 1 top: shear stress versus shear displacement; panel 2:
dilation versus shear displacement, or whatever series.json names). Each experiment is one color;
`agreed` points are filled, every other status hollow; the reading bounds are drawn as error
bars (they are bounds, not standard deviations, and the caption says so). Axes are SI (m, Pa).
Produced from data/experiments/<id>/observations.csv and series.json only; the figure carries the
file names so a reader can check every point.

With --readable (the reader-facing site, plan v3 A3.5 and A6.7), values are drawn with an SI prefix that keeps the
tick labels short (lengths in mm; stresses in kPa, or MPa for a modulus; forces in N, or kN above 10 kN; unit weight
in kN/m³), the gray family is labeled "other tests of the same figure", and no caption is baked into the image: the
page carries it, so it is never cut off at the image edge.

In both modes (2026-11-21, Dan: a y label too long for its axis): a long axis title wraps onto two lines; a
dimensionless quantity carries no unit, except a percentage, which is stored as a fraction of 1 and drawn in percent;
"rho c^2" is written ρc².

Needs matplotlib (run from a conda env that has it, for example pychrono10).
"""
import argparse
import csv
import json
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
UNIT_LABEL = {"m_s2": "m/s²", "N_m3": "N/m³", "kg_m3": "kg/m³", "m_s": "m/s"}   # the SI unit codes as printed on an axis
COLORS = ["#b00000", "#008c00", "#0000dc", "#c87800", "#960096", "#009696", "#783c00", "#ff0078", "#5a5a5a"]


def axis_display(unit, quantity, values, readable):
    """(factor, unit shown or None, quantity shown) for one axis, from its SI unit and the values drawn on it."""
    q = quantity.replace("rho c^2", "ρc²")
    if unit == "none":   # dimensionless: a percentage is stored as a fraction of 1 (percent finer: 0 to 1)
        return (100.0, "%", q) if quantity.startswith("percent") else (1.0, None, q)
    if readable:
        big = max((abs(v) for v in values), default=0.0)
        if unit == "m":
            return 1e3, "mm", q
        if unit == "Pa":
            return (1e-6, "MPa", q) if big >= 1e7 else (1e-3, "kPa", q)
        if unit == "N":
            return (1e-3, "kN", q) if big >= 1e4 else (1.0, "N", q)
        if unit == "N_m3":
            return 1e-3, "kN/m³", q
    return 1.0, UNIT_LABEL.get(unit, unit), q


def axis_title(q, u, wrap=None):
    """The axis title, 'quantity (unit)', wrapped onto lines of at most `wrap` characters when given."""
    s = f"{q} ({u})" if u else q
    return textwrap.fill(s, wrap) if wrap else s


def load(exp):
    d = ROOT / "data" / "experiments" / exp
    with (d / "observations.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    meta = json.loads((d / "series.json").read_text(encoding="utf-8"))
    return rows, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiments", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--highlight")
    ap.add_argument("--labels")
    ap.add_argument("--readable", action="store_true")
    a = ap.parse_args()

    order = [e for e in a.experiments if e != a.highlight] + ([a.highlight] if a.highlight in a.experiments else [])
    data = {e: load(e) for e in order}
    panels = sorted({p for _, (rows, _) in data.items() for p in {r["panel"] for r in rows}}, key=int)
    # panels share the x axis only with panels of the same x quantity: a record from several figures (the impact
    # runs: force and displacement against time, then force against displacement) has more than one
    xkey = {}
    for _, (rows, meta) in data.items():
        for p in panels:
            if p in meta["panels"]:
                xkey.setdefault(p, (meta["panels"][p]["x_quantity"], meta["panels"][p]["x_unit_si"]))
    fig, axes = plt.subplots(len(panels), 1, figsize=(7.5, 3.6 * len(panels)), squeeze=False)
    for i, p in enumerate(panels):
        j = next(k for k, q in enumerate(panels) if xkey[q] == xkey[p])
        if j < i:
            axes[i][0].sharex(axes[j][0])
    # an x label under the last panel of each run of panels with the same x quantity
    xlabel_at = {i for i, p in enumerate(panels) if i == len(panels) - 1 or xkey[panels[i + 1]] != xkey[p]}
    # one display scale per panel axis, chosen from every value drawn on it (all experiments of the plot)
    disp = {}
    for p in panels:
        pm = next(meta["panels"][p] for _, (rows, meta) in data.items() if p in meta["panels"])
        vals = {ax: [float(r[f"{ax}_si"]) for _, (rows, _) in data.items() for r in rows if r["panel"] == p] for ax in "xy"}
        disp[p] = {ax: axis_display(pm[f"{ax}_unit_si"], pm[f"{ax}_quantity"], vals[ax], a.readable) for ax in "xy"}
    labels = dict(zip(a.experiments, a.labels.split(","))) if a.labels else {}
    grey_labeled = False
    for k, (exp, (rows, meta)) in enumerate(data.items()):
        col = COLORS[k % len(COLORS)]
        label = labels.get(exp, exp)
        if a.highlight:
            if exp == a.highlight:
                col = COLORS[0]
            else:
                col = "#c0c0c0"
                label = None if grey_labeled else ("other tests of the same figure" if a.readable else "other tests of the family")
                grey_labeled = True
        for i, p in enumerate(panels):
            ax = axes[i][0]
            pr = [r for r in rows if r["panel"] == p]
            if not pr:
                continue
            # the file's order within a series is the drawing order; `sequence` is each reading's own numbering, and
            # sorting by it drew false zigzags where a series mixes both readings (Codex's review, 2026-11-19)
            pr.sort(key=lambda r: r["series_id"])
            cut = {(b["panel"], b["series_id"], b["after"]["source"], str(b["after"]["sequence"])) for b in meta.get("breaks", [])}
            trace = [r for r in pr if r["point_kind"] in ("trace", "gridline")]
            mark = [r for r in pr if r["point_kind"] in ("marker", "feature")]
            (sx, ux, qx), (sy, uy, qy) = disp[p]["x"], disp[p]["y"]
            for subset, ls, mk in ((trace, "-", None), (mark, "", "o")):
                if not subset:
                    continue
                x = [float(r["x_si"]) * sx for r in subset]
                y = [float(r["y_si"]) * sy for r in subset]
                xe = [float(r["x_bound_si"]) * sx for r in subset]
                ye = [float(r["y_bound_si"]) * sy for r in subset]
                agreed = [r["status"] == "agreed" for r in subset]
                if not a.highlight or exp == a.highlight:
                    ax.errorbar(x, y, xerr=xe, yerr=ye, fmt="none", ecolor=col, elinewidth=0.6, alpha=0.6)
                # the legend entry goes on the first artist of this experiment that has data
                if ls:
                    # one line per series: an average and its range bounds are three curves, and one artist
                    # for all of them drew diagonals from the end of one curve to the start of the next
                    for sid in dict.fromkeys(r["series_id"] for r in subset):
                        idx = [j for j, r in enumerate(subset) if r["series_id"] == sid]
                        # an explicit break (series.json `breaks`: a scan dropout) lifts the pen after its row
                        runs, cur = [], []
                        for j in idx:
                            cur.append(j)
                            if (p, sid, subset[j]["source"], subset[j]["sequence"]) in cut:
                                runs.append(cur); cur = []
                        runs.append(cur)
                        for run in [r for r in runs if r]:
                            ax.plot([x[j] for j in run], [y[j] for j in run], ls, color=col, lw=1.2, label=label)
                            label = None
                if mk:
                    xa, ya = [v for v, g in zip(x, agreed) if g], [v for v, g in zip(y, agreed) if g]
                    xp, yp = [v for v, g in zip(x, agreed) if not g], [v for v, g in zip(y, agreed) if not g]
                    ax.plot(xa, ya, "o", color=col, ms=4, label=label if xa else None)
                    ax.plot(xp, yp, "o", mfc="none", mec=col, ms=4, label=label if (xp and not xa) else None)
                    label = None
            ax.set_ylabel(axis_title(qy, uy, wrap=30))   # 30 characters: fits the height of one panel at this size
            if i in xlabel_at:
                ax.set_xlabel(axis_title(qx, ux))
            else:
                ax.tick_params(labelbottom=False)
            ax.grid(True, lw=0.4, alpha=0.5)
    axes[0][0].legend(fontsize=8, ncol=2, frameon=False)
    fig.suptitle(a.title or ", ".join(a.experiments), fontsize=10)
    if a.readable:
        fig.tight_layout(rect=(0, 0, 1, 0.97))
    else:
        fig.text(0.01, 0.004, "Plotted from data/experiments/<id>/observations.csv (SI). Error bars are reading bounds, not standard "
                 "deviations; filled markers were agreed by both readings, hollow ones were not (one-sided-verified, resolved, pending review).", fontsize=6.5, ha="left", va="bottom",
                 wrap=True)   # wrapped to the figure width: on one line it ran past the right edge (2026-11-19)
        fig.tight_layout(rect=(0, 0.035, 1, 0.97))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=a.dpi)
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
