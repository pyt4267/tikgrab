"""
Apply hamburger menu to all HTML pages - Improved Version
Handles different nav link patterns
"""
import os
import re
import glob

# Directory containing HTML files
html_dir = r"c:\Users\taiki\.gemini\antigravity\playground\cobalt-apogee"

# Mobile menu JavaScript
mobile_menu_js = '''    <script>
        // Mobile Menu Toggle
        document.addEventListener('DOMContentLoaded', function() {
            const mobileMenuBtn = document.getElementById('mobileMenuBtn');
            const mainNav = document.getElementById('mainNav');
            
            if (mobileMenuBtn && mainNav) {
                mobileMenuBtn.addEventListener('click', function() {
                    mobileMenuBtn.classList.toggle('active');
                    mainNav.classList.toggle('active');
                });
                
                mainNav.querySelectorAll('.nav-link').forEach(link => {
                    link.addEventListener('click', function() {
                        mobileMenuBtn.classList.remove('active');
                        mainNav.classList.remove('active');
                    });
                });
                
                document.addEventListener('click', function(e) {
                    if (!mainNav.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                        mobileMenuBtn.classList.remove('active');
                        mainNav.classList.remove('active');
                    }
                });
            }
        });
    </script>
'''

hamburger_button = '''<button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Menu">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>
            '''

# Get all HTML files
html_files = glob.glob(os.path.join(html_dir, "*.html"))
updated_count = 0
skipped_count = 0

for html_file in html_files:
    filename = os.path.basename(html_file)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has hamburger menu
    if 'mobile-menu-btn' in content:
        print(f"⏭️ Skip (has menu): {filename}")
        skipped_count += 1
        continue
    
    # Check if has nav class="nav"
    if '<nav class="nav">' not in content:
        print(f"⚠️ Skip (no nav): {filename}")
        skipped_count += 1
        continue
    
    modified = False
    
    # Add hamburger button before nav
    if '<nav class="nav">' in content and 'mobile-menu-btn' not in content:
        content = content.replace(
            '<nav class="nav">',
            hamburger_button + '<nav class="nav" id="mainNav">'
        )
        modified = True
    
    # Add mobile menu JS if not present
    if modified and '// Mobile Menu Toggle' not in content:
        if '</body>' in content:
            content = content.replace('</body>', mobile_menu_js + '</body>')
        elif '</html>' in content:
            content = content.replace('</html>', mobile_menu_js + '</html>')
    
    if modified:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated: {filename}")
        updated_count += 1
    else:
        print(f"⚠️ No change: {filename}")
        skipped_count += 1

print(f"\n📊 Summary:")
print(f"   Updated: {updated_count} files")
print(f"   Skipped: {skipped_count} files")
