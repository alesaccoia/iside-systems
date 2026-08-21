#!/usr/bin/env python3
"""Build launch-ready Google Ads creatives for Iside's AI Opportunity Sprint.

The art direction deliberately mirrors isidesystems.com: charcoal, warm white,
hairline grids, a coral accent, mono micro-labels, and the double-square mark.
"""
from pathlib import Path
import html
import shutil
import subprocess
from PIL import ImageFont

ROOT = Path(__file__).parent
STATIC = ROOT / "static"
CAROUSEL = ROOT / "carousel"
VIDEO = ROOT / "video"
SOURCE = ROOT / "source-slides"

BG, INK, DIM, ACC, LINE, BLUE = "#0e0e11", "#eceae4", "#a6a3a9", "#ff4a2b", "#eceae433", "#5aa9ff"
SANS = "Noto Sans, Arial, sans-serif"
MONO = "Noto Sans Mono, DejaVu Sans Mono, monospace"
MONO_FONT = "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"


def esc(value):
    return html.escape(str(value))


def text(x, y, value, size, color=INK, weight=400, family=SANS, anchor="start", letter=0, opacity=1):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
            f'letter-spacing="{letter}" opacity="{opacity}">{esc(value)}</text>')


def wrap(value, max_chars):
    words, lines, line = value.split(), [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if line and len(candidate) > max_chars:
            lines.append(line); line = word
        else:
            line = candidate
    if line: lines.append(line)
    return lines


def lines(x, y, value, size, max_chars, leading=1.08, **kwargs):
    return "".join(text(x, y + i * size * leading, line, size, **kwargs)
                   for i, line in enumerate(wrap(value, max_chars)))


def mark(x, y, s):
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="none" stroke="{INK}" stroke-width="{max(1.5, s*.07)}"/>'
            f'<rect x="{x+s*.28}" y="{y+s*.28}" width="{s*.44}" height="{s*.44}" fill="none" stroke="{ACC}" stroke-width="{max(1.5, s*.07)}"/>')


def grid(w, h, margin):
    # A single baseline guide keeps the dark system texture without crossing
    # typography, logo frames, or the workflow diagram.
    paths = f'<path d="M 0 {h-margin:.1f} H {w}"/>'
    return f'<g fill="none" stroke="{LINE}" stroke-width="1">{paths}</g>'


def badge(x, y, label, scale=1):
    value, size = label.upper(), 10*scale
    face = ImageFont.truetype(MONO_FONT, round(size))
    left, top, right, bottom = face.getbbox(value)
    tracking = size*.12
    pad_x, pad_y = 12*scale, 7*scale
    width = (right-left) + max(0, len(value)-1)*tracking + 2*pad_x
    height = (bottom-top) + 2*pad_y
    baseline = y + pad_y - top
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}" fill="{BG}" stroke="{LINE}"/>'
            + text(x+pad_x-left, baseline, value, size, DIM, 600, MONO, letter=tracking))


def hero_visual(w, h, margin, variant=0):
    # A deliberately abstract workflow map: no fake dashboard / no unreadable AI imagery.
    cx, cy = w*.73, h*.54
    r = min(w, h)*.18
    rings = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r*(.46+i*.22):.1f}" fill="none" stroke="{ACC if i==2 else LINE}" stroke-width="{2 if i==2 else 1}" opacity="{.9-i*.18}"/>' for i in range(3))
    nodes = [(cx-r*1.05,cy-r*.65),(cx+r*1.16,cy-r*.36),(cx+r*.76,cy+r*.96),(cx-r*.9,cy+r*.88)]
    links = ''.join(f'<path d="M {cx} {cy} L {x} {y}" stroke="{LINE}"/>' for x,y in nodes)
    ns = ''.join(f'<circle cx="{x}" cy="{y}" r="{max(4, min(w,h)*.012)}" fill="{ACC if i==variant%4 else BLUE}"/>' for i,(x,y) in enumerate(nodes))
    center = f'<rect x="{cx-r*.26}" y="{cy-r*.26}" width="{r*.52}" height="{r*.52}" fill="{BG}" stroke="{INK}" stroke-width="2"/>'
    return f'<g>{links}{rings}{ns}{center}</g>'


def svg(w, h, kind="main", slide=0):
    m = max(22, min(w,h)*.065)
    small = min(w,h) < 150
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">', f'<rect width="{w}" height="{h}" fill="{BG}"/>', grid(w,h,m)]
    out += [mark(m, m, max(18, min(w,h)*.055)), text(m+max(26,min(w,h)*.08), m+max(15,min(w,h)*.038), "ISIDE SYSTEMS", max(8,min(w,h)*.022), DIM, 650, MONO, letter=max(1,min(w,h)*.004))]
    if kind == "main":
        if small:
            out += [text(m, h*.46, "AI OPPORTUNITY", max(13,h*.17), INK, 700), text(m, h*.67, "SPRINT · 10 GIORNI", max(8,h*.09), ACC, 650, MONO, letter=1), text(w-m, h*.9, "€1.900 + IVA", max(8,h*.095), INK, 650, MONO, "end")]
        elif w/h > 5:
            out += [text(m, h*.5, "AI OPPORTUNITY SPRINT", h*.24, INK, 700), text(m, h*.76, "10 giorni per scegliere dove l'AI crea valore.", h*.11, DIM), text(w-m, h*.78, "€1.900 + IVA", h*.12, ACC, 700, MONO, "end")]
        else:
            portrait = w/h < .9
            out += [lines(m, h*.42, "Scopri dove l'AI crea valore reale.", min(w,h)*(.075 if portrait else .105), 16 if portrait else 23, weight=700), hero_visual(w,h,m,0), text(m, h-m*.55, "€1.900 + IVA", min(w,h)*.043, INK, 650, MONO), text(w-m, h-m*.55, "PRENOTA LO SPRINT  →", min(w,h)*.027, ACC, 650, MONO, "end", letter=1.3)]
    elif kind == "carousel_1":
        out += [lines(m,h*.38,"Mappa 10–15 opportunità AI.",min(w,h)*(.072 if w/h < .9 else .09),16 if w/h < .9 else 20,weight=700), hero_visual(w,h,m,1)]
    elif kind == "carousel_2":
        out += [lines(m,h*.38,"Scegli i casi con più valore.",min(w,h)*(.072 if w/h < .9 else .09),16 if w/h < .9 else 20,weight=700), hero_visual(w,h,m,2)]
    elif kind == "carousel_3":
        out += [lines(m,h*.38,"Esci con 3 workflow pronti.",min(w,h)*(.072 if w/h < .9 else .09),16 if w/h < .9 else 20,weight=700), hero_visual(w,h,m,3)]
    elif kind == "slide":
        headlines = ["Dove l'AI può creare valore?", "10–15 opportunità, ordinate per priorità.", "3 workflow dettagliati da implementare.", "Una roadmap concreta per i prossimi 90 giorni.", "AI Opportunity Sprint · €1.900 + IVA"]
        bodies = ["Un percorso intensivo di 10 giorni per partire dai processi, non dal rumore.", "Impatto × fattibilità × rischio: la scelta diventa una decisione operativa.", "Stack, effort, costi e ROI stimato. Niente slide decorative.", "Workshop iniziale, analisi, restituzione finale. Una direzione attuabile.", "Se implementiamo insieme un progetto, €900 dello Sprint vengono scalati."]
        out += [lines(m,h*.42,headlines[slide],min(w,h)*.09,22,weight=700), hero_visual(w,h,m,slide)]
        if slide == 4: out += [text(m,h-m*.55,"PRENOTA LO SPRINT  →",min(w,h)*.028,ACC,650,MONO,letter=1.3)]
    out.append('</svg>')
    return ''.join(out)


def write_svg(path, width, height, kind="main", slide=0):
    path.write_text(svg(width, height, kind, slide), encoding="utf-8")


def raster(svg_path, png_path):
    subprocess.run(["rsvg-convert", "-f", "png", "-o", str(png_path), str(svg_path)], check=True)


def make_video(width, height, name):
    frames = []
    for i in range(5):
        s = SOURCE / f"{name}-{i+1}.svg"; p = SOURCE / f"{name}-{i+1}.png"
        write_svg(s, width, height, "slide", i); raster(s,p); frames.append(p)
    clips = []
    for i, frame in enumerate(frames):
        clip = SOURCE / f"{name}-{i+1}.mp4"; clips.append(clip)
        subprocess.run(["ffmpeg","-y","-loop","1","-framerate","30","-t","3","-i",str(frame),
                        "-vf","format=yuv420p,fade=t=in:st=0:d=0.22,fade=t=out:st=2.78:d=0.22",
                        "-an","-c:v","libx264","-crf","20",str(clip)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    manifest = SOURCE / f"{name}.txt"
    manifest.write_text("".join(f"file '{clip}'\n" for clip in clips), encoding="utf-8")
    # Five rotating panels, 15 seconds, H.264 and no audio.
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(manifest),"-c","copy",
                    "-movflags","+faststart",str(VIDEO/name)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    for folder in (STATIC, CAROUSEL, VIDEO, SOURCE): folder.mkdir(parents=True, exist_ok=True)
    formats = {
        "ai-opportunity-sprint-1200x628": (1200,628), "ai-opportunity-sprint-1200x1200": (1200,1200),
        "ai-opportunity-sprint-960x1200": (960,1200), "ai-opportunity-sprint-300x250": (300,250),
        "ai-opportunity-sprint-336x280": (336,280), "ai-opportunity-sprint-728x90": (728,90),
        "ai-opportunity-sprint-970x250": (970,250), "ai-opportunity-sprint-300x600": (300,600),
        "ai-opportunity-sprint-160x600": (160,600), "ai-opportunity-sprint-320x50": (320,50),
        "ai-opportunity-sprint-320x100": (320,100), "ai-opportunity-sprint-468x60": (468,60),
        "ai-opportunity-sprint-250x250": (250,250), "ai-opportunity-sprint-120x600": (120,600),
    }
    for name,(w,h) in formats.items():
        s = STATIC/f"{name}.svg"; write_svg(s,w,h); raster(s,STATIC/f"{name}.png")
    for kind in ("carousel_1","carousel_2","carousel_3"):
        for suffix,w,h in (("1200x1200",1200,1200),("1200x628",1200,628),("960x1200",960,1200)):
            s=CAROUSEL/f"{kind}-{suffix}.svg"; write_svg(s,w,h,kind); raster(s,CAROUSEL/f"{kind}-{suffix}.png")
    make_video(1920,1080,Path("ai-opportunity-sprint-16x9-15s.mp4"))
    make_video(1080,1080,Path("ai-opportunity-sprint-1x1-15s.mp4"))
    make_video(1080,1920,Path("ai-opportunity-sprint-9x16-15s.mp4"))
    # Keep the package lean: SVG files are editable source; PNG/MP4 are upload-ready deliverables.
    print(f"Built assets in {ROOT}")

if __name__ == "__main__": main()
