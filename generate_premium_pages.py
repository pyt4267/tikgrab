"""
TikGrab - Premium Platform Download Pages Generator
Generates all download-*.html pages with the new premium design
"""

import os

# Platform definitions: (filename, name, color1, color2, svg_path, features)
PLATFORMS = [
    # Major Platforms
    ("download-youtube-videos.html", "YouTube", "#ff0000", "#cc0000", 
     '<path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>',
     "Download YouTube videos in HD, 4K quality. Save videos, Shorts, and extract audio as MP3."),
    
    ("download-instagram-videos.html", "Instagram", "#833ab4", "#fd1d1d",
     '<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>',
     "Download Instagram Reels, Stories, IGTV, and posts. Save videos and photos easily."),
    
    ("download-twitter-videos.html", "X (Twitter)", "#000000", "#333333",
     '<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>',
     "Download Twitter and X videos, GIFs, and images. Save tweets easily."),
    
    ("download-facebook-videos.html", "Facebook", "#1877f2", "#0d5fc5",
     '<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>',
     "Download Facebook videos from posts, pages, and groups in HD quality."),
    
    ("download-vimeo-videos.html", "Vimeo", "#1ab7ea", "#0d8ecf",
     '<path d="M23.977 6.416c-.105 2.338-1.739 5.543-4.894 9.609-3.268 4.247-6.026 6.37-8.29 6.37-1.409 0-2.578-1.294-3.553-3.881L5.322 11.4C4.603 8.816 3.834 7.522 3.01 7.522c-.179 0-.806.378-1.881 1.132L0 7.197c1.185-1.044 2.351-2.084 3.501-3.128C5.08 2.701 6.266 1.984 7.055 1.91c1.867-.18 3.016 1.1 3.447 3.838.465 2.953.789 4.789.971 5.507.539 2.45 1.131 3.674 1.776 3.674.502 0 1.256-.796 2.265-2.385 1.004-1.589 1.54-2.797 1.612-3.628.144-1.371-.395-2.061-1.614-2.061-.574 0-1.167.121-1.777.391 1.186-3.868 3.434-5.757 6.762-5.637 2.473.06 3.628 1.664 3.493 4.797l-.013.01z"/>',
     "Download Vimeo videos in high quality. Professional video content."),
    
    ("download-twitch-videos.html", "Twitch", "#9146ff", "#6441a5",
     '<path d="M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714z"/>',
     "Download Twitch clips, VODs, and highlights. Save gaming content."),
    
    ("download-dailymotion-videos.html", "Dailymotion", "#0066dc", "#004a9f",
     '<path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm4.5 16.5l-6-4.5v9l6-4.5z"/>',
     "Download Dailymotion videos in various quality options."),
    
    ("download-bilibili-videos.html", "Bilibili", "#00a1d6", "#0078a8",
     '<path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.995 1.524 2.249 1.56 3.76v7.36c-.036 1.51-.556 2.769-1.56 3.773s-2.262 1.524-3.773 1.56H5.333c-1.51-.036-2.769-.556-3.773-1.56S.036 18.858 0 17.347v-7.36c.036-1.511.556-2.765 1.56-3.76 1.004-.996 2.262-1.52 3.773-1.574h.774l-1.174-1.12a1.234 1.234 0 0 1-.373-.906c0-.356.124-.658.373-.907l.027-.027c.267-.249.573-.373.92-.373.347 0 .653.124.92.373L9.653 4.44c.071.071.134.142.187.213h4.267a.836.836 0 0 1 .16-.213l2.853-2.747c.267-.249.573-.373.92-.373.347 0 .662.151.929.4.267.249.391.551.391.907 0 .355-.124.657-.373.906z"/>',
     "Download Bilibili videos. Popular Chinese video platform."),
    
    ("download-soundcloud-music.html", "SoundCloud", "#ff5500", "#cc4400",
     '<path d="M1.175 12.225c-.051 0-.094.046-.101.1l-.233 2.154.233 2.105c.007.058.05.098.101.098.05 0 .09-.04.099-.098l.255-2.105-.27-2.154c-.009-.06-.052-.1-.084-.1zm4.35 2.31c-.255 0-.495.045-.705.135-.15-1.62-1.5-2.895-3.15-2.895-.405 0-.795.075-1.15.225-.135.06-.18.12-.18.24v5.67c0 .12.09.225.21.24h5.01c1.02 0 1.845-.825 1.845-1.845 0-1.005-.84-1.77-1.88-1.77z"/>',
     "Download SoundCloud tracks as MP3. Free music downloads."),
    
    ("download-pinterest-videos.html", "Pinterest", "#bd081c", "#8c0615",
     '<path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.162-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.401.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.354-.629-2.758-1.379l-.749 2.848c-.269 1.045-1.004 2.352-1.498 3.146 1.123.345 2.306.535 3.55.535 6.607 0 11.985-5.365 11.985-11.987C23.97 5.39 18.592.026 11.985.026L12.017 0z"/>',
     "Download Pinterest videos and pins. Save your inspiration."),
    
    ("download-reddit-videos.html", "Reddit", "#ff4500", "#cc3700",
     '<path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701z"/>',
     "Download Reddit videos from any subreddit."),
     
    ("download-rumble-videos.html", "Rumble", "#85c742", "#6ba832",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>',
     "Download Rumble videos. Alternative video platform content."),
     
    ("download-kick-videos.html", "Kick", "#53fc18", "#42c813",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>',
     "Download Kick clips and VODs. Streaming platform content."),
     
    ("download-streamable-videos.html", "Streamable", "#0773d8", "#0562b8",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>',
     "Download Streamable videos quickly and easily."),
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

def generate_pages():
    count = 0
    for filename, name, color1, color2, svg_path, description in PLATFORMS:
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
    print(f"\\nTotal: {count} premium pages generated")

if __name__ == "__main__":
    generate_pages()
