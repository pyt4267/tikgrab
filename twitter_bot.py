"""
TikGrab Twitter Bot v3.0 - プラットフォーム別画像対応版
Usage: python twitter_bot.py

Features:
- TikTok専用テンプレート + TikTok画像
- YouTube専用テンプレート + YouTube画像
- Instagram専用テンプレート + Instagram画像
- 一般テンプレート + 一般画像
"""

import os
import random
import time
from datetime import datetime
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

# Twitter API Credentials
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# ========================================
# Platform-specific Templates
# ========================================
PLATFORM_TEMPLATES = {
    "tiktok": {
        "image": "tiktok_promo.png",
        "tweets": [
            """🎵 Download TikTok videos WITHOUT watermark!

3 simple steps:
1️⃣ Copy TikTok URL
2️⃣ Paste on TikGrab
3️⃣ Download in HD!

No app needed: https://tikgrab.net

#TikTok #NoWatermark #VideoDownload""",

            """💡 Save TikTok videos in HD - No watermark!

TikGrab removes watermarks automatically.
No registration. No ads.

👉 https://tikgrab.net

#TikTok #TikTokDownloader""",

            """🎬 TikTok slideshows? No problem!

TikGrab downloads:
• Videos (HD, no watermark)
• Slideshows (all images)
• Audio (MP3)

Try it: https://tikgrab.net

#TikTok #ContentCreator""",

            """⚡ Fastest TikTok downloader!

Paste URL → Click Download → Done!

Save your favorite TikToks in seconds.

https://tikgrab.net

#TikTok #Viral""",

            """🔥 Going viral on TikTok?

Save your best videos with TikGrab!
No watermark. HD quality.

https://tikgrab.net""",
        ]
    },
    
    "youtube": {
        "image": "youtube_promo.png",
        "tweets": [
            """📺 Download YouTube videos in 4K!

TikGrab supports:
• 4K Ultra HD
• 1080p Full HD
• 720p HD
• Audio only (MP3)

Free & unlimited: https://tikgrab.net

#YouTube #4K #VideoDownload""",

            """🎧 Extract audio from YouTube!

Perfect for:
• Music
• Podcasts
• Lectures
• Audiobooks

Just paste URL and select "Audio"

https://tikgrab.net

#YouTube #MP3""",

            """📱 Watch YouTube offline!

Download with TikGrab:
1. Copy video URL
2. Paste on TikGrab
3. Save to your device!

https://tikgrab.net

#YouTube #OfflineVideo""",

            """🎬 Save YouTube tutorials forever!

Don't lose your favorite how-to videos.
Download them with TikGrab.

4K quality. Free forever.

https://tikgrab.net""",

            """🎵 YouTube to MP3 converter!

Extract audio from any YouTube video.
High quality. No limits.

Try: https://tikgrab.net

#YouTubeToMP3""",
        ]
    },
    
    "instagram": {
        "image": "instagram_promo.png",
        "tweets": [
            """📸 Save Instagram Reels in HD!

TikGrab works with:
• Reels
• Stories
• IGTV
• Posts

No login required: https://tikgrab.net

#Instagram #Reels #Download""",

            """💜 Download Instagram Reels easily!

Copy → Paste → Download

That's it! Works on all devices.

👉 https://tikgrab.net

#Instagram #InstaReels""",

            """📱 Save Instagram Stories!

Before they disappear, download them!

TikGrab - Fast & Free

https://tikgrab.net

#InstagramStories""",

            """🎥 Instagram video downloader!

Reels, Stories, IGTV - all supported!

No account needed. No limits.

https://tikgrab.net

#Instagram #ContentCreator""",

            """✨ Love that Reel? Save it!

TikGrab downloads Instagram content in HD.
Free. Fast. No signup.

https://tikgrab.net""",
        ]
    },
    
    "twitter": {
        "image": "twitter_promo.png",
        "tweets": [
            """🐦 Save Twitter/X videos instantly!

See a video you love? Save it!

1. Copy tweet URL
2. Paste on TikGrab
3. Download!

https://tikgrab.net

#Twitter #SaveVideo""",

            """⚡ Download X videos in HD!

TikGrab makes it easy.
No registration. No ads.

https://tikgrab.net

#X #VideoDownload""",

            """📹 Don't lose that viral tweet!

Download Twitter/X videos with TikGrab.

Free forever: https://tikgrab.net""",
        ]
    },
    
    "general": {
        "image": "general_promo.png",
        "tweets": [
            """🚀 TikGrab - Free Video Downloader!

✅ TikTok (no watermark)
✅ YouTube (4K)
✅ Instagram Reels
✅ Twitter/X
✅ 100+ platforms

No signup required!
👉 https://tikgrab.net

#VideoDownloader #FreeTools""",

            """🔥 Download ANY video in seconds!

TikGrab supports 100+ platforms:
• TikTok • YouTube • Instagram
• Twitter • Vimeo • Reddit
• And 94 more!

Free forever: https://tikgrab.net""",

            """⚡ One tool. 100+ platforms. Zero fees.

TikGrab - The ultimate video downloader.

Try it now: https://tikgrab.net

#FreeTools #VideoDownload""",

            """✨ Why 50,000+ users love TikGrab:

✓ 100+ platforms supported
✓ HD quality downloads
✓ No registration
✓ No annoying popups
✓ Works on mobile

Join them: https://tikgrab.net""",

            """🔒 TikGrab respects your privacy!

• No account needed
• No data collection
• No tracking
• Just downloads

Safe & free: https://tikgrab.net""",

            """📱 TikGrab works on ALL devices!

• iPhone & Android
• Windows & Mac
• Tablets
• Any browser

Download anywhere: https://tikgrab.net""",

            """💡 Pro tip: Use TikGrab Bookmarklet!

1-click downloads from any page.

Install: https://tikgrab.net/bookmarklet

#ProductivityHack""",

            """🎌 Anime fans! TikGrab supports:

• Crunchyroll clips
• Funimation
• 9Anime
• And more!

https://tikgrab.net

#Anime #Crunchyroll""",

            """👀 Still using sketchy download sites?

Try TikGrab instead:
• No popups
• No malware
• No BS

https://tikgrab.net""",

            """🌟 TikGrab - Updated daily!

New platforms added regularly.
Always free. Always fast.

https://tikgrab.net""",
        ]
    }
}

# Platform rotation order
PLATFORMS = ["tiktok", "youtube", "instagram", "twitter", "general"]

def create_client():
    """Create Twitter API v2 client"""
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    return client

def create_api_v1():
    """Create Twitter API v1.1 for media upload"""
    auth = tweepy.OAuth1UserHandler(
        API_KEY, API_SECRET,
        ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth)

def post_tweet(text):
    """Post a text-only tweet"""
    try:
        client = create_client()
        response = client.create_tweet(text=text)
        tweet_id = response.data['id']
        print(f"✅ Tweet posted successfully!")
        print(f"   Tweet ID: {tweet_id}")
        print(f"   URL: https://twitter.com/i/status/{tweet_id}")
        return True
    except tweepy.TweepyException as e:
        print(f"❌ Error posting tweet: {e}")
        return False

def post_tweet_with_image(text, image_path):
    """Post a tweet with an image"""
    try:
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"⚠️ Image not found: {image_path}")
            print("   Posting without image...")
            return post_tweet(text)
        
        # Upload media using v1.1 API
        api_v1 = create_api_v1()
        media = api_v1.media_upload(image_path)
        
        # Post tweet with media using v2 API
        client = create_client()
        response = client.create_tweet(text=text, media_ids=[media.media_id])
        
        tweet_id = response.data['id']
        print(f"✅ Tweet with image posted successfully!")
        print(f"   Tweet ID: {tweet_id}")
        print(f"   URL: https://twitter.com/i/status/{tweet_id}")
        return True
    except tweepy.TweepyException as e:
        print(f"❌ Error posting tweet with image: {e}")
        # Fallback to text-only
        print("   Trying text-only...")
        return post_tweet(text)

def post_platform_tweet(platform, with_image=True):
    """Post a tweet for a specific platform"""
    if platform not in PLATFORM_TEMPLATES:
        platform = "general"
    
    template = PLATFORM_TEMPLATES[platform]
    tweet_text = random.choice(template["tweets"])
    
    print(f"\n🎯 Platform: {platform.upper()}")
    print(f"📝 Tweet: {tweet_text[:80]}...")
    
    if with_image:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "images", template["image"])
        print(f"🖼️ Image: {template['image']}")
        return post_tweet_with_image(tweet_text, image_path)
    else:
        return post_tweet(tweet_text)

def post_random_platform_tweet(with_image=True):
    """Post a random platform tweet"""
    platform = random.choice(PLATFORMS)
    return post_platform_tweet(platform, with_image)

def run_scheduled_bot(interval_hours=8, with_images=True):
    """Run bot on schedule with platform rotation"""
    print(f"🤖 TikGrab Twitter Bot v3.0 Started!")
    print(f"   Mode: Platform rotation {'with images' if with_images else 'text only'}")
    print(f"   Posting every {interval_hours} hours")
    print(f"   Platforms: {', '.join(PLATFORMS)}")
    print(f"   Press Ctrl+C to stop\n")
    
    platform_index = 0
    post_count = 0
    
    while True:
        post_count += 1
        current_platform = PLATFORMS[platform_index % len(PLATFORMS)]
        
        print(f"\n{'='*50}")
        print(f"⏰ Post #{post_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Next platform: {current_platform.upper()}")
        print(f"{'='*50}")
        
        post_platform_tweet(current_platform, with_image=with_images)
        
        platform_index += 1
        wait_seconds = interval_hours * 3600
        next_platform = PLATFORMS[platform_index % len(PLATFORMS)]
        print(f"\n⏳ Next post in {interval_hours} hours ({next_platform.upper()})...")
        time.sleep(wait_seconds)

def main():
    """Main function"""
    print("=" * 50)
    print("🚀 TikGrab Twitter Bot v3.0")
    print("   Platform-specific tweets with matching images!")
    print("=" * 50)
    
    # Check credentials
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("❌ Missing API credentials!")
        print("   Please update .env file with your Twitter API keys")
        return
    
    # Count templates
    total_templates = sum(len(p["tweets"]) for p in PLATFORM_TEMPLATES.values())
    print(f"\n📊 Stats:")
    print(f"   Platforms: {len(PLATFORMS)}")
    print(f"   Total templates: {total_templates}")
    for p in PLATFORMS:
        print(f"   - {p}: {len(PLATFORM_TEMPLATES[p]['tweets'])} tweets")
    
    print("\n📌 Options:")
    print("1. Post TikTok tweet")
    print("2. Post YouTube tweet")
    print("3. Post Instagram tweet")
    print("4. Post Twitter/X tweet")
    print("5. Post General tweet")
    print("6. Post Random platform tweet")
    print("7. Start scheduled bot (rotate platforms)")
    print("8. Exit")
    
    choice = input("\nSelect option (1-8): ").strip()
    
    if choice == "1":
        post_platform_tweet("tiktok")
    elif choice == "2":
        post_platform_tweet("youtube")
    elif choice == "3":
        post_platform_tweet("instagram")
    elif choice == "4":
        post_platform_tweet("twitter")
    elif choice == "5":
        post_platform_tweet("general")
    elif choice == "6":
        post_random_platform_tweet()
    elif choice == "7":
        hours = input("Post interval (hours, default 8): ").strip()
        hours = int(hours) if hours.isdigit() else 8
        with_img = input("Include images? (y/n, default y): ").strip().lower()
        with_img = with_img != 'n'
        run_scheduled_bot(interval_hours=hours, with_images=with_img)
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
