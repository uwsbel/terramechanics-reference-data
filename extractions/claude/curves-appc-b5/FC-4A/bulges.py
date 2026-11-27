import numpy as np, json
from PIL import Image
g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
D = g < 160
F = json.load(open("out/FC-4A/linefit.json"))
for sid, typ in (("dr95", 15), ("dr0", 12)):
    a, b = F[sid]["a"], F[sid]["b"]
    flagged = []
    for u in range(930, 2372):
        vc = a + b * u
        col = D[int(vc - 28):int(vc + 29), u]
        n = col.sum()
        if n > typ + 4: flagged.append((u, int(n)))
    # group
    grp = []
    for u, n in flagged:
        if grp and u - grp[-1][-1][0] <= 2: grp[-1].append((u, n))
        else: grp.append([(u, n)])
    print(sid, [(gp[0][0], gp[-1][0], max(x[1] for x in gp)) for gp in grp])
