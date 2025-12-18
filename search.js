// ========================================
// TikGrab - Platform Search & Filter
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('platformSearch');
    const platformsGrid = document.getElementById('platformsGrid');
    const categoryFilters = document.querySelectorAll('.category-filter');
    const noResults = document.getElementById('noResults');

    if (!searchInput || !platformsGrid) return;

    let currentCategory = 'all';

    // Search functionality
    searchInput.addEventListener('input', (e) => {
        filterPlatforms(e.target.value.toLowerCase(), currentCategory);
    });

    // Category filter
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', () => {
            categoryFilters.forEach(f => f.classList.remove('active'));
            filter.classList.add('active');
            currentCategory = filter.dataset.category;
            filterPlatforms(searchInput.value.toLowerCase(), currentCategory);
        });
    });

    function filterPlatforms(searchTerm, category) {
        const cards = platformsGrid.querySelectorAll('.platform-card');
        let visibleCount = 0;

        cards.forEach(card => {
            const name = (card.dataset.name || card.textContent).toLowerCase();
            const cardCategory = card.dataset.category || 'social';

            const matchesSearch = name.includes(searchTerm);
            const matchesCategory = category === 'all' || cardCategory === category;

            if (matchesSearch && matchesCategory) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Show/hide no results message
        if (noResults) {
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    }

    // Keyboard shortcut: / to focus search
    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
        if (e.key === 'Escape' && document.activeElement === searchInput) {
            searchInput.value = '';
            filterPlatforms('', currentCategory);
            searchInput.blur();
        }
    });
});
