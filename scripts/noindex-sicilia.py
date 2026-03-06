#!/usr/bin/env python3
"""
Aggiunge noindex a tutte le pagine /sicilia/
Queste pagine hanno ~60-80 parole di contenuto e vengono
percepite da Google come thin content / content farm.
"""

import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SICILIA_DIR = ROOT_DIR / "sicilia"

OLD_ROBOTS = 'content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"'
NEW_ROBOTS = 'content="noindex,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"'


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if OLD_ROBOTS not in content:
        return False  # already noindex or different format

    new_content = content.replace(OLD_ROBOTS, NEW_ROBOTS)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    files = list(SICILIA_DIR.glob("*.html"))
    files = [f for f in files if f.name != "index.html"]

    fixed = 0
    skipped = 0

    for filepath in sorted(files):
        if process_file(filepath):
            fixed += 1
        else:
            skipped += 1

    print(f"✅ Noindex aggiunto: {fixed} file")
    print(f"⏭  Skippati (già noindex o formato diverso): {skipped} file")


if __name__ == "__main__":
    main()
