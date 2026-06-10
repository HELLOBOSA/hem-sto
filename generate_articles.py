#!/usr/bin/env python3
"""Generate 9 new SEO blog articles for Hemreform Göteborg."""

import os
import shutil

TEMPLATE_PATH = '/home/user/hem-got/blogg/badrumsrenovering-goteborg-checklista/index.html'
BLOGG_DIR = '/home/user/hem-got/blogg'
BASE_URL = 'https://goteborg.hemreform.se'

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    TEMPLATE = f.read()

def make_article_block(article):
    """Build the <article class="article"> ... </article> block for an article."""
    a = article

    # Build body sections
    body_sections = ''
    for section in a['body_sections']:
        if section['type'] == 'h2':
            body_sections += f'\n      <h2 data-en="{section["en"]}">{section["sv"]}</h2>'
        elif section['type'] == 'p':
            body_sections += f'\n      <p data-en="{section["en"]}">{section["sv"]}</p>'

    # Build pager
    prev = a['pager_prev']
    nxt = a['pager_next']
    pager = f'''      <nav class="article-pager" aria-label="Artikelnavigering">
        <a href="{prev['url']}"><small data-en="Previous article">Föregående artikel</small><strong data-en="{prev['en']}">{prev['sv']}</strong></a>
        <a href="{nxt['url']}"><small data-en="Next article">Nästa artikel</small><strong data-en="{nxt['en']}">{nxt['sv']}</strong></a>
      </nav>'''

    img_src = a['image_src']
    img_w = a['image_w']
    img_h = a['image_h']
    img_alt_sv = a['image_alt_sv']

    block = f'''<main id="top">
  <article class="article">
    <header class="article-hero wrap">
      <a class="article-back mono" href="/blogg/" data-en="Back to blog">Tillbaka till blogg</a>
      <span class="eyebrow"><span class="tick" aria-hidden="true"></span><span data-en="Guide · Gothenburg">Guide · Göteborg</span></span>
      <h1 data-en="{a['h1_en']}">{a['h1_sv']}</h1>
      <p data-en="{a['intro_en']}">{a['intro_sv']}</p>
      <figure>
        <img src="{img_src}" width="{img_w}" height="{img_h}" alt="{img_alt_sv}" fetchpriority="high">
        <figcaption data-en="Example image from Hemreform project archive.">Exempelbild från Hemreforms projektarkiv.</figcaption>
      </figure>
    </header>
    <div class="article-body wrap">{body_sections}
      <div class="article-cta">
        <h2 data-en="{a['cta_h2_en']}">{a['cta_h2_sv']}</h2>
        <p data-en="{a['cta_p_en']}">{a['cta_p_sv']}</p>
        <a class="btn btn-primary magnetic" href="/#kontakt" data-en="Tell us about your project <span class='arrow'>→</span>">Berätta om ditt projekt <span class="arrow">→</span></a>
      </div>
{pager}
    </div>
  </article>
</main>'''
    return block

def build_page(article):
    a = article
    slug = a['slug']
    canonical = f"{BASE_URL}/blogg/{slug}/"

    # Replace head meta tags
    html = TEMPLATE

    # Title
    html = html.replace(
        '<title>Badrumsrenovering Göteborg: checklista innan start | Hemreform</title>',
        f'<title>{a["title"]}</title>'
    )

    # Meta description
    html = html.replace(
        '<meta name="description" content="Checklista inför badrumsrenovering i Göteborg: budget, ROT, material, tidsplan, offert och vad du bör förbereda innan arbetet startar.">',
        f'<meta name="description" content="{a["meta_desc"]}">'
    )

    # Canonical
    html = html.replace(
        '<link rel="canonical" href="https://goteborg.hemreform.se/blogg/badrumsrenovering-goteborg-checklista/">',
        f'<link rel="canonical" href="{canonical}">'
    )

    # OG url
    html = html.replace(
        '<meta property="og:url" content="https://goteborg.hemreform.se/blogg/badrumsrenovering-goteborg-checklista/">',
        f'<meta property="og:url" content="{canonical}">'
    )

    # OG title
    html = html.replace(
        '<meta property="og:title" content="Badrumsrenovering i Göteborg: checklista innan du börjar">',
        f'<meta property="og:title" content="{a["h1_sv"]}">'
    )

    # OG description
    html = html.replace(
        '<meta property="og:description" content="Checklista inför badrumsrenovering i Göteborg: budget, ROT, material, tidsplan, offert och vad du bör förbereda innan arbetet startar.">',
        f'<meta property="og:description" content="{a["meta_desc"]}">'
    )

    # OG image
    html = html.replace(
        '<meta property="og:image" content="https://goteborg.hemreform.se/images/projekt/apartment-v1-after.webp">',
        f'<meta property="og:image" content="{BASE_URL}{a["image_src"]}">'
    )

    # Schema JSON-LD replacements
    html = html.replace(
        '"headline": "Badrumsrenovering i Göteborg: checklista innan du börjar"',
        f'"headline": "{a["h1_sv"]}"'
    )
    html = html.replace(
        '"description": "Checklista inför badrumsrenovering i Göteborg: budget, ROT, material, tidsplan, offert och vad du bör förbereda innan arbetet startar."',
        f'"description": "{a["meta_desc"]}"'
    )
    html = html.replace(
        '"image": "https://goteborg.hemreform.se/images/projekt/apartment-v1-after.webp"',
        f'"image": "{BASE_URL}{a["image_src"]}"'
    )

    # Schema mainEntityOfPage
    html = html.replace(
        '"mainEntityOfPage": "https://goteborg.hemreform.se/blogg/badrumsrenovering-goteborg-checklista/"',
        f'"mainEntityOfPage": "{canonical}"'
    )

    # Replace the article block
    # Find start and end markers
    start_marker = '<main id="top">'
    end_marker = '<!-- ===== FOOTER ===== -->'
    start_idx = html.index(start_marker)
    end_idx = html.index(end_marker)

    new_article = make_article_block(article)
    html = html[:start_idx] + new_article + '\n' + html[end_idx:]

    return html

# ============================================================
# Article data
# ============================================================

ARTICLES = [

# 1. badrumsrenovering-goteborg-pris
{
    'slug': 'badrumsrenovering-goteborg-pris',
    'title': 'Badrumsrenovering Göteborg pris 2026 | Kostnad & ROT | Hemreform',
    'meta_desc': 'Vad kostar en badrumsrenovering i Göteborg 2026? Prisintervall per storlek, vad som driver kostnaden och hur ROT-avdraget påverkar slutsumman.',
    'h1_sv': 'Vad kostar en badrumsrenovering i Göteborg?',
    'h1_en': 'What does a bathroom renovation cost in Gothenburg?',
    'intro_sv': 'Priset på en badrumsrenovering i Göteborg varierar kraftigt beroende på storlek, befintligt skick och vald standard. Den här guiden ger konkreta prisintervall, förklarar vad som driver kostnaden och visar hur ROT-avdraget 2026 påverkar vad du faktiskt betalar.',
    'intro_en': 'The cost of a bathroom renovation in Gothenburg varies significantly depending on size, existing condition and chosen standard. This guide gives concrete price ranges, explains what drives the cost and shows how the 2026 ROT deduction affects what you actually pay.',
    'image_src': '/images/projekt/apartment-k38-after.webp',
    'image_w': '1800',
    'image_h': '1344',
    'image_alt_sv': 'Renoverat badrum i Göteborg — Apartment K38',
    'body_sections': [
        {'type': 'h2', 'sv': 'Vad kostar ett badrum att renovera i Göteborg?', 'en': 'What does it cost to renovate a bathroom in Gothenburg?'},
        {'type': 'p', 'sv': 'Ett litet badrum på 3–5 kvm kostar normalt 80 000–150 000 kronor vid en grundlig renovering med nytt tätskikt, kakel, golvvärme och ny inredning. Ett mellanstort badrum på 6–10 kvm hamnar ofta på 130 000–250 000 kronor. För ett stort badrum eller om planlösningen ändras kan kostnaden överstiga 300 000 kronor. ROT-avdraget sänker din del av arbetskostnaden med 30 procent.', 'en': 'A small bathroom of 3–5 sqm normally costs 80,000–150,000 kronor for a thorough renovation with new waterproofing, tiles, underfloor heating and new fittings. A medium-sized bathroom of 6–10 sqm typically lands at 130,000–250,000 kronor. For a large bathroom or if the layout changes, costs can exceed 300,000 kronor. The ROT deduction reduces your share of labour costs by 30 percent.'},
        {'type': 'h2', 'sv': 'Vad påverkar priset mest?', 'en': 'What affects the price most?'},
        {'type': 'p', 'sv': 'De faktorer som driver kostnaden uppåt är rivning och bortforsling av gammalt material, VVS-arbete som kräver certifierad rörmokare, el-dragning för värmegolv och spotlights, tätskiktets kvalitet och utförande, kakel- och klinkermaterial, samt inredningsval som badkar kontra dusch och specialanpassad förvaring. Att byta ut befintliga installationer på samma plats är alltid billigare än att flytta dem.', 'en': 'The factors that drive costs up are demolition and removal of old material, plumbing work requiring a certified plumber, electrical work for underfloor heating and spotlights, waterproofing quality and workmanship, tile and stone materials, and fixture choices such as bathtub versus shower and custom storage. Replacing existing installations in the same place is always cheaper than moving them.'},
        {'type': 'h2', 'sv': 'Hur fungerar ROT-avdraget för badrum 2026?', 'en': 'How does the ROT deduction work for bathrooms in 2026?'},
        {'type': 'p', 'sv': 'ROT-avdraget innebär att du drar av 30 procent av arbetskostnaden direkt på fakturan. Du betalar alltså bara 70 procent av arbetet. Materialkostnaden och resekostnaden ingår inte i ROT. Maxbeloppet för ROT är 50 000 kronor per person och år. Hemreform ansöker om avdraget hos Skatteverket — du behöver inte göra något extra.', 'en': 'The ROT deduction means you deduct 30 percent of the labour cost directly from the invoice. You therefore only pay 70 percent of the labour. Material costs and travel costs are not included in ROT. The maximum ROT amount is 50,000 kronor per person per year. Hemreform applies for the deduction with the Swedish Tax Agency — you do not need to do anything extra.'},
        {'type': 'h2', 'sv': 'Tidsplan för en badrumsrenovering', 'en': 'Timeline for a bathroom renovation'},
        {'type': 'p', 'sv': 'En normal badrumsrenovering tar 2–4 veckor beroende på badrummets storlek och projektets komplexitet. Rivning och förberedelse tar 1–3 dagar, tätskikt och installationer tar 3–7 dagar, kakling tar 3–5 dagar och avslutande inredning och besiktning tar 1–2 dagar. Räkna alltid in några dagar för leveranstider på material och ev. VVS-bokningar.', 'en': 'A normal bathroom renovation takes 2–4 weeks depending on size and project complexity. Demolition and preparation takes 1–3 days, waterproofing and installations take 3–7 days, tiling takes 3–5 days and finishing and inspection take 1–2 days. Always allow a few days for material delivery times and any plumbing bookings.'},
        {'type': 'h2', 'sv': 'Vanliga frågor om badrumsrenovering i Göteborg', 'en': 'Common questions about bathroom renovation in Gothenburg'},
        {'type': 'p', 'sv': 'Behöver jag lämna lägenheten? Normalt sett inte. De flesta badrumsrenoveringar sker utan att du behöver flytta ut, men du kan behöva klara dig utan bad/dusch i 1–2 veckor. Vilka intyg ska jag begära? Be alltid om dokumentation av tätskiktet, VVS-intyg och elbesiktning. Behöver jag styrelsens tillstånd? I en bostadsrätt krävs oftast styrelsens godkännande för ingrepp i VVS och el. Kontakta din BRF i god tid.', 'en': 'Do I need to leave the apartment? Normally not. Most bathroom renovations happen without you moving out, but you may need to manage without bath or shower for 1–2 weeks. What certificates should I request? Always ask for waterproofing documentation, plumbing certificate and electrical inspection. Do I need board approval? In a housing cooperative a board decision is usually required for plumbing and electrical work. Contact your BRF well in advance.'},
    ],
    'cta_h2_sv': 'Planerar du badrumsrenovering i Göteborg?',
    'cta_h2_en': 'Planning a bathroom renovation in Gothenburg?',
    'cta_p_sv': 'Skicka en kort beskrivning och gärna några bilder. Vi återkommer med prisindikation och nästa steg.',
    'cta_p_en': 'Send a short description and some photos. We will get back to you with a price indication and next steps.',
    'pager_prev': {'url': '/blogg/badrumsrenovering-goteborg-checklista/', 'sv': 'Badrumsrenovering i Göteborg: checklista innan du börjar', 'en': 'Bathroom renovation in Gothenburg: checklist before you start'},
    'pager_next': {'url': '/blogg/koksrenovering-goteborg-pris/', 'sv': 'Köksrenovering i Göteborg: pris, materialval och smart budget 2026', 'en': 'Kitchen renovation in Gothenburg: price, materials and smart budget 2026'},
},

# 2. koksrenovering-goteborg-pris
{
    'slug': 'koksrenovering-goteborg-pris',
    'title': 'Köksrenovering Göteborg pris 2026 | Kostnad & budgettips | Hemreform',
    'meta_desc': 'Prisguide för köksrenovering i Göteborg. Jämför budget, standard och platsbyggda lösningar samt vad el, VVS och material påverkar slutkostnaden.',
    'h1_sv': 'Köksrenovering i Göteborg: pris, materialval och smart budget',
    'h1_en': 'Kitchen renovation in Gothenburg: price, materials and smart budget',
    'intro_sv': 'En köksrenovering i Göteborg kan kosta allt från 60 000 kronor för en kosmetisk uppfräschning till över 400 000 kronor för ett helt nytt kök med platsbyggda lösningar. Den här guiden ger dig konkreta prisintervall och hjälper dig att förstå vad som driver kostnaden.',
    'intro_en': 'A kitchen renovation in Gothenburg can cost anything from 60,000 kronor for a cosmetic refresh to over 400,000 kronor for a completely new kitchen with custom-built solutions. This guide gives you concrete price ranges and helps you understand what drives the cost.',
    'image_src': '/images/projekt/apartment-k12.webp',
    'image_w': '1800',
    'image_h': '798',
    'image_alt_sv': 'Renoverat kök i Göteborg — Apartment K12',
    'body_sections': [
        {'type': 'h2', 'sv': 'Vad kostar en köksrenovering i Göteborg?', 'en': 'What does a kitchen renovation cost in Gothenburg?'},
        {'type': 'p', 'sv': 'En kosmetisk uppfräschning med nya luckor, bänkskiva och vitvaror kostar 60 000–120 000 kronor. En standardrenovering med nya stommar, installationer och moderna vitvaror hamnar på 120 000–250 000 kronor. Ett platsbyggt kök eller en köksrenovering med ändrad planlösning kan kosta 250 000–500 000 kronor eller mer. ROT-avdraget sänker din andel av arbetskostnaden med 30 procent.', 'en': 'A cosmetic refresh with new cabinet fronts, worktop and appliances costs 60,000–120,000 kronor. A standard renovation with new frames, installations and modern appliances lands at 120,000–250,000 kronor. A custom-built kitchen or a renovation with a changed layout can cost 250,000–500,000 kronor or more. The ROT deduction reduces your share of labour costs by 30 percent.'},
        {'type': 'h2', 'sv': 'Vad är skillnaden mellan luckbyte och fullrenovering?', 'en': 'What is the difference between replacing doors and a full renovation?'},
        {'type': 'p', 'sv': 'Att byta luckor och bänkskiva är snabbaste sättet att förnya ett kök utan att röra stommarna. Det tar normalt 2–5 dagar och ger ett dramatiskt visuellt lyft till en bråkdel av priset. En fullrenovering innebär att stommarna rivs och allt byggs nytt, vilket ger möjlighet att ändra layout, flytta el och VVS och optimera förvaringen. Det tar 3–6 veckor men ger ett kök som är anpassat exakt efter din tillvaro.', 'en': 'Replacing doors and worktops is the fastest way to renew a kitchen without touching the frames. It normally takes 2–5 days and gives a dramatic visual lift at a fraction of the cost. A full renovation means the frames are torn out and everything is built new, giving the opportunity to change layout, move electrical and plumbing and optimise storage. It takes 3–6 weeks but gives a kitchen tailored exactly to your life.'},
        {'type': 'h2', 'sv': 'Vad kostar mest — material eller arbete?', 'en': 'What costs most — materials or labour?'},
        {'type': 'p', 'sv': 'I ett mellankvalitetskök är arbete och material ungefär lika dyra. Materialkostnaden stiger snabbt vid val av natursten som bänkskiva, inbyggda vitvaror och specialbeslag. Arbetet kostar mer om el och VVS behöver dras om, om köksön kräver ny ventilation eller om det finns fuktskador att sanera. En snickare, elektriker och VVS-firma behövs ofta i samma projekt — Hemreform samordnar alla yrkesgrupper.', 'en': 'In a mid-quality kitchen, labour and materials are roughly equally expensive. Material costs rise quickly with natural stone worktops, integrated appliances and custom hardware. Labour costs more if electrical and plumbing need rerouting, if a kitchen island requires new ventilation or if there is moisture damage to remediate. A carpenter, electrician and plumber are often needed in the same project — Hemreform coordinates all trades.'},
        {'type': 'h2', 'sv': 'Platsbyggt kök — när är det värt det?', 'en': 'Custom-built kitchen — when is it worth it?'},
        {'type': 'p', 'sv': 'Platsbyggda kök passar när standardmåtten inte passar — i landshövdingehus med snedväggar, i äldre lägenheter med oregelbundna mått eller när du vill utnyttja varje centimeter. Det är också det bästa alternativet när du vill ha ett genomgående formspråk som löper från kök till matplats och hall. Hemreform tillverkar och monterar platsbyggda köksmoduler direkt i din bostad i Göteborg.', 'en': 'Custom-built kitchens are suitable when standard measurements do not fit — in landshövdingehus with slanted walls, in older apartments with irregular dimensions or when you want to use every centimetre. It is also the best option when you want a consistent design language running from kitchen to dining area and hallway. Hemreform manufactures and installs custom kitchen modules directly in your home in Gothenburg.'},
        {'type': 'h2', 'sv': 'Vanliga frågor om köksrenovering', 'en': 'Common questions about kitchen renovation'},
        {'type': 'p', 'sv': 'Kan jag bo kvar under renoveringen? Ja, i de flesta fall. Förvänta dig några veckor utan ett fullt fungerande kök. Behöver jag bygglov? Nej, i normalfallet krävs inget bygglov för en köksrenovering. Om du ändrar ventilationen eller gör större planlösningsförändringar kan en anmälan behövas. Hur länge håller ett renoverat kök? Med bra material och korrekt utfört arbete håller ett kök 20–30 år.', 'en': 'Can I stay during the renovation? Yes, in most cases. Expect a few weeks without a fully functional kitchen. Do I need a building permit? No, normally no permit is required for a kitchen renovation. If you change the ventilation or make major layout changes an application may be needed. How long does a renovated kitchen last? With good materials and correctly executed work a kitchen lasts 20–30 years.'},
    ],
    'cta_h2_sv': 'Planerar du köksrenovering i Göteborg?',
    'cta_h2_en': 'Planning a kitchen renovation in Gothenburg?',
    'cta_p_sv': 'Berätta om ditt kök och vad du vill förändra. Vi återkommer med råd och prisindikation.',
    'cta_p_en': 'Tell us about your kitchen and what you want to change. We will get back to you with advice and a price indication.',
    'pager_prev': {'url': '/blogg/badrumsrenovering-goteborg-pris/', 'sv': 'Vad kostar en badrumsrenovering i Göteborg?', 'en': 'What does a bathroom renovation cost in Gothenburg?'},
    'pager_next': {'url': '/blogg/lagenhetsrenovering-goteborg/', 'sv': 'Lägenhetsrenovering i Göteborg: kostnad, tidsplan och BRF-regler', 'en': 'Apartment renovation in Gothenburg: cost, timeline and BRF rules'},
},

# 3. lagenhetsrenovering-goteborg
{
    'slug': 'lagenhetsrenovering-goteborg',
    'title': 'Lägenhetsrenovering Göteborg | Pris, BRF-regler & tidsplan | Hemreform',
    'meta_desc': 'Planerar du lägenhetsrenovering i Göteborg? Läs om kostnad, steg, BRF-godkännande, tidsplan och vanliga misstag innan du tar in offert.',
    'h1_sv': 'Lägenhetsrenovering i Göteborg: kostnad, tidsplan och BRF-regler',
    'h1_en': 'Apartment renovation in Gothenburg: cost, timeline and BRF rules',
    'intro_sv': 'Att renovera en lägenhet i Göteborg kräver planering på tre nivåer: budget och materialval, en realistisk tidsplan och förståelse för de regler som gäller i din bostadsrättsförening. Den här guiden täcker alla tre.',
    'intro_en': 'Renovating an apartment in Gothenburg requires planning at three levels: budget and material choices, a realistic timeline and an understanding of the rules in your housing cooperative. This guide covers all three.',
    'image_src': '/images/projekt/apartment-a75-after.webp',
    'image_w': '1800',
    'image_h': '1263',
    'image_alt_sv': 'Renoverad lägenhet i Göteborg — Apartment A75',
    'body_sections': [
        {'type': 'h2', 'sv': 'Vad kostar en lägenhetsrenovering i Göteborg?', 'en': 'What does an apartment renovation cost in Gothenburg?'},
        {'type': 'p', 'sv': 'En ytskiktsrenovering med nya golv, målade väggar och ny belysning kostar 80 000–180 000 kronor för en typisk 3:a. Lägger du till nytt kök hamnar du på 200 000–350 000 kronor. En hel lägenhet med badrum, kök, ytskikt och förvaring kostar typiskt 350 000–700 000 kronor. ROT-avdraget ger 30 procent av arbetskostnaden tillbaka, vilket kan innebära besparingar på 40 000–120 000 kronor beroende på projektets storlek.', 'en': 'A surface renovation with new floors, painted walls and new lighting costs 80,000–180,000 kronor for a typical 3-room apartment. Adding a new kitchen brings the total to 200,000–350,000 kronor. A full apartment with bathroom, kitchen, surfaces and storage typically costs 350,000–700,000 kronor. The ROT deduction gives back 30 percent of labour costs, potentially saving 40,000–120,000 kronor depending on project size.'},
        {'type': 'h2', 'sv': 'Vad behöver BRF-styrelsen godkänna?', 'en': 'What does the BRF board need to approve?'},
        {'type': 'p', 'sv': 'De flesta ytskiktsåtgärder — målning, tapetsering och golvbyte — kräver inget styrelsegodkännande. Ingrepp i VVS och el, ändringar av bärande konstruktion, installation av golvvärme via vatten och arbeten i våtrum kräver däremot tillstånd från styrelsen. Kontakta din BRF i god tid och lämna in en skriftlig ansökan med arbetsbeskrivning och tidsplan. Det kan ta 2–4 veckor att få svar.', 'en': 'Most surface work — painting, wallpapering and floor replacement — requires no board approval. Work involving plumbing and electrical, changes to load-bearing structures, installation of hydronic underfloor heating and work in wet rooms requires board permission. Contact your BRF well in advance and submit a written application with work description and timeline. It may take 2–4 weeks to receive a response.'},
        {'type': 'h2', 'sv': 'Hur planerar du tidsplanen rätt?', 'en': 'How do you plan the timeline correctly?'},
        {'type': 'p', 'sv': 'En hel lägenhetsrenovering tar vanligtvis 6–14 veckor beroende på projektets storlek. Börja med rivning och VVS-arbeten, sedan el, sedan badrum och kök och avsluta med ytskikt och måleri. Att göra allt i rätt ordning sparar tid och minimerar omarbeten. Räkna med extra tid för materialbeställningar, BRF-handläggning och eventuella fuktmätningar.', 'en': 'A complete apartment renovation typically takes 6–14 weeks depending on project size. Start with demolition and plumbing, then electrical, then bathroom and kitchen and finish with surfaces and painting. Doing everything in the right order saves time and minimises rework. Allow extra time for material orders, BRF processing and any moisture measurements.'},
        {'type': 'h2', 'sv': 'Vilka delar ger mest värde?', 'en': 'Which parts give the most value?'},
        {'type': 'p', 'sv': 'Badrum och kök ger störst effekt på bostadens marknads- och brukvärde. Nya golv och målade väggar ger mest visuell effekt per investerad krona. Platsbyggd förvaring i hall och sovrum är ett ofta underskattat tillskott — i Göteborgs äldre lägenheter med oregelbundna mått är det ibland det enda som ger ett riktigt bra resultat.', 'en': 'Bathroom and kitchen have the greatest impact on the property\'s market and use value. New floors and painted walls give the most visual impact per invested krona. Custom-built storage in the hallway and bedroom is an often underestimated addition — in Gothenburg\'s older apartments with irregular dimensions it is sometimes the only solution that gives a truly good result.'},
        {'type': 'h2', 'sv': 'Vanliga misstag vid lägenhetsrenovering', 'en': 'Common mistakes in apartment renovation'},
        {'type': 'p', 'sv': 'De vanligaste misstagen är: att starta utan styrelsegodkännande och sedan behöva riva arbeten, att underskatta rivningstiden i äldre byggnader, att inte boka elektriker och VVS i god tid (de har ofta lång leveranstid), att välja material utan att kontrollera leveranstider och att glömma att dokumentera arbeten i våtrum och el för framtida försäljning.', 'en': 'The most common mistakes are: starting without board approval and then having to tear out work, underestimating demolition time in older buildings, not booking electricians and plumbers well in advance (they often have long lead times), choosing materials without checking delivery times and forgetting to document work in wet rooms and electrical for future resale.'},
    ],
    'cta_h2_sv': 'Planerar du lägenhetsrenovering i Göteborg?',
    'cta_h2_en': 'Planning an apartment renovation in Gothenburg?',
    'cta_p_sv': 'Berätta vad du vill förändra — ytskikt, kök, badrum eller en helrenovering. Vi återkommer med en plan och prisindikation.',
    'cta_p_en': 'Tell us what you want to change — surfaces, kitchen, bathroom or a full renovation. We will get back to you with a plan and price indication.',
    'pager_prev': {'url': '/blogg/koksrenovering-goteborg-pris/', 'sv': 'Köksrenovering i Göteborg: pris, materialval och smart budget', 'en': 'Kitchen renovation in Gothenburg: price, materials and smart budget'},
    'pager_next': {'url': '/blogg/totalrenovering-goteborg-pris/', 'sv': 'Totalrenovering i Göteborg: pris per kvm, process och vanliga misstag', 'en': 'Total renovation in Gothenburg: price per sqm, process and common mistakes'},
},

# 4. totalrenovering-goteborg-pris
{
    'slug': 'totalrenovering-goteborg-pris',
    'title': 'Totalrenovering Göteborg | Pris per kvm & process | Hemreform',
    'meta_desc': 'Så planerar du en totalrenovering i Göteborg. Se pris per kvm, process, tidslinje och vilka kostnadsfällor du bör undvika.',
    'h1_sv': 'Totalrenovering i Göteborg: pris per kvm, process och vanliga misstag',
    'h1_en': 'Total renovation in Gothenburg: price per sqm, process and common mistakes',
    'intro_sv': 'En totalrenovering i Göteborg innebär att bostaden eller lokalen renoveras från grunden — badrum, kök, ytskikt, förvaring, el och VVS i ett sammanhängande projekt. Det kräver noggrann planering, rätt yrkeskompetens och en tydlig projektstyrning.',
    'intro_en': 'A total renovation in Gothenburg means the property is renovated from scratch — bathroom, kitchen, surfaces, storage, electrical and plumbing in one cohesive project. It requires careful planning, the right professional expertise and clear project management.',
    'image_src': '/images/projekt/villa-boa-after.webp',
    'image_w': '1800',
    'image_h': '1004',
    'image_alt_sv': 'Totalrenovering i Göteborg — Villa Boa',
    'body_sections': [
        {'type': 'h2', 'sv': 'Vad kostar en totalrenovering per kvm i Göteborg?', 'en': 'What does a total renovation cost per sqm in Gothenburg?'},
        {'type': 'p', 'sv': 'En totalrenovering av en lägenhet kostar normalt 8 000–20 000 kronor per kvm beroende på standard, byggnadens ålder och projektets komplexitet. En enklare renovering av en modern lägenhet hamnar i det lägre intervallet. En renovering av ett äldre landshövdingehus med fuktskador, gamla installationer och kulturhistoriska krav kan hamna i det övre. En villa med tillbyggnad och nytt kök och badrum kostar typiskt 2–5 miljoner kronor totalt.', 'en': 'A total apartment renovation normally costs 8,000–20,000 kronor per sqm depending on standard, building age and project complexity. A simpler renovation of a modern apartment lands in the lower range. Renovating an older landshövdingehus with moisture damage, old installations and heritage requirements can land in the upper range. A house with extension and new kitchen and bathroom typically costs 2–5 million kronor in total.'},
        {'type': 'h2', 'sv': 'Hur fungerar processen för en totalrenovering?', 'en': 'How does the process work for a total renovation?'},
        {'type': 'p', 'sv': 'En bra totalrenovering börjar alltid med en grundlig besiktning och projektering. Hemreform genomför ett platsbesök, identifierar dolda problem och lämnar en offert som täcker hela projektet. Sedan koordineras alla yrkesgrupper — snickare, elektriker, VVS, målare och vid behov arkitekt och inredningsarkitekt — i rätt ordning. Du har en kontakt hela vägen.', 'en': 'A good total renovation always starts with a thorough inspection and planning. Hemreform conducts a site visit, identifies hidden problems and submits a quote covering the entire project. All trades are then coordinated — carpenter, electrician, plumber, painter and if needed architect and interior designer — in the right order. You have one contact throughout.'},
        {'type': 'h2', 'sv': 'Vilka kostnadsfällor ska du undvika?', 'en': 'What cost traps should you avoid?'},
        {'type': 'p', 'sv': 'De vanligaste kostnadsfällorna är: att låsa materialval för sent (leveranstider påverkar hela tidsplanen), att inte besikta ordentligt innan start (dolda fuktskador och asbest är vanligt i äldre Göteborgsbyggnader), att inte ha en tydlig ansvarsfördelning mellan hantverkarna, att sakna en byggledare som håller ihop projektet och att inte budgetera 10–15 procent för oförutsedda kostnader.', 'en': 'The most common cost traps are: locking material choices too late (delivery times affect the entire timeline), not inspecting properly before start (hidden moisture damage and asbestos is common in older Gothenburg buildings), not having clear responsibility allocation between trades, lacking a site manager to coordinate the project and not budgeting 10–15 percent for unforeseen costs.'},
        {'type': 'h2', 'sv': 'När behövs arkitekt eller inredningsarkitekt?', 'en': 'When do you need an architect or interior designer?'},
        {'type': 'p', 'sv': 'För en totalrenovering som involverar planlösningsändringar, fasadarbeten, tillbyggnader eller kulturhistoriskt känsliga miljöer är en arkitekt ofta ett krav snarare än ett val. Hemreform samarbetar med registrerade arkitekter (SAR/MSA) och inredningsdesigners och kopplar in rätt kompetens när projektet kräver det — utan att du behöver hitta och samordna dem själv.', 'en': 'For a total renovation involving layout changes, facade work, extensions or historically sensitive environments an architect is often a requirement rather than a choice. Hemreform collaborates with registered architects (SAR/MSA) and interior designers and brings in the right expertise when the project requires it — without you having to find and coordinate them yourself.'},
        {'type': 'h2', 'sv': 'Hur lång tid tar en totalrenovering?', 'en': 'How long does a total renovation take?'},
        {'type': 'p', 'sv': 'En lägenhet på 70–100 kvm tar normalt 10–20 veckor för en fullständig renovering. En villa på 150–200 kvm tar 16–30 veckor beroende på projektets komplexitet. Räkna in 2–4 veckor för projektering och planering innan bygget börjar. En realistisk tidsplan som tar höjd för leveranstider, styrelsebeslut och oförutsedda arbeten är alltid bättre än en optimistisk plan som spricker.', 'en': 'An apartment of 70–100 sqm normally takes 10–20 weeks for a complete renovation. A house of 150–200 sqm takes 16–30 weeks depending on project complexity. Allow 2–4 weeks for planning and design before construction begins. A realistic timeline that accounts for delivery times, board decisions and unforeseen work is always better than an optimistic plan that breaks.'},
    ],
    'cta_h2_sv': 'Planerar du en totalrenovering i Göteborg?',
    'cta_h2_en': 'Planning a total renovation in Gothenburg?',
    'cta_p_sv': 'Kontakta oss för ett första samtal och platsbesök. Vi identifierar vad projektet kräver och lämnar ett heltäckande prisunderlag.',
    'cta_p_en': 'Contact us for an initial conversation and site visit. We identify what the project requires and submit a comprehensive price proposal.',
    'pager_prev': {'url': '/blogg/lagenhetsrenovering-goteborg/', 'sv': 'Lägenhetsrenovering i Göteborg: kostnad, tidsplan och BRF-regler', 'en': 'Apartment renovation in Gothenburg: cost, timeline and BRF rules'},
    'pager_next': {'url': '/blogg/bygglov-renovering-goteborg/', 'sv': 'Behöver du bygglov eller anmälan vid renovering i Göteborg?', 'en': 'Do you need a building permit or notification for renovation in Gothenburg?'},
},

# 5. bygglov-renovering-goteborg
{
    'slug': 'bygglov-renovering-goteborg',
    'title': 'Bygglov eller anmälan vid renovering i Göteborg? | Hemreform',
    'meta_desc': 'Behöver du bygglov eller anmälan vid renovering i Göteborg? Vi går igenom planlösning, bärande väggar, ventilation, VVS och startbesked.',
    'h1_sv': 'Behöver du bygglov eller anmälan vid renovering i Göteborg?',
    'h1_en': 'Do you need a building permit or notification for renovation in Gothenburg?',
    'intro_sv': 'Många renoveringsåtgärder i Göteborg kräver varken bygglov eller anmälan — men vissa ingrepp gör det. Att förstå skillnaden kan spara dig tid, pengar och juridiska problem. Den här guiden ger ett klart beslutsunderlag.',
    'intro_en': 'Many renovation measures in Gothenburg require neither a building permit nor a notification — but some do. Understanding the difference can save you time, money and legal problems. This guide gives clear decision-making guidance.',
    'image_src': '/images/projekt/norrsken-office-after.webp',
    'image_w': '1800',
    'image_h': '982',
    'image_alt_sv': 'Kommersiell renovering i Göteborg — Norrsken Office',
    'body_sections': [
        {'type': 'h2', 'sv': 'När behövs inget tillstånd alls?', 'en': 'When is no permit needed at all?'},
        {'type': 'p', 'sv': 'Du behöver normalt ingen anmälan för: målning, tapetsering och golvbyte inomhus, utbyte av vitvaror och fast inredning på samma plats, ytskiktsrenovering i badrum med nya kakel och klinker (om VVS-installationerna inte flyttas), utbyte av fönster och dörrar mot likvärdiga, byte av köksluckor och bänkskiva utan att röra installationerna.', 'en': 'You normally need no notification for: indoor painting, wallpapering and floor replacement, replacing appliances and fixed fittings in the same place, surface renovation in bathrooms with new tiles (if plumbing installations are not moved), replacing windows and doors with equivalent ones, replacing kitchen doors and worktops without touching the installations.'},
        {'type': 'h2', 'sv': 'När krävs en anmälan till Göteborg stads stadsbyggnadsförvaltning?', 'en': 'When is a notification to Gothenburg\'s city planning department required?'},
        {'type': 'p', 'sv': 'En anmälan — inte bygglov — krävs vid: rivning av bärande konstruktion (pelare, bjälklag, bärande väggar), installation eller ändring av ventilationssystem, ändring av vatten- och avloppsledningar i fastigheten, installation av eldstad eller rökkanal och ändring av planlösning som påverkar brandceller. Vid godkänd anmälan utfärdas ett startbesked — arbetet får inte påbörjas dessförinnan.', 'en': 'A notification — not a building permit — is required when: demolishing load-bearing structures (columns, floor beams, load-bearing walls), installing or modifying ventilation systems, changing water and drain pipes in the property, installing a fireplace or flue and changing floor plans that affect fire compartments. When notification is approved a start notice is issued — work may not begin before then.'},
        {'type': 'h2', 'sv': 'När behövs ett fullständigt bygglov?', 'en': 'When is a full building permit needed?'},
        {'type': 'p', 'sv': 'Ett bygglov krävs vid åtgärder som ändrar byggnadens yttre utseende i ett detaljplanelagt område, tillbyggnader som ökar byggnadsarean, ändring av byggnadstyp (t.ex. från bostad till lokal), nybyggnation och vid fasadändringar i känsliga kulturhistoriska miljöer. I Göteborgs innerstad och i landshövdingehuskvarter gäller ofta utökade krav.', 'en': 'A building permit is required when measures change the building\'s exterior appearance in a detailed plan area, extensions increasing the floor area, changes of building type (e.g. from residential to commercial), new construction and facade changes in sensitive heritage environments. In Gothenburg\'s inner city and landshövdingehus blocks, extended requirements often apply.'},
        {'type': 'h2', 'sv': 'Vad gäller i en bostadsrättsförening?', 'en': 'What applies in a housing cooperative?'},
        {'type': 'p', 'sv': 'Utöver kommunens krav tillkommer BRF-styrelsens egna regler. Styrelsen har rätt att kräva tillstånd för arbeten som berör husets gemensamma delar — stammar, stegar, ventilationskanaler och bärande konstruktion. Kontakta alltid styrelsen skriftligen i god tid innan du påbörjar en renovering som berör VVS, el eller konstruktion.', 'en': 'In addition to the municipality\'s requirements come the BRF board\'s own rules. The board has the right to require permission for work affecting the building\'s common parts — pipes, ladders, ventilation ducts and load-bearing structures. Always contact the board in writing well in advance before starting a renovation affecting plumbing, electrical or structure.'},
        {'type': 'h2', 'sv': 'Hur ansöker du om bygglov eller anmälan i Göteborg?', 'en': 'How do you apply for a building permit or notification in Gothenburg?'},
        {'type': 'p', 'sv': 'Ansökan görs via Göteborgs Stads e-tjänst för bygglov. Du behöver oftast bifoga situationsplan, fasadritningar och planritningar. Handläggningstiden är normalt 4–10 veckor för ett bygglov och 2–4 veckor för en anmälan. Hemreform kan hjälpa till med dokumentationen och koordinera ansökan som en del av projektet.', 'en': 'Applications are made through Gothenburg City\'s e-service for building permits. You normally need to attach a site plan, facade drawings and floor plans. Processing time is normally 4–10 weeks for a building permit and 2–4 weeks for a notification. Hemreform can assist with documentation and coordinate the application as part of the project.'},
    ],
    'cta_h2_sv': 'Osäker på vad som gäller för ditt projekt?',
    'cta_h2_en': 'Unsure what applies to your project?',
    'cta_p_sv': 'Kontakta oss för ett första samtal. Vi bedömer vad som krävs och hjälper till med hela processen.',
    'cta_p_en': 'Contact us for an initial conversation. We assess what is required and assist with the entire process.',
    'pager_prev': {'url': '/blogg/totalrenovering-goteborg-pris/', 'sv': 'Totalrenovering i Göteborg: pris per kvm, process och vanliga misstag', 'en': 'Total renovation in Gothenburg: price per sqm, process and common mistakes'},
    'pager_next': {'url': '/blogg/rot-avdrag-2026-goteborg/', 'sv': 'ROT-avdrag för renovering 2026: så fungerar det i Göteborg', 'en': 'ROT deduction for renovation 2026: how it works in Gothenburg'},
},

# 6. rot-avdrag-2026-goteborg
{
    'slug': 'rot-avdrag-2026-goteborg',
    'title': 'ROT-avdrag renovering 2026 | Badrum, kök & måleri | Hemreform',
    'meta_desc': 'Förstå ROT-avdraget 2026 för badrum, kök, måleri och renovering. Se hur mycket du kan dra av och vilka kostnader som inte räknas.',
    'h1_sv': 'ROT-avdrag för renovering 2026: så fungerar det i Göteborg',
    'h1_en': 'ROT deduction for renovation 2026: how it works in Gothenburg',
    'intro_sv': 'ROT-avdraget gör renovering märkbart billigare. Men reglerna har detaljer som är viktiga att känna till — vad som räknas, hur mycket du kan dra av och hur du säkerställer att avdraget faktiskt godkänns av Skatteverket.',
    'intro_en': 'The ROT deduction makes renovation noticeably cheaper. But the rules have details that are important to know — what counts, how much you can deduct and how you ensure the deduction is actually approved by the Swedish Tax Agency.',
    'image_src': '/images/projekt/apartment-v1-after.webp',
    'image_w': '1800',
    'image_h': '1004',
    'image_alt_sv': 'Renovering med ROT-avdrag i Göteborg — Apartment V1',
    'body_sections': [
        {'type': 'h2', 'sv': 'Vad är ROT-avdraget och hur fungerar det 2026?', 'en': 'What is the ROT deduction and how does it work in 2026?'},
        {'type': 'p', 'sv': 'ROT står för Reparation, Ombyggnad och Tillbyggnad. Avdraget innebär att du betalar 30 procent mindre för arbetskostnaden. Det maximala ROT-beloppet är 50 000 kronor per person och år (ROT och RUT tillsammans max 75 000 kronor). Hantverkaren fakturerar dig på den reducerade summan och söker själv avdraget hos Skatteverket. Du behöver inte göra något extra.', 'en': 'ROT stands for Repair, Conversion and Extension. The deduction means you pay 30 percent less for labour costs. The maximum ROT amount is 50,000 kronor per person per year (ROT and RUT together maximum 75,000 kronor). The contractor invoices you the reduced amount and applies for the deduction themselves from the Swedish Tax Agency. You do not need to do anything extra.'},
        {'type': 'h2', 'sv': 'Vad räknas som ROT-berättigat arbete?', 'en': 'What counts as ROT-eligible work?'},
        {'type': 'p', 'sv': 'ROT-avdraget gäller för arbete på din bostad, inte för material, resor eller utrustning. Godkänt arbete inkluderar: rivning och byggarbete, el-installationer och ändring, VVS-arbete, kakelsättning, målning, golvläggning, snickeriarbete och montering av köks- och badrumsinredning. Det gäller för villa, radhus, bostadsrätt och fritidshus som du äger.', 'en': 'The ROT deduction applies to work on your home, not materials, travel or equipment. Approved work includes: demolition and building work, electrical installation and modification, plumbing, tiling, painting, floor laying, carpentry and assembly of kitchen and bathroom fittings. It applies to houses, terraced houses, condominiums and holiday homes that you own.'},
        {'type': 'h2', 'sv': 'Vad ingår INTE i ROT?', 'en': 'What is NOT included in ROT?'},
        {'type': 'p', 'sv': 'Följande ingår inte: materialkostnader (kakel, kök, vitvaror, byggmaterial), resekostnader och mobilkostnad, arbete i lokaler som hyrs ut i affärsverksamhet, arbete på hyreslägenheter (hyresgästen äger inte bostaden) och om du som bostadsrättsinnehavare låter föreningen köpa tjänsten.', 'en': 'The following are not included: material costs (tiles, kitchen, appliances, building materials), travel and transport costs, work in commercial rental premises, work in rental apartments (the tenant does not own the property) and if you as a condominium holder let the association purchase the service.'},
        {'type': 'h2', 'sv': 'Räkneexempel: hur mycket sparar du?', 'en': 'Calculation example: how much do you save?'},
        {'type': 'p', 'sv': 'Badrumsrenovering med 100 000 kronor i arbetskostnad: ROT-avdrag 30 000 kronor, du betalar 70 000 kronor. Köksrenovering med 150 000 kronor i arbete: ROT-avdrag 45 000 kronor, du betalar 105 000 kronor. Lägenhetsrenovering med 200 000 kronor i arbete: ROT-avdrag 50 000 kronor (max), du betalar 150 000 kronor. Om ni är två ägare i ett hushåll kan ni vardera ta max 50 000 kronor — totalt upp till 100 000 kronor i ROT-avdrag.', 'en': 'Bathroom renovation with 100,000 kronor in labour cost: ROT deduction 30,000 kronor, you pay 70,000 kronor. Kitchen renovation with 150,000 kronor in labour: ROT deduction 45,000 kronor, you pay 105,000 kronor. Apartment renovation with 200,000 kronor in labour: ROT deduction 50,000 kronor (maximum), you pay 150,000 kronor. If you are two owners in a household you can each claim up to 50,000 kronor — totalling up to 100,000 kronor in ROT deductions.'},
        {'type': 'h2', 'sv': 'Vanliga frågor om ROT', 'en': 'Common questions about ROT'},
        {'type': 'p', 'sv': 'Kan jag kombinera ROT och RUT? Ja, men det gemensamma taket är 75 000 kronor per person. Vad händer om jag inte har tillräcklig slutlig skatt? Avdraget begränsas automatiskt till din slutliga skatt. Gäller ROT för nybyggnation? Nej, ROT gäller inte för nybyggnation — bara för reparation, ombyggnad och tillbyggnad. Hur kontrollerar jag att hantverkaren sökt avdraget? Begär alltid en specifikation på fakturan som visar ROT-avdraget som en separat post.', 'en': 'Can I combine ROT and RUT? Yes, but the combined cap is 75,000 kronor per person. What happens if I do not have enough final tax? The deduction is automatically limited to your final tax. Does ROT apply to new construction? No, ROT does not apply to new construction — only repair, conversion and extension. How do I verify that the contractor has applied for the deduction? Always request a specification on the invoice showing the ROT deduction as a separate item.'},
    ],
    'cta_h2_sv': 'Vill du veta hur ROT gäller för ditt projekt?',
    'cta_h2_en': 'Want to know how ROT applies to your project?',
    'cta_p_sv': 'Vi räknar ut vad ROT-avdraget ger i ditt fall och tar med det i offerten. Kontakta oss för ett prisunderlag.',
    'cta_p_en': 'We calculate what the ROT deduction gives in your case and include it in the quote. Contact us for a price proposal.',
    'pager_prev': {'url': '/blogg/bygglov-renovering-goteborg/', 'sv': 'Behöver du bygglov eller anmälan vid renovering i Göteborg?', 'en': 'Do you need a building permit or notification for renovation in Gothenburg?'},
    'pager_next': {'url': '/blogg/badrumsrenovering-bostadsratt-goteborg/', 'sv': 'Badrumsrenovering i bostadsrätt i Göteborg: regler, intyg och steg för steg', 'en': 'Bathroom renovation in a housing cooperative in Gothenburg: rules, certificates and step by step'},
},

# 7. badrumsrenovering-bostadsratt-goteborg
{
    'slug': 'badrumsrenovering-bostadsratt-goteborg',
    'title': 'Badrumsrenovering bostadsrätt Göteborg | Regler & intyg | Hemreform',
    'meta_desc': 'Renovera badrum i bostadsrätt i Göteborg? Här är reglerna, intygen och checklistan för BRF, BKR, Säker Vatten och el.',
    'h1_sv': 'Badrumsrenovering i bostadsrätt i Göteborg: regler, intyg och steg för steg',
    'h1_en': 'Bathroom renovation in a housing cooperative in Gothenburg: rules, certificates and step by step',
    'intro_sv': 'Att renovera badrummet i en bostadsrätt i Göteborg kräver mer förberedelse än en vanlig badrumsrenovering. BRF-regler, intyg för tätskikt och el, och styrelsens tillstånd är alla delar av processen — och om du hoppar över dem kan det bli kostsamt.',
    'intro_en': 'Renovating a bathroom in a housing cooperative in Gothenburg requires more preparation than a regular bathroom renovation. BRF rules, certificates for waterproofing and electrical work, and board approval are all part of the process — and skipping them can be costly.',
    'image_src': '/images/projekt/bistro-after.webp',
    'image_w': '1208',
    'image_h': '1800',
    'image_alt_sv': 'Renovering i Göteborg — Hemreform projektarkiv',
    'body_sections': [
        {'type': 'h2', 'sv': 'Varför är BRF-badrummet extra känsligt?', 'en': 'Why is the BRF bathroom particularly sensitive?'},
        {'type': 'p', 'sv': 'I en bostadsrättsförening delar du ansvaret för husets stammar och gemensamma installationer med övriga boende. En felaktigt utförd badrumsrenovering kan orsaka vattenskador som sprider sig till grannarna — och du kan bli personligt ansvarig för kostnaderna. Rätt utfört arbete med certifierade hantverkare och godkänt tätskikt skyddar dig och dina grannar.', 'en': 'In a housing cooperative you share responsibility for the building\'s main pipes and common installations with other residents. An incorrectly executed bathroom renovation can cause water damage that spreads to neighbours — and you may be personally liable for the costs. Correctly executed work with certified tradespeople and approved waterproofing protects you and your neighbours.'},
        {'type': 'h2', 'sv': 'Vad behöver styrelsen godkänna?', 'en': 'What does the board need to approve?'},
        {'type': 'p', 'sv': 'Kontakta alltid din BRF-styrelse skriftligen innan en badrumsrenovering som involverar VVS eller el. Vanligtvis kräver styrelsen en skriftlig ansökan med: arbetsbeskrivning och tidsplan, namn och F-skatteintyg för alla inblandade hantverkare, hur VA-systemen berörs och bekräftelse på att arbetet uppfyller BBV/BKR-kraven för våtrum.', 'en': 'Always contact your BRF board in writing before a bathroom renovation involving plumbing or electrical work. The board typically requires a written application with: work description and timeline, name and F-tax certificate for all involved tradespeople, how the water and drainage systems are affected and confirmation that the work meets BBV/BKR requirements for wet rooms.'},
        {'type': 'h2', 'sv': 'Vilka intyg krävs för ett BRF-badrum?', 'en': 'What certificates are required for a BRF bathroom?'},
        {'type': 'p', 'sv': 'Tätskiktsintyg — dokumentation att våtrummet uppfyller Byggkeramikrådets (BKR) eller branschorganisationens krav. Säker Vatten-intyg — krävs om VVS-installationer görs av en certifierad firma. Elbesiktning — elektriker måste alltid utföra och dokumentera elarbete i badrum, inklusive jordfelsbrytare och zonsäker belysning. Dessa intyg bör sparas för framtida försäljning — köpare och banker kräver allt oftare dokumentation.', 'en': 'Waterproofing certificate — documentation that the wet room meets the Building Ceramics Council (BKR) or trade association requirements. Säker Vatten certificate — required if plumbing installations are done by a certified firm. Electrical inspection — an electrician must always perform and document electrical work in bathrooms, including earth fault circuit breakers and zone-safe lighting. These certificates should be saved for future resale — buyers and banks increasingly require documentation.'},
        {'type': 'h2', 'sv': 'Checklista för BRF-badrumsrenovering', 'en': 'Checklist for BRF bathroom renovation'},
        {'type': 'p', 'sv': '1. Kontakta styrelsen och ansök om tillstånd. 2. Anlita certifierade hantverkare med F-skattsedel. 3. Säkerställ att tätskiktet utförs av BBV- eller GVK-certifierad firma. 4. Boka certifierad VVS-firma (Säker Vatten). 5. Boka auktoriserad elektriker för el i badrum. 6. Dokumentera allt arbete med foton och intyg. 7. Lämna kopia på intyg till styrelsen efter avslutad renovering.', 'en': '1. Contact the board and apply for permission. 2. Hire certified tradespeople with F-tax certificates. 3. Ensure waterproofing is performed by a BBV or GVK-certified firm. 4. Book a certified plumbing firm (Säker Vatten). 5. Book an authorised electrician for bathroom electrical work. 6. Document all work with photos and certificates. 7. Submit copies of certificates to the board after the renovation is complete.'},
        {'type': 'h2', 'sv': 'Vad kostar ett BRF-badrum i Göteborg?', 'en': 'What does a BRF bathroom cost in Gothenburg?'},
        {'type': 'p', 'sv': 'En badrumsrenovering i bostadsrätt kostar typiskt 100 000–250 000 kronor beroende på storlek och standard. Räkna med något högre kostnad än i villa p.g.a. svårare tillgänglighet för material och strikta krav på intyg och dokumentation. ROT-avdraget gäller och kan sänka din arbetskostnad med upp till 50 000 kronor.', 'en': 'A bathroom renovation in a housing cooperative typically costs 100,000–250,000 kronor depending on size and standard. Expect somewhat higher costs than in a house due to more difficult material access and strict requirements for certificates and documentation. The ROT deduction applies and can reduce your labour costs by up to 50,000 kronor.'},
    ],
    'cta_h2_sv': 'Ska du renovera badrummet i din bostadsrätt?',
    'cta_h2_en': 'Planning to renovate the bathroom in your condominium?',
    'cta_p_sv': 'Vi hanterar hela processen — BRF-ansökan, certifierade hantverkare, tätskikt och intyg. Kontakta oss för ett prisunderlag.',
    'cta_p_en': 'We handle the entire process — BRF application, certified tradespeople, waterproofing and certificates. Contact us for a price proposal.',
    'pager_prev': {'url': '/blogg/rot-avdrag-2026-goteborg/', 'sv': 'ROT-avdrag för renovering 2026: så fungerar det i Göteborg', 'en': 'ROT deduction for renovation 2026: how it works in Gothenburg'},
    'pager_next': {'url': '/blogg/koksrenovering-bostadsratt-goteborg/', 'sv': 'Köksrenovering i bostadsrätt i Göteborg: ventilation, el, VVS och styrelsens krav', 'en': 'Kitchen renovation in a housing cooperative in Gothenburg: ventilation, electrical, plumbing and board requirements'},
},

# 8. koksrenovering-bostadsratt-goteborg
{
    'slug': 'koksrenovering-bostadsratt-goteborg',
    'title': 'Köksrenovering bostadsrätt Göteborg | Regler för BRF | Hemreform',
    'meta_desc': 'Guide till köksrenovering i bostadsrätt i Göteborg. Läs om BRF-regler, ventilation, el, VVS, tidsplan och smart köksplanering.',
    'h1_sv': 'Köksrenovering i bostadsrätt i Göteborg: ventilation, el, VVS och styrelsens krav',
    'h1_en': 'Kitchen renovation in a housing cooperative in Gothenburg: ventilation, electrical, plumbing and board requirements',
    'intro_sv': 'En köksrenovering i bostadsrätt är mer komplex än den verkar. VVS, ventilation och el berör ofta husets gemensamma system — och styrelsens tillstånd är ett måste om du ändrar dessa. Den här guiden hjälper dig att planera rätt från start.',
    'intro_en': 'A kitchen renovation in a housing cooperative is more complex than it appears. Plumbing, ventilation and electrical work often affect the building\'s common systems — and board approval is a must if you change these. This guide helps you plan correctly from the start.',
    'image_src': '/images/projekt/apartment-k38.webp',
    'image_w': '1344',
    'image_h': '1800',
    'image_alt_sv': 'Köksrenovering i bostadsrätt Göteborg — Apartment K38',
    'body_sections': [
        {'type': 'h2', 'sv': 'Vad kan du göra utan styrelsens tillstånd?', 'en': 'What can you do without board approval?'},
        {'type': 'p', 'sv': 'Du behöver normalt inget styrelsetillstånd för: byte av köksluckor och bänkskivor (utan att röra installationer), byte av vitvaror till likvärdiga, ommålning av väggar och tak, byte av golvmaterial och ny belysning utan ändring av elinstallationer. Kontrollera alltid din BRF:s egna regler — de kan vara striktare än lagens minimikrav.', 'en': 'You normally need no board approval for: replacing kitchen cabinet doors and worktops (without touching installations), replacing appliances with equivalent ones, repainting walls and ceilings, replacing floor material and new lighting without changing electrical installations. Always check your BRF\'s own rules — they may be stricter than the legal minimum requirements.'},
        {'type': 'h2', 'sv': 'När krävs styrelsens tillstånd?', 'en': 'When is board approval required?'},
        {'type': 'p', 'sv': 'Tillstånd krävs vanligtvis för: flytt av vatten eller avlopp, ändring eller utbyte av ventilationslösning (köksfläkt som kopplas till fastighetens frånluft), installation av diskhylla med avlopp i nytt läge, nya eluttag eller ändring av befintliga och planlösningsförändringar. Lämna alltid in en skriftlig ansökan med ritningar och hantverkaruppgifter.', 'en': 'Approval is typically required for: moving water or drainage pipes, modifying or replacing ventilation solutions (kitchen fan connected to the building\'s exhaust air), installing a dish rack with drainage in a new position, new electrical outlets or modification of existing ones and layout changes. Always submit a written application with drawings and contractor details.'},
        {'type': 'h2', 'sv': 'Köksfläkten — den vanligaste fallgropen', 'en': 'The kitchen fan — the most common pitfall'},
        {'type': 'p', 'sv': 'Köksfläktar i bostadsrätter är antingen kolfilterfläktar (recirkulation, inga ingrepp i ventilationen) eller frånluftsfläktar (anslutna till fastighetens ventilationssystem). Om du byter en frånluftsfläkt eller installerar en ny måste ventilationsflödena balanseras om — annars påverkas hela husets ventilation. En OVK-besiktning (obligatorisk ventilationskontroll) kan krävas.', 'en': 'Kitchen fans in housing cooperatives are either carbon filter fans (recirculation, no ventilation intervention) or exhaust air fans (connected to the building\'s ventilation system). If you replace or install a new exhaust air fan, ventilation flows must be rebalanced — otherwise the entire building\'s ventilation is affected. An OVK inspection (mandatory ventilation control) may be required.'},
        {'type': 'h2', 'sv': 'Vad kostar en köksrenovering i bostadsrätt?', 'en': 'What does a kitchen renovation in a housing cooperative cost?'},
        {'type': 'p', 'sv': 'En enklare köksrenovering i bostadsrätt (nya luckor, bänkskiva, inget VVS-arbete) kostar 60 000–120 000 kronor. En standardrenovering med nya stommar och installationer kostar 150 000–280 000 kronor. Ett platsbyggt kök med ändrad layout och ny ventilation kan kosta 250 000–450 000 kronor. ROT-avdraget sänker din arbetskostnad med 30 procent.', 'en': 'A simpler kitchen renovation in a housing cooperative (new doors, worktop, no plumbing work) costs 60,000–120,000 kronor. A standard renovation with new frames and installations costs 150,000–280,000 kronor. A custom-built kitchen with changed layout and new ventilation can cost 250,000–450,000 kronor. The ROT deduction reduces your labour cost by 30 percent.'},
        {'type': 'h2', 'sv': 'Hur gör du BRF-ansökan för köksrenovering?', 'en': 'How do you make a BRF application for kitchen renovation?'},
        {'type': 'p', 'sv': 'Förbered: ritning över nuläge och planerade ändringar, namn och F-skatteintyg på alla hantverkare, beskrivning av hur VVS och ventilation påverkas och preliminär tidsplan. Skicka ansökan till styrelsen minst 4–6 veckor innan planerat byggstart. Hemreform hjälper dig med dokumentationen och koordinerar kommunikationen med styrelsen.', 'en': 'Prepare: drawing of current state and planned changes, name and F-tax certificate for all tradespeople, description of how plumbing and ventilation are affected and preliminary timeline. Submit the application to the board at least 4–6 weeks before planned construction start. Hemreform assists with documentation and coordinates communication with the board.'},
    ],
    'cta_h2_sv': 'Planerar du köksrenovering i din bostadsrätt?',
    'cta_h2_en': 'Planning a kitchen renovation in your condominium?',
    'cta_p_sv': 'Vi hanterar BRF-ansökan, koordinerar alla hantverkare och ser till att ventilation och installationer uppfyller kraven. Kontakta oss för ett prisunderlag.',
    'cta_p_en': 'We handle the BRF application, coordinate all tradespeople and ensure ventilation and installations meet requirements. Contact us for a price proposal.',
    'pager_prev': {'url': '/blogg/badrumsrenovering-bostadsratt-goteborg/', 'sv': 'Badrumsrenovering i bostadsrätt i Göteborg: regler, intyg och steg för steg', 'en': 'Bathroom renovation in a housing cooperative in Gothenburg: rules, certificates and step by step'},
    'pager_next': {'url': '/blogg/specialsnickeri-goteborg/', 'sv': 'Specialsnickeri i Göteborg: platsbyggda garderober, bokhyllor och smart förvaring', 'en': 'Custom carpentry in Gothenburg: built-in wardrobes, bookshelves and smart storage'},
},

# 9. specialsnickeri-goteborg
{
    'slug': 'specialsnickeri-goteborg',
    'title': 'Specialsnickeri Göteborg | Platsbyggd förvaring & garderober | Hemreform',
    'meta_desc': 'Behöver du specialsnickeri i Göteborg? Läs om platsbyggda garderober, bokhyllor och måttanpassad förvaring för äldre lägenheter och landshövdingehus.',
    'h1_sv': 'Specialsnickeri i Göteborg: platsbyggda garderober, bokhyllor och smart förvaring',
    'h1_en': 'Custom carpentry in Gothenburg: built-in wardrobes, bookshelves and smart storage',
    'intro_sv': 'I Göteborgs landshövdingehus, sekelskifteslägenheter och moderna bostäder finns sällan en standard lösning som passar. Platsbyggda garderober, bokhyllor och förvaring gör att varje centimeter används rätt — och att formspråket håller ihop hela bostaden.',
    'intro_en': 'In Gothenburg\'s landshövdingehus, turn-of-the-century apartments and modern homes there is rarely a standard solution that fits. Built-in wardrobes, bookshelves and custom storage means every centimetre is used correctly — and that the design language holds the entire home together.',
    'image_src': '/images/projekt/apartment-a75.webp',
    'image_w': '1800',
    'image_h': '1344',
    'image_alt_sv': 'Platsbyggd förvaring i Göteborg — Hemreform specialsnickeri',
    'body_sections': [
        {'type': 'h2', 'sv': 'När är platsbyggt bättre än standardsnickerier?', 'en': 'When is custom-built better than standard joinery?'},
        {'type': 'p', 'sv': 'Platsbyggd förvaring passar bättre när: standardmåtten inte passar (snedväggar, taksnedning, äldre lägenhetsmått), du vill ha ett genomgående formspråk från kök till hall och sovrum, platsen är ovanlig (under trappan, i ett smalt utrymme, runt ett fönster) och när du vill kombinera funktion och estetik utan att kompromissa med något av dem.', 'en': 'Custom-built storage is better when: standard measurements do not fit (slanted walls, sloped ceilings, older apartment dimensions), you want a consistent design language from kitchen to hallway and bedroom, the space is unusual (under the stairs, in a narrow gap, around a window) and when you want to combine function and aesthetics without compromising either.'},
        {'type': 'h2', 'sv': 'Specialsnickeri i Göteborgs landshövdingehus', 'en': 'Custom carpentry in Gothenburg\'s landshövdingehus'},
        {'type': 'p', 'sv': 'Landshövdingehuset är Göteborgs signaturfastighet — tre våningar med bottenplan i tegel och övre plan i trä. De har höga tak, oregelbundna mått och ett kulturhistoriskt värde som ställer krav på hantverk och materialval. Platsbyggda snickerier i dessa miljöer kräver hantverkare som förstår hur träkonstruktioner beter sig och hur man jobbar varsamt med äldre byggnadsdelar.', 'en': 'The landshövdingehus is Gothenburg\'s signature building — three storeys with ground floor in brick and upper floors in wood. They have high ceilings, irregular dimensions and a heritage value that demands craftsmanship and material choices. Custom joinery in these environments requires craftspeople who understand how wood structures behave and how to work carefully with older building elements.'},
        {'type': 'h2', 'sv': 'Vad kan du beställa som specialsnickeri?', 'en': 'What can you order as custom carpentry?'},
        {'type': 'p', 'sv': 'Vanliga beställningar hos Hemreform inkluderar: platsbyggda garderober med skjutdörrar eller pendeldörrar anpassade för snedtak, bokhyllor som täcker en hel vägg med integrerade detaljer och belysning, köksöar och bufféskåp som matchar befintlig köksinredning, entréförvaring med kombinerade hyllor, krokar och sittbänk, och badrumsmöbler i trä anpassade för fuktiga miljöer.', 'en': 'Common orders at Hemreform include: built-in wardrobes with sliding or hinged doors adapted for sloped ceilings, bookshelves covering an entire wall with integrated details and lighting, kitchen islands and buffet cabinets matching existing kitchen fittings, hallway storage with combined shelves, hooks and a bench and bathroom furniture in wood adapted for humid environments.'},
        {'type': 'h2', 'sv': 'Hur ser processen ut från idé till monterat snickeri?', 'en': 'What does the process look like from idea to installed joinery?'},
        {'type': 'p', 'sv': '1. Platsbesök och mätning — vi besöker bostaden och dokumenterar mått, underlag och önskemål. 2. Förslag och skiss — vi presenterar ett förslag med mått, materialval och ungefärligt pris. 3. Tillverkning — moduler och detaljer tillverkas i rätt material och finish. 4. Montering och justeringar — vi monterar på plats och justerar för att passa det exakta utrymmet. 5. Slutbesiktning — du godkänner resultatet.', 'en': '1. Site visit and measurement — we visit the home and document dimensions, substrate and wishes. 2. Proposal and sketch — we present a proposal with dimensions, material choices and approximate price. 3. Manufacturing — modules and details are manufactured in the right material and finish. 4. Installation and adjustments — we install on site and adjust to fit the exact space. 5. Final inspection — you approve the result.'},
        {'type': 'h2', 'sv': 'Vad kostar specialsnickeri i Göteborg?', 'en': 'What does custom carpentry cost in Gothenburg?'},
        {'type': 'p', 'sv': 'Priset beror på storlek, material och komplexitet. En platsbyggd garderob kostar typiskt 15 000–60 000 kronor. En väggfylld bokhylla med detaljer kostar 20 000–80 000 kronor. En komplett entréförvaring med bänk och hyllor kostar 25 000–70 000 kronor. ROT-avdraget gäller för arbetet och kan sänka din kostnad med 30 procent.', 'en': 'The price depends on size, material and complexity. A built-in wardrobe typically costs 15,000–60,000 kronor. A wall-filling bookshelf with details costs 20,000–80,000 kronor. Complete hallway storage with bench and shelves costs 25,000–70,000 kronor. The ROT deduction applies to the labour and can reduce your cost by 30 percent.'},
    ],
    'cta_h2_sv': 'Har du ett utrymme som behöver en platsbyggd lösning?',
    'cta_h2_en': 'Have a space that needs a custom-built solution?',
    'cta_p_sv': 'Skicka bilder och beskriv utrymmet och dina önskemål. Vi återkommer med ett förslag och en prisindikation.',
    'cta_p_en': 'Send photos and describe the space and your wishes. We will get back to you with a proposal and price indication.',
    'pager_prev': {'url': '/blogg/koksrenovering-bostadsratt-goteborg/', 'sv': 'Köksrenovering i bostadsrätt i Göteborg: ventilation, el, VVS och styrelsens krav', 'en': 'Kitchen renovation in a housing cooperative in Gothenburg: ventilation, electrical, plumbing and board requirements'},
    'pager_next': {'url': '/blogg/badrumsrenovering-goteborg-checklista/', 'sv': 'Badrumsrenovering i Göteborg: checklista innan du börjar', 'en': 'Bathroom renovation in Gothenburg: checklist before you start'},
},

]  # end ARTICLES

# ============================================================
# Generate files
# ============================================================
for article in ARTICLES:
    slug = article['slug']
    out_dir = os.path.join(BLOGG_DIR, slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')
    html = build_page(article)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Written: {out_path}')

print('All articles generated.')
