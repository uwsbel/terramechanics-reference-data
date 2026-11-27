"""File the blind readings of one curve batch into extractions/ (both agents), after both have finished.
Usage: file_batch.py <batch> <codex run dir name> <claude readers json>
<claude readers json>: {"FC-8": {"reader": "one subagent for FC-8 to FC-10A", "elapsed_sec": .., "tokens": .., "tool_uses": ..}, ...}"""
import json
import shutil
import sys
from pathlib import Path

SP = Path(r"<local path>")
CX = Path(r"<local path>")
REPO = Path(r"<repository>")
SKIP_EXT = {".png", ".jpg", ".zip", ".pyc"}
SKIP_DIRS = {"__pycache__", "crops", "crops2"}
batch, run_name, readers = sys.argv[1], sys.argv[2], json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
cfg = json.loads((REPO / "qa" / batch / "batch.json").read_text(encoding="utf-8"))
figs = list(cfg["figures"])
date = run_name[:8]
date = f"{date[:4]}-{date[4:6]}-{date[6:]}"


def copy_tree(src, dst):
    n = 0
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        if p.is_dir() or p.suffix.lower() in SKIP_EXT or any(part in SKIP_DIRS for part in rel.parts):
            continue
        t = dst / rel
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, t)
        n += 1
    return n


run = CX / run_name
m = json.loads((run / "meta.json").read_text(encoding="utf-8-sig"))
assert m["codex_exit_code"] == 0 and m["answer_present"], "the Codex run has not finished cleanly"
for fid in figs:
    for d in (SP / "blind" / batch / fid / "out" / fid, run / "work" / "out" / fid):
        assert (d / "points-p1-native.csv").exists(), f"missing points: {d}"
cdst, xdst = REPO / "extractions/claude" / batch, REPO / "extractions/codex" / batch
assert not cdst.exists() and not xdst.exists(), f"{batch} already filed"
for fid in figs:
    print(f"claude {fid}: {copy_tree(SP / 'blind' / batch / fid / 'out' / fid, cdst / fid)} files")
shutil.copy2(SP / "blind" / batch / "TASK.md", cdst / "TASK.md")
meta = {"agent": "claude", "batch": batch, "date": date,
        "model": "claude-opus-5-5 (subagents launched from a Claude Code session)",
        "prompt": "TASK.md plus a task naming the workspace and the figures of each reader",
        "evidence_packet": f"written by tools/make_reading_packet.py from qa/{batch}/batch.json: page images, figures-rows.csv without the agents' notes columns, series.csv, CURVE-READING.md, tools/calibrate_axes.py, tools/plot_grid.py",
        "blindness": "workspaces outside the repository; the task forbids opening the repository, the Codex run folder and other scratchpad folders; filed after the Codex run had finished",
        "readers": readers}
(cdst / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
print(f"codex: {copy_tree(run / 'work' / 'out', xdst)} files")
for f in ("prompt.md", "codex-answer.md"):
    shutil.copy2(run / f, xdst / f)
(xdst / "meta.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
print("filed", batch)
