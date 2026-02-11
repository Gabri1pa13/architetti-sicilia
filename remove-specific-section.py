#!/usr/bin/env python3
"""
Rimuove la sezione 'Esperienza Concreta su Progetti Reali' dalle pagine migliori-architetti
"""

import re
from pathlib import Path

PROVINCES = [
    'palermo', 'catania', 'messina', 'siracusa',
    'ragusa', 'trapani', 'agrigento', 'enna', 'caltanissetta'
]

def remove_section(province):
    """Rimuove la sezione specifica dalla pagina"""
    page_file = Path(f'/home/user/architetti-sicilia/province/{province}/migliori-architetti/index.html')

    if not page_file.exists():
        print(f"⚠️  File non trovato: {page_file}")
        return

    content = page_file.read_text(encoding='utf-8')

    # Pattern per trovare la sezione H3 + paragrafo
    pattern = r'<h3[^>]*>Esperienza Concreta su Progetti Reali</h3>\s*<p[^>]*>La prima cosa da verificare.*?Diffida di chi mostra solo progetti teorici\.</p>'

    # Rimuovi la sezione
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Salva il file
    page_file.write_text(content, encoding='utf-8')
    print(f"✅ Sezione rimossa da: {province}")

def main():
    print("🗑️  Rimozione sezione 'Esperienza Concreta su Progetti Reali'\n")

    for province in PROVINCES:
        remove_section(province)

    print("\n✅ Sezione rimossa da tutte le 9 province!")

if __name__ == '__main__':
    main()
