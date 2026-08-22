# LinkedIn covers

Two banners, drawn at final pixel size with real font metrics. No mark: on a
personal profile the picture already carries it, and a company page draws the
logo over the lower left of the banner. What is left is the type and the same
lattice the site's hero draws.

| File | Size | Where |
| --- | --- | --- |
| iside-linkedin-profile-1584x396.png | 1584x396 | personal profile cover |
| iside-linkedin-page-1128x191.png | 1128x191 | company page cover |

Both keep a clear strip on the left — 430px on the profile, 270px on the page —
because that is where LinkedIn puts the avatar and the logo. On phones the
cover is cropped from the centre, so nothing that matters sits near the edges.

Rebuild: python3 build_banner.py
