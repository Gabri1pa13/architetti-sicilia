#!/usr/bin/env python3
"""
Rimuove il paragrafo "Quanti progetti ha completato..." dalle pagine migliori-architetti
"""

import re
from pathlib import Path

PROVINCES = [
    'palermo', 'catania', 'messina', 'siracusa',
    'ragusa', 'trapani', 'agrigento', 'enna', 'caltanissetta'
]

def remove_paragraph(province):
    """Rimuove il paragrafo specifico dalla pagina"""
    page_file = Path(f'/home/user/architetti-sicilia/province/{province}/migliori-architetti/index.html')

    if not page_file.exists():
        print(f"⚠️  File non trovato: {page_file}")
        return

    content = page_file.read_text(encoding='utf-8')

    # Pattern per matchare l'intero paragrafo con il tag strong
    pattern = r'\s*<p[^>]*>\s*<strong>Quanti progetti ha completato su edifici vincolati o in contesti storici\?</strong>.*?Chiedi cifre concrete e referenze verificabili\.\s*</p>\s*'

    content = re.sub(pattern, '\n', content, flags=re.DOTALL)

    # Salva il file
    page_file.write_text(content, encoding='utf-8')
    print(f"✅ Paragrafo rimosso da: {province}")

def main():
    print("🗑️  Rimozione paragrafo 'Quanti progetti ha completato...'\n")

    for province in PROVINCES:
        remove_paragraph(province)

    print("\n✅ Paragrafo rimosso da tutte le 9 province!")

if __name__ == '__main__':
    main()
