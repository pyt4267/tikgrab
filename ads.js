/**
 * TikGrab Ad Network Manager
 * Manages PropellerAds, Adsterra, and PopAds integration
 * 
 * SETUP INSTRUCTIONS:
 * 1. Register at each ad network:
 *    - PropellerAds: https://propellerads.com
 *    - Adsterra: https://adsterra.com
 *    - PopAds: https://popads.net
 * 2. Get your publisher IDs and ad codes
 * 3. Replace the placeholder values below with your actual codes
 */

(function () {
    'use strict';

    // ============================================
    // CONFIGURATION - Replace with your actual IDs
    // ============================================
    const CONFIG = {
        // PropellerAds Configuration
        propellerAds: {
            enabled: true,
            publisherId: 'YOUR_PROPELLERADS_PUBLISHER_ID', // Replace this
            // Native Banner Zone ID
            nativeBannerZoneId: 'YOUR_NATIVE_BANNER_ZONE_ID',
            // Push Notifications Zone ID (optional)
            pushZoneId: 'YOUR_PUSH_ZONE_ID'
        },

        // Adsterra Configuration
        adsterra: {
            enabled: true,
            publisherId: 'YOUR_ADSTERRA_PUBLISHER_ID', // Replace this
            // Banner Zone IDs for different placements
            headerBannerKey: 'YOUR_HEADER_BANNER_KEY',
            contentBannerKey: 'YOUR_CONTENT_BANNER_KEY',
            footerBannerKey: 'YOUR_FOOTER_BANNER_KEY'
        },

        // PopAds Configuration
        popads: {
            enabled: true,
            publisherId: 'YOUR_POPADS_PUBLISHER_ID' // Replace this
        },

        // Global Settings
        settings: {
            // Delay before loading ads (ms) - helps with page speed
            loadDelay: 1000,
            // Show placeholder text before ads load
            showPlaceholders: true,
            // Enable console logging for debugging
            debug: false
        }
    };

    // ============================================
    // AD CONTAINER TEMPLATES
    // ============================================

    /**
     * Create a styled ad container
     */
    function createAdContainer(id, position) {
        const container = document.createElement('div');
        container.id = id;
        container.className = `ad-container ad-${position}`;
        container.setAttribute('data-ad-position', position);

        // Add placeholder content
        if (CONFIG.settings.showPlaceholders) {
            container.innerHTML = `
                <div class="ad-placeholder">
                    <span class="ad-label">Advertisement</span>
                </div>
            `;
        }

        return container;
    }

    // ============================================
    // PROPELLERADS INTEGRATION
    // ============================================

    function loadPropellerAds() {
        if (!CONFIG.propellerAds.enabled) return;

        log('Loading PropellerAds...');

        // Native Banner Script
        const script = document.createElement('script');
        script.async = true;
        script.setAttribute('data-cfasync', 'false');
        script.src = `//pl${CONFIG.propellerAds.publisherId}.profitablegatecpm.com/${CONFIG.propellerAds.nativeBannerZoneId}.js`;

        // Insert into content ad container
        const contentAd = document.getElementById('ad-content');
        if (contentAd) {
            contentAd.innerHTML = '';
            contentAd.appendChild(script);
        }

        log('PropellerAds loaded');
    }

    // ============================================
    // ADSTERRA INTEGRATION
    // ============================================

    function loadAdsterra() {
        if (!CONFIG.adsterra.enabled) return;

        log('Loading Adsterra...');

        // Header Banner
        loadAdsterraBanner('ad-header', CONFIG.adsterra.headerBannerKey, 728, 90);

        // Footer Banner
        loadAdsterraBanner('ad-footer', CONFIG.adsterra.footerBannerKey, 728, 90);

        log('Adsterra loaded');
    }

    function loadAdsterraBanner(containerId, key, width, height) {
        const container = document.getElementById(containerId);
        if (!container || !key || key.includes('YOUR_')) return;

        container.innerHTML = '';

        // Create script element for Adsterra
        const script = document.createElement('script');
        script.async = true;
        script.setAttribute('data-cfasync', 'false');
        script.src = `//www.highperformanceformat.com/${key}/invoke.js`;

        // Create ad container div
        const adDiv = document.createElement('div');
        adDiv.id = `container-${key}`;

        container.appendChild(adDiv);
        container.appendChild(script);
    }

    // ============================================
    // POPADS INTEGRATION (PopUnder)
    // ============================================

    function loadPopAds() {
        if (!CONFIG.popads.enabled) return;
        if (CONFIG.popads.publisherId.includes('YOUR_')) return;

        log('Loading PopAds...');

        // PopAds script
        const script = document.createElement('script');
        script.async = true;
        script.src = `//c1.popads.net/pop.js?key=${CONFIG.popads.publisherId}`;
        document.head.appendChild(script);

        log('PopAds loaded');
    }

    // ============================================
    // INITIALIZATION
    // ============================================

    function initAds() {
        log('Initializing TikGrab Ad Manager...');

        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', onDOMReady);
        } else {
            onDOMReady();
        }
    }

    function onDOMReady() {
        // Delay loading for better page performance
        setTimeout(function () {
            loadAdsterra();
            loadPropellerAds();
            loadPopAds();
            log('All ad networks initialized');
        }, CONFIG.settings.loadDelay);
    }

    // ============================================
    // UTILITY FUNCTIONS
    // ============================================

    function log(message) {
        if (CONFIG.settings.debug) {
            console.log('[TikGrab Ads]', message);
        }
    }

    // ============================================
    // ANTI-ADBLOCK DETECTION (Optional)
    // ============================================

    function checkAdBlock() {
        const testAd = document.createElement('div');
        testAd.innerHTML = '&nbsp;';
        testAd.className = 'adsbox';
        testAd.style.cssText = 'position:absolute;left:-10000px;';
        document.body.appendChild(testAd);

        setTimeout(function () {
            if (testAd.offsetHeight === 0) {
                // AdBlock detected - show friendly message
                showAdBlockMessage();
            }
            testAd.remove();
        }, 100);
    }

    function showAdBlockMessage() {
        const message = document.createElement('div');
        message.className = 'adblock-notice';
        message.innerHTML = `
            <div class="adblock-content">
                <span class="adblock-icon">💡</span>
                <p>We rely on ads to keep TikGrab free. Please consider disabling your ad blocker.</p>
                <button class="adblock-close">✕</button>
            </div>
        `;

        message.querySelector('.adblock-close').addEventListener('click', function () {
            message.remove();
        });

        document.body.appendChild(message);
    }

    // ============================================
    // START
    // ============================================

    // Initialize when script loads
    initAds();

    // Optional: Check for ad blockers after page load
    // window.addEventListener('load', checkAdBlock);

})();
