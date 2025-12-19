"""
Remove Adsterra Social Bar from all HTML pages
"""
import os
import glob
import re

def remove_adsterra(filepath):
    """Remove Adsterra Social Bar code from HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has Adsterra code
    if 'effectivegatecpm.com' not in content:
        print(f"  Skip (no Adsterra): {os.path.basename(filepath)}")
        return False
    
    # Remove Adsterra Social Bar script and comment
    # Pattern: <!-- Adsterra Social Bar --> followed by script tag
    pattern = r'\s*<!-- Adsterra Social Bar -->\s*<script[^>]*effectivegatecpm\.com[^>]*></script>'
    new_content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # Also remove standalone script without comment
    pattern2 = r'\s*<script[^>]*effectivegatecpm\.com[^>]*></script>'
    new_content = re.sub(pattern2, '', new_content, flags=re.IGNORECASE)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Removed Adsterra: {os.path.basename(filepath)}")
        return True
    else:
        print(f"  No change: {os.path.basename(filepath)}")
        return False

def main():
    # Get all HTML files
    html_files = glob.glob('*.html')
    
    print(f"Found {len(html_files)} HTML files")
    print("=" * 50)
    
    removed = 0
    for filepath in html_files:
        if remove_adsterra(filepath):
            removed += 1
    
    print("=" * 50)
    print(f"Removed Adsterra from {removed} files")

if __name__ == '__main__':
    main()
