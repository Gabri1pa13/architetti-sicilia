#!/bin/bash

# Quick test su singola pagina per vedere risultati prima di processare tutte le 800
# Uso: ./test-single-page.sh

set -e

TEST_FILE="guide/palermo/architetto-a-palermo-come-impostare-un-progetto-senza-sorprese.html"
BACKUP_FILE="${TEST_FILE}.backup"

echo "🧪 Test su singola pagina: $TEST_FILE"
echo ""

# Backup
if [ ! -f "$BACKUP_FILE" ]; then
  echo "📦 Creating backup..."
  cp "$TEST_FILE" "$BACKUP_FILE"
  echo "   ✅ Backup saved to $BACKUP_FILE"
else
  echo "📦 Backup already exists, using it..."
fi

echo ""
echo "🔧 Applying optimizations..."
echo ""

# Create temp Python script to process single file
cat > _test_single.py << 'EOFPYTHON'
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import re
import html

filepath = Path(sys.argv[1])

with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("Applying fixes...")

# 1. Fix JSON-LD
print("  → Cleaning JSON-LD structured data...")
json_ld_scripts = soup.find_all('script', type='application/ld+json')
for script in json_ld_scripts:
    if script.string:
        content = html.unescape(script.string)
        content = re.sub(r'<span[^>]*>', '', content)
        content = re.sub(r'</span>', '', content)
        content = re.sub(r'<a[^>]*>([^<]+)</a>', r'\1', content)
        script.string = content

# 2. Fix title
print("  → Fixing title tag...")
title = soup.find('title')
if title:
    clean_text = title.get_text(strip=True)
    title.clear()
    title.string = clean_text

# 3. Add lazy loading
print("  → Adding lazy loading to images...")
images = soup.find_all('img')
for i, img in enumerate(images):
    if i == 0:
        img['loading'] = 'eager'
        img['fetchpriority'] = 'high'
    else:
        img['loading'] = 'lazy'
        img['decoding'] = 'async'

# 4. Add phone CTA after H1
print("  → Adding phone CTA...")
article = soup.find('article', class_='article')
if article:
    h1 = article.find('h1')
    if h1:
        phone_cta = '''<div class="phone-cta" style="margin:14px 0; padding:12px; background:rgba(122,29,82,0.08); border-left:4px solid #7a1d52; border-radius:12px">
<p style="margin:0; font-size:14px; font-weight:600">📞 Hai un caso urgente? <a href="tel:+393299736697" style="color:#7a1d52; font-weight:700">Chiama ora: +39 329 973 6697</a></p>
</div>'''
        phone_tag = BeautifulSoup(phone_cta, 'html.parser')
        h1.insert_after(phone_tag)

# 5. Replace CTA
print("  → Replacing CTA with optimized version...")
notices = soup.find_all('div', class_='notice')
for notice in notices:
    strong = notice.find('strong')
    if strong and 'Contatta' in strong.get_text():
        new_cta = '''<div class="notice cta-standard">
<strong>Stai pianificando una ristrutturazione?</strong>
<p>Studio 4e a Palermo dal 2002. <strong>Preventivo e primo confronto gratuiti</strong>. Sopralluogo, progetto, pratiche e direzione lavori.</p>
<p style="margin-top:12px">
<a class="btn" href="tel:+393299736697">📞 Chiama: +39 329 973 6697</a>
<a class="btn secondary" href="/inizia-da-qui/" style="margin-left:10px">Inizia da qui</a>
</p>
<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 4.8/5 su Houzz • 20+ anni di esperienza • 50+ progetti in Sicilia</p>
</div>'''
        new_tag = BeautifulSoup(new_cta, 'html.parser')
        notice.replace_with(new_tag)
        break

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("")
print("✅ All fixes applied!")
EOFPYTHON

# Run test script
python3 _test_single.py "$TEST_FILE"

# Clean up
rm _test_single.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TEST COMPLETED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 Modified file: $TEST_FILE"
echo "💾 Original backup: $BACKUP_FILE"
echo ""
echo "🔍 Next steps:"
echo ""
echo "1. Open the modified file in browser:"
echo "   open $TEST_FILE"
echo ""
echo "2. Verify changes:"
echo "   ✓ Phone CTA appears after H1"
echo "   ✓ New CTA box with rating and social proof"
echo "   ✓ Page loads correctly"
echo ""
echo "3. Check structured data validity:"
echo "   https://search.google.com/test/rich-results"
echo "   Paste your page URL and validate"
echo ""
echo "4. If everything looks good, run full optimization:"
echo "   python3 fix-structured-data.py"
echo "   python3 add-social-proof.py"
echo ""
echo "5. To restore original:"
echo "   cp $BACKUP_FILE $TEST_FILE"
echo ""
