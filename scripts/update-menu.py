import os
import re

def update_nav(content):
    # Pattern to find the menu div and its contents
    # We want to add <a href="/chi-siamo.html">Chi Siamo</a> before "Inizia da qui"
    
    old_menu_item = '<a class="" href="/inizia-da-qui/">Inizia da qui</a>'
    new_menu_items = '<a href="/chi-siamo.html">Chi Siamo</a>\n                <a href="/inizia-da-qui/">Inizia da qui</a>'
    
    if old_menu_item in content:
        return content.replace(old_menu_item, new_menu_items)
    
    # Try another variation without class=""
    old_menu_item_no_class = '<a href="/inizia-da-qui/">Inizia da qui</a>'
    if old_menu_item_no_class in content and '/chi-siamo.html' not in content:
        return content.replace(old_menu_item_no_class, new_menu_items)
        
    return content

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        # Skip some dirs
        if '.git' in root or 'assets' in root or 'backup' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = update_nav(content)
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    process_directory('.')
