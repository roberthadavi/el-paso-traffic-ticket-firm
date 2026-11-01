#!/usr/bin/env python3
"""Static site generator for elpasotrafficticketfirm.com.
Run: python3 build/build.py   → writes public/**/index.html, sitemap.xml, robots.txt
Content lives in build/pages.py. Header/footer/schema live here."""
import json, pathlib, datetime, re, html
import pages as P
import services as S

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SITE = P.SITE
TODAY = datetime.date.today().isoformat()

ICON = {
 "fb": '<svg viewBox="0 0 320 512" aria-hidden="true"><path d="M279.1 288l14.2-92.7h-88.9v-60.1c0-25.4 12.4-50.1 52.2-50.1h40.4V6.3S260.4 0 225.4 0c-73.2 0-121.1 44.4-121.1 124.7v70.6H22.9V288h81.4v224h100.2V288z"/></svg>',
 "tw": '<svg viewBox="0 0 512 512" aria-hidden="true"><path d="M389.2 48h70.6L305.6 224.2 487 464H345L233.7 318.6 106.5 464H35.8L200.7 275.5 26.8 48H172.4L272.9 180.9 389.2 48zM364.4 421.8h39.1L151.1 88h-42L364.4 421.8z"/></svg>',
 "ig": '<svg viewBox="0 0 448 512" aria-hidden="true"><path d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z"/></svg>',
 "in": '<svg viewBox="0 0 448 512" aria-hidden="true"><path d="M100.3 448H7.4V148.9h92.9zM53.8 108.1C24.1 108.1 0 83.5 0 53.8a53.8 53.8 0 0 1 107.6 0c0 29.7-24.1 54.3-53.8 54.3zM447.9 448h-92.7V302.4c0-34.7-.7-79.2-48.3-79.2-48.3 0-55.7 37.7-55.7 76.7V448h-92.8V148.9h89.1v40.8h1.3c12.4-23.5 42.7-48.3 87.9-48.3 94 0 111.3 61.9 111.3 142.3V448z"/></svg>',
 "g": '<svg viewBox="0 0 488 512" aria-hidden="true"><path d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"/></svg>',
 "phone": '<svg viewBox="0 0 512 512" aria-hidden="true"><path d="M497.4 361.8l-112-48a24 24 0 0 0-28 6.9l-49.6 60.6A370.7 370.7 0 0 1 130.6 204.1l60.6-49.6a23.9 23.9 0 0 0 6.9-28l-48-112A24.2 24.2 0 0 0 122.6.6l-104 24A24 24 0 0 0 0 48c0 256.5 207.9 464 464 464a24 24 0 0 0 23.4-18.6l24-104a24.3 24.3 0 0 0-14-27.6z"/></svg>',
 "hand": '<svg viewBox="0 0 512 512" aria-hidden="true"><path d="M512 176.001C512 273.203 433.202 352 336 352h-32V448h-96V352H144c-26.51 0-48-21.49-48-48V240H48c-26.51 0-48-21.49-48-48 0-46.392 37.608-84 84-84h12V48c0-26.51 21.49-48 48-48s48 21.49 48 48v60h32V48c0-26.51 21.49-48 48-48s48 21.49 48 48v60h32V48c0-26.51 21.49-48 48-48s48 21.49 48 48v60.2c43.063 8.03 76 45.857 76 91.8h16c26.51 0 48 21.49 48 48z"/></svg>',
}

def esc(s): return html.escape(s, quote=True)

def nav_html(cur):
    items = []
    for label, href in SITE["nav"]:
        ac = ' aria-current="page"' if href == cur else ''
        items.append(f'<li><a href="{href}"{ac}>{label}</a></li>')
    return "\n".join(items)

def head(p):
    url = SITE["url"] + p["path"]
    title = p["title"]
    desc = p["description"]
    img = SITE["url"] + p.get("image", "/images/el-paso-traffic-ticket-firm-google-reviews-550.webp")
    robots = p.get("robots", "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")
    ld = json.dumps(schema(p), ensure_ascii=False, separators=(",", ":"))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{"" if p.get("nocanonical") else f'<link rel="canonical" href="{url}">'}
<meta name="robots" content="{robots}">
<meta property="og:type" content="{'article' if p.get('type')=='post' else 'website'}">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="El Paso">
<meta name="theme-color" content="#D72227">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Maven+Pro:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={SITE['v']}">
{p.get('head_extra','')}
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span>📞 Call <a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a></span><span class="hours">Free case evaluation · Mon–Fri 7:30–6:30 · Sat 9–4 · Se habla español</span><span><a href="/traffic-ticket-and-warrants-lookup-form/">Free warrant check →</a></span></div></div>
<header class="hdr">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{esc(SITE['name'])} home"><img src="/images/el-paso-traffic-ticket-firm-logo-300.webp" srcset="/images/el-paso-traffic-ticket-firm-logo-300.webp 300w, /images/el-paso-traffic-ticket-firm-logo-510.webp 510w" sizes="150px" width="150" height="95" alt="El Paso Traffic Ticket Firm logo — Traffic Ticket Lawyer El Paso, TX" fetchpriority="high"></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="menu">☰ Menu</button>
    <nav class="nav" aria-label="Main">
      <ul id="menu">
{nav_html(p["path"])}
      </ul>
    </nav>
    <a class="btn cta" href="/fight-your-ticket/">Fight Your Ticket</a>
  </div>
</header>
<main id="main">
'''

def footer(p):
    s = SITE
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{ICON[k]}</a>' for k, n, u in s["social"])
    year = datetime.date.today().year
    return f'''</main>
<footer>
  <div class="main">
    <div class="wrap">
      <h2>El Paso Traffic Ticket Firm – West</h2>
      <div class="social">{soc}</div>
      <div class="cols3">
        <div>
          <h3>Contact</h3>
          <p><strong>El Paso Traffic Ticket Firm – West</strong><br>{s['address']}<br>Phone: <a href="tel:{s['phone_e164']}">{s['phone']}</a><br>Email: <a href="mailto:{s['email']}">{s['email']}</a></p>
          <p><a href="{s['maps']}" target="_blank" rel="noopener">Directions &amp; Google reviews</a></p>
        </div>
        <div>
          <h3>Traffic Ticket Help</h3>
          <ul>
            <li><a href="/">Traffic Ticket Lawyer El Paso</a></li>
            <li><a href="/services/">All Services</a></li>
            <li><a href="/areas-served/">Areas Served</a></li>
            <li><a href="/warrant-lawyer/">Warrant Lawyer</a></li>
            <li><a href="/should-i-hire-a-traffic-ticket-lawyer/">Should I Hire a Traffic Ticket Lawyer?</a></li>
            <li><a href="/fight-your-ticket/">Fight Your Ticket</a></li>
            <li><a href="/hire-me/">Hire Me Online</a></li>
            <li><a href="/traffic-ticket-and-warrants-lookup-form/">Check for Tickets / Warrants</a></li>
            <li><a href="/schedule-an-appointment/">Schedule an Appointment</a></li>
            <li><a href="/faqs/">FAQs</a></li>
            <li><a href="/contact/">Contact</a></li>
          </ul>
        </div>
        <div>
          <h3>Traffic Blog</h3>
          <ul>
            <li><a href="/category/blog/">All blog posts</a></li>
            <li><a href="/how-to-fight-a-traffic-ticket-in-el-paso-texas/">How to Fight a Traffic Ticket in El Paso</a></li>
            <li><a href="/texas-points-system-explained/">Texas Points System Explained</a></li>
            <li><a href="/defensive-driving-in-el-paso-texas/">Defensive Driving in El Paso</a></li>
            <li><a href="/el-paso-warrants-lifted/">El Paso Warrants Lifted</a></li>
            <li><a href="/finding-a-traffic-ticket-dismissal-lawyer-in-el-paso-texas/">Finding a Ticket Dismissal Lawyer</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="bottom">
    <p>© Copyright {year} all rights reserved. <a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms-and-conditions/">Terms and Conditions</a></p>
    <p>El Paso Traffic Ticket Firm – West. Attorney Robert Navar, principal office {s['address']}. LEGAL DISCLAIMER: The information on this website is for advertising and general information purposes. This information is not intended to be legal advice for you to rely on. Past results do not guarantee a similar outcome; no result is guaranteed.</p>
  </div>
</footer>
<div class="mobile-call"><a href="tel:{s['phone_e164']}">📞 Call {s['phone']}</a><a class="fight" href="/fight-your-ticket/">Fight Your Ticket</a></div>
<script src="/assets/site.js?v={SITE['v']}" defer></script>
<!-- Cloudflare Web Analytics --><script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "3e55cb8c58d646d4bf0d2b1bc2913885"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
'''

def org():
    s = SITE
    return {
        "@type": ["LegalService", "Attorney"],
        "@id": s["url"] + "/#organization",
        "name": "El Paso Traffic Ticket Firm – West",
        "alternateName": s["name"],
        "url": s["url"] + "/",
        "logo": s["url"] + "/images/el-paso-traffic-ticket-firm-logo.png",
        "image": s["url"] + "/images/el-paso-traffic-ticket-firm-team-1200.webp",
        "telephone": s["phone_e164"],
        "email": s["email"],
        "priceRange": "$$",
        "description": "Traffic ticket lawyer in El Paso, TX. Attorney Robert Navar fights speeding tickets, warrants, failure to appear, no insurance tickets and all Class C misdemeanors in El Paso Municipal Court and Justice of the Peace courts. Free consultations.",
        "address": {"@type": "PostalAddress", "streetAddress": "7362 Remcon Cir", "addressLocality": "El Paso", "addressRegion": "TX", "postalCode": "79912", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 31.8393468, "longitude": -106.5630568},
        "hasMap": s["maps"],
        "areaServed": [{"@type": "City", "name": n} for n in ["El Paso", "Canutillo", "Horizon City", "Socorro", "Clint", "Anthony", "Vinton"]] + [{"@type": "AdministrativeArea", "name": "El Paso County, Texas"}],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:30", "closes": "18:30"}, {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "16:00"}],
        "founder": {"@type": "Person", "name": "Robert Navar", "jobTitle": "Attorney", "alumniOf": "Southern Methodist University Dedman School of Law"},
        "knowsAbout": ["Traffic tickets", "Speeding tickets", "Traffic warrants", "Failure to appear", "No insurance tickets", "CDL violations", "Class C misdemeanors", "Defensive driving dismissal", "Deferred adjudication"],
        "sameAs": [u for _, _, u in s["social"]] + [s["maps"]],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Traffic ticket defense services", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "areaServed": "El Paso, TX", "url": s["url"] + ("/warrant-lawyer/" if "Warrant" in n else "/fight-your-ticket/")}} for n in P.SERVICES]},
    }

def schema(p):
    s = SITE
    graph = [org(), {"@type": "WebSite", "@id": s["url"] + "/#website", "url": s["url"] + "/", "name": s["name"], "publisher": {"@id": s["url"] + "/#organization"}, "inLanguage": "en-US"}]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": s["url"] + "/"}]
    if p["path"] != "/":
        if p.get("type") == "post":
            crumbs.append({"@type": "ListItem", "position": 2, "name": "Blog", "item": s["url"] + "/category/blog/"})
        if p.get("type") == "service":
            crumbs.append({"@type": "ListItem", "position": 2, "name": "Services", "item": s["url"] + "/services/"})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": p["h1"], "item": s["url"] + p["path"]})
    graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    wp = {"@type": p.get("page_type", "WebPage"), "@id": s["url"] + p["path"] + "#webpage", "url": s["url"] + p["path"], "name": p["title"], "description": p["description"], "isPartOf": {"@id": s["url"] + "/#website"}, "about": {"@id": s["url"] + "/#organization"}, "inLanguage": "en-US", "dateModified": TODAY}
    if p.get("image"):
        wp["primaryImageOfPage"] = {"@type": "ImageObject", "url": s["url"] + p["image"]}
    graph.append(wp)
    if p.get("type") == "post":
        graph.append({"@type": "BlogPosting", "@id": s["url"] + p["path"] + "#article", "headline": p["h1"], "description": p["description"], "image": s["url"] + p["image"], "datePublished": p["date"], "dateModified": p.get("modified", TODAY), "author": {"@type": "Person", "name": "Robert Navar", "url": s["url"] + "/contact/"}, "publisher": {"@id": s["url"] + "/#organization"}, "mainEntityOfPage": {"@id": s["url"] + p["path"] + "#webpage"}, "inLanguage": "en-US", "articleSection": "Traffic Blog"})
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in p["faq"]]})
    for extra in p.get("schema_extra", []):
        graph.append(extra)
    return {"@context": "https://schema.org", "@graph": graph}

def write(path, content):
    f = PUB / path.strip("/") / "index.html" if path != "/" else PUB / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content)

def main():
    P.PAGES.extend(S.pages())
    for p in P.PAGES:
        body = p["body"]() if callable(p["body"]) else p["body"]
        write(p["path"], head(p) + body + footer(p))
    # 404
    p404 = {"path": "/404/", "title": "Page Not Found | " + SITE["name"], "description": "The page you requested could not be found.", "h1": "Page not found", "robots": "noindex, follow", "nocanonical": True}
    (PUB / "404.html").write_text(head(p404) + P.body_404() + footer(p404))
    # sitemap
    urls = [p for p in P.PAGES if "noindex" not in p.get("robots", "")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for p in urls:
        sm.append("<url>")
        sm.append(f"<loc>{SITE['url']}{p['path']}</loc>")
        sm.append(f"<lastmod>{p.get('modified', TODAY)}</lastmod>")
        sm.append(f"<changefreq>{p.get('changefreq','monthly')}</changefreq>")
        sm.append(f"<priority>{p.get('priority','0.7')}</priority>")
        if p.get("image"):
            sm.append(f"<image:image><image:loc>{SITE['url']}{p['image']}</image:loc></image:image>")
        sm.append("</url>")
    # Spanish twins (built by es_build.py from the same page list)
    try:
        import es_build
        for p in urls:
            es = es_build.SLUGS.get(p["path"])
            if not es: continue
            sm.append("<url>")
            sm.append(f"<loc>{SITE['url']}{es}</loc>")
            sm.append(f"<lastmod>{p.get('modified', TODAY)}</lastmod>")
            sm.append(f"<changefreq>{p.get('changefreq','monthly')}</changefreq>")
            sm.append(f"<priority>{p.get('priority','0.7')}</priority>")
            sm.append("</url>")
    except ImportError:
        pass
    sm.append("</urlset>")
    (PUB / "sitemap.xml").write_text("\n".join(sm))
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    print(f"Built {len(P.PAGES)} pages + 404, sitemap ({len(urls)} URLs)")

if __name__ == "__main__":
    main()
