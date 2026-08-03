#!/usr/bin/env python3
# One-off generator for CYB blog/content pages. Safe to delete after running.
import os, urllib.parse, re, json as _jsonmod

PHONE = "6289670119008"
IG = "https://www.instagram.com/cyb_bali"
DATE = "2026-06-06"

def _json(s): return _jsonmod.dumps(s, ensure_ascii=False)

def wa(msg="Hi CYB! I'd like to book a cut."):
    return "https://wa.me/" + PHONE + "?text=" + urllib.parse.quote(msg)

def enrich(t):
    """Style FAQ answers: gold prices + bold keywords. Schema keeps the plain text."""
    t = re.sub(r'(Rp [\d,]+(?:K)?)', r'<span class="price">\1</span>', t)
    for kw in ["WhatsApp", "travel included", "travel to your door included", "travel to your villa or hotel included"]:
        t = t.replace(kw, f"<strong>{kw}</strong>")
    return t

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#000;--bg-2:#0b0a09;--gold:#c79a5a;--gold-soft:#ddb87e;--sage:#729274;--sage-soft:#8fad91;--cream:#ece5d7;--muted:#8d8579;--line:rgba(199,154,90,.25);--maxw:760px;--f-disp:"Bebas Neue",sans-serif;--f-body:"Archivo",system-ui,sans-serif}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--cream);font-family:var(--f-body);font-size:17px;line-height:1.75;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.eyebrow{font-family:var(--f-body);text-transform:uppercase;letter-spacing:.34em;font-size:.7rem;color:var(--gold);font-weight:600}
header.nav{position:sticky;top:0;z-index:60;background:rgba(0,0,0,.82);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav-in{max-width:1100px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:68px}
.brand{display:flex;align-items:center;gap:11px;font-family:var(--f-disp);font-size:1.6rem;letter-spacing:.2em;color:var(--cream)}
.brand img{width:42px;height:42px;border:1.5px solid var(--gold);border-radius:50%;padding:4px;object-fit:contain}
.nav-cta{background:#25D366;color:#04210f;font-weight:700;padding:10px 18px;border-radius:40px;font-size:.92rem;letter-spacing:.02em}
.post-head{padding:clamp(48px,9vw,92px) 0 10px}
.post-head h1{font-family:var(--f-disp);color:var(--cream);font-weight:400;line-height:1.02;letter-spacing:.02em;font-size:clamp(2.4rem,7vw,4.2rem);margin:12px 0 14px}
.post-head h1 b{color:var(--sage);font-weight:400}
.post-meta{color:var(--muted);font-size:.86rem;letter-spacing:.04em;text-transform:uppercase}
.prose{padding:18px 0 40px}
.prose p{margin:0 0 18px;color:#d8d0c2}
.prose .lead{font-size:1.18rem;color:var(--cream)}
.prose h2{font-family:var(--f-disp);color:var(--sage);font-weight:400;letter-spacing:.03em;font-size:clamp(1.7rem,4.5vw,2.4rem);line-height:1.05;margin:38px 0 14px}
.prose h2 b{color:#fff;font-weight:400}
.prose ul{margin:0 0 18px;padding-left:20px;color:#d8d0c2}
.prose li{margin:0 0 8px}
.prose strong{color:var(--sage-soft);font-weight:700}
.prose a{color:var(--gold-soft);font-weight:600;border-bottom:1px solid var(--line)}
.prose a:hover{color:var(--gold);border-color:var(--gold)}
.ptable{width:100%;border-collapse:collapse;margin:6px 0 24px;font-size:.98rem}
.ptable th,.ptable td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line)}
.ptable th{color:var(--gold);text-transform:uppercase;letter-spacing:.1em;font-size:.74rem}
.ptable td.price{font-family:var(--f-disp);color:var(--gold-soft);font-size:1.3rem;text-align:right;white-space:nowrap}
.ptable td:first-child{color:var(--cream)}
.callout{border:1px solid var(--line);border-radius:16px;background:var(--bg-2);padding:26px;margin:30px 0;text-align:center}
.callout h3{font-family:var(--f-disp);color:var(--sage);font-size:1.7rem;font-weight:400;letter-spacing:.03em;margin-bottom:6px}
.callout p{color:var(--muted);margin-bottom:16px}
.btn{display:inline-flex;align-items:center;gap:10px;padding:14px 26px;border-radius:44px;font-weight:700;letter-spacing:.03em;font-size:1rem;background:#25D366;color:#04210f}
.btn svg{width:20px;height:20px}
.faqs{border-top:1px solid var(--line);padding:34px 0 10px}
.faqs h2{font-family:var(--f-disp);color:var(--sage);font-weight:400;font-size:clamp(1.7rem,4.5vw,2.4rem);margin-bottom:18px}
.faq-item{border:1px solid var(--line);border-radius:14px;background:var(--bg-2);overflow:hidden;margin-bottom:12px}
.faq-item[open]{border-color:rgba(199,154,90,.5)}
.faq-item summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:18px 20px;font-weight:600;color:var(--cream)}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary .ico{flex:0 0 auto;width:20px;height:20px;position:relative}
.faq-item summary .ico::before,.faq-item summary .ico::after{content:"";position:absolute;background:var(--gold);border-radius:2px}
.faq-item summary .ico::before{top:50%;left:0;right:0;height:2px;transform:translateY(-50%)}
.faq-item summary .ico::after{left:50%;top:0;bottom:0;width:2px;transform:translateX(-50%);transition:opacity .3s}
.faq-item[open] summary .ico::after{opacity:0}
.faq-item .a{padding:0 20px 18px;color:var(--muted);line-height:1.65;font-size:.97rem}
.faq-item .a strong{color:var(--sage-soft);font-weight:700}
.faq-item .a .price{color:var(--gold-soft);font-weight:700;white-space:nowrap}
.faq-item .a a{color:var(--gold-soft);font-weight:600;border-bottom:1px solid var(--line)}
.faq-item .a a:hover{color:var(--gold)}
.related{border-top:1px solid var(--line);padding:30px 0;display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center}
.related span{color:var(--muted);font-size:.85rem;text-transform:uppercase;letter-spacing:.1em;width:100%}
.related a{border:1px solid var(--line);border-radius:40px;padding:9px 18px;color:var(--sage-soft);font-size:.92rem}
.related a:hover{border-color:var(--gold);color:var(--gold-soft)}
.cards{padding:14px 0 50px;display:grid;gap:16px}
.card{border:1px solid var(--line);border-radius:16px;background:var(--bg-2);padding:26px;transition:border-color .3s,transform .3s}
.card:hover{border-color:rgba(199,154,90,.55);transform:translateY(-2px)}
.card h2{font-family:var(--f-disp);color:var(--cream);font-weight:400;font-size:1.7rem;letter-spacing:.02em;margin:6px 0 8px;line-height:1.05}
.card p{color:var(--muted);font-size:.97rem}
.card .more{color:var(--gold-soft);font-weight:600;font-size:.9rem;margin-top:12px;display:inline-block}
footer{padding:40px 0;border-top:1px solid var(--line);background:#000}
.foot-in{max-width:1100px;margin:0 auto;padding:0 24px;display:flex;flex-wrap:wrap;gap:18px 26px;align-items:center;justify-content:space-between}
.foot-brand{display:flex;align-items:center;gap:11px;font-family:var(--f-disp);font-size:1.5rem;letter-spacing:.2em;color:var(--cream)}
.foot-brand img{width:46px;height:46px;border:1.5px solid var(--gold);border-radius:50%;padding:4px;object-fit:contain}
.foot-links{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.9rem;color:var(--muted)}
.foot-links a:hover{color:var(--gold-soft)}
.foot-note{width:100%;color:var(--muted);font-size:.82rem;letter-spacing:.05em;border-top:1px solid var(--line);padding-top:16px;margin-top:4px}
"""

WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.82 11.82 0 018.413 3.488 11.82 11.82 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.86 9.86 0 001.51 5.26l-.999 3.648 3.978-1.044zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg>'

CALLOUT = ('<div class="callout"><h3>Call your barber</h3><p>One message and Sunny brings the full barbershop to your villa, hotel or home across Bali.</p>'
           '<a class="btn" href="' + wa() + '" target="_blank" rel="noopener">' + WA_SVG + ' Book on WhatsApp</a></div>')

AREA_LINKS = ('<div class="related"><span>Mobile barber by area</span>'
              '<a href="/canggu/">Canggu</a><a href="/seminyak/">Seminyak</a><a href="/uluwatu/">Uluwatu</a><a href="/ubud/">Ubud</a><a href="/nusa-dua/">Nusa Dua</a></div>')

POSTS = {
  "haircut-prices-bali": {
    "title": "Haircut Prices in Bali (2026): An Honest Guide",
    "h1": "Haircut Prices in <b>Bali</b>",
    "desc": "How much does a haircut cost in Bali in 2026? A clear breakdown of barbershop, salon and mobile barber prices, what's included, and tipping.",
    "read": "4 min read",
    "body": """
<p class="lead">Wondering what a haircut actually costs in Bali? Here's an honest, up-to-date breakdown for 2026, from cheap local shops to mobile barbers who come to your villa.</p>
<h2>How much is a haircut in <b>Bali?</b></h2>
<p>Prices vary massively depending on where you go. As a rough guide for 2026:</p>
<ul>
<li><strong>Local Indonesian barbershop:</strong> Rp 35,000 to 70,000 for a simple cut.</li>
<li><strong>Expat-focused barbershop</strong> (Canggu, Seminyak, Uluwatu): Rp 150,000 to 350,000.</li>
<li><strong>Hotel salon or premium studio:</strong> Rp 300,000 and up.</li>
<li><strong>Mobile barber</strong> (comes to you): mid-to-upper range, because you're paying for a private one-on-one session at your door.</li>
</ul>
<p>The cheap local shops are great value if you want a basic cut and don't mind a language gap. For a proper fade, beard work or a straight-razor finish, the expat-focused and mobile barbers are where the skill and consistency are.</p>
<h2>CYB price list</h2>
<p>CYB is a mobile barber covering Canggu, Seminyak, Uluwatu, Nusa Dua and Ubud. Travel within the service area is included, so the price you see is what you pay:</p>
<table class="ptable"><thead><tr><th>Service</th><th style="text-align:right">Price</th></tr></thead><tbody>
<tr><td>Haircut</td><td class="price">Rp 500K</td></tr>
<tr><td>Beard Trim</td><td class="price">Rp 200K</td></tr>
<tr><td>Full Shave</td><td class="price">Rp 300K</td></tr>
<tr><td>Hair Colour</td><td class="price">From Rp 1M</td></tr>
<tr><td>Hair Perm</td><td class="price">From Rp 1M</td></tr>
</tbody></table>
<h2>What's <b>included?</b></h2>
<p>With a mobile barber, the price should cover travel, setup, the consultation and the cut itself, with no surprise add-ons. At CYB, travel inside the service area is built into the price. Further out, a small extra may apply, which is always agreed before you book.</p>
<h2>Do you tip a barber in Bali?</h2>
<p>Tipping isn't expected in Bali the way it is in the US, but it's always appreciated for a great cut. Rounding up or adding 10 to 20 percent is a friendly gesture, never an obligation.</p>
<h2>Cash or card?</h2>
<p>Most barbershops in Bali take cash, and many now accept QRIS (the local QR payment standard). CYB takes cash or QRIS, settled once your cut is exactly how you want it.</p>
""",
    "faq": [
      ("Is a haircut in Bali cheap?", "It can be. Local barbershops charge as little as Rp 35,000, while expat-focused and mobile barbers charge Rp 150,000 to 350,000 for a more polished cut with consistent results."),
      ("How much is a good fade in Bali?", "For a proper skin fade with a clean line-up, expect Rp 150,000 to 350,000 at a quality barber. CYB charges Rp 500,000 with travel to your villa or hotel included."),
      ("Do mobile barbers cost more?", "Usually a little, because you're getting a private session at your own place with no travel or waiting on your end. With CYB, travel included means no surprise add-ons."),
    ],
  },
  "mobile-barber-bali": {
    "title": "How to Book a Mobile Barber in Bali (Villa & Hotel Haircuts)",
    "h1": "Mobile Barber in <b>Bali</b>",
    "desc": "What a mobile barber in Bali is, how it works, which areas are covered and what you need to set up for a haircut at your villa or hotel.",
    "read": "4 min read",
    "body": """
<p class="lead">A mobile barber brings the whole barbershop to your door: clippers, fresh blades, products and a proper setup, so you get a sharp cut at your villa, hotel or home without leaving. Here's how it works in Bali.</p>
<h2>What is a <b>mobile barber?</b></h2>
<p>Instead of you travelling to a shop, the barber travels to you. They arrive with everything needed, set up in a few minutes, give you the cut, and pack down. It's the same quality as a good barbershop chair, minus the traffic, the queue and the waiting room.</p>
<h2>How does it <b>work?</b></h2>
<ul>
<li><strong>Message:</strong> send one WhatsApp with your service, your location and a preferred time.</li>
<li><strong>We come to you:</strong> your barber arrives on schedule with the full kit.</li>
<li><strong>Fresh cut:</strong> sit back in your own space and pay by cash or QRIS when it's done.</li>
</ul>
<h2>Which areas of Bali are <b>covered?</b></h2>
<p>CYB covers the main expat and visitor areas: <a href="/canggu/">Canggu</a>, <a href="/seminyak/">Seminyak</a>, <a href="/uluwatu/">Uluwatu</a>, <a href="/nusa-dua/">Nusa Dua</a> and <a href="/ubud/">Ubud</a>, plus the surrounding spots. Travel within these areas is included in the price.</p>
<h2>What do you need to set up?</h2>
<p>Not much. A little space, a chair (the barber can advise), and a power point nearby. A terrace, balcony, bathroom or kitchen area all work fine. The barber handles the rest, including cleanup.</p>
<h2>Why it beats a barbershop in Bali</h2>
<p>Bali traffic is the main reason. A 15-minute trip can easily become 45 minutes each way on a scooter in the heat. A mobile barber gives you back that time, plus a private, unhurried session on your own schedule, with your own music going.</p>
""",
    "faq": [
      ("How much does a mobile barber in Bali cost?", "At CYB a men's haircut is Rp 500,000 with travel included, a beard trim is Rp 200,000 and a full straight-razor shave is Rp 300,000."),
      ("Do you bring everything for the haircut?", "Yes. The barber arrives with clippers, scissors, fresh blades, products and everything needed to set up at your villa, hotel or home."),
      ("How do I book a barber to my villa in Bali?", "Send one message on WhatsApp with your service, your address and a preferred time. Same-day appointments are often available."),
    ],
  },
  "barber-canggu-guide": {
    "title": "Getting a Good Haircut in Canggu: A Quick Guide",
    "h1": "A Haircut in <b>Canggu</b>",
    "desc": "How to get a sharp haircut in Canggu as a visitor or new expat, including walk-in shops, booking ahead and the mobile barber option that skips the traffic.",
    "read": "3 min read",
    "body": """
<p class="lead">Finding a good barber in Canggu as a visitor or new expat can be hit or miss. Here's how to get a sharp cut without the guesswork, including the mobile option that skips the traffic entirely.</p>
<h2>The Canggu barber <b>scene</b></h2>
<p>Canggu has gone from a quiet surf village to one of Bali's busiest hubs, and the barber options have grown with it. You'll find everything from Rp 50,000 local shops to polished expat-focused barbershops around Berawa, Batu Bolong and Pererenan.</p>
<h2>Walk-in or book ahead?</h2>
<p>The popular shops get busy, especially in high season, so walk-ins can mean a wait. If your time matters, booking ahead, or having a barber come to you, is the safer bet.</p>
<h2>The mobile option</h2>
<p>If you're staying in a villa or co-living in Canggu, a <a href="/canggu/">mobile barber</a> is hard to beat. No scooter ride down Batu Bolong, no waiting room, just a fresh cut on your own terrace. CYB covers Berawa, Batu Bolong, Pererenan and Echo Beach with travel included.</p>
<h2>What to ask for</h2>
<ul>
<li>Bring a photo. It removes any language gap and gets you exactly the look you want.</li>
<li>Be clear on fade height (low, mid or high) and how much length to keep on top.</li>
<li>Mention your hair type. Bali's humidity changes how some styles sit.</li>
</ul>
""",
    "faq": [
      ("Where can I get a haircut in Canggu?", "You'll find local shops and expat-focused barbershops around Berawa, Batu Bolong and Pererenan. For convenience, CYB is a mobile barber that comes to your villa or hotel anywhere in Canggu."),
      ("How much is a haircut in Canggu?", "Expat-focused barbershops charge around Rp 150,000 to 350,000. CYB charges Rp 500,000 with travel to your door included."),
      ("Can a barber come to my villa in Canggu?", "Yes. CYB covers Berawa, Batu Bolong, Pererenan and Echo Beach. Send one WhatsApp message to book a cut at your place."),
    ],
  },
}

def nav():
    return ('<header class="nav"><div class="nav-in">'
            '<a href="/" class="brand"><img src="/images/cyb-logo.png" alt="CYB mobile barber Bali logo"> CYB</a>'
            '<a href="' + wa() + '" class="nav-cta" target="_blank" rel="noopener">Book now</a>'
            '</div></header>')

def footer():
    return ('<footer><div class="foot-in">'
            '<a href="/" class="foot-brand"><img src="/images/cyb-logo.png" alt="CYB logo"> CYB</a>'
            '<nav class="foot-links"><a href="/">Home</a><a href="/blog/">Journal</a>'
            '<a href="/canggu/">Canggu</a><a href="/seminyak/">Seminyak</a><a href="/uluwatu/">Uluwatu</a>'
            '<a href="/ubud/">Ubud</a><a href="/nusa-dua/">Nusa Dua</a>'
            '<a href="' + IG + '" target="_blank" rel="noopener">Instagram</a></nav>'
            '<small class="foot-note">© 2026 CYB Mobile Barbershop · Bali. Mobile barber across Bali.</small>'
            '</div></footer>')

def head(title, desc, url, og_title):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://cybbali.com/images/og-cover.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/images/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="/images/favicon-48.png">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/images/favicon-180.png">
<meta name="theme-color" content="#0b0a09">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Bebas+Neue&display=swap" rel="stylesheet">"""

def post_page(slug, p):
    url = f"https://cybbali.com/blog/{slug}/"
    faq_html = "".join(
      f'<details class="faq-item"><summary>{q}<span class="ico"></span></summary><div class="a">{enrich(a)}</div></details>' for q,a in p["faq"])
    faq_items = ",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (_json(q),_json(a)) for q,a in p["faq"])
    h1_plain = p["h1"].replace("<b>","").replace("</b>","")
    article_ld = '{"@context":"https://schema.org","@type":"BlogPosting","headline":%s,"description":%s,"datePublished":"%s","dateModified":"%s","image":"https://cybbali.com/images/og-cover.jpg","mainEntityOfPage":"%s","author":{"@type":"Organization","name":"CYB · Call Your Barber"},"publisher":{"@type":"Organization","name":"CYB · Call Your Barber","logo":{"@type":"ImageObject","url":"https://cybbali.com/images/cyb-logo.png"}}}' % (
        _json(h1_plain), _json(p["desc"]), DATE, DATE, url)
    faq_ld = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % faq_items
    breadcrumb = '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://cybbali.com/"},{"@type":"ListItem","position":2,"name":"Journal","item":"https://cybbali.com/blog/"},{"@type":"ListItem","position":3,"name":%s,"item":"%s"}]}' % (_json(h1_plain), url)
    return head(p["title"], p["desc"], url, p["title"]) + f"""
<script type="application/ld+json">{article_ld}</script>
<script type="application/ld+json">{faq_ld}</script>
<script type="application/ld+json">{breadcrumb}</script>
<style>{CSS}</style>
</head>
<body>
{nav()}
<article class="wrap">
  <div class="post-head">
    <a href="/blog/" class="eyebrow">CYB Journal</a>
    <h1>{p['h1']}</h1>
    <div class="post-meta">{p['read']} · Bali</div>
  </div>
  <div class="prose">{p['body']}</div>
  {CALLOUT}
  <div class="faqs"><h2>FAQ</h2>{faq_html}</div>
  {AREA_LINKS}
</article>
{footer()}
</body>
</html>
"""

def index_page():
    url = "https://cybbali.com/blog/"
    cards = ""
    for slug, p in POSTS.items():
        cards += f'<a class="card" href="/blog/{slug}/"><div class="eyebrow">{p["read"]}</div><h2>{p["title"]}</h2><p>{p["desc"]}</p><span class="more">Read more &rarr;</span></a>'
    return head("CYB Journal · Mobile Barber Tips & Bali Haircut Guides",
                "Guides and tips from CYB, a mobile barber in Bali: haircut prices, how mobile barbering works and where to get a good cut.",
                url, "CYB Journal · Bali Barber Guides") + f"""
<style>{CSS}</style>
</head>
<body>
{nav()}
<main class="wrap">
  <div class="post-head">
    <div class="eyebrow">CYB Journal</div>
    <h1>Bali barber <b>guides.</b></h1>
    <div class="post-meta">Tips, prices &amp; how mobile barbering works</div>
  </div>
  <div class="cards">{cards}</div>
  {AREA_LINKS}
</main>
{footer()}
</body>
</html>
"""

ROOT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(ROOT,"blog"), exist_ok=True)
with open(os.path.join(ROOT,"blog","index.html"),"w",encoding="utf-8") as f:
    f.write(index_page())
print("wrote blog/index.html")
for slug,p in POSTS.items():
    folder=os.path.join(ROOT,"blog",slug)
    os.makedirs(folder,exist_ok=True)
    with open(os.path.join(folder,"index.html"),"w",encoding="utf-8") as f:
        f.write(post_page(slug,p))
    print("wrote blog/"+slug+"/index.html")
print("done")
