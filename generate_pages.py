"""
TikGrab - Platform Download Pages Generator
Generates all download-*.html pages from a template
"""

import os

# Platform definitions: (filename, name, emoji, color1, color2, category, description)
PLATFORMS = [
    # Major Social
    ("download-youtube-videos.html", "YouTube", "▶️", "#ff0000", "#cc0000", "video", "Download YouTube videos in HD, 4K quality. Save videos, Shorts, and extract audio as MP3."),
    ("download-instagram-videos.html", "Instagram", "📷", "#833ab4", "#fd1d1d", "social", "Download Instagram Reels, Stories, IGTV, and posts. Save videos and photos."),
    ("download-twitter-videos.html", "Twitter / X", "🐦", "#1da1f2", "#0d8ecf", "social", "Download Twitter and X videos, GIFs, and images. Save tweets easily."),
    ("download-facebook-videos.html", "Facebook", "👤", "#1877f2", "#0d5fc5", "social", "Download Facebook videos from posts, pages, and groups. Save in HD quality."),
    
    # Video Platforms
    ("download-vimeo-videos.html", "Vimeo", "🎬", "#1ab7ea", "#0d8ecf", "video", "Download Vimeo videos in high quality. Professional video content."),
    ("download-twitch-videos.html", "Twitch", "🎮", "#9146ff", "#6441a5", "video", "Download Twitch clips, VODs, and highlights. Save gaming content."),
    ("download-dailymotion-videos.html", "Dailymotion", "🎥", "#0066dc", "#004a9f", "video", "Download Dailymotion videos in various quality options."),
    ("download-bilibili-videos.html", "Bilibili", "📺", "#00a1d6", "#0078a8", "regional", "Download Bilibili videos. Popular Chinese video platform."),
    ("download-rumble-videos.html", "Rumble", "📢", "#85c742", "#6ba832", "video", "Download Rumble videos. Alternative video platform content."),
    ("download-streamable-videos.html", "Streamable", "⚡", "#0773d8", "#0562b8", "video", "Download Streamable videos quickly and easily."),
    ("download-kick-videos.html", "Kick", "🟢", "#53fc18", "#42c813", "video", "Download Kick clips and VODs. Streaming platform content."),
    
    # Audio Platforms
    ("download-soundcloud-music.html", "SoundCloud", "🎧", "#ff5500", "#cc4400", "audio", "Download SoundCloud tracks as MP3. Free music downloads."),
    ("download-bandcamp-music.html", "Bandcamp", "🎸", "#629aa9", "#4a7a86", "audio", "Download Bandcamp music. Support independent artists."),
    ("download-mixcloud-music.html", "Mixcloud", "🎛️", "#5000ff", "#3d00cc", "audio", "Download Mixcloud mixes and radio shows."),
    ("download-spotify-podcasts.html", "Spotify", "🎵", "#1db954", "#17a34a", "audio", "Download Spotify podcasts. Audio content only."),
    
    # Social Platforms
    ("download-pinterest-videos.html", "Pinterest", "📌", "#bd081c", "#8c0615", "social", "Download Pinterest videos and pins. Save inspiration."),
    ("download-reddit-videos.html", "Reddit", "🔴", "#ff4500", "#cc3700", "social", "Download Reddit videos from any subreddit."),
    ("download-tumblr-videos.html", "Tumblr", "📝", "#35465c", "#2a3849", "social", "Download Tumblr videos and GIFs."),
    ("download-linkedin-videos.html", "LinkedIn", "💼", "#0a66c2", "#085299", "social", "Download LinkedIn videos. Professional content."),
    ("download-snapchat-videos.html", "Snapchat", "👻", "#fffc00", "#ccca00", "social", "Download Snapchat spotlight videos."),
    ("download-threads-videos.html", "Threads", "🧵", "#000000", "#333333", "social", "Download Threads videos. Meta's Twitter alternative."),
    ("download-bluesky-videos.html", "Bluesky", "🦋", "#0085ff", "#006acc", "social", "Download Bluesky videos. Decentralized social media."),
    ("download-telegram-videos.html", "Telegram", "✈️", "#0088cc", "#006da3", "social", "Download Telegram videos from public channels."),
    ("download-mastodon-videos.html", "Mastodon", "🐘", "#6364ff", "#4f50cc", "social", "Download Mastodon videos. Federated social network."),
    
    # Regional Platforms
    ("download-douyin-videos.html", "Douyin", "🎵", "#000000", "#ff0050", "regional", "Download Douyin videos. Chinese TikTok."),
    ("download-weibo-videos.html", "Weibo", "🌐", "#df2029", "#b21920", "regional", "Download Weibo videos. Chinese social media."),
    ("download-vk-videos.html", "VK", "💙", "#4a76a8", "#3b5e86", "regional", "Download VK videos. Russian social network."),
    ("download-okru-videos.html", "OK.ru", "🟠", "#ee8208", "#be6806", "regional", "Download OK.ru videos. Russian platform."),
    ("download-rutube-videos.html", "Rutube", "🎬", "#00b0ec", "#008dbd", "regional", "Download Rutube videos. Russian video platform."),
    ("download-niconico-videos.html", "Niconico", "📺", "#252525", "#1a1a1a", "regional", "Download Niconico videos. Japanese video platform."),
    ("download-xiaohongshu-videos.html", "Xiaohongshu", "📕", "#ff2442", "#cc1d35", "regional", "Download Xiaohongshu videos. Little Red Book."),
    
    # Misc
    ("download-imgur-videos.html", "Imgur", "📸", "#1bb76e", "#169258", "social", "Download Imgur videos and GIFs."),
    ("download-gfycat-videos.html", "Gfycat", "🎞️", "#1c1c1c", "#0a0a0a", "social", "Download Gfycat GIFs and videos."),
    ("download-9gag-videos.html", "9GAG", "😂", "#000000", "#333333", "social", "Download 9GAG videos and memes."),
    ("download-coub-videos.html", "Coub", "🔄", "#2e8be5", "#2570b7", "video", "Download Coub loops and videos."),
    ("download-ted-videos.html", "TED", "💡", "#e62b1e", "#b82218", "video", "Download TED talks and educational videos."),
    ("download-likee-videos.html", "Likee", "❤️", "#00d5b8", "#00aa93", "social", "Download Likee videos. Short video platform."),
    ("download-kwai-videos.html", "Kwai", "🎥", "#ff6c00", "#cc5600", "social", "Download Kwai videos."),
    ("download-triller-videos.html", "Triller", "🎤", "#ff007f", "#cc0066", "social", "Download Triller videos."),
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="keywords" content="{name} downloader, download {name} videos, {name} video saver, free {name} download">
    <meta name="author" content="TikGrab">
    <meta property="og:title" content="{name} Video Downloader | TikGrab">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tikgrab.net/{filename}">
    <link rel="canonical" href="https://tikgrab.net/{filename}">
    <title>{name} Video Downloader - Download Free | TikGrab</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="pages.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>

<body>
    <header class="header">
        <div class="header-container">
            <a href="index.html" class="logo">
                <span class="logo-icon">⚡</span>
                <span class="logo-text">Tik<span class="logo-accent">Grab</span></span>
            </a>
            <nav class="nav">
                <a href="index.html" class="nav-link">Home</a>
                <a href="platforms.html" class="nav-link">All Sites</a>
                <a href="faq.html" class="nav-link">FAQ</a>
                <button class="theme-toggle" id="themeToggle" aria-label="Toggle Theme">
                    <span class="theme-icon">🌙</span>
                </button>
            </nav>
        </div>
    </header>

    <main>
        <section class="platform-hero" style="--platform-color: {color1};">
            <div class="platform-badge">
                <span class="platform-badge-icon">{emoji}</span>
                <span>{name}</span>
            </div>
            <h1>{name} Video Downloader</h1>
            <p class="platform-subtitle">{description}</p>

            <div class="download-card">
                <div class="input-wrapper">
                    <input type="text" class="url-input" id="urlInput" placeholder="Paste {name} video URL here..." autocomplete="off">
                    <button class="paste-btn" id="pasteBtn">📋 Paste</button>
                </div>
                <button class="download-btn" id="downloadBtn">
                    <span class="btn-text">Download</span>
                    <span class="btn-icon">⬇</span>
                </button>
            </div>
        </section>

        <section class="platform-features">
            <h2>Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Fast Downloads</h3>
                    <p>Download {name} videos quickly with our optimized servers.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3>HD Quality</h3>
                    <p>Save videos in the highest quality available.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎵</div>
                    <h3>Audio Extract</h3>
                    <p>Download just the audio as MP3.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>100% Safe</h3>
                    <p>No registration required. Your privacy protected.</p>
                </div>
            </div>
        </section>

        <section class="platform-howto">
            <h2>How to Download {name} Videos</h2>
            <div class="steps-list">
                <div class="step">
                    <span class="step-number">1</span>
                    <div class="step-content">
                        <h3>Copy the {name} URL</h3>
                        <p>Open {name}, find the video, and copy the URL from your browser or the share button.</p>
                    </div>
                </div>
                <div class="step">
                    <span class="step-number">2</span>
                    <div class="step-content">
                        <h3>Paste & Download</h3>
                        <p>Paste the URL in the box above and click Download.</p>
                    </div>
                </div>
                <div class="step">
                    <span class="step-number">3</span>
                    <div class="step-content">
                        <h3>Save Your Video</h3>
                        <p>Choose your quality and save the video to your device.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="other-platforms">
            <h2>Download from Other Platforms</h2>
            <div class="platforms-mini-grid">
                <a href="download-tiktok-videos.html" class="platform-mini-card">🎵 TikTok</a>
                <a href="download-youtube-videos.html" class="platform-mini-card">▶️ YouTube</a>
                <a href="download-instagram-videos.html" class="platform-mini-card">📷 Instagram</a>
                <a href="download-twitter-videos.html" class="platform-mini-card">🐦 Twitter</a>
                <a href="platforms.html" class="platform-mini-card">🌐 All Platforms</a>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="footer-content">
            <div class="footer-logo">
                <span class="logo-icon">⚡</span>
                <span>TikGrab</span>
            </div>
            <p class="footer-text">© 2025 TikGrab. All rights reserved.</p>
            <div class="footer-links">
                <a href="privacy.html">Privacy Policy</a>
                <a href="terms.html">Terms of Service</a>
                <a href="dmca.html">DMCA</a>
                <a href="contact.html">Contact</a>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
    <script src="theme.js"></script>
</body>
</html>
'''

def generate_pages():
    count = 0
    for filename, name, emoji, color1, color2, category, description in PLATFORMS:
        content = TEMPLATE.format(
            filename=filename,
            name=name,
            emoji=emoji,
            color1=color1,
            color2=color2,
            category=category,
            description=description
        )
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Generated: {filename}")
    print(f"\nTotal: {count} pages generated")

if __name__ == "__main__":
    generate_pages()
