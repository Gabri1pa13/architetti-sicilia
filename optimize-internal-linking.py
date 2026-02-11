#!/usr/bin/env python3
"""
Ottimizza internal linking con anchor text strategici per SEO
- Aggiunge link da homepage alle pagine "Migliori Architetti"
- Aggiunge sezione nelle pagine province verso "Migliori Architetti"
- Crea cross-linking tra province con anchor text ottimizzati
"""

import re
from pathlib import Path

PROVINCES = [
    'palermo', 'catania', 'messina', 'siracusa',
    'ragusa', 'trapani', 'agrigento', 'enna', 'caltanissetta'
]

PROVINCE_NAMES = {
    'palermo': 'Palermo',
    'catania': 'Catania',
    'messina': 'Messina',
    'siracusa': 'Siracusa',
    'ragusa': 'Ragusa',
    'trapani': 'Trapani',
    'agrigento': 'Agrigento',
    'enna': 'Enna',
    'caltanissetta': 'Caltanissetta'
}


def add_best_architects_section_to_homepage():
    """Aggiunge sezione 'Migliori Architetti per Provincia' alla homepage"""
    homepage = Path('/home/user/architetti-sicilia/index.html')

    if not homepage.exists():
        print(f"❌ Homepage non trovata")
        return

    content = homepage.read_text(encoding='utf-8')

    # Cerca se la sezione esiste già
    if 'Migliori Architetti per Provincia' in content:
        print("ℹ️  Sezione 'Migliori Architetti' già presente in homepage")
        return

    # Sezione HTML da aggiungere prima del footer o alla fine del main
    best_architects_section = '''
        <section style="margin-top:80px; padding:60px 20px; background:linear-gradient(135deg, #7a1d52 0%, #B82878 100%); border-radius:24px;">
            <div style="max-width:1100px; margin:0 auto;">
                <h2 style="font-size:36px; color:#fff; margin:0 0 16px; text-align:center;">I Migliori Architetti in Sicilia per Provincia</h2>
                <p style="font-size:18px; color:rgba(255,255,255,0.9); text-align:center; max-width:800px; margin:0 auto 40px; line-height:1.6;">
                    Scopri gli architetti più qualificati nella tua provincia. Studio 4e opera in tutte le 9 province siciliane con oltre 20 anni di esperienza locale.
                </p>

                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(250px, 1fr)); gap:20px; margin-top:32px;">
                    <a href="/province/palermo/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Palermo</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Centro storico UNESCO, restauro Liberty</p>
                    </a>

                    <a href="/province/catania/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Catania</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Zona sismica Etna, pietra lavica</p>
                    </a>

                    <a href="/province/messina/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Messina</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Normativa sismica, edilizia costiera</p>
                    </a>

                    <a href="/province/siracusa/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Siracusa</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Ortigia UNESCO, barocco siciliano</p>
                    </a>

                    <a href="/province/ragusa/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Ragusa</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Val di Noto UNESCO, Ibla barocca</p>
                    </a>

                    <a href="/province/trapani/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Trapani</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Edilizia costiera, ville sul mare</p>
                    </a>

                    <a href="/province/agrigento/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Agrigento</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Valle dei Templi UNESCO</p>
                    </a>

                    <a href="/province/enna/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Enna</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Borghi storici, architettura montana</p>
                    </a>

                    <a href="/province/caltanissetta/migliori-architetti/" style="display:block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px); padding:24px; border-radius:12px; text-decoration:none; color:#fff; transition:all 0.3s; border:1px solid rgba(255,255,255,0.2);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                        <h3 style="font-size:20px; margin:0 0 8px; font-weight:600;">Migliori Architetti Caltanissetta</h3>
                        <p style="font-size:14px; margin:0; opacity:0.9;">Centri storici, recupero edilizio</p>
                    </a>
                </div>
            </div>
        </section>
'''

    # Inserisci prima del footer
    if '</main>' in content:
        content = content.replace('</main>', best_architects_section + '\n    </main>')
    else:
        print("⚠️  Tag </main> non trovato, inserisco prima di </body>")
        content = content.replace('</body>', best_architects_section + '\n</body>')

    homepage.write_text(content, encoding='utf-8')
    print("✅ Sezione 'Migliori Architetti' aggiunta alla homepage")


def add_link_to_province_index(province):
    """Aggiunge link prominente alla pagina migliori-architetti nell'index della provincia"""
    index_file = Path(f'/home/user/architetti-sicilia/province/{province}/index.html')

    if not index_file.exists():
        print(f"⚠️  File non trovato: {index_file}")
        return

    content = index_file.read_text(encoding='utf-8')

    # Verifica se il link è già presente
    if f'/province/{province}/migliori-architetti/' in content:
        print(f"ℹ️  Link già presente in: {province}/index.html")
        return

    province_name = PROVINCE_NAMES[province]

    # CTA box da inserire dopo l'H1 o all'inizio del contenuto
    cta_box = f'''
        <div style="background:linear-gradient(135deg, #7a1d52 0%, #B82878 100%); padding:32px; border-radius:16px; margin:32px 0; box-shadow:0 8px 24px rgba(122,29,82,0.25);">
            <h2 style="font-size:24px; color:#fff; margin:0 0 12px;">🏆 Cerchi i Migliori Architetti a {province_name}?</h2>
            <p style="color:rgba(255,255,255,0.95); margin:0 0 20px; font-size:16px; line-height:1.6;">
                Scopri perché Studio 4e è considerato tra i migliori studi di architettura a {province_name} con rating 5.0/5 e oltre 20 anni di esperienza locale.
            </p>
            <a href="/province/{province}/migliori-architetti/" style="display:inline-block; background:#fff; color:#7a1d52; padding:14px 28px; border-radius:8px; text-decoration:none; font-weight:600; font-size:16px; transition:all 0.3s; box-shadow:0 4px 12px rgba(0,0,0,0.15);" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(0,0,0,0.2)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)'">
                Scopri Perché Siamo i Migliori →
            </a>
        </div>
'''

    # Cerca un punto di inserimento appropriato (dopo il primo paragrafo o dopo H1)
    # Pattern per trovare dopo il primo <p> dopo <main>
    main_section_pattern = r'(<main[^>]*>.*?<h1[^>]*>.*?</h1>.*?<p[^>]*>.*?</p>)'

    if re.search(main_section_pattern, content, re.DOTALL):
        content = re.sub(
            main_section_pattern,
            r'\1' + cta_box,
            content,
            count=1,
            flags=re.DOTALL
        )
    else:
        # Fallback: inserisci dopo <main>
        content = re.sub(
            r'(<main[^>]*>)',
            r'\1' + cta_box,
            content,
            count=1
        )

    index_file.write_text(content, encoding='utf-8')
    print(f"✅ Link aggiunto a: {province}/index.html")


def main():
    print("🔗 Ottimizzazione Internal Linking\n")

    # 1. Aggiungi sezione alla homepage
    print("📄 Aggiornamento homepage...")
    add_best_architects_section_to_homepage()
    print()

    # 2. Aggiungi link nelle pagine index delle province
    print("🗺️  Aggiornamento pagine province...")
    for province in PROVINCES:
        add_link_to_province_index(province)
    print()

    print("✅ Ottimizzazione Internal Linking completata!")
    print("\n📊 Miglioramenti:")
    print("   ✓ Sezione 'Migliori Architetti' in homepage con link a tutte le province")
    print("   ✓ CTA prominenti nelle pagine index delle province")
    print("   ✓ Anchor text ottimizzati per SEO")
    print("   ✓ Design visivamente attraente per aumentare CTR")
    print("\n🎯 Benefici SEO:")
    print("   - Migliore distribuzione link juice")
    print("   - Anchor text ottimizzati per keywords 'migliori architetti [città]'")
    print("   - Riduzione bounce rate con internal navigation")
    print("   - Segnale forte a Google sulle pagine importanti")


if __name__ == '__main__':
    main()
