"""
Add Adsterra Social Bar ad to all HTML pages
"""
import os
import glob

# Adsterra Social Bar code
AD_CODE = '''
    <!-- Adsterra Social Bar -->
    <script type="text/javascript" src="https://pl28293503.effectivegatecpm.com/17/1d/0a/171d0afca588569c141457cb75ca400c.js"></script>
'''

def add_ad_to_html(filepath):
    """Add Adsterra ad code before </body> if not already present"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has the ad
    if 'pl28293503.effectivegatecpm.com' in content:
        print(f"  Skip (already has ad): {os.path.basename(filepath)}")
        return False
    
    # Find </body> and insert ad before it
    if '</body>' in content:
        content = content.replace('</body>', AD_CODE + '</body>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Added ad: {os.path.basename(filepath)}")
        return True
    else:
        print(f"  Skip (no </body>): {os.path.basename(filepath)}")
        return False

def main():
    # Get all HTML files
    html_files = glob.glob('*.html')
    
    print(f"Found {len(html_files)} HTML files")
    print("=" * 50)
    
    added = 0
    for filepath in html_files:
        if add_ad_to_html(filepath):
            added += 1
    
    print("=" * 50)
    print(f"Added ads to {added} files")

if __name__ == '__main__':
    main()
