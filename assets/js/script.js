document.addEventListener('DOMContentLoaded', () => {
    // Initialize AOS Animation Library
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100,
            easing: 'ease-out-cubic'
        });
    }

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

    // Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const closeMenu = document.querySelector('.close-menu');
    const overlay = document.querySelector('.mobile-menu-overlay');

    function openMenu() {
        mobileMenu.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenuFunc() {
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (mobileToggle) mobileToggle.addEventListener('click', openMenu);
    if (closeMenu) closeMenu.addEventListener('click', closeMenuFunc);
    if (overlay) overlay.addEventListener('click', closeMenuFunc);

    const mobileLinks = document.querySelectorAll('.mobile-nav-links a');
    mobileLinks.forEach(link => link.addEventListener('click', closeMenuFunc));


    /* ===========================
       Lead Generation Modal Logic
       =========================== */
    const leadModal = document.getElementById('leadModal');
    // Only run if modal exists on this page (index.html)
    if (leadModal) {
        const closeModalBtn = leadModal.querySelector('.close-modal');
        // Initial Flex setup to allow display:flex behavior via class
        leadModal.style.display = 'flex';

        // Auto-show logic: Wait for preloader (2000ms) or show instantly if no preloader
        const hasPreloader = document.querySelector('.preloader');
        const delay = hasPreloader ? 2500 : 500;

        setTimeout(() => {
            leadModal.classList.add('show');
        }, delay);

        // Close on 'X' click
        if (closeModalBtn) {
            closeModalBtn.addEventListener('click', () => {
                leadModal.classList.remove('show');
                setTimeout(() => {
                    leadModal.style.display = 'none';
                }, 400);
            });
        }

        // Close on outside click
        window.addEventListener('click', (e) => {
            if (e.target === leadModal) {
                leadModal.classList.remove('show');
                setTimeout(() => {
                    leadModal.style.display = 'none';
                }, 400);
            }
        });

        // Handle Form Submit (Prevent Reset for demo)
        const leadForm = document.getElementById('leadForm');
        if (leadForm) {
            leadForm.addEventListener('submit', (e) => {
                e.preventDefault();
                alert('Thank you! We will contact you shortly.');
                leadModal.classList.remove('show');
                setTimeout(() => {
                    leadModal.style.display = 'none';
                }, 400);
            });
        }
    }

    // Header Scroll Effect
    const header = document.querySelector('.header');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        if (header) {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
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

    /* ===========================
       Impact Dashboard Counters
       =========================== */
    const impactSection = document.querySelector('.impact-dashboard');
    const impactCounters = document.querySelectorAll('.impact-number');
    let impactStarted = false;

    const startImpactCounters = () => {
        if (impactStarted) return;
        impactStarted = true;

        impactCounters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const duration = 2000;
            const increment = Math.ceil(target / (duration / 20));

            let current = 0;
            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.innerText = current.toLocaleString();
                    setTimeout(updateCounter, 20);
                } else {
                    counter.innerText = target.toLocaleString() + '+';
                }
            };
            updateCounter();
        });
    };

    if (impactSection) {
        // Robust Trigger: Overlapping check + Visibility check
        const impactObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                // Trigger if *any* part is visible
                if (entry.isIntersecting) {
                    startImpactCounters();
                    impactObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 }); // 10% visible

        impactObserver.observe(impactSection);

        // Fallback: Check visibility on load (in case already in view)
        setTimeout(() => {
            const rect = impactSection.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom >= 0) {
                startImpactCounters();
            }
        }, 500);
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
        if (!billInput || !areaInput) return; // Guard clause
        const bill = parseInt(billInput.value);
        const area = parseInt(areaInput.value);

        // Update UI values
        if (billValue) billValue.innerText = bill;
        if (areaValue) areaValue.innerText = area;

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
        if (systemSize) systemSize.innerText = recommendedKw + ' kW';
        if (annualSavings) annualSavings.innerText = savings.toLocaleString();
        if (co2Saved) co2Saved.innerText = co2;
        if (document.getElementById('carKm')) document.getElementById('carKm').innerText = carKm.toLocaleString();
    }

    if (billInput && areaInput) {
        billInput.addEventListener('input', calculateSolar);
        areaInput.addEventListener('input', calculateSolar);
        // Initial calc
        calculateSolar();
    }

    // Lead Modal Helpers ( Global Scope required?)
    window.openLeadForm = function () {
        const lm = document.getElementById('leadModal');
        if (lm) {
            lm.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    window.closeLeadForm = function () {
        const lm = document.getElementById('leadModal');
        if (lm) {
            lm.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    // Project Filters
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectItems = document.querySelectorAll('.project-card');

    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filterValue = btn.getAttribute('data-filter');

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
            });
        });
    }

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                faqItems.forEach(i => i.classList.remove('active'));
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        }
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

    // Testimonial Tabs Logic (Modified to only show client testimonials)
    window.showTestimonialTab = function (tabName) {
        document.querySelectorAll('.testimonial-content').forEach(content => {
            content.classList.remove('active');
        });
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Always show client testimonials regardless of input, as video tab is removed
        const cTest = document.getElementById('client-testimonials');
        if (cTest) cTest.classList.add('active');
        const btn2 = document.querySelector('.tab-btn:nth-child(2)');
        if (btn2) btn2.classList.add('active');
    }

    /* ===========================
       Achievements Section Counters 
       (Separate from Impact Dashboard)
       =========================== */
    const achievementCounters = document.querySelectorAll('.counter');
    let achievementStarted = false; // Flag for this section

    const animateAchievementCounters = () => {
        if (achievementStarted) return;
        achievementStarted = true;

        achievementCounters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                const count = +counter.innerText;
                const speed = 200;
                const inc = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + inc);
                    setTimeout(updateCount, 20);
                } else {
                    counter.innerText = target;
                }
            };
            counter.innerText = '0';
            updateCount();
        });
    };

    let counterSection = document.querySelector('.achievements-section');
    if (counterSection) {
        let obs = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateAchievementCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        obs.observe(counterSection);
    }

    /* ===========================
       Apply Modal Logic (Careers)
       =========================== */
    window.openApplyForm = function (role) {
        const modal = document.getElementById('applyModal');
        const roleInput = document.getElementById('jobRole');
        const titleSpan = document.getElementById('jobTitleSpan');

        if (modal) {
            if (roleInput) roleInput.value = role;
            if (titleSpan) titleSpan.innerText = role;
            modal.classList.add('show');
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeApplyForm = function () {
        const modal = document.getElementById('applyModal');
        if (modal) {
            modal.classList.remove('show');
            setTimeout(() => {
                modal.style.display = 'none';
            }, 400);
            document.body.style.overflow = '';
        }
    };

    // File Input Name Update
    const fileInput = document.getElementById('resumeFile');
    const fileNameDisplay = document.getElementById('fileName');
    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                fileNameDisplay.innerText = this.files[0].name;
                fileNameDisplay.style.color = 'var(--primary-dark)';
            } else {
                fileNameDisplay.innerText = 'Click to Upload Resume';
            }
        });
    }

    // Apps Script WEb App URL
    const SCRIPT_URL = "https://script.google.com/macros/s/AKfycby1yiHO2DVO5zNnTbJFxRVPiyp61W7QBuKHNNnYEg6iZgg-tfiq7HNf5PcyUElN8gcE/exec";

    // Submssion Logic
    const applyForm = document.getElementById('applyForm');
    if (applyForm) {
        applyForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const submitBtn = this.querySelector('.btn-submit-lead');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = 'Uploading...';
            submitBtn.disabled = true;

            const file = fileInput.files[0];
            const reader = new FileReader();

            reader.onload = function (e) {
                const base64Data = e.target.result.split(',')[1]; // Remove header "data:application/pdf;base64,"

                const payload = {
                    user_info: {
                        role: document.getElementById('jobRole').value,
                        name: applyForm.querySelector('[name="user_name"]').value,
                        email: applyForm.querySelector('[name="user_email"]').value,
                        phone: applyForm.querySelector('[name="user_phone"]').value,
                        message: applyForm.querySelector('[name="message"]').value
                    },
                    file_data: {
                        name: file.name,
                        type: file.type,
                        base64: base64Data
                    }
                };

                fetch(SCRIPT_URL, {
                    method: 'POST',
                    mode: 'no-cors', // Important for Google Apps Script
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                })
                    .then(response => {
                        // With no-cors, we get an opaque response, so we assume success if no error thrown
                        alert('Application Sent Successfully!');
                        submitBtn.innerText = originalText;
                        submitBtn.disabled = false;
                        closeApplyForm();
                        applyForm.reset();
                        fileNameDisplay.innerText = 'Click to Upload Resume';
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Something went wrong. Please try again.');
                        submitBtn.innerText = originalText;
                        submitBtn.disabled = false;
                    });
            };

            if (file) {
                reader.readAsDataURL(file);
            } else {
                alert("Please select a file!");
                submitBtn.innerText = originalText;
                submitBtn.disabled = false;
            }
        });
    }


    /* ===========================
       Contact Form Logic (Contact Us Page)
       =========================== */
    const contactForm = document.getElementById('contactForm');
    const CONTACT_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxOG89Ag2dcwIbY66VRWVT9OF4hB8CLQEm1mnJKdbBvHByztLHkOx6jdV_NR1KcuC30vg/exec";

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = 'Sending...';
            submitBtn.disabled = true;

            const payload = {
                user_info: {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    subject: document.getElementById('subject').value,
                    message: document.getElementById('message').value
                }
            };

            fetch(CONTACT_SCRIPT_URL, {
                method: 'POST',
                mode: 'no-cors',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
                .then(response => {
                    alert('Message Sent Successfully! We will contact you soon.');
                    contactForm.reset();
                    submitBtn.innerText = originalText;
                    submitBtn.disabled = false;
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Something went wrong. Please try again.');
                    submitBtn.innerText = originalText;
                    submitBtn.disabled = false;
                });
        });
    }



    /* ===========================
       Consultation Form Logic (Consultation Page)
       =========================== */
    const consultForm = document.getElementById('consultForm');
    const CONSULT_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxcfro31APArChvMZQKKHvjNwdUJmPfjDhULn_VxOCNcWRM0wTTqu05zDX-CAUkwj2BEQ/exec";

    if (consultForm) {
        consultForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = 'Requesting...';
            submitBtn.disabled = true;

            // Combine inputs
            const fullName = (document.getElementById('firstName').value + ' ' + document.getElementById('lastName').value).trim();
            const propType = document.getElementById('propertyType').value;
            // As backend expects 'message', we'll pass PropertyType there

            const payload = {
                user_info: {
                    name: fullName,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    city: document.getElementById('city').value,
                    load: document.getElementById('billAmount').value,
                    message: "Property Type: " + propType // Mapping property type to message
                }
            };

            fetch(CONSULT_SCRIPT_URL, {
                method: 'POST',
                mode: 'no-cors',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
                .then(response => {
                    alert('Quote Request Sent! We will get back to you with a solar plan.');
                    consultForm.reset();
                    submitBtn.innerText = originalText;
                    submitBtn.disabled = false;
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Something went wrong. Please try again.');
                    submitBtn.innerText = originalText;
                    submitBtn.disabled = false;
                });
        });
    }

});
