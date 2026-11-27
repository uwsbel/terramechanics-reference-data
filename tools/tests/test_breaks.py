"""Checks of a documented break in a drawn line in the comparison (tools/diff_curves.py --break, from batch
curves-s5-b1, 2026-11-19): the other reading is never interpolated across a break, a sample beside it is compared with
the other reading's end sample on its own side only, a sample inside the break has no side, and bad limits stop the
run with exit status 2.

Run: python tools/tests/test_breaks.py (from the repository root or this folder).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import diff_curves as dc  # noqa: E402


def check(ok, what):
    print(("ok    " if ok else "FAIL  ") + what)
    return ok


def row(seq, x, y, bx=0.005, by=0.1):
    return {"panel": "1", "series_id": "s", "point_kind": "trace", "sequence": str(seq), "x_native": str(x),
            "y_native": str(y), "x_read_bound": str(bx), "y_read_bound": str(by), "pixel_u": str(100 * x),
            "pixel_v": str(10 * y)}


def main():
    dc.AXES = ("linear", "linear")
    ok = True
    # the other reading has samples at 0.98 and 1.03 on either side of a break from 1.00 to 1.01 (Codex's example)
    other = [row(1, 0.90, 9.0), row(2, 0.98, 9.8), row(3, 1.03, 10.3), row(4, 1.10, 11.0)]
    marked = dc.mark_breaks(other, [("s", "1.00", "1.01")])
    ok &= check([r.get("_scan_break", "") != "" for r in marked] == [False, False, True, False],
                "only the step across the break is marked")
    # the end sample on the wrong side is the nearer one here: 0.995 is 0.025 from a sample at 1.02, 1.06 is 0.04
    far = dc.mark_breaks([row(1, 0.90, 9.0), row(2, 0.995, 9.95), row(3, 1.06, 10.6), row(4, 1.10, 11.0)],
                         [("s", "1.00", "1.01")])
    it = dc.interp_trace(far, 1.02, 0.5, reach=0.05)
    ok &= check(it is not None and it[0] == 10.6 and it[6] == 1.06,
                "a sample at 1.02 is compared with the end sample on its own side (1.06), not the nearer 0.995")
    it = dc.interp_trace(far, 0.99, 0.5, reach=0.05)
    ok &= check(it is not None and abs(it[0] - 9.9) < 1e-9 and it[6] == 0.99,
                "a sample at 0.99 is interpolated on the intact step before the break (0.90 to 0.995)")
    it = dc.interp_trace(marked, 0.985, 0.5, reach=0.005)
    ok &= check(it is not None and it[0] == 9.8 and it[6] == 0.98, "a sample at 0.985 is compared with 0.98")
    ok &= check(dc.interp_trace(marked, 1.005, 0.5, reach=0.005) is None, "a sample inside the break has no side")
    ok &= check(dc.interp_trace(marked, 0.995, 0.5, reach=0.001) is None,
                "an end sample beyond the bounds is not used (0.995 against 0.98, reach and bound 0.006)")
    it = dc.interp_trace(dc.mark_breaks(other, []), 1.02, 0.5, reach=0.005)
    ok &= check(it is not None and abs(it[0] - 10.2) < 1e-9 and it[6] == 1.02, "without a break the step is interpolated")
    # two breaks in one step: the step carries the outer limits of both, whatever their order (Codex's review)
    two = [row(1, 0.98, 9.8), row(2, 1.13, 11.3)]
    for order in ([("s", "1.00", "1.01"), ("s", "1.10", "1.12")], [("s", "1.10", "1.12"), ("s", "1.00", "1.01")]):
        ok &= check(dc.interp_trace(dc.mark_breaks(two, order), 1.11, 0.5, reach=0.05) is None,
                    f"a sample at 1.11, inside the second of two breaks in one step, has no side (order {order[0][1]} first)")
    for bad in (("s", "1.01", "1.00"), ("s", "nan", "1.0"), ("t", "1.00", "1.01")):
        try:
            dc.mark_breaks(other, [bad])
            ok &= check(False, f"break {bad} is refused")
        except SystemExit as e:
            ok &= check(e.code == 2, f"break {bad} is refused with exit status 2")
    print("all checks passed" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
