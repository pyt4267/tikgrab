// ========================================
// TikGrab - JavaScript (実機能版)
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // 要素取得
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

    // 現在のモード
    let currentMode = 'video';

    // Cobalt API エンドポイント (公開インスタンス)
    const COBALT_API = 'https://api.cobalt.tools';

    // Video Proxy (Netlify Function)
    const PROXY_URL = '/.netlify/functions/download';

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
    // ペーストボタン
    // ========================================
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

    // ========================================
    // ダウンロードボタン
    // ========================================
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

    // ========================================
    // TikTokダウンロード処理
    // ========================================
    async function downloadTikTok(url) {
        try {
            // Cobalt APIを使用
            const response = await fetch(COBALT_API, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    downloadMode: currentMode === 'audio' ? 'audio' : 'auto',
                    filenameStyle: 'pretty',
                    videoQuality: '1080'
                })
            });

            if (!response.ok) {
                // Cobalt APIが使えない場合、代替方法を試す
                return await tryAlternativeMethod(url);
            }

            const data = await response.json();

            if (data.status === 'error') {
                return await tryAlternativeMethod(url);
            }

            // ダウンロードURLを取得
            if (data.url) {
                return {
                    success: true,
                    downloadUrl: data.url,
                    filename: data.filename || 'tiktok_video.mp4'
                };
            }

            // 複数のピッカーがある場合
            if (data.picker) {
                return {
                    success: true,
                    picker: data.picker,
                    isMultiple: true
                };
            }

            return await tryAlternativeMethod(url);

        } catch (error) {
            console.error('Cobalt API エラー:', error);
            return await tryAlternativeMethod(url);
        }
    }

    // ========================================
    // 代替ダウンロード方法
    // ========================================
    async function tryAlternativeMethod(url) {
        // tikwm.com API を試す (代替)
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

        // 両方失敗した場合
        return {
            success: false,
            error: 'ダウンロードサービスに接続できません。しばらく後でお試しください。'
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
    // Download with Proxy (Global Function)
    // ========================================
    window.downloadWithProxy = function (videoUrl, filename) {
        const statusEl = document.getElementById('downloadStatus');

        if (PROXY_URL) {
            // Use Cloudflare Worker proxy
            const proxyLink = `${PROXY_URL}?url=${encodeURIComponent(videoUrl)}&filename=${encodeURIComponent(filename)}`;

            if (statusEl) {
                statusEl.innerHTML = '<p>⏳ Downloading via proxy...</p>';
            }

            // Use hidden iframe to download (prevents page navigation)
            let iframe = document.getElementById('downloadFrame');
            if (!iframe) {
                iframe = document.createElement('iframe');
                iframe.id = 'downloadFrame';
                iframe.style.display = 'none';
                document.body.appendChild(iframe);
            }
            iframe.src = proxyLink;

            setTimeout(() => {
                if (statusEl) {
                    statusEl.innerHTML = '<p>✅ Download started! Check your downloads folder.</p>';
                }
            }, 2000);
        } else {
            // Direct download (filename may be random)
            if (statusEl) {
                statusEl.innerHTML = '<p>⏳ Opening video... Right-click and save if needed.</p>';
            }

            // Use hidden link with download attribute
            const link = document.createElement('a');
            link.href = videoUrl;
            link.download = filename;
            link.target = '_blank';
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            setTimeout(() => {
                if (statusEl) {
                    statusEl.innerHTML = `<p><strong>📁 Note:</strong> Filename may be random. Rename to <code>${filename}</code></p>`;
                }
            }, 1000);
        }
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

        if (result.isMultiple && result.picker) {
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
                        ${result.title ? `<p class="result-title">${result.title.substring(0, 80)}${result.title.length > 80 ? '...' : ''}</p>` : '<p class="result-title">TikTok Video</p>'}
                        ${result.author ? `<p class="result-author">@${result.author}</p>` : ''}
                    </div>
                </div>
                <div class="result-buttons">
                    ${videoUrl ? `
                        <button class="result-btn primary" onclick="downloadWithProxy('${videoUrl}', 'tiktok_video.mp4')">
                            <span class="btn-icon-left">⬇️</span>
                            Download Video
                        </button>
                    ` : ''}
                    ${hdUrl && hdUrl !== videoUrl ? `
                        <button class="result-btn secondary" onclick="downloadWithProxy('${hdUrl}', 'tiktok_video_hd.mp4')">
                            <span class="btn-icon-left">⬇️</span>
                            Server 02 (HD)
                </button>
                    ` : ''}
                    ${hdUrl && hdUrl !== videoUrl ? `
                        <button class="result-btn secondary" onclick="downloadWithProxy('${hdUrl}', 'tiktok_video_hd.mp4')">
                            <span class="btn-icon-left">⬇️</span>
                            Server 02 (HD)
                        </button>
                    ` : ''}
                    <!-- Native Ad Space (Between Buttons) -->
                    <div class="ad-native-inline" id="adNativeInline">
                        <div class="ad-label-small">Ad</div>
                        <!-- Adsterra Native Ad will be inserted here -->
                    </div>
                    ${audioUrl ? `
                        <button class="result-btn audio" onclick="downloadWithProxy('${audioUrl}', 'tiktok_audio.mp3')">
                            <span class="btn-icon-left">🎵</span>
                            Audio Only (MP3)
                        </button>
                    ` : ''}
                    <button class="result-btn reset" onclick="this.closest('.download-result').remove(); document.getElementById('urlInput').value = ''; document.getElementById('urlInput').focus();">
                        <span class="btn-icon-left">🔄</span>
                        Download Another Video
                    </button>
                </div>
                <!-- Result Ad Space (300x250) -->
                <div class="ad-native-result" id="adNativeResult">
                    <div class="ad-label-small">Advertisement</div>
                    <!-- Adsterra 300x250 Ad will be inserted here -->
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

        // ダウンロードカードの後に追加
        const downloadCard = document.querySelector('.download-card');
        downloadCard.parentNode.insertBefore(resultDiv, downloadCard.nextSibling);

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

            // プレースホルダーを更新
            const placeholders = {
                video: 'TikTokの動画URLをここに貼り付け...',
                audio: 'TikTokのURLをここに貼り付け (MP3抽出)...',
                slide: 'TikTokのスライドショーURLをここに貼り付け...'
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
    themeToggle.addEventListener('click', () => {
        const themeIcon = themeToggle.querySelector('.theme-icon');
        const isLight = document.body.classList.toggle('light-mode');

        if (isLight) {
            themeIcon.textContent = '☀️';
            localStorage.setItem('theme', 'light');
            showNotification('Switched to Light Mode', 'info');
        } else {
            themeIcon.textContent = '🌙';
            localStorage.setItem('theme', 'dark');
            showNotification('Switched to Dark Mode', 'info');
        }
    });

    // Apply saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        themeToggle.querySelector('.theme-icon').textContent = '☀️';
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
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            downloadBtn.click();
        }
    });
});

