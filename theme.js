// ========================================
// TikGrab - テーマ切り替え（共通）
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');

    if (themeToggle) {
        const themeIcon = themeToggle.querySelector('.theme-icon');

        // 保存されたテーマを適用
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {
            document.body.classList.add('light-mode');
            if (themeIcon) themeIcon.textContent = '☀️';
        }

        // テーマ切り替え
        themeToggle.addEventListener('click', () => {
            const isLight = document.body.classList.toggle('light-mode');

            if (isLight) {
                if (themeIcon) themeIcon.textContent = '☀️';
                localStorage.setItem('theme', 'light');
            } else {
                if (themeIcon) themeIcon.textContent = '🌙';
                localStorage.setItem('theme', 'dark');
            }
        });
    }
});
