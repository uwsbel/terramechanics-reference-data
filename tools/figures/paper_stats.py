"""Counts and statistics quoted in the data paper, computed from the repository, never typed.

    python tools/figures/paper_stats.py [--tex <macros.tex>] [--md <summary.md>] [--soils <table.tex>]

Reads sources/register.csv, the corpus page files and figure indexes, data/experiments (index,
observations, series sidecars), the batch diff reports and ink checks under qa/, the audit record
(qa/audits.csv, qa/audits/returns-log.csv) and two adjudication records (the 2026-10-27 re-check of
the disputed audit points, the 2026-10-28 validation of the off-ink check). Writes LaTeX macros
(\\statName{value}) for the manuscript and a Markdown summary, both stamped with the commit they were
computed at. Every number in the paper is regenerated from release v1.0 with this script before
submission. Standard library only.
"""
import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from ingest_review import pair_outcome  # noqa: E402  the audit's own rule for a point's outcome


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout.strip()


def page_header(path):
    """A page file's review status and the number of differences between its two transcriptions."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^review_status:\s*(\S+)", text, re.M)
    d = re.search(r"^differences:\s*(\d+)", text, re.M)
    return (m.group(1) if m else "missing"), (int(d.group(1)) if d else None)


def compute():
    s = {}
    s["Commit"] = git("rev-parse", "--short=10", "HEAD")
    s["Dirty"] = "yes" if git("status", "--porcelain", "--untracked-files=no") else "no"

    # Sources and corpus
    reg = rows(ROOT / "sources/register.csv")
    st = Counter(r["status"] for r in reg)
    s["SourcesRegistered"] = len(reg)
    s["SourcesAcquired"] = st["acquired"]
    diffs = []
    for key, folder in (("VolI", "1968"), ("VolII", "1968-vol2")):
        pages = sorted((ROOT / "corpus" / folder / "pages").glob("p*.md"))
        heads = [page_header(p) for p in pages]
        ps = Counter(h[0] for h in heads)
        diffs += [h[1] for h in heads if h[1] is not None]
        s[f"Pages{key}"] = len(pages)
        s[f"PagesPending{key}"] = ps["pending"]
        fig = rows(ROOT / "corpus" / folder / "figures.csv")
        s[f"FigIndex{key}"] = len(fig)
        s[f"FigInScope{key}"] = sum(r["in_scope"] == "yes" for r in fig)
    s["PagesTotal"] = s["PagesVolI"] + s["PagesVolII"]
    s["PagesWithDiffCount"] = len(diffs)
    s["PagesNoDiff"] = sum(d == 0 for d in diffs)
    s["PageDiffsTotal"] = sum(diffs)

    # Experiment index
    idx = rows(ROOT / "data/experiments/index.csv")
    s["Records"] = len(idx)
    kinds = Counter(r["kind"] for r in idx)
    for k, name in (("single", "Single"), ("averaged-series", "Averaged"), ("derived-series", "Derived"),
                    ("correlation", "Correlation"), ("summary", "Summary"), ("sample", "Sample")):
        s[f"Kind{name}"] = kinds[k]
    single = [r for r in idx if r["kind"] == "single"]
    tt = Counter(r["test_type"] for r in single)
    for t in ("lpt", "ds", "dpt", "dens", "sonic", "gs", "tx"):
        s[f"Single{t.capitalize()}"] = tt[t]
    s["SetupComplete"] = sum(r["setup_status"] == "complete" for r in idx)
    rel = Counter(r["relation"] for r in idx if r["relation"])
    s["RelSameAs"] = rel["same-as"]
    s["RelDerivedFrom"] = rel["derived-from"]  # rows; each row may name several targets
    s["RelDerivedFromTargets"] = len({x.strip() for r in idx if r["relation"] == "derived-from"
                                      for x in r["relation_target"].split(";") if x.strip()})
    s["RelDerivedFromLinks"] = sum(len([x for x in r["relation_target"].split(";") if x.strip()])
                                   for r in idx if r["relation"] == "derived-from")
    s["SetupIncomplete"] = sum(r["setup_status"] == "setup_incomplete" for r in idx)
    s["SetupPending"] = sum(r["setup_status"] == "pending" for r in idx)

    # Observations
    status, kind, figs, lpt_points = Counter(), Counter(), set(), 0
    with_obs, single_with_obs, obs_keys = 0, Counter(), set()
    by_id = {r["experiment_id"]: r for r in idx}
    for obs in sorted((ROOT / "data/experiments").glob("*/observations.csv")):
        with_obs += 1
        pts = rows(obs)
        rec = by_id.get(obs.parent.name, {})
        if rec.get("kind") == "single":
            single_with_obs[rec.get("test_type")] += 1
        status.update(p["status"] for p in pts)
        kind.update(p["point_kind"] for p in pts)
        if by_id.get(obs.parent.name, {}).get("test_type") == "lpt":
            lpt_points += len(pts)
        sj = obs.parent / "series.json"
        if sj.exists():
            meta = json.loads(sj.read_text(encoding="utf-8"))
            for ser in meta.get("series", [meta]) if isinstance(meta, dict) else meta:
                f = ser.get("figure_id") or ser.get("figure")
                if f:
                    figs.add(f)
                figs.update(ser.get("figures", []))   # a record read from several figures (Figs. 4-19 and 4-20)
            # the audit names a point <figure>/<panel>/<series>/<kind>/<source>/<sequence> with the printed figure's own
            # panel; a record from several figures numbers its panels across them (series.json panels: figure_id,
            # figure_panel), so its keys use each panel's figure and figure panel (Codex's review, 2026-11-19)
            pan = meta.get("panels", {}) if isinstance(meta, dict) else {}
            fig_of = lambda p: (pan.get(p["panel"], {}).get("figure_id") or meta.get("figure_id"),
                                pan.get(p["panel"], {}).get("figure_panel") or p["panel"])
            obs_keys.update("{}/{}/{}/{}/{}/{}".format(*fig_of(p), p["series_id"], p["point_kind"], p["source"], p["sequence"])
                            for p in pts)
    s["WithObs"] = with_obs
    s["SingleLptWithObs"] = single_with_obs["lpt"]
    s["SingleDsWithObs"] = single_with_obs["ds"]
    sonic = [float(p["x_si"]) for obs in (ROOT / "data/experiments").glob("b68-sonic-*/observations.csv")
             for p in rows(obs) if p["point_kind"] == "marker"]
    s["SonicMaxConfiningkPa"] = f"{max(sonic) / 1000:.0f}" if sonic else "n/a"  # highest measured confining pressure
    s["SetupFiles"] = len(list((ROOT / "data/experiments").glob("*/setup.json")))
    s["Points"] = sum(status.values())
    s["PointsLpt"] = lpt_points
    for k, name in (("agreed", "Agreed"), ("resolved", "Resolved"), ("one-sided-verified", "OneSidedVerified"),
                    ("one-sided", "OneSided"), ("pending-review", "PendingReview"), ("confirmed", "Confirmed"),
                    ("audited", "Audited")):
        s[f"Pts{name}"] = status[k]
    s["PtsOtherStatus"] = s["Points"] - sum(status[k] for k in ("agreed", "resolved", "one-sided-verified", "one-sided",
                                                                  "pending-review", "confirmed", "audited"))
    for k in ("marker", "trace", "feature", "gridline"):
        s[f"Pts{k.capitalize()}"] = kind[k]
    s["FiguresRead"] = len(figs)
    s["CurveBatches"] = len([p for p in (ROOT / "qa").glob("curves-*") if p.is_dir() and "rederivation" not in p.name])

    # Agreement of the two readings, from the batch diff reports (before adjudication)
    m = Counter()
    panels = 0
    for rep in sorted((ROOT / "qa").glob("curves-*/diff-*.md")):
        for line in rep.read_text(encoding="utf-8").splitlines():
            mm = re.match(r"Matched: (\d+); agreed (\d+); disagreed (\d+); unmatched (\d+)", line)
            if mm:
                panels += 1
                m.update(dict(zip(("matched", "agreed", "disagreed", "unmatched"), map(int, mm.groups()))))
    s["DiffPanels"] = panels
    s["DiffMatched"], s["DiffAgreed"] = m["matched"], m["agreed"]
    s["DiffDisagreed"], s["DiffUnmatched"] = m["disagreed"], m["unmatched"]
    s["DiffAgreedPct"] = f"{100 * m['agreed'] / m['matched']:.1f}" if m["matched"] else "n/a"

    # Off-ink check (D-031, D-032): verdicts over both readings' trace samples, and its blind validation
    ink = Counter()
    for f in sorted((ROOT / "qa").glob("curves-*/ink-checks.csv")):
        ink.update(r["verdict"] for r in rows(f))
    s["InkChecked"] = sum(ink.values())
    s["InkExcluded"], s["InkReview"] = ink["excluded"], ink["review"]
    val = rows(ROOT / "qa/adjudication-2026-10-28-inkrule/validation-results.csv")
    settled_ex = [r for r in val if r["verdict"] == "excluded" and r["truth"] in ("on", "off")]
    s["InkValItems"] = len(val)
    s["InkValExcludedSampled"] = sum(r["verdict"] == "excluded" for r in val)
    s["InkValUnsettled"] = sum(r["truth"] == "unsettled" for r in val)
    s["InkValExcludedSettled"] = len(settled_ex)
    s["InkValExcludedRight"] = sum(r["truth"] == "off" for r in settled_ex)

    # Re-check of the disputed points of audit wave 1 (qa/adjudication-2026-10-27)
    fd = rows(ROOT / "qa/adjudication-2026-10-27/final-decisions.csv")
    s["RecheckItems"] = len(fd)
    alld = Counter(r["decision"] for r in fd)
    s["RecheckKeep"], s["RecheckSwitch"], s["RecheckOffInk"] = alld["keep"], alld["switch"], alld["off-ink trace"]
    s["RecheckOutsideBox"], s["RecheckUnresolved"], s["RecheckSplit"] = alld["outside box"], alld["unresolved"], alld["split"]
    flagged = [r for r in fd if r["review_outcome"] == "flagged"]
    dec = Counter(r["decision"] for r in flagged)
    s["RecheckFlagged"] = len(flagged)
    s["RecheckFlaggedOffInk"] = dec["off-ink trace"]
    s["RecheckFlaggedSwitch"] = dec["switch"]
    s["RecheckFlaggedWrong"] = dec["off-ink trace"] + dec["switch"]
    s["RecheckFlaggedKeep"] = dec["keep"]

    # Human audits
    aud = rows(ROOT / "qa/audits.csv")
    s["AuditRows"] = len(aud)
    s["AuditReviewers"] = len({r["auditor"] for r in aud})
    per = defaultdict(dict)
    for r in aud:
        per[r["object"]][r["auditor"]] = r["outcome"]
    oc = Counter()
    for v in per.values():
        o = pair_outcome(list(v.values()))
        oc["single" if o.startswith("single") else o] += 1
    s["AuditPoints"] = len(per)  # distinct point ids with a recorded answer, as named when they were audited
    s["AuditPointsInRelease"] = sum(o in obs_keys for o in per)  # of those, still a point of the release
    # split is a real contradiction (ok against problem) since 2026-11-23; a mix whose definite answers agree beside a
    # cannot tell is counted apart, and any other mix (an unreadable answer beside a definite one) as AuditMixOther
    for k, name in (("confirmed", "Confirmed"), ("flagged", "Flagged"), ("split", "Split"),
                    ("cannot-tell", "CannotTell"), ("ok + cannot tell", "OkCannotTell"),
                    ("problem + cannot tell", "ProblemCannotTell"), ("single", "Single")):
        s[f"Audit{name}"] = oc[k]
    named = {"confirmed", "flagged", "split", "cannot-tell", "ok + cannot tell", "problem + cannot tell", "single"}
    s["AuditMixOther"] = sum(v for k, v in oc.items() if k not in named)
    s["AuditTwoOrMore"] = s["AuditPoints"] - oc["single"]
    log = rows(ROOT / "qa/audits/returns-log.csv")
    ctl = Counter(r["controls"] for r in log)
    s["ChunksReturned"] = len(log)  # returns (one reviewer, one chunk)
    s["ChunksDistinct"] = len({r["chunk"] for r in log})
    s["ChunksControlsPassed"] = ctl["passed"]
    s["ChunksDeclined"] = ctl["declined"]
    s["ChunksAccepted"] = ctl["accepted"]
    return s


def write_tex(s, path):
    out = [f"% Generated by tools/figures/paper_stats.py at commit {s['Commit']} (dirty: {s['Dirty']}). Do not edit;",
           "% regenerate from release v1.0 before submission."]
    for k, v in s.items():
        out.append(f"\\newcommand{{\\stat{k}}}{{{v}}}")
    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def write_soils(path, commit):
    """Table of the twelve test soils (Vol. I Table 2-3) with the Appendix A values that differ from it."""
    spec = defaultdict(dict)
    for r in rows(ROOT / "data/materials/specifications.csv"):
        if r["quantity"] in ("friction_angle", "elastic_modulus"):
            spec[r["soil_no"]][r["quantity"]] = r
    out = [f"% Generated by tools/figures/paper_stats.py --soils at commit {commit}. Do not edit.",
           r"\begin{tabular}{rllrrrr}", r"\toprule",
           r"No. & Designation & $D_r$ & Bulk density, kg/m$^3$ (unit weight, pcf) & $\phi$, deg & App.~A $\phi$, deg & $E$, MPa (psi) \\",
           r"\midrule"]
    for r in rows(ROOT / "data/materials/materials.csv"):
        sp = spec.get(r["soil_no"], {})
        phi_a = sp.get("friction_angle", {}).get("value_native", "")
        phi_a = phi_a if phi_a and float(phi_a) != float(r["friction_angle_deg"]) else "same"
        e = sp.get("elastic_modulus", {})
        est = r"$^{\dagger}$" if e.get("qualifier", "").startswith("estimated") else ""
        out.append(f"{r['soil_no']} & {r['bendix_designation']} & {r['relative_density']} & "
                   f"{float(r['bulk_density_kg_m3']):.0f} ({r['unit_weight_native']}) & {r['friction_angle_deg']} & {phi_a} & "
                   f"{float(r['elastic_modulus_Pa']) / 1e6:.1f} ({r['elastic_modulus_native']}){est} \\\\")
    out += [r"\bottomrule", r"\end{tabular}"]
    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def write_md(s, path):
    out = [f"# Paper statistics at commit {s['Commit']} (uncommitted changes in tracked files: {s['Dirty']})", "",
           "| macro | value |", "|---|---|"]
    out += [f"| \\stat{k} | {v} |" for k, v in s.items()]
    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tex")
    ap.add_argument("--md")
    ap.add_argument("--soils", help="write the soils table (LaTeX tabular) to this path")
    a = ap.parse_args()
    s = compute()
    if a.tex:
        write_tex(s, a.tex)
    if a.soils:
        write_soils(a.soils, s["Commit"])
    if a.md:
        write_md(s, a.md)
    for k, v in s.items():
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
