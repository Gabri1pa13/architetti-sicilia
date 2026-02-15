#!/usr/bin/env python3
"""
Fix SEO canonical URL issues:
1. Convert relative canonical URLs to absolute URLs
2. Ensure consistent domain (architettisicilia.it without www)
"""

import os
import re
from pathlib import Path

# Canonical domain (from CNAME file)
CANONICAL_DOMAIN = "https://architettisicilia.it"

def fix_canonical_url(html_content, file_path):
    """
    Fix canonical URL in HTML content.

    Converts:
    - <link href="/" rel="canonical"/> -> <link href="https://architettisicilia.it/" rel="canonical"/>
    - <link href="/page/" rel="canonical"/> -> <link href="https://architettisicilia.it/page/" rel="canonical"/>
    - <link href="https://www.architettisicilia.it/..." -> <link href="https://architettisicilia.it/..."
    """
    changes = []

    # Pattern 1: Relative canonical URLs (href="/...")
    # Match: <link href="/..." rel="canonical"/> or <link rel="canonical" href="/..."/>
    pattern1 = r'(<link[^>]*?)\s+href="(/[^"]*?)"\s+rel="canonical"'
    pattern2 = r'(<link[^>]*?)\s+rel="canonical"\s+href="(/[^"]*?)"'

    def replace_relative(match):
        prefix = match.group(1)
        path = match.group(2)
        absolute_url = CANONICAL_DOMAIN + path
        changes.append(f"Relative canonical: {path} -> {absolute_url}")
        return f'{prefix} href="{absolute_url}" rel="canonical"'

    html_content = re.sub(pattern1, replace_relative, html_content)
    html_content = re.sub(pattern2, replace_relative, html_content)

    # Pattern 2: www.architettisicilia.it -> architettisicilia.it
    pattern3 = r'href="https://www\.architettisicilia\.it(/[^"]*?)"'

    def replace_www(match):
        path = match.group(1)
        absolute_url = CANONICAL_DOMAIN + path
        changes.append(f"Removed www: https://www.architettisicilia.it{path} -> {absolute_url}")
        return f'href="{absolute_url}"'

    html_content = re.sub(pattern3, replace_www, html_content)

    return html_content, changes

def process_html_files():
    """Process all HTML files in the directory."""
    root_dir = Path("/home/user/architetti-sicilia")
    html_files = list(root_dir.glob("**/*.html"))

    total_files = 0
    total_changes = 0
    files_modified = []

    for html_file in html_files:
        # Skip backup directories
        if "backup" in str(html_file):
            continue

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Only process files with canonical links
            if 'rel="canonical"' not in original_content:
                continue

            modified_content, changes = fix_canonical_url(original_content, html_file)

            if changes:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(modified_content)

                total_files += 1
                total_changes += len(changes)
                files_modified.append((str(html_file.relative_to(root_dir)), changes))

        except Exception as e:
            print(f"Error processing {html_file}: {e}")

    return total_files, total_changes, files_modified

if __name__ == "__main__":
    print("Starting canonical URL fix...")
    print(f"Canonical domain: {CANONICAL_DOMAIN}\n")

    total_files, total_changes, files_modified = process_html_files()

    print(f"\n=== Summary ===")
    print(f"Files modified: {total_files}")
    print(f"Total changes: {total_changes}")

    if files_modified:
        print(f"\n=== First 10 Modified Files ===")
        for file_path, changes in files_modified[:10]:
            print(f"\n{file_path}:")
            for change in changes[:3]:  # Show first 3 changes per file
                print(f"  - {change}")

    print("\nDone!")
