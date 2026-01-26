#!/usr/bin/env python3
"""
Remove AI-generated template phrases from lede paragraphs
"""

import re
from pathlib import Path

ROOT_DIR = Path(".")

def clean_lede(content):
    """Remove template AI phrases from lede"""

    # Find lede paragraph
    lede_match = re.search(r'<p class="lede">([^<]+)</p>', content, re.DOTALL)
    if not lede_match:
        return content

    original_lede = lede_match.group(1)
    cleaned_lede = original_lede

    # Remove: "la differenza la fanno [varie cose] e [altre cose], non le scelte fatte "a cantiere aperto"."
    cleaned_lede = re.sub(
        r':\s*la differenza la fanno[^.]+non le scelte fatte[^.]+\.',
        '.',
        cleaned_lede,
        flags=re.IGNORECASE
    )

    # Remove: "Prima di decidere, serve mettere in fila dati, requisiti e verifiche misurabili."
    cleaned_lede = re.sub(
        r'\s*Prima di decidere,\s*serve mettere in fila dati,\s*requisiti e verifiche misurabili\.',
        '',
        cleaned_lede,
        flags=re.IGNORECASE
    )

    # Clean up double spaces and extra punctuation
    cleaned_lede = re.sub(r'\s+', ' ', cleaned_lede)
    cleaned_lede = re.sub(r'\.\s*\.', '.', cleaned_lede)
    cleaned_lede = re.sub(r':\s*\.', '.', cleaned_lede)

    # If lede becomes too short, add a more natural ending
    if len(cleaned_lede) < 100:
        # Add context-appropriate ending
        if 'diventa un problema quando' in cleaned_lede or 'diventa critico quando' in cleaned_lede:
            cleaned_lede = re.sub(
                r'(diventa (?:un problema|critico) quando[^.]+)\.',
                r'\1: ogni dettaglio conta.',
                cleaned_lede
            )

    # Replace in content
    content = content.replace(original_lede, cleaned_lede.strip())

    return content

def process_file(filepath):
    """Process single file"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if no lede
    if '<p class="lede">' not in content:
        return False

    original_content = content
    content = clean_lede(content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    print("🚀 Removing AI template phrases...")
    print()

    # Find all guide pages
    guide_files = list(ROOT_DIR.glob("guide/**/*.html")) + list(ROOT_DIR.glob("sicilia/**/*.html"))

    processed = 0

    for filepath in guide_files:
        if 'backup-original' in str(filepath):
            continue

        if process_file(filepath):
            processed += 1
            if processed <= 10:
                print(f"✅ {filepath.relative_to(ROOT_DIR)}")

    print()
    print(f"✅ Done! Cleaned {processed} files")
    print()
    print("Removed phrases:")
    print("  ❌ 'la differenza la fanno... non le scelte fatte a cantiere aperto'")
    print("  ❌ 'serve mettere in fila dati, requisiti e verifiche misurabili'")
    print()
    print("Result: More natural, less template-y content.")

if __name__ == "__main__":
    main()
