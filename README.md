# elpasotrafficticketfirm.com

Static rebuild of the El Paso Traffic Ticket Firm – West website (formerly WordPress/Elementor), hosted as a Cloudflare Worker with static assets. Same URL structure and color scheme as the original.

## Layout
- `build/pages.py` — all page content, titles, meta descriptions, FAQ, reviews, nav. **Edit content here.**
- `build/build.py` — generator: header/footer, JSON-LD schema (LegalService, BreadcrumbList, BlogPosting, FAQPage), sitemap.xml, robots.txt.
- `public/` — generated HTML (committed) + `assets/site.css`, `assets/site.js`, `images/*.webp`.
- `src/index.js` — Worker: serves assets, www→apex, legacy WordPress 301/410s, `POST /api/contact` lead emails via Resend.
- `wrangler.jsonc` — Worker config (assets binding, `run_worker_first`).

## Editing
```
npm run gen                 # = python3 build/build.py && python3 build/es_build.py build  (needs: pip install beautifulsoup4 lxml)
git commit -am "..." && git push   # Cloudflare Workers Builds deploys on push to main (its build step is a no-op; public/ is committed)
```
Spanish mirror: every EN page has an `/es/<slug>/` twin (slug map in `build/es_build.py` SLUGS; translations in `build/es/strings.json`).
**Rule: any EN copy change must be mirrored to ES.** After editing EN content run `python3 build/build.py && python3 build/es_build.py extract` — new/changed strings appear with empty values in `strings.json`; translate them, then `npm run gen`. Never run `build/build.py` alone before pushing (it strips the ES toggle/hreflang from EN pages until `es_build.py build` re-adds them).
Service pages / blog posts are JSON in `build/content/` (schema in `build/content/README.md`).
Bump `SITE["v"]` in `build/pages.py` whenever `site.css` / `site.js` change (assets are cached for a year by `?v=`).

## Secrets / vars (Cloudflare → Worker → Settings)
- `RESEND_API_KEY` (secret) — required for lead emails. Until it is set the forms show the call/text fallback.
- `LEAD_TO_EMAIL` — where leads go (default west@elpasotrafficticket.com; comma-separate for several).
- `LEAD_FROM_EMAIL` — must be on a Resend-verified domain (default leads@elpasotrafficticketfirm.com).
