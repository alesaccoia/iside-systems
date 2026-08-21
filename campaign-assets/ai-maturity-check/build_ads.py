#!/usr/bin/env python3
"""Native PNG ads: every text line is fitted with real font metrics."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).parent/"static"
BG,INK,DIM,ACC,BLUE="#0e0e11","#eceae4","#a6a3a9","#ff4a2b","#5aa9ff"
BOLD="/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
MONO="/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf"
FORMATS={"ai-maturity-check-1200x628":(1200,628),"ai-maturity-check-1200x1200":(1200,1200),"ai-maturity-check-960x1200":(960,1200),"ai-maturity-check-1080x1920":(1080,1920),"ai-maturity-check-300x250":(300,250),"ai-maturity-check-336x280":(336,280),"ai-maturity-check-728x90":(728,90),"ai-maturity-check-970x90":(970,90),"ai-maturity-check-160x600":(160,600),"ai-maturity-check-300x600":(300,600),"ai-maturity-check-320x50":(320,50)}
def ft(p,n):return ImageFont.truetype(p,max(1,round(n)))
def wrap(t,f,w):
  rows=[];line=""
  for word in t.split():
    v=(line+" "+word).strip()
    if line and f.getlength(v)>w:rows.append(line);line=word
    else:line=v
  return rows+[line]
def fit(t,w,high,low,limit):
  while high>=low:
    f=ft(BOLD,high);r=wrap(t,f,w)
    if len(r)<=limit:return f,r
    high-=1
  return ft(BOLD,low),wrap(t,ft(BOLD,low),w)
def mark(d,x,y,s):
  z=max(1,round(s*.075));d.rectangle((x,y,x+s,y+s),outline=INK,width=z);i=s*.28;d.rectangle((x+i,y+i,x+s-i,y+s-i),outline=ACC,width=z)
def lockup(d,x,y,u):
  s=max(16,u*.95);mark(d,x,y,s);f=ft(MONO,max(8,u*.32));l,t,r,b=f.getbbox("ISIDE SYSTEMS");d.text((x+s+u*.35,y+s/2-(t+b)/2),"ISIDE SYSTEMS",font=f,fill=INK)
def grid(d,w,h,m):
  for x in(m,w*.34,w*.66,w-m):d.line((x,0,x,h),fill=(236,234,228,20))
  for y in(m,h*.28,h*.58,h-m):d.line((0,y,w,y),fill=(236,234,228,20))
def diagram(d,cx,cy,r,v):
  nodes=[(cx-r*.95,cy-r*.62),(cx+r*1.02,cy-r*.39),(cx+r*.78,cy+r*.8),(cx-r*.88,cy+r*.76)]
  for x,y in nodes:d.line((cx,cy,x,y),fill=(236,234,228,32))
  for q,col,z in((.46,(236,234,228,32),1),(.68,(236,234,228,32),1),(.90,ACC,2)):d.ellipse((cx-r*q,cy-r*q,cx+r*q,cy+r*q),outline=col,width=z)
  for i,(x,y) in enumerate(nodes):q=max(3,round(r*.065));d.ellipse((x-q,y-q,x+q,y+q),fill=ACC if i==v%4 else BLUE)
  q=r*.25;d.rectangle((cx-q,cy-q,cx+q,cy+q),outline=INK,width=2)
def render(n,w,h):
  im=Image.new("RGB",(w,h),BG);d=ImageDraw.Draw(im);m=max(10,round(min(w,h)*.065));grid(d,w,h,m);ratio=w/h
  title="La tua azienda è pronta a far lavorare l’AI?";sub="4 minuti. 3 quick win."
  if min(w,h)<100:
    title="AI: a che punto sei?";sub="→";lockup(d,m,round((h-max(16,h*.38))/2),max(14,h*.42));f,rows=fit(title,w*.43,max(12,h*.26),9,1);d.text((w*.48,h/2),rows[0],font=f,fill=INK,anchor="lm");d.text((w-m,h/2),sub,font=ft(MONO,max(9,h*.19)),fill=ACC,anchor="rm")
  elif ratio>4:
    title="AI: a che punto sei?";lockup(d,m,m,max(18,h*.33));f,rows=fit(title,w*.47,h*.27,h*.16,1);d.text((w*.32,h*.48),rows[0],font=f,fill=INK,anchor="lm");d.text((w-m,h*.5),"Maturity Check →",font=ft(MONO,max(11,h*.16)),fill=ACC,anchor="rm")
  elif ratio<.7:
    lockup(d,m,m,max(22,min(w,h)*.07));f,rows=fit(title,w-2*m,min(w,h)*.105,min(w,h)*.07,4);y=h*.36
    for row in rows:d.text((m,y),row,font=f,fill=INK);y+=f.size*1.07
    d.text((m,y+min(w,h)*.055),sub,font=ft(MONO,max(12,min(w,h)*.033)),fill=ACC);diagram(d,w*.5,h*.78,min(w,h)*.19,1)
  else:
    lockup(d,m,m,max(24,min(w,h)*.065));f,rows=fit(title,w*.52,min(w,h)*.10,min(w,h)*.06,3);y=h*.40
    for row in rows:d.text((m,y),row,font=f,fill=INK);y+=f.size*1.07
    d.text((m,y+min(w,h)*.05),sub,font=ft(MONO,max(12,min(w,h)*.030)),fill=ACC);diagram(d,w*.77,h*.56,min(w,h)*.20,0)
  im.save(OUT/(n+".png"),optimize=True)
def main():
  OUT.mkdir(parents=True,exist_ok=True)
  for n,(w,h) in FORMATS.items():render(n,w,h)
  print("Built",len(FORMATS),"measured PNGs")
if __name__=="__main__":main()
