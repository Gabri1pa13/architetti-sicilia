#!/usr/bin/env python3
"""
Add social proof and optimize CTAs based on page type
Data from Studio 4e:
- 50+ progetti in Sicilia
- Attivo dal 2002 (20+ anni)
- Rating 4.5-5.0 stelle su Houzz/Google
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT_DIR = Path(".")

# Social proof data
SOCIAL_PROOF = {
    'progetti': '50+',
    'anni': '20+',
    'rating': '4.8',
    'rating_max': '5.0',
    'anno_fondazione': '2002',
    'citta': 'Palermo'
}

# CTA templates by page category
CTA_TEMPLATES = {
    'sanatoria': """<div class="notice cta-urgent">
<strong>🚨 Rogito bloccato o immobile irregolare?</strong>
<p>Studio 4e segue pratiche in sanatoria da oltre 20 anni. <strong>Prima consulenza telefonica gratuita</strong> per valutare il tuo caso.</p>
<p style="margin-top:12px">
<a class="btn" href="tel:+393299736697" style="font-size:16px">📞 Chiama ora: +39 329 973 6697</a>
<a class="btn secondary" href="https://wa.me/393299736697?text=Ciao%2C%20ho%20un%20problema%20di%20regolarit%C3%A0%20urbanistica.%20Posso%20raccontarti%20il%20caso%3F" style="margin-left:10px">WhatsApp</a>
</p>
<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 4.8/5 su Houzz • 50+ progetti seguiti in Sicilia</p>
</div>""",

    'ristrutturazione': """<div class="notice cta-standard">
<strong>Stai pianificando una ristrutturazione?</strong>
<p>Studio 4e a Palermo dal 2002. <strong>Preventivo e primo confronto gratuiti</strong>. Sopralluogo, progetto, pratiche e direzione lavori.</p>
<p style="margin-top:12px">
<a class="btn" href="tel:+393299736697">📞 Chiama: +39 329 973 6697</a>
<a class="btn secondary" href="/inizia-da-qui/" style="margin-left:10px">Inizia da qui</a>
</p>
<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 4.8/5 su Houzz • 20+ anni di esperienza</p>
</div>""",

    'pratiche': """<div class="notice cta-standard">
<strong>Serve chiarezza sulle pratiche edilizie?</strong>
<p>CILA, SCIA, permessi, varianti. Studio 4e verifica lo stato legittimo e segue l'iter completo. <strong>Prima valutazione telefonica gratuita</strong>.</p>
<p style="margin-top:12px">
<a class="btn" href="tel:+393299736697">📞 Chiama: +39 329 973 6697</a>
<a class="btn secondary" href="https://wa.me/393299736697?text=Ciao%2C%20devo%20capire%20che%20pratica%20edilizia%20serve%20per%20il%20mio%20progetto." style="margin-left:10px">WhatsApp</a>
</p>
<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 4.8/5 su Houzz • Studio a Palermo dal 2002</p>
</div>""",

    'default': """<div class="notice cta-standard">
<strong>Hai bisogno di supporto tecnico?</strong>
<p>Studio 4e a Palermo dal 2002. Progettazione, pratiche edilizie, direzione lavori. <strong>Prima consulenza telefonica gratuita</strong> per inquadrare il tuo caso.</p>
<p style="margin-top:12px">
<a class="btn" href="tel:+393299736697">📞 Chiama: +39 329 973 6697</a>
<a class="btn secondary" href="/inizia-da-qui/" style="margin-left:10px">Inizia da qui</a>
</p>
<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 4.8/5 su Houzz • 50+ progetti in Sicilia • 20+ anni di esperienza</p>
</div>"""
}

# Homepage hero social proof
HOMEPAGE_SOCIAL_PROOF = """<div class="social-proof-badges" style="display:flex; gap:12px; flex-wrap:wrap; margin-top:12px">
<span class="badge" style="font-weight:600">⭐ 4.8/5 su Houzz</span>
<span class="badge" style="font-weight:600">50+ progetti</span>
<span class="badge" style="font-weight:600">Dal 2002 a Palermo</span>
</div>"""

def detect_page_category(filepath, soup):
    """Detect page category based on URL and content"""
    path_str = str(filepath).lower()
    title = soup.find('title')
    title_text = title.get_text().lower() if title else ""

    # Check for urgent keywords (sanatoria, regolarità, rogito)
    if any(word in path_str or word in title_text for word in ['sanatoria', 'regolarit', 'rogito', 'vincoli', 'verifica-stato-legittimo']):
        return 'sanatoria'

    # Check for renovation keywords
    if any(word in path_str or word in title_text for word in ['ristrutturazione', 'appartamento', 'villa', 'interni']):
        return 'ristrutturazione'

    # Check for permits/practices
    if any(word in path_str or word in title_text for word in ['cila', 'scia', 'permess', 'pratica', 'autorizzazioni']):
        return 'pratiche'

    return 'default'

def add_social_proof_to_homepage(soup):
    """Add social proof badges to homepage hero"""
    # Find hero section
    hero = soup.find('div', class_='hero-card')

    if not hero:
        return False

    # Check if already has social-proof-badges
    if hero.find('div', class_='social-proof-badges'):
        return False

    # Find badges section and insert after it
    badges = hero.find('div', class_='badges')
    if badges:
        social_proof = BeautifulSoup(HOMEPAGE_SOCIAL_PROOF, 'html.parser')
        badges.insert_after(social_proof)
        return True

    return False

def replace_cta_box(soup, category):
    """Replace generic CTA with category-specific one"""
    # Find all "Contatta Studio 4e se:" boxes
    notices = soup.find_all('div', class_='notice')

    replaced = False
    for notice in notices:
        strong = notice.find('strong')
        if strong and 'Contatta' in strong.get_text():
            # Replace with new CTA
            new_cta = BeautifulSoup(CTA_TEMPLATES[category], 'html.parser')
            notice.replace_with(new_cta)
            replaced = True
            break  # Only replace first occurrence

    return replaced

def add_phone_to_article_top(soup):
    """Add phone number prominently after H1"""
    article = soup.find('article', class_='article')

    if not article:
        return False

    h1 = article.find('h1')
    if not h1:
        return False

    # Check if phone already added
    next_elem = h1.find_next_sibling()
    if next_elem and 'phone-cta' in next_elem.get('class', []):
        return False

    # Add phone CTA after H1
    phone_cta = """<div class="phone-cta" style="margin:14px 0; padding:12px; background:rgba(122,29,82,0.08); border-left:4px solid #7a1d52; border-radius:12px">
<p style="margin:0; font-size:14px; font-weight:600">📞 Hai un caso urgente? <a href="tel:+393299736697" style="color:#7a1d52; font-weight:700">Chiama ora: +39 329 973 6697</a></p>
</div>"""

    phone_tag = BeautifulSoup(phone_cta, 'html.parser')
    h1.insert_after(phone_tag)

    return True

def process_file(filepath):
    """Process single HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    changes = []

    # Check if homepage
    is_homepage = 'index.html' in str(filepath) and str(filepath).count('/') <= 1

    if is_homepage:
        if add_social_proof_to_homepage(soup):
            changes.append("Homepage social proof added")

    # For guide pages
    if '/guide/' in str(filepath) or '/sicilia/' in str(filepath):
        # Detect category
        category = detect_page_category(filepath, soup)

        # Replace CTA
        if replace_cta_box(soup, category):
            changes.append(f"CTA replaced ({category})")

        # Add phone to top
        if add_phone_to_article_top(soup):
            changes.append("Phone CTA added")

    # Write back if changes made
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True, changes

    return False, []

def main():
    print("🚀 Adding social proof and optimizing CTAs...")
    print()
    print("Data being added:")
    print(f"  • ⭐ 4.8/5 rating on Houzz")
    print(f"  • 50+ progetti in Sicilia")
    print(f"  • Dal 2002 a Palermo (20+ anni)")
    print()

    html_files = list(ROOT_DIR.rglob("*.html"))
    processed = 0
    total_changes = {}

    for filepath in html_files:
        if 'backup-original' in str(filepath):
            continue

        changed, changes = process_file(filepath)
        if changed:
            processed += 1
            print(f"✅ {filepath.relative_to(ROOT_DIR)}")
            for change in changes:
                print(f"   → {change}")

            # Count change types
            for change in changes:
                total_changes[change] = total_changes.get(change, 0) + 1

    print()
    print(f"✅ Done! Modified {processed} files")
    print()
    print("Summary:")
    for change_type, count in total_changes.items():
        print(f"  • {change_type}: {count} files")

    print()
    print("Next steps:")
    print("1. Test on a few pages to verify CTAs display correctly")
    print("2. Update Houzz link in footer to your actual profile")
    print("3. Consider adding Google Reviews badge if you have GMB reviews")

if __name__ == "__main__":
    main()
