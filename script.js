// ========================================
// TikGrab - JavaScript (Functional Version)
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // Element Selection
    const urlInput = document.getElementById('urlInput');
    const pasteBtn = document.getElementById('pasteBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const modeTabs = document.querySelectorAll('.mode-tab');
    const themeToggle = document.getElementById('themeToggle');

    // ========================================
    // Bookmarklet URL Parameter Handler
    // ========================================
    const urlParams = new URLSearchParams(window.location.search);
    const sharedUrl = urlParams.get('url');
    if (sharedUrl && urlInput) {
        urlInput.value = sharedUrl;
        urlInput.focus();
        // Optionally auto-trigger download after a short delay
        setTimeout(() => {
            if (downloadBtn) downloadBtn.click();
        }, 500);
    }

    // Current Mode
    let currentMode = 'video';

    // Cobalt API Endpoint (Public Instance)
    const COBALT_API = 'https://api.cobalt.tools';

    // Video Proxy (Cloudflare Pages Function)
    const PROXY_URL = '/functions/download';

    // Supported platforms (Cobalt API + additional services)
    const SUPPORTED_PLATFORMS = {
        // Major Social Media
        'tiktok.com': { name: 'TikTok', icon: '🎵', color: '#00f2ea' },
        'youtube.com': { name: 'YouTube', icon: '📺', color: '#ff0000' },
        'youtu.be': { name: 'YouTube', icon: '📺', color: '#ff0000' },
        'twitter.com': { name: 'Twitter', icon: '🐦', color: '#1da1f2' },
        'x.com': { name: 'X', icon: '✖️', color: '#000000' },
        'instagram.com': { name: 'Instagram', icon: '📷', color: '#e4405f' },
        'facebook.com': { name: 'Facebook', icon: '👤', color: '#1877f2' },
        'fb.watch': { name: 'Facebook', icon: '👤', color: '#1877f2' },

        // Video Platforms
        'vimeo.com': { name: 'Vimeo', icon: '🎬', color: '#1ab7ea' },
        'dailymotion.com': { name: 'Dailymotion', icon: '🎥', color: '#0066dc' },
        'twitch.tv': { name: 'Twitch', icon: '🎮', color: '#9146ff' },
        'bilibili.com': { name: 'Bilibili', icon: '📺', color: '#00a1d6' },
        'rutube.ru': { name: 'Rutube', icon: '🎬', color: '#00b0ec' },
        'streamable.com': { name: 'Streamable', icon: '▶️', color: '#0773d8' },
        'loom.com': { name: 'Loom', icon: '🎥', color: '#625df5' },
        'ok.ru': { name: 'OK.ru', icon: '🟠', color: '#ee8208' },
        'vk.com': { name: 'VK', icon: '💙', color: '#4a76a8' },

        // Community & Forums
        'reddit.com': { name: 'Reddit', icon: '🔴', color: '#ff4500' },
        'tumblr.com': { name: 'Tumblr', icon: '📝', color: '#35465c' },
        'pinterest.com': { name: 'Pinterest', icon: '📌', color: '#bd081c' },
        'pin.it': { name: 'Pinterest', icon: '📌', color: '#bd081c' },

        // Audio
        'soundcloud.com': { name: 'SoundCloud', icon: '🎧', color: '#ff5500' },
        'bandcamp.com': { name: 'Bandcamp', icon: '🎸', color: '#629aa9' },

        // New Platforms
        'threads.net': { name: 'Threads', icon: '🧵', color: '#000000' },
        'bsky.app': { name: 'Bluesky', icon: '🦋', color: '#0085ff' },
        'bluesky.social': { name: 'Bluesky', icon: '🦋', color: '#0085ff' },
        'vine.co': { name: 'Vine', icon: '🍃', color: '#00bf8f' },

        // Asian Platforms
        'weibo.com': { name: 'Weibo', icon: '🌐', color: '#df2029' },
        'douyin.com': { name: 'Douyin', icon: '🎵', color: '#000000' },
        'xiaohongshu.com': { name: 'Xiaohongshu', icon: '📕', color: '#ff2442' },

        // Other
        'likee.video': { name: 'Likee', icon: '❤️', color: '#00d5b8' },
        'snapchat.com': { name: 'Snapchat', icon: '👻', color: '#fffc00' },
        'coub.com': { name: 'Coub', icon: '🔄', color: '#2e8be5' }
    };

    // Detect platform from URL
    function detectPlatform(url) {
        for (const [domain, info] of Object.entries(SUPPORTED_PLATFORMS)) {
            if (url.includes(domain)) {
                return { domain, ...info };
            }
        }
        return null;
    }

    // ========================================
    // Paste Button
    // ========================================
    if (pasteBtn) {
        pasteBtn.addEventListener('click', async () => {
            try {
                const text = await navigator.clipboard.readText();
                urlInput.value = text;
                urlInput.focus();

                // フィードバックアニメーション
                pasteBtn.textContent = '✓ ペースト完了';
                pasteBtn.style.color = '#22c55e';

                setTimeout(() => {
                    pasteBtn.innerHTML = '📋 ペースト';
                    pasteBtn.style.color = '';
                }, 2000);
            } catch (err) {
                console.error('クリップボードからの読み取りに失敗:', err);
                pasteBtn.textContent = '⚠ 失敗';
                pasteBtn.style.color = '#ff6b6b';

                setTimeout(() => {
                    pasteBtn.innerHTML = '📋 ペースト';
                    pasteBtn.style.color = '';
                }, 2000);
            }
        });
    }

    // ========================================
    // ダウンロードボタン
    // ========================================
    if (downloadBtn) {
        downloadBtn.addEventListener('click', async () => {
            const url = urlInput.value.trim();

            if (!url) {
                // 空の場合のフィードバック
                urlInput.style.borderColor = '#ff6b6b';
                urlInput.style.boxShadow = '0 0 20px rgba(255, 107, 107, 0.3)';
                urlInput.placeholder = 'URLを入力してください...';

                setTimeout(() => {
                    urlInput.style.borderColor = '';
                    urlInput.style.boxShadow = '';
                    urlInput.placeholder = 'TikTokのURLをここに貼り付け...';
                }, 2000);
                return;
            }

            // Multi-platform URL validation
            const platform = detectPlatform(url);
            if (!platform) {
                urlInput.style.borderColor = '#ff6b6b';
                urlInput.style.boxShadow = '0 0 20px rgba(255, 107, 107, 0.3)';

                setTimeout(() => {
                    urlInput.style.borderColor = '';
                    urlInput.style.boxShadow = '';
                }, 2000);

                showNotification('Please enter a supported URL (TikTok, YouTube, Instagram, Twitter, etc.)', 'error');
                return;
            }

            // Show detected platform
            showNotification(`${platform.icon} ${platform.name} detected!`, 'info');

            // Start download process
            downloadBtn.innerHTML = '<span class="btn-text">🔄 Processing...</span>';
            downloadBtn.disabled = true;

            try {
                const result = await downloadTikTok(url);

                if (result.success) {
                    downloadBtn.innerHTML = '<span class="btn-text">✓ Ready!</span>';
                    showNotification('Video found! Click the download button below.', 'success');

                    // Show download result (no auto-download due to CORS)
                    showDownloadResult(result);
                } else {
                    throw new Error(result.error || 'Download failed');
                }
            } catch (error) {
                console.error('Download error:', error);
                downloadBtn.innerHTML = '<span class="btn-text">⚠ Error</span>';
                showNotification(error.message || 'Download failed', 'error');
            }

            setTimeout(() => {
                downloadBtn.innerHTML = '<span class="btn-text">Download</span><span class="btn-icon">→</span>';
                downloadBtn.disabled = false;
            }, 3000);
        });
    }

    // ========================================
    // TikTokダウンロード処理
    // ========================================
    async function downloadTikTok(url) {
        try {
            // TikTok/Douyinの場合のみTikWM APIを使用
            if (url.includes('tiktok.com') || url.includes('douyin.com')) {
                console.log('TikTok URL detected, trying TikWM API...');
                const tikwmResult = await tryTikWMApi(url);
                if (tikwmResult.success) {
                    console.log('TikWM API success:', tikwmResult);
                    return tikwmResult;
                }
            }

            // TikTok以外のURLまたはTikWM失敗時
            return {
                success: false,
                error: 'This service only supports TikTok videos. Please enter a valid TikTok URL.'
            };

        } catch (error) {
            console.error('Download error:', error);
            return {
                success: false,
                error: 'Download failed. Please try again.'
            };
        }
    }

    // ========================================
    // TikWM API (TikTok専用)
    // ========================================
    async function tryTikWMApi(url) {
        try {
            // Use &hd=1 to get HD quality video
            const apiUrl = `https://www.tikwm.com/api/?url=${encodeURIComponent(url)}&hd=1`;
            const response = await fetch(apiUrl);
            const data = await response.json();

            console.log('TikWM API Response:', data);

            if (data.code === 0 && data.data) {
                const videoData = data.data;

                // TikWM URL priority (NO watermark):
                // - play: Standard quality, NO watermark ✅
                // - hdplay: HD quality, NO watermark (requires &hd=1) ✅
                // - wmplay: With watermark (avoid this!) ❌

                // Use play for standard download (no watermark)
                const downloadUrl = videoData.play;

                // Use hdplay for HD download (no watermark, requires &hd=1)
                const hdUrl = videoData.hdplay || null;

                return {
                    success: true,
                    downloadUrl: downloadUrl,
                    hdUrl: hdUrl,
                    audioUrl: videoData.music,
                    thumbnail: videoData.cover,
                    title: videoData.title,
                    author: videoData.author?.nickname
                };
            }
        } catch (e) {
            console.error('TikWM API エラー:', e);
        }
        return { success: false };
    }

    // ========================================
    // Cobalt API (Universal downloader)
    // ========================================
    async function tryCobaltApi(url) {
        try {
            const apiUrl = 'https://cobalt-backend.canine.tools/';
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: url,
                    videoQuality: '1080',
                    audioFormat: 'mp3'
                })
            });

            const data = await response.json();
            console.log('Cobalt API Response:', data);

            if (data.status === 'tunnel' || data.status === 'redirect') {
                return {
                    success: true,
                    downloadUrl: data.url,
                    filename: data.filename || 'video.mp4'
                };
            } else if (data.status === 'picker' && data.picker && data.picker.length > 0) {
                // Multiple items available, use the first one
                return {
                    success: true,
                    downloadUrl: data.picker[0].url,
                    isMultiple: true,
                    picker: data.picker
                };
            }
        } catch (e) {
            console.error('Cobalt API エラー:', e);
        }
        return { success: false };
    }

    // ========================================
    // プラットフォーム別API実装
    // ========================================

    // Instagram API (iGram)
    async function tryInstagramApi(url) {
        try {
            const apiUrl = `https://api.igram.io/api/convert`;
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `url=${encodeURIComponent(url)}`
            });
            const data = await response.json();
            if (data && data.url) {
                return { success: true, downloadUrl: data.url };
            }
        } catch (e) {
            console.error('Instagram API エラー:', e);
        }
        return { success: false };
    }

    // Twitter/X API (sssTwitter)
    async function tryTwitterApi(url) {
        try {
            const apiUrl = `https://twitsave.com/info?url=${encodeURIComponent(url)}`;
            // Note: This may require CORS proxy
            const response = await fetch(apiUrl);
            const html = await response.text();
            // Parse for download link
            const match = html.match(/href="(https:\/\/[^"]+\.mp4[^"]*)"/);
            if (match && match[1]) {
                return { success: true, downloadUrl: match[1] };
            }
        } catch (e) {
            console.error('Twitter API エラー:', e);
        }
        return { success: false };
    }

    // Reddit API
    async function tryRedditApi(url) {
        try {
            // Convert to JSON API
            const jsonUrl = url.replace(/\/$/, '') + '.json';
            const response = await fetch(jsonUrl, {
                headers: { 'User-Agent': 'TikGrab/1.0' }
            });
            const data = await response.json();
            if (data[0]?.data?.children[0]?.data?.secure_media?.reddit_video?.fallback_url) {
                const videoUrl = data[0].data.children[0].data.secure_media.reddit_video.fallback_url;
                return { success: true, downloadUrl: videoUrl.replace('?source=fallback', '') };
            }
        } catch (e) {
            console.error('Reddit API エラー:', e);
        }
        return { success: false };
    }

    // YouTube API (external service)
    async function tryYouTubeApi(url) {
        // YouTube requires server-side processing due to CORS
        // Redirect to SaveFrom.net (mobile-friendly, supports all platforms)
        try {
            return {
                success: true,
                externalRedirect: `https://9xbuddy.com/process?url=${encodeURIComponent(url)}`,
                message: 'YouTube videos require external service. Click below to proceed.'
            };
        } catch (e) {
            console.error('YouTube API エラー:', e);
        }
        return { success: false };
    }

    function extractYouTubeId(url) {
        const patterns = [
            /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
            /youtube\.com\/shorts\/([^&\n?#]+)/
        ];
        for (const pattern of patterns) {
            const match = url.match(pattern);
            if (match) return match[1];
        }
        return null;
    }

    // ========================================
    // 代替ダウンロード方法（プラットフォーム別ルーティング）
    // ========================================
    async function tryAlternativeMethod(url) {
        // プラットフォーム別にAPIを試す
        if (url.includes('instagram.com')) {
            const result = await tryInstagramApi(url);
            if (result.success) return result;
        }

        if (url.includes('twitter.com') || url.includes('x.com')) {
            const result = await tryTwitterApi(url);
            if (result.success) return result;
        }

        if (url.includes('reddit.com')) {
            const result = await tryRedditApi(url);
            if (result.success) return result;
        }

        if (url.includes('youtube.com') || url.includes('youtu.be')) {
            const result = await tryYouTubeApi(url);
            if (result.success) return result;
        }

        // TikWM を最後のフォールバックとして試す
        try {
            const apiUrl = `https://www.tikwm.com/api/?url=${encodeURIComponent(url)}`;
            const response = await fetch(apiUrl);
            const data = await response.json();

            if (data.code === 0 && data.data) {
                const videoData = data.data;
                return {
                    success: true,
                    downloadUrl: videoData.play || videoData.hdplay || videoData.wmplay,
                    hdUrl: videoData.hdplay,
                    audioUrl: videoData.music,
                    thumbnail: videoData.cover,
                    title: videoData.title,
                    author: videoData.author?.nickname
                };
            }
        } catch (e) {
            console.error('代替API エラー:', e);
        }

        // 全て失敗した場合、外部サービスへの誘導
        return {
            success: true,
            externalRedirect: `https://9xbuddy.com/process?url=${encodeURIComponent(url)}`,
            message: 'Click below to download via external service.'
        };
    }

    // ========================================
    // Auto Download with proper filename
    // ========================================
    async function autoDownload(result) {
        let downloadUrl = null;

        if (result.isMultiple && result.picker && result.picker.length > 0) {
            downloadUrl = result.picker[0].url;
        } else if (result.downloadUrl) {
            downloadUrl = result.downloadUrl;
        }

        if (downloadUrl) {
            try {
                // Fetch the video as blob to force filename
                showNotification('Preparing download...', 'info');

                const response = await fetch(downloadUrl);
                const blob = await response.blob();

                // Create blob URL and download
                const blobUrl = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = blobUrl;

                // Generate filename with timestamp
                const timestamp = Date.now();
                const filename = result.filename || `tiktok_${timestamp}.mp4`;
                link.download = filename;

                link.style.display = 'none';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                // Cleanup blob URL
                setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);

                showNotification('Download complete!', 'success');
            } catch (error) {
                console.error('Download error:', error);
                // Fallback to direct link
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.download = result.filename || 'tiktok_video.mp4';
                link.style.display = 'none';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        }
    }

    // ========================================
    // Monetag Ad Loader (Hover Trigger)
    // ========================================
    let isAdLoaded = false;
    window.loadMonetagAd = function () {
        if (isAdLoaded) return;
        isAdLoaded = true;
        // Inject Moneytag Script
        (function (s) { s.dataset.zone = '10352135', s.src = 'https://al5sm.com/tag.min.js' })([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')));
        console.log("Monetag Ad Script Injected");
    };

    // ========================================
    // Download with Proxy (Global Function)
    // ========================================
    window.downloadWithProxy = async function (videoUrl, filename) {
        const statusEl = document.getElementById('downloadStatus');

        if (statusEl) {
            statusEl.innerHTML = '<p>⏳ Downloading... Please wait.</p>';
        }

        // iOS/Safari detection
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
            (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

        // iOS Safari cannot download blobs directly - show message
        if (isIOS) {
            if (statusEl) {
                statusEl.innerHTML = `
                    <div style="text-align: left; padding: 1rem; background: rgba(255,100,100,0.1); border: 1px solid rgba(255,100,100,0.3); border-radius: 12px; margin-top: 1rem;">
                        <p style="font-weight: 600; margin-bottom: 0.5rem;">⚠️ Direct Download Not Supported on iPhone</p>
                        <p style="margin-bottom: 0.75rem; color: var(--text-secondary);">Due to Apple's restrictions, you cannot save videos directly from the browser on iOS.</p>
                        <p style="font-weight: 500; margin-bottom: 0.5rem;">💡 Alternatives:</p>
                        <ul style="margin: 0; padding-left: 1.2rem; line-height: 1.8; color: var(--text-secondary);">
                            <li><strong>"Documents by Readdle"</strong> - Use this app's built-in browser</li>
                            <li><strong>PC</strong> - Use a computer to download</li>
                        </ul>
                    </div>
                `;
            }
            return;
        }

        // Determine file type from filename argument
        const isAudio = filename.includes('.mp3') || filename.includes('audio');
        const ext = isAudio ? 'mp3' : 'mp4';
        const mimeType = isAudio ? 'audio/mpeg' : 'video/mp4';

        // Generate timestamp-based filename with correct extension
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        const safeFilename = `tiktok_${timestamp}.${ext}`;

        // Use Cloudflare Worker proxy - open directly in new tab for proper download
        const proxyUrl = `https://tikgrab-proxy.cc1053970532.workers.dev/?url=${encodeURIComponent(videoUrl)}&filename=${encodeURIComponent(safeFilename)}`;

        if (statusEl) {
            statusEl.innerHTML = `<p style="color: #4ade80;">✅ Download Started! Filename: <strong>${safeFilename}</strong></p>`;
        }

        // Open proxy URL directly - browser will download with correct filename
        window.open(proxyUrl, '_blank');
    };

    // ========================================
    // Download All Slides (Global Function)
    // ========================================
    window.downloadAllSlides = async function (urls) {
        const statusEl = document.getElementById('downloadStatus');
        if (statusEl) {
            statusEl.innerHTML = `<p>⏳ Downloading ${urls.length} files...</p>`;
        }

        for (let i = 0; i < urls.length; i++) {
            const isImage = urls[i].includes('.jpg') || urls[i].includes('.jpeg') || urls[i].includes('.png') || urls[i].includes('.webp');
            const ext = isImage ? 'jpg' : 'mp4';
            const filename = `tiktok_${i + 1}.${ext}`;

            // Download with delay to prevent browser blocking
            await new Promise(resolve => setTimeout(resolve, 500));
            downloadWithProxy(urls[i], filename);

            if (statusEl) {
                statusEl.innerHTML = `<p>⏳ Downloading ${i + 1}/${urls.length}...</p>`;
            }
        }

        setTimeout(() => {
            if (statusEl) {
                statusEl.innerHTML = `<p>✅ All ${urls.length} files downloaded!</p>`;
            }
        }, 2000);
    };

    // ========================================
    // Download Result Display (SnapTik style)
    // ========================================
    function showDownloadResult(result) {
        // 既存の結果を削除
        const existing = document.querySelector('.download-result');
        if (existing) existing.remove();

        const resultDiv = document.createElement('div');
        resultDiv.className = 'download-result';

        // 外部リダイレクトの場合
        if (result.externalRedirect) {
            resultDiv.innerHTML = `
                <div class="result-preview">
                    <div class="result-thumb-placeholder">🔗</div>
                    <div class="result-meta">
                        <p class="result-title">${result.message || 'External download available'}</p>
                    </div>
                </div>
                <div class="result-buttons">
                    <a href="${result.externalRedirect}" target="_blank" rel="noopener noreferrer" class="result-btn primary">
                        <span class="btn-icon-left">🌐</span>
                        Open Download Page
                    </a>
                    <button class="result-btn reset" onclick="this.closest('.download-result').remove(); document.getElementById('urlInput').value = ''; document.getElementById('urlInput').focus();">
                        <span class="btn-icon-left">🔄</span>
                        Try Another URL
                    </button>
                </div>
                <div class="save-tip">
                    <p>Click the button to download on the external site</p>
                </div>
            `;
        } else if (result.isMultiple && result.picker) {
            // Multiple options (Slideshow)
            const isImage = result.picker[0]?.url?.includes('.jpg') || result.picker[0]?.url?.includes('.jpeg') || result.picker[0]?.url?.includes('.png') || result.picker[0]?.url?.includes('.webp');
            const ext = isImage ? 'jpg' : 'mp4';

            resultDiv.innerHTML = `
                <div class="result-preview">
                    <div class="result-thumb-large">📸</div>
                    <p class="result-title">${result.picker.length} files found</p>
                </div>
                <div class="result-buttons">
                    ${result.picker.map((item, i) => `
                        <button class="result-btn primary" onclick="downloadWithProxy('${item.url}', 'tiktok_${i + 1}.${ext}')">
                            <span class="btn-icon-left">⬇️</span>
                            Download ${i + 1}
                        </button>
                    `).join('')}
                    <button class="result-btn secondary" onclick="downloadAllSlides(${JSON.stringify(result.picker.map(p => p.url)).replace(/"/g, '&quot;')})">
                        <span class="btn-icon-left">📦</span>
                        Download All
                    </button>
                    <button class="result-btn reset" onclick="this.closest('.download-result').remove()">
                        <span class="btn-icon-left">🔄</span>
                        Download Another
                    </button>
                </div>
                <div class="save-tip" id="downloadStatus">
                    <p>Click a button to download</p>
                </div>
            `;
        } else {
            // Single download (SnapTik style)
            const videoUrl = result.downloadUrl;
            const hdUrl = result.hdUrl;
            const audioUrl = result.audioUrl;

            resultDiv.innerHTML = `
                <div class="result-preview">
                    ${result.thumbnail ?
                    `<img src="${result.thumbnail}" alt="Thumbnail" class="result-thumb-large">` :
                    `<div class="result-thumb-placeholder">🎬</div>`
                }
                    <div class="result-meta">
                        ${result.title ? `<p class="result-title">${result.title.substring(0, 80)}${result.title.length > 80 ? '...' : ''}</p>` : '<p class="result-title">Video Ready</p>'}
                        ${result.author ? `<p class="result-author">@${result.author}</p>` : ''}
                    </div>
                </div>
                <div class="result-buttons">
                    ${hdUrl || videoUrl ? `
                        <button class="result-btn primary" onmouseenter="loadMonetagAd()" onclick="downloadWithProxy('${hdUrl || videoUrl}', 'video_hd.mp4')">
                            <span class="btn-icon-left">⬇️</span>
                            Download Video HD
                        </button>
                    ` : ''}
                    ${audioUrl ? `
                        <button class="result-btn audio" onmouseenter="loadMonetagAd()" onclick="downloadWithProxy('${audioUrl}', 'audio.mp3')">
                            <span class="btn-icon-left">🎵</span>
                            Audio Only (MP3)
                        </button>
                    ` : ''}
                    <button class="result-btn reset" onclick="this.closest('.download-result').remove(); document.getElementById('urlInput').value = ''; document.getElementById('urlInput').focus();">
                        <span class="btn-icon-left">🔄</span>
                        Download Another Video
                    </button>
                </div>
                <div class="save-tip" id="downloadStatus">
                    <p>Click a button to download</p>
                </div>
            `;
        }

        // スタイル追加
        resultDiv.style.cssText = `
            margin-top: 1.5rem;
            padding: 1.5rem;
            background: var(--bg-card);
            border: 1px solid rgba(0, 245, 255, 0.2);
            border-radius: 16px;
            animation: fadeIn 0.3s ease;
        `;

        // ダウンロードカードの後に追加 (support both classes)
        const downloadCard = document.querySelector('.download-card') || document.querySelector('.download-card-premium');
        if (downloadCard && downloadCard.parentNode) {
            downloadCard.parentNode.insertBefore(resultDiv, downloadCard.nextSibling);
        } else {
            // Fallback: append to body
            document.body.appendChild(resultDiv);
        }

        // 結果カード用スタイル
        addResultStyles();
    }

    // ========================================
    // 結果カード用スタイル (SnapTik風)
    // ========================================
    function addResultStyles() {
        if (document.getElementById('result-styles')) return;

        const style = document.createElement('style');
        style.id = 'result-styles';
        style.textContent = `
            /* プレビューエリア */
            .result-preview {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                margin-bottom: 1.5rem;
                gap: 1rem;
            }
            .result-thumb-large {
                width: 200px;
                height: 280px;
                object-fit: cover;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            }
            .result-thumb-placeholder {
                width: 200px;
                height: 200px;
                background: linear-gradient(135deg, rgba(0, 245, 255, 0.2), rgba(255, 0, 229, 0.2));
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4rem;
            }
            .result-meta {
                max-width: 100%;
            }
            .result-title {
                font-size: 1rem;
                color: var(--text-primary);
                margin-bottom: 0.5rem;
                line-height: 1.4;
            }
            .result-author {
                font-size: 0.9rem;
                color: var(--neon-cyan);
                font-weight: 500;
            }
            
            /* ボタンエリア */
            .result-buttons {
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
                align-items: center;
            }
            .result-btn {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                width: 100%;
                max-width: 300px;
                padding: 1rem 1.5rem;
                border: none;
                border-radius: 12px;
                font-family: var(--font-main);
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                text-decoration: none;
                transition: all 0.2s ease;
            }
            .result-btn .btn-icon-left {
                font-size: 1.2rem;
            }
            
            /* メインダウンロードボタン（青） */
            .result-btn.primary {
                background: linear-gradient(135deg, #3b82f6, #2563eb);
                color: #fff;
            }
            .result-btn.primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
            }
            
            /* サブサーバーボタン（緑） */
            .result-btn.secondary {
                background: linear-gradient(135deg, #22c55e, #16a34a);
                color: #fff;
            }
            .result-btn.secondary:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(34, 197, 94, 0.5);
            }
            
            /* 音声ボタン（オレンジ） */
            .result-btn.audio {
                background: linear-gradient(135deg, #f59e0b, #d97706);
                color: #fff;
            }
            .result-btn.audio:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(245, 158, 11, 0.5);
            }
            
            /* リセットボタン（ダーク） */
            .result-btn.reset {
                background: rgba(255, 255, 255, 0.1);
                color: var(--text-secondary);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .result-btn.reset:hover {
                background: rgba(255, 255, 255, 0.15);
                color: var(--text-primary);
            }
            
            /* ライトモード対応 */
            body.light-mode .result-title {
                color: var(--text-primary);
            }
            body.light-mode .result-btn.reset {
                background: rgba(0, 0, 0, 0.05);
                color: var(--text-secondary);
                border-color: rgba(0, 0, 0, 0.1);
            }
            body.light-mode .result-btn.reset:hover {
                background: rgba(0, 0, 0, 0.1);
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Save Tip */
            .save-tip {
                margin-top: 1rem;
                padding: 0.75rem;
                background: rgba(59, 130, 246, 0.1);
                border: 1px dashed rgba(59, 130, 246, 0.3);
                border-radius: 8px;
                font-size: 0.85rem;
                color: var(--text-secondary);
                text-align: center;
            }
            body.light-mode .save-tip {
                background: rgba(59, 130, 246, 0.05);
            }
        `;
        document.head.appendChild(style);
    }

    // ========================================
    // モードタブ切り替え
    // ========================================
    modeTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            modeTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentMode = tab.dataset.mode;

            // Update placeholders
            const placeholders = {
                video: 'Paste TikTok video URL here...',
                audio: 'Paste TikTok URL here (MP3 Extraction)...',
                slide: 'Paste TikTok slideshow URL here...'
            };
            urlInput.placeholder = placeholders[currentMode] || placeholders.video;

            // 結果をクリア
            const existing = document.querySelector('.download-result');
            if (existing) existing.remove();
        });
    });

    // ========================================
    // Theme Toggle (Light Mode)
    // ========================================
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const themeIcon = themeToggle.querySelector('.theme-icon');
            const isLight = document.body.classList.toggle('light-mode');

            if (isLight) {
                if (themeIcon) themeIcon.textContent = '☀️';
                localStorage.setItem('theme', 'light');
                showNotification('Switched to Light Mode', 'info');
            } else {
                if (themeIcon) themeIcon.textContent = '🌙';
                localStorage.setItem('theme', 'dark');
                showNotification('Switched to Dark Mode', 'info');
            }
        });

        // Apply saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {
            document.body.classList.add('light-mode');
            const themeIcon = themeToggle.querySelector('.theme-icon');
            if (themeIcon) themeIcon.textContent = '☀️';
        }
    }

    // ========================================
    // 通知表示
    // ========================================
    function showNotification(message, type = 'info') {
        // 既存の通知を削除
        const existing = document.querySelector('.notification');
        if (existing) existing.remove();

        // 通知要素を作成
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        // スタイル適用
        Object.assign(notification.style, {
            position: 'fixed',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            padding: '12px 24px',
            borderRadius: '12px',
            fontFamily: 'var(--font-main)',
            fontSize: '0.95rem',
            fontWeight: '500',
            zIndex: '1000',
            animation: 'slideUp 0.3s ease',
            backdropFilter: 'blur(10px)'
        });

        // タイプ別スタイル
        const styles = {
            success: {
                background: 'rgba(34, 197, 94, 0.2)',
                border: '1px solid rgba(34, 197, 94, 0.5)',
                color: '#22c55e'
            },
            error: {
                background: 'rgba(255, 107, 107, 0.2)',
                border: '1px solid rgba(255, 107, 107, 0.5)',
                color: '#ff6b6b'
            },
            info: {
                background: 'rgba(0, 245, 255, 0.2)',
                border: '1px solid rgba(0, 245, 255, 0.5)',
                color: '#00f5ff'
            }
        };

        Object.assign(notification.style, styles[type] || styles.info);

        document.body.appendChild(notification);

        // 自動削除
        setTimeout(() => {
            notification.style.animation = 'slideDown 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // アニメーション用CSS追加
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            from { opacity: 0; transform: translateX(-50%) translateY(20px); }
            to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }
        @keyframes slideDown {
            from { opacity: 1; transform: translateX(-50%) translateY(0); }
            to { opacity: 0; transform: translateX(-50%) translateY(20px); }
        }
    `;
    document.head.appendChild(style);

    // ========================================
    // キーボードショートカット
    // ========================================
    if (urlInput && downloadBtn) {
        urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                downloadBtn.click();
            }
        });
    }
});

