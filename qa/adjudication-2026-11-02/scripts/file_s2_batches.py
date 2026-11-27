"""File the blind readings of curves-s2-b1 and -b2 into extractions/ (both agents), after both have finished.
Adapted from qa/adjudication-2026-10-15/scripts/file_batch.py for the 2026-11-02 locations. --dry-run lists sizes only."""
import json
import shutil
import sys
from pathlib import Path

BL = Path(r"<local path>")
REPO = Path(r"<repository>")
SKIP_EXT = {".png", ".jpg", ".zip", ".pyc", ".npy"}
SKIP_DIRS = {"__pycache__", "crops", "crops2", "crops3", "views", "checks", "tmp", "ov"}
DRY = "--dry-run" in sys.argv

B2_SP = BL / "curves-s2-b2" / "claude-scratchpad-20261030"
B2_READERS = {
    "F2-45": {"reader": "one subagent for F2-45 (claude-opus-5-5), resuming the 2026-10-30 workspace",
              "elapsed_sec": 1324.6, "subagent_tokens": 291423, "tool_uses": 119,
              "note": "redid everything (calibration, tracing, samples, features, overlay); the earlier reader's calibration box cut the left frame and is kept in earlier-reader/cal-p1; its helpers were rewritten, none of its outputs used"},
    "F2-46": {"reader": "one subagent for F2-46 (claude-opus-5-5), checking and finishing the 2026-10-30 reading",
              "elapsed_sec": 939.2, "subagent_tokens": 239479, "tool_uses": 86,
              "note": "kept the calibration (detect rerun gave identical anchors), all 50 trace samples and 14 features after checking each on the page; added 2 kinks; wrote eye checks and notes; earlier finals kept in work/ with suffix -earlier"},
    "F2-47": {"reader": "one subagent for F2-47 (claude-opus-5-5), resuming the 2026-10-30 workspace",
              "elapsed_sec": 1460.9, "subagent_tokens": 310399, "tool_uses": 97,
              "note": "reused cal-p1 after a byte-identical detect rerun; all tracing redone with its own helpers (helpers2/); the earlier reader produced no points"},
    "F2-48": {"reader": "one subagent for F2-48 (claude-opus-5-5), checking and finishing the 2026-10-30 reading",
              "elapsed_sec": 1175.2, "subagent_tokens": 286521, "tool_uses": 100,
              "note": "kept the calibration and all 63 trace samples after checking each on the page; moved one knee, added one knee and trace rows at the ink ends, recentered a plateau maximum, widened several bounds"},
}
PACKET = ("written by tools/make_reading_packet.py from qa/{b}/batch.json: page images, figures-rows.csv without the "
          "agents' notes columns, series.csv, CURVE-READING.md, tools/calibrate_axes.py, tools/plot_grid.py")
BATCHES = {
    "curves-s2-b1": {
        "claude_fig": lambda f: BL / "curves-s2-b1" / "claude" / f,
        "claude_task": BL / "curves-s2-b1" / "claude" / "TASK.md",
        "codex_run": BL / "curves-s2-b1" / "codex-run-20261031",
        "claude_meta": {
            "agent": "claude", "batch": "curves-s2-b1", "date": "2026-10-30",
            "model": "claude-fable-5-1 (subagents launched from a Claude Code session, one per figure)",
            "prompt": "TASK.md plus a task naming the workspace and the figure of each reader",
            "evidence_packet": PACKET.format(b="curves-s2-b1"),
            "blindness": "workspaces outside the repository; the task forbids opening the repository, the Codex run folder and other scratchpad folders; read before any Codex reading existed; filed after the Codex run had finished",
            "readers": {f: {"reader": f"one subagent for {f}"} for f in ("F2-29", "F2-32", "F2-33", "F2-34")}},
        "codex_note": "reading of record: the first complete run (2026-10-31 02:54, through the session relay of dan-codex-from-claude 2dca7b1). Three earlier attempts on 2026-10-30 failed before running any command (runner pipe-in timeout; their answers are kept outside the repository). A second complete run from the identical prompt and packet was made by mistake on 2026-11-02 and is kept outside the repository as a replicate (terramechanics-blind/curves-s2-b1/codex-run-20261102-replicate); it plays no part in reconciliation, a rule fixed before either run was compared with anything.",
    },
    "curves-s2-b2": {
        "claude_fig": lambda f: B2_SP / f / "out" / f,
        "claude_task": B2_SP / "TASK.md",
        "codex_run": BL / "curves-s2-b2" / "codex-run-20261031",
        "claude_meta": {
            "agent": "claude", "batch": "curves-s2-b2", "date": "2026-11-02",
            "model": "claude-opus-5-5 (subagents launched from a Claude Code session, one per figure); the interrupted 2026-10-30 start by claude-fable-5-1 subagents",
            "prompt": "TASK.md plus a task naming the workspace, the figure, and what the interrupted 2026-10-30 reader had left in it",
            "evidence_packet": PACKET.format(b="curves-s2-b2"),
            "blindness": "workspaces outside the repository; the task forbids opening the repository, the Codex run folder and other folders. Started 2026-10-30 before any Codex reading existed and interrupted (F2-46 and F2-48 had points, F2-45 and F2-47 calibrations only); finished 2026-11-02 by fresh subagents in the same workspaces, after the Codex reading existed. Before launching them the orchestrating session had read the Codex run's final summary (counts per series, calibration residuals, the ambiguities it listed); the briefs carried none of it, and each reader reports opening nothing outside its workspace and TASK.md. Filed after both had finished.",
            "readers": B2_READERS},
        "codex_note": "the first and only Codex run (2026-10-31 02:54, through the session relay of dan-codex-from-claude 2dca7b1)",
    },
}


def files(src):
    for p in sorted(src.rglob("*")):
        rel = p.relative_to(src)
        if p.is_dir() or p.suffix.lower() in SKIP_EXT or any(part in SKIP_DIRS for part in rel.parts):
            continue
        yield p, rel


def copy_tree(src, dst):
    n = size = 0
    for p, rel in files(src):
        n += 1
        size += p.stat().st_size
        if not DRY:
            t = dst / rel
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t)
    return n, size


for batch, c in BATCHES.items():
    cfg = json.loads((REPO / "qa" / batch / "batch.json").read_text(encoding="utf-8"))
    figs = list(cfg["figures"])
    run = c["codex_run"]
    m = json.loads((run / "meta.json").read_text(encoding="utf-8-sig"))
    assert m["codex_exit_code"] == 0 and m["answer_present"], f"{batch}: the Codex run has not finished cleanly"
    for fid in figs:
        for d in (c["claude_fig"](fid), run / "work" / "out" / fid):
            for need in ("points-p1-native.csv", "points-p1.csv", "notes.md", "calibration-eye-checks.csv"):
                assert (d / need).exists(), f"missing {need}: {d}"
    cdst, xdst = REPO / "extractions/claude" / batch, REPO / "extractions/codex" / batch
    assert not cdst.exists() and not xdst.exists(), f"{batch} already filed"
    for fid in figs:
        n, s = copy_tree(c["claude_fig"](fid), cdst / fid)
        print(f"{batch} claude {fid}: {n} files, {s / 1e6:.2f} MB")
    n, s = copy_tree(run / "work" / "out", xdst)
    print(f"{batch} codex: {n} files, {s / 1e6:.2f} MB")
    if DRY:
        continue
    shutil.copy2(c["claude_task"], cdst / "TASK.md")
    (cdst / "meta.json").write_text(json.dumps(c["claude_meta"], indent=2) + "\n", encoding="utf-8")
    for f in ("prompt.md", "codex-answer.md"):
        shutil.copy2(run / f, xdst / f)
    m["filing_note"] = c["codex_note"]
    (xdst / "meta.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
    print("filed", batch)
