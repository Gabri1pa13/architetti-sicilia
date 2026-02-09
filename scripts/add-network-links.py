#!/usr/bin/env python3
"""
Add cross-site network links to all HTML pages for SEO interlinking.

Changes:
1. Adds "Studio 4e in Sicilia" footer links to all pages (except homepage, already done)
2. Adds contextual sister-site links in province guide index pages
3. Updates Organization structured data with sameAs on all pages that have it
"""

import os
import re
import json

BASE_DIR = "/home/user/architetti-sicilia"

# Network sites (excluding the current site architettisicilia.it)
NETWORK_FOOTER = (
    '<div style="margin-top:10px; padding-top:10px; border-top:1px solid rgba(0,0,0,.06); font-size:12px">'
    'Studio 4e in Sicilia: '
    '<a href="https://architettisicilia.it">Architetti Sicilia</a> · '
    '<a href="https://architettipalermo.com">Architetti Palermo</a> · '
    '<a href="https://architetticatania.it">Architetti Catania</a> · '
    '<a href="https://architettitrapani.com">Architetti Trapani</a> · '
    '<a href="https://architettitaormina.it">Architetti Taormina</a>'
    '</div>'
)

# Province-to-sister-site mapping
PROVINCE_SITE_MAP = {
    "palermo": {
        "url": "https://architettipalermo.com",
        "name": "Architetti Palermo",
        "desc": "Portale dedicato a ristrutturazioni, pratiche edilizie e interior design a Palermo"
    },
    "catania": {
        "url": "https://architetticatania.it",
        "name": "Architetti Catania",
        "desc": "Architettura di lusso, sicurezza sismica e investimenti immobiliari nell'area etnea"
    },
    "trapani": {
        "url": "https://architettitrapani.com",
        "name": "Architetti Trapani",
        "desc": "Design contemporaneo, ville e restauro nella Sicilia occidentale"
    },
    "messina": {
        "url": "https://architettitaormina.it",
        "name": "Architetti Taormina",
        "desc": "Hospitality, luxury villas e vincoli paesaggistici nell'area di Taormina e Messina"
    },
}

SAME_AS_URLS = [
    "https://architettipalermo.com",
    "https://architetticatania.it",
    "https://architettitrapani.com",
    "https://architettitaormina.it",
    "https://www.houzz.it/professionisti/architetti-e-progettisti-di-interni/studio-4e-pfvwit-pf~1234567890"
]


def find_html_files(base_dir):
    """Find all HTML files, excluding backups, scripts, reports."""
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        # Skip non-content directories
        skip_dirs = ['backup-original', 'scripts', 'reports', '.git', 'node_modules']
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for f in files:
            if f.endswith('.html'):
                full_path = os.path.join(root, f)
                html_files.append(full_path)
    return html_files


def add_footer_network_links(content, filepath):
    """Add network links to the footer of a page."""
    # Skip homepage (already manually updated)
    if filepath == os.path.join(BASE_DIR, "index.html"):
        return content

    # Skip if already has network links
    if 'Studio 4e in Sicilia:' in content:
        return content

    # Pattern: find the closing of the footer div
    # Internal pages use: <div class="footer">...<div style="margin-top:8px">...</div></div></div>
    # The footer ends with </div></div></div> before <details class="contact-fab"

    # Try to insert before the closing of footer container
    # Look for the disclaimer div followed by footer closing divs

    # Pattern for internal pages (minified HTML)
    pattern = r'(Contenuti informativi, senza prezzi e senza promesse assolute\. Ogni intervento richiede verifiche sul caso specifico\.</div>)(</div></div>)'
    replacement = r'\1' + NETWORK_FOOTER + r'\2'

    new_content = re.sub(pattern, replacement, content, count=1)
    if new_content != content:
        return new_content

    # Fallback: try to find footer closing pattern
    # Some pages might have slightly different footer text
    pattern2 = r'(<div class="footer">.*?)(</div>\s*</div>\s*</div>\s*<details)'

    def insert_before_close(m):
        footer_content = m.group(1)
        closing = m.group(2)
        # Insert network links before the last closing divs
        return footer_content + NETWORK_FOOTER + closing

    new_content = re.sub(pattern2, insert_before_close, content, count=1, flags=re.DOTALL)
    return new_content


def add_province_contextual_link(content, filepath):
    """Add contextual link to sister site in province guide index pages."""
    # Only modify guide/[province]/index.html files
    rel_path = os.path.relpath(filepath, BASE_DIR)

    match = re.match(r'guide/(\w+)/index\.html$', rel_path)
    if not match:
        return content

    province = match.group(1)
    if province not in PROVINCE_SITE_MAP:
        return content

    site = PROVINCE_SITE_MAP[province]

    # Skip if link already exists
    if site["url"] in content:
        return content

    # Add a notice box with the sister site link before the existing CTA notice
    # Find the related-links section and add our link there
    sister_link = (
        f'<li><a href="{site["url"]}" target="_blank" rel="noopener">'
        f'{site["name"]} — {site["desc"]}</a></li>'
    )

    # Insert into the related-links section's <ul>
    pattern = r'(<section id="related-links"><h2>Approfondimenti utili</h2><p>Percorsi rapidi: servizi locali e guide correlate\.</p><ul>)'
    replacement = r'\1' + sister_link

    new_content = re.sub(pattern, replacement, content, count=1)
    return new_content


def update_structured_data_sameas(content, filepath):
    """Add sameAs to Organization structured data."""
    # Skip homepage (already manually updated)
    if filepath == os.path.join(BASE_DIR, "index.html"):
        return content

    # Skip if already has sameAs
    if '"sameAs"' in content:
        return content

    # Find Organization schema and add sameAs
    # Pattern: Organization schema in data-architetti-sicilia script
    org_pattern = r'("@type":\s*"Organization",\s*"name":\s*"Studio 4e",\s*"url":\s*"https://www\.studio4e\.it/"[^}]*?"addressCountry":\s*"IT"\s*\})'

    def add_sameas(m):
        org_json = m.group(1)
        sameas_str = ', "sameAs": ' + json.dumps(SAME_AS_URLS)
        # Insert sameAs before the last closing brace of the address, then close properly
        # Actually we need to add it at the Organization level, after the address object closes
        return org_json + sameas_str

    new_content = re.sub(org_pattern, add_sameas, content, count=1)
    if new_content != content:
        return new_content

    # Try simpler pattern for pages with Organization schema
    # Many internal pages have a simpler Organization schema
    org_pattern2 = r'("@type":\s*"Organization",\s*"name":\s*"Studio 4e",\s*"url":\s*"/studio-4e/"[^}]*?\})'

    def add_sameas2(m):
        org_json = m.group(1)
        # Remove the last } and add sameAs
        return org_json[:-1] + ', "sameAs": ' + json.dumps(SAME_AS_URLS) + '}'

    new_content = re.sub(org_pattern2, add_sameas2, content, count=1)
    return new_content


def process_file(filepath):
    """Process a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, IOError):
        return False

    original = content

    # 1. Add footer network links
    content = add_footer_network_links(content, filepath)

    # 2. Add contextual province links
    content = add_province_contextual_link(content, filepath)

    # 3. Update structured data
    content = update_structured_data_sameas(content, filepath)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    html_files = find_html_files(BASE_DIR)
    print(f"Found {len(html_files)} HTML files")

    modified = 0
    footer_added = 0
    province_added = 0
    schema_added = 0

    for filepath in sorted(html_files):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                before = f.read()
        except (UnicodeDecodeError, IOError):
            continue

        after = before

        # Track individual changes
        after_footer = add_footer_network_links(after, filepath)
        if after_footer != after:
            footer_added += 1
        after = after_footer

        after_province = add_province_contextual_link(after, filepath)
        if after_province != after:
            province_added += 1
        after = after_province

        after_schema = update_structured_data_sameas(after, filepath)
        if after_schema != after:
            schema_added += 1
        after = after_schema

        if after != before:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(after)
            modified += 1
            rel = os.path.relpath(filepath, BASE_DIR)
            print(f"  Modified: {rel}")

    print(f"\nDone. Modified {modified}/{len(html_files)} files.")
    print(f"  Footer links added: {footer_added}")
    print(f"  Province contextual links added: {province_added}")
    print(f"  Schema sameAs added: {schema_added}")


if __name__ == "__main__":
    main()
