    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    menuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
    // Highlight active link based on current page
    function highlightActiveLink() {
        const path = window.location.pathname;
        const links = {
            dashboard: ['nav-dashboard', 'nav-dashboard-mobile'],
            transactions: ['nav-transactions', 'nav-transactions-mobile'],
            reports: ['nav-reports', 'nav-reports-mobile']
        };
        let activePage = 'dashboard'; // Default
        if (path.includes('transactions')) activePage = 'transactions';
        else if (path.includes('reports')) activePage = 'reports';
        // Remove active class from all
        Object.values(links).flat().forEach(id => {
            const el = document.getElementById(id);
            if (el) el.classList.remove('text-primary-500', 'dark:text-primary-400', 'font-semibold');
        });
                // Add active class to current page links
        links[activePage].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.classList.add('text-primary-500', 'dark:text-primary-400', 'font-semibold');
        });
    }
    // Run on page load
    highlightActiveLink();
