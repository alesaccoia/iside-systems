#!/usr/bin/env python3
"""Three directions for the Iside mark in the new palette, on one sheet."""
from PIL import Image, ImageDraw, ImageFont

CORE = (255, 0, 101)      # the colour inside the letterforms
EDGE = (255, 0, 22)       # the colour on the rim
NIGHT = (14, 14, 17)
MAROON = (36, 6, 6)
PAPER = (244, 242, 237)

BLACKF = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
DINF = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
MONO = "/System/Library/Fonts/Menlo.ttc"


def f(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def wordmark(d, cx, cy, size, text="ISIDE"):
    """The OKT idea: one heavy word, core colour with a rim of the other."""
    font = f(BLACKF, size)
    d.text((cx, cy), text, font=font, fill=CORE, anchor="mm",
           stroke_width=max(2, size // 22), stroke_fill=EDGE)


def monogram(d, cx, cy, size):
    """A square that holds an I: the letter is the gap, not the ink."""
    half = size / 2
    d.rounded_rectangle((cx - half, cy - half, cx + half, cy + half),
                        radius=size * .12, fill=EDGE)
    inner = size * .82
    ih = inner / 2
    d.rounded_rectangle((cx - ih, cy - ih, cx + ih, cy + ih),
                        radius=size * .08, fill=CORE)
    # the I, cut out of the block
    bar_w, bar_h = size * .16, size * .46
    serif_w = size * .40
    top = cy - bar_h / 2
    d.rectangle((cx - serif_w / 2, top - size * .10, cx + serif_w / 2, top), fill=EDGE)
    d.rectangle((cx - bar_w / 2, top, cx + bar_w / 2, cy + bar_h / 2), fill=EDGE)
    d.rectangle((cx - serif_w / 2, cy + bar_h / 2, cx + serif_w / 2,
                 cy + bar_h / 2 + size * .10), fill=EDGE)


def nested(d, cx, cy, size):
    """The mark the site already uses, in the new palette."""
    half = size / 2
    w = size * .13
    d.rectangle((cx - half, cy - half, cx + half, cy + half), outline=EDGE, width=int(w))
    i = size * .30
    d.rectangle((cx - half + i, cy - half + i, cx + half - i, cy + half - i), fill=CORE)


def sheet(path):
    W, H, S = 1500, 1150, 2
    im = Image.new("RGB", (W * S, H * S), NIGHT)
    d = ImageDraw.Draw(im)
    label = f(MONO, 22 * S)
    cols = [(250, "01 / WORDMARK"), (750, "02 / MONOGRAMMA"), (1250, "03 / QUADRATI")]
    rows = [(250, NIGHT, "su nero"), (620, MAROON, "su bordeaux"), (960, PAPER, "su carta")]

    for y, bg, name in rows:
        d.rectangle((0, (y - 150) * S, W * S, (y + 150) * S), fill=bg)
        d.text((30 * S, (y - 140) * S), name.upper(), font=label,
               fill=(120, 120, 128) if bg != PAPER else (150, 148, 142))

    for x, name in cols:
        d.text((x * S, 40 * S), name, font=label, fill=(150, 148, 155), anchor="mm")

    for y, bg, _ in rows:
        wordmark(d, 250 * S, y * S, 96 * S)
        monogram(d, 750 * S, y * S, 190 * S)
        nested(d, 1250 * S, y * S, 190 * S)

    # small sizes, where a mark either survives or does not
    d.text((30 * S, 1090 * S), "A 32 PX", font=label, fill=(150, 148, 155))
    for i, (fn, size) in enumerate(((monogram, 32), (nested, 32))):
        fn(d, (200 + i * 90) * S, 1095 * S, size * S)
    wordmark(d, 500 * S, 1095 * S, 26 * S)

    im.resize((W, H), Image.LANCZOS).save(path, quality=95)
    print("wrote", path)


if __name__ == "__main__":
    sheet("esplorazione-logo.png")
