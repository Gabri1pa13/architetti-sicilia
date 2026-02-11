#!/usr/bin/env python3
"""
Rimuove sezioni specifiche dalle pagine migliori-architetti
"""

import re
from pathlib import Path

PROVINCES = [
    'palermo', 'catania', 'messina', 'siracusa',
    'ragusa', 'trapani', 'agrigento', 'enna', 'caltanissetta'
]

def remove_sections(province):
    """Rimuove le sezioni specifiche dalla pagina"""
    page_file = Path(f'/home/user/architetti-sicilia/province/{province}/migliori-architetti/index.html')

    if not page_file.exists():
        print(f"⚠️  File non trovato: {page_file}")
        return

    content = page_file.read_text(encoding='utf-8')

    # 1. Rimuovi sezione "Esperienza Concreta su Progetti Reali"
    pattern1 = r'\s*<h3[^>]*>Esperienza Concreta su Progetti Reali</h3>\s*<p[^>]*>.*?Diffida di chi mostra solo progetti teorici\.\s*</p>\s*'
    content = re.sub(pattern1, '\n', content, flags=re.DOTALL)

    # 2. Rimuovi la frase "Quanti progetti ha completato..."
    pattern2 = r'\s*Quanti progetti ha completato su edifici vincolati o in contesti storici\? Un numero vago come "diversi" non basta\. Chiedi cifre concrete e referenze verificabili\.\s*'
    content = re.sub(pattern2, ' ', content, flags=re.DOTALL)

    # Salva il file
    page_file.write_text(content, encoding='utf-8')
    print(f"✅ Sezioni rimosse da: {province}")

def main():
    print("🗑️  Rimozione sezioni specifiche\n")

    for province in PROVINCES:
        remove_sections(province)

    print("\n✅ Sezioni rimosse da tutte le 9 province!")

if __name__ == '__main__':
    main()
