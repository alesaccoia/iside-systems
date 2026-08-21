#!/usr/bin/env python3
"""
Renders the raster assets the SVG favicon cannot cover:

    apple-touch-icon.png   180x180   iOS home screen
    favicon-32.png          32x32    fallback for old browsers
    og-image.png          1200x630   Open Graph / Twitter card
    og-ai-maturity.png    1200x630   card for the AI Maturity Check

Run after changing the mark or the strapline:

    python3 assets/img/make-assets.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (244, 242, 237)
INK   = (22, 22, 26)
ACC   = (200, 52, 26)
DIM   = (119, 116, 108)
NIGHT = (14, 14, 17)                     # --bg in dark mode
LIGHT = (236, 234, 228)                  # --ink in dark mode
ACC_D = (255, 74, 43)                    # --acc in dark mode
DIM_D = (125, 122, 128)

HELV = "/System/Library/Fonts/Helvetica.ttc"
MONO = "/System/Library/Fonts/Menlo.ttc"


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def mark(d, cx, cy, size, w=None, ink=INK, acc=ACC):
    """Nested squares — the same glyph the site header uses."""
    s = size / 32.0
    w = w or max(2, int(round(2.6 * s)))
    X = lambda v: cx + (v - 16) * s
    Y = lambda v: cy + (v - 16) * s
    d.rectangle([X(3.3), Y(3.3), X(28.7), Y(28.7)], outline=ink, width=w)
    d.rectangle([X(10.6), Y(10.6), X(21.4), Y(21.4)], outline=acc, width=w)


def icon(px, path, bg=NIGHT):
    scale = 4
    im = Image.new("RGB", (px * scale, px * scale), bg)
    d = ImageDraw.Draw(im)
    mark(d, px * scale / 2, px * scale / 2, px * scale * 0.66, ink=LIGHT, acc=ACC_D)
    im.resize((px, px), Image.LANCZOS).save(path)
    print("wrote", os.path.relpath(path, HERE))


def og(path):
    W, H, S = 1200, 630, 2
    im = Image.new("RGB", (W * S, H * S), NIGHT)
    d = ImageDraw.Draw(im)

    # module grid on the right, echoing the hero figure
    gx0, gy0, gs = 780 * S, 95 * S, 27 * S
    for i in range(15):
        d.line([gx0 + i * gs, gy0, gx0 + i * gs, gy0 + 14 * gs], fill=(32, 32, 38), width=S)
        d.line([gx0, gy0 + i * gs, gx0 + 14 * gs, gy0 + i * gs], fill=(32, 32, 38), width=S)

    mark(d, gx0 + 7 * gs, gy0 + 7 * gs, 232 * S, w=int(9 * S), ink=LIGHT, acc=ACC_D)

    f_title = font(HELV, 82 * S, 1)
    f_sub   = font(HELV, 31 * S, 0)
    f_meta  = font(MONO, 19 * S)

    x = 80 * S
    d.text((x, 128 * S), "Iside Systems", font=f_title, fill=LIGHT)
    for k, line in enumerate(["Data Strategy", "AI Adoption",
                              "Growth Operations", "Marketing Science"]):
        d.text((x, (243 + k * 42) * S), line, font=f_sub, fill=LIGHT)
    d.line([x, 432 * S, x + 96 * S, 432 * S], fill=ACC_D, width=3 * S)
    d.text((x, 462 * S), "ALESSANDRO SACCOIA — MILANO", font=f_meta, fill=DIM_D)
    d.text((x, 493 * S), "ISIDESYSTEMS.COM", font=f_meta, fill=DIM_D)

    im.resize((W, H), Image.LANCZOS).save(path, quality=92)
    print("wrote", os.path.relpath(path, HERE))



def og_maturity(path):
    """Social card for the AI Maturity Check: the pentagon it ends on."""
    import math
    W, H, S = 1200, 630, 2
    im = Image.new("RGB", (W * S, H * S), NIGHT)
    layer = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    f_title = font(HELV, 66 * S, 1)
    f_sub   = font(HELV, 30 * S, 0)
    f_meta  = font(MONO, 19 * S)

    x = 80 * S
    d.text((x, 150 * S), "AI Maturity", font=f_title, fill=LIGHT)
    d.text((x, 222 * S), "Check", font=f_title, fill=LIGHT)
    d.text((x, 330 * S), "A che punto è la tua azienda", font=f_sub, fill=LIGHT)
    d.text((x, 372 * S), "16 domande, 5 minuti, gratis", font=f_sub, fill=DIM_D)
    d.line([x, 436 * S, x + 96 * S, 436 * S], fill=ACC_D, width=3 * S)
    d.text((x, 466 * S), "PIANO OPERATIVO A 90 GIORNI", font=f_meta, fill=DIM_D)
    d.text((x, 497 * S), "ISIDESYSTEMS.COM/AI-MATURITY", font=f_meta, fill=DIM_D)
    mark(d, x + 22 * S, 570 * S, 44 * S, w=int(3.4 * S), ink=LIGHT, acc=ACC_D)
    d.text((x + 62 * S, 562 * S), "ISIDE SYSTEMS", font=f_meta, fill=LIGHT)

    # the five axes, with a profile drawn on them
    axes = ["DATI", "PROCESSI", "MARKETING", "COMPETENZE", "GOVERNANCE"]
    shape = [0.78, 0.52, 0.63, 0.40, 0.55]
    cx, cy, r = 900 * S, 300 * S, 168 * S
    ang = lambda i: -math.pi / 2 + i * 2 * math.pi / 5
    line = (236, 234, 228, 40)
    for ring in (0.4, 0.7, 1.0):
        pts = [(cx + math.cos(ang(i)) * r * ring, cy + math.sin(ang(i)) * r * ring) for i in range(5)]
        d.line(pts + [pts[0]], fill=line, width=S)
    for i in range(5):
        d.line((cx, cy, cx + math.cos(ang(i)) * r, cy + math.sin(ang(i)) * r), fill=line, width=S)
    pts = [(cx + math.cos(ang(i)) * r * shape[i], cy + math.sin(ang(i)) * r * shape[i])
           for i in range(5)]
    d.polygon(pts, fill=(255, 74, 43, 52))
    d.line(pts + [pts[0]], fill=ACC_D, width=3 * S)
    for i, (px, py) in enumerate(pts):
        q = 7 * S
        d.ellipse((px - q, py - q, px + q, py + q), fill=ACC_D if i == 0 else (90, 169, 255))
    f_axis = font(MONO, 15 * S)
    for i, name in enumerate(axes):
        lx = cx + math.cos(ang(i)) * r * 1.30
        ly = cy + math.sin(ang(i)) * r * 1.30
        w = f_axis.getlength(name)
        # nothing may leave the card: pull the outermost labels back in
        px = min(max(lx - w / 2, 8 * S), W * S - w - 8 * S)
        d.text((px, ly - f_axis.size / 2), name, font=f_axis, fill=DIM_D)

    im.paste(layer, (0, 0), layer)
    im.resize((W, H), Image.LANCZOS).save(path, quality=92)
    print("wrote", os.path.relpath(path, HERE))


def og_priors(path):
    """Social card for the Priors tool: the network is the picture."""
    W, H, S = 1200, 630, 2
    im = Image.new("RGB", (W * S, H * S), NIGHT)
    d = ImageDraw.Draw(im)

    f_title = font(HELV, 86 * S, 1)
    f_sub   = font(HELV, 30 * S, 0)
    f_meta  = font(MONO, 19 * S)

    x = 80 * S
    d.text((x, 150 * S), "Priors", font=f_title, fill=LIGHT)
    d.text((x, 268 * S), "Reti bayesiane nel browser", font=f_sub, fill=LIGHT)
    d.text((x, 310 * S), "Bayesian networks in the browser", font=f_sub, fill=DIM_D)
    d.line([x, 382 * S, x + 96 * S, 382 * S], fill=ACC_D, width=3 * S)
    d.text((x, 412 * S), "UNO STRUMENTO DI ISIDE SYSTEMS", font=f_meta, fill=DIM_D)
    d.text((x, 443 * S), "ISIDESYSTEMS.COM/PRIORS", font=f_meta, fill=DIM_D)
    mark(d, x + 22 * S, 520 * S, 44 * S, w=int(3.4 * S), ink=LIGHT, acc=ACC_D)
    d.text((x + 62 * S, 512 * S), "ISIDE SYSTEMS", font=f_meta, fill=LIGHT)

    # a small network: two nodes, an edge, and the bars that carry the posterior
    def node(cx, cy, w, h, bars, accent=False):
        d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                    outline=ACC_D if accent else LIGHT, width=int(2 * S))
        d.line([cx - w / 2, cy - h / 2 + 30 * S, cx + w / 2, cy - h / 2 + 30 * S],
               fill=(70, 70, 76), width=int(1.6 * S))
        for i, frac in enumerate(bars):
            top = cy - h / 2 + (46 + i * 30) * S
            d.rectangle([cx - w / 2 + 10 * S, top, cx - w / 2 + 10 * S + (w - 20 * S) * frac,
                         top + 16 * S],
                        fill=ACC_D if (accent and i == 0) else (78, 78, 86))

    nx = 900 * S
    node(nx, 200 * S, 250 * S, 120 * S, [0.43, 0.57])
    d.line([nx, 262 * S, nx, 372 * S], fill=(120, 120, 128), width=int(2 * S))
    d.polygon([(nx, 384 * S), (nx - 7 * S, 370 * S), (nx + 7 * S, 370 * S)], fill=(120, 120, 128))
    node(nx, 452 * S, 250 * S, 120 * S, [1.0, 0.0], accent=True)

    im.resize((W, H), Image.LANCZOS).save(path, quality=92)
    print("wrote", os.path.relpath(path, HERE))


def og_algosynth(path):
    """Social card for AlgoSynth: a step grid with the playhead lit."""
    W, H, S = 1200, 630, 2
    im = Image.new("RGB", (W * S, H * S), NIGHT)
    d = ImageDraw.Draw(im)

    f_title = font(HELV, 86 * S, 1)
    f_sub   = font(HELV, 30 * S, 0)
    f_meta  = font(MONO, 19 * S)

    x = 80 * S
    d.text((x, 150 * S), "AlgoSynth", font=f_title, fill=LIGHT)
    d.text((x, 268 * S), "Sequencer algoritmico", font=f_sub, fill=LIGHT)
    d.text((x, 310 * S), "Algorithmic sequencer", font=f_sub, fill=DIM_D)
    d.line([x, 382 * S, x + 96 * S, 382 * S], fill=ACC_D, width=3 * S)
    d.text((x, 412 * S), "UNO STRUMENTO DI ISIDE SYSTEMS", font=f_meta, fill=DIM_D)
    d.text((x, 443 * S), "ISIDESYSTEMS.COM/ALGOSYNTH", font=f_meta, fill=DIM_D)
    mark(d, x + 22 * S, 520 * S, 44 * S, w=int(3.4 * S), ink=LIGHT, acc=ACC_D)
    d.text((x + 62 * S, 512 * S), "ISIDE SYSTEMS", font=f_meta, fill=LIGHT)

    # four tracks of sixteen steps, euclidean-ish, with the playhead on column 5
    cell, gap = 26 * S, 5 * S
    gx, gy = 700 * S, 150 * S
    rows = [                                    # twelve steps: any more runs off the card
        [1,0,0, 1,0,0, 1,0,0, 1,0,0],
        [0,0,0, 1,0,0, 0,0,0, 1,0,1],
        [1,0,1, 1,0,1, 1,0,1, 1,0,1],
        [0,0,1, 0,1,0, 0,1,0, 0,1,0],
    ]
    head = 3
    for r, row in enumerate(rows):
        for c, on in enumerate(row):
            x0 = gx + c * (cell + gap)
            y0 = gy + r * (cell + gap) * 1.6
            box = [x0, y0, x0 + cell, y0 + cell]
            if c == head:
                d.rectangle(box, fill=ACC_D if on else None, outline=ACC_D, width=int(1.6 * S))
            elif on:
                d.rectangle(box, fill=(150, 148, 156))
            else:
                d.rectangle(box, outline=(56, 56, 62), width=int(1.4 * S))

    im.resize((W, H), Image.LANCZOS).save(path, quality=92)
    print("wrote", os.path.relpath(path, HERE))


if __name__ == "__main__":
    icon(180, os.path.join(HERE, "apple-touch-icon.png"))
    icon(32, os.path.join(HERE, "favicon-32.png"))
    og(os.path.join(HERE, "og-image.png"))
    og_priors(os.path.join(HERE, "og-priors.png"))
    og_maturity(os.path.join(HERE, "og-ai-maturity.png"))
    og_algosynth(os.path.join(HERE, "og-algosynth.png"))
