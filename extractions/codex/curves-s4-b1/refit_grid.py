"""Refit the visible grid lines in the packet and write label-to-grid checks."""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path.cwd() / "tools"))
from calibrate_axes import fit_affine, intersect, piecewise_maps

ROOT = Path("out")
PLOTS = (
    ("F4-19", 1, "packet/p0208.png"),
    ("F4-19", 2, "packet/p0208.png"),
    ("F4-20", 1, "packet/p0209.png"),
)
# Time labels as transcribed visually, left to right, separately for both panels.
TIME_PRINTED = {
    1: [0,10,20,30,40,50,60,70,80,90,100,120,130,140,None],
    2: [0,10,20,30,40,50,60,70,80,90,100,120,130,140,None],
}
TIME_CENTRES = {
    1: [297,343,388,443,484,535,585,632,680,727,777,827,882,924,None],
    2: [296,348,396,446,495,538,591,642,691,740,789,837,886,932,None],
}

def continuous_measure(gray, box, direction, line, exclusion):
    u0, v0, u1, v1 = box
    if direction == "horizontal":
        t0, t1 = u0, u1
        m, b = line["slope_dv_du"], line["v_at_u0"]
    else:
        gray = gray.T
        t0, t1 = v0, v1
        m, b = line["slope_du_dv"], line["u_at_v0"]
    positions = []
    # Short along-line profiles at many positions resolve light, interrupted grids
    # without tracing the edge of a thick stroke.
    for t in range(t0+24, t1-20, 22):
        if exclusion and exclusion[0] < t < exclusion[1]:
            continue
        ts = np.arange(t-16, t+17)
        center = round(m * t + b)
        offsets = np.arange(center-12, center+13)
        p = np.array([np.mean((255-gray[np.round(s + m*(ts-t)).astype(int),ts])/255)
                      for s in offsets])
        for i in range(1,len(p)-1):
            if p[i] < .17 or p[i] < p[i-1] or p[i] <= p[i+1]:
                continue
            lo = hi = i
            while lo>0 and p[lo-1]>=.5*p[i]:
                lo -= 1
            while hi<len(p)-1 and p[hi+1]>=.5*p[i]:
                hi += 1
            if lo == 0 or hi == len(p)-1 or hi-lo>12:
                continue
            s = np.average(offsets[lo:hi+1],weights=p[lo:hi+1])
            positions.append((t,s,p[i]))
    arr = np.asarray(positions)
    ts, ss, scores = arr.T
    err = ss - (m*ts+b)
    best = (0, None)
    for j in range(len(arr)):
        for k in range(j+1,len(arr)):
            if ts[k]-ts[j] < .12*(t1-t0):
                continue
            slope = (err[k]-err[j])/(ts[k]-ts[j])
            if abs(slope) > .012:
                continue
            residual = np.abs(err-err[j]-slope*(ts-ts[j]))
            inside = residual <= 1.35
            score = np.sum(np.sqrt(scores[inside]) * (1-.14*residual[inside]))
            if score > best[0]:
                best = (score,inside)
    if best[1] is None:
        raise ValueError((direction,line,positions))
    pts = arr[best[1],:2]
    slope, intercept = np.polyfit(*pts.T, 1)
    rms = float(np.std(pts[:,1]-(slope*pts[:,0]+intercept)))
    return float(slope), float(intercept), pts.round(3).tolist(), rms

def axis_value(line):
    axis = "x" if "x_value" in line else "y"
    return axis, line[axis+"_value"]

def fit_grid(fig, panel, page):
    dest = ROOT / fig / f"cal-p{panel}"
    src = dest / "detect-seed.json"
    if not src.exists():
        src.write_bytes((dest/"calibration.json").read_bytes())
    cal = json.loads(src.read_text())
    gray = np.asarray(Image.open(page).convert("L"))
    specs = {}
    for direction, slope_key, intercept_key in (
        ("vertical","slope_du_dv","u_at_v0"),
        ("horizontal","slope_dv_du","v_at_u0"),
    ):
        fits = []
        for line in cal[direction+"_lines"]:
            axis, val = axis_value(line)
            exclusion = None
            if (fig,panel,axis)==("F4-19",1,"y") and val in (450,500,550):
                exclusion = (1275,2260)
            if (fig,panel,axis)==("F4-20",1,"y") and val in (450,500):
                exclusion = (1260,2340)
            slope, intercept, pts, rms = continuous_measure(gray,cal["box"],direction,line,exclusion)
            definition = "visible grid ink"
            if axis=="x" and fig=="F4-19" and val>100:
                definition += ", 10 ms sequence continued from 0–100"
            source = f"measured in {len(pts)} profiles, {definition}"
            line.update({slope_key:slope,intercept_key:intercept,
                         "source":source,"samples":pts,"profile_rms_px":rms})
            fits.append((val,slope,intercept,source,pts))
        specs[direction] = fits
    anchors = []
    for h in specs["horizontal"]:
        for v in specs["vertical"]:
            u, vv = intersect(h,v)
            xl, yl = (h,v) if fig=="F4-20" else (v,h)
            anchors.append(dict(x_value=xl[0],y_value=yl[0],u=round(u,3),v=round(vv,3),
                                x_source=xl[3],y_source=yl[3]))
    ax, ay, rx, ry, mx, my = fit_affine(anchors)
    cal.update(ax=ax,ay=ay,x_per_px=float(np.hypot(*ax[:2])),y_per_px=float(np.hypot(*ay[:2])),
               rms_residual_x=rx,rms_residual_y=ry,max_residual_x=mx,max_residual_y=my,n_anchors=len(anchors))
    (dest/"calibration.json").write_text(json.dumps(cal,indent=2,ensure_ascii=False),encoding="utf-8")
    with (dest/"anchors.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=anchors[0]);writer.writeheader();writer.writerows(anchors)
    return cal,specs

def eye_rows(fig,panel,cal,specs):
    sideways=fig=="F4-20"
    h=specs["horizontal"]
    v=specs["vertical"]
    xlines=sorted(h if sideways else v)
    ylines=sorted(v if sideways else h)
    rows=[]
    for axis, lines in (("x", xlines),("y",ylines)):
        for idx,line in enumerate(lines):
            val=line[0]
            if axis=="x":
                edge=ylines[0]
                u,vv=intersect(line,edge) if sideways else intersect(edge,line)
                printed=val
                label_u=label_v=""
                check="Printed numeral aligns to this grid line by eye"
                if not sideways:
                    printed=TIME_PRINTED[panel][idx]
                    estimate=TIME_CENTRES[panel][idx]
                    label_u="" if estimate is None else round(estimate*2.5,1)
                    label_v="" if estimate is None else (2033 if panel==1 else 3319)
                    if val==0:
                        check="Zero is adjacent to the origin frame"
                    if val>100:
                        check=("No numeral below right frame. Assigned by continuation of the 10 ms grid"
                               if printed is None else
                               "Printed numeral is beneath this line. Assigned by continuation of the 10 ms grid")
            else:
                edge=xlines[0]
                u,vv=intersect(edge,line) if sideways else intersect(line,edge)
                label_u=label_v=""
                printed=val if (val%100==0 if sideways or panel==1 else val%1==0) else None
                check="Printed numeral aligns to this grid line by eye"
                if printed is None:
                    check="Unlabelled half-step (upper frame for 4.5 in)" if val==4.5 else "Unlabelled half-step between adjacent numbered lines"
            rows.append(dict(figure_id=fig,panel=panel,axis=axis,printed_label="" if printed is None else f"{printed:g}",
                             assigned_value=f"{val:g}",grid_u=round(u,1),grid_v=round(vv,1),
                             label_u_approx=label_u,label_v_approx=label_v,check=check))
    return rows

def main():
    byfig={}
    for fig,panel,page in PLOTS:
        cal,specs=fit_grid(fig,panel,page)
        rows=eye_rows(fig,panel,cal,specs)
        folder=ROOT/fig/f"cal-p{panel}"
        _,x,y=piecewise_maps(folder,page)
        print(fig,panel,"RMS",cal["rms_residual_x"],cal["rms_residual_y"],
              "max",cal["max_residual_x"],cal["max_residual_y"])
        for k in (x,y):
            print("  knots",len(k.knots),"rejected",[(r["value"],r["reason"]) for r in k.rejected])
        byfig.setdefault(fig,[]).extend(rows)
    for fig, rows in byfig.items():
        with (ROOT/fig/"calibration-eye-checks.csv").open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)

if __name__=="__main__":
    main()


