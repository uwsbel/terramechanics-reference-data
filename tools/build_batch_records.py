"""Write the experiment records of every figure of a reconciled curve batch (data/experiments/<id>/).

Usage:
    python tools/build_batch_records.py <batch> [--out data/experiments]

Runs tools/build_observations.py on qa/<batch>/canonical.csv once per source, with all the figures of
qa/<batch>/overlays.csv from that source (a record may span several figures: the impact runs of Figs. 4-19
and 4-20, so its figures are built together), with qa/<batch>/series-map.csv and panel-map.csv and the calibrations the points were derived with:
qa/<batch>/rederived/<reader>/<figure>/ (tools/reconcile_curves.py, D-025). The source is the
figure's source in the corpus (bendix-1968-vol2 for figures of Volume II). One command per batch, so
the records can be regenerated from the repository alone.
"""
import argparse
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = {"1968": "bendix-1968-vol1", "1968-vol2": "bendix-1968-vol2"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch")
    ap.add_argument("--out", default="data/experiments")
    a = ap.parse_args()
    q = ROOT / "qa" / a.batch
    with (q / "overlays.csv").open(encoding="utf-8-sig", newline="") as f:
        ovs = list(csv.DictReader(f))
    figs = list(dict.fromkeys(o["figure_id"] for o in ovs))
    by_source = {}
    for fid in figs:
        corpus = Path(next(o["image"] for o in ovs if o["figure_id"] == fid)).parts[1]
        by_source.setdefault(SOURCE[corpus], []).append(fid)
    for source, fids in by_source.items():
        cmd = [sys.executable, str(ROOT / "tools" / "build_observations.py"), str(q / "canonical.csv"),
               "--figure", *fids, "--source", source, "--series-map", str(q / "series-map.csv"),
               "--panel-map", str(q / "panel-map.csv"), "--cal-a", *(str(q / "rederived" / "claude" / f) for f in fids),
               "--cal-b", *(str(q / "rederived" / "codex" / f) for f in fids), "--batch", a.batch, "--out", a.out]
        if (q / "breaks.csv").exists():   # explicit breaks of a drawn line (a scan dropout), from 2026-11-19
            cmd += ["--breaks", str(q / "breaks.csv")]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if r.returncode:
            sys.exit(f"{' '.join(fids)}: tools/build_observations.py failed\n{r.stderr}")
        print(r.stdout.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
