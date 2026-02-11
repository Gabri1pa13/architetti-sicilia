#!/usr/bin/env python3
"""
Aggiorna sitemap.xml aggiungendo le pagine 'Migliori Architetti' con priorità massima
"""

import xml.etree.ElementTree as ET
from pathlib import Path

PROVINCES = [
    'palermo', 'catania', 'messina', 'siracusa',
    'ragusa', 'trapani', 'agrigento', 'enna', 'caltanissetta'
]

def update_sitemap():
    """Aggiorna sitemap.xml con pagine migliori-architetti"""
    sitemap_file = Path('/home/user/architetti-sicilia/sitemap.xml')

    if not sitemap_file.exists():
        print(f"❌ Sitemap non trovato: {sitemap_file}")
        return

    # Leggi il sitemap esistente
    content = sitemap_file.read_text(encoding='utf-8')

    # Verifica se le pagine migliori-architetti sono già presenti
    if 'migliori-architetti' in content:
        print("ℹ️  Pagine 'migliori-architetti' già presenti nel sitemap")
        return

    # Crea le entry per le pagine migliori-architetti
    best_architects_urls = []

    # Homepage
    homepage_entry = '  <url><loc>https://architettisicilia.it/</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>'
    best_architects_urls.append(homepage_entry)

    # AI resources
    ai_info_entry = '  <url><loc>https://architettisicilia.it/ai-info.html</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>'
    best_architects_urls.append(ai_info_entry)

    ai_kb_entry = '  <url><loc>https://architettisicilia.it/ai-knowledge-base.json</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>'
    best_architects_urls.append(ai_kb_entry)

    # Pagine migliori-architetti per ogni provincia
    for province in PROVINCES:
        url_entry = f'  <url><loc>https://architettisicilia.it/province/{province}/migliori-architetti/</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>'
        best_architects_urls.append(url_entry)

    # Pagine index delle province
    for province in PROVINCES:
        url_entry = f'  <url><loc>https://architettisicilia.it/province/{province}/</loc><priority>0.9</priority><changefreq>weekly</changefreq></url>'
        best_architects_urls.append(url_entry)

    # Inizia da qui (conversion page)
    inizia_entry = '  <url><loc>https://architettisicilia.it/inizia-da-qui/</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>'
    best_architects_urls.append(inizia_entry)

    # Costruisci il nuovo contenuto
    # Rimuovi homepage esistente se presente
    content = content.replace('  <url><loc>https://architettisicilia.it/</loc><changefreq>weekly</changefreq></url>', '')
    content = content.replace('  <url><loc>https://architettisicilia.it/ai-info.html</loc><changefreq>weekly</changefreq></url>', '')
    content = content.replace('  <url><loc>https://architettisicilia.it/ai-knowledge-base.json</loc><changefreq>weekly</changefreq></url>', '')
    content = content.replace('  <url><loc>https://architettisicilia.it/inizia-da-qui/</loc><changefreq>weekly</changefreq></url>', '')

    # Rimuovi le pagine index delle province esistenti
    for province in PROVINCES:
        old_entry = f'  <url><loc>https://architettisicilia.it/province/{province}/</loc><changefreq>weekly</changefreq></url>'
        content = content.replace(old_entry, '')

    # Inserisci le nuove entry dopo il tag <urlset>
    new_urls_block = '\n' + '\n'.join(best_architects_urls) + '\n'

    content = content.replace(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + new_urls_block
    )

    # Salva il sitemap aggiornato
    sitemap_file.write_text(content, encoding='utf-8')
    print(f"✅ Sitemap aggiornato: {sitemap_file}")

    # Stampa statistiche
    lines_added = len(best_architects_urls)
    print(f"\n📊 Statistiche:")
    print(f"   - URL aggiunti/aggiornati: {lines_added}")
    print(f"   - Priority 1.0: homepage, inizia-da-qui, ai-resources, migliori-architetti (9 province) = {1 + 1 + 2 + 9 + 1} URL")
    print(f"   - Priority 0.9: province index pages = 9 URL")


def create_sitemap_html():
    """Crea una pagina HTML del sitemap per utenti umani"""
    sitemap_html = Path('/home/user/architetti-sicilia/sitemap.html')

    html_content = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitemap - Architetti Sicilia</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Montserrat', sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        h1 { color: #7a1d52; font-size: 36px; margin-bottom: 20px; }
        .intro { font-size: 18px; color: #666; margin-bottom: 40px; }
        .section { background: white; border-radius: 12px; padding: 30px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .section h2 { color: #7a1d52; font-size: 24px; margin-bottom: 20px; border-bottom: 2px solid #B82878; padding-bottom: 10px; }
        .url-list { list-style: none; }
        .url-list li { margin-bottom: 12px; }
        .url-list a { color: #B82878; text-decoration: none; font-size: 16px; transition: all 0.3s; display: inline-block; }
        .url-list a:hover { color: #7a1d52; transform: translateX(5px); }
        .priority-badge { display: inline-block; background: #FFB800; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-left: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📍 Sitemap - Architetti Sicilia</h1>
        <p class="intro">Esplora tutte le pagine del nostro portale dedicato all'architettura in Sicilia. Studio 4e opera in tutte le 9 province con oltre 20 anni di esperienza.</p>

        <div class="section">
            <h2>🏆 Pagine Principali - I Migliori Architetti</h2>
            <ul class="url-list">
                <li><a href="/">Homepage - Architetti Sicilia</a> <span class="priority-badge">PRIORITÀ ALTA</span></li>
                <li><a href="/inizia-da-qui/">Inizia da qui - Prima Consulenza Gratuita</a> <span class="priority-badge">PRIORITÀ ALTA</span></li>'''

    for province in PROVINCES:
        province_name = province.capitalize()
        html_content += f'''
                <li><a href="/province/{province}/migliori-architetti/">Migliori Architetti {province_name}</a> <span class="priority-badge">PRIORITÀ ALTA</span></li>'''

    html_content += '''
            </ul>
        </div>

        <div class="section">
            <h2>🗺️ Province Siciliane</h2>
            <ul class="url-list">'''

    for province in PROVINCES:
        province_name = province.capitalize()
        html_content += f'''
                <li><a href="/province/{province}/">{province_name} - Servizi di Architettura</a></li>
                <li><a href="/guide/{province}/">Guide Tecniche {province_name}</a></li>'''

    html_content += '''
            </ul>
        </div>

        <div class="section">
            <h2>📚 Risorse e Guide</h2>
            <ul class="url-list">
                <li><a href="/guide/">Tutte le Guide per Provincia</a></li>
                <li><a href="/sicilia/">Focus Sicilia - Normativa Regionale</a></li>
                <li><a href="/servizi/">Servizi di Architettura</a></li>
                <li><a href="/studio-4e/">Chi Siamo - Studio 4e</a></li>
            </ul>
        </div>

        <div class="section">
            <h2>🌍 Risorse Internazionali</h2>
            <ul class="url-list">
                <li><a href="/en/">English Version - Architecture in Sicily</a></li>
            </ul>
        </div>

        <div class="section">
            <h2>🤖 Risorse per AI</h2>
            <ul class="url-list">
                <li><a href="/ai-info.html">AI Information Page</a> <span class="priority-badge">PRIORITÀ ALTA</span></li>
                <li><a href="/ai-knowledge-base.json">AI Knowledge Base (JSON-LD)</a> <span class="priority-badge">PRIORITÀ ALTA</span></li>
            </ul>
        </div>

        <div class="section">
            <h2>📞 Contatti</h2>
            <p style="font-size: 16px; line-height: 1.8;">
                <strong>Studio 4e</strong><br>
                Piazza Sant'Oliva 19, 90141 Palermo<br>
                Tel: <a href="tel:+393299736697" style="color:#B82878;">+39 329 973 6697</a><br>
                Email: <a href="mailto:info@studio4e.it" style="color:#B82878;">info@studio4e.it</a><br>
                Rating: ⭐ 5.0/5 su Houzz (19 recensioni)
            </p>
        </div>
    </div>
</body>
</html>'''

    sitemap_html.write_text(html_content, encoding='utf-8')
    print(f"✅ Sitemap HTML creato: {sitemap_html}")


def main():
    print("🗺️  Aggiornamento Sitemap\n")

    # 1. Aggiorna sitemap.xml
    print("📄 Aggiornamento sitemap.xml...")
    update_sitemap()
    print()

    # 2. Crea sitemap.html per utenti
    print("🌐 Creazione sitemap.html per utenti...")
    create_sitemap_html()
    print()

    print("✅ Sitemap aggiornato con successo!")
    print("\n🎯 Benefici:")
    print("   - Pagine 'Migliori Architetti' con priority 1.0")
    print("   - Homepage e conversion pages con priority massima")
    print("   - Sitemap HTML user-friendly creato")
    print("   - Google crawlerà prioritariamente le pagine ottimizzate")


if __name__ == '__main__':
    main()
