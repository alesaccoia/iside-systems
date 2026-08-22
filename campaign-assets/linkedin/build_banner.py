#!/usr/bin/env python3
"""LinkedIn cover images, drawn at final pixel size with real font metrics.

    iside-linkedin-profile-1584x396.png   personal profile cover
    iside-linkedin-page-1128x191.png      company page cover

No mark: the profile picture already carries the logo on a personal cover, and
on a company page LinkedIn draws the logo over the banner. What is left is type
and the lattice — the same figure the site's hero draws.

Rebuild: python3 build_banner.py     (needs Pillow)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, random

OUT = Path(__file__).parent
BG, INK, DIM, ACC, BLUE = "#0e0e11", "#eceae4", "#a6a3a9", "#ff4a2b", "#5aa9ff"
LINE = (236, 234, 228, 34)


def pick(*candidates):
    for path, index in candidates:
        if Path(path).exists():
            return path, index
    raise SystemExit("no font found")


BOLD = pick(("/System/Library/Fonts/HelveticaNeue.ttc", 1),
            ("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 0))
MONO = pick(("/System/Library/Fonts/Menlo.ttc", 1),
            ("/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf", 0))


def ft(font, size):
    path, index = font
    return ImageFont.truetype(path, max(1, round(size)), index=index)


def lattice(d, x0, y0, w, h, seed=7):
    """Signals in, a decision out: four layers, edges that only go forward."""
    r = random.Random(seed)
    layers = [4, 5, 4, 2]
    nodes = []
    for li, count in enumerate(layers):
        lx = x0 + w * (li / (len(layers) - 1))
        for i in range(count):
            t = 0.5 if count == 1 else i / (count - 1)
            pad = h * (0.22 if li == len(layers) - 1 else 0.04)
            nodes.append((lx, y0 + pad + (h - pad * 2) * t, li))
    edges = []
    for li in range(len(layers) - 1):
        a_layer = [n for n in nodes if n[2] == li]
        b_layer = [n for n in nodes if n[2] == li + 1]
        for ai, a in enumerate(a_layer):
            for bi, b in enumerate(b_layer):
                near = abs(ai / max(1, len(a_layer) - 1) - bi / max(1, len(b_layer) - 1))
                if near < .27 or r.random() < .12:
                    edges.append((a, b))
    for a, b in edges:
        d.line((a[0], a[1], b[0], b[1]), fill=LINE, width=1)
    lit = [n for n in nodes if n[2] == 0][1]
    path = [lit]
    for li in range(len(layers) - 1):
        outs = [e for e in edges if e[0] == path[-1]]
        if not outs:
            break
        path.append(outs[len(outs) // 2][1])
    for i in range(len(path) - 1):
        d.line((path[i][0], path[i][1], path[i + 1][0], path[i + 1][1]), fill=ACC, width=2)
    for n in nodes:
        q = 4 if n in path else 3
        d.ellipse((n[0] - q, n[1] - q, n[0] + q, n[1] + q), fill=ACC if n in path else INK)


def wrap(text, font, width):
    rows, line = [], ""
    for word in text.split():
        probe = (line + " " + word).strip()
        if line and font.getlength(probe) > width:
            rows.append(line)
            line = word
        else:
            line = probe
    return rows + [line]


def cover(path, w, h, title, meta, left_safe):
    """`left_safe` is the strip LinkedIn covers with the avatar or the logo."""
    im = Image.new("RGB", (w, h), BG)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    x = left_safe
    right = w - h * .12
    f = ft(BOLD, h * .175)
    rows = wrap(title, f, (right - x) * .62)
    while len(rows) > 2:
        f = ft(BOLD, f.size - 1)
        rows = wrap(title, f, (right - x) * .62)
    block = len(rows) * f.size * 1.12
    y = h * .5 - block / 2 - h * .06
    for row in rows:
        d.text((x, y), row, font=f, fill=INK)
        y += f.size * 1.12

    mf = ft(MONO, max(11, h * .055))
    d.line((x, y + h * .05, x + h * .22, y + h * .05), fill=ACC, width=max(2, round(h * .012)))
    d.text((x, y + h * .085), meta, font=mf, fill=DIM)

    gw = (right - x) * .30
    lattice(d, right - gw, h * .18, gw, h * .64)

    im.paste(layer, (0, 0), layer)
    im.save(OUT / path, optimize=True)
    print("wrote", path, f"{w}x{h}")


def main():
    # the avatar sits low-left on a personal cover, so nothing lives there
    cover("iside-linkedin-profile-1584x396.png", 1584, 396,
          "AI Enablement, Data e Marketing Strategy.",
          "ISIDE SYSTEMS · MILANO · ISIDESYSTEMS.COM", left_safe=430)
    # a company page draws the logo over the lower left corner
    cover("iside-linkedin-page-1128x191.png", 1128, 191,
          "Data, AI e Marketing.",
          "ISIDE SYSTEMS · ISIDESYSTEMS.COM", left_safe=270)


if __name__ == "__main__":
    main()
