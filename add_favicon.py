"""Add favicon to all HTML files"""
import os
import re

FAVICON_LINKS = '''    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">'''

def add_favicon():
    count = 0
    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Skip if already has favicon.svg
                if 'favicon.svg' in content:
                    print(f"Already has favicon: {filename}")
                    continue
                
                # Add favicon before </head>
                if '</head>' in content:
                    content = content.replace('</head>', FAVICON_LINKS + '\n</head>')
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
                    print(f"Added favicon: {filename}")
            except Exception as e:
                print(f"Error: {filename} - {e}")
    
    print(f"\nTotal: {count} files updated")

if __name__ == "__main__":
    add_favicon()
