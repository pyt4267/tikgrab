"""Remove theme toggle from all HTML files"""
import os
import re

def remove_theme_toggle():
    count = 0
    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove theme toggle button (any variation)
                original = content
                content = re.sub(
                    r'<button class="theme-toggle"[^>]*>[\s\S]*?</button>\s*',
                    '',
                    content
                )
                
                if content != original:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
                    print(f"Fixed: {filename}")
            except Exception as e:
                print(f"Error: {filename} - {e}")
    
    print(f"\nTotal: {count} files updated")

if __name__ == "__main__":
    remove_theme_toggle()
