#!/usr/bin/env python3
"""AI Maturity Check — carousel and video.

Every layout is measured with real font metrics at final pixel size, so nothing
is placed from a character count. The visual is the same pentagon the tool draws
at the end of the check: the ad shows the thing you actually get.

Carousel: five cards in 1:1, 1.91:1 and 4:5, as native PNG and as editable SVG.
Video:    silent 15s H.264 in 16:9, 1:1 and 9:16, animated frame by frame.

Rebuild: python3 build_assets.py     (needs Pillow and ffmpeg)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import html, math, shutil, subprocess, tempfile

R = Path(__file__).parent
CAR, VID = R / "carousel", R / "video"
BG, INK, DIM, ACC, BLUE = "#0e0e11", "#eceae4", "#a6a3a9", "#ff4a2b", "#5aa9ff"
LINE = (236, 234, 228, 38)


def pick(*candidates):
    """First font that exists, as (path, face index). The kit is built on more
    than one machine, so nothing is pinned to a single distribution path."""
    for path, index in candidates:
        if Path(path).exists():
            return path, index
    raise SystemExit("no font found among: " + ", ".join(c[0] for c in candidates))


BOLD = pick(("/System/Library/Fonts/HelveticaNeue.ttc", 1),          # the site face
            ("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 0),
            ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0))
MONO = pick(("/System/Library/Fonts/Menlo.ttc", 1),
            ("/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf", 0),
            ("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 0))

# The five beats of the campaign. Kicker, headline, and the axis that lights up.
CARDS = [
    ("01 / DIAGNOSI", "A che punto è la tua azienda con l’AI?", 0),
    ("02 / PERCORSO", "Sedici domande. Cinque minuti.", 1),
    ("03 / MAPPA", "Un punteggio su dati, processi, marketing e competenze.", 2),
    ("04 / QUICK WIN", "Tre azioni per i prossimi 90 giorni.", 3),
    ("05 / CHECK", "Fai il check. È gratuito.", 4),
]
AXES = ["DATI", "PROCESSI", "MARKETING", "COMPETENZE", "GOVERNANCE"]
SHAPE = [0.78, 0.52, 0.63, 0.40, 0.55]      # the profile the pentagon draws
URL = "isidesystems.com/ai-maturity.html"


def ft(font, size):
    path, index = font
    return ImageFont.truetype(path, max(1, round(size)), index=index)


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


def fit(text, width, high, low, limit, max_height=None):
    """Largest size at which the headline fits `limit` lines and, when a height
    is given, the vertical room it was allotted. Nothing is placed on trust."""
    while high >= low:
        f = ft(BOLD, high)
        rows = wrap(text, f, width)
        if len(rows) <= limit and (max_height is None or len(rows) * f.size * 1.08 <= max_height):
            return f, rows
        high -= 1
    f = ft(BOLD, low)
    return f, wrap(text, f, width)


def mark(d, x, y, s):
    z = max(1, round(s * .075))
    d.rectangle((x, y, x + s, y + s), outline=INK, width=z)
    i = s * .28
    d.rectangle((x + i, y + i, x + s - i, y + s - i), outline=ACC, width=z)


def lockup(d, x, y, unit):
    s = max(16, unit * .95)
    mark(d, x, y, s)
    f = ft(MONO, max(9, unit * .32))
    box = f.getbbox("ISIDE SYSTEMS")
    d.text((x + s + unit * .35, y + s / 2 - (box[1] + box[3]) / 2), "ISIDE SYSTEMS", font=f, fill=INK)


def pentagon(d, cx, cy, r, lit, grow=1.0, labels=True, bounds=None):
    """The radar the tool ends on: five axes, one filled profile."""
    ang = lambda i: -math.pi / 2 + i * 2 * math.pi / 5
    for ring in (0.4, 0.7, 1.0):
        pts = [(cx + math.cos(ang(i)) * r * ring, cy + math.sin(ang(i)) * r * ring) for i in range(5)]
        d.line(pts + [pts[0]], fill=LINE, width=1)
    for i in range(5):
        d.line((cx, cy, cx + math.cos(ang(i)) * r, cy + math.sin(ang(i)) * r), fill=LINE)
    pts = [(cx + math.cos(ang(i)) * r * SHAPE[i] * grow,
            cy + math.sin(ang(i)) * r * SHAPE[i] * grow) for i in range(5)]
    if grow > 0.02:
        d.polygon(pts, fill=(255, 74, 43, 46))
        d.line(pts + [pts[0]], fill=ACC, width=max(2, round(r * .012)))
    for i, (x, y) in enumerate(pts):
        q = max(3, round(r * .035))
        d.ellipse((x - q, y - q, x + q, y + q), fill=ACC if i == lit % 5 else BLUE)
    if labels and r > 90:
        f = ft(MONO, max(9, r * .085))
        for i, name in enumerate(AXES):
            lx = cx + math.cos(ang(i)) * r * 1.28
            ly = cy + math.sin(ang(i)) * r * 1.28
            w = f.getlength(name)
            x = lx - w / 2
            if bounds:                       # never let a label leave the frame
                x = min(max(x, bounds[0]), bounds[1] - w)
            d.text((x, ly - f.size / 2), name, font=f, fill=DIM)


def layout(w, h, i):
    """Geometry shared by the PNG and the SVG, so the two cannot drift apart.

    Only genuinely wide formats put the headline beside the pentagon; square and
    portrait ones stack it above. Either way the type is sized to the room that
    is actually left once the diagram, its labels and the URL have taken theirs.
    """
    kicker, title, lit = CARDS[i]
    m = max(14, round(min(w, h) * .062))
    side = w / h > 1.35
    kick = max(11, min(w, h) * .029)
    url = max(10, min(w, h) * .024)
    lockup_h = max(22, min(w, h) * .062) * .95

    if side:
        r = min(h * .29, w * .16)
        cx, cy = w - m - r * 1.32, h * .50
        text_w = max(140, cx - r * 1.34 - m - min(w, h) * .04)
        f, rows = fit(title, text_w, min(w, h) * .115, min(w, h) * .05, 3, h * .46)
        y0 = h * .5 - len(rows) * f.size * 1.08 / 2
    else:
        r = min(w * .24, h * .175)
        cx = w / 2
        label_pad = max(9, r * .085) * 2.2
        block_h = r * 1.28 * 2 + label_pad          # diagram plus its labels
        bottom = h - m - min(w, h) * .085           # URL and progress rule live here
        cy = bottom - block_h / 2
        top = m + lockup_h + min(w, h) * .07 + kick * 1.6
        text_w = w - 2 * m
        f, rows = fit(title, text_w, min(w, h) * .092, min(w, h) * .042, 4,
                      (cy - block_h / 2) - top - min(w, h) * .03)
        y0 = top
    return dict(m=m, kicker=kicker, lit=lit, font=f, rows=rows, y0=y0,
                cx=cx, cy=cy, r=r, kick=kick, url=url)


def frame(w, h, i, t=1.0, motion=False):
    """One card. `t` in 0..1 drives the animation when rendering video frames."""
    L = layout(w, h, i)
    im = Image.new("RGB", (w, h), BG)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    m = L["m"]

    ease = 1 - pow(1 - min(1.0, max(0.0, t)), 3)
    slide = 0 if not motion else round((1 - ease) * min(w, h) * .045)
    fade = 1.0 if not motion else min(1.0, ease * 1.35)

    lockup(d, m, m, max(22, min(w, h) * .062))
    d.text((m, L["y0"] - L["kick"] * 2.1 + slide), L["kicker"], font=ft(MONO, L["kick"]), fill=ACC)
    y = L["y0"] + slide
    for row in L["rows"]:
        d.text((m, y), row, font=L["font"], fill=INK)
        y += L["font"].size * 1.08
    pentagon(d, L["cx"], L["cy"], L["r"], L["lit"],
             grow=1.0 if not motion else ease, bounds=(m * .5, w - m * .5))
    d.text((m, h - m - min(w, h) * .040), URL, font=ft(MONO, L["url"]), fill=DIM)

    # progress rule: how far along the five beats we are
    p = (i + (ease if motion else 1)) / len(CARDS)
    d.line((m, h - m * .42, w - m, h - m * .42), fill=LINE, width=1)
    d.line((m, h - m * .42, m + (w - 2 * m) * p, h - m * .42), fill=ACC,
           width=max(2, round(h * .0035)))

    if motion and fade < 1:
        layer.putalpha(layer.getchannel("A").point(lambda a: round(a * fade)))
    im.paste(layer, (0, 0), layer)
    return im


# ---------------------------------------------------------------- SVG twin
def tx(x, y, text, size, fill, weight=400, family="Helvetica Neue,Arial,sans-serif",
       sp=0, length=None, anchor="start"):
    # textLength pins each line to the width we measured, so a viewer without the
    # font gets the same layout instead of a reflowed one
    extra = (f' textLength="{length:.1f}" lengthAdjust="spacingAndGlyphs"' if length else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-family="{family}" '
            f'font-size="{size:.1f}" font-weight="{weight}" letter-spacing="{sp:.2f}" '
            f'text-anchor="{anchor}"{extra}>{html.escape(text)}</text>')


def svg(w, h, i):
    L = layout(w, h, i)
    m, r, cx, cy, f = L["m"], L["r"], L["cx"], L["cy"], L["font"]
    ang = lambda k: -math.pi / 2 + k * 2 * math.pi / 5
    rings = "".join(
        '<polygon points="' + " ".join(
            f"{cx+math.cos(ang(k))*r*ring:.1f},{cy+math.sin(ang(k))*r*ring:.1f}" for k in range(5)) +
        '" fill="none" stroke="#eceae4" stroke-opacity=".15"/>' for ring in (.4, .7, 1))
    spokes = "".join(
        f'<path d="M{cx:.1f} {cy:.1f}L{cx+math.cos(ang(k))*r:.1f} {cy+math.sin(ang(k))*r:.1f}" '
        'stroke="#eceae4" stroke-opacity=".15"/>' for k in range(5))
    pts = " ".join(f"{cx+math.cos(ang(k))*r*SHAPE[k]:.1f},{cy+math.sin(ang(k))*r*SHAPE[k]:.1f}"
                   for k in range(5))
    dots = "".join(
        f'<circle cx="{cx+math.cos(ang(k))*r*SHAPE[k]:.1f}" cy="{cy+math.sin(ang(k))*r*SHAPE[k]:.1f}" '
        f'r="{max(3,r*.035):.1f}" fill="{ACC if k==L["lit"]%5 else BLUE}"/>' for k in range(5))
    labels = ""
    if r > 90:
        lf = ft(MONO, max(9, r * .085))
        for k, name in enumerate(AXES):
            tw = lf.getlength(name)
            lx = cx + math.cos(ang(k)) * r * 1.28
            lx = min(max(lx - tw / 2, m * .5), w - m * .5 - tw) + tw / 2
            ly = cy + math.sin(ang(k)) * r * 1.28 + lf.size * .34
            labels += tx(lx, ly, name, lf.size, DIM, 600, "Menlo,Courier New,monospace",
                         length=tw, anchor="middle")
    body = "".join(tx(m, L["y0"] + n * f.size * 1.08 + f.size * .82, row, f.size, INK, 700,
                      length=f.getlength(row))
                   for n, row in enumerate(L["rows"]))
    s = min(w, h) * .062 * .95
    z = max(1, round(s * .075))
    kf = ft(MONO, L["kick"])
    uf = ft(MONO, L["url"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>'
            f'<rect x="{m}" y="{m}" width="{s:.1f}" height="{s:.1f}" fill="none" stroke="{INK}" stroke-width="{z}"/>'
            f'<rect x="{m+s*.28:.1f}" y="{m+s*.28:.1f}" width="{s*.44:.1f}" height="{s*.44:.1f}" '
            f'fill="none" stroke="{ACC}" stroke-width="{z}"/>'
            + tx(m + s * 1.35, m + s * .68, "ISIDE SYSTEMS", max(9, min(w, h) * .062 * .32), INK, 650,
                 "Menlo,Courier New,monospace")
            + tx(m, L["y0"] - L["kick"] * 1.25, L["kicker"], L["kick"], ACC, 600,
                 "Menlo,Courier New,monospace", length=kf.getlength(L["kicker"]))
            + body + f'<g>{rings}{spokes}'
            + f'<polygon points="{pts}" fill="rgba(255,74,43,.18)" stroke="{ACC}" stroke-width="{max(2,r*.012):.1f}"/>'
            + dots + labels + "</g>"
            + tx(m, h - m - min(w, h) * .040 + uf.size * .82, URL, L["url"], DIM, 600,
                 "Menlo,Courier New,monospace", length=uf.getlength(URL))
            + f'<path d="M{m} {h-m*.42:.1f}H{w-m}" stroke="#eceae4" stroke-opacity=".15"/>'
            + f'<path d="M{m} {h-m*.42:.1f}H{w-m}" stroke="{ACC}" stroke-width="{max(2,round(h*.0035))}"/>'
            + "</svg>")


def movie(w, h, name, seconds_per_card=3, fps=30):
    tmp = Path(tempfile.mkdtemp())
    n = 0
    for i in range(len(CARDS)):
        for k in range(seconds_per_card * fps):
            frame(w, h, i, t=k / (fps * .55), motion=True).save(tmp / f"f{n:05d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(tmp / "f%05d.png"),
                    "-vf", "format=yuv420p", "-an", "-c:v", "libx264", "-crf", "20",
                    "-movflags", "+faststart", str(VID / name)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(tmp, ignore_errors=True)


def main():
    for folder in (CAR, VID):
        folder.mkdir(parents=True, exist_ok=True)
    for i in range(len(CARDS)):
        for suffix, w, h in (("1x1", 1200, 1200), ("1_91x1", 1200, 628), ("4x5", 960, 1200)):
            stem = CAR / f"ai-maturity-check-{i+1:02d}-{suffix}"
            frame(w, h, i).save(stem.with_suffix(".png"), optimize=True)
            stem.with_suffix(".svg").write_text(svg(w, h, i), encoding="utf-8")
    movie(1920, 1080, "ai-maturity-check-16x9-15s.mp4")
    movie(1080, 1080, "ai-maturity-check-1x1-15s.mp4")
    movie(1080, 1920, "ai-maturity-check-9x16-15s.mp4")
    print("Built", len(CARDS) * 3, "carousel cards (PNG + SVG) and 3 videos")


if __name__ == "__main__":
    main()
