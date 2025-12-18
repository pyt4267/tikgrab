#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikGrab - Batch fix HTML files
Fixes broken HTML tags and incorrect links
"""

import os
import re
import glob

def fix_file(filepath):
    """Fix a single HTML file"""
    try:
        # Try UTF-8 first, then fall back to latin-1
        content = None
        encoding = 'utf-8'
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            encoding = 'latin-1'
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        
        original = content
        
        # Fix broken download button icon
        content = re.sub(r'ↁE/span>', '↓</span>', content)
        content = re.sub(r'ↁE/span\u003e', '↓</span>', content)
        
        # Fix broken emoji tags - various patterns
        content = re.sub(r'▶�E�E/span>', '▶️</span>', content)
        content = re.sub(r'✖︁E/div>', '✖️</div>', content)
        content = re.sub(r'ニコニコ動画ダウンローチE/span>', 'ニコニコ動画ダウンローダー</span>', content)
        
        # Fix more broken patterns
        content = re.sub(r'\?\?E\?E/span>', '▶️</span>', content)
        content = re.sub(r'\?\?\?E\?E/span>', '📸</span>', content)
        content = re.sub(r'\?E/span>', '⭐</span>', content)
        content = re.sub(r'\?\?E/span>', '☁️</span>', content)
        
        # Fix broken platform links
        content = re.sub(r'href="tiktok\.html"', 'href="download-tiktok-videos.html"', content)
        content = re.sub(r'href="youtube\.html"', 'href="download-youtube-videos.html"', content)
        content = re.sub(r'href="twitter\.html"', 'href="download-twitter-videos.html"', content)
        content = re.sub(r'href="instagram\.html"', 'href="download-instagram-videos.html"', content)
        content = re.sub(r'href="facebook\.html"', 'href="download-facebook-videos.html"', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    base_dir = r"c:\Users\taiki\.gemini\antigravity\playground\cobalt-apogee"
    pattern = os.path.join(base_dir, "download-*.html")
    
    files = glob.glob(pattern)
    fixed_count = 0
    
    print(f"Found {len(files)} files to check...")
    
    for filepath in files:
        filename = os.path.basename(filepath)
        if fix_file(filepath):
            print(f"Fixed: {filename}")
            fixed_count += 1
    
    print(f"\nComplete! Fixed {fixed_count} files.")

if __name__ == "__main__":
    main()
