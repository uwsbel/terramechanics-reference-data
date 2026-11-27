"""Sample visually identified centerlines, constrained to ink in the packet."""
import csv
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


from reading_tiles import PICS, TEMP
from refit_grid import PLOTS
from trace_guides import REGIONS, ROUTES, VOID

sys.path.insert(0, str(Path.cwd() / "tools"))
from calibrate_axes import piecewise_maps

FIELDS = ["figure_id","panel","series_id","point_kind","sequence","pixel_u","pixel_v",
          "u_bound_px","v_bound_px","symbol","note"]

def parse_path(guide, scale):
    vertices = np.array([list(map(float,p.split(","))) for p in guide.split()])*scale
    progress = np.r_[0,np.cumsum(np.linalg.norm(np.diff(vertices,axis=0),axis=1))]
    arc = np.linspace(0,progress[-1],int(progress[-1]/.65)+1)
    centers = np.column_stack([np.interp(arc,progress,vertices[:,j]) for j in (0,1)])
    tangent = centers[np.minimum(np.arange(len(arc))+5,len(arc)-1)] - centers[np.maximum(np.arange(len(arc))-5,0)]
    tangent /= np.linalg.norm(tangent,axis=1)[:,None]
    normal = tangent[:,::-1] * [-1,1]
    return arc,centers,tangent,normal

def to_page(pix, rotated):
    return np.stack((pix[...,1],4557-pix[...,0]),axis=-1) if rotated else pix

def grid_distance(rays, cal, rotated):
    page=to_page(rays,rotated)
    u,v=page[...,0],page[...,1]
    distance=np.full_like(u,10000)
    for direction in ("horizontal","vertical"):
        lines=cal[direction+"_lines"]
        for i,line in enumerate(lines):
            if direction=="horizontal":
                delta=v-line["v_at_u0"]-line["slope_dv_du"]*u
            else:
                delta=u-line["u_at_v0"]-line["slope_du_dv"]*v
            margin=2.3 if i in (0,len(lines)-1) else 1.25
            distance=np.minimum(distance,np.abs(delta)-margin)
    return distance

def regions(key, c, scale):
    x,y=c/scale
    return [(extra,note) for xmin,xmax,ymin,ymax,extra,note in REGIONS.get(key,[])
            if xmin<=x<=xmax and ymin<=y<=ymax]

def broken(key, c, scale):
    x,y=c/scale
    return any((a<x<b and d<y<e) if axis=="x" else (a<y<b and d<x<e)
               for axis,a,b,d,e in VOID.get(key,[]))

def runs(mask):
    edges = np.flatnonzero(np.diff(np.r_[False,mask,False]))
    return list(zip(edges[::2],edges[1::2]))

def find_ink(key, gray, scale, cal, rotated, arc, centers, tangent, normal):
    offsets = np.arange(-16.,16.1,.5)
    rays=centers[:,None,:]+normal[:,None,:]*offsets[None,:,None]
    u=rays[...,0]
    v=rays[...,1]
    x,y=np.floor(u).astype(int),np.floor(v).astype(int)
    fx,fy=u-x,v-y
    ink=((1-fx)*(1-fy)*gray[y,x]+fx*(1-fy)*gray[y,x+1]
         +(1-fx)*fy*gray[y+1,x]+fx*fy*gray[y+1,x+1])
    grids=grid_distance(rays,cal,rotated)
    found=np.full_like(centers,np.nan)
    half_width=np.full(len(centers),np.nan)
    solid=key[-1]=="run4"
    for i,(c,pr,gd) in enumerate(zip(centers,ink,grids)):
        if broken(key,c,scale):
            continue
        region=regions(key,c,scale)
        ambiguous=any(phrase.startswith(("left-edge","origin crowded","rising pulse","minimum touches"))
                      for _,phrase in region)
        last_tail=key==("F4-20",1,"run10") and 584<c[1]/scale<616
        choices=[]
        raw=pr < 160
        if key==("F4-19",1,"run10") and c[0]/scale>855:
            # The dot tops survive above the overlapping lower dashed stroke.
            raw &= rays[i,:,1]<=c[1]+1.1*scale
        for lo,hi in runs(raw):
            if lo==0 or hi==len(pr):
                if not ambiguous and not last_tail:
                    continue
            if hi-lo<4:
                continue
            q=offsets[lo:hi]
            core=gd[lo:hi]>=0
            if not (ambiguous or last_tail) and np.count_nonzero(core)<3:
                continue
            w=255-pr[lo:hi]
            position=np.average(q,weights=w)
            if ambiguous or last_tail:
                # A joined blob can include the frame. Stay at the identified
                # departure rather than moving the point into the frame core.
                position=np.clip(position, max(q.min(),-2.), min(q.max(),2.)) if q.min()<=2 and q.max()>=-2 else position
            gap_distance=min(np.abs(q))
            limit=9 if solid else 7.5
            if abs(position)>limit or gap_distance>limit-2:
                continue
            score=abs(position)+.6*gap_distance
            choices.append((score,position,(q[-1]-q[0]+.5)/2))
        if choices:
            _,shift,width=min(choices)
            found[i]=c+shift*normal[i]
            half_width[i]=max(.6,width)
    valid=np.isfinite(half_width)
    # A grid intersection alone can look like a dot in a transverse profile.
    # Demand neighboring curve ink outside the grid strip in that case.
    for i in np.flatnonzero(valid):
        c=found[i]
        region=regions(key,centers[i],scale)
        if (any(n.startswith(("left-edge","origin crowded","rising pulse","minimum touches"))
                for _,n in region)
                or (key==("F4-20",1,"run10") and 585<c[1]/scale<616)):
            continue
        if grid_distance(c,cal,rotated)>1.5:
            continue
        stencil=(c + np.arange(-7.,7.1,1.)[:,None,None]*tangent[i]
                   + np.arange(-2.,2.1,1.)[None,:,None]*normal[i])
        pix=np.rint(stencil).astype(int)
        dark=gray[pix[...,1],pix[...,0]]<145
        support=(dark & (grid_distance(stencil,cal,rotated)>.9)).any(axis=1)
        if np.count_nonzero(support)<3:
            valid[i]=False
    # Drop tangential hits shorter than 1.3 px, mostly flecks and grid tails.
    for a,b in runs(valid):
        if b-a<3:
            valid[a:b]=False
    return found,half_width,valid

def native_values(pixels, rotated, X, Y):
    page=to_page(pixels,rotated)
    values=np.full((2,len(page)),np.nan)
    ix=np.isfinite(page[:,0])
    for i,k in enumerate((X,Y)):
        values[i,ix]=[k.value(*p)[0] for p in page[ix]]
    return values

def crossings(values,levels):
    out=[]
    for value in levels:
        for i in np.flatnonzero(np.diff(values>=value)):
            # Ignore scan wiggles and recrossings that stay within a small
            # fraction of the station spacing on either side.
            a=values[max(0,i-15):i+1]
            b=values[i+1:min(len(values),i+16)]
            if not len(a) or not len(b) or np.median(a)<value<=np.median(b) or np.median(b)<value<=np.median(a):
                out.append((int(i),float(value)))
    return out

def select_indices(key, arc, centers, found, valid, scale, guide_vals, observed_vals, features, grid_clearance):
    if key[0]=="F4-19":
        xlevels=sorted(set(range(0,11))|set(range(12,31,2))|set(range(35,141,5)))
    else:
        xlevels=np.round(np.arange(0,4.51,.1),3)
    ix=np.flatnonzero(valid)
    # Add the instrument's force grid stations as well as the requested times
    # or displacements. Keep the order of both passes through a turning point.
    stations=[(i,z,0) for i,z in crossings(guide_vals[0],xlevels)]
    if key[0]=="F4-20" or key[1]==1:
        stations += [(i,z,1) for i,z in crossings(guide_vals[1],range(50,601,50))]
    trace=[ix[0],ix[-1]]
    radius={"run4":32,"run10":28,"run12":64}[key[-1]]
    for i,value,axis in stations:
        if broken(key,centers[i],scale):
            continue
        nearby=ix[np.abs(arc[ix]-arc[i])<=radius]
        if not len(nearby):
            continue
        denominator=50 if axis else (1 if key[0]=="F4-19" else .1)
        offset=np.abs(observed_vals[axis,nearby]-value)/denominator
        deviation=np.abs(arc[nearby]-arc[i])/(2.5*radius)
        on_grid=.15*np.clip(1-grid_clearance[nearby]/2.,0,1)
        trace.append(nearby[np.argmin(offset+deviation+on_grid)])
    features_out=[]
    for x0,y0,role in features:
        if role.startswith("first"):
            i=ix[0]
        elif role.startswith("last"):
            i=ix[-1]
        else:
            p=np.array([x0,y0])*scale
            guide_i=np.argmin(np.linalg.norm(centers-p,axis=1))
            near=ix[np.abs(arc[ix]-arc[guide_i])<=scale*4.5]
            if len(near)==0:
                near=ix
            d=np.linalg.norm(found[near]-p,axis=1)+.25*np.abs(arc[near]-arc[guide_i])
            i=near[np.argmin(d)]
        features_out.append((i,role))
        trace.append(i)
    # Report both visible margins of an obvious break in the page.
    if key in VOID:
        for axis,a,b,d,e in VOID[key]:
            for target in (a,b):
                near=ix[(found[ix,1]/scale>=d-5)&(found[ix,1]/scale<=e+5)]
                if len(near):
                    i=near[np.argmin(np.abs(found[near,0]/scale-target))]
                    trace.append(i)
    trace=sorted(set(trace))
    # Keep the first/last pixels and each distinct station, but avoid two
    # trace rows for what is effectively the same place on one stroke.
    keep=[]
    for i in trace:
        if not keep or arc[i]-arc[keep[-1]]>3:
            keep.append(i)
        elif i==ix[-1] and len(keep)>1:
            keep[-1]=i
    return keep,features_out

def point_bounds(key,i,arc,c,t,n,w,valid,scale):
    trace_regions=regions(key,c,scale)
    if key[-1]=="run4":
        along=.6
    else:
        gaps=[]
        for a,b in runs(valid):
            if not a<=i<b:
                continue
            if a>0:
                prev=np.flatnonzero(valid[:a])
                if len(prev):
                    gaps.append(arc[a]-arc[prev[-1]])
            if b<len(arc):
                following=np.flatnonzero(valid[b:])
                if len(following):
                    gaps.append(arc[b+following[0]]-arc[b-1])
            break
        gaps=[gap for gap in gaps if gap<75]
        along=max(.8,max(gaps,default=0)/2)
    # Bounds are the axis projections of a local rectangle, including half
    # the adjacent on-paper gap along a dotted or dashed stroke.
    widths=np.maximum(.6,np.abs(n)*min(w,9) + np.abs(t)*along)
    if trace_regions:
        widths += max(n for n,_ in trace_regions)
    return widths,"; ".join(phrase for _,phrase in trace_regions)

def extract(fig,panel,page):
    fig_num=int(fig[-2:])
    rotated=fig_num==20
    im,scale=PICS[fig_num]
    gray=np.asarray(im,dtype=np.float32)
    folder=Path("out")/fig
    cal,X,Y=piecewise_maps(folder/f"cal-p{panel}",page)
    rows=[]
    preview=im.convert("RGB")
    draw=ImageDraw.Draw(preview)
    for series,color in zip(("run4","run10","run12"),("red","#1788eb","#03a150")):
        key=fig,panel,series
        guide,features=ROUTES[key]
        arc,centers,t,n=parse_path(guide,scale)
        found,w,valid=find_ink(key,gray,scale,cal,rotated,arc,centers,t,n)
        guide_vals=native_values(centers,rotated,X,Y)
        observed_vals=native_values(found,rotated,X,Y)
        clearance=grid_distance(found,cal,rotated)
        trace,selected=select_indices(key,arc,centers,found,valid,scale,guide_vals,observed_vals,features,clearance)
        for kind, sch in (("trace",[(i,"") for i in trace]),("feature",selected)):
            for sequence,(i,role) in enumerate(sch,1):
                point=found[i]
                u,v=to_page(point,rotated)
                bound,note=point_bounds(key,i,arc,centers[i],t[i],n[i],w[i],valid,scale)
                bu,bv=bound[::-1] if rotated else bound
                rows.append(dict(figure_id=fig,panel=panel,series_id=series,point_kind=kind,sequence=sequence,
                                 pixel_u=round(u,2),pixel_v=round(v,2),u_bound_px=round(bu,2),v_bound_px=round(bv,2),
                                 symbol="",note="; ".join(s for s in (role,note) if s)))
                x,y=point
                r=3 if kind=="trace" else 7
                draw.ellipse((x-r,y-r,x+r,y+r),outline=color,width=2)
    with (folder/f"points-p{panel}.csv").open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=FIELDS);wr.writeheader();wr.writerows(rows)
    box=cal["box"]
    if rotated:
        u0,v0,u1,v1=box
        box=(4557-v1,u0,4557-v0,u1)
    preview.crop(tuple(b+e for b,e in zip(box,(-12,-12,12,12)))).save(TEMP/f"b1-preview-{fig}-p{panel}.png")

if __name__=="__main__":
    for plot in PLOTS:
        extract(*plot)

