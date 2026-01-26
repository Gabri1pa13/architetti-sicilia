#!/usr/bin/env python3
"""
Fix critical SEO issues across all HTML files:
1. Remove HTML tags from JSON-LD structured data
2. Fix title tags (remove <span> and <a> tags)
3. Add lazy loading to images
4. Extract inline CSS to external file
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import html

# Configuration
ROOT_DIR = Path(".")
BACKUP_DIR = Path("./backup-original")
CSS_OUTPUT = Path("./assets/css/inline-fixes.css")

def backup_file(filepath):
    """Create backup of original file"""
    backup_path = BACKUP_DIR / filepath.relative_to(ROOT_DIR)
    backup_path.parent.mkdir(parents=True, exist_ok=True)

    if not backup_path.exists():
        import shutil
        shutil.copy2(filepath, backup_path)

def clean_json_ld(script_tag):
    """Remove HTML from JSON-LD content"""
    try:
        content = script_tag.string
        if not content:
            return False

        # Unescape HTML entities first
        content = html.unescape(content)

        # Remove <span> tags
        content = re.sub(r'<span[^>]*>', '', content)
        content = re.sub(r'</span>', '', content)

        # Remove <a> tags but keep the text
        content = re.sub(r'<a[^>]*>([^<]+)</a>', r'\1', content)

        # Validate JSON
        try:
            json.loads(content)
            script_tag.string = content
            return True
        except json.JSONDecodeError:
            print(f"  ⚠️  Invalid JSON after cleaning, skipping")
            return False

    except Exception as e:
        print(f"  ⚠️  Error cleaning JSON-LD: {e}")
        return False

def fix_title_tag(soup):
    """Remove HTML tags from <title>"""
    title = soup.find('title')
    if title:
        # Get text content only, strip all HTML
        clean_text = title.get_text(strip=True)
        title.clear()
        title.string = clean_text
        return True
    return False

def add_lazy_loading(soup):
    """Add native lazy loading to images"""
    images = soup.find_all('img')
    count = 0

    for img in images:
        # Skip if already has loading attribute
        if img.get('loading'):
            continue

        # Skip first image (hero/LCP)
        if count == 0:
            img['loading'] = 'eager'
            img['fetchpriority'] = 'high'
        else:
            img['loading'] = 'lazy'
            img['decoding'] = 'async'

        count += 1

    return count

def extract_inline_css(soup, css_file_path):
    """Extract global-fixes-style to external file"""
    style_tag = soup.find('style', id='global-fixes-style')

    if style_tag and style_tag.string:
        css_content = style_tag.string

        # Write to external CSS file (append mode, check if already exists)
        if not css_file_path.exists():
            css_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(css_file_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            print(f"✅ Extracted inline CSS to {css_file_path}")

        # Replace inline style with link to external CSS
        link_tag = soup.new_tag('link', rel='stylesheet', href='/assets/css/inline-fixes.css')
        style_tag.replace_with(link_tag)

        return True

    return False

def process_html_file(filepath):
    """Process single HTML file"""
    print(f"Processing: {filepath}")

    # Backup original
    backup_file(filepath)

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    changes = []

    # 1. Fix JSON-LD structured data
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        if clean_json_ld(script):
            changes.append("JSON-LD cleaned")

    # 2. Fix title tag
    if fix_title_tag(soup):
        changes.append("Title fixed")

    # 3. Add lazy loading
    img_count = add_lazy_loading(soup)
    if img_count > 0:
        changes.append(f"{img_count} images lazy-loaded")

    # 4. Extract inline CSS (only once, first file)
    if extract_inline_css(soup, CSS_OUTPUT):
        changes.append("CSS extracted")

    # Write back
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"  ✅ {', '.join(changes)}")
        return True
    else:
        print(f"  ⏭️  No changes needed")
        return False

def main():
    """Process all HTML files"""
    print("🚀 Starting HTML optimization...")
    print(f"📁 Root directory: {ROOT_DIR.absolute()}")
    print(f"💾 Backups will be saved to: {BACKUP_DIR.absolute()}")
    print()

    # Find all HTML files
    html_files = list(ROOT_DIR.rglob("*.html"))
    print(f"Found {len(html_files)} HTML files")
    print()

    # Process files
    processed = 0
    for filepath in html_files:
        # Skip backup directory
        if BACKUP_DIR in filepath.parents:
            continue

        if process_html_file(filepath):
            processed += 1

    print()
    print(f"✅ Done! Processed {processed}/{len(html_files)} files")
    print(f"📁 Backups saved to: {BACKUP_DIR}")
    print(f"📄 Inline CSS extracted to: {CSS_OUTPUT}")

if __name__ == "__main__":
    main()
