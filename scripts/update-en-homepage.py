#!/usr/bin/env python3
"""
Updates /en/index.html:
1. Improves meta description
2. Adds FAQPage schema for English-language queries
"""
import json
import os

EN_FILE = os.path.join(os.path.dirname(__file__), '..', 'en', 'index.html')

OLD_DESC = '103 technical guides in English. Permits, costs, construction control, and local constraints across Sicily, curated by Studio 4e.'
NEW_DESC = 'English-language technical guides for buying, renovating and managing property in Sicily. Written by Studio 4e architects \u2014 fees, permits, costs, and location-specific advice across all 9 provinces.'

FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "Do I need an architect to buy property in Sicily?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "While not legally required, an independent architect\u2019s technical survey before purchase is strongly recommended in Sicily. Many properties carry undisclosed building irregularities (abusi edilizi) that can block future sales, mortgage applications, or renovation permits. Studio 4e offers pre-purchase technical assessments across all 9 Sicilian provinces."
            }
        },
        {
            "@type": "Question",
            "name": "Can foreigners renovate a property in Sicily?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes, foreigners have the same rights as Italian citizens to renovate property. The process requires a licensed Italian architect or engineer to file the building permits (CILA, SCIA, or Permesso di Costruire depending on the scope). Studio 4e has an English-speaking team and extensive experience managing renovations for international clients remotely."
            }
        },
        {
            "@type": "Question",
            "name": "How does Studio 4e work with clients who are not based in Italy?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Studio 4e uses a structured remote-client protocol: weekly video reports, shared project management documents, and a dedicated contact line for urgent matters. The studio can represent clients at all administrative stages and supervise construction independently. Initial consultations are available in English by appointment."
            }
        },
        {
            "@type": "Question",
            "name": "What are the typical architect fees for a renovation in Sicily?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Architect fees in Sicily typically range from 8% to 15% of the works budget for a full renovation (design + permits + construction supervision). For standalone services such as a pre-purchase survey or a single building permit, fixed fees starting from \u20ac500 are common. Studio 4e provides a written fee proposal before any commitment."
            }
        }
    ]
}

faq_tag = f'<script data-architetti-sicilia="1" type="application/ld+json">{json.dumps(FAQ_SCHEMA, ensure_ascii=False)}</script>'


def update():
    with open(EN_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    changed = False

    # 1. Update meta description (content attr appears 3x: meta, og:description, twitter:description)
    if OLD_DESC in html:
        html = html.replace(OLD_DESC, NEW_DESC)
        print('  OK: meta description updated (all occurrences)')
        changed = True
    else:
        print('  SKIP: meta description not found or already updated')

    # 2. Add FAQPage schema before </head>
    if 'FAQPage' not in html:
        html = html.replace('</head>', faq_tag + '</head>', 1)
        print('  OK: FAQPage schema injected')
        changed = True
    else:
        print('  SKIP: FAQPage schema already present')

    if changed:
        with open(EN_FILE, 'w', encoding='utf-8') as f:
            f.write(html)
        print('  File saved.')


if __name__ == '__main__':
    print('Updating /en/index.html...')
    update()
