"""
Add PropellerAds Multitag to all HTML pages
"""
import os
import glob

# PropellerAds Multitag code
MULTITAG_CODE = '''
    <!-- PropellerAds Multitag -->
    <script src="https://quge5.com/88/tag.min.js" data-zone="194556" async data-cfasync="false"></script>
'''

def add_multitag(filepath):
    """Add Multitag code before Adsterra code or before </body>"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has this multitag
    if 'quge5.com' in content or 'data-zone="194556"' in content:
        print(f"  Skip (already has Multitag): {os.path.basename(filepath)}")
        return False
    
    # Add before Adsterra code if exists
    if 'effectivegatecpm.com' in content:
        content = content.replace(
            '<!-- Adsterra Social Bar -->',
            MULTITAG_CODE + '\n    <!-- Adsterra Social Bar -->'
        )
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Added Multitag: {os.path.basename(filepath)}")
        return True
    # Or add before </body>
    elif '</body>' in content:
        content = content.replace(
            '</body>',
            MULTITAG_CODE + '</body>'
        )
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Added Multitag (before body): {os.path.basename(filepath)}")
        return True
    else:
        print(f"  Skip (no suitable location): {os.path.basename(filepath)}")
        return False

def main():
    # Get all HTML files
    html_files = glob.glob('*.html')
    
    print(f"Found {len(html_files)} HTML files")
    print("=" * 50)
    
    added = 0
    for filepath in html_files:
        if add_multitag(filepath):
            added += 1
    
    print("=" * 50)
    print(f"Added Multitag to {added} files")

if __name__ == '__main__':
    main()
