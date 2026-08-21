#!/usr/bin/env python3
"""AI Advisory creatives with real font-metric layout."""
from pathlib import Path
from PIL import ImageFont
import html, subprocess

R=Path(__file__).parent; C=R/"carousel"; V=R/"video"; S=R/"source-slides"; L=R/"logo"
F="/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"; B="/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
BG,INK,DIM,ACC,LINE,BLUE="#0e0e11","#eceae4","#a6a3a9","#ff4a2b","#eceae433","#5aa9ff"
CARDS=[
("01 / DIREZIONE","L’AI deve partire dai processi.","Non da una lista di tool. Dalla domanda: dove può liberare tempo, qualità o capacità decisionale?"),
("02 / PRIORITÀ","Una strategia che diventa scelta.","Valutiamo opportunità, vincoli e sequenza: ciò che conviene fare ora, dopo e non fare affatto."),
("03 / WORKFLOW","Dalla promessa al flusso di lavoro.","Disegniamo workflow, ruoli, dati e strumenti perché l’AI entri davvero nell’operatività del team."),
("04 / GOVERNANCE","Velocità, senza perdere il controllo.","Policy, dati, sicurezza e responsabilità: basi chiare per adottare l’AI con fiducia."),
("05 / ADVISORY","AI Advisory per team che vogliono costruire.","Strategia, governance, workflow ed enablement. Da una conversazione, a una pratica quotidiana.")]
def ff(s,b=False): return ImageFont.truetype(B if b else F,round(s))
def wrap(t,s,w,b=False):
    f,out,line=ff(s,b),[],""
    for q in t.split():
        n=(line+" "+q).strip()
        if line and f.getlength(n)>w: out.append(line);line=q
        else: line=n
    return out+[line]
def fit(t,s,w,n):
    low=s*.62
    while s>=low:
        a=wrap(t,s,w,True)
        if len(a)<=n:return s,a
        s-=1
    return s,wrap(t,s,w,True)
def tx(x,y,t,s,c=INK,wt=400,f="Noto Sans,Arial,sans-serif",a="start",sp=0):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-family="{f}" font-size="{s:.1f}" font-weight="{wt}" text-anchor="{a}" letter-spacing="{sp:.2f}">{html.escape(t)}</text>'
def tl(x,y,rows,s,**kw): return "".join(tx(x,y+i*s*1.12,t,s,**kw) for i,t in enumerate(rows))
def shape(w,h,m):
    # Keep the outer grid lines out of the logo frame. Interior guides are
    # useful for rhythm, but may never pass through a framed element.
    # Keep the field quiet around all typography and the central diagram.
    # The single baseline guide cannot intersect either region.
    p=f'<path d="M0 {h-m:.1f}H{w}"/>'
    z=max(2,m*.08)
    return f'<g fill="none" stroke="{LINE}" stroke-width="1">{p}</g><rect x="{m}" y="{m}" width="{m*.85}" height="{m*.85}" fill="none" stroke="{INK}" stroke-width="{z}"/><rect x="{m+m*.238}" y="{m+m*.238}" width="{m*.374}" height="{m*.374}" fill="none" stroke="{ACC}" stroke-width="{z}"/>'
def visual(cx,cy,r,i):
    nodes=[(cx-r*.95,cy-r*.62),(cx+r*1.02,cy-r*.39),(cx+r*.78,cy+r*.8),(cx-r*.88,cy+r*.76)]
    links="".join(f'<path d="M{cx:.1f} {cy:.1f}L{x:.1f} {y:.1f}" stroke="{LINE}"/>' for x,y in nodes)
    circles="".join(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*(.46+n*.22):.1f}" fill="none" stroke="{ACC if n==2 else LINE}" stroke-width="{2 if n==2 else 1}"/>' for n in range(3))
    dots="".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(3,r*.065):.1f}" fill="{ACC if n==i%4 else BLUE}"/>' for n,(x,y) in enumerate(nodes))
    return f'<g>{links}{circles}{dots}<rect x="{cx-r*.25:.1f}" y="{cy-r*.25:.1f}" width="{r*.5:.1f}" height="{r*.5:.1f}" fill="{BG}" stroke="{INK}" stroke-width="2"/></g>'
def badge(x,y,t):
    h,s,p=28,10,12;w=ff(s).getlength(t)*1.04+2*p
    return f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" fill="{BG}" stroke="{LINE}"/>'+tx(x+p,y+19,t.upper(),s,DIM,600,"Noto Sans Mono,monospace",sp=1)
def art(w,h,i):
    _,title,_=CARDS[i];m=min(w,h)*.04;portrait=w/h<.9
    # Deliberately no microcopy: every rendered word remains display-sized.
    brand_size=max(20,m*.45)
    z=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',f'<rect width="{w}" height="{h}" fill="{BG}"/>',shape(w,h,m),tx(m+m*1.15,m+m*.61,"ISIDE SYSTEMS",brand_size,INK,650,"Noto Sans Mono,monospace",sp=brand_size*.08)]
    if portrait:
        x=m;aw=w-2*m
        s,a=fit(title,min(w,h)*.105,aw,3);y=h*.29;z+=[tl(x,y,a,s,wt=700)]
        # A separate lower safe area keeps the graphic clear of every glyph.
        z+=[visual(w*.50,h*.70,min(w,h)*.16,i)]
    else:
        x=m;aw=w*(.52 if w/h>1.2 else .62)
        s,a=fit(title,min(w,h)*(.125 if w/h>1.2 else .105),aw,3);y=h*.46;z+=[tl(x,y,a,s,wt=700),visual(w*(.77 if w/h>1.2 else .72),h*.57,min(w,h)*(.20 if w/h>1.2 else .18),i)]
    z+=["</svg>"]
    return "".join(z)
def save(s,p,w,h,i): s.write_text(art(w,h,i),encoding="utf-8");subprocess.run(["rsvg-convert","-f","png","-o",str(p),str(s)],check=True)
def movie(w,h,name):
    clips=[]
    for i in range(5):
        s=S/f"{name.stem}-{i+1}.svg";p=s.with_suffix(".png");save(s,p,w,h,i);c=S/f"{name.stem}-{i+1}.mp4";clips.append(c)
        subprocess.run(["ffmpeg","-y","-loop","1","-framerate","30","-t","3","-i",str(p),"-vf","format=yuv420p,fade=t=in:st=0:d=0.22,fade=t=out:st=2.78:d=0.22","-an","-c:v","libx264","-crf","20",str(c)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    q=S/f"{name.stem}.txt";q.write_text("".join(f"file '{c}'\n" for c in clips))
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(q),"-c","copy","-movflags","+faststart",str(V/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def main():
    for d in(C,V,S,L):d.mkdir(parents=True,exist_ok=True)
    logo=L/"iside-systems-logo-1200x1200.svg"
    logo.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200"><rect width="1200" height="1200" fill="#0e0e11"/><rect x="180" y="180" width="840" height="840" fill="none" stroke="#eceae4" stroke-width="72"/><rect x="415" y="415" width="370" height="370" fill="none" stroke="#ff4a2b" stroke-width="72"/></svg>',encoding="utf-8")
    subprocess.run(["rsvg-convert","-f","png","-o",str(logo.with_suffix(".png")),str(logo)],check=True)
    for i in range(5):
        for n,w,h in(("1x1",1200,1200),("1_91x1",1200,628),("4x5",960,1200)):
            s=C/f"ai-advisory-{i+1:02d}-{n}.svg";save(s,s.with_suffix(".png"),w,h,i)
    movie(1920,1080,Path("ai-advisory-16x9-15s.mp4"));movie(1080,1080,Path("ai-advisory-1x1-15s.mp4"));movie(1080,1920,Path("ai-advisory-9x16-15s.mp4"))
if __name__=="__main__":main()
