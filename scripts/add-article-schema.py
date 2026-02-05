#!/usr/bin/env python3
"""
Script per aggiungere Article Schema (BlogPosting) a tutti gli articoli
e correggere gli URL relativi in assoluti nel JSON-LD.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

BASE_URL = "https://architettisicilia.it"
STUDIO_URL = "https://www.studio4e.it/"

def extract_meta(html, name, attr="name"):
    """Estrae il contenuto di un meta tag."""
    pattern = rf'<meta\s+{attr}=["\']([^"\']+)["\']\s+content=["\']([^"\']+)["\']'
    match = re.search(pattern, html, re.IGNORECASE)
    if match and match.group(1).lower() == name.lower():
        return match.group(2)

    pattern = rf'<meta\s+content=["\']([^"\']+)["\']\s+{attr}=["\']([^"\']+)["\']'
    match = re.search(pattern, html, re.IGNORECASE)
    if match and match.group(2).lower() == name.lower():
        return match.group(1)
    return None

def extract_title(html):
    """Estrae il titolo dalla pagina."""
    match = re.search(r'<title>([^<]+)</title>', html)
    return match.group(1) if match else ""

def extract_h1(html):
    """Estrae l'H1 dalla pagina."""
    match = re.search(r'<h1>([^<]+)</h1>', html)
    return match.group(1) if match else ""

def create_article_schema(title, description, url, lang="en"):
    """Crea lo schema Article/BlogPosting."""
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title[:110] if title else "",
        "description": description or "",
        "url": url,
        "inLanguage": lang,
        "datePublished": "2025-01-15",
        "dateModified": datetime.now().strftime("%Y-%m-%d"),
        "author": {
            "@type": "Organization",
            "name": "Studio 4e",
            "url": STUDIO_URL
        },
        "publisher": {
            "@type": "Organization",
            "name": "Architetti Sicilia",
            "url": BASE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/assets/images/studio4e-logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        },
        "image": f"{BASE_URL}/assets/images/og.jpg"
    }
    return schema

def fix_relative_urls_in_json(html):
    """Corregge gli URL relativi nei JSON-LD."""
    # Pattern per trovare "url": "/something"
    html = re.sub(
        r'"url":\s*"/([^"]+)"',
        rf'"url": "{BASE_URL}/\1"',
        html
    )
    # Corregge anche url: /studio-4e/ -> url assoluto Studio 4e
    html = re.sub(
        rf'"url":\s*"{BASE_URL}/studio-4e/"',
        f'"url": "{STUDIO_URL}"',
        html
    )
    return html

def add_article_schema(html, filepath):
    """Aggiunge Article Schema al file HTML."""
    # Estrai metadati
    title = extract_title(html) or extract_h1(html)
    description = extract_meta(html, "description")

    # Determina la lingua
    lang_match = re.search(r'<html\s+lang=["\'](\w+)["\']', html)
    lang = lang_match.group(1) if lang_match else "en"

    # Costruisci URL
    rel_path = filepath.relative_to(Path("/home/user/architetti-sicilia"))
    url = f"{BASE_URL}/{rel_path}"

    # Crea schema
    schema = create_article_schema(title, description, url, lang)
    schema_json = json.dumps(schema, ensure_ascii=False)
    schema_tag = f'<script data-architetti-sicilia="1" type="application/ld+json">{schema_json}</script>'

    # Verifica se esiste già un Article/BlogPosting schema
    if '"@type": "BlogPosting"' in html or '"@type": "Article"' in html:
        print(f"  [SKIP] Article schema già presente: {filepath.name}")
        return html

    # Trova posizione per inserire (prima di </head>)
    # Inseriamo dopo l'ultimo script JSON-LD esistente
    last_jsonld = html.rfind('</script><meta content="#7a1d52"')
    if last_jsonld == -1:
        last_jsonld = html.rfind('</head>')

    if last_jsonld != -1:
        # Trova la fine dell'ultimo script JSON-LD
        insert_pos = html.rfind('</script>', 0, last_jsonld)
        if insert_pos != -1:
            insert_pos += len('</script>')
            html = html[:insert_pos] + schema_tag + html[insert_pos:]

    return html

def process_file(filepath):
    """Processa un singolo file HTML."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. Correggi URL relativi nel JSON-LD
        html = fix_relative_urls_in_json(html)

        # 2. Aggiungi Article Schema
        html = add_article_schema(html, filepath)

        # 3. Salva
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  [OK] {filepath.name}")
        return True
    except Exception as e:
        print(f"  [ERROR] {filepath.name}: {e}")
        return False

def main():
    base_path = Path("/home/user/architetti-sicilia")

    # Process EN articles
    en_path = base_path / "en"
    print(f"\n=== Processing EN articles ({en_path}) ===")

    count = 0
    for html_file in sorted(en_path.glob("*.html")):
        if html_file.name == "index.html":
            continue
        if process_file(html_file):
            count += 1

    print(f"\nProcessed {count} EN articles")

    # Process guide articles (IT)
    guide_path = base_path / "guide"
    if guide_path.exists():
        print(f"\n=== Processing Guide articles ({guide_path}) ===")
        for province_dir in guide_path.iterdir():
            if province_dir.is_dir():
                for html_file in sorted(province_dir.glob("*.html")):
                    if html_file.name == "index.html":
                        continue
                    process_file(html_file)

if __name__ == "__main__":
    main()
