# iside.systems

Static bilingual site for Iside Systems SRLS. No framework, no dependencies,
no build step in production — Vercel serves `dist/` as-is.

    /            Italian   index.html · progetti.html · chi-sono.html
    /en/         English   index.html · projects.html · about.html

## Layout

    build.py              generates all six pages; every string lives here
    deploy.sh             runs build.py, then copies only publishable files into dist/
    assets/site.css       shared stylesheet (light + dark)
    assets/site.js        shared behaviour (figures, filters, theme, consent)
    assets/img/           mark, favicons, social card, portrait
    assets/img/make-assets.py   regenerates the raster icons and the OG card
    dist/                 what Vercel serves — generated, do not edit by hand

## Changing the site

Copy lives in the `L_IT` / `L_EN` dictionaries in `build.py`, projects in the
`PROJECTS` list. Edit there, then:

    ./deploy.sh
    git add -A && git commit -m "..." && git push

Editing the HTML directly works until the next build overwrites it.

Domain and Google Tag Manager id are the `SITE` and `GTM` constants at the top
of `build.py`.

## Notes

- Consent Mode v2: everything is denied until the visitor accepts in the
  cookie bar. GTM loads either way but writes nothing without consent.
- The contact form has no backend: it opens the visitor's mail client with the
  message prefilled. Point it at an endpoint if that changes.
- Figures are drawn on canvas from a fixed seed, so they look identical on
  every visit. Nothing animates except the project thumbnails, gently.
