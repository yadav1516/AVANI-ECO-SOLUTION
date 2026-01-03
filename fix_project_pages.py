import os
import re

# The files to process
PROJECT_FILES = [
    'project-asahi.html',
    'project-dongkwang.html',
    'project-euro_safety.html',
    'project-lalru.html',
    'project-lodha.html',
    'project-nssi.html',
    'project-sharman.html',
    'project-smi.html',
    'project-sportking.html',
    'project-sportking_bhatinda_exp.html',
    'project-sportking_ludhiana.html',
    'project-st_export.html',
    'project-tkm.html',
    'project-waree.html',
    'project-welspun.html'
]

PROJECT_DIR = '/Users/avinash/Pareesan Services Pvt. Ltd./PAREESAN/'

# The Gold Standard Header HTML (Taken from projects.html)
HEADER_HTML = """    <!-- Header -->
    <header class="header">
        <div class="container header-container">
            <a href="index.html" class="logo" aria-label="Pareesan Home">
                <img src="assets/img/general/logo_nav.png" alt="Pareesan Services" class="logo-img">
            </a>

            <nav class="navbar">
                <ul class="nav-links">
                    <li class="nav-item has-dropdown">
                        <a href="about.html" class="nav-link">About Us</a>
                        <div class="dropdown-menu">
                            <a href="about.html" class="dropdown-item">Who We Are</a>
                            <a href="team.html" class="dropdown-item">Our Team</a>
                            <a href="clients.html" class="dropdown-item">Our Clients</a>
                            <a href="careers.html" class="dropdown-item">Careers</a>
                        </div>
                    </li>
                    <li class="nav-item has-dropdown">
                        <a href="solutions.html" class="nav-link">Services</a>
                        <div class="dropdown-menu">
                            <a href="solutions.html" class="dropdown-item">Our Solutions</a>
                            <a href="solar-epc.html" class="dropdown-item">Solar EPC</a>
                            <a href="installation.html" class="dropdown-item">Installation</a>
                            <a href="om-services.html" class="dropdown-item">O&M Services</a>
                        </div>
                    </li>
                    <li><a href="projects.html" class="nav-link">Projects</a></li>
                    <li><a href="catalogue.html" class="nav-link">Catalogue</a></li>
                    <li class="nav-item has-dropdown">
                        <a href="calc.html" class="nav-link">Calculators</a>
                        <div class="dropdown-menu">
                            <a href="calc.html" class="dropdown-item">Solar ROI Calculator</a>
                            <a href="load-calculator.html" class="dropdown-item">Load Calculator</a>
                        </div>
                    </li>
                    <li><a href="blog.html" class="nav-link">Blog</a></li>
                </ul>
            </nav>

            <div class="header-right">
                <a href="contact.html" class="btn btn-outline-dark header-btn">Contact Us</a>
                <a href="consultation.html" class="btn btn-primary header-btn pulse-btn">Get Free Consultation</a>
                <button class="mobile-toggle" aria-label="Open Menu">
                    <span class="bar"></span>
                    <span class="bar"></span>
                    <span class="bar"></span>
                </button>
            </div>
        </div>
    </header>

    <!-- Mobile Menu Overlay -->
    <div class="mobile-menu-overlay"></div>
    <div class="mobile-menu">
        <div class="mobile-menu-header">
            <!-- Logo Removed as per user request -->
            <button class="close-menu" aria-label="Close Menu"><i class="fas fa-times"></i></button>
        </div>
        <ul class="mobile-nav-links">
            <li class="mobile-dropdown">
                <a href="javascript:void(0)">About Us <i class="fas fa-chevron-down"></i></a>
                <ul class="mobile-submenu">
                    <li><a href="about.html">Who We Are</a></li>
                    <li><a href="team.html">Our Team</a></li>
                    <li><a href="clients.html">Our Clients</a></li>
                    <li><a href="careers.html">Careers</a></li>
                </ul>
            </li>
            <li class="mobile-dropdown">
                <a href="javascript:void(0)">Services <i class="fas fa-chevron-down"></i></a>
                <ul class="mobile-submenu">
                    <li><a href="solutions.html">Our Solutions</a></li>
                    <li><a href="solar-epc.html">Solar EPC</a></li>
                    <li><a href="installation.html">Installation</a></li>
                    <li><a href="om-services.html">O&M Services</a></li>
                </ul>
            </li>
            <li><a href="projects.html">Projects</a></li>
            <li><a href="catalogue.html">Catalogue</a></li>
            <li class="mobile-dropdown">
                <a href="javascript:void(0)">Calculators <i class="fas fa-chevron-down"></i></a>
                <ul class="mobile-submenu">
                    <li><a href="calc.html">Solar ROI Calculator</a></li>
                    <li><a href="load-calculator.html">Load Calculator</a></li>
                </ul>
            </li>
            <li><a href="blog.html">Blog</a></li>
        </ul>
        <div class="mobile-menu-actions">
            <a href="contact.html" class="btn btn-outline-dark btn-block mb-3"
                style="width: 100%; border-radius: 50px; text-align: center; display: block; margin-bottom: 15px;">Contact
                Us</a>
            <a href="consultation.html" class="btn btn-primary btn-block"
                style="width: 100%; border-radius: 50px; text-align: center; display: block;">Get Free Consultation</a>
        </div>
    </div>"""

# Footer Standard (Optional, but good for consistency)
FOOTER_HTML = """    <!-- Footer -->
    <footer id="contact" class="footer">
        <div class="container">
            <div class="footer-top">
                <div class="footer-brand">
                    <img src="assets/img/general/logo_transparent.png" alt="Pareesan" class="footer-logo">
                    <p>Pareesan Services Pvt Ltd is a leading Solar EPC company committed to quality, safety, and
                        sustainability.</p>
                    <div class="social-links">
                        <a href="https://www.facebook.com/profile.php?id=61563198731468" aria-label="Facebook"
                            target="_blank"><i class="fab fa-facebook-f"></i></a>
                        <a href="https://www.linkedin.com/company/pareesan-service-pvt-ltd/" aria-label="LinkedIn"
                            target="_blank"><i class="fab fa-linkedin-in"></i></a>
                        <a href="javascript:void(0)"><i class="fab fa-twitter"></i></a>
                        <a href="https://www.youtube.com/@PareesanServices" aria-label="YouTube" target="_blank"><i
                                class="fab fa-youtube"></i></a>
                        <a href="https://www.instagram.com/pareesan_services/" aria-label="Instagram" target="_blank"><i
                                class="fab fa-instagram"></i></a>
                    </div>
                </div>
                <div class="footer-links-group">
                    <div class="footer-col">
                        <h4>Company</h4>
                        <ul>
                            <li><a href="index.html#about">About Us</a></li>
                            <li><a href="careers.html">Careers</a></li>
                            <li><a href="blog.html">Blog</a></li>
                            <li><a href="partners.html">Partner With Us</a></li>
                            <li><a href="reviews.html">Reviews</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Solutions</h4>
                        <ul>
                            <li><a href="solar-epc.html">Solar EPC Services</a></li>
                            <li><a href="installation.html">Installation + BOS</a></li>
                            <li><a href="om-services.html">O&M Services</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Contact</h4>
                        <ul class="contact-info">
                            <li><i class="fas fa-map-marker-alt"></i> Unit no 401 4th floor, Erose garden, Suraj Kund
                                Rd, Charmwood Village, Faridabad, Haryana 121009</li>
                            <li><i class="fas fa-phone"></i> <strong>Phone:</strong> +91 9873886002</li>
                            <li><i class="fas fa-envelope"></i> <strong>Email:</strong> info@pareesan.com</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Pareesan Services Pvt Ltd. All Rights Reserved.</p>
            </div>
        </div>
    </footer>"""

def fix_file(filename):
    file_path = os.path.join(PROJECT_DIR, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Body Class
    if 'class="projects-page"' not in content:
        content = content.replace('<body>', '<body class="projects-page">')
    
    # 2. Replace Header and Mobile Menu
    # Regex to find everything from <header> to end of mobile menu div
    # This is tricky because mobile menu might be separate.
    # Strategy: Replace <header.../header> with NEW_HEADER.
    # Then remove old mobile-menu divs if they exist separately.
    
    # Simple Replace for Header
    header_pattern = re.compile(r'<header.*?</header>', re.DOTALL)
    content = header_pattern.sub(HEADER_HTML, content)

    # Remove old navbar/mobile menu overlapping trash if it exists immediately after header
    # We will just inject the header. The user's files have <div class="mobile-menu"> usually after header.
    # Let's try to find and replace the standard block of header + mobile menu if possible.
    # Given the variance, I'll rely on Replacing <header>... and then Cleaning up known mobile menu artifacts.
    
    mobile_menu_pattern = re.compile(r'<div class="mobile-menu-overlay">.*?<div class="mobile-menu">.*?</div>\s*</div>', re.DOTALL)
    # The pattern in project-lalru.html is:
    # <div class="mobile-menu-overlay"></div>
    # <div class="mobile-menu">...</div>
    
    # Let's brutally remove old mobile menu fragments to avoid duplicates, as HEADER_HTML includes them.
    content = re.sub(r'<div class="mobile-menu-overlay"></div>', '', content)
    # Remove the mobile menu container
    content = re.sub(r'<div class="mobile-menu">.*?</div>', '', content, flags=re.DOTALL)
    
    # Now, verify HEADER_HTML is intact. The regex replacement of header might have worked. 
    # But wait, HEADER_HTML *includes* the mobile menu.
    # So if I replaced <header> with HEADER_HTML, I have the menu.
    # But I need to make sure I didn't leave a DOUBLE menu.
    # Hence the removal steps above.

    # 3. Replace Footer
    footer_pattern = re.compile(r'<footer.*?</footer', re.DOTALL) # Match until closing tag start
    # This is risky with regex. Let's start with Header fix which is the main visual bug.
    
    # 4. Inject Script at bottom
    if '<script src="assets/js/script.js"></script>' not in content:
        content = content.replace('</body>', '<script src="assets/js/script.js"></script>\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {filename}")

def main():
    print("Starting Project Page Fix...")
    for file in PROJECT_FILES:
        fix_file(file)
    print("Done.")

if __name__ == "__main__":
    main()
