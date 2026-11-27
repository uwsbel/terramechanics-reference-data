from PIL import Image,ImageDraw
import numpy as np
im=np.array(Image.open('packet/p0110.png').convert('L'));u0,v0,u1,v1=915,2727,990,2820;Y,X=np.mgrid[v0:v1,u0:u1];B=im[v0:v1,u0:u1]<160
# Count only outer-left area, away from drawn polyline.
for u,v in [(953,2755),(943,2778),(943,2792)]:
 a=np.linspace(0,2*np.pi,360,endpoint=False);x=np.round(u+17*np.cos(a)).astype(int);y=np.round(v+17*np.sin(a)).astype(int);print((u,v),'outer black',np.mean(im[y,x]<160))
# fit union annuli on left of original line (removing its known stroke)
P=[(953,2755),(943,2792)];R=[np.hypot(X-u,Y-v) for u,v in P];M=np.any([(r>12)&(r<20) for r in R],axis=0)
extra=B&(~M)&(X<950)
print('unexplained black left region by rows:')
for v in range(2740,2810,5):
 yy=v-v0;xx=np.where(extra[yy:yy+5].any(axis=0))[0]+u0;print(v,list(xx))
can=Image.new('RGB',(1000,450),'white');d=ImageDraw.Draw(can)
for i,cs in enumerate([[(953,2755),(943,2792)],[(953,2755),(943,2778),(943,2792)]]):
 C=Image.fromarray(im[v0:v1,u0:u1]).convert('RGB');dd=ImageDraw.Draw(C)
 for u,v in cs:dd.ellipse((u-u0-19,v-v0-19,u-u0+19,v-v0+19),outline='red',width=1)
 can.paste(C.resize((300,372)),(i*330,30));d.text((i*330,0),str(cs),fill='blue')
can.save('out/B4-knee-ring-check.png')
