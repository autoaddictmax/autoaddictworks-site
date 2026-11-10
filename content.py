"""Page copy for autoaddictworks.com. Each page: title (≤60 chars ideal), desc (≤155), crumbs, body(ctx)."""
import json, html
CFG = json.load(open(__file__.rsplit("/", 1)[0] + "/config.json"))
A = CFG["address"]
CITY = "Marlborough, MA"

SERVICES_NAV = [
    ("Diagnostics & Programming", "/services/diagnostics/"),
    ("Maintenance & Inspections", "/services/maintenance/"),
    ("Engine & Drivetrain Repair", "/services/engine-repair/"),
    ("Brakes, Suspension & Steering", "/services/brakes-suspension/"),
    ("Performance & Tuning", "/services/performance-tuning/"),
    ("Pre-Purchase Inspection", "/services/pre-purchase-inspection/"),
]
MAKES_NAV = [
    ("BMW", "/bmw-repair/"), ("Audi", "/audi-repair/"),
    ("Volkswagen", "/volkswagen-repair/"), ("Mercedes-Benz", "/mercedes-benz-repair/"),
    ("MINI", "/mini-repair/"), ("Porsche", "/porsche-repair/"),
]

def e(s): return html.escape(s)

import os
_ROOT = os.path.dirname(os.path.abspath(__file__))
def photo(slot):
    """Real photo if you drop one in static/img/photos/<slot>.jpg|.webp, else the generated atmosphere art."""
    for ext in ("webp", "jpg", "jpeg", "png"):
        if os.path.exists(os.path.join(_ROOT, "static/img/photos", f"{slot}.{ext}")):
            return f"/img/photos/{slot}.{ext}"
    fallback = {"hero": "hero", "band": "band", "approach": "approach", "diagnostics": "tile-1", "maintenance": "tile-2",
                "repairs": "tile-3", "performance": "tile-4", "sales": "tile-2", "page": "hero"}
    return f"/img/art/{fallback.get(slot, 'tile-1')}.jpg"
def has_photo(slot): return not photo(slot).startswith("/img/art/")

_I = lambda d: f'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
ICON = {
 "diag": _I('<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M1 19.5h22"/><path d="M6 10.5h3l1.5-3 3 6 1.5-3H18"/>'),
 "wrench": _I('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>'),
 "gear": _I('<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9 7 7M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>'),
 "turbo": _I('<circle cx="10" cy="13" r="7"/><circle cx="10" cy="13" r="1.8"/><path d="M10 6c2.2 2 2.2 5 0 7M17 13c-2 2.2-5 2.2-7 0M10 20c-2.2-2-2.2-5 0-7M3 13c2-2.2 5-2.2 7 0"/><path d="M14.5 7V3.5H21V8"/>'),
 "car": _I('<path d="M3 15.5 4.6 11a2 2 0 0 1 1.9-1.4h11a2 2 0 0 1 1.9 1.4l1.6 4.5v2.7h-2.3M5.3 18.2H3v-2.7"/><circle cx="7.5" cy="18" r="1.8"/><circle cx="16.5" cy="18" r="1.8"/><path d="M9.5 18.2h5M3.2 15.5h17.6M7 9.6l1.2-3h7.6l1.2 3"/>'),
 "shield": _I('<path d="M12 3l8 3v6c0 4.5-3.5 8-8 9-4.5-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'),
 "disc": _I('<circle cx="11" cy="12" r="8"/><circle cx="11" cy="12" r="2.5"/><path d="M11 6.5v1M16.5 12h-1M11 17.5v-1M5.5 12h1"/><path d="M17 5.5a9 9 0 0 1 3.5 6.5"/>'),
 "cal": _I('<rect x="3" y="5" width="18" height="16" rx="1"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
 "arrow": _I('<path d="M5 12h14M13 6l6 6-6 6"/>'),
 "check": _I('<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.6 2.6L16 9.5"/>'),
}
SVC_ICON = {"/services/diagnostics/": "diag", "/services/maintenance/": "wrench", "/services/engine-repair/": "gear",
            "/services/brakes-suspension/": "disc", "/services/performance-tuning/": "turbo", "/services/pre-purchase-inspection/": "shield"}


# ------------------------------------------------------------------ helpers
def page_hero(ctx, eyebrow, h1, lede, crumbs, ctas=True):
    cr = ""
    if crumbs:
        parts = []
        for i, (n, p) in enumerate(crumbs):
            parts.append(f'<a href="{ctx.L(p)}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page" style="margin:0;opacity:1">{e(n)}</span>')
        cr = '<nav class="crumbs" aria-label="Breadcrumb">' + '<span>/</span>'.join(parts) + '</nav>'
    btns = (f'<div class="btn-row"><a class="btn btn-primary" href="{CFG["bookingUrl"] or ctx.L("/contact/")}">{ICON["cal"]}Book Appointment</a>'
            f'<a class="btn btn-ghost" href="tel:{CFG["phoneE164"]}">Call {e(CFG["phoneDisplay"])}</a></div>') if ctas else ""
    return f'''<section class="page-hero" style="--bg:url({ctx.L(photo('page'))})"><div class="wrap">{cr}<span class="eyebrow line">{e(eyebrow)}</span>
<h1>{h1}</h1><p class="lede">{lede}</p>{btns}</div></section>'''

def faq_block(faqs, title="Common questions"):
    items = "".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in faqs)
    return f'<section class="section"><div class="wrap"><div class="head"><span class="eyebrow">FAQ</span><h2>{title}</h2></div><div class="faq">{items}</div></div></section>'

def cards(ctx, items, cols=3, deep=False):
    out = []
    for i, it in enumerate(items):
        title, text = it[0], it[1]
        href = it[2] if len(it) > 2 else None
        num = f'<div class="num">{i+1:02d}</div>'
        if href:
            out.append(f'<a class="card" href="{ctx.L(href)}">{num}<h3>{e(title)}</h3><p>{text}</p><span class="more">Learn more →</span></a>')
        else:
            out.append(f'<div class="card">{num}<h3>{e(title)}</h3><p>{text}</p></div>')
    return f'<div class="grid g{cols}">{"".join(out)}</div>'

def ticks(items): return '<ul class="ticks">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def side_panel(ctx, heading="Visit the shop"):
    return f'''<aside class="panel"><h3>{heading}</h3>
<address class="nap"><strong>{e(CFG["name"])}</strong><br>{e(A["street"])}<br>{e(A["city"])}, {A["region"]} {A["postal"]}<br>
<a href="tel:{CFG["phoneE164"]}">{e(CFG["phoneDisplay"])}</a></address>
<p class="muted small" style="margin:16px 0 24px">Drop-off by appointment. Written estimate before any work begins.</p>
<div class="btn-row"><a class="btn btn-primary" href="{CFG["bookingUrl"] or ctx.L("/contact/")}">Book Service</a>
<a class="btn btn-ghost" href="{CFG["mapsUrl"]}" target="_blank" rel="noopener">Directions</a></div></aside>'''

def marques(ctx):
    return '<nav class="marques" aria-label="Makes we service">' + "".join(
        f'<a href="{ctx.L(p)}">{e(n)}</a>' for n, p in MAKES_NAV) + f'<a href="{ctx.L("/build/")}">Build Yours</a></nav>'

TOWNS = ", ".join(CFG["areasServed"][:-1]) + " and " + CFG["areasServed"][-1]

# ------------------------------------------------------------------ home
HOME_FAQS = [
    ("Do I have to go to the dealer to keep my BMW, Audi, VW or Mercedes warranty?",
     "No. Federal law (the Magnuson-Moss Warranty Act) lets you have maintenance done at any qualified shop without voiding your factory warranty, as long as the work follows the manufacturer's schedule with correct-spec parts and fluids. We document every service on your repair order so you have the record."),
    ("What diagnostic equipment do you use?",
     "For BMW and MINI we run ISTA, the same factory software BMW dealers use for fault-finding, test plans, coding and programming. For other European makes we use professional multi-brand diagnostic tools, and we follow the manufacturer's test procedures rather than guessing from a code."),
    ("Do you use OEM parts?",
     "Yes. We source genuine and OE-supplier parts (the companies that build the factory parts, like Bosch, Lemförder, Mahle and ZF) through European parts distributors and BMW dealer wholesale. If an aftermarket upgrade is the better choice for your goals, we'll explain why and price both."),
    ("How do your prices compare to the dealer?",
     "Our estimates are built from published labor times and real parts pricing, and you approve a written estimate before work starts. Most owners save meaningfully versus dealer service, without giving up factory-level diagnostics or parts quality."),
    ("Can you help me modify or tune my car?",
     "Yes. Performance is where our team lives. Start with the <a href=\"/build/\">Build Your Car</a> tool to see what your power goal takes and a ballpark price, then we'll confirm the plan after inspecting the car."),
]

BRANDS = ["FCP Euro", "Precision Raceworks", "RK Autowerks", "Precision Turbo", "Turbosmart", "bootmod3", "MHD Tuning",
          "xHP", "Dorch Engineering", "Spool Performance", "Pure Turbos", "CSF", "Wagner Tuning", "Eventuri", "Mishimoto", "KW Suspension", "Motul"]
def brands_marquee():
    items = "".join(f"<li>{e(b)}</li>" for b in BRANDS)
    return f'''<section class="brands" aria-label="Brands we build with"><span class="eyebrow line">Brands we build with</span>
<div class="marquee"><div class="marquee-track"><ul>{items}</ul><ul aria-hidden="true">{items}</ul></div></div></section>'''

def home(ctx):
    L = ctx.L
    book = CFG["bookingUrl"] or L("/contact/")
    strip_items = [("Factory-Level Diagnostics", "diag", "/services/diagnostics/"),
                   ("Service & Maintenance", "wrench", "/services/maintenance/"),
                   ("Repairs & Troubleshooting", "gear", "/services/engine-repair/"),
                   ("Performance Builds", "turbo", "/services/performance-tuning/"),
                   (("Vehicle Sales & Sourcing", "car", "/vehicle-sales/") if CFG.get("showVehicleSales") else ("Pre-Purchase Inspection", "shield", "/services/pre-purchase-inspection/"))]
    strip = "".join(f'<a class="istrip-i" href="{L(p)}">{ICON[i]}<span>{e(n)}</span></a>' for n, i, p in strip_items)
    tiles = [("Service & Maintenance", "maintenance", "/services/maintenance/", "wrench"),
             ("Repairs", "repairs", "/services/engine-repair/", "gear"),
             ("Performance Builds", "performance", "/services/performance-tuning/", "turbo"),
             (("Vehicle Sales", "sales", "/vehicle-sales/", "car") if CFG.get("showVehicleSales") else ("Diagnostics", "diagnostics", "/services/diagnostics/", "diag"))]
    tile_html = "".join(f'''<a class="ptile{'' if has_photo(slot) else ' art'}" href="{L(p)}"><div class="ptile-in" style="--img:url({L(photo(slot))})">
<span class="ptile-ico">{ICON[ic]}</span><span class="ptile-t">{e(n)}</span><span class="ptile-a">{ICON["arrow"]}</span></div></a>''' for n, slot, p, ic in tiles)
    hero_bg = L(photo("hero"))
    return f'''<section class="hero2" style="--hero:url({hero_bg})"><div class="wrap hero2-grid">
<div class="hero2-copy">
<h1><span class="h1-loc">Marlborough, MA</span> <span class="h1-a">European</span> <span class="h1-b">Auto Specialists</span></h1>
<p class="hero2-sub">Diagnostics. Maintenance. Repairs.<br>Performance Builds.</p>
<div class="btn-row"><a class="btn btn-primary" href="{book}">{ICON["cal"]}Book an Appointment</a><a class="btn btn-ghost" href="{L("/services/")}">Our Services {ICON["arrow"]}</a></div>
<nav class="hero2-makes" aria-label="Makes we service"><span class="slash" aria-hidden="true"></span>{" <i>/</i> ".join(f'<a href="{L(p)}">{e("VW" if n=="Volkswagen" else "Mercedes" if n=="Mercedes-Benz" else n)}</a>' for n, p in MAKES_NAV)}</nav>
</div>
<div class="hero2-art" aria-hidden="true">
<img class="medal" src="{L("/img/emblem-gold.svg")}" alt="" width="520" height="520">
<div class="gauge"><svg viewBox="0 0 120 70"><path class="g-bg" d="M10 62a50 50 0 0 1 100 0"/><path class="g-fg" d="M10 62a50 50 0 0 1 100 0"/></svg>
<div><small>Shop car · B58 340i</small><b>1,300<em>HP</em></b></div></div>
<div class="chip-ista">{ICON["diag"]}<span>BMW ISTA<br><small>Factory diagnostics</small></span></div>
</div></div></section>

<section class="istrip"><div class="wrap istrip-row">{strip}</div></section>

{brands_marquee()}

<section class="approach"><div class="approach-img{'' if has_photo('approach') else ' art'}" style="--img:url({L(photo("approach"))})">
<div class="ista-mock" aria-hidden="true"><b>ISTA</b><ul><li>Vehicle identification</li><li>Diagnostics</li><li>Service functions</li><li>Programming / encoding</li></ul></div></div>
<div class="approach-copy"><span class="eyebrow line">Our approach</span>
<h2>Dealer-level capabilities.<br><span class="gold">An independent experience.</span></h2>
<p class="lede">We combine factory-grade tools, real technical depth and a genuine obsession with European cars to keep yours performing at its best, on the road and at the track.</p>
<ul class="badges"><li>{ICON["check"]}Factory ISTA diagnostics</li><li>{ICON["check"]}Genuine &amp; OE parts</li><li>{ICON["check"]}Enthusiast-run</li></ul>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><span class="eyebrow line">Our services</span><a class="link-more" href="{L("/services/")}">All services {ICON["arrow"]}</a></div>
<div class="ptiles">{tile_html}</div>
</div></section>

<section class="section deep feature"><div class="wrap split">
<div><span class="eyebrow line">Build your car</span><h2>Tell us the goal.<br><span class="gold">We'll map the build.</span></h2>
<p class="lede">Pick your car, set the power you want and how you'll use it. The build planner lists the parts and supporting mods it takes, with a ballpark price, whether it's a street, track or full competition build.</p>
<div class="btn-row"><a class="btn btn-primary" href="{L("/build/")}">Start a Build {ICON["arrow"]}</a></div></div>
<a class="build-preview" href="{L("/build/")}" aria-label="Open the build planner">
<div class="bp-h"><small>B58 Gen 1 · ZF 8-speed</small><b>Stage 2+ E85</b><span>~540 hp · Spirited street</span></div>
<div class="bp-bar"><i style="width:42%"></i></div>
<ul><li>ECU flash tune</li><li>Catted downpipe &amp; intake</li><li>Intercooler upgrade</li><li>Flex-fuel kit + fuel pump</li><li>Transmission tune</li></ul>
<div class="bp-f"><span>Ballpark</span><b>Your build, priced</b></div></a>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><span class="eyebrow line">How it works</span></div>
<div class="steps4">
<div><b>01</b><h3>Diagnose</h3><p>We verify the complaint, scan every module and follow the factory test plan to find the actual cause.</p></div>
<div><b>02</b><h3>Estimate</h3><p>Findings, photos and a written estimate. Nothing is done without your approval.</p></div>
<div><b>03</b><h3>Repair to spec</h3><p>Correct parts, torque specs, fluids and coding, plus any software the repair needs.</p></div>
<div><b>04</b><h3>Road test</h3><p>We verify the fix and walk you through exactly what we found.</p></div>
</div></div></section>

<section class="section tight"><div class="wrap">{marques(ctx)}</div></section>

{faq_block(HOME_FAQS)}

<section class="section tight"><div class="wrap"><p class="muted small" style="max-width:900px">
Auto Addict Works is an independent European auto repair shop at {e(A["street"])}, {e(A["city"])}, MA, serving drivers from {e(TOWNS)}. <a href="{L("/areas-we-serve/")}">See all areas we serve</a>.</p></div></section>
'''

# ------------------------------------------------------------------ makes
MAKES = {
 "bmw": dict(path="/bmw-repair/", name="BMW",
  title="BMW Repair & Service in Marlborough, MA | Auto Addict Works",
  desc="BMW specialist in Marlborough, MA. Factory ISTA diagnostics, coding and programming, genuine parts, maintenance, repair and performance for every BMW.",
  h1="BMW Repair &amp; Service in Marlborough, MA",
  lede="BMW is what we do first and know best. Factory ISTA diagnostics, coding and programming, genuine and OE parts, and a team that builds BMWs for fun.",
  intro="From an F30 328i commuter to a G80 M3, we service and repair the full BMW lineup (2, 3, 4, 5, 7 and 8 Series, X models, Z4, i-models and M cars) plus MINI. Because we run ISTA, BMW's own diagnostic and programming software, we can follow the same guided test plans, register batteries, code retrofits and update module software the way the dealer does.",
  issues=[
   "<strong>Oil leaks:</strong> oil filter housing gasket, valve cover gasket and oil pan gasket on N20, N52, N54, N55 and B58 engines.",
   "<strong>Cooling system:</strong> electric water pumps, thermostats, expansion tanks and plastic coolant pipes.",
   "<strong>Charge pipe and boost leaks:</strong> the factory plastic charge pipe on N55 and B58 engines is a known failure point.",
   "<strong>VANOS and timing:</strong> VANOS solenoids, N20/N26 timing chain guides, and N63 timing and valve-stem-seal work.",
   "<strong>Carbon buildup:</strong> direct-injection intake valve cleaning (walnut blasting) for rough idle and misfires.",
   "<strong>Electrical:</strong> battery registration, coding after retrofits, iDrive and module faults, parasitic drain.",
   "<strong>Driveline:</strong> ZF 8-speed fluid service, transfer case (xDrive) service and actuator faults, differential service.",
   "<strong>Suspension:</strong> thrust-arm and control-arm bushings, air springs on X5/X7 and 7 Series.",
  ],
  services=["Oil service and Condition Based Service (CBS) resets","Brake fluid, coolant, spark plugs and ZF transmission service","ISTA diagnostics, coding, programming and software updates","Battery registration and retrofits","Engine, cooling and oil-leak repair","Performance: bootmod3 / MHD tunes, downpipes, intercoolers, port injection, turbo upgrades"],
  faqs=[("Do you work on BMW M cars?", "Yes. We service and modify M cars including the S55 (F80 M3, F82 M4, F87 M2 Competition) and S58 (G80 M3, G82 M4, G87 M2), from routine service to complete performance builds."),
        ("Can you code and program my BMW?", "Yes. We use ISTA for programming and module software updates, and can code retrofits and features after repairs or upgrades. If a repair needs a module programmed, we handle it in-house."),
        ("How often should my BMW's oil be changed?", "BMW's Condition Based Service intervals can stretch past 10,000 miles. For turbocharged engines driven in New England weather (short trips, cold starts, or any tuning), we recommend every 5,000 to 7,500 miles."),
        ("Do you service MINI?", "Yes. MINI shares BMW engines and electronics, and ISTA covers MINI as well.")]),
 "audi": dict(path="/audi-repair/", name="Audi",
  title="Audi Repair & Service in Marlborough, MA | Auto Addict Works",
  desc="Audi specialist in Marlborough, MA. Diagnostics, maintenance, S tronic and quattro service, engine repair and tuning for A3–A8, Q-models, S and RS.",
  h1="Audi Repair &amp; Service in Marlborough, MA",
  lede="Maintenance, diagnostics and repair for Audi A, S, RS and Q models, plus performance work for the 2.0T, 2.5 TFSI and 2.9/3.0T platforms.",
  intro="We work on the Audi models New England actually drives: A3/S3, A4/S4, A5/S5, A6, Q5/SQ5, Q7 and the RS cars. Every repair starts with a full module scan and the manufacturer's test procedure, and we use genuine or OE-supplier parts so your Audi drives the way it should.",
  issues=[
   "<strong>Cooling system:</strong> water pump and thermostat housing leaks on EA888 2.0T engines.",
   "<strong>PCV and oil leaks:</strong> PCV valve failures, valve cover and timing cover leaks.",
   "<strong>Timing chain:</strong> tensioner and guide wear on earlier EA888 2.0T engines.",
   "<strong>Carbon buildup:</strong> intake valve cleaning on direct-injection engines.",
   "<strong>S tronic and quattro:</strong> DSG/S tronic fluid service, Haldex service on transverse quattro models, rear differential service.",
   "<strong>Suspension:</strong> control-arm bushings, air suspension on Q7 and A8, alignment.",
  ],
  services=["Scheduled maintenance and inspections","S tronic / DSG and Haldex service","Diagnostics and electrical fault-finding","Engine, cooling and oil-leak repair","Brakes, suspension and alignment","Performance: tunes, intakes, intercoolers and turbo upgrades for 2.0T, 2.5 TFSI, 2.9T and 3.0T"],
  faqs=[("How often does an S tronic need fluid service?", "Most Audi dual-clutch (S tronic/DSG) transmissions call for a fluid and filter service around every 40,000 miles. Skipping it is a common cause of harsh shifts and mechatronic problems."),
        ("Do you work on Audi RS models?", "Yes, including the RS3 and TT RS 2.5 TFSI five-cylinder and the RS5 2.9 TFSI, from maintenance through full performance builds."),
        ("Is my Audi still under warranty if I service it with you?", "Yes. Your factory warranty stays intact when maintenance is done to Audi's schedule with correct-spec parts and fluids, and we document every service.")]),
 "volkswagen": dict(path="/volkswagen-repair/", name="Volkswagen",
  title="VW Repair & Service in Marlborough, MA | Auto Addict Works",
  desc="Volkswagen specialist in Marlborough, MA. GTI, Golf R, Jetta, Tiguan and Atlas service, DSG service, diagnostics, repair and performance tuning.",
  h1="Volkswagen Repair &amp; Service in Marlborough, MA",
  lede="GTI, Golf R, Jetta, GLI, Tiguan, Atlas and more. Maintained, repaired and tuned by European specialists.",
  intro="Volkswagens share much of their engineering with Audi, and we treat them with the same care: full module scans, manufacturer test procedures and correct parts. We're especially at home with the EA888 2.0T in the GTI, GLI and Golf R, stock or modified.",
  issues=[
   "<strong>Water pump / thermostat housing</strong> leaks on EA888 2.0T engines.",
   "<strong>PCV valve</strong> failures causing rough idle, whistling and oil consumption.",
   "<strong>DSG service:</strong> dual-clutch fluid and filter service to keep shifts crisp.",
   "<strong>Haldex service</strong> on 4MOTION models like the Golf R, Tiguan and Atlas.",
   "<strong>Ignition:</strong> coil packs and spark plugs, especially on tuned cars.",
   "<strong>Carbon buildup</strong> on direct-injection engines.",
  ],
  services=["Scheduled maintenance","DSG and Haldex service","Diagnostics and electrical repair","Cooling, oil-leak and engine repair","Brakes, suspension and alignment","Performance: Stage 1–2 tunes, intakes, intercoolers, downpipes and IS38/hybrid turbo upgrades"],
  faqs=[("What does a Stage 1 tune do on a GTI or Golf R?", "On the EA888 2.0T, a Stage 1 software tune typically adds 50–80 horsepower with no hardware changes. Use the <a href=\"/build/\">Build Your Car</a> tool to see what higher goals require."),
        ("How often should a DSG be serviced?", "Volkswagen typically specifies a DSG fluid and filter service around every 40,000 miles. More often is smart on tuned or hard-driven cars."),
        ("Do you work on the VW Atlas and Tiguan?", "Yes. Maintenance, Haldex service, diagnostics and repair on VW's SUVs as well as the GTI and Golf R.")]),
 "mercedes-benz": dict(path="/mercedes-benz-repair/", name="Mercedes-Benz",
  title="Mercedes-Benz Repair in Marlborough, MA | Auto Addict Works",
  desc="Mercedes-Benz repair and service in Marlborough, MA. Service A and B, diagnostics, 7G/9G-Tronic service, Airmatic suspension, AMG maintenance.",
  h1="Mercedes-Benz Repair &amp; Service in Marlborough, MA",
  lede="Service A and Service B, diagnostics, suspension and engine repair for C, E, S and GLC/GLE-Class, including AMG models.",
  intro="We service Mercedes-Benz cars and SUVs to the factory schedule with correct-spec oils and genuine or OE-supplier parts. From a Service B on a GLC 300 to an AMG 43 or 63 that needs more power, every job starts with a proper diagnosis.",
  issues=[
   "<strong>Service A / Service B</strong> on the factory schedule, including brake fluid and cabin filters.",
   "<strong>Transmission service:</strong> 7G-Tronic and 9G-Tronic fluid and filter service.",
   "<strong>Airmatic suspension:</strong> air struts, compressors and valve blocks.",
   "<strong>Oil leaks:</strong> oil cooler, valve cover and front-cover leaks.",
   "<strong>Electrical:</strong> battery and charging faults, module diagnostics.",
   "<strong>AMG:</strong> maintenance and performance for M276 (43), M177/M178 (63) and M139 (45) engines.",
  ],
  services=["Service A and Service B","Diagnostics and electrical repair","7G / 9G-Tronic transmission service","Airmatic and suspension repair","Engine and oil-leak repair","AMG performance: tunes, intakes, downpipes and turbo upgrades"],
  faqs=[("What's the difference between Service A and Service B?", "Service A is the lighter interval (oil, filter and inspections). Service B adds items like the cabin filter and brake fluid. Your car's display tells you which is due; we perform either to the factory checklist."),
        ("Can you work on AMG models?", "Yes. Maintenance, repair and performance work on AMG 43, 45, 53 and 63 models."),
        ("Do you repair Airmatic suspension?", "Yes. We diagnose whether it's a strut, the compressor, a valve block or a leak before replacing anything.")]),

 "mini": dict(path="/mini-repair/", name="MINI",
  title="MINI Cooper Repair & Service in Marlborough, MA | Auto Addict Works",
  desc="MINI specialist in Marlborough, MA. Cooper, Cooper S, JCW and Countryman diagnostics, maintenance and repair with BMW ISTA and genuine parts.",
  h1="MINI Repair &amp; Service in Marlborough, MA",
  lede="MINIs are BMWs underneath, and we treat them that way: ISTA diagnostics, genuine and OE parts, and technicians who know their engines.",
  intro="We service Cooper, Cooper S, John Cooper Works, Clubman and Countryman models, from the older N14 and N18 Cooper S to the current B38 and B48 cars. ISTA covers MINI the same way it covers BMW, so we can run guided diagnostics, register batteries, code modules and update software in-house.",
  issues=[
   "<strong>Timing chain:</strong> chain stretch and tensioner wear on N14 and N18 Cooper S engines.",
   "<strong>Oil leaks:</strong> oil filter housing, valve cover and oil pan gaskets.",
   "<strong>Cooling system:</strong> water pumps, thermostat housings and coolant hoses.",
   "<strong>Carbon buildup:</strong> intake valve cleaning on direct-injection engines.",
   "<strong>Ignition:</strong> coils and spark plugs, especially on turbocharged models.",
   "<strong>Suspension:</strong> control-arm bushings, struts and mounts.",
  ],
  services=["Oil service and Condition Based Service resets","ISTA diagnostics, coding and programming","Timing chain, cooling and oil-leak repair","Clutch and transmission service","Brakes, suspension and alignment","JCW and Cooper S tuning: tunes, intakes and downpipes"],
  faqs=[("Do you use dealer-level diagnostics on MINI?", "Yes. ISTA, BMW's factory software, covers MINI, so we diagnose, code and program MINIs the same way the dealer does."),
        ("Is the timing chain on my Cooper S a problem?", "The N14 and N18 engines in 2007 to 2016 Cooper S models are known for timing chain wear. A rattle on cold start is the usual warning sign. We can inspect it and tell you where yours stands."),
        ("Do you tune MINIs?", "Yes, including JCW and Cooper S models. Tell us your goal and we'll plan it properly.")]),
 "porsche": dict(path="/porsche-repair/", name="Porsche",
  title="Porsche Repair & Service in Marlborough, MA | Auto Addict Works",
  desc="Porsche service and repair in Marlborough, MA. 911, Cayman, Boxster, Macan, Cayenne and Panamera maintenance, diagnostics and repair.",
  h1="Porsche Repair &amp; Service in Marlborough, MA",
  lede="Maintenance, diagnostics and repair for the 911, Cayman, Boxster, Macan, Cayenne and Panamera, done by European specialists.",
  intro="Porsche owners expect precision, and so do we. Every job starts with a proper diagnosis, and we use genuine or OE-supplier parts and the correct fluids for your model.",
  issues=[
   "<strong>Scheduled maintenance:</strong> oil service, spark plugs, brake fluid and filters on the factory schedule.",
   "<strong>PDK service:</strong> transmission fluid and filter service.",
   "<strong>Cooling system:</strong> coolant pipes, water pumps and thermostats, including the known coolant pipe issue on early V8 Cayennes.",
   "<strong>Oil leaks:</strong> valve cover, rear main seal and air-oil separator problems.",
   "<strong>Engine health:</strong> inspections for IMS bearing and bore scoring concerns on 996, 997.1 and 986/987 models.",
   "<strong>Suspension and brakes:</strong> control arms, air suspension on Cayenne and Panamera, pads and rotors.",
  ],
  services=["Scheduled maintenance","PDK and transmission service","Diagnostics and electrical repair","Cooling and oil-leak repair","Brakes, suspension and alignment","Pre-purchase inspections"],
  faqs=[("Do you work on air-cooled 911s?", "Call us about your specific car. We focus on water-cooled models from the 996 on, plus the Macan, Cayenne and Panamera."),
        ("Can you inspect for IMS bearing or bore scoring issues?", "Yes. If you own or are buying a 996, 997.1, Boxster or Cayman with the M96 or M97 engine, we can inspect it and explain the risk and your options."),
        ("Do you do pre-purchase inspections on Porsches?", "Yes. A used Porsche should always be inspected by someone who knows the model's weak points before you buy.")]),
}

def make_page(key):
    m = MAKES[key]
    def body(ctx):
        return page_hero(ctx, f"{m['name']} specialists · {CITY}", m["h1"], m["lede"],
                         [("Home", "/"), (f"{m['name']} Repair", m["path"])]) + f'''
<section class="section"><div class="wrap split"><div class="prose">
<h2>{m["name"]} service done properly</h2><p>{m["intro"]}</p>
<h2>Common {m["name"]} problems we fix</h2>{ticks(m["issues"])}
<h2>{m["name"]} services</h2><ul>{"".join(f"<li>{s}</li>" for s in m["services"])}</ul>
<p>Want more from your {m["name"]}? <a href="{ctx.L("/build/")}">Build your car</a> and see what your power goal takes.</p>
</div>{side_panel(ctx, f"Book your {m['name']}")}</div></section>
{faq_block(m["faqs"], f"{m['name']} questions")}'''
    return dict(title=m["title"], desc=m["desc"], crumbs=[("Home", "/"), (f"{m['name']} Repair", m["path"])],
                faqs=m["faqs"], service=f"{m['name']} repair and service", body=body, priority="0.9")

# ------------------------------------------------------------------ services
SERVICES = {
 "/services/diagnostics/": dict(name="Diagnostics & Programming",
  title="European Car Diagnostics & Coding | Marlborough, MA",
  desc="Check engine light, electrical faults and module programming for BMW, Audi, VW and Mercedes in Marlborough, MA. Factory BMW ISTA diagnostics.",
  h1="European Car Diagnostics &amp; Programming",
  lede="A code tells you where to start, not what to replace. We find the actual cause, using factory BMW ISTA and professional tools for every European make.",
  body=[
   ("How we diagnose", "<p>Every diagnostic starts with verifying the complaint and a full scan of every control module, not just the engine. From there we follow the manufacturer's guided test plan: live data, component tests, wiring checks and, where needed, smoke testing for vacuum and boost leaks. You get a clear finding and a written estimate before any repair.</p>"),
   ("BMW ISTA: dealer-level software", "<p>For BMW and MINI we use ISTA, the factory diagnostic and programming platform. That means guided fault-finding, battery registration, coding after repairs and retrofits, and module software updates, without a trip to the dealer.</p>"),
   ("What we diagnose", ticks(["Check-engine and drivetrain warning lights","Misfires, rough idle and loss of power","Boost leaks and turbo faults","Electrical faults, parasitic battery drain and module communication errors","ABS, stability-control and airbag warnings","Transmission shift faults and limp mode"])),
  ],
  faqs=[("How much does a diagnostic cost?", "Diagnostic time depends on the fault. We'll tell you the starting diagnostic charge up front, and if more time is needed we call before going further."),
        ("Can you clear my check engine light?", "We can, but we'd rather fix why it's on. Clearing a code without a repair usually just brings it back, and readiness monitors must reset before a Massachusetts inspection."),
        ("Can you program a new module or key?", "For BMW and MINI, module programming and coding are done in-house with ISTA. For other makes, ask us about your specific job.")]),
 "/services/maintenance/": dict(name="Maintenance & Inspections",
  title="BMW, Audi, VW & Mercedes Maintenance | Marlborough, MA",
  desc="Factory-schedule maintenance for European cars in Marlborough, MA: oil, brake fluid, spark plugs, transmission and differential fluid. Warranty-safe.",
  h1="European Car Maintenance in Marlborough, MA",
  lede="Factory-schedule maintenance with correct-spec oils, fluids and parts. Every service is documented, so your warranty and resale value are protected.",
  body=[
   ("Maintenance that matches the manufacturer", "<p>European cars are specific about oil approvals, coolant types and transmission fluids. We use fluids that meet the manufacturer's specification (BMW LL-01/LL-17, VW 502/504/508, MB 229.5/229.71 and so on) and record every service on your repair order.</p>"),
   ("Services", ticks(["Oil and filter service, with Condition Based Service resets","Brake fluid flush","Spark plugs and ignition coils","Engine and cabin air filters","Coolant service","Automatic, DSG/S tronic and manual transmission fluid","Differential, transfer case and Haldex service","Multi-point inspection with photos"])),
   ("Why intervals matter in New England", "<p>Short trips, cold starts and road salt are hard on European cars. For turbocharged engines we generally recommend oil changes every 5,000–7,500 miles rather than stretching to the maximum interval, especially if the car is tuned.</p>"),
  ],
  faqs=[("Will servicing my car here void the warranty?", "No. Under the Magnuson-Moss Warranty Act you can have maintenance done at any qualified shop. Keep your records. We provide them on every repair order."),
        ("Do you reset the service indicator?", "Yes, including BMW Condition Based Service (CBS) items and Mercedes Service A/B reminders.")]),
 "/services/engine-repair/": dict(name="Engine & Drivetrain Repair",
  title="European Engine & Drivetrain Repair | Marlborough, MA",
  desc="Oil leaks, cooling systems, timing chains, VANOS, turbos and transmissions for BMW, Audi, VW and Mercedes in Marlborough, MA. Genuine and OE parts.",
  h1="Engine &amp; Drivetrain Repair",
  lede="The jobs other shops send away (oil leaks, cooling, timing, turbos and transmissions), repaired with genuine or OE-supplier parts.",
  body=[
   ("Engine repair", ticks(["Oil filter housing, valve cover and oil pan gaskets","Water pumps, thermostats and coolant pipes","Timing chains, guides and tensioners","VANOS solenoids and variable-valve-timing faults","Turbochargers, wastegates and charge pipes","Fuel injectors and high-pressure fuel pumps","Carbon cleaning (walnut blasting) on direct-injection engines"])),
   ("Drivetrain repair", ticks(["ZF 8-speed, DSG/S tronic and 7G/9G-Tronic service and repair","Clutches, flywheels and slave cylinders","xDrive transfer cases, quattro and Haldex","Driveshafts, guibos, center bearings and axles","Differential service and seals"])),
   ("Done right the first time", "<p>Big jobs are where shortcuts hurt. We replace the related wear items while we're in there, and tell you which ones are optional, so you aren't paying the same labor twice.</p>"),
  ],
  faqs=[("Is my oil leak worth fixing?", "Often, yes. Leaking oil on European engines frequently lands on exhaust parts or rots the serpentine belt and rubber hoses. We'll show you where it's coming from and what it's affecting."),
        ("Do you rebuild engines?", "For performance builds, yes: forged internals as part of a build plan. For stock engines we'll give you honest repair-versus-replace numbers.")]),
 "/services/brakes-suspension/": dict(name="Brakes, Suspension & Steering",
  title="European Brakes & Suspension Repair | Marlborough, MA",
  desc="Brakes, control arms, bushings, air suspension, coilovers and alignment for BMW, Audi, VW and Mercedes in Marlborough, MA.",
  h1="Brakes, Suspension &amp; Steering",
  lede="European cars are defined by how they stop and steer. We keep them tight, with OE parts for comfort, or performance parts for the track.",
  body=[
   ("Brakes", ticks(["Pads, rotors and sensors (OE or performance compounds)","Brake fluid flush (every two years is the factory norm)","Calipers and brake lines","Big brake kits for track and performance builds"])),
   ("Suspension & steering", ticks(["Control arms, thrust arms and bushings","Shocks, struts and mounts","Air suspension (BMW X5/X7, Audi Q7/A8, Mercedes Airmatic)","Coilovers and lowering springs","Wheel alignment to factory or performance specs"])),
  ],
  faqs=[("How do I know if my control arm bushings are worn?", "Common signs are a shimmy under braking, clunks over bumps, vague steering or uneven tire wear. We'll inspect and show you."),
        ("Can you align a lowered car?", "Yes, we align to factory spec or to a performance spec that suits your tires and driving.")]),
 "/services/performance-tuning/": dict(name="Performance & Tuning",
  title="BMW & European Performance Tuning | Marlborough, MA",
  desc="ECU tuning, turbo upgrades, fueling, cooling and drivetrain builds for BMW, Audi, VW and Mercedes in Marlborough, MA. Plan your build online.",
  h1="Performance &amp; Tuning",
  lede="Our shop car is a B58-powered 340i making 1,300 horsepower. Whether you want a clean Stage 1 or a full build, we plan it as a system: power, fueling, cooling, drivetrain and brakes.",
  body=[
   ("Plan your build", "<p>Use our <a href=\"/build/\">Build Your Car</a> tool to pick your car, set a power goal and see the parts and supporting mods it takes with a ballpark price. Every build starts with a health check, compression or leak-down, a full scan and a look at known weak points, because power on a tired engine is money wasted.</p>"),
   ("What we do", ticks(["Software tunes (bootmod3, MHD and platform-appropriate tuners) and custom tuning","Intakes, charge pipes, intercoolers and heat exchangers","Downpipes and exhaust","Fueling: port injection, low-pressure fuel pumps, injectors and flex-fuel/E85","Hybrid and big-single turbo upgrades","Transmission tuning, clutches, axles and driveshafts","Oil and transmission coolers","Brakes, suspension and tires to match the power"])),
   ("Street, track or competition", "<p>Street builds stay emissions-compliant with catted parts. If you're building a dedicated off-road or competition vehicle, tell us. The build tool has a competition option, and we'll talk through what that means for registration and inspection.</p>"),
  ],
  faqs=[("Will a tune hurt reliability?", "A conservative, well-supported tune on a healthy car is very reliable. Problems come from skipping supporting mods: fueling, cooling, ignition and drivetrain. That's why our build tool adds them automatically."),
        ("Can a tuned car pass Massachusetts inspection?", "Street builds using catted downpipes and emissions-compliant parts can pass as long as there are no warning lights and readiness monitors are set. Removing catalytic converters or emissions equipment won't pass and isn't legal on a road-registered car."),
        ("Do you dyno tune?", "Ask us about custom tuning for your platform when you send your build.")]),
 "/services/pre-purchase-inspection/": dict(name="Pre-Purchase Inspection",
  title="Used BMW & European Pre-Purchase Inspection | Marlborough",
  desc="Pre-purchase inspection for used BMW, Audi, VW and Mercedes in Marlborough, MA. Full module scan, known-failure checks and a written cost report.",
  h1="Pre-Purchase Inspection",
  lede="A used European car is a great buy or a money pit, usually decided by what you don't see in the listing. We'll tell you which one it is.",
  body=[
   ("What's included", ticks(["Full scan of every control module, including stored and history faults","Oil leaks, coolant leaks and known platform failures","Brakes, tires, suspension and steering","Evidence of accident repair or flood damage","Service history and software status review","Road test","Written report with photos and estimated costs to address findings"])),
   ("Why use a specialist", "<p>General shops miss model-specific issues: the parts that fail on <em>that</em> engine at <em>that</em> mileage. We know what to look for, and we can price it accurately so you can negotiate or walk away.</p>"),
  ],
  faqs=[("Can you inspect a car at a dealer?", "The best inspection happens on our lift. Most sellers, including dealers, will allow a pre-purchase inspection if you ask."),
        ("How long does it take?", "Plan on a couple of hours. We'll send the report and photos the same day whenever possible.")]),
}

def service_page(path):
    s = SERVICES[path]
    def body(ctx):
        sections = "".join(f"<h2>{h}</h2>{b}" for h, b in s["body"])
        sections = sections.replace('href="/build/"', f'href="{ctx.L("/build/")}"')
        return page_hero(ctx, f"Services · {CITY}", s["h1"], s["lede"],
                         [("Home", "/"), ("Services", "/services/"), (s["name"], path)]) + f'''
<section class="section"><div class="wrap split"><div class="prose">{sections}
<h2>Makes we service</h2><p>{" · ".join(f'<a href="{ctx.L(p)}">{e(n)}</a>' for n, p in MAKES_NAV)}</p></div>
{side_panel(ctx)}</div></section>{faq_block(s["faqs"])}'''
    return dict(title=s["title"], desc=s["desc"], crumbs=[("Home", "/"), ("Services", "/services/"), (s["name"], path)],
                faqs=s["faqs"], service=s["name"], body=body, priority="0.8")

def services_hub(ctx):
    items = [(n, SERVICES[p]["lede"], p) for n, p in SERVICES_NAV]
    return page_hero(ctx, f"Services · {CITY}", "European Auto Services", "Everything a BMW, Audi, Volkswagen or Mercedes-Benz needs, diagnosed properly, repaired with the right parts, and explained in plain language.",
                     [("Home", "/"), ("Services", "/services/")]) + '<section class="section"><div class="wrap"><div class="grid g3">' + "".join(
        f'<a class="card icard" href="{ctx.L(p)}">{ICON[SVC_ICON[p]]}<h3>{e(n)}</h3><p>{SERVICES[p]["lede"]}</p><span class="more">Learn more →</span></a>' for n, p in SERVICES_NAV) + f'</div></div></section><section class="section tight"><div class="wrap">{marques(ctx)}</div></section>'
    items = None
    return page_hero(ctx, f"Services · {CITY}", "European Auto Services", "Everything a BMW, Audi, Volkswagen or Mercedes-Benz needs, diagnosed properly, repaired with the right parts, and explained in plain language.",
                     [("Home", "/"), ("Services", "/services/")]) + f'<section class="section"><div class="wrap">{cards(ctx, items)}</div></section><section class="section tight"><div class="wrap">{marques(ctx)}</div></section>'

# ------------------------------------------------------------------ about / areas / contact / build / 404
def about(ctx):
    return page_hero(ctx, "About us", "European Car People, First", "Auto Addict Works is an independent European specialist in Marlborough, MA, built around factory-level diagnostics, correct parts and an honest explanation of every job.",
                     [("Home", "/"), ("About", "/about/")]) + f'''
<section class="section"><div class="wrap split"><div class="prose">
<h2>Why we started</h2>
<p>Owners of European cars usually get two choices: the dealer, with dealer pricing, or a general shop that treats a BMW like any other car. We built Auto Addict Works to be the third option: a specialist shop with the dealer's diagnostic software and parts quality, run by enthusiasts who explain what's actually going on with your car.</p>
<h2>BMW first, European always</h2>
<p>Our team drives BMWs, and our shop car, a B58-powered 340i, makes 1,300 horsepower. BMW is our deepest specialty, with Audi and Volkswagen close behind and Mercedes-Benz service as well. Whether it's your family's X5 or a weekend track car, it gets the same attention.</p>
<h2>How we work</h2>
{ticks(["Diagnose first, using factory procedures, never parts-cannon guessing.","Genuine and OE-supplier parts by default.","Written estimates and your approval before any work.","Photos and plain-language explanations of what we found.","Records on every repair order, so your service history stays complete."])}
</div>{side_panel(ctx)}</div></section>'''

def areas(ctx):
    towns = "".join(f"<li>{e(t)}, MA</li>" for t in CFG["areasServed"])
    return page_hero(ctx, "Areas we serve", "European Auto Repair Near You", f"Our shop is in {CITY}, a short drive from across MetroWest and Central Massachusetts via I-495, I-290, Route 20 and Route 9.",
                     [("Home", "/"), ("Areas We Serve", "/areas-we-serve/")]) + f'''
<section class="section"><div class="wrap split"><div class="prose">
<h2>Drivers come to us from</h2><ul style="columns:2">{towns}</ul>
<p>Don't see your town? Plenty of our customers drive further for a specialist. Call us and we'll help you plan drop-off.</p>
<h2>What we service</h2><p>{" · ".join(f'<a href="{ctx.L(p)}">{e(n)} repair</a>' for n, p in MAKES_NAV)}, plus <a href="{ctx.L("/services/performance-tuning/")}">performance builds</a> and <a href="{ctx.L("/services/pre-purchase-inspection/")}">pre-purchase inspections</a>.</p>
</div>{side_panel(ctx)}</div></section>'''

def contact(ctx):
    hrs = "<br>".join(__import__("build").hours_text())
    return page_hero(ctx, "Contact", "Book Service or Ask a Question", "Tell us about your car and what's going on. We'll reply with next steps, or call us directly.",
                     [("Home", "/"), ("Contact", "/contact/")], ctas=False) + f'''
<section class="section"><div class="wrap split">
<form class="form" id="contact-form" novalidate>
<div id="build-summary-wrap" hidden><label for="build">Your build</label><textarea id="build" name="build" readonly style="min-height:180px"></textarea></div>
<div class="row"><div><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
<div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div></div>
<div class="row"><div><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email"></div>
<div><label for="vehicle">Year, make &amp; model</label><input id="vehicle" name="vehicle" placeholder="e.g. 2019 BMW 340i"></div></div>
<div><label for="reason">What can we help with?</label><select id="reason" name="reason"><option>Maintenance / service</option><option>Diagnosis / warning light</option><option>Repair</option><option>Performance build</option><option>Pre-purchase inspection</option><option>Something else</option></select></div>
<div><label for="msg">Details</label><textarea id="msg" name="message" placeholder="Symptoms, warning lights, mileage, preferred drop-off day…"></textarea></div>
<div class="form-status" id="form-status" role="status"></div>
<div><button class="btn btn-primary" type="submit">Send Request</button></div>
<p class="note">We'll only use your details to respond to this request.</p>
</form>
<aside class="panel"><h3>Shop</h3>
<address class="nap"><strong>{e(CFG["name"])}</strong><br>{e(A["street"])}<br>{e(A["city"])}, {A["region"]} {A["postal"]}</address>
<p style="margin-top:16px"><a href="tel:{CFG["phoneE164"]}">{e(CFG["phoneDisplay"])}</a><br><a href="mailto:{CFG["email"]}">{e(CFG["email"])}</a></p>
<h3 style="margin-top:28px">Hours</h3><p class="muted">{hrs}</p>
<a class="btn btn-ghost" href="{CFG["mapsUrl"]}" target="_blank" rel="noopener">Get Directions</a></aside>
</div></section>'''

BUILD_FAQS = [
 ("How do you price a build?", "Every build is quoted after a pre-build health check, because condition, mileage and previous mods change the plan. Send us your build and we'll follow up with a written quote."),
 ("Why does the build add parts I didn't pick?", "Power needs support. Fueling, cooling, ignition and drivetrain limits are the usual reasons tuned cars fail, so the tool adds what your goal and use actually require."),
 ("What does the off-road / competition option change?", "It unlocks parts that remove or modify emissions equipment, such as catless downpipes. Those builds are for vehicles used off public roads only. They can't pass Massachusetts inspection and aren't legal on a road-registered car."),
 ("My car isn't listed. Can you still build it?", "The planner covers the BMW platforms we build most: B58, S55 and S58. For anything else, send us a note through the contact form and we'll quote it directly."),
]

def build_page(ctx):
    crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{ctx.L("/")}">Home</a><span>/</span><span aria-current="page" style="margin:0;opacity:1">Build Your Car</span></nav>'
    return f'''<div class="bx" id="builder" data-contact="{ctx.L("/contact/")}">
<section class="bx-hero"><div class="wrap">{crumbs}
 <span class="eyebrow line">BMW performance builds</span>
 <h1>Build Your <span>Car</span></h1>
 <p class="lede">Pick your platform, set your goal and see exactly what it takes to get there: every part, every supporting mod, start to finish.</p>
 <div class="progress" id="prog"><div class="on"><b>01</b>Platform</div><div><b>02</b>How you drive</div><div><b>03</b>Power goal</div><div><b>04</b>Build sheet</div></div>
</div></section>

<section class="sec"><div class="wrap">
 <div class="sec-h"><b>01</b><h2>Choose your platform</h2><p>BMW turbo platforms we build in-house</p></div>
 <div class="plats" id="plats"></div>
 <div class="vinbar"><span>Not sure? Decode your VIN</span><input id="vin" placeholder="17-character VIN" maxlength="17" autocomplete="off" spellcheck="false" aria-label="VIN"><button class="btn" id="vin-go" type="button">Decode</button></div><div class="vinmsg" id="vin-msg" aria-live="polite"></div>
</div></section>

<section class="sec"><div class="wrap">
 <div class="sec-h"><b>02</b><h2>How you'll drive it</h2><p>We add the supporting mods your use actually needs</p></div>
 <div class="modes" id="modes"></div>
 <div class="compete"><button class="switch" id="comp" type="button" role="switch" aria-checked="false" aria-label="Off-road / competition build"></button>
  <div><b>Off-road / competition build</b><small>Unlocks catless downpipes and race parts. Not for street-registered cars and won't pass MA inspection.</small></div>
  <span class="tag">Signed waiver</span></div>
</div></section>

<section class="sec"><div class="wrap">
 <div class="sec-h"><b>03</b><h2>Set your power goal</h2><p>Drag the needle or jump to a stage</p></div>
 <div class="power">
  <div class="gauge-card">
   <svg class="bx-gauge" viewBox="0 0 400 300" id="gauge">
    <defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#A8864F"/><stop offset=".5" stop-color="#E6D3A8"/><stop offset="1" stop-color="#C5A572"/></linearGradient></defs>
    <g id="g-ticks"></g>
    <path class="g-track" id="g-track"/>
    <path class="g-stock" id="g-stock"/>
    <path class="g-fill" id="g-fill"/>
    <g id="g-marks"></g>
    <g class="needle" id="needle"><line x1="200" y1="100" x2="200" y2="40" stroke="#F1EBDF" stroke-width="4" stroke-linecap="round"/><circle cx="200" cy="40" r="5" fill="#F1EBDF"/></g>
   </svg>
   <div class="readout"><b id="hp">0</b><span>EST. WHEEL HP</span><em id="gain">Stock power</em></div>
   <div class="slider"><input type="range" id="range" step="10" aria-label="Target horsepower"></div>
   <div class="stages" id="stagechips"></div>
  </div>
  <div class="dyno-card">
   <div class="dyno-top"><h3>Dyno projection</h3><div class="legend"><span><i style="background:#6F7D82"></i>Stock</span><span><i style="background:#C5A572"></i>Your build</span></div></div>
   <svg class="dyno" viewBox="0 0 720 360" id="dyno">
    <defs><linearGradient id="dg" x1="0" x2="1"><stop offset="0" stop-color="#A8864F"/><stop offset=".6" stop-color="#E6D3A8"/><stop offset="1" stop-color="#C5A572"/></linearGradient>
     <linearGradient id="da" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(197,165,114,.28)"/><stop offset="1" stop-color="rgba(197,165,114,0)"/></linearGradient></defs>
    <g id="d-grid"></g>
    <path class="d-area" id="d-area"/><path class="d-stock" id="d-stock"/><path class="d-tgt" id="d-tgt"/>
   </svg>
   <div class="kpis"><div><b id="k1">+75%</b><span>Power gain</span></div><div><b id="k2">Stage 2+ E85</b><span>Build level</span></div><div><b id="k3">E85 / 93</b><span>Fuel</span></div></div>
   <span class="illus">Illustrative curve from typical tuner results, not your car&#39;s dyno sheet</span>
  </div>
 </div>
</div></section>

<section class="sec" id="sheet"><div class="wrap">
 <div class="sec-h"><b>04</b><h2>Your build sheet</h2><p>The path from stock to your goal</p></div>
 <div class="sheet">
  <div><div class="road" id="road"></div><div id="supportwrap"></div></div>
  <aside class="summary">
   <div class="sum-h"><small id="s-car">B58 Gen 1 · ZF 8-speed</small><h3 id="s-stage">Stage 2+ E85</h3><p id="s-sub">~560 hp · Spirited street</p>
    <div class="bar"><i id="s-bar"></i><u id="s-stockmark"></u></div><div class="barl"><span id="s-stock">Stock 320</span><span id="s-max">Max 1,300</span></div></div>
   <div class="price"><div class="price-top"><span>Estimated investment</span><button class="mini" id="ptog" type="button" hidden><span class="switch" id="psw"></span>Show pricing</button></div>
    <div id="pbody"></div></div>
   <div class="flags" id="flags"></div>
   <div class="bx-cta"><button class="btn gold" id="r-send" type="button">Request this build →</button><button class="btn" id="r-copy" type="button">Copy build sheet</button>
    <div class="share"><a href="#" id="r-link">Copy link to this build</a></div></div>
  </aside>
 </div>
</div></section>

<a class="mbar" id="mbar" href="#sheet" hidden><span id="mbar-t">Your build</span><b>View build ↓</b></a>
</div>
{faq_block(BUILD_FAQS, "About the build planner")}'''

def notfound(ctx):
    return page_hero(ctx, "404", "Page Not Found", "That page has moved or doesn't exist. Try one of these instead.", None, ctas=False) + \
        f'<section class="section"><div class="wrap">{cards(ctx, [("Services", "Diagnostics, maintenance, repair and performance.", "/services/"), ("Build Your Car", "Map a build and see a ballpark price.", "/build/"), ("Contact", "Book service or ask a question.", "/contact/")])}</div></section>'

# ------------------------------------------------------------------ registry
PAGES = {
 "/": dict(title="BMW & European Auto Repair, Marlborough MA | Auto Addict Works",
           desc="European auto repair in Marlborough, MA. Factory BMW ISTA diagnostics, genuine parts and performance builds for BMW, Audi, VW and Mercedes-Benz.",
           faqs=HOME_FAQS, body=home, priority="1.0"),
 "/services/": dict(title="European Auto Repair Services | Auto Addict Works", desc="Diagnostics, maintenance, engine and drivetrain repair, brakes and suspension, performance tuning and pre-purchase inspections in Marlborough, MA.",
           crumbs=[("Home", "/"), ("Services", "/services/")], body=services_hub, priority="0.8"),
 "/build/": dict(title="Build Your Car: Performance Build Planner | Auto Addict Works",
           desc="Plan your BMW, Audi, VW or Mercedes build. Pick your car and power goal to see the parts, supporting mods and a ballpark price. Street, track or race.",
           crumbs=[("Home", "/"), ("Build Your Car", "/build/")], faqs=BUILD_FAQS, body=build_page, builder=True, priority="0.9"),
 "/about/": dict(title="About Auto Addict Works | European Specialists, Marlborough", desc="Independent BMW and European specialist in Marlborough, MA, factory diagnostics, genuine parts and enthusiasts who build these cars.",
           crumbs=[("Home", "/"), ("About", "/about/")], body=about, priority="0.6"),
 "/areas-we-serve/": dict(title="European Auto Repair Near Hudson, Framingham & Marlborough", desc="Auto Addict Works serves BMW, Audi, VW and Mercedes owners across MetroWest: Marlborough, Hudson, Southborough, Northborough, Sudbury, Framingham and more.",
           crumbs=[("Home", "/"), ("Areas We Serve", "/areas-we-serve/")], body=areas, priority="0.6"),
 "/contact/": dict(title="Contact & Book Service | Auto Addict Works, Marlborough MA", desc="Book European auto service in Marlborough, MA. 41 Brigham Street, Unit 1. Call, email or send a request online.",
           crumbs=[("Home", "/"), ("Contact", "/contact/")], body=contact, priority="0.7"),
 "/404.html": dict(title="Page Not Found | Auto Addict Works", desc="Page not found.", body=notfound, noindex=True),
}
def sales_page(ctx):
    return page_hero(ctx, "Vehicle sales & sourcing", "Vehicle Sales &amp; Sourcing", "Hand-picked European cars, inspected and reconditioned by the same team that services them, or tell us what you're looking for and we'll find it.",
                     [("Home", "/"), ("Vehicle Sales", "/vehicle-sales/")]) + f'''<section class="section"><div class="wrap split"><div class="prose">
<h2>Every car goes through the shop first</h2>{ticks(["Full ISTA / module scan and known-failure inspection","Reconditioning with genuine and OE parts","Service records and findings shared with you"])}
<h2>Looking for something specific?</h2><p>Tell us the model, spec and budget. We source from dealer auctions and inspect before you commit.</p></div>{side_panel(ctx, "Talk to us")}</div></section>'''

if CFG.get("showVehicleSales"):
    PAGES["/vehicle-sales/"] = dict(title="Used BMW & European Cars for Sale | Auto Addict Works", desc="Inspected, reconditioned European cars and vehicle sourcing from the team at Auto Addict Works in Marlborough, MA.",
        crumbs=[("Home", "/"), ("Vehicle Sales", "/vehicle-sales/")], body=sales_page, priority="0.7")
for k in MAKES: PAGES[MAKES[k]["path"]] = make_page(k)
for p in SERVICES: PAGES[p] = service_page(p)
