import numpy as np, json
from PIL import Image
g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
D = g < 160
F = json.load(open("out/FC-4A/linefit.json"))
def show(name, u0, v0, u1, v1):
    sub = D[v0:v1+1, u0:u1+1]
    print(name)
    for i, row in enumerate(sub):
        print("%4d " % (v0 + i) + "".join("#" if x else "." for x in row))
    print("     u0=%d" % u0)
show("S1", 1115, 2745, 1158, 2788)
show("C1", 1125, 3225, 1170, 3282)
