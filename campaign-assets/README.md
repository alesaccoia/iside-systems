# Iside Systems campaign assets

This folder keeps all campaign deliverables alongside the site that they
promote. Generated PNG and MP4 files are committed intentionally: they are
the upload-ready creative, while the included Python build scripts are the
editable source of truth.

## Contents

| Folder | Purpose | Main deliverables |
| --- | --- | --- |
| ai-maturity-check | Traffic to the AI Maturity Check at /ai-maturity | 11 static Google Ads formats; 5-card carousel in three crops; 16:9, 1:1 and 9:16 videos |
| ai-advisory | AI Advisory narrative | 5-card carousel in three crops; 16:9, 1:1 and 9:16 videos |
| ai-opportunity-sprint | Paid AI Opportunity Sprint | Display banners, carousel, and three videos |

## Rebuild

Run the script from the relevant campaign folder:

    python3 build_ads.py
    python3 build.py
    python3 build_assets.py

The Maturity Check scripts require Pillow, and ffmpeg for the videos. The
Advisory and Sprint scripts also require rsvg-convert. Do not edit the exported PNG/MP4
directly; change the matching build script and rebuild.

## Google Ads final URLs

- AI Maturity Check: https://www.isidesystems.com/ai-maturity
- Advisory and Opportunity Sprint: https://www.isidesystems.com/chi-sono.html#contact
