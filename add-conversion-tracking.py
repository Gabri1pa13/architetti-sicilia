#!/usr/bin/env python3
"""
Add conversion tracking and GTM to all HTML files
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path(".")

# GTM snippet (replace GTM-XXXXX with your actual GTM ID)
GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXX');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

# Conversion tracking script
CONVERSION_SCRIPT = """<script>
// Conversion tracking events
(function() {
  const dataLayer = window.dataLayer || [];

  // Track phone clicks
  document.addEventListener('click', function(e) {
    const phoneLink = e.target.closest('a[href^="tel:"]');
    if (phoneLink) {
      dataLayer.push({
        'event': 'click_phone',
        'phone_number': phoneLink.getAttribute('href'),
        'page_path': window.location.pathname,
        'page_title': document.title
      });
    }

    // Track WhatsApp clicks
    const waLink = e.target.closest('a[href*="wa.me"]');
    if (waLink) {
      dataLayer.push({
        'event': 'click_whatsapp',
        'page_path': window.location.pathname,
        'page_title': document.title
      });
    }
  });

  // Track form submissions
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      dataLayer.push({
        'event': 'form_submit',
        'form_id': this.id || 'unknown',
        'page_path': window.location.pathname
      });
    });
  });
})();
</script>"""

def add_tracking(filepath):
    """Add GTM and conversion tracking to HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Check if GTM already exists
    if soup.find(string=lambda text: 'googletagmanager.com/gtm.js' in text if text else False):
        return False

    # Add GTM to <head>
    head = soup.find('head')
    if head:
        gtm_head_tag = BeautifulSoup(GTM_HEAD, 'html.parser')
        head.insert(0, gtm_head_tag)

    # Add GTM noscript to <body>
    body = soup.find('body')
    if body:
        gtm_body_tag = BeautifulSoup(GTM_BODY, 'html.parser')
        body.insert(0, gtm_body_tag)

    # Add conversion tracking script before </body>
    if body:
        tracking_script = BeautifulSoup(CONVERSION_SCRIPT, 'html.parser')
        body.append(tracking_script)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return True

def main():
    print("🚀 Adding conversion tracking...")
    print()
    print("⚠️  IMPORTANT: Replace 'GTM-XXXXX' with your actual Google Tag Manager ID")
    print("⚠️  in this script before running!")
    print()

    response = input("Have you updated the GTM ID? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Aborted. Please update GTM ID first.")
        return

    html_files = list(ROOT_DIR.rglob("*.html"))
    processed = 0

    for filepath in html_files:
        if 'backup-original' in str(filepath):
            continue

        if add_tracking(filepath):
            processed += 1
            print(f"✅ {filepath}")

    print()
    print(f"✅ Done! Added tracking to {processed} files")
    print()
    print("Next steps:")
    print("1. Create Google Tag Manager account if you don't have one")
    print("2. Set up triggers and tags in GTM:")
    print("   - click_phone event")
    print("   - click_whatsapp event")
    print("   - form_submit event")
    print("3. Connect GTM to Google Analytics 4")

if __name__ == "__main__":
    main()
