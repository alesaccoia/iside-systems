# isidesystems.com

Single static page for Iside Systems SRLS, in English. No framework, no dependencies, no build step: Vercel serves `public/` as-is.

    public/index.html     the whole site: copy, styles and script inline
    public/assets/        favicons (winged disk), self-hosted Inter (OFL)
    api/contact.js        contact form endpoint (Mailjet), the only server code
    brand/                logo sources, not published
    vercel.json           serves public/, redirects every old URL to /

## Changing the site

Edit `public/index.html`, then commit and push: Vercel deploys `main`.

## Notes

- Google Tag Manager (`GTM-584NQHC3`) loads with Consent Mode v2 set to denied for every purpose and nothing ever grants it: Google Ads tags send cookieless pings only, no cookie is set, so there is no cookie bar. Granting any consent type requires adding one. The font is served from this domain.
- A successful form submission pushes `contact_sent` to the dataLayer, for a conversion trigger in GTM.
- The contact form posts to `/api/contact`. Mailjet credentials live in Vercel environment variables (see `.env.example`), never in the repository.
- The previous multi-page site (blog, case studies, labs, AI Maturity Check) is in the git history before the `pagina-unica` branch.
