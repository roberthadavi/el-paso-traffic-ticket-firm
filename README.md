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
python3 build/build.py      # regenerate public/**/index.html + sitemap
git commit -am "..." && git push   # Cloudflare Workers Builds deploys on push to main
```
Bump `SITE["v"]` in `build/pages.py` whenever `site.css` / `site.js` change (assets are cached for a year by `?v=`).

## Secrets / vars (Cloudflare → Worker → Settings)
- `RESEND_API_KEY` (secret) — required for lead emails. Until it is set the forms show the call/text fallback.
- `LEAD_TO_EMAIL` — where leads go (default help@elpasotrafficticket.com; comma-separate for several).
- `LEAD_FROM_EMAIL` — must be on a Resend-verified domain (default leads@elpasotrafficticketfirm.com).
