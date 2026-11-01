# Service landing pages, /services/ hub, areas-served page and JSON blog posts.
# Content lives in build/content/services/*.json and build/content/posts/*.json (see build/content/README.md).
import json, pathlib, html
import pages as P

HERE = pathlib.Path(__file__).resolve().parent
SVC_DIR = HERE / "content" / "services"
POST_DIR = HERE / "content" / "posts"
SITE = P.SITE; PH = P.PH; TEL = P.TEL; MAIL = P.MAIL

# Simple line icons (currentColor) for service tiles
ICONS = {
 "gauge": '<path d="M12 4a9 9 0 0 0-9 9c0 2.4.9 4.5 2.4 6.1h13.2A9 9 0 0 0 12 4zm0 2a7 7 0 0 1 5.9 10.8l-4.5-4.5a2 2 0 1 0-1.4 1.4l-1.9 3.3A7 7 0 0 1 12 6z"/>',
 "light": '<path d="M9 2h6a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm3 3a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm0 5a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm0 5a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/>',
 "shield": '<path d="M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5l-8-3zm-1 14-3.5-3.5 1.4-1.4L11 13.2l4.6-4.6 1.4 1.4L11 16z"/>',
 "truck": '<path d="M2 6h12v9H2zM14 9h4l3 3v3h-7zM6 19a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm12 0a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"/>',
 "star": '<path d="M12 2l2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.3 5.9 20.6l1.4-6.8L2.2 9.1l6.9-.8z"/>',
 "stop": '<path d="M7.8 2h8.4L22 7.8v8.4L16.2 22H7.8L2 16.2V7.8zM11 7v6h2V7zm0 8v2h2v-2z"/>',
 "school": '<path d="M12 3 1 8l11 5 9-4.1V15h2V8zm-7 9.5V16c0 1.7 3.1 3 7 3s7-1.3 7-3v-3.5l-7 3.2z"/>',
 "eye": '<path d="M12 5C6.5 5 2.3 8.6 1 12c1.3 3.4 5.5 7 11 7s9.7-3.6 11-7c-1.3-3.4-5.5-7-11-7zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm0-6a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/>',
 "car": '<path d="M5 11 6.5 6.5h11L19 11h1a1 1 0 0 1 1 1v6h-2v2h-3v-2H8v2H5v-2H3v-6a1 1 0 0 1 1-1zm2.1 0h9.8l-.9-2.5H8zM6.5 15a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm11 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>',
 "box": '<path d="M12 2 2 7v10l10 5 10-5V7zm0 2.2L18.8 7.6 12 11 5.2 7.6zM4 9.3l7 3.5v7.6l-7-3.5z"/>',
 "building": '<path d="M3 21V5l9-3 9 3v16h-7v-5h-4v5zm4-11h2V8H7zm4 0h2V8h-2zm4 0h2V8h-2zM7 14h2v-2H7zm8 0h2v-2h-2z"/>',
 "scale": '<path d="M11 2h2v3h5l-3 7h6a4 4 0 0 1-8 0h.2L15 7h-2v12h5v2H6v-2h5V7H9l1.8 5H11a4 4 0 0 1-8 0h6L6 5h5z"/>',
 "warrant": '<path d="M6 2h9l5 5v15H6zm8 1.5V8h4.5zM8 11h8v2H8zm0 4h8v2H8z"/>',
}
def icon_svg(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">{ICONS.get(name, ICONS["scale"])}</svg>'

def load(dirpath):
    out = []
    if not dirpath.exists(): return out
    for f in sorted(dirpath.glob("*.json")):
        d = json.loads(f.read_text())
        d.setdefault("slug", f.stem)
        out.append(d)
    return out

SERVICES = load(SVC_DIR)
BY_SLUG = {s["slug"]: s for s in SERVICES}
ORDER = ["speeding-ticket-lawyer-el-paso-tx", "red-light-stop-sign-ticket-lawyer-el-paso-tx", "no-insurance-ticket-lawyer-el-paso-tx", "failure-to-appear-lawyer-el-paso-tx", "warrant-lawyer", "dps-state-trooper-ticket-lawyer-el-paso-tx", "school-zone-speeding-ticket-lawyer-el-paso-tx", "cdl-trucking-violation-lawyer-el-paso-tx", "no-drivers-license-ticket-lawyer-el-paso-tx", "moving-violation-lawyer-el-paso-tx", "corrective-lenses-restriction-ticket-lawyer-el-paso-tx", "class-c-misdemeanor-lawyer-el-paso-tx", "animal-control-ticket-lawyer-el-paso-tx", "city-ordinance-violation-lawyer-el-paso-tx"]
WARRANT = {"slug": "warrant-lawyer", "h1": "Warrant Lawyer El Paso, TX", "short": "Alias and capias warrants recalled with an appearance bond, then we fight the underlying ticket.", "icon": "warrant"}

def svc_path(slug): return "/warrant-lawyer/" if slug == "warrant-lawyer" else f"/{slug}/"
def svc_meta(slug): return WARRANT if slug == "warrant-lawyer" else BY_SLUG.get(slug)

def tile(slug):
    s = svc_meta(slug)
    if not s: return ""
    return f'<a class="tile" href="{svc_path(slug)}"><span class="ic">{icon_svg(s.get("icon","scale"))}</span><span class="t">{s["h1"].replace(" El Paso, TX","")}</span><span class="d">{html.escape(s.get("short",""))}</span><span class="more">Learn more →</span></a>'

def tiles(slugs): return '<div class="tiles">' + "".join(tile(s) for s in slugs) + "</div>"

def faq_html(faq):
    if not faq: return ""
    items = "".join(f'<details><summary>{html.escape(q["q"])}</summary><div class="a"><p>{html.escape(q["a"])}</p></div></details>' for q in faq)
    return f'<h2>Frequently asked questions</h2><div class="faq">{items}</div>'

def resources_html(res):
    if not res: return ""
    lis = "".join(f'<li><a href="{r["url"]}" target="_blank" rel="noopener">{html.escape(r["label"])}</a></li>' for r in res)
    return f'<aside class="resources"><h3>Helpful official resources</h3><ul>{lis}</ul></aside>'

def service_body(s):
    secs = "".join(f'<h2>{html.escape(x["h2"])}</h2>{x["html"]}' for x in s["sections"])
    rel = [r for r in s.get("related", []) if svc_meta(r)]
    return f'''
<div class="band"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/services/">Services</a> › <span>{html.escape(s["h1"])}</span></nav><h1>{html.escape(s["h1"])}</h1><p>{html.escape(s.get("short",""))}</p>
<div class="ctarow" style="margin:22px 0 0"><a class="btn" href="/fight-your-ticket/">Fight Your Ticket</a><a class="btn ghost" href="tel:{SITE['phone_e164']}">Call {PH}</a></div></div></div>
<section class="sec"><div class="wrap layout">
<article class="content">
  {s["intro"]}
  {secs}
  {faq_html(s.get("faq"))}
  <div class="callout"><strong>Talk to a lawyer about your ticket.</strong> Free case evaluation by phone or text at {TEL}, or <a href="/fight-your-ticket/">send us your citation online</a>. No office visit needed.</div>
  {resources_html(s.get("resources"))}
  <section class="related-svc"><h2>Related services</h2>{tiles(rel)}</section>
  {P.related([("All services", "/services/"), ("Should I Hire a Traffic Ticket Lawyer?", "/should-i-hire-a-traffic-ticket-lawyer/"), ("Frequently Asked Questions", "/faqs/"), ("Check for tickets & warrants (free)", "/traffic-ticket-and-warrants-lookup-form/")])}
</article>
{P.sidebar()}
</div></section>'''

def hub_body():
    return f'''
<div class="band"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span>Services</span></nav><h1>Traffic Ticket Lawyer Services in El Paso, TX</h1><p>Every Class C citation we defend in El Paso Municipal Court, the El Paso County Justice of the Peace courts and the surrounding city courts</p></div></div>
<section class="sec"><div class="wrap">
  <p class="lead center" style="max-width:860px;margin:0 auto 36px">Whatever the citation says, the goal is the same: keep a conviction off your record without you going to court. Pick the ticket you received, or <a href="/traffic-ticket-and-warrants-lookup-form/">let us look it up for free</a> if you're not sure what you have.</p>
  {tiles(ORDER)}
  <div class="ctarow" style="margin-top:40px"><a class="btn lg" href="/fight-your-ticket/">Fight Your Ticket</a><a class="btn lg outline" href="tel:{SITE['phone_e164']}">Call {PH}</a></div>
</div></section>
<section class="sec alt"><div class="wrap content" style="max-width:900px">
  <h2 style="margin-top:0">How we handle an El Paso traffic ticket</h2>
  <ol class="steps">
    <li><strong>Free case evaluation.</strong> Call, text or <a href="/fight-your-ticket/">send the citation online</a>. We check every El Paso court for other tickets or warrants under your name at no charge.</li>
    <li><strong>Flat fee, quoted up front.</strong> You know the cost before we start. Most clients find it is less than the fine plus the insurance increase a conviction causes.</li>
    <li><strong>We appear for you.</strong> We file our appearance so you do not miss work or school, request discovery, and pursue a dismissal, deferred disposition or driving safety course — whichever protects your record.</li>
    <li><strong>You get updates until it's closed.</strong> Text or email, your choice.</li>
  </ol>
  <p>Serving El Paso and the surrounding communities — see our <a href="/areas-served/">areas served</a> page. Read <a href="/should-i-hire-a-traffic-ticket-lawyer/">why hiring a lawyer usually costs less than paying the ticket</a>.</p>
</div></section>'''

AREAS = [
 ("El Paso (West Side)", "Our office is at 7362 Remcon Cir on the West Side, near Mesa and I-10. City of El Paso police tickets are filed in El Paso Municipal Court downtown; we appear there for you."),
 ("El Paso (East, Northeast, Central, Mission Valley)", "Tickets from any El Paso Police Department regional command — Pebble Hills, Mission Valley, Northeast, Central, Westside — all go to the same Municipal Court. You never need to come to our office."),
 ("Fort Bliss", "Soldiers and families stationed at Fort Bliss, often with out-of-state licenses and insurance. We handle city, county and DPS tickets while you are deployed or in the field."),
 ("Socorro", "Socorro Police citations are heard in Socorro Municipal Court. We appear there and in the El Paso County JP courts for Lower Valley tickets."),
 ("Horizon City", "Horizon City Municipal Court for city police tickets; county JP Precinct courts for Sheriff and DPS tickets on I-10 and Horizon Blvd."),
 ("Canutillo & Vinton", "Village of Vinton Municipal Court and the JP Precinct 1 courts covering the Upper Valley and Canutillo; many DPS tickets on I-10 near the New Mexico line."),
 ("Anthony, TX", "Anthony Municipal Court and the JP courts; tickets from the DPS weigh station and the I-10 corridor, including CDL citations."),
 ("Clint, San Elizario & Fabens", "Lower Valley tickets from the Sheriff's Office, constables and DPS are filed in the El Paso County Justice of the Peace precincts; we handle them without you traveling."),
]
def areas_body():
    cards = "".join(f'<div class="area"><h2>{html.escape(n)}</h2><p>{html.escape(d)}</p></div>' for n, d in AREAS)
    return f'''
<div class="band"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span>Areas Served</span></nav><h1>Areas Served — Traffic Ticket Lawyer for El Paso County</h1><p>City, county and DPS tickets anywhere in El Paso County, handled by phone — no office visit required</p></div></div>
<section class="sec"><div class="wrap">
  <div class="areas">{cards}</div>
  <div class="callout" style="margin-top:36px"><strong>Which court is my ticket in?</strong> The court name is printed on the citation. City police tickets go to that city's municipal court; Sheriff, constable and Texas DPS trooper tickets go to an El Paso County Justice of the Peace precinct. Not sure? <a href="/traffic-ticket-and-warrants-lookup-form/">We'll look it up for free</a>, or check the <a href="https://public-fce.elpasotexas.gov/fullcourtweb/start.do" target="_blank" rel="noopener">El Paso Municipal Court</a> and <a href="https://casesearch.epcounty.com/PublicAccess/default.aspx" target="_blank" rel="noopener">El Paso County</a> case searches yourself.</div>
  <div class="ctarow"><a class="btn" href="/fight-your-ticket/">Fight Your Ticket</a><a class="btn outline" href="/services/">See all services</a></div>
</div></section>'''

def post_body(p):
    return P.post_wrap(
        {"h1": p["h1"], "date": p["date"], "img": f'/images/{p["image"]}-800.webp', "alt": p["image_alt"], "path": f'/{p["slug"]}/'},
        p["html"] + faq_html(p.get("faq")),
        [("All blog posts", "/category/blog/"), ("Fight Your Ticket", "/fight-your-ticket/"), ("Warrant Lawyer", "/warrant-lawyer/"), ("All services", "/services/")],
        published=p["date"])

POSTS = load(POST_DIR)

def pages():
    out = []
    for s in SERVICES:
        out.append({"path": f'/{s["slug"]}/', "title": s["title"], "h1": s["h1"], "description": s["description"], "body": (lambda s=s: service_body(s)),
                    "faq": [(q["q"], q["a"]) for q in s.get("faq", [])], "priority": "0.8", "changefreq": "monthly", "type": "service",
                    "image": "/images/el-paso-traffic-ticket-firm-team-1200.webp",
                    "schema_extra": [{"@type": "Service", "name": s["h1"], "serviceType": s["h1"].replace(" El Paso, TX", ""), "provider": {"@id": SITE["url"] + "/#organization"}, "areaServed": {"@type": "AdministrativeArea", "name": "El Paso County, Texas"}, "url": SITE["url"] + f'/{s["slug"]}/', "description": s["description"]}]})
    if SERVICES:
        out.append({"path": "/services/", "title": "Traffic Ticket Lawyer Services in El Paso, TX | Navar Law", "h1": "Traffic Ticket Lawyer Services in El Paso, TX",
                    "description": "Every Class C ticket we defend in El Paso: speeding, red light, no insurance, school zone, CDL, DPS trooper, failure to appear, warrants, ordinance and animal control.",
                    "body": hub_body, "page_type": "CollectionPage", "priority": "0.9", "changefreq": "monthly",
                    "schema_extra": [{"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE["url"] + svc_path(sl), "name": svc_meta(sl)["h1"]} for i, sl in enumerate(ORDER) if svc_meta(sl)]}]})
        out.append({"path": "/areas-served/", "title": "Areas Served | Traffic Ticket Lawyer El Paso County, TX", "h1": "Areas Served — Traffic Ticket Lawyer for El Paso County",
                    "description": "Traffic ticket defense across El Paso County: El Paso, Fort Bliss, Socorro, Horizon City, Canutillo, Vinton, Anthony, Clint and Fabens — municipal, JP and DPS tickets by phone.",
                    "body": areas_body, "priority": "0.6", "changefreq": "yearly"})
    for p in POSTS:
        out.append({"path": f'/{p["slug"]}/', "title": p["title"], "h1": p["h1"], "description": p["description"], "image": f'/images/{p["image"]}-800.webp', "type": "post", "date": p["date"], "modified": p["date"], "body": (lambda p=p: post_body(p)), "faq": [(q["q"], q["a"]) for q in p.get("faq", [])], "priority": "0.6", "changefreq": "yearly"})
    return out
