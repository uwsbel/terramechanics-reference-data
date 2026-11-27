from pathlib import Path
p=Path('out/read_curves.py');s=p.read_text().replace('rad=24;u=int(u);v=int(v);','rad=35;u=int(u);v=int(v);').replace("if abs(cx-u)<12 and abs(cy-v)<12: candidates.append((len(cc),cx,cy))", "ratio=len(cc)/((max(xs)-min(xs)+1)*(max(ys)-min(ys)+1))\n  shape_ok=ratio<.72 if sym.startswith('triangle') else (ratio>.75 if sym=='square' else .6<ratio<.94)\n  if shape_ok and abs(cx-u)<22 and abs(cy-v)<22: candidates.append((len(cc),cx,cy))")
p.write_text(s)
