# AI Opportunity Sprint — Google Ads asset kit

Upload-ready creative for Iside Systems, designed from the site’s dark palette:
`#0e0e11` charcoal, `#eceae4` warm white, and `#ff4a2b` coral accent.

## Deliverables

- `static/`: fourteen Google Display / responsive-image sizes, in editable SVG and upload-ready PNG.
- `carousel/`: three-message sequence in square, landscape, and portrait crops, in SVG and PNG.
- `video/`: silent 15-second rotating-panel videos in 16:9, 1:1, and 9:16 H.264 MP4.
- `copy.csv`: ad copy, carousel order, and final URLs to paste into Google Ads.

## Recommended use

| Placement | Assets |
| --- | --- |
| Demand Gen / Discovery image ad | `static/*1200x628.png`, `*1200x1200.png`, `*960x1200.png` |
| Responsive Display / Display placements | all files in `static/` |
| Carousel sequence | the matching-size `carousel/carousel_1`, `_2`, `_3` files in that order |
| Video action / Demand Gen video | the three files in `video/` |

The videos have no audio; use the supplied on-screen copy and captions in the ad platform. Keep the visible URL / final URL aligned to the actual booking page before publishing.

## Rebuild

`python3 build_assets.py`

The SVG sources remain editable; avoid changing the PNG or MP4 manually.
