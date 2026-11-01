#!/usr/bin/env python3
"""Spanish mirror builder.
  python3 build/es_build.py extract   → writes build/es/strings.json with every EN string (keeps existing translations)
  python3 build/es_build.py build     → writes public/es/<slug>/index.html for every EN page + patches EN pages (hreflang, toggle)
Run `python3 build/build.py` first (EN pages must exist). Translations: build/es/strings.json {en: es}. Slugs: SLUGS below.
"""
import sys, json, pathlib, re, copy
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
ESD = ROOT / "build" / "es"; ESD.mkdir(exist_ok=True)
STR = ESD / "strings.json"
SITE = "https://elpasotrafficticketfirm.com"

SLUGS = {  # EN path → ES path
 "/": "/es/abogado-de-multas-de-transito-el-paso-tx/",
 "/services/": "/es/servicios/",
 "/areas-served/": "/es/areas-de-servicio/",
 "/contact/": "/es/contacto/",
 "/schedule-an-appointment/": "/es/agendar-una-cita/",
 "/warrant-lawyer/": "/es/abogado-de-ordenes-de-arresto/",
 "/should-i-hire-a-traffic-ticket-lawyer/": "/es/debo-contratar-un-abogado-de-multas/",
 "/faqs/": "/es/preguntas-frecuentes/",
 "/category/blog/": "/es/blog/",
 "/hire-me/": "/es/contrateme/",
 "/fight-your-ticket/": "/es/pelee-su-multa/",
 "/traffic-ticket-and-warrants-lookup-form/": "/es/consulta-de-multas-y-ordenes-de-arresto/",
 "/privacy-policy/": "/es/politica-de-privacidad/",
 "/terms-and-conditions/": "/es/terminos-y-condiciones/",
 "/texas-points-system-explained/": "/es/sistema-de-puntos-de-texas/",
 "/finding-a-traffic-ticket-dismissal-lawyer-in-el-paso-texas/": "/es/como-encontrar-un-abogado-para-desestimar-multas-en-el-paso/",
 "/how-to-fight-a-traffic-ticket-in-el-paso-texas/": "/es/como-pelear-una-multa-de-transito-en-el-paso/",
 "/defensive-driving-in-el-paso-texas/": "/es/manejo-defensivo-en-el-paso-texas/",
 "/el-paso-warrants-lifted/": "/es/ordenes-de-arresto-levantadas-en-el-paso/",
 "/speeding-ticket-lawyer-el-paso-tx/": "/es/abogado-multas-por-exceso-de-velocidad-el-paso-tx/",
 "/red-light-stop-sign-ticket-lawyer-el-paso-tx/": "/es/abogado-multas-luz-roja-y-senal-de-alto-el-paso-tx/",
 "/no-insurance-ticket-lawyer-el-paso-tx/": "/es/abogado-multa-por-no-tener-seguro-el-paso-tx/",
 "/cdl-trucking-violation-lawyer-el-paso-tx/": "/es/abogado-infracciones-cdl-y-camiones-el-paso-tx/",
 "/school-zone-speeding-ticket-lawyer-el-paso-tx/": "/es/abogado-exceso-de-velocidad-en-zona-escolar-el-paso-tx/",
 "/dps-state-trooper-ticket-lawyer-el-paso-tx/": "/es/abogado-multas-de-la-policia-estatal-dps-el-paso-tx/",
 "/failure-to-appear-lawyer-el-paso-tx/": "/es/abogado-por-falta-de-comparecencia-el-paso-tx/",
 "/no-drivers-license-ticket-lawyer-el-paso-tx/": "/es/abogado-multa-por-no-tener-licencia-el-paso-tx/",
 "/class-c-misdemeanor-lawyer-el-paso-tx/": "/es/abogado-delitos-menores-clase-c-el-paso-tx/",
 "/animal-control-ticket-lawyer-el-paso-tx/": "/es/abogado-multas-de-control-animal-el-paso-tx/",
 "/city-ordinance-violation-lawyer-el-paso-tx/": "/es/abogado-infracciones-de-ordenanzas-municipales-el-paso-tx/",
 "/moving-violation-lawyer-el-paso-tx/": "/es/abogado-infracciones-de-transito-en-movimiento-el-paso-tx/",
 "/corrective-lenses-restriction-ticket-lawyer-el-paso-tx/": "/es/abogado-multa-por-restriccion-de-lentes-correctivos-el-paso-tx/",
 "/what-happens-if-you-miss-your-court-date-in-el-paso-municipal-court/": "/es/que-pasa-si-falta-a-su-cita-en-la-corte-municipal-de-el-paso/",
 "/no-insurance-ticket-in-texas-what-it-really-costs/": "/es/multa-por-no-tener-seguro-en-texas-lo-que-realmente-cuesta/",
 "/does-a-class-c-ticket-go-on-your-record-in-texas/": "/es/una-multa-clase-c-aparece-en-su-record-en-texas/",
}
ATTRS = ["alt", "title", "aria-label", "placeholder", "content"]
SKIP_META = {"viewport", "robots", "geo.region", "geo.placename", "theme-color", "og:type", "og:locale", "og:url", "og:image", "twitter:card", "twitter:image", "og:site_name"}
NO_TRANSLATE = re.compile(r"^[\s\d\W]*$")  # numbers / punctuation only

def en_pages():
    for f in sorted(PUB.glob("**/index.html")):
        rel = "/" + str(f.relative_to(PUB).parent).replace("\\", "/")
        rel = "/" if rel == "/." else rel + "/"
        if rel.startswith("/es/"): continue
        yield rel, f

def walk(soup, fn):
    """fn(string, kind) → replacement or None. kind: 'text' | attr name."""
    for t in soup.find_all(string=True):
        if isinstance(t, (Comment, Doctype)) or t.parent.name in ("script", "style", "noscript"): continue
        s = str(t)
        if not s.strip() or NO_TRANSLATE.match(s): continue
        r = fn(s, "text")
        if r is not None: t.replace_with(r)
    for tag in soup.find_all(True):
        for a in ATTRS:
            v = tag.get(a)
            if not v or not isinstance(v, str) or not v.strip(): continue
            if a == "content":
                k = tag.get("name") or tag.get("property")
                if not k or k in SKIP_META: continue
            if tag.name == "meta" and a != "content": continue
            if NO_TRANSLATE.match(v): continue
            r = fn(v, a)
            if r is not None: tag[a] = r

def key(s):
    return re.sub(r"\s+", " ", s.strip())

def extract():
    table = json.loads(STR.read_text()) if STR.exists() else {}
    seen = set()
    for rel, f in en_pages():
        soup = BeautifulSoup(f.read_text(), "lxml")
        def fn(s, kind):
            k = key(s); seen.add(k)
            table.setdefault(k, ""); return None
        walk(soup, fn)
        # JSON-LD strings
        for sc in soup.find_all("script", type="application/ld+json"):
            for k in ld_strings(json.loads(sc.string)):
                seen.add(k); table.setdefault(k, "")
    # drop keys no longer used
    table = {k: v for k, v in table.items() if k in seen}
    STR.write_text(json.dumps(table, ensure_ascii=False, indent=0))
    todo = [k for k, v in table.items() if not v]
    print(f"{len(table)} strings, {len(todo)} untranslated, {sum(len(k.split()) for k in todo)} words to translate")

LD_KEYS = {"name", "description", "headline", "alternateName", "articleSection", "serviceType", "text", "jobTitle"}
def ld_strings(obj, out=None):
    if out is None: out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in LD_KEYS and isinstance(v, str) and v.strip() and not NO_TRANSLATE.match(v): out.append(key(v))
            else: ld_strings(v, out)
    elif isinstance(obj, list):
        for v in obj: ld_strings(v, out)
    return out

def ld_translate(obj, T):
    if isinstance(obj, dict):
        o = {}
        for k, v in obj.items():
            if k in LD_KEYS and isinstance(v, str): o[k] = T.get(key(v)) or v
            elif k == "inLanguage": o[k] = "es-US"
            elif k in ("url", "item", "@id", "mainEntityOfPage") and isinstance(v, str): o[k] = map_url(v)
            else: o[k] = ld_translate(v, T)
        return o
    if isinstance(obj, list): return [ld_translate(v, T) for v in obj]
    return obj

def map_url(u):
    for en, es in SLUGS.items():
        if u == SITE + en or u == en: return u.replace(en, es) if u.startswith(SITE) else es
        if u.startswith(SITE + en + "#"): return SITE + es + u[len(SITE + en):]
    return u

def build():
    T = json.loads(STR.read_text())
    missing = 0
    for rel, f in en_pages():
        es_rel = SLUGS.get(rel)
        if not es_rel:
            print("no ES slug for", rel); continue
        en_html = f.read_text()
        # --- ES page
        soup = BeautifulSoup(en_html, "lxml")
        soup.html["lang"] = "es"
        def fn(s, kind):
            nonlocal missing
            k = key(s); v = T.get(k)
            if v is None: return None
            if not v: missing += 1; return None
            lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
            return lead + v + trail
        walk(soup, fn)
        # links
        for a in soup.find_all("a", href=True):
            h = a["href"]
            if h.startswith("/") and not h.startswith("//"):
                base = h.split("#")[0]; frag = h[len(base):]
                if base in SLUGS: a["href"] = SLUGS[base] + frag
        for l in soup.find_all("link"):
            if l.get("rel") == ["canonical"]: l["href"] = SITE + es_rel
            if l.get("rel") == ["alternate"] and l.get("hreflang"): l.decompose()
        for m in soup.find_all("meta"):
            k = m.get("property") or m.get("name")
            if k == "og:url": m["content"] = SITE + es_rel
            if k == "og:locale": m["content"] = "es_US"
        head = soup.head
        for hl, href in (("en", SITE + rel), ("es", SITE + es_rel), ("x-default", SITE + rel)):
            tag = soup.new_tag("link", rel="alternate", hreflang=hl, href=href); head.append(tag)
        for sc in soup.find_all("script", type="application/ld+json"):
            sc.string = json.dumps(ld_translate(json.loads(sc.string), T), ensure_ascii=False, separators=(",", ":"))
        # language toggle
        add_toggle(soup, "English", rel, "en")
        out = PUB / es_rel.strip("/") / "index.html"; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(str(soup))
        # --- patch EN page: hreflang + toggle
        en = BeautifulSoup(en_html, "lxml")
        for l in en.find_all("link"):
            if l.get("rel") == ["alternate"] and l.get("hreflang"): l.decompose()
        for hl, href in (("en", SITE + rel), ("es", SITE + es_rel), ("x-default", SITE + rel)):
            en.head.append(en.new_tag("link", rel="alternate", hreflang=hl, href=href))
        add_toggle(en, "Español", es_rel, "es")
        f.write_text(str(en))
    print("ES pages built; untranslated strings hit:", missing)

def add_toggle(soup, label, href, lang):
    for old in soup.select("a.lang"): old.decompose()
    ul = soup.find("ul", id="menu")
    if ul:
        li = soup.new_tag("li"); a = soup.new_tag("a", href=href, rel="alternate", hreflang=lang); a["class"] = ["lang"]; a.string = label; li.append(a); ul.append(li)
    strip = soup.select_one(".strip .wrap")
    if strip:
        sp = soup.new_tag("span"); a = soup.new_tag("a", href=href, rel="alternate", hreflang=lang); a["class"] = ["lang"]; a.string = "🌐 " + label; sp.append(a); strip.append(sp)

if __name__ == "__main__":
    {"extract": extract, "build": build}[sys.argv[1]]()
