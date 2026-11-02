from PIL import Image
import math,random
random.seed(21);n=512;im=Image.new('RGB',(n,n));pixels=[]
for j in range(n):
 v=1-j/(n-1);z=math.cos(math.pi*(1-v));r=math.sin(math.pi*(1-v))
 for i in range(n):
  u=i/(n-1);x=r*math.cos(math.tau*u);y=r*math.sin(math.tau*u)
  noise=math.sin(u*210+math.sin(v*45))*math.sin(v*170)*.8+random.gauss(0,.55)
  base=(z*.7+math.sin(u*12)*.1)*9+noise
  boundary=-.23+.105*math.exp(-(x/.22)**2)+.09*abs(x)
  mask=max(0,min(1,(boundary-z)*75+.5))*max(0,min(1,(-y-.05)*9))
  blush=math.exp(-((abs(x)-.56)/.16)**2-((z+.02)/.15)**2)*max(0,-y)*.22
  pixels.append(tuple(int(max(0,min(255,((g+base)*(1-mask)+(c+noise*.7)*mask)*(1-blush)+b*blush))) for g,c,b in zip((239,173,87),(255,232,189),(237,137,82))))
im.putdata(pixels);im.save(str(__import__('pathlib').Path(__file__).resolve().parent/'face-paint.png'))
