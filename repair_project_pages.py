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

# The Gold Standard Header HTML
CLEAN_HEADER_BLOCK = """
    <!-- Header -->
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
    </div>
"""

def repair_file(filename):
    file_path = os.path.join(PROJECT_DIR, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex Strategy:
    # 1. Match <body ...> (which we ensured is <body class="projects-page"> or just <body>)
    # 2. Match <div class="page-header"> (Start of unique content)
    # 3. Replace EVERYTHING in between with CLEAN_HEADER_BLOCK
    
    # Pattern: (<body.*?>)(.*?)(<div class="page-header">)
    # This will capture the body tag, the mess in between, and the start of page-header.
    # We replace with group(1) + CLEAN_HEADER_BLOCK + group(3).
    
    pattern = re.compile(r'(<body.*?>)(.*?)(<div class="page-header">)', re.DOTALL | re.IGNORECASE)
    
    match = pattern.search(content)
    if match:
        body_tag = match.group(1)
        # Ensure projects-page class
        if 'class="projects-page"' not in body_tag:
            body_tag = '<body class="projects-page">'
            
        new_content = pattern.sub(f'{body_tag}{CLEAN_HEADER_BLOCK}\n    <div class="page-header">', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Repaired: {filename}")
    else:
        print(f"Skipping (Pattern not found): {filename}")

def main():
    print("Starting Project Page Repair...")
    for file in PROJECT_FILES:
        repair_file(file)
    print("Done.")

if __name__ == "__main__":
    main()
