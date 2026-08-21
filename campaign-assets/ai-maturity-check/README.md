# AI Maturity Check — creative kit

Everything for the campaign that points at the AI Maturity Check. Layouts are
measured with real font metrics at final pixel size: no text box is estimated,
and nothing is scaled up after the fact.

- `static/` — 11 Google Ads formats
  - Demand Gen: 1200x628, 1200x1200, 960x1200, 1080x1920
  - Display: 300x250, 336x280, 728x90, 970x90, 160x600, 300x600, 320x50
- `carousel/` — five cards in 1:1, 1.91:1 and 4:5, as PNG and as editable SVG
- `video/` — silent 15s H.264 in 16:9, 1:1 and 9:16

Card order and what each one carries:

1. Diagnosi — the five-axis pentagon, the same figure the tool ends on
2. Domande — the real questions, small, drifting upward (they scroll in the video)
3. Mappa — the pentagon again, now as the result
4. Quick win — type only, no figure
5. Check — type only: the call, and the ninety-day plan

`copy.csv` holds the Demand Gen text — headlines (40), long headlines (90),
descriptions (90) and the business name (25) — with the character count of each
line, all inside Google's limits.

Final URL: https://www.isidesystems.com/ai-maturity

## Rebuild

    python3 build_ads.py       # the static formats — needs Pillow
    python3 build_assets.py    # carousel and video — needs Pillow and ffmpeg

Do not edit the exported PNG, SVG or MP4: change the script and rebuild. Fonts
resolve to the first that exists on the machine (Helvetica Neue and Menlo on
macOS, Noto on Linux), so both build hosts produce the same layout.
