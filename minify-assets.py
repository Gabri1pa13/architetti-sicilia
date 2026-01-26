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
    """Simple JS minification (remove comments and whitespace)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove single-line comments
    import re
    minified = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)

    # Remove multi-line comments
    minified = re.sub(r'/\*.*?\*/', '', minified, flags=re.DOTALL)

    # Remove extra whitespace
    minified = re.sub(r'\s+', ' ', minified)
    minified = re.sub(r'\s*([{};,:])\s*', r'\1', minified)

    output_path = filepath.with_suffix('.min.js')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(minified)

    original_size = len(content)
    minified_size = len(minified)
    savings = (1 - minified_size / original_size) * 100

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

    print()
    print("⚠️  IMPORTANT:")
    print("For production-grade JS minification, use tools like:")
    print("  • Terser: npm install -g terser && terser main.js -o main.min.js -c -m")
    print("  • UglifyJS: npm install -g uglify-js && uglifyjs main.js -o main.min.js -c -m")

if __name__ == "__main__":
    main()
