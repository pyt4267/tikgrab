"""
TikGrab Twitter Bot v4.1 - TikTok専用版（30分定期実行対応）
Usage: python twitter_bot.py

Features:
- TikTokダウンロード訴求に特化
- 画像付きツイート (tiktok_promo.png)
- 自動定期ツイート機能
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
# TikTok Promotion Templates
# ========================================
PROMO_IMAGE = "tiktok_promo.png"

TIKTOK_TWEETS = [
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

    """📱 Watch TikToks offline anywhere!

Download your favorites with TikGrab.
• No Watermark
• High Quality
• Free Forever

👉 https://tikgrab.net

#TikTokVideo #OfflineViewing""",

    """✨ Best TikTok Downloader 2025

Save videos without the logo!
Easy & Fast.

Try it now: https://tikgrab.net

#TikTokTools #CreatorEconomy""",
    
    """🎵 Extract MP3 from TikToks!

Love that sound? Get the audio only.
TikGrab makes it easy.

https://tikgrab.net/

#TikTokMusic #MP3Download"""
]

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

def post_tweet_with_image(text):
    """Post a tweet with the TikTok promo image"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "images", PROMO_IMAGE)
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"⚠️ Image not found: {image_path}")
            print("   Posting text only...")
            return post_tweet_text_only(text)
        
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
        return False

def post_tweet_text_only(text):
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

def post_random_tweet(with_image=True):
    """Post a random TikTok promo tweet"""
    tweet_text = random.choice(TIKTOK_TWEETS)
    
    print(f"\n🎵 Selecting random TikTok tweet...")
    print(f"📝 Text: {tweet_text[:60]}...")
    
    if with_image:
        return post_tweet_with_image(tweet_text)
    else:
        return post_tweet_text_only(tweet_text)

def run_scheduled_bot(interval_minutes=30, with_images=True):
    """Run bot on schedule"""
    print(f"🤖 TikGrab TikTok Bot Started!")
    print(f"   Mode: {'Image + Text' if with_images else 'Text Only'}")
    print(f"   Interval: Every {interval_minutes} minutes")
    print(f"   Press Ctrl+C to stop\n")
    
    post_count = 0
    
    while True:
        post_count += 1
        print(f"\n{'='*50}")
        print(f"⏰ Post #{post_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        
        post_random_tweet(with_image=with_images)
        
        wait_seconds = interval_minutes * 60
        print(f"\n⏳ Sleeping for {interval_minutes} minutes...")
        time.sleep(wait_seconds)

def main():
    """Main function"""
    print("=" * 50)
    print("🎵 TikGrab Twitter Bot v4.1 (TikTok Only)")
    print("=" * 50)
    
    # Check credentials
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("❌ Missing API credentials!")
        print("   Please update .env file with your Twitter API keys")
        return
    
    print(f"\n📊 Config:")
    print(f"   Review templates: {len(TIKTOK_TWEETS)} available")
    print(f"   Image: {PROMO_IMAGE}")
    
    print("\n📌 Options:")
    print("1. Post a random TikTok tweet now")
    print("2. Start scheduled bot (Default: 30 min)")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        with_img = input("Include image? (y/n, default y): ").strip().lower() != 'n'
        post_random_tweet(with_image=with_img)
    elif choice == "2":
        mins = input("Post interval (minutes, default 30): ").strip()
        mins = int(mins) if mins.isdigit() else 30
        with_img = input("Include images? (y/n, default y): ").strip().lower() != 'n'
        run_scheduled_bot(interval_minutes=mins, with_images=with_img)
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
