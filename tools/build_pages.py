#!/usr/bin/env python3
"""Builds the SSR Group Civil inner pages (service pages, cost calculator, 404) as static HTML.

Run from the repo root:  python3 tools/build_pages.py
Edit the PAGES content below, re-run, commit. Vercel serves the output with clean URLs.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://ssrgroupcivil.in'
PHONE = '+91 87961 38550'
TEL = '+918796138550'
EMAIL = 'info@ssrgroupcivil.in'
WA = '918796138550'

# Package rates (Rs per sq ft of built-up area). Source: SSR BOQ tiers, October 2026 (Rishikesh G+1, 2,008 sq ft).
RATES = {'Essential': 1800, 'Comfort': 2100, 'Premium': 2740}

SERVICE_LINKS = [
    ('/builder-floor-construction-delhi', 'Builder floors & G+3 homes'),
    ('/villa-farmhouse-construction', 'Villas & farmhouses'),
    ('/flat-interiors-greater-noida-west', 'Flat interiors'),
    ('/project-management-consultancy', 'Project control / PMC'),
    ('/firefighting-plumbing-contractor', 'Firefighting & plumbing'),
    ('/3d-project-pages', '3D project pages'),
]
NAV = [
    ('/builder-floor-construction-delhi', 'Builder floors'),
    ('/villa-farmhouse-construction', 'Villas'),
    ('/flat-interiors-greater-noida-west', 'Interiors'),
    ('/project-management-consultancy', 'PMC'),
    ('/3d-project-pages', '3D pages'),
    ('/construction-cost-calculator', 'Cost calculator'),
]

BUSINESS = {
    '@context': 'https://schema.org',
    '@type': 'GeneralContractor',
    '@id': BASE + '/#business',
    'name': 'SSR Group Civil',
    'url': BASE + '/',
    'logo': BASE + '/img/logo-cut.png',
    'image': BASE + '/img/villa-dusk.jpg',
    'telephone': PHONE,
    'email': EMAIL,
    'address': {'@type': 'PostalAddress', 'streetAddress': 'E/207, Apex Aura Society, Sector 1',
                'addressLocality': 'Greater Noida West', 'addressRegion': 'Uttar Pradesh', 'addressCountry': 'IN'},
    'areaServed': ['Delhi', 'Noida', 'Greater Noida West', 'Greater Noida', 'Ghaziabad', 'Gurugram'],
    'description': 'Construction management consultancy in Delhi NCR: builder floors and houses, villas, '
                   'flat interiors, project control (PMC), firefighting and plumbing, and 3D project pages.',
    'knowsAbout': ['RCC construction', 'Builder floor construction', 'Project management consultancy',
                   'Interior fit-out', 'Firefighting systems', 'Plumbing', '3D walkthroughs'],
}

SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-wa" viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 20zm4.4-6c-.2-.1-1.4-.7-1.6-.8s-.4-.1-.5.1-.6.8-.8 1-.3.2-.5.1a6.5 6.5 0 0 1-3.2-2.8c-.2-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.7-1.7c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6a2.6 2.6 0 0 0 1.7-1.2 2 2 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3z"/></symbol>
<symbol id="i-right" viewBox="0 0 24 24"><path d="M4 12h16M14 6l6 6-6 6"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M3 7h18M3 12h18M3 17h12"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="i-cube" viewBox="0 0 24 24"><path d="M12 2.8l8 4.5v9.4l-8 4.5-8-4.5V7.3z"/><path d="M4 7.3l8 4.5 8-4.5M12 11.8v9.4"/></symbol>
</svg>'''

ARROW = '<svg class="icon"><use href="#i-right"/></svg>'
WAI = '<svg class="icon fill"><use href="#i-wa"/></svg>'
PHI = '<svg class="icon"><use href="#i-phone"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'


def header(current):
    links = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else '', esc(t)) for h, t in NAV)
    mlinks = '<a href="/">Home</a>' + ''.join('<a href="%s">%s</a>' % (h, esc(t)) for h, t in SERVICE_LINKS) + \
        '<a href="/construction-cost-calculator">Cost calculator</a><a href="/#work">Our work</a><a href="/#contact">Contact</a>'
    return '''<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="SSR Group Civil, home"><img src="/img/logo.png" alt="" width="141" height="112"><span><b>SSR Group Civil</b><small>Civil · PMC · Interiors · 3D</small></span></a>
    <nav class="nav" aria-label="Services">%s</nav>
    <div class="tools">
      <a class="call-btn" href="tel:%s">%s Call</a>
      <a class="tool" data-wa="Hi Sankalp, I saw ssrgroupcivil.in and want to talk about a project." href="https://wa.me/%s" target="_blank" rel="noopener" aria-label="WhatsApp SSR Group Civil">%s</a>
      <button class="tool menu-btn" id="menu-btn" type="button" aria-label="Open menu" aria-expanded="false"><svg class="icon"><use href="#i-menu"/></svg></button>
    </div>
  </div>
</header>
<nav class="mobile-nav" id="mobile-nav" aria-label="Menu">
  <button class="close" id="menu-close" type="button" aria-label="Close menu"><svg class="icon"><use href="#i-x"/></svg></button>
  %s
</nav>''' % (links, TEL, PHI, WA, WAI, mlinks)


def footer():
    svc = ''.join('<a href="%s">%s</a>' % (h, esc(t)) for h, t in SERVICE_LINKS)
    return '''<footer class="site">
  <div class="wrap">
    <div class="fgrid">
      <div><img src="/img/logo-cut.png" alt="SSR Group Civil" width="404" height="319" loading="lazy"><p>Civil execution, project control, firefighting, plumbing, interiors and 3D for Delhi NCR.</p></div>
      <div><h4>Services</h4>%s</div>
      <div><h4>Tools &amp; work</h4><a href="/construction-cost-calculator">Construction cost calculator</a><a href="/site-log">Free daily progress report tool</a><a href="/#work">Signature projects</a><a href="/#aura01">AURA01, live build</a><a href="/#walk">Walkthroughs</a></div>
      <div><h4>Office</h4><span>E/207, Apex Aura Society, Sector 1, Greater Noida West, Uttar Pradesh</span><a href="tel:%s">%s</a><a href="mailto:%s">%s</a></div>
    </div>
    <div class="base"><span>© 2026 SSR Group Civil</span><span>Renders and models are artist's impressions unless marked as a live project.</span></div>
  </div>
</footer>
<div class="callbar"><a class="c" href="tel:%s">%s Call</a><a class="w" data-wa="Hi Sankalp, I saw ssrgroupcivil.in and want to talk about a project." href="https://wa.me/%s" target="_blank" rel="noopener">%s WhatsApp</a></div>''' % (svc, TEL, PHONE, EMAIL, EMAIL, TEL, PHI, WA, WAI)


def enquiry(topic, heading='Tell us about your <em>project.</em>', blurb=None):
    blurb = blurb or 'Leave your number and SSR will get back to you, or send the same message on WhatsApp. Drawings, photos and brochures can follow in the chat.'
    return '''<section class="section" id="enquire" aria-labelledby="enq-h">
  <div class="wrap enq-grid">
    <div>
      <p class="eyebrow">Enquiry</p>
      <h2 id="enq-h">%s</h2>
      <p class="lede" style="margin-top:16px">%s</p>
      <address class="contact-list">
        <div><small>Call or WhatsApp</small><a class="big" href="tel:%s">%s</a></div>
        <div><small>Email</small><a href="mailto:%s">%s</a></div>
        <div><small>Office</small><span>E/207, Apex Aura Society, Sector 1, Greater Noida West</span></div>
      </address>
    </div>
    <form class="enq" data-topic="%s" novalidate>
      <div class="pair">
        <label class="field">Your name<input name="name" autocomplete="name" required></label>
        <label class="field">Mobile<input name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+91" required></label>
      </div>
      <label class="field">Site location<input name="place" placeholder="e.g. Kirari, Delhi / Gaur City 2, Greater Noida West"></label>
      <label class="field">What do you want built?<textarea name="msg" placeholder="Plot or flat size, number of floors, and when you want to start."></textarea></label>
      <input type="hidden" name="topic" value="%s">
      <label class="hp" aria-hidden="true">Leave empty<input name="_honey" tabindex="-1" autocomplete="off"></label>
      <div class="form-actions">
        <button class="btn ink" type="submit" data-send>Send enquiry %s</button>
        <a class="btn" data-wa-form href="https://wa.me/%s" target="_blank" rel="noopener">%s WhatsApp instead</a>
      </div>
      <p class="status" role="status" aria-live="polite" hidden></p>
      <p class="fine" style="margin:0">Send enquiry emails your name, number and message to SSR. Nothing is stored on this site.</p>
    </form>
  </div>
</section>''' % (heading, esc(blurb), TEL, PHONE, EMAIL, EMAIL, esc(topic), esc(topic), ARROW, WA, WAI)


def faq_html(faqs):
    items = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (esc(q), a) for q, a in faqs)
    return '''<section class="section" aria-labelledby="faq-h">
  <div class="narrow">
    <div class="head"><p class="eyebrow">Questions</p><h2 id="faq-h">Asked <em>before every job</em></h2></div>
    <div class="faq">%s</div>
  </div>
</section>''' % items


def strip_tags(s):
    import re
    return re.sub(r'<[^>]+>', '', s)


def page(p):
    url = BASE + p['path']
    crumbs = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">%s</span></nav>' % esc(p['crumb'])
    if p.get('hero_img'):
        hero = '''<section class="phero">
  <div class="wrap">
    %s
    <div class="phero-grid">
      <div>
        <p class="eyebrow">%s</p>
        <h1 style="margin-top:12px">%s</h1>
        <p class="lede">%s</p>
        <div class="actions"><a class="btn ink" href="#enquire">Ask for a quote %s</a><a class="btn" href="/construction-cost-calculator">Estimate the cost</a></div>
      </div>
      <figure><img src="%s" alt="%s" width="960" height="540" fetchpriority="high"><figcaption>%s</figcaption></figure>
    </div>
  </div>
</section>''' % (crumbs, esc(p['eyebrow']), p['h1'], p['lede'], ARROW, p['hero_img'], esc(p['hero_alt']), esc(p['hero_cap']))
    else:
        hero = '''<section class="phero night">
  <div class="wrap">
    %s
    <div style="max-width:880px;margin-top:22px">
      <p class="eyebrow">%s</p>
      <h1 style="margin-top:12px">%s</h1>
      <p class="lede">%s</p>
      <div class="actions"><a class="btn gold" href="#enquire">Ask for a quote %s</a><a class="btn ghost-night" href="/project-management-consultancy">See project control</a></div>
    </div>
  </div>
</section>''' % (crumbs, esc(p['eyebrow']), p['h1'], p['lede'], ARROW)

    others = ''.join('<a href="%s">%s</a>' % (h, esc(t)) for h, t in SERVICE_LINKS if h != p['path'])
    related = '''<section class="section" aria-labelledby="rel-h"><div class="wrap"><div class="head"><p class="eyebrow">Also from SSR</p><h2 id="rel-h" style="font-size:clamp(28px,3vw,40px)">Other work we take on</h2></div><div class="related">%s<a href="/construction-cost-calculator">Construction cost calculator</a></div></div></section>''' % others

    schema = [BUSINESS, {
        '@context': 'https://schema.org', '@type': 'Service', 'name': p['service_name'], 'serviceType': p['service_type'],
        'url': url, 'description': p['description'], 'provider': {'@id': BASE + '/#business'},
        'areaServed': p.get('area', ['Delhi', 'Noida', 'Greater Noida West', 'Ghaziabad', 'Gurugram'])
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': p['crumb'], 'item': url}]
    }]
    if p.get('faqs'):
        schema.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in p['faqs']]})

    body = hero + p['body'] + (faq_html(p['faqs']) if p.get('faqs') else '') + enquiry(p['topic']) + related
    return doc(p['title'], p['description'], url, p.get('og_img') or (p.get('hero_img') or '/img/villa-dusk.jpg').replace('-960', ''), schema, header(p['path']), body, p.get('extra_head', ''), p.get('extra_tail', ''))


def doc(title, desc, url, og_img, schema, head_html, body, extra_head='', extra_tail=''):
    return '''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0A1020">
<meta property="og:type" content="website"><meta property="og:site_name" content="SSR Group Civil"><meta property="og:locale" content="en_IN">
<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/img/favicon.png"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Carlito:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap">
<link rel="stylesheet" href="/assets/site.css">
%s
%s
</head>
<body>
%s
%s
<main>
%s
</main>
%s
<script src="/assets/site.js" defer></script>
%s
</body>
</html>
''' % (esc(title), esc(desc), url, esc(title), esc(desc), url, BASE + og_img, '\n'.join(ld(s) for s in schema), extra_head,
       SPRITE, head_html, body, footer(), extra_tail)


def ticks(items):
    return '<ul class="ticks">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'


def two_col(eyebrow, h2, inner, sid=None):
    return '''<section class="section"%s><div class="wrap two-col"><div><p class="eyebrow">%s</p><h2 style="margin-top:10px">%s</h2></div><div>%s</div></div></section>''' % (
        ' id="%s"' % sid if sid else '', esc(eyebrow), h2, inner)


def rates_block(note):
    cards = ''.join('<div class="rate%s"><small>%s</small><b>₹%s<sub>/ sq ft</sub></b><p>%s</p></div>' % (
        ' pick' if k == 'Comfort' else '', k, format(v, ','), d) for (k, v), d in zip(RATES.items(), [
            'Branded economy finishes. The structure is never reduced.',
            'Mid-range finishes and fittings.',
            'Premium finishes and fittings throughout.']))
    return '<div class="rates">%s</div><p class="fine">%s</p>' % (cards, note)


RATE_NOTE = ('Indicative rates per sq ft of built-up area, from SSR\'s October 2026 BOQ. Every package keeps M25 concrete, '
             'Fe500D steel and SSR supervision. Land, map approval fees, utility connections, lift and basement are extra. '
             'The fixed quote comes after a site visit and drawings.')

STEPS_BUILD = '''<ol class="steps">
<li><b>Approved drawings</b><p>We build from the issued set and log every revision.</p></li>
<li><b>BOQ and BBS</b><p>Quantities measured from the drawings; a bar bending schedule for every footing, column, beam and slab.</p></li>
<li><b>Pour card</b><p>An IS 456 pour card, signed by the proprietor, before every pour.</p></li>
<li><b>Daily report</b><p>Photos, manpower and progress, sent every site day.</p></li>
</ol>'''

PAGES = []

# 1 ---------------------------------------------------------------- builder floors
PAGES.append(dict(
    path='/builder-floor-construction-delhi', crumb='Builder floors & G+3 homes', topic='Builder floor / G+3 construction',
    title='Builder Floor & G+3 House Construction in Delhi | SSR Group Civil',
    description='G+3 and G+4 builder floors and houses built across Delhi NCR, with a drawing for every slab, a pour card before every pour and a daily site report. See package rates and a live build.',
    service_name='Builder floor and house construction', service_type='Residential construction',
    eyebrow='Builder floors · Delhi NCR', h1='Builder floors and G+3 homes, built <em>slab by slab</em>',
    lede='SSR builds G+3 and G+4 homes on tight urban plots in Delhi, Noida and Greater Noida West: structure, services and finishes, with a drawing for every slab and a record of every pour.',
    hero_img='/img/aura01-ref-960.jpg', hero_alt='AURA01 corner residence at dusk in ivory and charcoal, reference visualisation of a live SSR build',
    hero_cap='AURA01 · reference visualisation',
    body=two_col('What SSR handles', 'From the footing to the <em>façade</em>', ticks([
        'Foundation, column, beam and slab rebar drawings, and a bar bending schedule for each',
        'A shuttering plan and a signed pour card before each slab',
        'Electrical and plumbing layouts, floor by floor',
        'Brick, steel and concrete estimates for every floor cycle',
        'The façade scheme agreed on a 3D model before it is built',
        'Concealed CPVC plumbing, FR copper wiring with RCCB protection, and waterproofing tested before tiling'])) +
    '''<section class="section band" aria-labelledby="live-h"><div class="wrap">
<p class="eyebrow">Live build</p><h2 id="live-h" style="margin-top:10px">AURA01, <em>Kiradi, Delhi</em></h2>
<div class="prose" style="margin-top:18px;max-width:70ch"><p>A G+3 residence on an <b>18 × 32 ft corner plot</b> with roads on two sides, executed and documented by SSR from demolition onward. Three-foot balconies wrap the front, side and rear on every upper floor; the frame is RCC on nine columns, with a lift shaft and a dog-leg stair.</p>
<p>The first-floor slab was cast in September 2026 and the second-floor slab is underway. Every slab has its own rebar and shuttering drawing, and every week has a progress report built from site photographs.</p></div>
<div class="stats"><div><b>G+3</b><span>ground floor 9 ft, upper floors 10 ft</span></div><div><b>9</b><span>RCC columns on isolated footings</span></div><div><b>5 in</b><span>slabs on 9 × 9 in beams</span></div><div><b>3 ft</b><span>wrap-around balconies with open MS railings</span></div></div>
<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:30px"><a class="btn gold" href="/viewer-aura01-facade"><svg class="icon"><use href="#i-cube"/></svg>Turn the façade in 3D</a><a class="btn ghost-night" href="/#aura01">See the progress ledger</a></div>
</div></section>''' +
    '''<section class="section"><div class="wrap"><div class="head"><p class="eyebrow">How the build runs</p><h2>One chain, from <em>drawing to site</em></h2></div>%s</div></section>''' % STEPS_BUILD +
    '''<section class="section"><div class="wrap"><div class="head"><p class="eyebrow">What it costs</p><h2>Three packages, <em>one structure</em></h2><p class="lede">A 100 gaj plot (900 sq ft) built G+3 is about 3,600 sq ft of construction plus a stair mumty. At the Comfort rate that is roughly ₹78 lakh before land, approvals and a lift. Put in your own plot in the calculator.</p></div>%s<div style="margin-top:22px"><a class="link-arrow" href="/construction-cost-calculator">Open the cost calculator %s</a></div></div></section>''' % (rates_block(RATE_NOTE), ARROW),
    faqs=[
        ('How much does it cost to build a G+3 builder floor in Delhi?',
         'It depends on the built-up area and the finishes. SSR\'s October 2026 package rates are about ₹1,800 (Essential), ₹2,100 (Comfort) and ₹2,740 (Premium) per sq ft of built-up area, before land, map approval fees, utility connections and a lift. Use the <a href="/construction-cost-calculator">cost calculator</a> for your plot, then ask for a fixed quote after a site visit.'),
        ('Do you work from my architect\'s drawings?',
         'Yes. Design stays with your architect. SSR builds from the issued set, logs every revision, and prepares the rebar, shuttering, electrical and plumbing drawings the site needs.'),
        ('How will I know the work is being done right?',
         'A pour card is signed by the proprietor before every pour, steel is tracked from the bar bending schedule to fixing, and you get a daily progress report with site photographs.'),
        ('Which areas do you build in?',
         'Delhi, Noida, Greater Noida West, Ghaziabad and Gurugram, from our office at Apex Aura Society, Sector 1, Greater Noida West.'),
    ]))

# 2 ---------------------------------------------------------------- flat interiors
PAGES.append(dict(
    path='/flat-interiors-greater-noida-west', crumb='Flat interiors', topic='Flat interior fit-out',
    title='Flat Interior Fit-Out in Greater Noida West & Noida | SSR Group Civil',
    description='Modular kitchens, wardrobes, false ceilings, lighting and painting for society flats in Greater Noida West and Noida. A measured plan and a material board before anything is ordered.',
    service_name='Flat interior fit-out', service_type='Interior fit-out',
    area=['Greater Noida West', 'Greater Noida', 'Noida', 'Ghaziabad', 'Delhi'],
    eyebrow='Interiors · society flats', h1='Interiors for <em>society flats</em>',
    lede='Kitchens, wardrobes, ceilings and lighting for flat owners in Greater Noida West and across NCR, planned on a furnished drawing and a material board before anything is ordered. Our own office is in Apex Aura Society, Sector 1.',
    hero_img='/img/flat-living-960.jpg', hero_alt='Ivory and oak apartment living and dining room, concept render', hero_cap='Apartment concept render',
    body=two_col('What we fit out', 'Choose a part, <em>or the whole flat</em>', ticks([
        'Measured survey and a furnished plan',
        'A material board before anything is ordered',
        'Modular kitchen and wardrobe drawings, built in BWP ply with branded hardware',
        'Gypsum false ceiling with cove lighting',
        'Painting, polish and bathroom upgrades',
        'A progress update on WhatsApp every site day'])) +
    '''<section class="section"><div class="wrap"><div class="head"><p class="eyebrow">How it runs</p><h2>Three steps to <em>moving in</em></h2></div><ol class="steps">
<li><b>We visit and measure</b><p>We measure the flat and note what stays.</p></li>
<li><b>Plan and material board</b><p>You approve a furnished plan and the materials on samples.</p></li>
<li><b>Work starts</b><p>With a progress update on WhatsApp every site day.</p></li></ol></div></section>''' +
    two_col('Typical costs', 'From a recent <em>SSR quote</em>', '''<div class="prose"><p>Prices from a fixed quote SSR issued in October 2026 for a three-bedroom home. Your flat is priced after a measured survey.</p></div>
<div class="rates" style="margin-top:20px;grid-template-columns:1fr"><div class="rate"><small>L-shaped modular kitchen</small><b>₹1,50,000</b><p>About 10 × 8 ft; BWP ply with laminate shutters, soft-close hinges, drawer units, tall unit and under-cabinet lighting.</p></div>
<div class="rate"><small>Four wardrobes</small><b>₹1,45,000</b><p>6 ft wide × 7 ft high each, BWP ply carcass with laminate shutters, mirror shutter in the master.</p></div>
<div class="rate"><small>False ceiling</small><b>₹55,000</b><p>About 450 sq ft of gypsum board with cove lighting in the living-dining and three bedrooms.</p></div></div>
<p class="fine">Palettes to start from: Ivory &amp; Oak, Charcoal &amp; Brass, Sandstone &amp; Teak, Sage &amp; Walnut. Try them in the <a href="/#studio">interiors studio</a>.</p>'''),
    faqs=[
        ('What does a flat interior fit-out include?',
         'Whatever you choose: a modular kitchen, wardrobes, false ceiling and lighting, painting and polish, bathroom work, or a full fit-out of the flat.'),
        ('How much does a modular kitchen cost in Greater Noida West?',
         'In a recent SSR quote, an L-shaped kitchen of about 10 × 8 ft in BWP ply with laminate shutters and soft-close hardware came to ₹1.5 lakh. Your price depends on size, materials and hardware, and is fixed after a measured survey.'),
        ('Will I see the design before work starts?',
         'Yes. You approve a furnished plan and a material board before anything is ordered, and SSR can show the rooms in 3D.'),
        ('Which societies do you work in?',
         'Societies across Greater Noida West and Noida, as well as Ghaziabad and Delhi. Our office is in Apex Aura Society, Sector 1, Greater Noida West.'),
    ]))

# 3 ---------------------------------------------------------------- villas
PAGES.append(dict(
    path='/villa-farmhouse-construction', crumb='Villas & farmhouses', topic='Villa / farmhouse / courtyard home',
    title='Villa & Farmhouse Construction in Delhi NCR | SSR Group Civil',
    description='Villas, farmhouses and courtyard homes planned, modelled in 3D and built by SSR: double-height rooms, pools, jaali and stone, with the RCC executed from structural drawings.',
    service_name='Villa and farmhouse construction', service_type='Residential construction',
    eyebrow='Villas · farmhouses · courtyard homes', h1='Villas, farmhouses and <em>courtyard homes</em>',
    lede='Double-height rooms, pools and façades, modelled and walked through before they are built. Then the RCC goes up from structural drawings, with interiors and landscape coordinated with the build.',
    hero_img='/img/villa-dusk-960.jpg', hero_alt='Two-storey villa with double-height glazing and a pool terrace at dusk, concept render', hero_cap='Villa concept render',
    body=two_col('What SSR handles', 'Planned in 3D, <em>built on site</em>', ticks([
        'Concept plans, sections and elevations',
        'A walk-through 3D model of every room',
        'RCC execution from structural drawings',
        'Courtyard planning, jaali screens, stone and board-formed concrete detailing',
        'Interiors and landscape coordinated with the build'])) +
    '''<section class="section"><div class="wrap"><div class="head"><p class="eyebrow">Walk one now</p><h2>Two villas you can <em>step inside</em></h2><p class="lede">Concept models, not built projects. They show the level of detail you get before construction starts.</p></div>
<div class="cards"><a class="card" href="/viewer-jharokha-residence"><span class="im"><img src="/img/m-jharokha.jpg" alt="Jharokha Residence 3D model" width="900" height="506" loading="lazy"></span><span class="tx"><b>Jharokha Residence</b><small>Sandstone jaali and a double-height living room</small><span class="go">Walk through</span></span></a>
<a class="card" href="/viewer-complete-villa"><span class="im"><img src="/img/m-villa.jpg" alt="The Complete Villa 3D model" width="900" height="506" loading="lazy"></span><span class="tx"><b>The Complete Villa</b><small>Furnished interior in walk mode</small><span class="go">Walk through</span></span></a>
<a class="card" href="/3d-project-pages"><span class="im"><img src="/img/c-courtyard.jpg" alt="Sandstone courtyard with a jaali screen, concept render" width="720" height="960" loading="lazy" style="object-position:50% 60%"></span><span class="tx"><b>Courtyard homes</b><small>Jaali light on a shaded court</small><span class="go">More 3D models</span></span></a></div></div></section>''' +
    '''<section class="section"><div class="wrap"><div class="head"><p class="eyebrow">What it costs</p><h2>Package rates for <em>the structure and finishes</em></h2></div>%s<div style="margin-top:22px"><a class="link-arrow" href="/construction-cost-calculator">Estimate your villa %s</a></div></div></section>''' % (rates_block(RATE_NOTE + ' Pools, landscape and interiors are priced on top.'), ARROW),
    faqs=[
        ('Can I see my villa in 3D before it is built?',
         'Yes. Every room is modelled so you can walk through it. Open the <a href="/viewer-jharokha-residence">Jharokha Residence</a> or <a href="/viewer-complete-villa">The Complete Villa</a> to see the level of detail.'),
        ('Do you build courtyard and jaali homes?',
         'Yes: planning around a central court, jaali screens, stone and board-formed concrete, with concept sheets and 3D views before drawings are issued.'),
        ('What does a villa cost per sq ft?',
         'SSR\'s October 2026 package rates run from about ₹1,800 to ₹2,740 per sq ft of built-up area. Pools, landscape and interiors are priced separately. The <a href="/construction-cost-calculator">cost calculator</a> gives a first figure.'),
        ('Do you design the villa as well?',
         'SSR prepares concept plans, sections, elevations and 3D for villa clients, and works with your architect if you already have one.'),
    ]))

# 4 ---------------------------------------------------------------- PMC
PAGES.append(dict(
    path='/project-management-consultancy', crumb='Project control / PMC', topic='Project control / PMC',
    title='PMC & Construction Project Control in Noida, Delhi NCR | SSR Group Civil',
    description='Execution control for developers and societies: BOQ, BBS, pour cards, RFI and NCR registers, firefighting supervision and weekly earned-value reports. A fee, never a margin on materials.',
    service_name='Project management consultancy (PMC)', service_type='Construction project management',
    eyebrow='Project control · PMC', h1='Project control between the drawings <em>and the site</em>',
    lede='An execution-control layer for developers, societies and main contractors. Design stays with your architect; SSR makes sure what is built matches what was drawn, and keeps the record to prove it.',
    hero_img='/img/towers-960.jpg', hero_alt='Residential towers beside a landscaped garden, concept render', hero_cap='Concept render',
    body=two_col('What we control', 'Quantities, quality <em>and time</em>', ticks([
        'BOQ, bar bending schedules and material reconciliation',
        'IS 456 pour cards before every pour',
        'RFI and NCR registers, kept open until closed',
        'Firefighting risers, sprinklers and detection, tested and commissioned',
        'Weekly reports with planned against actual and earned value',
        'A fee as a percentage of project cost or a fixed retainer, never a margin on materials'])) +
    '''<section class="section band" aria-labelledby="tf-h"><div class="wrap">
<p class="eyebrow">From the site</p><h2 id="tf-h" style="margin-top:10px">Apex Aura Society, <em>Tower F</em></h2>
<div class="prose" style="margin-top:18px;max-width:70ch"><p>Shuttering, slab and firefighting supervision on a 22-week programme from April 2026, from excavation and slabs through firefighting risers to testing and commissioning. These are the controls that ran on it.</p></div>
<div class="stats"><div><b>1.8%</b><span>steel wastage, held against the BBS</span></div><div><b>19:00</b><span>GPS-tagged daily report to the project director, every site day</span></div><div><b>22 wk</b><span>programme, slabs to firefighting commissioning</span></div><div><b>Zero</b><span>core cutting: MEP sleeves placed before the pour</span></div></div>
</div></section>''' +
    two_col('What you receive', 'Reports a director <em>can act on</em>', '''<div class="prose"><p>A <b>daily progress report</b> with photographs, manpower and work done, every site day. A <b>weekly progress report</b> with a management dashboard, BOQ-linked activity log, planned against actual, earned value (SPI and CPI), RFI log, NCR register, material reconciliation, risk register, photo log and next week's plan.</p>
<p>Want to see the daily format? Try the <a href="/site-log">free daily progress report tool</a>.</p></div>'''),
    faqs=[
        ('What does a PMC do on a construction site?',
         'A project management consultant controls execution between the approved drawings and the site: quantities, bar bending schedules, pour approvals, quality registers, progress reports and material reconciliation. SSR does not change the design.'),
        ('How is SSR\'s PMC fee charged?',
         'As a percentage of project cost or a fixed retainer, never as a margin on materials, so SSR has no reason to inflate quantities.'),
        ('What reports will we receive?',
         'A daily progress report with photos every site day, and a weekly report with planned against actual, earned value, RFI and NCR registers, material reconciliation and a look-ahead.'),
        ('Do you supervise firefighting work?',
         'Yes. On Apex Aura Society Tower F the scope ran from slabs and shuttering through firefighting risers, sprinklers and detection to testing and commissioning.'),
    ]))

# 5 ---------------------------------------------------------------- firefighting & plumbing
PAGES.append(dict(
    path='/firefighting-plumbing-contractor', crumb='Firefighting & plumbing', topic='Firefighting / plumbing',
    title='Firefighting & Plumbing Contractor in Greater Noida & Delhi NCR | SSR',
    description='Firefighting risers, sprinklers and detection installed, tested and commissioned; concealed CPVC plumbing and drainage with pressure and ponding tests, across Delhi NCR.',
    service_name='Firefighting and plumbing works', service_type='MEP contractor', og_img='/img/towers.jpg',
    eyebrow='Firefighting · plumbing · waterproofing', h1='Firefighting and plumbing, <em>tested before handover</em>',
    lede='The services that fail first are the ones SSR tests hardest: fire risers and sprinklers commissioned, every water line pressure-tested before plaster, and every wet area ponded for 48 hours before tiling.',
    body=two_col('Firefighting', 'Risers, sprinklers <em>and detection</em>', ticks([
        'Firefighting riser pipework to IS 1239',
        'Sprinkler and fire detection systems',
        'Testing and commissioning as part of the scope',
        'Sleeves placed before the pour, so services need no core cutting later',
        'Supervised on Apex Aura Society Tower F, Greater Noida West'])) +
    two_col('Plumbing and waterproofing', 'Concealed, tested, <em>recorded</em>', ticks([
        'Concealed CPVC hot and cold supply, pressure-tested before plaster',
        'SWR drainage stacks, inspection chambers and rainwater down-takes',
        'Polymer waterproofing in toilets, balconies and terraces, with a 48-hour ponding test',
        'Branded pipes and fittings, such as Astral or Ashirvad CPVC and Supreme or Prince SWR',
        'Test results recorded and handed over with the building'])),
    faqs=[
        ('Do you test the firefighting system?',
         'Yes. Risers, sprinklers and detection are tested and commissioned as part of the scope, as on Apex Aura Society Tower F.'),
        ('How do you stop toilets and terraces from leaking?',
         'Polymer-modified waterproofing with upturns at the walls, then a 48-hour ponding test before any tile is laid.'),
        ('Can you take plumbing or firefighting on its own?',
         'Yes. Plumbing and firefighting can be part of a full SSR build or a separate package. Send the drawings and scope on WhatsApp for a price.'),
    ]))

# 6 ---------------------------------------------------------------- 3D pages
PAGES.append(dict(
    path='/3d-project-pages', crumb='3D project pages', topic='3D model page for a project',
    title='3D Walkthroughs & Project Pages for Builders | SSR Group Civil',
    description='Turn drawings or a brochure into an interactive 3D project page with your branding and an enquiry form that sends buyer leads to your WhatsApp. For developers, builders and architects.',
    service_name='3D walkthroughs and project pages', service_type='Architectural visualisation',
    eyebrow='Post your 3D models through SSR Group', h1='Your project as a <em>live 3D page</em>',
    lede='Send the drawings. SSR builds the model, hosts it on a page with your name, and gives you one link for a chat window, a hoarding QR code or a sales office.',
    hero_img='/img/masterplan-960.jpg', hero_alt='Aerial view of a residential masterplan with towers around a central green, generic concept render', hero_cap='Generic concept render',
    body='''<section class="section"><div class="wrap"><div class="head"><p class="eyebrow">How it works</p><h2>Three steps, <em>one link</em></h2></div><ol class="steps">
<li><b>Send what you have</b><p>A brochure, AutoCAD or PDF drawings, a SketchUp file, or a model you already have and only want hosted.</p></li>
<li><b>We build and set it up</b><p>Towers, amenities and homes modelled to the drawing, with an enquiry form that lands on your WhatsApp.</p></li>
<li><b>You share one link</b><p>Hosted on SSR's site or yours, with your branding. It updates when the design changes.</p></li></ol></div></section>''' +
    '''<section class="section"><div class="wrap"><div class="head"><p class="eyebrow">Open one</p><h2>Models SSR has <em>built</em></h2><p class="lede">Concepts and demonstrations unless marked live. Each opens in your browser, on a phone or a laptop.</p></div>
<div class="cards">
<a class="card" href="/viewer-aura01-facade"><span class="im"><img src="/img/aura01-front.jpg" alt="AURA01 façade render" width="1600" height="1200" loading="lazy"></span><span class="tx"><b>AURA01 façade 3D</b><small>Live project · issued façade scheme</small><span class="go">Turn the model</span></span></a>
<a class="card" href="https://claude.ai/artifact/6JNEWYypMZHLZxRCTbofEY" target="_blank" rel="noopener"><span class="im"><img src="/img/splendour-aerial.jpg" alt="Splendour by Apex Floral aerial, artist's impression" width="1264" height="848" loading="lazy"></span><span class="tx"><b>Splendour microsite</b><small>Demonstration by SSR, not the developer's official page</small><span class="go">Open the page</span></span></a>
<a class="card" href="/viewer-jharokha-residence"><span class="im"><img src="/img/m-jharokha.jpg" alt="Jharokha Residence 3D model" width="900" height="506" loading="lazy"></span><span class="tx"><b>Jharokha Residence</b><small>Villa concept · walk every room</small><span class="go">Walk through</span></span></a>
<a class="card" href="/viewer-complete-villa"><span class="im"><img src="/img/m-villa.jpg" alt="The Complete Villa 3D model" width="900" height="506" loading="lazy"></span><span class="tx"><b>The Complete Villa</b><small>Furnished interior · walk mode</small><span class="go">Walk through</span></span></a>
<a class="card" href="/viewer-apex-aura-towers-i-j"><span class="im"><img src="/p-aura-towers-800.jpg" alt="Apex Aura Towers I and J 3D model" width="800" height="450" loading="lazy"></span><span class="tx"><b>Apex Aura Towers I &amp; J</b><small>Tower model</small><span class="go">Open in 3D</span></span></a>
<a class="card" href="/viewer-s4-residence"><span class="im"><img src="/p-s4-residence-800.jpg" alt="S+4 residence 3D model" width="800" height="450" loading="lazy"></span><span class="tx"><b>S+4 Residence</b><small>Builder floor concept, one 3 BHK per floor</small><span class="go">Open in 3D</span></span></a>
<a class="card" href="/viewer-3bhk-interior"><span class="im"><img src="/p-3bhk-interior-800.jpg" alt="3 BHK interior 3D model" width="800" height="450" loading="lazy"></span><span class="tx"><b>3 BHK Interior</b><small>Apartment interior walkthrough</small><span class="go">Walk through</span></span></a>
<a class="card" href="/viewer-sankalp-world-city"><span class="im"><img src="/p-world-city-800.jpg" alt="Sankalp World City 3D master plan" width="800" height="450" loading="lazy"></span><span class="tx"><b>Sankalp World City</b><small>Master-plan concept</small><span class="go">Open in 3D</span></span></a>
<a class="card" href="/viewer-ssr-group-world"><span class="im"><img src="/p-ssr-world-800.jpg" alt="SSR Group World 3D showcase" width="800" height="450" loading="lazy"></span><span class="tx"><b>SSR Group World</b><small>3D showcase</small><span class="go">Open in 3D</span></span></a>
</div></div></section>''' +
    two_col('What a page includes', 'Built to <em>sell homes</em>', ticks([
        'An aerial with tap-to-see amenities',
        'Each home with its plan and interiors',
        'An enquiry form wired to your WhatsApp',
        'One link for chats, QR codes and the sales office',
        'Built from a brochure, drawings, a SketchUp file or an existing model'])),
    faqs=[
        ('What do you need from us to build a 3D project page?',
         'A brochure, AutoCAD or PDF drawings, a SketchUp file, or a model you already have and only want hosted.'),
        ('Where is the page hosted?',
         'On SSR\'s site or yours, with your branding, as one link you can share anywhere.'),
        ('Can buyers enquire from the page?',
         'Yes. The enquiry form sends the buyer\'s details to your WhatsApp.'),
    ]))


def calculator():
    rates_js = json.dumps(RATES)
    body = '''<section class="phero" style="padding-bottom:20px">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">Construction cost calculator</span></nav>
    <div style="max-width:880px;margin-top:22px">
      <p class="eyebrow">Delhi NCR · 2026 rates</p>
      <h1 style="margin-top:12px">What will your building <em>cost?</em></h1>
      <p class="lede">Enter your plot and floors, pick a package, and see an indicative range from SSR's October 2026 rates. Send it on WhatsApp and we turn it into a fixed quote.</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:20px" aria-label="Calculator">
  <div class="wrap calc">
    <form class="calc-in" id="calc" onsubmit="return false">
      <div class="pair">
        <label class="field">Plot size<input id="c-plot" type="number" inputmode="decimal" min="10" step="any" value="100"></label>
        <label class="field">Unit<select id="c-unit"><option value="gaj" selected>sq yd (gaj)</option><option value="sqft">sq ft</option><option value="sqm">sq m</option></select></label>
      </div>
      <fieldset class="opt"><legend>Floors</legend><div class="seg" id="c-floors">
        <button type="button" data-v="1">G</button><button type="button" data-v="2">G+1</button><button type="button" data-v="3">G+2</button><button type="button" data-v="4" aria-pressed="true">G+3</button><button type="button" data-v="5">G+4</button></div></fieldset>
      <label class="field">Covered area on each floor (sq ft)<input id="c-cover" type="number" inputmode="decimal" min="50" step="any"><small class="hint" id="c-cover-hint">Starts at the full plot. Add balconies that project beyond the plot, or reduce it for setbacks.</small></label>
      <label class="check"><input type="checkbox" id="c-mumty" checked> Stair mumty on the roof (adds about 135 sq ft)</label>
      <fieldset class="opt"><legend>Package</legend><div class="pk" id="c-pkg">
        <button type="button" data-v="Essential"><b>Essential</b><span>₹1,800 / sq ft</span><small>Branded economy finishes</small></button>
        <button type="button" data-v="Comfort" aria-pressed="true"><b>Comfort</b><span>₹2,100 / sq ft</span><small>Mid-range finishes and fittings</small></button>
        <button type="button" data-v="Premium"><b>Premium</b><span>₹2,740 / sq ft</span><small>Premium finishes throughout</small></button></div></fieldset>
      <label class="field">Homes to fit out with kitchen, wardrobes and false ceiling<select id="c-int"><option value="0" selected>None</option><option value="1">1 home</option><option value="2">2 homes</option><option value="3">3 homes</option><option value="4">4 homes</option><option value="5">5 homes</option></select><small class="hint">About ₹3.5 lakh per 3 BHK home, from a recent SSR quote.</small></label>
    </form>
    <aside class="calc-out" aria-live="polite">
      <p class="eyebrow">Indicative cost</p>
      <p class="big" id="o-range">—</p>
      <dl class="calc-dl">
        <dt>Built-up area</dt><dd id="o-area">—</dd>
        <dt>Package rate</dt><dd id="o-rate">—</dd>
        <dt>Construction</dt><dd id="o-build">—</dd>
        <dt>Interiors</dt><dd id="o-int">—</dd>
      </dl>
      <div class="always"><b>Every package keeps</b> M25 concrete, Fe500D steel, Seismic Zone IV detailing, waterproofing with a ponding test, RCCB and earthing, and SSR supervision.</div>
      <div class="calc-act"><a class="btn gold" id="o-wa" href="https://wa.me/''' + WA + '''" target="_blank" rel="noopener">''' + WAI + ''' Send this on WhatsApp</a><a class="btn ghost-night" href="#enquire">Get a fixed quote</a></div>
      <p class="calc-fine">Not included: land, map approval fees and labour cess, electricity, water and sewer connections, lift, basement, boundary wall, fans, lights and ACs. Rates are from SSR's October 2026 BOQ and vary with site, soil, design and market prices. This is an estimate, not a quote.</p>
    </aside>
  </div>
</section>
<section class="section"><div class="wrap two-col"><div><p class="eyebrow">How the figure is worked out</p><h2 style="margin-top:10px">Area × rate, <em>nothing hidden</em></h2></div><div class="prose">
<p><b>Built-up area</b> is the covered area on each floor times the number of floors, plus the stair mumty. Balconies count where they are covered and slabbed.</p>
<p><b>Package rates</b> come from SSR's October 2026 bill of quantities for a ground-plus-one home of about 2,000 sq ft: about ₹1,800 per sq ft for Essential, ₹2,100 for Comfort and ₹2,740 for Premium. The range shown is 6% either side.</p>
<p><b>Interiors</b> use the same quote: an L-shaped modular kitchen at ₹1.5 lakh, wardrobes at ₹1.45 lakh and false ceiling at ₹55,000 for a three-bedroom home.</p>
<p>Want to see how SSR builds? Read about <a href="/builder-floor-construction-delhi">builder floors</a>, <a href="/villa-farmhouse-construction">villas</a> or <a href="/flat-interiors-greater-noida-west">flat interiors</a>.</p></div></div></section>'''
    faqs = [
        ('What is the construction cost per sq ft in Delhi NCR in 2026?',
         'At SSR\'s October 2026 rates, about ₹1,800 per sq ft for an Essential finish, ₹2,100 for Comfort and ₹2,740 for Premium, per sq ft of built-up area. Land, approvals, connections and a lift are extra.'),
        ('How much does it cost to build a house on a 100 gaj plot?',
         'A 100 gaj plot is 900 sq ft. Built G+1 that is about 1,800 sq ft plus a stair mumty, which at the Comfort rate comes to roughly ₹41 lakh. Built G+3 it is about 3,600 sq ft plus the mumty, roughly ₹78 lakh. Change the inputs above for your plot.'),
        ('Is the calculator figure a quote?',
         'No. It is an indicative range. SSR gives a fixed quote after a site visit and drawings, with every item priced in a bill of quantities.'),
    ]
    head = '''<style>
.calc{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(20px,3vw,40px);align-items:start}
.calc>*{min-width:0}
.calc-in{background:var(--sheet);border:1px solid var(--line);border-radius:6px;padding:clamp(20px,3vw,32px);display:grid;gap:20px}
.calc-in .hint{font-size:13px;letter-spacing:0;text-transform:none;font-weight:400;color:var(--ink-2)}
.opt{border:0;margin:0;padding:0;min-width:0}
.opt legend{font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--ink-2);padding:0;margin-bottom:8px}
.seg{display:flex;flex-wrap:wrap;gap:8px}
.seg button{flex:1 1 0;min-height:44px;min-width:52px;padding:8px 10px;border:1px solid var(--line);border-radius:4px;background:var(--paper);font-weight:700}
.calc-in .pair{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--sheet);border-color:var(--ink)}
.pk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.pk button{text-align:left;display:grid;gap:2px;padding:12px 14px;border:1px solid var(--line);border-radius:6px;background:var(--paper)}
.pk button b{font-family:var(--display);font-size:22px;font-weight:600;line-height:1.1}
.pk button span{font-weight:700;font-size:14.5px}
.pk button small{font-size:13px;color:var(--ink-2);line-height:1.35}
.pk button[aria-pressed="true"]{border-color:var(--gold);box-shadow:inset 0 0 0 1px var(--gold);background:var(--sheet)}
.check{display:flex;gap:10px;align-items:center;font-size:16px}
.check input{width:20px;height:20px;accent-color:var(--ink)}
.calc-out{position:sticky;top:96px;background:var(--night);color:#EDE8DC;border-radius:6px;padding:clamp(22px,3vw,34px);display:grid;gap:16px}
.calc-out .eyebrow{color:var(--gold-hi)}
.calc-out .big{font-family:var(--display);font-size:clamp(38px,4.6vw,58px);line-height:1;color:#F7F2E6;font-variant-numeric:lining-nums}
.calc-dl{display:grid;grid-template-columns:auto 1fr;gap:8px 20px;margin:0;border-top:1px solid var(--night-line);padding-top:16px;font-size:16px}
.calc-dl dt{color:var(--mist);font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;padding-top:3px}
.calc-dl dd{margin:0;text-align:right;font-variant-numeric:tabular-nums}
.always{font-size:14.5px;color:var(--mist);border-left:2px solid var(--gold-hi);padding-left:12px}
.always b{color:#F7F2E6}
.calc-act{display:flex;flex-wrap:wrap;gap:10px}
.calc-fine{font-size:13px;color:var(--mist)}
@media (max-width:900px){.calc{grid-template-columns:1fr}.calc-out{position:static}}
@media (max-width:560px){.pk{grid-template-columns:1fr}}
</style>'''
    tail = '''<script>
(function () {
  'use strict';
  var RATES = ''' + rates_js + ''', INT = 350000, MUMTY = 135, SPREAD = 0.06;
  var st = { floors: 4, pkg: 'Comfort', coverEdited: false };
  function $(s) { return document.querySelector(s); }
  function inr(n) { return '₹' + Math.round(n).toLocaleString('en-IN'); }
  function lakh(n) { if (n >= 1e7) return '₹' + (n / 1e7).toFixed(2) + ' crore'; return '₹' + (n / 1e5).toFixed(1) + ' lakh'; }
  function plotSqft() {
    var v = parseFloat($('#c-plot').value) || 0, u = $('#c-unit').value;
    return u === 'gaj' ? v * 9 : u === 'sqm' ? v * 10.7639 : v;
  }
  function seg(box, key, after) {
    Array.prototype.forEach.call(box.querySelectorAll('button'), function (b) {
      b.addEventListener('click', function () {
        Array.prototype.forEach.call(box.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        st[key] = key === 'floors' ? Number(b.getAttribute('data-v')) : b.getAttribute('data-v'); calc();
      });
    });
  }
  seg($('#c-floors'), 'floors'); seg($('#c-pkg'), 'pkg');
  function syncCover() { if (!st.coverEdited) $('#c-cover').value = Math.round(plotSqft()); }
  $('#c-plot').addEventListener('input', function () { syncCover(); calc(); });
  $('#c-unit').addEventListener('change', function () { syncCover(); calc(); });
  $('#c-cover').addEventListener('input', function () { st.coverEdited = true; calc(); });
  $('#c-mumty').addEventListener('change', calc);
  $('#c-int').addEventListener('change', calc);
  var fl = ['G', 'G+1', 'G+2', 'G+3', 'G+4'];
  function calc() {
    var cover = parseFloat($('#c-cover').value) || 0;
    var area = cover * st.floors + ($('#c-mumty').checked ? MUMTY : 0);
    var rate = RATES[st.pkg], build = area * rate, homes = Number($('#c-int').value), interiors = homes * INT;
    var lo = build * (1 - SPREAD) + interiors, hi = build * (1 + SPREAD) + interiors;
    if (!(area > 0)) { $('#o-range').textContent = '—'; return; }
    $('#o-range').textContent = lakh(lo) + ' – ' + lakh(hi);
    $('#o-area').textContent = Math.round(area).toLocaleString('en-IN') + ' sq ft';
    $('#o-rate').textContent = st.pkg + ', ' + inr(rate) + ' / sq ft';
    $('#o-build').textContent = lakh(build);
    $('#o-int').textContent = homes ? lakh(interiors) + ' (' + homes + (homes > 1 ? ' homes)' : ' home)') : 'not included';
    var plot = $('#c-plot').value + ' ' + $('#c-unit').options[$('#c-unit').selectedIndex].text;
    var msg = 'Hi Sankalp, I used the cost calculator on ssrgroupcivil.in.\\n\\nPlot: ' + plot + '\\nFloors: ' + fl[st.floors - 1] +
      '\\nBuilt-up area: about ' + Math.round(area).toLocaleString('en-IN') + ' sq ft\\nPackage: ' + st.pkg +
      (homes ? '\\nInteriors: ' + homes + ' home(s)' : '') + '\\nEstimate shown: ' + lakh(lo) + ' to ' + lakh(hi) +
      '\\n\\nPlease send me a fixed quote.\\n\\n(sent from ssrgroupcivil.in)';
    $('#o-wa').href = 'https://wa.me/''' + WA + '''?text=' + encodeURIComponent(msg);
    var f = document.querySelector('form.enq textarea[name=msg]');
    if (f && !f.dataset.touched) f.value = 'Calculator: ' + plot + ', ' + fl[st.floors - 1] + ', about ' + Math.round(area).toLocaleString('en-IN') + ' sq ft, ' + st.pkg + (homes ? ', interiors for ' + homes : '') + '. Estimate ' + lakh(lo) + ' to ' + lakh(hi) + '.';
  }
  var t = document.querySelector('form.enq textarea[name=msg]');
  if (t) t.addEventListener('input', function () { t.dataset.touched = '1'; });
  syncCover(); calc();
})();
</script>'''
    url = BASE + '/construction-cost-calculator'
    schema = [BUSINESS, {
        '@context': 'https://schema.org', '@type': 'WebApplication', 'name': 'House construction cost calculator',
        'url': url, 'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Any',
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'INR'}, 'provider': {'@id': BASE + '/#business'}
    }, {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Construction cost calculator', 'item': url}]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in faqs]}]
    full = body + faq_html(faqs) + enquiry('Construction quote (from the calculator)', heading='Turn the estimate into a <em>fixed quote.</em>',
                                           blurb='Leave your number and the calculator figures go with it. SSR visits the site, reads the drawings and sends a priced bill of quantities.')
    return doc('House Construction Cost Calculator, Delhi NCR 2026 | SSR Group Civil',
               'Estimate the cost to build a house or builder floor in Delhi NCR. Enter plot size and floors, pick Essential, Comfort or Premium, and see an indicative range at SSR\'s 2026 rates.',
               url, '/img/aura01-ref.jpg', schema, header('/construction-cost-calculator'), full, head, tail)


def not_found():
    body = '''<section class="phero night" style="min-height:60vh;display:grid;align-items:center"><div class="wrap" style="max-width:820px">
<p class="eyebrow">Page not found</p><h1 style="margin-top:12px">This page has <em>moved.</em></h1>
<p class="lede">The link may be from our older website. Everything SSR does is a tap away from here.</p>
<div class="actions" style="display:flex;flex-wrap:wrap;gap:12px;margin-top:26px"><a class="btn gold" href="/">Go to the home page</a><a class="btn ghost-night" href="/construction-cost-calculator">Cost calculator</a></div>
<div class="related" style="margin-top:28px">''' + ''.join('<a href="%s" style="background:transparent;color:#F4EEDF;border-color:var(--night-line)">%s</a>' % (h, esc(t)) for h, t in SERVICE_LINKS) + '''</div></div></section>'''
    out = doc('Page not found | SSR Group Civil', 'The page you were looking for has moved.', BASE + '/', '/img/villa-dusk.jpg', [], header(''), body)
    return out.replace('<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex">')


def main():
    written = []
    for p in PAGES:
        fn = p['path'].strip('/') + '.html'
        open(os.path.join(ROOT, fn), 'w', encoding='utf-8').write(page(p))
        written.append(fn)
    open(os.path.join(ROOT, 'construction-cost-calculator.html'), 'w', encoding='utf-8').write(calculator())
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(not_found())
    written += ['construction-cost-calculator.html', '404.html']
    print('\n'.join(written))


if __name__ == '__main__':
    main()
