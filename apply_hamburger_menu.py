"""
Apply hamburger menu to all HTML pages
"""
import os
import re
import glob

# Directory containing HTML files
html_dir = r"c:\Users\taiki\.gemini\antigravity\playground\cobalt-apogee"

# Old nav pattern (without hamburger)
old_nav_pattern = r'<nav class="nav">\s*<a href="[^"]*" class="nav-link">How to</a>\s*<a href="[^"]*" class="nav-link">All Sites</a>\s*<a href="[^"]*" class="nav-link">FAQ</a>\s*</nav>'

# New nav with hamburger button
new_nav = '''<button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Menu">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>
            <nav class="nav" id="mainNav">
                <a href="how-to-download.html" class="nav-link">How to</a>
                <a href="platforms.html" class="nav-link">All Sites</a>
                <a href="faq.html" class="nav-link">FAQ</a>
            </nav>'''

# Mobile menu JavaScript
mobile_menu_js = '''<script>
        // Mobile Menu Toggle
        document.addEventListener('DOMContentLoaded', function() {
            const mobileMenuBtn = document.getElementById('mobileMenuBtn');
            const mainNav = document.getElementById('mainNav');
            
            if (mobileMenuBtn && mainNav) {
                mobileMenuBtn.addEventListener('click', function() {
                    mobileMenuBtn.classList.toggle('active');
                    mainNav.classList.toggle('active');
                });
                
                // Close menu when clicking a link
                mainNav.querySelectorAll('.nav-link').forEach(link => {
                    link.addEventListener('click', function() {
                        mobileMenuBtn.classList.remove('active');
                        mainNav.classList.remove('active');
                    });
                });
                
                // Close menu when clicking outside
                document.addEventListener('click', function(e) {
                    if (!mainNav.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                        mobileMenuBtn.classList.remove('active');
                        mainNav.classList.remove('active');
                    }
                });
            }
        });
    </script>'''

# Get all HTML files except index.html (already updated)
html_files = glob.glob(os.path.join(html_dir, "*.html"))
updated_count = 0
skipped_count = 0

for html_file in html_files:
    filename = os.path.basename(html_file)
    
    # Skip index.html (already updated)
    if filename == "index.html":
        continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Check if already has hamburger menu
    if 'mobile-menu-btn' in content:
        print(f"⏭️ Skipped (already has menu): {filename}")
        skipped_count += 1
        continue
    
    # Update nav
    if '<nav class="nav">' in content:
        # Replace the nav section
        content = re.sub(
            r'<nav class="nav">\s*<a href="[^"]*" class="nav-link">How to</a>\s*<a href="[^"]*" class="nav-link">All Sites</a>\s*<a href="[^"]*" class="nav-link">FAQ</a>\s*</nav>',
            new_nav,
            content,
            flags=re.DOTALL
        )
        modified = True
    
    # Add mobile menu JS before </body> if not present
    if modified and mobile_menu_js not in content:
        # Insert before first <script or before </body>
        if '<script src="' in content:
            # Insert before first script tag
            content = content.replace('<script src="', mobile_menu_js + '\n    <script src="', 1)
        else:
            # Insert before </body>
            content = content.replace('</body>', mobile_menu_js + '\n</body>')
    
    if modified:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated: {filename}")
        updated_count += 1
    else:
        print(f"⚠️ No nav found: {filename}")
        skipped_count += 1

print(f"\n📊 Summary:")
print(f"   Updated: {updated_count} files")
print(f"   Skipped: {skipped_count} files")
