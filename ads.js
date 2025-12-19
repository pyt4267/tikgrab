/**
 * TikGrab - Ad Integration Script
 * Supports: PropellerAds, Adsterra, PopAds
 * Reference: TubeOffline ad placement style
 */

(function () {
    'use strict';

    // Ad Configuration - Replace with your actual ad codes
    const AD_CONFIG = {
        propellerAds: {
            enabled: true,
            zoneId: 'YOUR_PROPELLER_ZONE_ID', // Replace with your PropellerAds zone ID
            scriptUrl: '//pl20888138.profitablegatecpm.com/YOUR_ID.js' // Replace with your script
        },
        adsterra: {
            enabled: true,
            key: 'YOUR_ADSTERRA_KEY', // Replace with your Adsterra key
            bannerId: 'YOUR_BANNER_ID'
        },
        popAds: {
            enabled: true,
            siteId: 'YOUR_POPADS_SITE_ID' // Replace with your PopAds site ID
        }
    };

    // Create ad containers
    function createAdContainer(position, className) {
        const container = document.createElement('div');
        container.className = `ad-container ad-${position} ${className || ''}`;
        container.innerHTML = `
            <div class="ad-wrapper">
                <span class="ad-label">Advertisement</span>
                <div class="ad-content" id="ad-${position}"></div>
            </div>
        `;
        return container;
    }

    // Insert ad placeholders
    function insertAdContainers() {
        // Header Ad (below navigation)
        const header = document.querySelector('.header');
        if (header) {
            const headerAd = createAdContainer('header', 'ad-banner');
            header.after(headerAd);
        }

        // Content Ad (between sections)
        const featuresSection = document.querySelector('.features-premium, .platform-features');
        if (featuresSection) {
            const contentAd = createAdContainer('content', 'ad-rectangle');
            featuresSection.before(contentAd);
        }

        // Sidebar Ads (for desktop)
        if (window.innerWidth > 1200) {
            const main = document.querySelector('main');
            if (main) {
                const leftSidebar = createAdContainer('sidebar-left', 'ad-sidebar');
                const rightSidebar = createAdContainer('sidebar-right', 'ad-sidebar');
                main.appendChild(leftSidebar);
                main.appendChild(rightSidebar);
            }
        }

        // Footer Ad (above footer)
        const footer = document.querySelector('.footer');
        if (footer) {
            const footerAd = createAdContainer('footer', 'ad-banner');
            footer.before(footerAd);
        }
    }

    // Load PropellerAds
    function loadPropellerAds() {
        if (!AD_CONFIG.propellerAds.enabled) return;

        // Native Banner
        const script = document.createElement('script');
        script.async = true;
        script.dataset.cfasync = 'false';
        script.src = AD_CONFIG.propellerAds.scriptUrl;
        document.head.appendChild(script);
    }

    // Load Adsterra
    function loadAdsterra() {
        if (!AD_CONFIG.adsterra.enabled) return;

        // Social Bar or Banner
        const adSlots = document.querySelectorAll('.ad-content');
        adSlots.forEach((slot, index) => {
            if (index % 2 === 0) { // Alternate ad networks
                const script = document.createElement('script');
                script.async = true;
                script.src = `//www.topcreativeformat.com/${AD_CONFIG.adsterra.key}/invoke.js`;
                slot.appendChild(script);
            }
        });
    }

    // Load PopAds (interstitial/popunder)
    function loadPopAds() {
        if (!AD_CONFIG.popAds.enabled) return;

        const script = document.createElement('script');
        script.async = true;
        script.src = '//c.popads.net/shpop.js';
        document.head.appendChild(script);

        // PopAds configuration
        window.popAdsDelay = 3000; // 3 second delay
    }

    // Initialize Ads
    function initAds() {
        // Only load ads on non-localhost
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            console.log('Ads disabled on localhost');
            // Show placeholder ads for development
            document.querySelectorAll('.ad-content').forEach(slot => {
                slot.innerHTML = '<div style="background: rgba(255,255,255,0.05); padding: 20px; text-align: center; color: #666; border-radius: 8px;">Ad Space</div>';
            });
            return;
        }

        loadPropellerAds();
        loadAdsterra();
        loadPopAds();
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            insertAdContainers();
            initAds();
        });
    } else {
        insertAdContainers();
        initAds();
    }
})();
