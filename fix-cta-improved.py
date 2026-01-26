#!/usr/bin/env python3
"""
Improved CTA replacement script
Works with both formatted and minified HTML
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path(".")

# CTA templates
CTA_SANATORIA = '''<div class="notice cta-urgent">
<strong>🚨 Rogito bloccato o immobile irregolare?</strong>
<p>Studio 4e segue pratiche in sanatoria da oltre 20 anni. <strong>Prima consulenza telefonica gratuita</strong> per valutare il tuo caso.</p>
<p style="margin-top:12px">
<a class="btn" href="tel:+393299736697" style="font-size:16px">📞 Chiama ora: +39 329 973 6697</a>
<a class="btn secondary" href="https://wa.me/393299736697?text=Ciao%2C%20ho%20un%20problema%20di%20regolarit%C3%A0%20urbanistica.%20Posso%20raccontarti%20il%20caso%3F" style="margin-left:10px">WhatsApp</a>
</p>
<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 4.8/5 su Houzz • 50+ progetti seguiti in Sicilia • 20+ anni esperienza</p>
</div>'''

CTA_RISTRUTTURAZIONE = '''<div class="notice cta-standard">
<strong>Stai pianificando una ristrutturazione?</strong>
<p>Studio 4e a Palermo dal 2002. <strong>Preventivo e primo confronto gratuiti</strong>. Sopralluogo, progetto, pratiche e direzione lavori.</p>
<p style="margin-top:12px">
<a class="btn" href="tel:+393299736697">📞 Chiama: +39 329 973 6697</a>
<a class="btn secondary" href="/inizia-da-qui/" style="margin-left:10px">Inizia da qui</a>
</p>
<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 4.8/5 su Houzz • 20+ anni di esperienza • 50+ progetti in Sicilia</p>
</div>'''

CTA_PRATICHE = '''<div class="notice cta-standard">
<strong>Serve chiarezza sulle pratiche edilizie?</strong>
<p>CILA, SCIA, permessi, varianti. Studio 4e verifica lo stato legittimo e segue l'iter completo. <strong>Prima valutazione telefonica gratuita</strong>.</p>
<p style="margin-top:12px">
<a class="btn" href="tel:+393299736697">📞 Chiama: +39 329 973 6697</a>
<a class="btn secondary" href="https://wa.me/393299736697?text=Ciao%2C%20devo%20capire%20che%20pratica%20edilizia%20serve%20per%20il%20mio%20progetto." style="margin-left:10px">WhatsApp</a>
</p>
<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 4.8/5 su Houzz • Studio a Palermo dal 2002</p>
</div>'''

PHONE_CTA = '''<div class="phone-cta" style="margin:14px 0; padding:12px; background:rgba(122,29,82,0.08); border-left:4px solid #7a1d52; border-radius:12px">
<p style="margin:0; font-size:14px; font-weight:600">📞 Hai un caso urgente? <a href="tel:+393299736697" style="color:#7a1d52; font-weight:700">Chiama ora: +39 329 973 6697</a></p>
</div>'''

def detect_category(filepath, content):
    """Detect page category"""
    path_str = str(filepath).lower()
    content_lower = content.lower()

    if any(word in path_str or word in content_lower for word in ['sanatoria', 'regolarit', 'rogito', 'vincoli', 'verifica-stato-legittimo']):
        return 'sanatoria'

    if any(word in path_str or word in content_lower for word in ['ristrutturazione', 'appartamento', 'villa', 'interni']):
        return 'ristrutturazione'

    if any(word in path_str or word in content_lower for word in ['cila', 'scia', 'permess', 'pratica', 'autorizzazioni']):
        return 'pratiche'

    return 'default'

def process_file(filepath):
    """Process single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has our CTA
    if 'cta-urgent' in content or 'cta-standard' in content:
        return False, []

    # Skip if no article
    if '<article class="article">' not in content:
        return False, []

    changes = []

    # 1. Add phone CTA after H1
    h1_pattern = r'(<h1>[^<]+</h1>)'
    if re.search(h1_pattern, content):
        if 'phone-cta' not in content:
            content = re.sub(h1_pattern, r'\1' + PHONE_CTA, content, count=1)
            changes.append('Phone CTA added')

    # 2. Replace first CTA box
    category = detect_category(filepath, content)

    # Find and replace the "Contatta Studio 4e se:" box
    cta_pattern = r'<div class="notice"><strong>Contatta <a[^>]+>Studio 4e</a> se:</strong>.*?</div>'

    if re.search(cta_pattern, content, re.DOTALL):
        if category == 'sanatoria':
            content = re.sub(cta_pattern, CTA_SANATORIA, content, count=1, flags=re.DOTALL)
        elif category == 'ristrutturazione':
            content = re.sub(cta_pattern, CTA_RISTRUTTURAZIONE, content, count=1, flags=re.DOTALL)
        elif category == 'pratiche':
            content = re.sub(cta_pattern, CTA_PRATICHE, content, count=1, flags=re.DOTALL)
        else:
            content = re.sub(cta_pattern, CTA_RISTRUTTURAZIONE, content, count=1, flags=re.DOTALL)

        changes.append(f'CTA replaced ({category})')

    # Write back if changes
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes

    return False, []

def main():
    print("🚀 Adding optimized CTAs and phone links...")
    print()

    # Process guide pages
    guide_pages = list(ROOT_DIR.glob("guide/**/*.html")) + list(ROOT_DIR.glob("sicilia/**/*.html"))

    processed = 0
    stats = {'sanatoria': 0, 'ristrutturazione': 0, 'pratiche': 0, 'default': 0}

    for filepath in guide_pages:
        if 'backup-original' in str(filepath):
            continue

        changed, changes = process_file(filepath)
        if changed:
            processed += 1

            # Track stats
            for change in changes:
                if 'sanatoria' in change:
                    stats['sanatoria'] += 1
                elif 'ristrutturazione' in change:
                    stats['ristrutturazione'] += 1
                elif 'pratiche' in change:
                    stats['pratiche'] += 1
                elif 'default' in change:
                    stats['default'] += 1

            if processed <= 10:
                print(f"✅ {filepath.relative_to(ROOT_DIR)}")
                for change in changes:
                    print(f"   → {change}")

    print()
    print(f"✅ Done! Modified {processed} files")
    print()
    print("CTA types applied:")
    for cta_type, count in stats.items():
        if count > 0:
            print(f"  • {cta_type}: {count} pages")

if __name__ == "__main__":
    main()
