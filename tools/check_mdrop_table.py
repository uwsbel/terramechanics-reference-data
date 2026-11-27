"""Check the touchdown velocities of Table 5-T3 (the detail correlation drops) against the equation |V_v| = g tau,
the speed of a free fall from rest over the printed time tau from release to touchdown.

    python tools/check_mdrop_table.py tables-s5-b1

The report says only that the velocities "were calculated based on the exact time interval between the instant of
model release to the instant of ground contact" (AM-68-1 Vol. I, printed 5-44, PDF 324); it prints no formula. This
check asks one question per drop: does |V_v| fall inside the interval g * tau takes over the rounding of the printed
tau (half a unit of its last digit), allowing |V_v| its own printed rounding? A drop that fits is consistent with
that equation; one that does not is inconsistent with it. Consistency is not the authors' method, which the report
does not state. It shows the printed columns consistent with each other or not; it does not show a transcription
right, and it is our arithmetic, not the report's. A drop with a cell that is not a number (no agreed value, or an
unreadable `?`) is listed as `unreadable` and left out of the counts.

Two values of g, because the verdicts depend on which one is used at this precision (Codex's review, 2026-11-20):
the report's own value for Earth, 32.2 ft/s^2 (its glossary, AM-68-1 Vol. I, printed 2-2, PDF 27), first, and
standard gravity, 9.80665 m/s^2, second. The two differ by 0.08 percent, about the rounding of a printed tau.

Writes qa/<batch>/arithmetic-checks.csv (one row per drop and value of g; verdict `consistent`, `differs` or
`unreadable`, none of which marks a run in runs.csv `check`), arithmetic.json (the summary
tools/build_run_table.py copies into runs.json: the report's g at the top level, standard gravity under `standard`)
and arithmetic.md.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from to_si import G0  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
G_STD_IN_S2 = G0 / 0.0254   # standard gravity in in./sec.^2 (386.0886), the table's units
G_REPORT_IN_S2 = 32.2 * 12  # the report's g for Earth, 32.2 ft/s^2 (glossary, printed 2-2, PDF 27), in in./sec.^2
GS = [("report", G_REPORT_IN_S2, "g = 32.2 ft/s^2, the report's value for Earth (glossary, printed 2-2, PDF 27)"),
      ("standard", G_STD_IN_S2, "g = standard gravity, 9.80665 m/s^2")]


def half_unit(s):
    """Half a unit of the last printed digit ('.298' -> 0.0005, '-114.9' -> 0.05, '0' -> 0.5)."""
    s = s.strip().lstrip("+-")
    return 0.5 * 10 ** -(len(s.split(".")[1]) if "." in s else 0)


def main():
    batch = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    q = ROOT / "qa" / batch
    rows = list(csv.DictReader(open(q / "agreed.csv", encoding="utf-8-sig", newline="")))
    out, sides = [], {}
    for name, g, label in GS:
        summary = {"vertical": [], "with_vh": []}
        for r in rows:
            tau, vv, vh = r["tau_s"], r["VV_in_s"], r["Vh_in_s"]
            check = f"|V_v| against g tau, {label}"
            try:
                float(tau), float(vv), float(vh)
            except ValueError:   # a pending or unreadable cell: no verdict
                out.append({"run_number": r["nasa_test_no"], "check": check, "computed": "", "printed": vv,
                            "tolerance": "", "verdict": "unreadable"})
                continue
            t, dt = float(tau), half_unit(tau)
            lo, hi = g * (t - dt), g * (t + dt)
            v, dv = abs(float(vv)), half_unit(vv)
            fits = (v + dv) >= lo and (v - dv) <= hi
            out.append({"run_number": r["nasa_test_no"], "check": check,
                        "computed": f"{g * t:.3f} ({lo:.3f} to {hi:.3f})", "printed": vv.lstrip("-"),
                        "tolerance": f"{dv:g}", "verdict": "consistent" if fits else "differs"})
            (summary["vertical"] if float(vh) == 0 else summary["with_vh"]).append(
                {"run": r["nasa_test_no"], "g_tau_in_s": round(g * t, 2), "VV_in_s": vv, "fits": fits})
        sides[name] = {"g_in_s2": round(g, 4), "g": label,
                       "vertical_fit": sum(x["fits"] for x in summary["vertical"]), "vertical": len(summary["vertical"]),
                       "with_vh_fit": sum(x["fits"] for x in summary["with_vh"]), "with_vh": len(summary["with_vh"]),
                       "drops_detail": summary["vertical"] + summary["with_vh"]}
    with (q / "arithmetic-checks.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    side = {"table": f"qa/{batch}/agreed.csv", "drops": len(rows), **sides["report"], "standard": sides["standard"]}
    (q / "arithmetic.json").write_text(json.dumps(side, indent=1) + "\n", encoding="utf-8", newline="\n")
    md = [f"# Arithmetic check of Table 5-T3: touchdown velocity against |V_v| = g tau (batch {batch})", "",
          "Written by `tools/check_mdrop_table.py`; our arithmetic, not the report's. A drop fits when |V_v| (with half "
          "a unit of its last printed digit) meets the interval g tau takes over the rounding of the printed tau. Two "
          "values of g, since the verdicts depend on which is used at this precision.", ""]
    for name, g, label in GS:
        sd = sides[name]
        md += [f"## {label} ({g:.4f} in./sec.^2)", "",
               "| NASA test | V_h printed | tau printed | g tau (in./sec.) | interval | abs V_v printed | verdict |",
               "| --- | --- | --- | --- | --- | --- | --- |"]
        for r, o in zip(rows, [o for o in out if o["check"].endswith(label)]):
            if o["verdict"] == "unreadable":
                md.append(f"| {r['nasa_test_no']} | {r['Vh_in_s']} | {r['tau_s']} |  |  | {o['printed']} | unreadable |")
                continue
            gt, rng = o["computed"].split(" (")
            md.append(f"| {r['nasa_test_no']} | {r['Vh_in_s']} | {r['tau_s']} | {gt} | {rng.rstrip(')')} | {o['printed']} | {o['verdict']} |")
        fit_vh = [x["run"] for x in sd["drops_detail"][sd["vertical"]:] if x["fits"]]
        md += ["", f"Vertical drops (V_h 0): {sd['vertical_fit']} of {sd['vertical']} are consistent with |V_v| = g tau "
               f"within both printed roundings. Drops with a horizontal velocity: {sd['with_vh_fit']} of {sd['with_vh']}"
               + (f" (NASA Test No. {', '.join(fit_vh)})" if fit_vh else "") + ".", ""]
    md += ["Consistency is not the method: the report says the velocities were calculated using the measured interval "
           "tau and prints no formula.", ""]
    (q / "arithmetic.md").write_text("\n".join(md), encoding="utf-8", newline="\n")
    for name, _, _ in GS:
        sd = sides[name]
        print(f"{name}: vertical drops consistent with g tau: {sd['vertical_fit']} of {sd['vertical']}; "
              f"with V_h: {sd['with_vh_fit']} of {sd['with_vh']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
