#!/usr/bin/env python3
"""Auto Addict Works static site generator.
Usage:  python3 build.py            -> dist/     (production: clean URLs, deploy this folder)
        python3 build.py --preview  -> preview/  (relative links, opens from disk or any host path)
Edit config.json for phone, hours, email, form endpoint; edit content.py for page copy."""
import json, os, shutil, sys, re, html, datetime, posixpath

ROOT = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(ROOT, "config.json")))
PREVIEW = "--preview" in sys.argv
OUT = os.path.join(ROOT, "preview" if PREVIEW else "dist")
TODAY = datetime.date.today().isoformat()

import content  # page definitions

def esc(s): return html.escape(s, quote=True)

class Ctx:
    def __init__(self, path):
        self.path = path  # e.g. "/" or "/services/diagnostics/"
    def L(self, target):
        """Link to a site path like '/build/' or '/css/site.css'."""
        if not PREVIEW:
            return target
        here = self.path if self.path.endswith("/") else posixpath.dirname(self.path) + "/"
        rel = posixpath.relpath(target if not target.endswith("/") else target + "index.html", here)
        return rel
    def abs(self, target):
        return CFG["siteUrl"].rstrip("/") + target

def phone_link(): return f'tel:{CFG["phoneE164"]}'

def hours_text():
    out = []
    for h in CFG["hours"]:
        d = h["days"]; label = d[0][:3] + (" to " + d[-1][:3] if len(d) > 1 else "")
        def t(x):
            hh, mm = map(int, x.split(":")); ap = "am" if hh < 12 else "pm"; hh = hh % 12 or 12
            return f"{hh}{':%02d' % mm if mm else ''}{ap}"
        out.append(f"{label}: {t(h['opens'])} to {t(h['closes'])}")
    return out

def business_schema(ctx):
    a = CFG["address"]
    s = {
        "@context": "https://schema.org", "@type": "AutoRepair", "@id": ctx.abs("/") + "#business",
        "name": CFG["name"], "legalName": CFG["legalName"], "slogan": CFG["tagline"],
        "url": ctx.abs("/"), "logo": ctx.abs("/img/emblem-1000.png"), "image": ctx.abs("/img/og-share-image-1200x630.png"),
        "email": CFG["email"], "priceRange": "$$$",
        "address": {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"],
                    "addressRegion": a["region"], "postalCode": a["postal"], "addressCountry": a["country"]},
        "areaServed": [{"@type": "City", "name": f"{c}, MA"} for c in CFG["areasServed"]],
        "knowsAbout": ["BMW repair", "BMW ISTA diagnostics", "Audi repair", "Volkswagen repair", "Mercedes-Benz repair",
                       "European car maintenance", "Performance tuning", "Pre-purchase inspection"],
        "hasMap": CFG["mapsUrl"],
    }
    if not CFG.get("phoneIsPlaceholder"): s["telephone"] = CFG["phoneE164"]
    if not CFG.get("hoursArePlaceholder"):
        s["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"],
                                           "opens": h["opens"], "closes": h["closes"]} for h in CFG["hours"]]
    same = [v for v in CFG["social"].values() if v]
    if same: s["sameAs"] = same
    return s

def breadcrumb_schema(ctx, crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ctx.abs(p)} for i, (n, p) in enumerate(crumbs)]}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]}

def service_schema(ctx, name, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "serviceType": name, "provider": {"@id": ctx.abs("/") + "#business"},
            "areaServed": {"@type": "City", "name": "Marlborough, MA"}, "url": ctx.abs(ctx.path)}

def book_href(ctx):
    return CFG["bookingUrl"] or ctx.L("/contact/")

def header(ctx):
    L = ctx.L
    cur = lambda p: ' aria-current="page"' if ctx.path == p or (p != "/" and ctx.path.startswith(p)) else ""
    svc = "".join(f'<a href="{L(p)}">{esc(n)}</a>' for n, p in content.SERVICES_NAV)
    mk = "".join(f'<a href="{L(p)}">{esc(n)}</a>' for n, p in content.MAKES_NAV)
    sales = f'<a href="{L("/vehicle-sales/")}"{cur("/vehicle-sales/")}>Vehicle Sales</a>' if CFG.get("showVehicleSales") else ""
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="{L('/')}" aria-label="{esc(CFG['name'])} home"><img src="{L('/img/logo-horizontal.svg')}" alt="{esc(CFG['name'])}, {esc(CFG['tagline'])}" width="252" height="50"></a>
<button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
<nav class="nav" id="nav" aria-label="Main">
<a href="{L('/')}"{' aria-current="page"' if ctx.path == "/" else ""}>Home</a>
<div class="dd"><a href="{L('/services/')}"{cur('/services/')}>Services</a><div class="dd-menu">{svc}<hr>{mk}</div></div>
<a href="{L('/services/performance-tuning/')}">Performance</a>
<a href="{L('/build/')}"{cur('/build/')}>Build Your Car</a>
{sales}
<a href="{L('/about/')}"{cur('/about/')}>About</a>
<a class="btn btn-line" href="{book_href(ctx)}">{content.ICON["cal"]}Book Appointment</a>
</nav></div></header>'''

def footer(ctx):
    L = ctx.L; a = CFG["address"]
    svc = "".join(f'<li><a href="{L(p)}">{esc(n)}</a></li>' for n, p in content.SERVICES_NAV)
    mk = "".join(f'<li><a href="{L(p)}">{esc(n)}</a></li>' for n, p in content.MAKES_NAV)
    hrs = "<br>".join(hours_text())
    return f'''<section class="band" style="background-image:linear-gradient(90deg,rgba(13,19,21,.96) 30%,rgba(13,19,21,.55)),url({L(content.photo('band'))})"><div class="wrap">
<div><h2><span class="slash" aria-hidden="true"></span>Built for enthusiasts</h2><p>Expert care for European cars by people who actually drive them.</p></div>
<div class="btn-row"><a class="btn btn-primary" href="{book_href(ctx)}">{content.ICON["cal"]}Book Your Appointment</a><a class="btn btn-ghost" href="{phone_link()}">Call {esc(CFG['phoneDisplay'])}</a></div></div></section>
<footer class="site-footer"><div class="wrap"><div class="fgrid">
<div><img src="{L('/img/emblem.svg')}" alt="" width="96" height="96" loading="lazy" style="width:96px;margin-bottom:20px">
<address class="nap"><strong>{esc(CFG['name'])}</strong><br>{esc(a['street'])}<br>{esc(a['city'])}, {a['region']} {a['postal']}<br>
<a href="{phone_link()}">{esc(CFG['phoneDisplay'])}</a><br><a href="mailto:{CFG['email']}">{esc(CFG['email'])}</a></address>
<p class="muted small" style="margin-top:12px">{hrs}</p></div>
<div><h3 class="fh">Services</h3><ul>{svc}</ul></div>
<div><h3 class="fh">Makes</h3><ul>{mk}</ul></div>
<div><h3 class="fh">Shop</h3><ul><li><a href="{L('/build/')}">Build Your Car</a></li><li><a href="{L('/about/')}">About</a></li>
<li><a href="{L('/areas-we-serve/')}">Areas We Serve</a></li><li><a href="{L('/contact/')}">Contact &amp; Directions</a></li>
<li><a href="{CFG['mapsUrl']}" rel="noopener" target="_blank">Google Maps</a></li></ul></div>
</div><div class="fbase"><span>© {datetime.date.today().year} {esc(CFG['legalName'])}. Independent service specialist, not affiliated with BMW AG, Audi AG, Volkswagen AG or Mercedes-Benz Group.</span>
<span>{esc(a['city'])}, Massachusetts</span></div></div></footer>'''

def page_html(ctx, p):
    L = ctx.L
    title = p["title"]; desc = p["desc"]
    canonical = ctx.abs(ctx.path)
    schemas = [business_schema(ctx)] if ctx.path == "/" else [{"@context": "https://schema.org", "@type": "AutoRepair",
               "@id": ctx.abs("/") + "#business", "name": CFG["name"], "url": ctx.abs("/")}]
    if p.get("crumbs"): schemas.append(breadcrumb_schema(ctx, p["crumbs"]))
    if p.get("faqs"): schemas.append(faq_schema(p["faqs"]))
    if p.get("service"): schemas.append(service_schema(ctx, p["service"], desc))
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    body = p["body"](ctx)
    if PREVIEW:
        body = re.sub(r'href="(/[^"]*)"', lambda m: f'href="{ctx.L(m.group(1))}"', body)
    scripts = f'<script src="{L("/js/site.js")}" defer></script>'
    if p.get("builder"):
        scripts += f'<script src="{L("/js/builder-data.js")}" defer></script><script src="{L("/js/builder.js")}" defer></script>'
    cfg_js = json.dumps({k: CFG.get(k) for k in ("formEndpoint", "email", "phoneDisplay", "phoneE164", "laborRate", "bookingUrl", "builderShowPricing")})
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#1B2528">
<meta property="og:type" content="website"><meta property="og:site_name" content="{esc(CFG['name'])}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{ctx.abs('/img/og-share-image-1200x630.png')}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="US-MA"><meta name="geo.placename" content="Marlborough">
<link rel="icon" href="{L('/img/favicon.ico')}" sizes="any"><link rel="icon" href="{L('/img/favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{L('/img/apple-touch-icon.png')}"><link rel="manifest" href="{L('/site.webmanifest')}">
<link rel="preload" href="{L('/fonts/Montserrat-700-italic.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{L('/fonts/Inter-400.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{L('/fonts/Montserrat-700-italic.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{L('/css/site.css')}">
{('<link rel="preload" as="image" fetchpriority="high" href="' + L(content.photo('hero')) + '">') if ctx.path == "/" else ""}
{ld}
<script>window.AAW={cfg_js};</script>
</head>
<body>
{header(ctx)}
<main id="main">
{body}
</main>
{footer(ctx)}
{scripts}
</body>
</html>
'''

def build():
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "static"), OUT)
    urls = []
    for path, p in content.PAGES.items():
        ctx = Ctx(path)
        dest = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.strip("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w").write(page_html(ctx, p))
        if not p.get("noindex"):
            urls.append((path, p.get("priority", "0.7")))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pr in urls:
        sm.append(f"  <url><loc>{CFG['siteUrl'].rstrip('/')}{path}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {CFG['siteUrl'].rstrip('/')}/sitemap.xml\n")
    json.dump({"name": CFG["name"], "short_name": "AA Works", "start_url": "/", "display": "standalone",
               "background_color": "#1B2528", "theme_color": "#1B2528",
               "icons": [{"src": "/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                         {"src": "/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
              open(os.path.join(OUT, "site.webmanifest"), "w"))
    # Netlify / Cloudflare Pages headers: long cache for fonts/images
    open(os.path.join(OUT, "_headers"), "w").write("/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n/img/*\n  Cache-Control: public, max-age=2592000\n/css/*\n  Cache-Control: public, max-age=86400\n/js/*\n  Cache-Control: public, max-age=86400\n")
    todo = [k for k in ("phoneIsPlaceholder", "hoursArePlaceholder") if CFG.get(k)]
    print(f"Built {len(content.PAGES)} pages -> {OUT}")
    if todo: print("TODO before launch:", ", ".join(todo), "(see config.json)")

if __name__ == "__main__":
    build()
