#!/usr/bin/env python3
"""
Minify CSS and JavaScript files
Requires: csscompressor (pip install csscompressor)
"""

import os
from pathlib import Path

try:
    import csscompressor
    HAS_CSS = True
except ImportError:
    HAS_CSS = False
    print("⚠️  csscompressor not installed. Run: pip install csscompressor")

ROOT_DIR = Path(".")
CSS_DIR = ROOT_DIR / "assets" / "css"
JS_DIR = ROOT_DIR / "assets" / "js"

def minify_css_file(filepath):
    """Minify single CSS file"""
    if not HAS_CSS:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create .min.css version
    minified = csscompressor.compress(content)

    output_path = filepath.with_suffix('.min.css')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(minified)

    original_size = len(content)
    minified_size = len(minified)
    savings = (1 - minified_size / original_size) * 100

    return output_path, original_size, minified_size, savings

def minify_js_simple(filepath):
    """Minify JS with terser (real AST-based minifier).

    A previous regex-based approach (strip `//...` comments, then
    collapse whitespace) mistook `https://` inside string literals for
    a line comment and truncated code after it, shipping broken JS to
    production. Terser understands JS syntax, so it can't make that
    mistake; if terser isn't available we fall back to copying the
    file unminified rather than risk corrupting it.
    """
    import subprocess

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    output_path = filepath.with_suffix('.min.js')

    try:
        subprocess.run(
            ['npx', '--yes', 'terser', str(filepath), '-o', str(output_path),
             '-c', '-m', '--comments', 'false'],
            check=True, capture_output=True, text=True,
        )
        with open(output_path, 'r', encoding='utf-8') as f:
            minified = f.read()
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"  ⚠️  terser unavailable/failed for {filepath.name}, copying unminified: {e}")
        minified = content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified)

    # Guard against ever shipping broken JS again.
    try:
        subprocess.run(['node', '-c', str(output_path)], check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print("  ⚠️  node not found, skipping syntax check")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"{output_path} failed syntax check after minification:\n{e.stderr}"
        )

    original_size = len(content)
    minified_size = len(minified)
    savings = (1 - minified_size / original_size) * 100 if original_size else 0

    return output_path, original_size, minified_size, savings

def update_html_references():
    """Update HTML files to reference .min.css and .min.js"""
    html_files = list(ROOT_DIR.rglob("*.html"))
    updated = 0

    for filepath in html_files:
        if 'backup-original' in str(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Replace CSS references
        content = content.replace('/assets/css/styles.css', '/assets/css/styles.min.css')
        content = content.replace('/assets/css/inline-fixes.css', '/assets/css/inline-fixes.min.css')

        # Replace JS references
        content = content.replace('/assets/js/main.js', '/assets/js/main.min.js')

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1

    return updated

def main():
    print("🚀 Minifying assets...")
    print()

    total_savings = 0
    files_processed = 0

    # Minify CSS
    if CSS_DIR.exists():
        print("📄 Minifying CSS files...")
        for css_file in CSS_DIR.glob("*.css"):
            if '.min.css' in css_file.name:
                continue

            result = minify_css_file(css_file)
            if result:
                output, orig, minified, savings = result
                print(f"  ✅ {css_file.name} → {output.name}")
                print(f"     {orig:,} bytes → {minified:,} bytes ({savings:.1f}% smaller)")
                total_savings += (orig - minified)
                files_processed += 1

    print()

    # Minify JS
    if JS_DIR.exists():
        print("📄 Minifying JavaScript files...")
        for js_file in JS_DIR.glob("*.js"):
            if '.min.js' in js_file.name:
                continue

            result = minify_js_simple(js_file)
            if result:
                output, orig, minified, savings = result
                print(f"  ✅ {js_file.name} → {output.name}")
                print(f"     {orig:,} bytes → {minified:,} bytes ({savings:.1f}% smaller)")
                total_savings += (orig - minified)
                files_processed += 1

    print()

    # Update HTML references
    print("🔗 Updating HTML file references...")
    updated = update_html_references()
    print(f"  ✅ Updated {updated} HTML files")

    print()
    print(f"✅ Done! Minified {files_processed} files")
    print(f"💾 Total bandwidth saved: {total_savings:,} bytes ({total_savings/1024:.1f} KB)")

if __name__ == "__main__":
    main()
