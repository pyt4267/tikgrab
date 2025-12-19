/**
 * TikGrab - Theme Script (Dark Mode Only)
 * Theme toggle removed - always dark mode
 */

// Ensure dark mode is always active
document.addEventListener('DOMContentLoaded', function () {
    // Remove any light-mode class if it exists
    document.body.classList.remove('light-mode');
    // Clear any saved theme preference
    localStorage.removeItem('theme');
});
