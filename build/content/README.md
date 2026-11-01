# Content files for elpasotrafficticketfirm.com

Each service page / blog post is a JSON file in this folder. The generator (`build/build.py`) renders them.

## Service page JSON (`services/<slug>.json`)
```json
{
  "slug": "speeding-ticket-lawyer-el-paso-tx",
  "h1": "Speeding Ticket Lawyer El Paso, TX",
  "title": "Speeding Ticket Lawyer El Paso, TX | El Paso Traffic Ticket Firm",   (<= 65 chars)
  "description": "...",                                                        (120-155 chars)
  "short": "One-sentence card blurb used on the /services/ hub and related-service tiles.",
  "icon": "gauge",                       (one of: gauge, light, shield, truck, star, stop, school, eye, car, box, building, scale, warrant)
  "intro": "<p>...</p><p>...</p>",       (2 paragraphs HTML, lawyer voice, 'El Paso' + the service keyword in the first sentence)
  "sections": [ {"h2": "...", "html": "<p>...</p><ul>...</ul>"} , ... ],   (5-7 sections, 900-1200 words total page)
  "faq": [ {"q": "...", "a": "..."} , ... ],                                (4-6 Q&A, plain text answers, no HTML)
  "resources": [ {"label": "Texas Transportation Code §545.351 (speed)", "url": "https://statutes.capitol.texas.gov/Docs/TN/htm/TN.545.htm#545.351"} ],  (2-4 official outbound links: statutes.capitol.texas.gov, elpasotexas.gov, epcounty.com, dps.texas.gov, tdlr.texas.gov, txdmv.gov, tdi.texas.gov, fmcsa.dot.gov)
  "related": ["warrant-lawyer-el-paso-tx", "no-insurance-ticket-lawyer-el-paso-tx"]   (3 slugs of other services; the warrant page is "/warrant-lawyer/" — use slug "warrant-lawyer")
}
```

## Blog post JSON (`posts/<slug>.json`)
```json
{ "slug": "...", "h1": "...", "title": "...", "description": "...", "excerpt": "...", "date": "2026-11-01",
  "image": "el-paso-police-department-traffic-cop" (one of the existing image basenames), "image_alt": "...",
  "html": "<p>...</p><h2>...</h2>..." (1,000-1,400 words, h2/h3 only, may link to /services pages and other posts),
  "faq": [ {"q":"...","a":"..."} ] (optional, 3-4) }
```

## Voice rules (Robert Navar reviews everything)
- Write as a Texas lawyer explaining to a client: precise, plain, confident, no hype. "Class C misdemeanor", "deferred disposition", "driving safety course", "appearance bond", "capias pro fine" used correctly.
- Never promise or guarantee an outcome, never state a dismissal percentage, never say "best", "top-rated", "#1", never claim relationships with judges or prosecutors. "In many cases", "we will pursue", "may be eligible".
- First person plural ("we", "our office") except quotes. Attorney Robert Navar is the lawyer. Phone 915-200-1133, email help@elpasotrafficticketfirm.com, office 7362 Remcon Cir, El Paso, TX 79912 (West side). Courts: El Paso Municipal Court (city police tickets), El Paso County Justice of the Peace precincts (DPS/sheriff/constable tickets), plus Socorro, Horizon City, Anthony, Vinton, Clint, Canutillo municipal courts.
- Texas facts to get right: paying a ticket = plea of guilty/no contest = conviction; driving safety course dismissal rules (TDLR; not for CDL holders, not 25+ over, not 95+ mph, once per 12 months); deferred disposition (CCP art. 45.051) not available to CDL holders; Driver Responsibility Program surcharges were repealed Sept 1, 2019; failure to appear → warrant, Failure to Appear charge (Transp. Code §543.009 / Penal Code §38.10 for Class C); OmniBase holds on license renewal; no insurance = Transp. Code §601.191, fine $175-$350 first offense, license suspension risk on repeat; CDL: 49 CFR 383.51 masking prohibition, serious traffic violations; school zone: §545.356, fines doubled; red light non-camera §544.007.
- Internal links to use naturally: /fight-your-ticket/, /warrant-lawyer/, /traffic-ticket-and-warrants-lookup-form/, /should-i-hire-a-traffic-ticket-lawyer/, /defensive-driving-in-el-paso-texas/, /faqs/, /contact/.
