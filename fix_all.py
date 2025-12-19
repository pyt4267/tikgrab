"""
Fix remaining pages:
1. Generate premium pages for missing platforms
2. Fix 2024 -> 2025
3. Fix email
"""
import os
import re

# Platforms that need premium upgrade
MISSING_PLATFORMS = [
    ("download-9gag-videos.html", "9GAG", "#000000", "#333333", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download 9GAG videos and memes."),
    ("download-bandcamp-music.html", "Bandcamp", "#1da0c3", "#177a96", '<path d="M0 18.75l7.437-13.5H24l-7.438 13.5H0z"/>', "Download Bandcamp music and albums."),
    ("download-bluesky-videos.html", "Bluesky", "#0085ff", "#0066cc", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Bluesky videos and posts."),
    ("download-coub-videos.html", "Coub", "#2e76fb", "#1e5bc9", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Coub looping videos."),
    ("download-douyin-videos.html", "Douyin", "#00f2ea", "#ff0050", '<path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43V8.3a8.16 8.16 0 0 0 4.77 1.52V6.35a4.85 4.85 0 0 1-1-.22l-.04.56z"/>', "Download Douyin (Chinese TikTok) videos."),
    ("download-gfycat-videos.html", "Gfycat", "#1d9bf0", "#1680c9", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Gfycat GIFs and videos."),
    ("download-imgur-videos.html", "Imgur", "#1bb76e", "#159d5c", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Imgur images and videos."),
    ("download-kwai-videos.html", "Kwai", "#ff6b00", "#cc5500", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Kwai videos."),
    ("download-likee-videos.html", "Likee", "#ff0066", "#cc0052", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Likee videos."),
    ("download-linkedin-videos.html", "LinkedIn", "#0077b5", "#005e94", '<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>', "Download LinkedIn videos."),
    ("download-mastodon-videos.html", "Mastodon", "#6364ff", "#4f50cc", '<path d="M23.268 5.313c-.35-2.578-2.617-4.61-5.304-5.004C17.51.242 15.792 0 11.813 0h-.03c-3.98 0-4.835.242-5.288.309C3.882.692 1.496 2.518.917 5.127.64 6.412.61 7.837.661 9.143c.074 1.874.088 3.745.26 5.611.118 1.24.325 2.47.62 3.68.55 2.237 2.777 4.098 4.96 4.857 2.336.792 4.849.923 7.256.38.265-.061.527-.132.786-.213.585-.184 1.27-.39 1.774-.753a.057.057 0 0 0 .023-.043v-1.809a.052.052 0 0 0-.02-.041.053.053 0 0 0-.046-.01 20.282 20.282 0 0 1-4.709.545c-2.73 0-3.463-1.284-3.674-1.818a5.593 5.593 0 0 1-.319-1.433.053.053 0 0 1 .066-.054 19.648 19.648 0 0 0 4.581.536c.376 0 .75 0 1.125-.01 2.02-.058 4.15-.205 6.106-.614 .046-.01.09-.021.135-.034 2.325-.508 4.537-2.108 4.763-6.027.009-.063.016-3.241-.008-3.305 0-.023.027-1.428-.016-2.195z"/>', "Download Mastodon videos."),
    ("download-mixcloud-music.html", "Mixcloud", "#5000ff", "#4000cc", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Mixcloud DJ mixes."),
    ("download-niconico-videos.html", "Niconico", "#252525", "#1a1a1a", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Niconico videos (Japanese platform)."),
    ("download-okru-videos.html", "OK.ru", "#ee8208", "#cc6f07", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download OK.ru (Odnoklassniki) videos."),
    ("download-rutube-videos.html", "Rutube", "#000000", "#333333", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Rutube videos (Russian platform)."),
    ("download-snapchat-videos.html", "Snapchat", "#fffc00", "#ccc900", '<path d="M12.206.793c.99 0 4.347.276 5.93 3.821.529 1.193.403 3.219.299 4.847l-.003.06c-.012.18-.022.345-.03.51.075.045.203.09.401.09.3-.016.659-.12 1.033-.301a.42.42 0 01.3-.039c.099.03.186.09.24.165 .18.24.27.48.18.72-.12.3-.39.45-.69.42l-.18-.03c-.21-.06-.42-.12-.63-.12-.12 0-.24.015-.33.045-.3.09-.5.25-.6.48-.15.36-.15.78-.18 1.11-.015.18-.03.33-.045.48-.045.36-.15.72-.3 1.05-.24.51-.66.99-1.26 1.41-.78.54-1.86.93-3.21 1.17-.45.09-.9.12-1.35.12-.39 0-.78-.03-1.17-.09-1.35-.24-2.43-.63-3.21-1.17-.6-.42-1.02-.9-1.26-1.41-.15-.33-.255-.69-.3-1.05a5.62 5.62 0 01-.045-.48c-.03-.33-.03-.75-.18-1.11-.105-.225-.3-.39-.6-.48-.09-.03-.21-.045-.33-.045-.21 0-.42.06-.63.12l-.18.03c-.3.03-.57-.12-.69-.42-.09-.24 0-.48.18-.72.054-.075.141-.135.24-.165a.42.42 0 01.3.039c.375.18.735.285 1.035.3l1.64-.63c1.05-2.61.54-4.37-.09-5.22-.66-.87-1.5-1.2-2.52-1.2L12.206.793z"/>', "Download Snapchat stories and videos."),
    ("download-spotify-podcasts.html", "Spotify", "#1db954", "#17a045", '<path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>', "Download Spotify podcasts."),
    ("download-ted-videos.html", "TED", "#e62b1e", "#b82218", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download TED Talks."),
    ("download-telegram-videos.html", "Telegram", "#0088cc", "#006da6", '<path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>', "Download Telegram videos."),
    ("download-threads-videos.html", "Threads", "#000000", "#333333", '<path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.96-.065-1.182.408-2.256 1.33-3.022.812-.675 1.89-1.058 3.119-1.109 1.057-.044 2.018.072 2.893.275l.012-1.558c.004-.513-.108-.905-.333-1.17-.262-.31-.698-.468-1.298-.468h-.052c-.517.009-.936.144-1.248.402-.231.19-.378.456-.438.79l-2.108-.262c.146-.774.525-1.418 1.131-1.914.764-.626 1.777-.958 2.932-.958h.062c1.283.011 2.288.38 2.986 1.095.629.645.951 1.529.96 2.631l-.022 3.322c-.017 2.58-.017 2.708.238 3.584l.094.312H18.58l-.044-.188c-.126-.538-.17-.895-.177-1.988.495.455 1.012.809 1.554 1.057 1.097.502 2.37.758 3.785.758l.007-.001h.003z"/>', "Download Threads videos."),
    ("download-triller-videos.html", "Triller", "#ff0089", "#cc006d", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Triller videos."),
    ("download-tumblr-videos.html", "Tumblr", "#35465c", "#2a3849", '<path d="M14.563 24c-5.093 0-7.031-3.756-7.031-6.411V9.747H5.116V6.648c3.63-1.313 4.512-4.596 4.71-6.469C9.84.051 9.941 0 9.999 0h3.517v6.114h4.801v3.633h-4.82v7.47c.016 1.001.375 2.371 2.207 2.371h.09c.631-.02 1.486-.205 1.936-.419l1.156 3.425c-.436.636-2.4 1.374-4.156 1.404h-.237z"/>', "Download Tumblr videos and GIFs."),
    ("download-vk-videos.html", "VK", "#4a76a8", "#3c5f87", '<path d="M15.684 0H8.316C1.592 0 0 1.592 0 8.316v7.368C0 22.408 1.592 24 8.316 24h7.368C22.408 24 24 22.408 24 15.684V8.316C24 1.592 22.391 0 15.684 0zm3.692 17.123h-1.744c-.66 0-.862-.525-2.049-1.714-1.033-1.01-1.49-1.135-1.744-1.135-.356 0-.458.102-.458.593v1.575c0 .424-.135.678-1.253.678-1.846 0-3.896-1.12-5.339-3.202-2.17-3.052-2.763-5.339-2.763-5.814 0-.254.102-.491.593-.491h1.744c.44 0 .61.203.78.678.847 2.49 2.27 4.675 2.865 4.675.22 0 .322-.102.322-.66V9.721c-.068-1.186-.695-1.287-.695-1.71 0-.203.17-.407.44-.407h2.744c.373 0 .508.203.508.643v3.473c0 .372.17.508.271.508.22 0 .407-.136.813-.542 1.254-1.406 2.151-3.574 2.151-3.574.119-.254.305-.491.729-.491h1.744c.525 0 .644.27.525.644-.22 1.017-2.354 4.031-2.354 4.031-.186.305-.254.44 0 .78.186.254.796.779 1.203 1.253.745.847 1.32 1.558 1.473 2.049.17.457-.085.694-.576.694z"/>', "Download VK videos."),
    ("download-weibo-videos.html", "Weibo", "#df2029", "#b21a21", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Weibo videos."),
    ("download-xiaohongshu-videos.html", "Xiaohongshu", "#ff2442", "#cc1d35", '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>', "Download Xiaohongshu (RED) videos."),
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="keywords" content="{name} downloader, download {name} videos, {name} video saver, free download">
    <meta name="author" content="TikGrab">
    <meta property="og:title" content="{name} Video Downloader | TikGrab">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tikgrab.net/{filename}">
    <link rel="canonical" href="https://tikgrab.net/{filename}">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
    <title>{name} Video Downloader - Download Free | TikGrab</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="pages.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        .platform-hero-premium {{
            padding: calc(80px + 3rem) 1.5rem 3rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .platform-hero-premium::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(ellipse at 30% 20%, {color1}22 0%, transparent 50%),
                radial-gradient(ellipse at 70% 80%, {color2}22 0%, transparent 50%);
            pointer-events: none;
        }}
        
        .hero-content {{ position: relative; z-index: 1; max-width: 700px; margin: 0 auto; }}
        
        .logo-wrapper {{
            width: 100px; height: 100px; margin: 0 auto 1.5rem;
            background: linear-gradient(135deg, {color1}, {color2});
            border-radius: 24px; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 60px {color1}66, 0 0 100px {color2}44;
            animation: pulse 3s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        .logo-wrapper svg {{ width: 50px; height: 50px; color: white; }}
        
        .platform-hero-premium h1 {{
            font-size: clamp(2rem, 6vw, 3.5rem); font-weight: 800; margin-bottom: 0.75rem;
            background: linear-gradient(135deg, {color1}, {color2});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        }}
        
        .subtitle {{ font-size: 1.25rem; color: var(--text-secondary); margin-bottom: 2.5rem; }}
        
        .download-card-premium {{
            background: rgba(20, 20, 30, 0.9); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 2rem; backdrop-filter: blur(20px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        }}
        
        .input-row {{ display: flex; gap: 0.75rem; margin-bottom: 1rem; }}
        
        .url-input-premium {{
            flex: 1; padding: 1.25rem 1.5rem; background: rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.1); border-radius: 14px;
            color: #fff; font-size: 1.1rem; font-family: var(--font-main); transition: all 0.3s ease;
        }}
        
        .url-input-premium:focus {{ outline: none; border-color: {color1}; box-shadow: 0 0 30px {color1}44; }}
        .url-input-premium::placeholder {{ color: rgba(255, 255, 255, 0.4); }}
        
        .paste-btn-premium {{
            padding: 1.25rem 1.5rem; background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2); border-radius: 14px;
            color: #fff; font-size: 1rem; font-weight: 600; cursor: pointer;
            transition: all 0.3s ease; display: flex; align-items: center; gap: 0.5rem;
        }}
        
        .paste-btn-premium:hover {{ background: rgba(255, 255, 255, 0.15); }}
        
        .download-btn-premium {{
            width: 100%; padding: 1.25rem;
            background: linear-gradient(135deg, {color1}, {color2});
            border: none; border-radius: 14px; color: #fff; font-size: 1.2rem; font-weight: 700;
            cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.75rem;
            transition: all 0.3s ease; box-shadow: 0 10px 40px {color1}44;
        }}
        
        .download-btn-premium:hover {{ transform: translateY(-3px); box-shadow: 0 15px 50px {color1}66; }}
        .download-btn-premium svg {{ width: 24px; height: 24px; }}
        
        .features-premium {{ padding: 4rem 1.5rem; max-width: 1100px; margin: 0 auto; }}
        .features-premium h2 {{ text-align: center; font-size: 2rem; margin-bottom: 2.5rem; color: var(--text-primary); }}
        .features-grid-premium {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }}
        
        .feature-card-premium {{
            background: var(--bg-card); border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px; padding: 2rem; transition: all 0.3s ease;
        }}
        
        .feature-card-premium:hover {{ border-color: {color1}44; transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2); }}
        
        .feature-icon-premium {{
            width: 56px; height: 56px;
            background: linear-gradient(135deg, {color1}33, {color2}33);
            border-radius: 14px; display: flex; align-items: center; justify-content: center;
            font-size: 1.75rem; margin-bottom: 1rem;
        }}
        
        .feature-card-premium h3 {{ font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; }}
        .feature-card-premium p {{ color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; }}
        
        .steps-premium {{ padding: 4rem 1.5rem; background: linear-gradient(180deg, transparent, {color1}08, transparent); }}
        .steps-container {{ max-width: 900px; margin: 0 auto; }}
        .steps-premium h2 {{ text-align: center; font-size: 2rem; margin-bottom: 3rem; color: var(--text-primary); }}
        .steps-timeline {{ display: flex; flex-direction: column; gap: 1.5rem; }}
        .step-item {{ display: flex; gap: 1.5rem; align-items: flex-start; }}
        
        .step-number-premium {{
            width: 48px; height: 48px; min-width: 48px;
            background: linear-gradient(135deg, {color1}, {color2});
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 1.25rem; font-weight: 800; color: #fff; box-shadow: 0 0 30px {color1}44;
        }}
        
        .step-content-premium {{
            flex: 1; background: var(--bg-card); border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px; padding: 1.5rem;
        }}
        
        .step-content-premium h3 {{ font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; }}
        .step-content-premium p {{ color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; margin: 0; }}
        
        .other-platforms-premium {{ padding: 4rem 1.5rem; text-align: center; }}
        .other-platforms-premium h2 {{ font-size: 1.5rem; margin-bottom: 2rem; color: var(--text-primary); }}
        .platforms-chips {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 0.75rem; max-width: 800px; margin: 0 auto; }}
        
        .platform-chip {{
            display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem;
            background: var(--bg-card); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 100px; color: var(--text-secondary); text-decoration: none;
            font-weight: 500; transition: all 0.3s ease;
        }}
        
        .platform-chip:hover {{ border-color: {color1}; color: {color1}; transform: translateY(-2px); box-shadow: 0 10px 30px {color1}33; }}
        .platform-chip svg {{ width: 20px; height: 20px; }}
        
        @media (max-width: 600px) {{
            .input-row {{ flex-direction: column; }}
            .paste-btn-premium {{ justify-content: center; }}
            .step-item {{ flex-direction: column; align-items: center; text-align: center; }}
        }}
    </style>
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
        <section class="platform-hero-premium">
            <div class="hero-content">
                <div class="logo-wrapper">
                    <svg viewBox="0 0 24 24" fill="currentColor">{svg_path}</svg>
                </div>
                <h1>{name} Video Downloader</h1>
                <p class="subtitle">{description}</p>
                
                <div class="download-card-premium">
                    <div class="input-row">
                        <input type="text" class="url-input-premium" id="urlInput" placeholder="Paste {name} video URL here..." autocomplete="off">
                        <button class="paste-btn-premium" id="pasteBtn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
                            Paste
                        </button>
                    </div>
                    <button class="download-btn-premium" id="downloadBtn">
                        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
                        Download Now
                    </button>
                </div>
            </div>
        </section>

        <section class="features-premium">
            <h2>Why Choose TikGrab?</h2>
            <div class="features-grid-premium">
                <div class="feature-card-premium"><div class="feature-icon-premium">⚡</div><h3>Lightning Fast</h3><p>Our servers process your download instantly. No waiting.</p></div>
                <div class="feature-card-premium"><div class="feature-icon-premium">📱</div><h3>HD Quality</h3><p>Save videos in the highest quality available.</p></div>
                <div class="feature-card-premium"><div class="feature-icon-premium">🎵</div><h3>Extract Audio</h3><p>Download just the audio track as MP3.</p></div>
                <div class="feature-card-premium"><div class="feature-icon-premium">🔒</div><h3>100% Private</h3><p>No registration. We don't store your data.</p></div>
            </div>
        </section>

        <section class="steps-premium">
            <div class="steps-container">
                <h2>How to Download {name} Videos</h2>
                <div class="steps-timeline">
                    <div class="step-item"><div class="step-number-premium">1</div><div class="step-content-premium"><h3>Copy the {name} URL</h3><p>Open {name}, find the video and copy the URL from your browser or share button.</p></div></div>
                    <div class="step-item"><div class="step-number-premium">2</div><div class="step-content-premium"><h3>Paste & Download</h3><p>Paste the URL in the box above and click "Download Now".</p></div></div>
                    <div class="step-item"><div class="step-number-premium">3</div><div class="step-content-premium"><h3>Save to Your Device</h3><p>Choose your quality and save the video directly to your device.</p></div></div>
                </div>
            </div>
        </section>

        <section class="other-platforms-premium">
            <h2>Also Download From</h2>
            <div class="platforms-chips">
                <a href="download-tiktok-videos.html" class="platform-chip">🎵 TikTok</a>
                <a href="download-youtube-videos.html" class="platform-chip">▶️ YouTube</a>
                <a href="download-instagram-videos.html" class="platform-chip">📷 Instagram</a>
                <a href="download-twitter-videos.html" class="platform-chip">🐦 X (Twitter)</a>
                <a href="platforms.html" class="platform-chip">🌐 All Platforms</a>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="footer-content">
            <div class="footer-logo"><span class="logo-icon">⚡</span><span>TikGrab</span></div>
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

def generate_missing_pages():
    count = 0
    for filename, name, color1, color2, svg_path, description in MISSING_PLATFORMS:
        content = TEMPLATE.format(
            filename=filename,
            name=name,
            color1=color1,
            color2=color2,
            svg_path=svg_path,
            description=description
        )
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Generated: {filename}")
    print(f"\nTotal: {count} pages upgraded to premium")

def fix_year_and_email():
    files_to_fix = ['privacy.html', 'terms.html', 'contact.html', 'faq.html', 'dmca.html']
    for filename in files_to_fix:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            # Fix year
            content = content.replace('2024', '2025')
            # Fix email
            content = content.replace('support@tikgrab.com', 'taiki5660@gmail.com')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filename}")

if __name__ == "__main__":
    generate_missing_pages()
    fix_year_and_email()
