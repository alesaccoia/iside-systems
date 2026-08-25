#!/usr/bin/env python3
"""The Iside mark, in the palette Alessandro picked.

The wordmark is drawn from real glyph outlines — Archivo Black, SIL Open Font
License, so the logo carries no font-licensing question — and shipped as paths,
not as text: it renders identically on a machine that has never seen the font.

    logo-iside-wordmark.svg     ISIDE, core fill with a rim
    logo-iside-lockup.svg       wordmark + SYSTEMS
    logo-iside-mark.svg         the square monogram, for avatars and favicons
    plus PNG renders of each, on dark and on paper

Rebuild: python3 build_logo.py     (needs fonttools and Pillow)
"""
from pathlib import Path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
import subprocess

HERE = Path(__file__).parent
FONT = HERE / "fonts" / "ArchivoBlack.ttf"

CORE = "#FF0065"          # 255, 0, 101 — inside the letterforms
EDGE = "#FF0016"          # 255, 0, 22 — on the rim
NIGHT = "#0e0e11"
PAPER = "#f4f2ed"
DIM = "#a6a3a9"


def outline(text, tracking=0.012):
    """Glyph outlines as one SVG path, in font units, plus the advance width."""
    font = TTFont(FONT)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    paths, x = [], 0
    upem = font["head"].unitsPerEm
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        d = pen.getCommands()
        if d:
            paths.append(f'<path transform="translate({x} 0)" d="{d}"/>')
        x += hmtx[name][0] + upem * tracking
    return "".join(paths), x - upem * tracking, upem


def wordmark_svg(text="ISIDE", pad=110, rim=30):
    body, width, upem = outline(text)
    cap = TTFont(FONT)["OS/2"].sCapHeight
    w = width + pad * 2
    h = cap + pad * 2
    # y flips: font units grow upward, SVG downward
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w/upem*100:.0f}" height="{h/upem*100:.0f}" role="img" '
            f'aria-label="Iside">'
            f'<g transform="translate({pad} {cap + pad}) scale(1 -1)" '
            f'fill="{CORE}" stroke="{EDGE}" stroke-width="{rim}" '
            f'stroke-linejoin="round" paint-order="stroke fill">{body}</g></svg>')


def lockup_svg():
    body, width, upem = outline("ISIDE")
    cap = TTFont(FONT)["OS/2"].sCapHeight
    pad, rim, gap = 110, 30, 300
    sub = "SYSTEMS"
    sub_size = cap * .21
    w = width + pad * 2
    h = cap + pad * 2 + gap
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w/upem*100:.0f}" height="{h/upem*100:.0f}" role="img" '
            f'aria-label="Iside Systems">'
            f'<g transform="translate({pad} {cap + pad}) scale(1 -1)" '
            f'fill="{CORE}" stroke="{EDGE}" stroke-width="{rim}" '
            f'stroke-linejoin="round" paint-order="stroke fill">{body}</g>'
            f'<text x="{pad + width/2:.0f}" y="{cap + pad + gap*.78:.0f}" fill="{CORE}" '
            f'text-anchor="middle" font-family="Menlo,Consolas,monospace" '
            f'font-size="{sub_size:.0f}" letter-spacing="{sub_size*.42:.0f}" '
            f'font-weight="700">{sub}</text></svg>')


def mark_svg(size=1000):
    """The square: the nested frame the studio already uses, recoloured. The
    rim colour goes on the outside, the core colour inside — the same rule the
    wordmark follows, made geometric."""
    w = size * .118                      # frame weight
    inner = size * .30                   # inset of the solid block
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'width="{size}" height="{size}" role="img" aria-label="Iside Systems">'
            f'<rect x="{w/2:.1f}" y="{w/2:.1f}" width="{size-w:.1f}" height="{size-w:.1f}" '
            f'fill="none" stroke="{EDGE}" stroke-width="{w:.1f}"/>'
            f'<rect x="{inner:.1f}" y="{inner:.1f}" width="{size-inner*2:.1f}" '
            f'height="{size-inner*2:.1f}" fill="{CORE}"/></svg>')


def mark_alt_svg(size=1000):
    """Alternative: the I of the wordmark, centred on its own outline."""
    from fontTools.pens.boundsPen import BoundsPen
    font = TTFont(FONT)
    glyphs = font.getGlyphSet()
    name = font.getBestCmap()[ord("I")]
    bounds = BoundsPen(glyphs)
    glyphs[name].draw(bounds)
    x0, y0, x1, y1 = bounds.bounds
    body, _, upem = outline("I")
    scale = size * .54 / (y1 - y0)
    x = size / 2 - (x0 + x1) / 2 * scale
    y = size / 2 + (y0 + y1) / 2 * scale
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'width="{size}" height="{size}" role="img" aria-label="Iside Systems">'
            f'<rect width="{size}" height="{size}" rx="{size*.13:.0f}" fill="{CORE}"/>'
            f'<g transform="translate({x:.1f} {y:.1f}) scale({scale:.4f} -{scale:.4f})" '
            f'fill="{EDGE}">{body}</g></svg>')


def png(svg_path, out, width, bg):
    """Render through the browser-free route: Pillow cannot read SVG, so use
    the system's qlmanage-free path — cairosvg when present, else skip."""
    try:
        import cairosvg
    except ImportError:
        return False
    cairosvg.svg2png(url=str(svg_path), write_to=str(out), output_width=width,
                     background_color=bg)
    return True


def main():
    files = {
        "logo-iside-wordmark.svg": wordmark_svg(),
        "logo-iside-lockup.svg": lockup_svg(),
        "logo-iside-mark.svg": mark_svg(),
        "logo-iside-mark-alt.svg": mark_alt_svg(),
    }
    for name, svg in files.items():
        (HERE / name).write_text(svg, encoding="utf-8")
        print("wrote", name)
    for name, bg, suffix in (("logo-iside-wordmark.svg", NIGHT, "-nero"),
                             ("logo-iside-wordmark.svg", PAPER, "-carta"),
                             ("logo-iside-lockup.svg", NIGHT, "-nero"),
                             ("logo-iside-mark.svg", NIGHT, ""),
                             ("logo-iside-mark-alt.svg", NIGHT, "")):
        out = HERE / (Path(name).stem + suffix + ".png")
        if png(HERE / name, out, 1200, bg):
            print("wrote", out.name)


if __name__ == "__main__":
    main()
