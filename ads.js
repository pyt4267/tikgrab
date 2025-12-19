/**
 * TikGrab - Ad Integration Script v2.0
 * Features:
 * - Timed Modal Ad (5 seconds after page load)
 * - Download Click Overlay Ad
 * - Sticky Footer Ad
 * - Native Inline Ads
 */

(function () {
    'use strict';

    // ========================================
    // Configuration (Optimized - Multitag Only)
    // ========================================
    const AD_CONFIG = {
        // Timing settings - Modal and Download Overlay DISABLED
        modalDelay: 15000,
        modalCooldown: 1800000,
        downloadAdDelay: 3,

        // DISABLED - Only Multitag enabled
        modalAdEnabled: false, // Modal popup disabled
        downloadAdEnabled: false, // Download overlay disabled

        // Ad network settings
        adsterra: {
            enabled: false, // Adsterra disabled
            key: ''
        },
        propellerads: {
            enabled: true, // Only Multitag enabled (in HTML)
            zoneId: '10350749'
        },

        // Show mock ads on localhost for testing layout
        showMockAds: false // Disabled
    };

    // ========================================
    // Mock Social Bar Ad for localhost testing
    // ========================================
    function createMockSocialBar() {
        if (!AD_CONFIG.showMockAds) return;

        const mockAd = document.createElement('div');
        mockAd.id = 'mockSocialBar';
        mockAd.innerHTML = `
            <div style="
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                padding: 15px 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9998;
                box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.5);
            ">
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 12px 30px;
                    border-radius: 8px;
                    color: white;
                    font-weight: 600;
                    font-size: 14px;
                    text-align: center;
                    cursor: pointer;
                " onclick="this.parentElement.parentElement.remove()">
                    🎁 Special Offer - Click Here!
                </div>
            </div>
        `;
        document.body.appendChild(mockAd);
    }

    // ========================================
    // Modal Popup Ad - DISABLED
    // ========================================
    function createModalAd() {
        // Disabled - using Multitag instead
        return;

        const modal = document.createElement('div');
        modal.id = 'adModal';
        modal.className = 'ad-modal';
        modal.innerHTML = `
            <div class="ad-modal-overlay"></div>
            <div class="ad-modal-content" style="padding: 0; background: transparent; border: none; box-shadow: none;">
                <div id="propellerAdContainer"></div>
            </div>
        `;

        document.body.appendChild(modal);

        // Load PropellerAds In-Page Push
        const propellerScript = document.createElement('script');
        propellerScript.innerHTML = "(function(s){s.dataset.zone='10350749',s.src='https://nap5k.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))";
        document.getElementById('propellerAdContainer').appendChild(propellerScript);

        // Close on overlay click
        modal.querySelector('.ad-modal-overlay').addEventListener('click', function () {
            modal.classList.add('closing');
            setTimeout(() => modal.remove(), 300);
            localStorage.setItem('tikgrab_modal_shown', Date.now().toString());
        });

        // Show with animation
        requestAnimationFrame(() => modal.classList.add('visible'));
    }

    // ========================================
    // Download Click Overlay Ad
    // ========================================
    function createDownloadOverlayAd(callback) {
        const delay = AD_CONFIG.downloadAdDelay;
        const overlay = document.createElement('div');
        overlay.id = 'downloadAdOverlay';
        overlay.className = 'download-ad-overlay';
        overlay.innerHTML = `
            <div class="download-ad-content">
                <div class="download-ad-header">
                    <div class="download-ad-timer" id="adTimer">
                        <span id="timerCount">${delay}</span>秒後にダウンロード開始
                    </div>
                </div>
                <div class="download-ad-body" id="downloadAdContent">
                    <!-- PropellerAds In-Page Push -->
                    <div id="downloadPropellerAd"></div>
                </div>
                <button class="download-ad-skip" id="skipAdBtn" disabled>
                    スキップまで <span id="skipTimer">${delay}</span>秒
                </button>
            </div>
        `;

        document.body.appendChild(overlay);

        // Load PropellerAds In-Page Push for download overlay
        const propellerScript = document.createElement('script');
        propellerScript.innerHTML = "(function(s){s.dataset.zone='10350749',s.src='https://nap5k.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))";
        document.getElementById('downloadPropellerAd').appendChild(propellerScript);

        // Countdown timer (use config value)
        let countdown = AD_CONFIG.downloadAdDelay;
        const timerCount = document.getElementById('timerCount');
        const skipTimer = document.getElementById('skipTimer');
        const skipBtn = document.getElementById('skipAdBtn');

        const timer = setInterval(() => {
            countdown--;
            timerCount.textContent = countdown;
            skipTimer.textContent = countdown;

            if (countdown <= 0) {
                clearInterval(timer);
                skipBtn.innerHTML = '✓ ダウンロード開始中...';
                skipBtn.classList.add('ready');

                // Auto-start download after countdown
                setTimeout(() => {
                    overlay.classList.add('closing');
                    setTimeout(() => {
                        overlay.remove();
                        if (callback) callback();
                    }, 300);
                }, 500);
            }
        }, 1000);

        // Skip/Continue button (manual click also works)
        skipBtn.addEventListener('click', function () {
            if (countdown <= 0) {
                overlay.classList.add('closing');
                setTimeout(() => {
                    overlay.remove();
                    if (callback) callback();
                }, 300);
            }
        });

        // Show with animation
        requestAnimationFrame(() => overlay.classList.add('visible'));
    }

    // ========================================
    // Add Styles
    // ========================================
    function addAdStyles() {
        if (document.getElementById('adModalStyles')) return;

        const style = document.createElement('style');
        style.id = 'adModalStyles';
        style.textContent = `
            /* Modal Ad Styles */
            .ad-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .ad-modal.visible {
                opacity: 1;
                visibility: visible;
            }
            
            .ad-modal.closing {
                opacity: 0;
            }
            
            .ad-modal-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(5px);
            }
            
            .ad-modal-content {
                position: relative;
                background: var(--bg-secondary, #12121a);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                max-width: 500px;
                width: 90%;
                overflow: hidden;
                transform: scale(0.9);
                transition: transform 0.3s ease;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            }
            
            .ad-modal.visible .ad-modal-content {
                transform: scale(1);
            }
            
            .ad-modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 16px;
                background: rgba(255, 255, 255, 0.05);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .ad-modal-label {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.5);
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .ad-modal-close {
                width: 32px;
                height: 32px;
                border: none;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 20px;
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                justify-content: center;
                align-items: center;
                transition: all 0.2s ease;
            }
            
            .ad-modal-close:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: scale(1.1);
            }
            
            .ad-modal-body {
                padding: 24px;
                min-height: 280px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            /* Download Overlay Ad Styles */
            .download-ad-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10001;
                display: flex;
                justify-content: center;
                align-items: center;
                background: rgba(0, 0, 0, 0.9);
                backdrop-filter: blur(10px);
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .download-ad-overlay.visible {
                opacity: 1;
                visibility: visible;
            }
            
            .download-ad-overlay.closing {
                opacity: 0;
            }
            
            .download-ad-content {
                background: var(--bg-secondary, #12121a);
                border: 1px solid rgba(0, 245, 255, 0.2);
                border-radius: 20px;
                max-width: 600px;
                width: 95%;
                overflow: hidden;
                box-shadow: 0 0 60px rgba(0, 245, 255, 0.1);
            }
            
            .download-ad-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 16px 20px;
                background: linear-gradient(135deg, rgba(0, 245, 255, 0.1), rgba(255, 0, 229, 0.1));
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .download-ad-timer {
                color: var(--neon-cyan, #00f5ff);
                font-weight: 600;
                font-size: 14px;
            }
            
            .download-ad-timer #timerCount {
                display: inline-block;
                width: 20px;
                height: 20px;
                background: var(--neon-cyan, #00f5ff);
                color: #000;
                border-radius: 50%;
                text-align: center;
                line-height: 20px;
                margin-right: 4px;
            }
            
            .download-ad-body {
                padding: 32px;
                min-height: 300px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .download-ad-skip {
                display: block;
                width: 100%;
                padding: 16px;
                border: none;
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.5);
                font-size: 16px;
                font-weight: 600;
                cursor: not-allowed;
                transition: all 0.3s ease;
            }
            
            .download-ad-skip.ready {
                background: linear-gradient(135deg, var(--neon-cyan, #00f5ff), var(--neon-green, #22c55e));
                color: #000;
                cursor: pointer;
            }
            
            .download-ad-skip.ready:hover {
                transform: scale(1.02);
            }
            
            /* Ad Placeholder Styles */
            .ad-placeholder-content,
            .ad-placeholder-large {
                text-align: center;
                padding: 32px;
            }
            
            .ad-placeholder-icon {
                font-size: 48px;
                margin-bottom: 16px;
            }
            
            .ad-placeholder-text {
                font-size: 18px;
                font-weight: 600;
                color: var(--text-primary, #fff);
                margin-bottom: 8px;
            }
            
            .ad-placeholder-subtext {
                font-size: 14px;
                color: var(--text-muted, rgba(255, 255, 255, 0.5));
            }
            
            .ad-placeholder-large .ad-placeholder-icon {
                font-size: 64px;
            }
            
            .ad-placeholder-large .ad-placeholder-text {
                font-size: 24px;
            }
            
            /* Light mode */
            body.light-mode .ad-modal-content,
            body.light-mode .download-ad-content {
                background: #fff;
                border-color: rgba(0, 0, 0, 0.1);
            }
            
            body.light-mode .ad-modal-header,
            body.light-mode .download-ad-header {
                background: rgba(0, 0, 0, 0.05);
            }
            
            body.light-mode .ad-placeholder-text {
                color: #000;
            }
        `;

        document.head.appendChild(style);
    }

    // ========================================
    // Intercept Download Clicks
    // ========================================
    function setupDownloadInterception() {
        if (!AD_CONFIG.downloadAdEnabled) return;

        // Store original download function
        const originalDownloadWithProxy = window.downloadWithProxy;

        // Override download function
        window.downloadWithProxy = function (url, filename) {
            // Check if ad was shown recently
            const lastDownloadAd = localStorage.getItem('tikgrab_download_ad');
            const showAd = !lastDownloadAd || Date.now() - parseInt(lastDownloadAd) > 60000; // 1 minute cooldown

            if (showAd) {
                createDownloadOverlayAd(() => {
                    localStorage.setItem('tikgrab_download_ad', Date.now().toString());
                    // Call original function
                    if (originalDownloadWithProxy) {
                        originalDownloadWithProxy(url, filename);
                    } else {
                        // Fallback: redirect to download URL
                        window.location.href = `/.netlify/functions/download?url=${encodeURIComponent(url)}&filename=${encodeURIComponent(filename)}`;
                    }
                });
            } else {
                // No ad, direct download
                if (originalDownloadWithProxy) {
                    originalDownloadWithProxy(url, filename);
                } else {
                    window.location.href = `/.netlify/functions/download?url=${encodeURIComponent(url)}&filename=${encodeURIComponent(filename)}`;
                }
            }
        };
    }

    // ========================================
    // Initialize
    // ========================================
    function init() {
        addAdStyles();

        // Show mock Social Bar on localhost (if enabled)
        if (AD_CONFIG.showMockAds) {
            createMockSocialBar();
        }

        // Show modal ad after delay (if enabled)
        if (AD_CONFIG.modalAdEnabled) {
            setTimeout(() => {
                // Only show on main page, not on download pages
                if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
                    createModalAd();
                }
            }, AD_CONFIG.modalDelay);
        }

        // Setup download interception
        setupDownloadInterception();

        console.log('TikGrab Ads v2.0 initialized');
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
