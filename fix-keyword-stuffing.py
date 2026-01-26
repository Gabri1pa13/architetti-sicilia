#!/usr/bin/env python3
"""
Remove keyword stuffing from lede paragraphs
Pattern: "A Città, keyword a città diventa..."
"""

import re
from pathlib import Path

ROOT_DIR = Path(".")

def fix_lede(content):
    """Remove keyword stuffing from lede paragraphs"""

    # Pattern 1: "A Città, keyword a città diventa un problema quando"
    # Replace with: "Quando si lavora su [context], keyword diventa critico quando"

    patterns = [
        # Generic pattern: A [Città], [keyword] a [città] diventa
        (
            r'A ([A-Z][a-zà-ù]+), ([a-zà-ù\s]+) a \1 diventa un problema quando',
            lambda m: f'Quando si lavora su {get_context(m.group(2))}, {m.group(2)} diventa critico quando'
        ),
        # Pattern 2: duplicate city name anywhere
        (
            r'([A-Z][a-zà-ù]+),\s*([a-zà-ù\s]+)\s+a\s+\1',
            lambda m: f'{m.group(1)}, {m.group(2)}'
        ),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    return content

def get_context(keyword):
    """Get natural context for keyword"""
    contexts = {
        'architetto': 'progetti residenziali e commerciali',
        'sanatoria': 'immobili con difformità urbanistiche',
        'ristrutturazione': 'interventi edilizi complessi',
        'cila': 'manutenzione straordinaria e piccoli interventi',
        'scia': 'opere che modificano prospetti o volumi',
        'pratiche': 'iter amministrativi e autorizzazioni',
        'direzione lavori': 'cantieri con più specialità',
        'computo metrico': 'preventivi e gare d\'appalto',
        'capitolato': 'specifiche tecniche e qualità',
        'verifica': 'due diligence e acquisti immobiliari',
        'regolarità': 'compravendite e rogiti',
        'vincoli': 'aree soggette a tutela',
        'cambio destinazione': 'trasformazioni funzionali',
        'frazionamento': 'divisioni catastali',
        'accorpamento': 'unioni immobiliari',
    }

    keyword_lower = keyword.lower().strip()
    for key, context in contexts.items():
        if key in keyword_lower:
            return context

    return 'interventi edilizi'

def fix_lede_simple(content):
    """Simpler approach: just remove duplicate city mentions in lede"""

    # Find lede paragraph
    lede_match = re.search(r'<p class="lede">([^<]+)</p>', content, re.DOTALL)
    if not lede_match:
        return content

    original_lede = lede_match.group(1)

    # Remove pattern: "A Città, keyword a città"
    # Replace with: "A Città, keyword"
    fixed_lede = re.sub(
        r'A ([A-Z][a-zà-ù]+),\s*([^,]+?)\s+a\s+\1',
        r'A \1, \2',
        original_lede,
        flags=re.IGNORECASE
    )

    # If no change, try another pattern
    if fixed_lede == original_lede:
        # Pattern: mentions city twice in first sentence
        cities = ['Palermo', 'Catania', 'Messina', 'Siracusa', 'Trapani',
                  'Ragusa', 'Agrigento', 'Caltanissetta', 'Enna']

        for city in cities:
            # Count occurrences in first 150 chars
            first_part = fixed_lede[:150]
            count = first_part.lower().count(city.lower())

            if count >= 2:
                # Remove second mention
                fixed_lede = re.sub(
                    rf'\b{city}\b',
                    lambda m, c=[0]: m.group(0) if (c.__setitem__(0, c[0] + 1), c[0] == 1)[1] else '',
                    fixed_lede,
                    count=1,
                    flags=re.IGNORECASE
                )
                # Clean up double spaces
                fixed_lede = re.sub(r'\s+', ' ', fixed_lede)

    # Replace in content
    content = content.replace(original_lede, fixed_lede)

    return content

def process_file(filepath):
    """Process single file"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if no lede
    if '<p class="lede">' not in content:
        return False

    original_content = content
    content = fix_lede_simple(content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    print("🚀 Removing keyword stuffing from lede paragraphs...")
    print()

    # Find all HTML guide pages
    guide_files = list(ROOT_DIR.glob("guide/**/*.html")) + list(ROOT_DIR.glob("sicilia/**/*.html"))

    processed = 0

    for filepath in guide_files:
        if 'backup-original' in str(filepath):
            continue

        if process_file(filepath):
            processed += 1
            if processed <= 20:
                print(f"✅ {filepath.relative_to(ROOT_DIR)}")

    print()
    print(f"✅ Done! Fixed {processed} files")
    print()
    print("Examples of fixes:")
    print("  ❌ BEFORE: 'A Palermo, architetto a palermo diventa un problema'")
    print("  ✅ AFTER:  'A Palermo, architetto diventa critico'")
    print()
    print("  ❌ BEFORE: 'A Catania, sanatoria edilizia a Catania quando'")
    print("  ✅ AFTER:  'A Catania, sanatoria edilizia quando'")

if __name__ == "__main__":
    main()
