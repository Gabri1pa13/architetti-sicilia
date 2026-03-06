#!/usr/bin/env python3
"""
Rimuove lo schema WebSite duplicato con URL sbagliato.

In molte pagine esiste un secondo script JSON-LD con data-site="architetti-sicilia"
che contiene un WebSite schema con l'URL della pagina specifica (non homepage).
Questo è sbagliato: WebSite schema deve sempre avere l'URL dell'homepage.

Lo schema corretto con data-architetti-sicilia="1" è già presente e corretto.
Questo script rimuove il blocco errato (data-site="architetti-sicilia") dalle pagine.
"""

import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

# Pattern del blocco schema da rimuovere
# <script data-site="architetti-sicilia" type="application/ld+json">...</script>
PATTERN = re.compile(
    r'<script data-site="architetti-sicilia" type="application/ld\+json">.*?</script>',
    re.DOTALL,
)


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if 'data-site="architetti-sicilia"' not in content:
        return False

    new_content = PATTERN.sub("", content)

    if new_content == content:
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    dirs = ["sicilia", "guide", "province", "en"]

    fixed = 0

    for d in dirs:
        target = ROOT_DIR / d
        if not target.exists():
            continue
        for filepath in sorted(target.rglob("*.html")):
            if process_file(filepath):
                fixed += 1

    print(f"✅ Schema WebSite duplicato rimosso: {fixed} file")


if __name__ == "__main__":
    main()
