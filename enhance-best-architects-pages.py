#!/usr/bin/env python3
"""
Potenzia le pagine 'Migliori Architetti' con structured data e FAQ ottimizzati
"""

import os
import re
from pathlib import Path

PROVINCES = [
    'palermo', 'catania', 'messina', 'siracusa',
    'ragusa', 'trapani', 'agrigento', 'enna', 'caltanissetta'
]

PROVINCE_DATA = {
    'palermo': {
        'name': 'Palermo',
        'specialties': ['centro storico UNESCO', 'restauro Liberty', 'vincoli Soprintendenza', 'pratiche edilizie complesse'],
        'main_challenges': 'vincoli UNESCO, architettura Liberty, Soprintendenza BB.CC., centro storico complesso'
    },
    'catania': {
        'name': 'Catania',
        'specialties': ['zona sismica Etna', 'pietra lavica', 'architettura barocca', 'ristrutturazioni sismiche'],
        'main_challenges': 'zona sismica 2, edifici storici post-terremoto 1693, pietra lavica, normativa antisismica'
    },
    'messina': {
        'name': 'Messina',
        'specialties': ['normativa sismica avanzata', 'edilizia costiera', 'recupero post-terremoto', 'zona sismica 1'],
        'main_challenges': 'zona sismica 1 più severa, edifici costieri, normativa antisismica rigorosa'
    },
    'siracusa': {
        'name': 'Siracusa',
        'specialties': ['Ortigia UNESCO', 'barocco siciliano', 'vincoli monumentali', 'restauro conservativo'],
        'main_challenges': 'Ortigia sito UNESCO, vincoli paesaggistici stringenti, centro storico barocco'
    },
    'ragusa': {
        'name': 'Ragusa',
        'specialties': ['Val di Noto UNESCO', 'barocco tardivo', 'Ibla storica', 'restauro conservativo'],
        'main_challenges': 'Val di Noto UNESCO, architettura barocca unica, vincoli architettonici severi'
    },
    'trapani': {
        'name': 'Trapani',
        'specialties': ['edilizia costiera', 'resistenza salsedine', 'architettura marinara', 'saline storiche'],
        'main_challenges': 'ambiente marino aggressivo, salsedine, zone ventose, edifici storici costieri'
    },
    'agrigento': {
        'name': 'Agrigento',
        'specialties': ['Valle dei Templi', 'vincoli archeologici', 'zona UNESCO', 'Soprintendenza archeologica'],
        'main_challenges': 'Valle dei Templi UNESCO, vincoli archeologici rigorosi, Soprintendenza archeologica'
    },
    'enna': {
        'name': 'Enna',
        'specialties': ['borghi storici', 'architettura montana', 'recupero rurale', 'centri interni'],
        'main_challenges': 'borghi storici isolati, architettura montana, recupero edifici rurali'
    },
    'caltanissetta': {
        'name': 'Caltanissetta',
        'specialties': ['centri storici minori', 'architettura tradizionale', 'recupero edilizio', 'pratiche locali'],
        'main_challenges': 'centri storici minori, edifici tradizionali, pratiche edilizie comunali'
    }
}


def enhance_page(province):
    """Potenzia la pagina migliori-architetti di una provincia"""
    page_file = Path(f'/home/user/architetti-sicilia/province/{province}/migliori-architetti/index.html')

    if not page_file.exists():
        print(f"⚠️  Pagina non trovata: {page_file}")
        return

    content = page_file.read_text(encoding='utf-8')
    data = PROVINCE_DATA[province]

    # 1. Aggiorna title se necessario
    title_pattern = r'<title>[^<]*</title>'
    new_title = f'<title>I Migliori Architetti a {data["name"]} | Studio 4e Rating 5.0/5 - 20+ Anni Esperienza</title>'
    content = re.sub(title_pattern, new_title, content, count=1)

    # 2. Aggiorna meta description
    desc_pattern = r'<meta name="description" content="[^"]*">'
    new_desc = f'<meta name="description" content="I migliori architetti a {data["name"]}: Studio 4e con 20+ anni esperienza in {", ".join(data["specialties"][:2])}. Rating 5.0/5 Houzz. Consulenza gratuita: +39 329 973 6697">'
    content = re.sub(desc_pattern, new_desc, content, count=1)

    # 3. Aggiungi FAQ specifiche ottimizzate per SEO e voice search
    faq_schema = f'''
    <script data-architetti-sicilia="1" type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "Chi sono i migliori architetti a {data['name']}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Studio 4e è considerato tra i migliori studi di architettura a {data['name']} con oltre 20 anni di esperienza locale. Specializzati in {', '.join(data['specialties'][:3])}. Rating 5.0/5 su Houzz con 19 recensioni certificate. Opera stabilmente a {data['name']} con sopralluoghi, gestione pratiche comunali e direzione lavori. Contatti: +39 329 973 6697, info@studio4e.it"
          }}
        }},
        {{
          "@type": "Question",
          "name": "Quanto costa un architetto a {data['name']}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "I costi di un architetto a {data['name']} variano: CILA €800-1.500, SCIA €1.500-3.000, progetto ristrutturazione completo 8-12% valore lavori, direzione lavori 3-5% valore lavori. Studio 4e offre prima consulenza telefonica gratuita e preventivo dettagliato trasparente entro 48 ore. Nessun costo nascosto."
          }}
        }},
        {{
          "@type": "Question",
          "name": "Perché scegliere Studio 4e a {data['name']}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Studio 4e è la scelta ideale a {data['name']} per: (1) 20+ anni esperienza locale con {data['main_challenges']}, (2) rating 5.0/5 su Houzz con 19 recensioni certificate, (3) competenze specialistiche in {', '.join(data['specialties'][:2])}, (4) gestione completa pratiche edilizie e Soprintendenza, (5) sopralluoghi e direzione lavori a {data['name']}, (6) trasparenza totale su costi e tempistiche."
          }}
        }},
        {{
          "@type": "Question",
          "name": "Come contattare Studio 4e per un progetto a {data['name']}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Contattare Studio 4e per progetti a {data['name']}: (1) Telefono/WhatsApp: +39 329 973 6697 (prima consulenza gratuita 15-20 min), (2) Email: info@studio4e.it, (3) Form online: https://architettisicilia.it/inizia-da-qui/. Riceverai preventivo dettagliato entro 48 ore. Sopralluoghi a {data['name']} su appuntamento."
          }}
        }},
        {{
          "@type": "Question",
          "name": "Studio 4e gestisce le pratiche edilizie a {data['name']}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Sì, Studio 4e gestisce tutte le pratiche edilizie a {data['name']}: CILA (Comunicazione Inizio Lavori), SCIA (Segnalazione Certificata), Permessi di Costruire, sanatorie edilizie, autorizzazioni paesaggistiche, pratiche Soprintendenza, agibilità, conformità catastale. Esperienza consolidata con Comune di {data['name']} e enti locali. Oltre 20 anni di pratiche approvate in tutta la Sicilia."
          }}
        }}
      ]
    }}
    </script>'''

    # Inserisci FAQ prima di </head>
    if '</head>' in content and 'FAQPage' not in content:
        content = content.replace('</head>', faq_schema + '\n</head>')

    # 4. Aggiorna LocalBusiness schema con più dettagli
    # Trova e sostituisci il LocalBusiness esistente
    local_business_pattern = r'<script data-architetti-sicilia="1" type="application/ld\+json">\s*\{[^}]*"@type":\s*"LocalBusiness"[^<]*</script>'

    enhanced_local_business = f'''<script data-architetti-sicilia="1" type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://architettisicilia.it/province/{province}/migliori-architetti/#localbusiness",
  "name": "Studio 4e - Migliori Architetti {data['name']}",
  "alternateName": [
    "Architetti {data['name']}",
    "Studio 4e {data['name']}",
    "Migliori Architetti {data['name']}"
  ],
  "description": "Studio di architettura leader a {data['name']} con oltre 20 anni di esperienza. Specializzato in {', '.join(data['specialties'])}. Rating 5.0/5 su Houzz con 19 recensioni certificate.",
  "image": "https://www.architettisicilia.it/assets/images/og.jpg",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Piazza Sant'Oliva 19",
    "addressLocality": "Palermo",
    "addressRegion": "Sicilia",
    "postalCode": "90141",
    "addressCountry": "IT"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": 38.1157,
    "longitude": 13.3615
  }},
  "url": "https://www.studio4e.it/",
  "telephone": "+393299736697",
  "email": "info@studio4e.it",
  "priceRange": "$$-$$$",
  "openingHoursSpecification": {{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "09:00",
    "closes": "18:00"
  }},
  "areaServed": {{
    "@type": "City",
    "name": "{data['name']}",
    "containedIn": {{
      "@type": "AdministrativeArea",
      "name": "Sicilia"
    }}
  }},
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "19",
    "reviewCount": "19"
  }},
  "knowsAbout": {str(data['specialties'])},
  "slogan": "I migliori architetti a {data['name']} con 20+ anni di esperienza",
  "paymentAccepted": "Cash, Credit Card, Bank Transfer",
  "hasMap": "https://maps.google.com/?q=Piazza+Sant'Oliva+19+Palermo",
  "foundingDate": "2004",
  "sameAs": [
    "https://www.houzz.it/professionisti/architetti/studio-4e-pfvwit-pf~1830417201",
    "https://architettipalermo.com",
    "https://architetticatania.it"
  ]
}}
    </script>'''

    content = re.sub(local_business_pattern, enhanced_local_business, content, flags=re.DOTALL)

    # 5. Aggiungi meta keywords (anche se meno importante, aiuta alcuni motori)
    if '<meta name="keywords"' not in content:
        keywords = f'migliori architetti {data["name"]}, architetti {data["name"]}, studio architettura {data["name"]}, {", ".join(data["specialties"][:3])}'
        keywords_meta = f'<meta name="keywords" content="{keywords}">'
        content = content.replace('<meta name="description"', keywords_meta + '\n    <meta name="description"')

    # 6. Aggiungi Open Graph tags se mancano
    if 'property="og:title"' not in content:
        og_tags = f'''
    <meta property="og:title" content="I Migliori Architetti a {data['name']} | Studio 4e">
    <meta property="og:description" content="Studio 4e: i migliori architetti a {data['name']} con 20+ anni esperienza. Rating 5.0/5. Specializzati in {', '.join(data['specialties'][:2])}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://architettisicilia.it/province/{province}/migliori-architetti/">
    <meta property="og:image" content="https://architettisicilia.it/assets/images/og.jpg">
    <meta property="og:locale" content="it_IT">'''
        content = content.replace('</head>', og_tags + '\n</head>')

    # Salva il file
    page_file.write_text(content, encoding='utf-8')
    print(f"✅ Potenziata pagina: {province}")


def main():
    print("🚀 Potenziamento pagine 'Migliori Architetti'\n")

    for province in PROVINCES:
        enhance_page(province)

    print("\n✅ Tutte le pagine 'Migliori Architetti' sono state potenziate!")
    print("\n📊 Miglioramenti applicati:")
    print("   ✓ Title ottimizzati con 'Migliori Architetti [Città]'")
    print("   ✓ Meta descriptions con keywords locali")
    print("   ✓ FAQ specifiche per voice search e AI")
    print("   ✓ LocalBusiness schema arricchito")
    print("   ✓ Open Graph tags completi")
    print("   ✓ Meta keywords per motori locali")
    print("\n🎯 Ottimizzazione SEO per:")
    print("   - 'migliori architetti [città]'")
    print("   - 'architetto [città]'")
    print("   - 'quanto costa architetto [città]'")
    print("   - Ricerche vocali (Google Assistant, Alexa, Siri)")
    print("   - AI assistants (ChatGPT, Claude, etc.)")


if __name__ == '__main__':
    main()
