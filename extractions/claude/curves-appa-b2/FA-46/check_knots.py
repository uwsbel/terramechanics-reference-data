import sys, json
sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(sys.argv[2], sys.argv[3])
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    print("==", ax)
    for kn in s[ax]:
        ck = kn["ink_check"]
        print(f"  {kn['value']:>6g} s0={kn['s0_px']:9.2f} tilt={kn['tilt']:+.5f} err={kn['location_error_px']:.2f} n={kn['n_anchors']} "
              f"found={len(ck.get('found', []))}/{ck.get('positions')} span={ck.get('span_fraction')} inkoff={ck.get('ink_line_offset_px')} scat={ck.get('ink_scatter_px')} aside={ck.get('set_aside')} {kn.get('reason','')}")
