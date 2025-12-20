import os
import glob

# Phase 1で残すプラットフォーム（20個）
KEEP_PLATFORMS = [
    'tiktok',
    'youtube',
    'instagram',
    'twitter',
    'facebook',
    'reddit',
    'pinterest',
    'threads',
    'twitch',
    'bilibili',
    'vk',
    'telegram',
    'ted',
    'vimeo',
    'dailymotion',
    'soundcloud',
    'snapchat',
    'linkedin',
    'tumblr',
    'bluesky',
]

# その他の必須ページ
KEEP_OTHER = [
    'index.html',
    'how-to-download.html',
    'faq.html',
    'platforms.html',
    'contact.html',
    'privacy.html',
    'terms.html',
    'dmca.html',
    'bookmarklet.html',
]

def main():
    # 全HTMLファイル取得
    html_files = glob.glob('*.html')
    
    print(f"Found {len(html_files)} HTML files")
    print("=" * 50)
    
    keep_files = []
    delete_files = []
    
    for filepath in html_files:
        filename = os.path.basename(filepath)
        
        # その他必須ページはスキップ
        if filename in KEEP_OTHER:
            keep_files.append(filename)
            continue
        
        # download-*-videos.html または download-*-music.html
        if filename.startswith('download-'):
            # プラットフォーム名を抽出
            platform = filename.replace('download-', '').replace('-videos.html', '').replace('-music.html', '').replace('-podcasts.html', '')
            
            if platform in KEEP_PLATFORMS:
                keep_files.append(filename)
            else:
                delete_files.append(filename)
        else:
            keep_files.append(filename)
    
    print(f"\n📁 残すファイル ({len(keep_files)}個):")
    for f in sorted(keep_files):
        print(f"  ✅ {f}")
    
    print(f"\n🗑️ 削除するファイル ({len(delete_files)}個):")
    for f in sorted(delete_files):
        print(f"  ❌ {f}")
    
    # 確認
    print(f"\n" + "=" * 50)
    print(f"削除を実行しますか？ (y/n)")
    response = input().strip().lower()
    
    if response == 'y':
        for f in delete_files:
            os.remove(f)
            print(f"  Deleted: {f}")
        print(f"\n✅ {len(delete_files)}個のファイルを削除しました")
    else:
        print("キャンセルしました")

if __name__ == '__main__':
    main()
