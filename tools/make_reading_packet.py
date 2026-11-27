"""Write the evidence packets of a blind curve-reading batch (docs/CURVE-READING.md, section 1).

Usage:
    python tools/make_reading_packet.py <batch.json> --codex-dir <dir> --claude-dir <dir>

<batch.json> names the batch, its figures, the context pages, the series of each figure and the
figure-specific instructions:

    {"batch": "curves-appc-b6", "source": "1968-vol2", "context_pages": [115],
     "figures": {"FC-5A": {"series": [{"series_id": "dr2-13", "label": "Dr .02 to .13", ...}, ...]}},
     "specific": "markdown text: what these figures are and what to produce for them",
     "lessons": ["..."]}

Writes one Codex workdir for the whole batch (<codex-dir>/work/packet, tools, out, and
<codex-dir>/prompt.md) and one workspace per figure for the Claude readers (<claude-dir>/<FIG>/packet,
tools, out, and <claude-dir>/TASK.md, the same prompt with the Claude reader's rules). Both readers
get the same packet: the page images (the figures' pages and the context pages), the figures-index
rows WITHOUT the agents' notes columns (notes of an earlier step stay out of evidence packets,
AGENTS.md), a series list, the protocol and the two reading tools. Nothing from extractions/ or qa/.
"""
import argparse
import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ("calibrate_axes.py", "plot_grid.py")


def figure_rows(source):
    with (ROOT / "corpus" / source / "figures.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = {r["id"]: r for r in csv.DictReader(f)}
    cols = [c for c in next(iter(rows.values())) if not c.startswith("notes_")]
    return rows, cols


def write_packet(dest, cfg, figs, rows, cols):
    for d in ("packet", "tools", "out"):
        (dest / d).mkdir(parents=True, exist_ok=True)
    pages = sorted({int(rows[f]["pdf_page"]) for f in figs} | set(cfg.get("context_pages", [])))
    for p in pages:
        shutil.copy2(ROOT / "corpus" / cfg["source"] / "images" / f"p{p:04d}.png", dest / "packet" / f"p{p:04d}.png")
    with (dest / "packet" / "figures-rows.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for fid in figs:
            w.writerow(rows[fid])
    series = [dict(figure_id=fid, **s) for fid in figs for s in cfg["figures"][fid]["series"]]
    keys = list(dict.fromkeys(k for s in series for k in s))
    with (dest / "packet" / "series.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, lineterminator="\n")
        w.writeheader()
        w.writerows(series)
    shutil.copy2(ROOT / "docs" / "CURVE-READING.md", dest / "packet" / "CURVE-READING.md")
    for t in TOOLS:
        shutil.copy2(ROOT / "tools" / t, dest / "tools" / t)
    return pages


def prompt(cfg, rows, figs, pages):
    listing = "\n".join(f"   - `p{int(rows[f]['pdf_page']):04d}.png`: Figure {f[1:]} ({f}), printed page {rows[f]['printed_page']}"
                        for f in figs)
    context = ", ".join(f"`p{p:04d}.png`" for p in pages if p not in {int(rows[f]["pdf_page"]) for f in figs})
    lessons = "\n".join(f"{i}. {l}" for i, l in enumerate(cfg.get("lessons", []), 1))
    return f"""# Blind reading of {', '.join('Figure ' + f[1:] for f in figs)}, batch {cfg['batch']}

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
{listing}
   Context pages: {context or 'none'}.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

{cfg['specific'].strip()}

## Lessons from earlier figures

{lessons or 'None beyond the protocol.'}

## Tools (folder `tools/`)

Python with Pillow and NumPy: `<local path>` (set
PYTHONIOENCODING=utf-8). Run each script with `--help` first: `tools/calibrate_axes.py detect|apply`
(grid lines, tilt, figures printed sideways with `--x-direction`/`--y-direction`), `tools/plot_grid.py
lines|crop|scan|overlay`. A figure with ticks but no grid lines: calibrate on the measured ticks
(your own helper, writing the same `calibration.json` layout, with `box`); a map whose interior lines
are only predicted from the frame does not count as calibrated (protocol section 4). Write helpers
under `out/`; do not modify `tools/`.

Finish with a short answer: per figure the counts per series and kind, the calibration residuals,
the by-eye label checks, the ambiguities, and the files written. Do not paste the CSVs.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--codex-dir", required=True)
    ap.add_argument("--claude-dir", required=True)
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    rows, cols = figure_rows(cfg["source"])
    figs = list(cfg["figures"])
    codex, claude = Path(a.codex_dir), Path(a.claude_dir)
    if (codex / "work").exists() or claude.exists():
        sys.exit("packet folders exist already; a batch's packets are written once")
    pages = write_packet(codex / "work", cfg, figs, rows, cols)
    text = prompt(cfg, rows, figs, pages)
    (codex / "prompt.md").write_text(text, encoding="utf-8", newline="\n")
    for fid in figs:
        write_packet(claude / fid, cfg, [fid], rows, cols)
    (claude / "TASK.md").write_text(text + """
## For the Claude reader

You read ONE figure (named in your task) in your own workspace; write under `out/<figure_id>/`.
Blindness: do not open anything under the project repository, the dan-codex-from-claude folder, or
any other folder of the scratchpad than your workspace and this TASK.md. Look at PNGs with the Read
tool; make zoomed crops with `tools/plot_grid.py crop` (zoom 3 to 6).
""", encoding="utf-8", newline="\n")
    print(f"{cfg['batch']}: codex {codex}, claude {claude}, figures {figs}, pages {pages}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
