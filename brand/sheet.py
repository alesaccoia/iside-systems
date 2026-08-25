#!/usr/bin/env python3
"""One sheet showing the proposal: wordmark, lockup, marks, palette, small sizes."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import cairosvg, io

HERE = Path(__file__).parent
NIGHT, PAPER = (14, 14, 17), (244, 242, 237)
CORE, EDGE = (255, 0, 101), (255, 0, 22)
MONO = "/System/Library/Fonts/Menlo.ttc"


def svg_img(name, width, bg=None):
    png = cairosvg.svg2png(url=str(HERE / name), output_width=width,
                           background_color=None if bg is None else
                           "#%02x%02x%02x" % bg)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def label(d, xy, text, fill=(150, 148, 155), size=22):
    d.text(xy, text, font=ImageFont.truetype(MONO, size), fill=fill)


W, H, S = 1500, 1560, 2
im = Image.new("RGB", (W * S, H * S), NIGHT)
d = ImageDraw.Draw(im)

label(d, (40 * S, 40 * S), "ISIDE SYSTEMS / PROPOSTA LOGO", size=24 * S // 2)

# 1. wordmark on night
mark = svg_img("logo-iside-wordmark.svg", 1000 * S)
im.paste(mark, (250 * S, 120 * S), mark)
label(d, (40 * S, 300 * S), "01 WORDMARK")

# 2. lockup on paper
d.rectangle((0, 380 * S, W * S, 700 * S), fill=PAPER)
lock = svg_img("logo-iside-lockup.svg", 820 * S)
im.paste(lock, (340 * S, 420 * S), lock)
label(d, (40 * S, 400 * S), "02 LOCKUP SU CARTA", fill=(150, 148, 142))

# 3. the two marks
label(d, (40 * S, 760 * S), "03 MARCHIO — QUADRATO E ALTERNATIVA")
for i, name in enumerate(("logo-iside-mark.svg", "logo-iside-mark-alt.svg")):
    m = svg_img(name, 240 * S)
    im.paste(m, ((330 + i * 420) * S, 820 * S), m)

# 4. small sizes
label(d, (40 * S, 1130 * S), "04 A 64, 32 E 16 PX")
x = 330 * S
for size in (64, 32, 16):
    m = svg_img("logo-iside-mark.svg", size * S)
    im.paste(m, (x, (1180 + (64 - size) // 2) * S), m)
    x += (size + 40) * S
word = svg_img("logo-iside-wordmark.svg", 300 * S)
im.paste(word, (700 * S, 1180 * S), word)

# 5. palette
label(d, (40 * S, 1330 * S), "05 COLORI")
for i, (name, rgb) in enumerate((("CORE  #FF0065  255 0 101", CORE),
                                 ("RIM   #FF0016  255 0 22", EDGE))):
    y = (1380 + i * 70) * S
    d.rectangle((330 * S, y, 390 * S, y + 50 * S), fill=rgb)
    label(d, (410 * S, y + 14 * S), name, fill=(210, 208, 205))

im.resize((W, H), Image.LANCZOS).save("proposta-logo.png", quality=95)
print("wrote proposta-logo.png")
