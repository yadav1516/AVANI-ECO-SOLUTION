document.addEventListener('DOMContentLoaded', () => {
    // Initialize AOS
    AOS.init({
        duration: 800,
        once: true
    });

    // Header Scroll Effect
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Mobile Menu Logic
    const mobileToggle = document.querySelector('.mobile-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const overlay = document.querySelector('.mobile-menu-overlay');
    const closeMenu = document.querySelector('.close-menu');

    function toggleMenu() {
        mobileMenu.classList.toggle('active');
        overlay.classList.toggle('active');
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    }

    if (mobileToggle) mobileToggle.addEventListener('click', toggleMenu);
    if (closeMenu) closeMenu.addEventListener('click', toggleMenu);
    if (overlay) overlay.addEventListener('click', toggleMenu);

    // Project Filtering Logic
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    const zoneSelect = document.getElementById('zoneSelect');

    function filterProjects() {
        const activeBtn = document.querySelector('.filter-btn.active');
        const categoryFilter = activeBtn ? activeBtn.getAttribute('data-filter') : 'all';
        const zoneFilter = zoneSelect ? zoneSelect.value : 'all';

        projectCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            const cardZone = card.getAttribute('data-zone');

            const categoryMatch = categoryFilter === 'all' || cardCategory === categoryFilter;
            const zoneMatch = zoneFilter === 'all' || cardZone === zoneFilter;

            if (categoryMatch && zoneMatch) {
                card.style.display = 'block';
                // Add animation
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.transition = 'all 0.4s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 50);
            } else {
                card.style.display = 'none';
            }
        });
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            btn.classList.add('active');
            filterProjects();
        });
    });

    if (zoneSelect) {
        zoneSelect.addEventListener('change', filterProjects);
    }
});

function openLeadForm() {
    // Reusing the logic from other pages, ideally this should be a shared script
    // For now, just a placeholder or simple alert if the modal isn't present
    const modal = document.getElementById('leadModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    } else {
        alert("Contact form opening...");
    }
}

function closeLeadForm() {
    const modal = document.getElementById('leadModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}
