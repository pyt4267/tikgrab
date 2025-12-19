"""
Add new video platform download pages
Categories: Anime, Movies/TV, Popular
"""
import os

# New platforms to add
NEW_PLATFORMS = [
    # Anime Platforms
    ("download-crunchyroll-videos.html", "Crunchyroll", "#f47521", "#c45e1a", 
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.76 5-5 5z"/>',
     "Download Crunchyroll anime episodes. Watch offline without subscription."),
    
    ("download-funimation-videos.html", "Funimation", "#5b0bb5", "#480994",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Funimation anime. Save dubbed and subbed episodes."),
    
    ("download-9anime-videos.html", "9Anime", "#2196f3", "#1976d2",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download anime from 9Anime. Free anime streaming downloads."),
    
    ("download-gogoanime-videos.html", "GogoAnime", "#00c853", "#00a843",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download GogoAnime videos. Popular anime streaming site."),
    
    ("download-animepahe-videos.html", "AnimePahe", "#e91e63", "#c2185b",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download AnimePahe episodes. High quality anime downloads."),
    
    ("download-kissanime-videos.html", "KissAnime", "#ff5722", "#e64a19",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download KissAnime videos. Classic anime streaming."),
    
    ("download-zoro-videos.html", "Zoro.to", "#ffeb3b", "#fbc02d",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download anime from Zoro.to. Ad-free anime streaming."),
    
    ("download-aniwatch-videos.html", "AniWatch", "#9c27b0", "#7b1fa2",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download AniWatch anime episodes. Modern anime platform."),
    
    # Movies/TV Platforms  
    ("download-odysee-videos.html", "Odysee", "#e50914", "#b8070f",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Odysee videos. Decentralized video platform."),
    
    ("download-bitchute-videos.html", "BitChute", "#ef6c00", "#e65100",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download BitChute videos. Alternative video hosting."),
    
    ("download-peertube-videos.html", "PeerTube", "#f1680d", "#c75500",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download PeerTube videos. Open-source video platform."),
    
    ("download-veoh-videos.html", "Veoh", "#ff9800", "#f57c00",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Veoh videos. Long-form video content."),
    
    ("download-metacafe-videos.html", "Metacafe", "#00bcd4", "#0097a7",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Metacafe videos. Short-form entertainment."),
    
    ("download-viki-videos.html", "Viki", "#1ce783", "#17b86a",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Viki K-dramas and Asian content."),
    
    ("download-dramacool-videos.html", "DramaCool", "#673ab7", "#512da8",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Korean dramas from DramaCool."),
    
    # Popular Platforms
    ("download-lbry-videos.html", "LBRY", "#2f9176", "#267a63",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download LBRY videos. Blockchain-based video platform."),
    
    ("download-dtube-videos.html", "DTube", "#ff0000", "#cc0000",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download DTube videos. Decentralized YouTube alternative."),
    
    ("download-floatplane-videos.html", "Floatplane", "#00aeef", "#0095cc",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Floatplane creator content."),
    
    ("download-nebula-videos.html", "Nebula", "#5a67d8", "#4c56b8",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Nebula educational videos."),
    
    ("download-curiositystream-videos.html", "CuriosityStream", "#00a3e0", "#0088bb",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download CuriosityStream documentaries."),
    
    ("download-patreon-videos.html", "Patreon", "#ff424d", "#e63946",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Patreon exclusive content."),
    
    ("download-vidlii-videos.html", "VidLii", "#ff6600", "#e65c00",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download VidLii videos. Retro YouTube clone."),
    
    ("download-liveleak-videos.html", "LiveLeak", "#cc0000", "#aa0000",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download LiveLeak videos. News and current events."),
    
    ("download-izlesene-videos.html", "İzlesene", "#ff5722", "#e64a19",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download İzlesene videos. Turkish video platform."),
    
    ("download-aparat-videos.html", "Aparat", "#ed1c24", "#c41920",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>',
     "Download Aparat videos. Iranian video sharing."),
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
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
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
                <div class="feature-card-premium"><div class="feature-icon-premium">⚡</div><h3>Lightning Fast</h3><p>Our servers process your download instantly.</p></div>
                <div class="feature-card-premium"><div class="feature-icon-premium">📱</div><h3>HD Quality</h3><p>Save videos in the highest quality available.</p></div>
                <div class="feature-card-premium"><div class="feature-icon-premium">🎵</div><h3>Extract Audio</h3><p>Download just the audio track as MP3.</p></div>
                <div class="feature-card-premium"><div class="feature-icon-premium">🔒</div><h3>100% Private</h3><p>No registration. We don't store your data.</p></div>
            </div>
        </section>

        <section class="steps-premium">
            <div class="steps-container">
                <h2>How to Download {name} Videos</h2>
                <div class="steps-timeline">
                    <div class="step-item"><div class="step-number-premium">1</div><div class="step-content-premium"><h3>Copy the {name} URL</h3><p>Open {name}, find the video and copy the URL.</p></div></div>
                    <div class="step-item"><div class="step-number-premium">2</div><div class="step-content-premium"><h3>Paste & Download</h3><p>Paste the URL above and click "Download Now".</p></div></div>
                    <div class="step-item"><div class="step-number-premium">3</div><div class="step-content-premium"><h3>Save to Your Device</h3><p>Choose quality and save the video.</p></div></div>
                </div>
            </div>
        </section>

        <section class="other-platforms-premium">
            <h2>Also Download From</h2>
            <div class="platforms-chips">
                <a href="download-tiktok-videos.html" class="platform-chip">🎵 TikTok</a>
                <a href="download-youtube-videos.html" class="platform-chip">▶️ YouTube</a>
                <a href="download-instagram-videos.html" class="platform-chip">📷 Instagram</a>
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

def generate_new_platforms():
    count = 0
    for filename, name, color1, color2, svg_path, description in NEW_PLATFORMS:
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
        print(f"Created: {filename}")
    print(f"\nTotal: {count} new platform pages created")

if __name__ == "__main__":
    generate_new_platforms()
