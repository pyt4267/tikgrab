"""
Add ads.js to all HTML pages that don't have it
"""
import os
import glob

def add_ads_js(filepath):
    """Add ads.js before </body> if not already present"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has ads.js
    if 'ads.js' in content:
        print(f"  Skip (already has ads.js): {os.path.basename(filepath)}")
        return False
    
    # Find theme.js and add ads.js after it
    if 'theme.js' in content:
        content = content.replace(
            '<script src="theme.js"></script>',
            '<script src="theme.js"></script>\n    <script src="ads.js"></script>'
        )
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Added ads.js: {os.path.basename(filepath)}")
        return True
    # Or add before </body>
    elif '</body>' in content:
        content = content.replace(
            '</body>',
            '    <script src="ads.js"></script>\n</body>'
        )
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Added ads.js (before body): {os.path.basename(filepath)}")
        return True
    else:
        print(f"  Skip (no theme.js or </body>): {os.path.basename(filepath)}")
        return False

def main():
    # Get all HTML files
    html_files = glob.glob('*.html')
    
    print(f"Found {len(html_files)} HTML files")
    print("=" * 50)
    
    added = 0
    for filepath in html_files:
        if add_ads_js(filepath):
            added += 1
    
    print("=" * 50)
    print(f"Added ads.js to {added} files")

if __name__ == '__main__':
    main()
