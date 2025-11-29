document.addEventListener('DOMContentLoaded', () => {
    // Initialize AOS Animation Library
    AOS.init({
        duration: 1000,
        once: true,
        offset: 100,
        easing: 'ease-out-cubic'
    });

    // Preloader
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                preloader.classList.add('fade-out');
                setTimeout(() => {
                    preloader.style.display = 'none';
                }, 500);
            }, 1500);
        });
    }

    // Mobile Menu
    const mobileToggle = document.querySelector('.mobile-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const overlay = document.querySelector('.mobile-menu-overlay');
    const closeMenu = document.querySelector('.close-menu');
    const mobileLinks = document.querySelectorAll('.mobile-nav-links a');

    function toggleMenu() {
        mobileMenu.classList.toggle('active');
        overlay.classList.toggle('active');
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    }

    mobileToggle.addEventListener('click', toggleMenu);
    closeMenu.addEventListener('click', toggleMenu);
    overlay.addEventListener('click', toggleMenu);

    mobileLinks.forEach(link => {
        link.addEventListener('click', toggleMenu);
    });

    // Header Scroll Effect
    const header = document.querySelector('.header');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }, { passive: true });

    // Active Link Highlighting with IntersectionObserver
    const sections = document.querySelectorAll('section');

    const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -70% 0px', // Trigger when section is near top
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                if (id) {
                    navLinks.forEach(link => {
                        link.classList.remove('active');
                        if (link.getAttribute('href').includes(id)) {
                            link.classList.add('active');
                        }
                    });
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });

    // Expanding Cards (Services)
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            cards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
        });
    });

    // Impact Dashboard Counters
    const impactSection = document.querySelector('.impact-dashboard');
    const impactCounters = document.querySelectorAll('.impact-number');
    let impactStarted = false;

    const startImpactCounters = () => {
        impactCounters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const duration = 2500;
            const increment = target / (duration / 16);

            let current = 0;
            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.innerText = Math.ceil(current).toLocaleString();
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.innerText = target.toLocaleString() + '+';
                }
            };
            updateCounter();
        });
    };

    if (impactSection) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !impactStarted) {
                startImpactCounters();
                impactStarted = true;
            }
        }, { threshold: 0.5 });
        observer.observe(impactSection);
    }

    // Solar Calculator Logic
    const billInput = document.getElementById('billAmount');
    const areaInput = document.getElementById('roofArea');
    const billValue = document.getElementById('billValue');
    const areaValue = document.getElementById('areaValue');
    const systemSize = document.getElementById('systemSize');
    const annualSavings = document.getElementById('annualSavings');
    const co2Saved = document.getElementById('co2Saved');

    function calculateSolar() {
        const bill = parseInt(billInput.value);
        const area = parseInt(areaInput.value);

        // Update UI values
        billValue.innerText = bill;
        areaValue.innerText = area;

        // Simple Logic: 1kW requires ~100 sqft and saves ~Rs. 12000/year
        // System size based on bill (approx Rs. 8/unit, 4 units/kW/day)
        // Or based on area constraint

        // Calculate recommended size based on bill
        const unitsNeeded = bill / 8; // Monthly units
        const kwNeeded = unitsNeeded / (4 * 30); // kW needed

        // Calculate max size based on area
        const maxKwArea = area / 100;

        // Final recommended size (limited by area)
        let recommendedKw = Math.min(kwNeeded, maxKwArea);
        recommendedKw = Math.round(recommendedKw * 10) / 10; // Round to 1 decimal
        if (recommendedKw < 1) recommendedKw = 1;

        // Calculate Savings
        const yearlyUnits = recommendedKw * 4 * 365;
        const savings = Math.round(yearlyUnits * 8);
        const co2 = Math.round(yearlyUnits * 0.82 / 1000); // 0.82kg CO2 per unit
        const carKm = Math.round(co2 * 1000 / 0.12); // Approx 0.12kg CO2 per km for a car

        // Update Results
        systemSize.innerText = recommendedKw + ' kW';
        annualSavings.innerText = savings.toLocaleString();
        co2Saved.innerText = co2;
        document.getElementById('carKm').innerText = carKm.toLocaleString();
    }

    if (billInput && areaInput) {
        billInput.addEventListener('input', calculateSolar);
        areaInput.addEventListener('input', calculateSolar);
        // Initial calc
        calculateSolar();
    }

    // Lead Modal Logic
    window.openLeadForm = function () {
        document.getElementById('leadModal').classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    window.closeLeadForm = function () {
        document.getElementById('leadModal').classList.remove('active');
        document.body.style.overflow = '';
    }

    window.nextStep = function (step) {
        document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
        document.getElementById('step' + step).classList.add('active');
    }

    // Close modal on outside click
    document.getElementById('leadModal').addEventListener('click', (e) => {
        if (e.target === document.getElementById('leadModal')) {
            closeLeadForm();
        }
    });

    // Project Filters (Index Page)
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectItems = document.querySelectorAll('.project-card'); // Updated selector to match new class

    // Function to filter projects
    function filterProjects(filterValue) {
        projectItems.forEach(item => {
            const hasClass = item.classList.contains(filterValue);
            const categoryAttr = item.getAttribute('data-category');

            if (filterValue === 'all' || hasClass || categoryAttr === filterValue) {
                item.style.display = 'block';
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 50);
            } else {
                item.style.display = 'none';
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
            }
        });
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            projectItems.forEach(item => {
                // Check for category in classList (legacy) or data-category attribute
                const hasClass = item.classList.contains(filterValue);
                const categoryAttr = item.getAttribute('data-category');

                if (filterValue === 'all' || hasClass || categoryAttr === filterValue) {
                    item.style.display = 'block';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    }, 50);
                } else {
                    item.style.display = 'none';
                    item.style.opacity = '0';
                    item.style.transform = 'translateY(20px)';
                }
            });
        });
    });

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            faqItems.forEach(i => i.classList.remove('active'));
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Testimonial Tabs
window.showTestimonialTab = function (tabName) {
    // Hide all contents
    document.querySelectorAll('.testimonial-content').forEach(content => {
        content.classList.remove('active');
    });

    // Deactivate all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected content
    if (tabName === 'video') {
        document.getElementById('video-testimonials').classList.add('active');
        document.querySelector('.tab-btn:nth-child(1)').classList.add('active');
    } else {
        document.getElementById('client-testimonials').classList.add('active');
        document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
    }
}


// Counter Animation
document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.counter');
    const speed = 200; // The lower the slower

    const animateCounters = () => {
        counters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                const count = +counter.innerText;
                const inc = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + inc);
                    setTimeout(updateCount, 20);
                } else {
                    counter.innerText = target;
                }
            };
            // Reset to 0 before starting animation
            counter.innerText = '0';
            updateCount();
        });
    };

    // Trigger animation when section is in view
    let counterSection = document.querySelector('.achievements-section');
    if (counterSection) {
        let options = {
            rootMargin: '0px',
            threshold: 0.3
        }
        let observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, options);
        observer.observe(counterSection);
    }
});
