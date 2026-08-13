#!/usr/bin/env python3
"""
Renders the raster assets the SVG favicon cannot cover:

    apple-touch-icon.png   180x180   iOS home screen
    favicon-32.png          32x32    fallback for old browsers
    og-image.png          1200x630   Open Graph / Twitter card

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


if __name__ == "__main__":
    icon(180, os.path.join(HERE, "apple-touch-icon.png"))
    icon(32, os.path.join(HERE, "favicon-32.png"))
    og(os.path.join(HERE, "og-image.png"))
